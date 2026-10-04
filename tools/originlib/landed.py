"""Attribution when another VM's commits land in the middle of a session.

Reconciliation answers one question — which files did *this* session change? It
answers it by diffing against the commit the session started from, which is
correct only while the branch moves nowhere. `sync pull` and `sync land` move it,
and the work they bring in belongs to the machine that wrote it, so a session
that lands a colleague's task closes with `unlogged_change` events naming files
it never touched: session 029 (T-0016) reported nine, and inherited four false
`doc_update` events and a `documentation_gaps` report from another VM.

The evidence has to be recorded while the move happens. Once the branch has
moved, nothing in the tree separates the two machines' commits, because both
commit under one git identity (`Ihsan Ai Server Bot`, every commit in this
repository's history as of 2026-10-04). So `sync` records what arrived, and this
module replays it at the end of the session.

Two rules, and both are needed:

1. A path introduced by a landed commit is not this session's change.
2. Attribution follows the *newest* thing that touched the path: the last commit
   that changed it, or an uncommitted edit in the working tree. A file this
   session edits after landing is its own again, so landing a colleague's work
   and then touching the same file is still reported.

The ceiling, stated rather than hidden: a base move performed with raw git
records nothing, so its paths stay reported. The tooling never silences a file it
cannot prove belongs to someone else.
"""

from __future__ import annotations

from . import events, gitutil

# A base that moved by more commits than this is recorded truncated, with the
# count kept: the event stays readable, and reconciliation falls back to
# reporting the paths it could not attribute.
COMMIT_LIMIT = 400


def record(reason: str, before: str, after: str, arrived: list[str]) -> dict | None:
    """Record a base move into the session open in this working tree.

    Returns the event data, or None when no session is open or nothing arrived:
    a landing outside a session has no record to belong to, and inventing one
    would be a worse lie than the missing entry.
    """
    from .activestate import load_active

    active = load_active()
    if active is None or not arrived:
        return None
    truncated = len(arrived) > COMMIT_LIMIT
    data = {
        "summary": f"{reason}: base moved {before[:12]} -> {after[:12]}, "
        f"{len(arrived)} commit(s) arrived from the shared base",
        "reason": reason,
        "from": before,
        "to": after,
        "commits": arrived[:COMMIT_LIMIT],
        "commit_count": len(arrived),
        "truncated": truncated,
    }
    events.append(active.session, "base_advance", data, actor=active.agent, host=active.host)
    return data


def landed_commits(session_id: str) -> list[str]:
    """Every commit this session's record says arrived from the shared base."""
    found: list[str] = []
    for event in events.events_for(session_id):
        if event.kind != "base_advance":
            continue
        for sha in event.data.get("commits", []) or []:
            if isinstance(sha, str) and sha and sha not in found:
                found.append(sha)
    return found


def landed_paths(session_id: str) -> set[str]:
    """Paths whose current content came from the base rather than from this session."""
    commits = landed_commits(session_id)
    if not commits:
        return set()
    arrived = set(commits)
    settled = {
        path
        for path in gitutil.touched_paths(commits)
        if gitutil.last_commit_touching(path) in arrived
    }
    # A landed path with an uncommitted edit is this session's again. Without
    # this the newest-commit rule would be blind to every edit made after the
    # landing, because an uncommitted edit has no commit to point at.
    return settled - set(gitutil.dirty_paths())


def session_changes(active) -> list[str]:
    """The paths this session changed, excluding what it merely landed."""
    changed = set(gitutil.changed_paths(active.start_head))
    return sorted(changed - landed_paths(active.session))