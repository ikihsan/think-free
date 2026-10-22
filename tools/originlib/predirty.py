"""Paths that were already untracked when this session opened.

`session start` records the tree it opens on (`dirty_at_start`), because a
reconciliation that only diffs against `start_head` cannot separate this
session's work from a file an earlier session left uncommitted. Session
2026-10-21-003 is what it cost not to read it: it preserved 6 236 files that
seven closed sessions had left uncommitted, one commit at the start of its own
work, and then `session finish` reported **every one of them** as a change it
had failed to declare — 6 200 `unlogged_change` events naming no file this
session wrote. A report that large is not a report; it trains the reader to skip
the next one, and the next one is the interesting one. It also cost the session
its close twice, because writing that many events took longer than the machine
stayed up. (D305)

The rule is deliberately narrow: only a path the session found **untracked** is
excluded. A tracked file that was already modified at start is still reported,
because the one thing `finish` exists to surface is a change no session recorded
— `tests/test_task_rewrite.py` pins that a command run outside any session is
reported by the next one. A new untracked file is different: the session that
wrote it had a record to make, and committing it is the act this session
performs; the producing session is closed and cannot declare anything now.

The record is a `git status --porcelain` line list, so both shapes have to be
read:

* `?? path` — an untracked path. Excluded.
* `?? dir/` — an untracked *directory*, the collapse the default porcelain
  performs. It is a prefix, not a path: the files inside it were not listed, and
  files created inside it *after* `start` cannot be told apart from files that
  were already there.
* ` M path` — a tracked path already modified at start — is read and discarded:
  it is reported.

The directory shape is the ceiling, and it is stated rather than hidden: on a
session started before `--untracked-files=all`, a file written inside a
directory that was already untracked at start is excluded too. The rule is still
the right one — the alternative reported thousands of paths no session in the
tree had touched — and the ceiling disappears for any session started after the
capture change, because a per-file capture has no directory entries to
over-match.
"""

from __future__ import annotations

from . import events

# The two columns `git status --porcelain` uses for the index and worktree
# status. A path only counts as status-plus-path when both characters come from
# this set, so an untracked file whose *name* begins with something that looks
# like a status is not truncated into the wrong path.
STATUS_CHARS = set(". MADRCU?!")
RENAME = " -> "


def split_line(line: str) -> str:
    """The path half of one porcelain line, rename destinations kept."""
    if len(line) >= 4 and line[2] == " " and set(line[:2]) <= STATUS_CHARS:
        path = line[3:]
    else:
        path = line
    if RENAME in path:
        path = path.split(RENAME, 1)[1]
    return path.strip('"')


def start_lines(active) -> list[str]:
    """The `dirty_at_start` lines of the session's own `session_start` event."""
    for event in events.events_for(active.session):
        if event.kind == "session_start":
            return list(event.data.get("dirty_at_start") or [])
    return []


def load(active) -> tuple[set[str], list[str]]:
    """`(untracked_paths, directory_prefixes)` the session found untracked.

    Only `??` lines are read. A tracked file already modified at start is
    reported, so `finish` still surfaces a change no session recorded
    (`test_task_rewrite`).
    """
    untracked: set[str] = set()
    prefixes: list[str] = []
    for line in start_lines(active):
        if not line.startswith("?? "):
            continue
        path = split_line(line)
        if not path:
            continue
        if path.endswith("/"):
            prefixes.append(path)
        else:
            untracked.add(path)
    return untracked, prefixes


def is_untracked_at_start(rel: str, untracked: set[str], prefixes: list[str]) -> bool:
    """True when the path was untracked in the tree the session started from."""
    if rel in untracked:
        return True
    return any(rel.startswith(prefix) for prefix in prefixes)
