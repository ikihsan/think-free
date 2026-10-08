"""Command capture.

Appends a command's argv, output, exit code, and duration to the session's
commands.log and emits a `command` event pointing at the exact log lines, so a
reader can check the record without replaying anything.

Output is redacted before it reaches disk. Losing evidence is worse than masking
a token, and the redaction itself is recorded as an event.
"""

from __future__ import annotations

from pathlib import Path

from . import events, paths, secrets
from .activestate import load_active

RULE = "=" * 78
THIN = "-" * 78


def format_block(
    seq: int,
    argv: list[str],
    cwd: str,
    returncode: int,
    duration_ms: int,
    output: str,
    redactions: list[str],
) -> list[str]:
    return [
        RULE,
        f"[seq {seq}] {events.now_iso()}",
        f"$ {' '.join(argv)}",
        f"cwd: {cwd}",
        THIN,
        output.rstrip("\n"),
        THIN,
        f"exit: {returncode}  duration_ms: {duration_ms}  redactions: {', '.join(redactions) or 'none'}",
    ]


def record_command(
    argv: list[str],
    returncode: int,
    duration_ms: int,
    output: str,
    cwd: str,
    session_id: str | None = None,
) -> dict:
    """Append command output to the session log and emit a `command` event.

    The caller has already run the command; this only records it. Returns a
    summary describing what was written, or `recorded: False` when there is no
    session to record into.
    """
    active = load_active()
    target_session = session_id or (active.session if active else None)
    if target_session is None:
        return {"recorded": False, "reason": "no active session"}
    clean, redactions = secrets.redact(output)
    log_path = paths.commands_log(target_session)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    # The log block's header seq and the event's seq must be the same
    # number, and a second process appending in between would assign
    # two. One lock covers both the log write and the event append.
    with events.locked(paths.events_file(target_session)):
        existing = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
        seq = events.next_seq(paths.events_file(target_session))
        block = format_block(seq, argv, cwd, returncode, duration_ms, clean, redactions)
        with open(log_path, "a", encoding="utf-8") as handle:
            handle.write("\n".join(block) + "\n")
            handle.flush()
        data = {
            "summary": f"$ {' '.join(argv)[:140]}",
            "argv": argv,
            "cwd": cwd,
            "exit_code": returncode,
            "duration_ms": duration_ms,
            "log": paths.paths_repo_relative(log_path),
            "log_line_start": len(existing) + 1,
            "log_line_end": len(existing) + len(block),
            "redactions": redactions,
        }
        events._append_locked(
            target_session,
            "command",
            data,
            target=paths.events_file(target_session),
            actor=active.agent if active else None,
            host=active.host if active else None,
            duration_ms=duration_ms,
            exit_code=returncode,
        )
        if redactions:
            events._append_locked(
                target_session,
                "redaction",
                {
                    "summary": f"redacted {len(redactions)} secret pattern(s) from command output",
                    "patterns": redactions,
                    "argv": argv,
                },
                target=paths.events_file(target_session),
                actor=active.agent if active else None,
                host=active.host if active else None,
            )
        # The report is generated from this stream, so appending to the stream
        # invalidates it. A commit made before the next regeneration publishes a
        # stale report and reddens CI — observed as run 37180487906, where a capture
        # and an artifact were recorded after the last write and the tree was
        # committed in between.
        from . import session as session_module

        session_module.refresh_reports(target_session)
    return {
        "recorded": True,
        "seq": seq,
        "redactions": redactions,
        "log": data["log"],
        "lines": [data["log_line_start"], data["log_line_end"]],
    }


def read_slice(log_path: Path, start: int, end: int) -> list[str]:
    """The exact log lines an event points at, for verification."""
    if not log_path.exists():
        return []
    return log_path.read_text(encoding="utf-8", errors="replace").splitlines()[start - 1 : end]