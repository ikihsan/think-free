"""What a session owes the other machines at its two boundaries.

Split out of `session.py` so that the cross-VM rules are readable on their own:
one place decides what "starting" means when several VMs share a repository, and
one place decides what "finishing" must leave behind.

The asymmetry is deliberate. On the way in, the tooling fetches and
fast-forwards, because a session that starts from a stale tree reconciles
against a commit nobody else has seen. On the way out, the tooling commits only
the session's own record, because the agent's work needs a message that says
what the work actually is; silently publishing unreviewed edits is precisely
what this repository exists to prevent.
"""

from __future__ import annotations

from . import gitutil, sync
from .activestate import SessionError

SESSION_OWNED_PREFIX = "sessions/"


def sync_before_start() -> dict:
    """Fast-forward onto the shared base before recording anything.

    Returns what was synced, so the session record says which remote commit the
    work started from. Offline machines get `{"remote": ""}` and proceed.
    """
    remote = sync.remote_name()
    if not remote:
        return {"remote": ""}
    base = sync.base_branch()
    try:
        outcome = sync.pull()
    except sync.SyncError as exc:
        raise SessionError(
            f"cannot start a session from a stale or dirty tree: {exc}"
        ) from exc
    return {
        "remote": remote,
        "base_branch": base,
        "fast_forwarded": bool(outcome.get("fast_forwarded")),
        "behind_before": int(outcome.get("behind_before", 0)),
        "remote_head": gitutil.text(["rev-parse", f"{remote}/{base}"]),
    }


def session_owned_paths(session_id: str) -> tuple[str, ...]:
    """The files a session's own record consists of, generated indexes included."""
    return (
        f"{SESSION_OWNED_PREFIX}{session_id}",
        f"{SESSION_OWNED_PREFIX}INDEX.md",
        "docs/INDEX.md",
        "tasks/INDEX.md",
    )


def uncommitted_work(session_id: str) -> list[str]:
    """Dirty paths that are not part of the session record."""
    owned = set(session_owned_paths(session_id))
    prefix = f"{SESSION_OWNED_PREFIX}{session_id}/"
    return [
        path
        for path in sync.dirty_paths()
        if path not in owned and not path.startswith(prefix)
    ]


def commit_session_record(session_id: str, outcome: str) -> str:
    """Commit the session's own files, and nothing else. Empty when nothing changed."""
    gitutil.run(["add", "--", *session_owned_paths(session_id)])
    if gitutil.run(["diff", "--cached", "--quiet"]).returncode == 0:
        return ""
    if gitutil.run(["commit", "-q", "-m", f"session: {session_id} ({outcome})"]).returncode != 0:
        return ""
    return gitutil.text(["rev-parse", "HEAD"])
