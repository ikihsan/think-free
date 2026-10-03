"""Active-session state.

One session may be open per working tree. The pointer lives in
`sessions/active.json` and is removed by `session.finish`, so an interrupted
session leaves evidence behind instead of silently allowing a second one.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass

from . import events, paths

OUTCOMES = ("worked", "partial", "failed", "no-change")
MAX_SLUG = 40
# A session longer than this is unattended automation or a forgotten pointer.
# Both are worth reporting rather than trusting.
STALE_HOURS = 24


class SessionError(RuntimeError):
    """Raised for misuse of the session API. Maps to exit code 1."""


@dataclass
class ActiveSession:
    session: str
    goal: str
    agent: str
    task: str
    started_at: str
    started_epoch: float
    start_head: str
    branch: str
    host: str

    def to_json(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_json(cls, raw: dict) -> "ActiveSession":
        return cls(**{key: raw.get(key, "") for key in cls.__annotations__})


def slugify(text: str, limit: int = MAX_SLUG) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if len(slug) > limit:
        slug = slug[:limit].rstrip("-")
    return slug or "session"


def next_session_id(goal: str) -> str:
    """Date plus a per-day ordinal plus a goal slug: 2026-10-03-001-x."""
    today = events.now_iso()[:10]
    prefix = f"{today}-"
    used = [s for s in events.all_sessions() if s.startswith(prefix)]
    ordinal = len(used) + 1
    while f"{prefix}{ordinal:03d}-{slugify(goal)}" in used:
        ordinal += 1
    return f"{prefix}{ordinal:03d}-{slugify(goal)}"


def load_active() -> ActiveSession | None:
    path = paths.active_file()
    if not path.exists():
        return None
    try:
        return ActiveSession.from_json(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, TypeError) as exc:
        raise SessionError(f"{path} is unreadable: {exc}") from exc


def require_active() -> ActiveSession:
    active = load_active()
    if active is None:
        raise SessionError(
            'no active session; run \'tools/origin session start --goal "..."\' first'
        )
    return active


def elapsed(active: ActiveSession) -> float:
    return max(0.0, time.time() - active.started_epoch)


def hours_since(active: ActiveSession) -> float:
    return elapsed(active) / 3600.0


def write_pointer(active: ActiveSession) -> None:
    paths.ensure_dir(paths.sessions_dir())
    paths.active_file().write_text(
        json.dumps(active.to_json(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def clear_pointer() -> None:
    paths.active_file().unlink(missing_ok=True)