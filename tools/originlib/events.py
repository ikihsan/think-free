"""Append-only session event stream.

Events are the authoritative record. Prose reports are regenerated from them,
so the two can never silently disagree.

One file per session (`sessions/<id>/events.jsonl`) rather than one global
file, so that two sessions running on different branches never produce a merge
conflict in an append-only log.
"""

from __future__ import annotations

import fcntl
import json
import os
import re
from contextlib import contextmanager
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
    """The next sequence number, read without the lock.

    Fine for a preview; not safe to write with, which is what `hold_stream` is
    for. Defect 24: this read-then-write was the whole race.
    """
    return _last_seq(read(path)) + 1


def _last_seq(events: list[dict]) -> int:
    last = 0
    for event in events:
        if isinstance(event.get("seq"), int):
            last = max(last, event["seq"])
    return last


@contextmanager
def hold_stream(path: Path):
    """Hold an exclusive advisory lock on one stream and yield the seq to use.

    `seq` is allocated by reading the file and writing `max + 1`, so two
    processes appending without a lock both read the same tail and both write
    the same number. That is not hypothetical: two concurrent `session finish`
    runs on one session on 2026-10-08 produced 19 duplicated `seq` values and a
    stream that `session verify` rejects, which is defect 24.

    Every writer takes this lock. A caller that needs to write something else
    against the same number — `recorder` writes the command log block first, so
    the log header and the event agree — keeps the lock across both writes and
    passes the number it was given as `append(seq=...)`.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    handle = open(path, "a+", encoding="utf-8")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        yield _last_seq(_read_lines(handle)) + 1
    finally:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def append(
    session: str,
    kind: str,
    data: dict | None = None,
    *,
    path: Path | None = None,
    seq: int | None = None,
    **extra,
) -> Event:
    """Append one event and return it. Flushes and fsyncs for durability.

    `seq` is for a caller already inside `hold_stream`. Passing it without that
    lock reopens defect 24, and `tests/test_event_stream_concurrency.py` covers
    the path that matters: concurrent `append` from separate processes.
    """
    if kind not in KINDS:
        raise ValueError(f"unknown event kind: {kind}")
    target = path or paths.events_file(session)
    if seq is None:
        with hold_stream(target) as allocated:
            return _emit(target, session, kind, data, allocated, extra)
    return _emit(target, session, kind, data, seq, extra)


def _emit(target: Path, session: str, kind: str, data, seq: int, extra: dict) -> Event:
    payload = {
        "schema": paths.EVENT_SCHEMA,
        "seq": seq,
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
    return list(_read_lines(path.read_text(encoding="utf-8", errors="replace").splitlines()))


def _read_lines(lines) -> list[dict]:
    events: list[dict] = []
    for line in lines:
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