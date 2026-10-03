"""Event helpers for the active session.

The thin wrappers (`step`, `note`, `decision`, `block`, `experiment_result`)
and `artifact` live apart from `session` so that neither file grows past the
line cap. `session` re-exports them, so callers still import one module.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from . import events, gitutil, paths, secrets
from .activestate import SessionError, require_active


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
    if gitutil.is_ignored(rel):
        raise SessionError(
            f"{rel} is excluded by .gitignore; declare the source that produces it instead"
        )
    found, suppressed = secrets.scan_file(target, report_suppressions=True)
    if suppressed:
        events.append(
            active.session,
            "note",
            {
                "summary": (
                    f"{rel} declares origin-allow-secret-patterns: "
                    f"{', '.join(sorted(suppressed))}; suppressed for this file only"
                ),
                "path": rel,
                "suppressed_patterns": sorted(suppressed),
            },
            actor=active.agent,
            host=active.host,
        )
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



