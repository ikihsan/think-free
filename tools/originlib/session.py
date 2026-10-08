"""Session lifecycle: start, finish, status.

Event helpers live in `sessionlog`, active-session state in `activestate`, git
reconciliation in `reconcile`. All of them are re-exported here so callers need
one import.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from . import events, gitutil, paths, sessionflow, sessionlock, sync
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
from .sessionlog import (
    artifact,
    block,
    decision,
    experiment_result,
    log,
    note,
    step,
)


def start(
    goal: str,
    agent: str | None = None,
    task: str | None = None,
    sync_remote: bool = True,
) -> ActiveSession:
    existing = load_active()
    if existing is not None:
        raise SessionError(
            f"session {existing.session} is already active (started {existing.started_at}); "
            "finish it or run 'tools/origin session status'"
        )
    if not goal.strip():
        raise SessionError("--goal must not be empty")
    sync_report = sessionflow.sync_before_start() if sync_remote else {"remote": ""}
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
    events.append(
        session,
        "session_start",
        {
            "goal": active.goal,
            "agent": active.agent,
            "task": active.task,
            "dirty_at_start": git.porcelain,
            **sync_report,
        },
        actor=active.agent,
        host=host,
        git={"head": git.head, "branch": git.branch},
    )
    # After the first event, not before. The report renders from the event
    # stream, so regenerating first produced a stub with no `origin-meta` and
    # an index that listed no session — and `doc lint` failed on both for as
    # long as the session was open, which is the whole time anyone lints.
    refresh_reports(session)
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


def refresh_reports(session_id: str) -> None:
    """Rebuild this session's report and `sessions/INDEX.md` from the stream.

    Two reasons, both observed. From the moment of opening: otherwise
    `sessions/INDEX.md` would link to a report that does not exist yet, and a
    broken link in a generated file is a lint failure. And after **every**
    append: the report is a generated file, so any commit made between an
    event and the next report write publishes a stale one, which is a red CI
    run (run 37180487906, from a `tools/x` capture and an artifact recorded
    after the last regeneration). Called from `session start` and `finish`
    before T-0034; from every other appender after it.
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



def session_owned_paths(session_id: str) -> tuple[str, ...]:
    """Files a session's own record consists of, including generated indexes."""
    return sessionflow.session_owned_paths(session_id)


def _prepare_push(active: ActiveSession) -> str:
    """Refuse to close with unpublished work still sitting in the tree.

    The session record is committed and pushed by `finish`, but the agent's own
    changes are committed by the agent, with a message that says what the work
    actually is. Auto-committing unreviewed edits under a generated message is
    exactly the kind of silent publication this repository is built to prevent.
    """
    remote = sync.remote_name()
    if not remote:
        raise SessionError(
            "no git remote configured; commit and push with git, or finish without --push"
        )
    stray = sessionflow.uncommitted_work(active.session)
    if stray:
        raise SessionError(
            "commit these before finishing with --push, so the record and the work "
            "travel together: " + ", ".join(stray[:8])
        )
    return remote


def finish(outcome: str, summary: str, next_steps: str, push: bool = False) -> dict:
    """Close the active session, emitting exactly one reconciliation and end.

    `sessionlock.single_finish` holds ownership for the whole operation. The
    in-stream check below is still needed — it is what refuses a *sequential*
    re-finish — but it can no longer be the only guard, because a check that
    reads and then appends cannot order two processes. That is how session 008
    acquired two ends and two reconciliations (defect 24).
    """
    if outcome not in OUTCOMES:
        raise SessionError(f"--outcome must be one of {', '.join(OUTCOMES)}")
    with sessionlock.single_finish():
        return _finish_locked(outcome, summary, next_steps, push)


def _finish_locked(outcome: str, summary: str, next_steps: str, push: bool) -> dict:
    active = require_active()
    prior_ends = [e for e in events.events_for(active.session) if e.kind == "session_end"]
    if prior_ends:
        raise SessionError(
            f"session {active.session} already ended at seq {prior_ends[0].seq}; "
            "start a new session instead of re-finishing"
        )
    if push:
        _prepare_push(active)
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
    for record in sorted(set(report["own"]) & set(paths.MISSION_RECORDS)):
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
            "landed_paths": len(report["landed"]),
            "documentation_gaps": gaps,
            "push_requested": bool(push),
        },
        actor=active.agent,
        host=active.host,
    )
    clear_pointer()
    pushed = ""
    session_commit = ""
    if push:
        from . import report as report_module

        report_module.regenerate_session(active.session)
        report_module.regenerate_sessions_index()
        session_commit = sessionflow.commit_session_record(active.session, outcome)
        pushed = sync.push().get("head", "")
    return {
        "session": active.session,
        "outcome": outcome,
        "seq": end.seq,
        "elapsed_s": round(elapsed(active), 1),
        "pushed": pushed,
        "session_commit": session_commit,
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
