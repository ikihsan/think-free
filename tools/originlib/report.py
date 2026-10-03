"""Generated reports: session summaries and the session index.

Everything here is derived from `events.jsonl`. Regenerating must be
idempotent, because lint fails when a committed generated file differs from
what the tool would produce now.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from . import events, gitutil, paths
from .doclint import GENERATED_NOTE


MAX_LINES = 300
TIMELINE_HEAD = 40
TIMELINE_TAIL = 10
INDEX_RECENT = 25


def _meta(owner: str, verified: str | None = None) -> str:
    stamp = verified or events.now_iso()[:10]
    return (
        "<!-- origin-meta\n"
        f"owner: {owner}\n"
        "status: active\n"
        f"last-verified: {stamp}\n"
        "-->"
    )


def _table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["_none_", ""]
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(_cell(c) for c in row) + " |" for row in rows]
    out.append("")
    return out


def _cell(value: object) -> str:
    text = str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")
    return text[:150]


def _clip(lines: list[str]) -> tuple[str, bool]:
    """Join lines, enforcing the documentation line cap."""
    text = "\n".join(lines).rstrip() + "\n"
    overflow = len(text.splitlines()) > MAX_LINES
    return text, overflow


def render_session_report(session: str) -> str:
    items = events.events_for(session)
    if not items:
        return f"# Session {session}\n\n_No events recorded._\n"
    start = next((e for e in items if e.kind == "session_start"), None)
    end = next((e for e in items if e.kind == "session_end"), None)
    data = end.data if end else {}
    lines: list[str] = [
        f"# Session {session}",
        "",
        _meta("sessions/INDEX.md"),
        "",
        GENERATED_NOTE,
        "",
        "## Outcome",
        "",
        f"- **Result:** `{data.get('outcome', 'unfinished')}`",
        f"- **Agent:** `{_agent(items)}`",
        f"- **Started:** {start.ts if start else 'unknown'}",
        f"- **Duration:** {data.get('duration_s', '?')}s",
        f"- **Host:** `{_host(items)}`",
        f"- **Branch:** `{_branch(items)}`",
        "",
        "## Goal",
        "",
        (start.data.get("goal", "_(none recorded)_") if start else "_(none recorded)_"),
        "",
    ]
    lines += ["## Summary", "", data.get("summary", "_(none recorded)_"), ""]
    if data.get("next"):
        lines += ["## Next", "", data["next"], ""]

    artifacts = [e for e in items if e.kind == "artifact"]
    lines += ["## Artifacts", ""]
    lines += _table(
        ["path", "sha256 (first 12)", "bytes"],
        [[a.data.get("path"), a.data.get("sha256", "")[:12], a.data.get("bytes")] for a in artifacts],
    )

    commands = [e for e in items if e.kind == "command"]
    failed = [c for c in commands if c.data.get("exit_code") not in (0, None)]
    lines += [
        "## Commands",
        "",
        f"{len(commands)} captured, {len(failed)} non-zero exit.",
        "",
    ]
    lines += _table(
        ["#", "command", "exit", "ms"],
        [
            [c.seq, c.data.get("argv", []), c.data.get("exit_code"), c.data.get("duration_ms")]
            for c in commands[:40]
        ],
    )

    integrity = _integrity(items)
    lines += ["## Integrity", ""]
    lines += _table(["check", "result"], integrity) if integrity else ["_no integrity findings_", ""]

    lines += _timeline(items)
    lines += [
        "## Reproduce this record",
        "",
        "```bash",
        "tools/origin session verify",
        f"cat {paths.paths_repo_relative(paths.events_file(session))}",
        "```",
        "",
    ]
    text, overflow = _clip(lines)
    if overflow:
        note = f"\n> Truncated to {MAX_LINES} lines. Full record: `{paths.paths_repo_relative(paths.events_file(session))}`\n"
        text = text.rstrip() + "\n" + note
    return text


def _agent(items: list[events.Event]) -> str:
    for item in items:
        if item.raw.get("actor"):
            return str(item.raw["actor"])
    return "unknown"


def _host(items: list[events.Event]) -> str:
    for item in items:
        if item.raw.get("host"):
            return str(item.raw["host"])
    return "unknown"


def _branch(items: list[events.Event]) -> str:
    for item in items:
        git = item.raw.get("git") or {}
        if git.get("branch"):
            return str(git["branch"])
    return "unknown"


def _integrity(items: list[events.Event]) -> list[list[str]]:
    rows: list[list[str]] = []
    unlogged = [e for e in items if e.kind == "unlogged_change"]
    missing = [e for e in items if e.kind == "artifact" and e.data.get("missing")]
    errors = [e for e in items if e.kind == "integrity_error"]
    redactions = [e for e in items if e.kind == "redaction"]
    end = next((e for e in items if e.kind == "session_end"), None)
    if not end:
        rows.append(["session_end event", "MISSING - session may be unfinished"])
    rows.append(["undeclared file changes", len(unlogged)])
    rows.append(["declared artifacts now missing", len(missing)])
    rows.append(["integrity errors", len(errors)])
    rows.append(["redactions applied to command output", len(redactions)])
    for item in unlogged[:10]:
        rows.append(["  undeclared", item.data.get("path", "")])
    for item in errors[:10]:
        rows.append(["  error", item.data.get("summary", "")[:120]])
    return rows


def _timeline(items: list[events.Event]) -> list[str]:
    lines = ["## Timeline", ""]
    shown = items
    truncated = 0
    if len(items) > TIMELINE_HEAD + TIMELINE_TAIL:
        truncated = len(items) - TIMELINE_HEAD - TIMELINE_TAIL
        shown = items[:TIMELINE_HEAD] + items[-TIMELINE_TAIL:]
    lines += _table(["seq", "time", "kind", "summary"], [[e.seq, e.ts[11:19], e.kind, e.summary()] for e in shown])
    if truncated:
        lines += [f"_{truncated} middle events omitted; see `events.jsonl`._", ""]
    return lines


def render_sessions_index() -> str:
    sessions = events.all_sessions()
    rows: list[list[str]] = []
    for session in reversed(sessions):
        items = events.events_for(session)
        end = next((e for e in items if e.kind == "session_end"), None)
        start = next((e for e in items if e.kind == "session_start"), None)
        goal = (start.data.get("goal", "") if start else "")[:70]
        rows.append(
            [
                f"[{session}]({session}/README.md)",
                _agent(items),
                (end.data.get("outcome") if end else "**unfinished**"),
                goal,
                end.ts[:16] if end else (start.ts[:16] if start else ""),
            ]
        )
    head = [
        "# Sessions index",
        "",
        _meta("docs/INDEX.md"),
        "",
        GENERATED_NOTE,
        "",
        f"{len(sessions)} recorded session(s). One `events.jsonl` per session, so concurrent",
        "sessions on separate branches never conflict.",
        "",
    ]
    if len(rows) > INDEX_RECENT:
        older = len(rows) - INDEX_RECENT
        rows = rows[:INDEX_RECENT]
        head.append(f"Showing the {INDEX_RECENT} most recent. {older} older session(s) are in the directory listing.")
        head.append("")
    tail = [
        "",
        "## Reading a session",
        "",
        "```bash",
        "tools/origin session resume <session-id>   # compressed brief for continuing work",
        "tools/origin session verify                # integrity across all sessions",
        "```",
        "",
        "Protocol: [`docs/process/session-protocol.md`](../docs/process/session-protocol.md).",
        "",
    ]
    text, _ = _clip(head + _table(["session", "agent", "outcome", "goal", "ended"], rows) + tail)
    return text


def write_if_changed(path: Path, content: str) -> bool:
    """Write only when content differs. Returns True when it wrote."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def regenerate_session(session: str) -> bool:
    return write_if_changed(paths.session_report(session), render_session_report(session))


def regenerate_sessions_index() -> bool:
    return write_if_changed(paths.sessions_index(), render_sessions_index())


def archive_hint() -> str | None:
    """Name of the archive file to split into when the index gets too long."""
    index = paths.sessions_index()
    if not index.exists():
        return None
    stamp = datetime.now().astimezone().strftime("%Y-%m")
    return f"INDEX-{stamp}.md"


def env_flag(name: str) -> bool:
    return os.environ.get(name, "") not in ("", "0", "false", "no")


def current_head() -> str:
    return gitutil.text(["rev-parse", "--short", "HEAD"]) or "(no commits)"