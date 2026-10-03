"""Session lifecycle: start, log, artifact, finish.

Active-session state lives in `activestate`, command capture in `recorder`, and
the git-versus-record comparison in `reconcile`.

Re-exported for callers, which should import from this module only:
`SessionError`, `OUTCOMES`, `STALE_HOURS`, `MAX_SLUG`, `ActiveSession`,
`load_active`, `require_active`, `elapsed`, `hours_since`, `slugify`,
`next_session_id`, `write_pointer`, `clear_pointer`, `reconcile`,
`doc_implications`.

Those names are imported below for that purpose and are not all used in this
file.
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

from . import events, gitutil, paths, secrets
from .activestate import (
    MAX_SLUG,
    OUTCOMES,
    STALE_HOURS,
    ActiveSession,
    SessionError,
    clear_pointer,
    elapsed,
    hours_since,
    load_active,
    next_session_id,
    require_active,
    slugify,
    write_pointer,
)
from .reconcile import doc_implications, reconcile



def start(goal: str, agent: str | None = None, task: str | None = None) -> ActiveSession:
    existing = load_active()
    if existing is not None:
        raise SessionError(
            f"session {existing.session} is already active (started {existing.started_at}); "
            "finish it or run 'tools/origin session status'"
        )
    if not goal.strip():
        raise SessionError("--goal must not be empty")
    git = gitutil.state()
    host, _ = gitutil.host_identity()
    session = next_session_id(goal)
    active = ActiveSession(
        session=session,
        goal=goal.strip(),
        agent=agent or _default_agent(),
        task=task or "",
        started_at=events.now_iso(),
        started_epoch=time.time(),
        start_head=git.head,
        branch=git.branch,
        host=host,
    )
    paths.ensure_dir(paths.session_dir(session))
    write_pointer(active)
    _refresh_reports(session)
    events.append(
        session,
        "session_start",
        {
            "goal": active.goal,
            "agent": active.agent,
            "task": active.task,
            "dirty_at_start": git.porcelain,
        },
        actor=active.agent,
        host=host,
        git={"head": git.head, "branch": git.branch},
    )
    return active


# Agent fingerprints, most specific first. Checked in order so a nested runner
# is not misreported as its parent.
AGENT_MARKERS = (
    ("opencode", ("OPENCODE_CALLER", "OPENCODE_PID")),
    ("claude", ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT")),
    ("codex", ("CODEX_SANDBOX", "CODEX_HOME", "CODEX_MANAGED_BY_NPM")),
    ("cursor", ("CURSOR_TRACE_ID",)),
    ("gemini", ("GEMINI_CLI", "GEMINI_SANDBOX")),
)


def _refresh_reports(session_id: str) -> None:
    """Keep the session report and index present from the moment of opening.

    Otherwise `sessions/INDEX.md` would link to a report that does not exist
    yet, and a broken link in a generated file is a lint failure.
    """
    from . import report

    report.regenerate_session(session_id)
    report.regenerate_sessions_index()


def _default_agent() -> str:
    """Best-effort identity of the agent runtime.

    Detection is a convenience for the record, never a security boundary. Set
    ORIGIN_AGENT to state it explicitly; VM runners should always do so.
    """
    explicit = _env("ORIGIN_AGENT")
    if explicit:
        return explicit.strip() or "unknown-agent"
    for name, markers in AGENT_MARKERS:
        if any(_env(marker) for marker in markers):
            return name
    argv0 = _sys_argv0()
    if "opencode" in argv0:
        return "opencode"
    if "claude" in argv0:
        return "claude"
    if "codex" in argv0:
        return "codex"
    return "unknown-agent"


def _sys_argv0() -> str:
    try:
        return Path(sys.argv[0]).resolve().as_posix().lower()
    except (OSError, IndexError):
        return ""


def _env(name: str) -> str:
    import os

    return os.environ.get(name, "")


def log(kind: str, summary: str, data: dict | None = None, **extra) -> events.Event:
    """Append an event to the active session."""
    active = require_active()
    payload = {"summary": summary}
    payload.update(data or {})
    return events.append(active.session, kind, payload, actor=active.agent, host=active.host, **extra)


def step(summary: str) -> events.Event:
    return log("milestone", summary)


def note(summary: str) -> events.Event:
    return log("note", summary)


def decision(summary: str, refs: list[str] | None = None) -> events.Event:
    return log("decision", summary, {"refs": refs or []})


def block(reason: str) -> events.Event:
    return log("block", reason)


def experiment_result(experiment: str, decision_text: str, refs: list[str] | None = None) -> events.Event:
    return log("experiment_result", decision_text, {"experiment": experiment, "refs": refs or []})


def artifact(path: str, note_text: str = "") -> events.Event:
    """Record a file the session produced, with its content hash.

    Refuses when a secret pattern matches: the file itself would become the
    exposure, and redacting it would corrupt the artifact.
    """
    active = require_active()
    target = Path(path)
    if not target.is_absolute():
        target = paths.repo_root() / target
    rel = _relative(target)
    if not target.exists():
        raise SessionError(f"artifact does not exist: {rel}")
    if target.is_dir():
        raise SessionError(f"artifact is a directory, record files individually: {rel}")
    found = secrets.scan_file(target)
    if found:
        events.append(
            active.session,
            "integrity_error",
            {
                "summary": f"refused artifact {rel}: secret pattern(s) {', '.join(found)}",
                "path": rel,
                "patterns": found,
                "action": "artifact-not-recorded",
            },
            actor=active.agent,
            host=active.host,
        )
        raise SessionError(
            f"refusing to record {rel}: matched secret pattern(s) {', '.join(found)}. "
            "Rotate the credential if it is real, remove it from the file, then re-run."
        )
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return events.append(
        active.session,
        "artifact",
        {
            "summary": note_text or f"wrote {rel}",
            "path": rel,
            "sha256": digest,
            "bytes": target.stat().st_size,
            "tracked": gitutil.is_tracked(rel),
        },
        actor=active.agent,
        host=active.host,
    )


def _relative(target: Path) -> str:
    try:
        return target.resolve().relative_to(paths.repo_root()).as_posix()
    except ValueError:
        return target.as_posix()



def finish(outcome: str, summary: str, next_steps: str) -> dict:
    if outcome not in OUTCOMES:
        raise SessionError(f"--outcome must be one of {', '.join(OUTCOMES)}")
    active = require_active()
    report = reconcile(active)
    gaps = doc_implications(active)
    for record, kinds in gaps.items():
        events.append(
            active.session,
            "integrity_error",
            {
                "summary": f"{record} was not updated although the session recorded {', '.join(kinds)}",
                "path": record,
                "implied_by": kinds,
                "action": "documentation-gap",
            },
            actor=active.agent,
            host=active.host,
        )
    for record in sorted(set(gitutil.changed_paths(active.start_head)) & set(paths.MISSION_RECORDS)):
        events.append(
            active.session,
            "doc_update",
            {"summary": f"updated {record}", "path": record},
            actor=active.agent,
            host=active.host,
        )
    end = events.append(
        active.session,
        "session_end",
        {
            "summary": summary,
            "outcome": outcome,
            "next": next_steps,
            "duration_s": round(elapsed(active), 1),
            "unlogged_changes": len(report["unlogged"]),
            "missing_artifacts": len(report["missing"]),
            "documentation_gaps": gaps,
        },
        actor=active.agent,
        host=active.host,
    )
    clear_pointer()
    return {
        "session": active.session,
        "outcome": outcome,
        "seq": end.seq,
        "elapsed_s": round(elapsed(active), 1),
        **report,
        "documentation_gaps": gaps,
    }


def status() -> dict:
    active = load_active()
    if active is None:
        return {"active": False}
    return {
        "active": True,
        "session": active.session,
        "goal": active.goal,
        "agent": active.agent,
        "task": active.task,
        "started_at": active.started_at,
        "elapsed_s": round(elapsed(active), 1),
        "stale": hours_since(active) > STALE_HOURS,
        "events": len(events.events_for(active.session)),
    }
