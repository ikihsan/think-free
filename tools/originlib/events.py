"""Append-only session event stream.

Events are the authoritative record. Prose reports are regenerated from them,
so the two can never silently disagree.

One file per session (`sessions/<id>/events.jsonl`) rather than one global
file, so that two sessions running on different branches never produce a merge
conflict in an append-only log.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from . import paths

# Every kind the tooling may emit. `verify` rejects unknown kinds so a typo in
# a new caller cannot create an event nothing else understands.
KINDS = frozenset(
    {
        "session_start",
        "milestone",
        "decision",
        "note",
        "artifact",
        "command",
        "block",
        "base_advance",
        "unlogged_change",
        "doc_update",
        "task_claim",
        "task_status",
        "task_rewrite",
        "experiment_result",
        "redaction",
        "integrity_error",
        "session_end",
    }
)

REQUIRED_FIELDS = ("schema", "seq", "ts", "session", "kind", "data")

SESSION_ID = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{3}-[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass
class Event:
    seq: int
    ts: str
    session: str
    kind: str
    data: dict
    raw: dict

    def summary(self) -> str:
        """One-line human description used in reports and the status view."""
        data = self.data
        for key in ("summary", "goal", "path", "command", "reason", "next", "message"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                text = value.strip().replace("\n", " ")
                return text if len(text) <= 160 else text[:157] + "..."
        return self.kind


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def next_seq(path: Path) -> int:
    last = 0
    if path.exists():
        for event in read(path):
            if isinstance(event.get("seq"), int):
                last = max(last, event["seq"])
    return last + 1


def append(
    session: str,
    kind: str,
    data: dict | None = None,
    *,
    path: Path | None = None,
    **extra,
) -> Event:
    """Append one event and return it. Flushes and fsyncs for durability."""
    if kind not in KINDS:
        raise ValueError(f"unknown event kind: {kind}")
    target = path or paths.events_file(session)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": paths.EVENT_SCHEMA,
        "seq": next_seq(target),
        "ts": now_iso(),
        "session": session,
        "kind": kind,
        "data": data or {},
    }
    payload.update({k: v for k, v in extra.items() if v is not None})
    line = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    with open(target, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return Event(payload["seq"], payload["ts"], session, kind, payload["data"], payload)


def read(path: Path) -> list[dict]:
    """Read all events. Malformed lines are preserved as-is for the verifier."""
    if not path.exists():
        return []
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({"__malformed__": line})
    return events


def events_for(session: str) -> list[Event]:
    return [Event(e["seq"], e["ts"], e["session"], e["kind"], e.get("data", {}), e)
            for e in read(paths.events_file(session))
            if "__malformed__" not in e]


def all_sessions() -> list[str]:
    root = paths.sessions_dir()
    if not root.exists():
        return []
    return sorted(
        entry.name
        for entry in root.iterdir()
        if entry.is_dir() and SESSION_ID.match(entry.name) and (entry / "events.jsonl").exists()
    )


def validate(event: dict) -> list[str]:
    """Return a list of problems. Empty means valid."""
    problems: list[str] = []
    if "__malformed__" in event:
        return ["malformed JSON line"]
    for field_name in REQUIRED_FIELDS:
        if field_name not in event:
            problems.append(f"missing field {field_name!r}")
    if event.get("schema") != paths.EVENT_SCHEMA:
        problems.append(f"unexpected schema {event.get('schema')!r}")
    if event.get("kind") not in KINDS:
        problems.append(f"unknown kind {event.get('kind')!r}")
    if not isinstance(event.get("seq"), int):
        problems.append("seq is not an integer")
    if not isinstance(event.get("data"), dict):
        problems.append("data is not an object")
    return problems