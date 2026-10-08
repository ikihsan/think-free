"""One writer at a time for `session finish`.

Split out of `session.py` on 2026-10-08 (defect 24) when the cap found the
file at 318 lines, and by invariant: `session` decides *what* closing a session
means, while this only decides *whose turn it is*. A lock is a concurrency
primitive; mixing it into the lifecycle dispatcher is what made the race hard to
see, because the guard that was supposed to prevent it lived three functions
away from the append that overtook it.

Defect 24 in one paragraph. Session 008's stream held 181 lines over 162
sequence numbers, which `session verify` rejects and no later commit could land.
Two overlapping `finish` runs each swept the tree, and `finish`'s guard against a
second end was a read of the stream followed by the append — both runs read
before either wrote, both saw no `session_end`, both proceeded. Each
reconciliation re-emitted 84 `unlogged_change` events for the same 84 paths.

Two locks, because they guard different things:

- `events.hold_stream` serialises sequence allocation against every writer,
  including `recorder` and `tools/x` running while a finish is in progress.
  Without it, an append from any source can allocate a number another source
  already holds.
- `single_finish` serialises finishes *against each other*, over the whole
  operation. The stream lock alone would leave the record well-formed and
  doubly reconciled: two `session_end` events, two full sweeps.
"""

from __future__ import annotations

import fcntl
from contextlib import contextmanager

from . import paths
from .activestate import SessionError, load_active

LOCK_NAME = ".finish.lock"


@contextmanager
def single_finish():
    """Hold exclusive ownership of closing the active session.

    Raises `SessionError` when another process already holds it, which is the
    message an agent needs: the first finish is still running, so a second is
    not a retry of anything.
    """
    active = load_active()
    if active is None:
        # Nothing to serialise. `finish` requires an active session and will
        # say so itself with a better message than a lock could.
        yield
        return
    lock_path = paths.session_dir(active.session) / LOCK_NAME
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(lock_path, "a+", encoding="utf-8")
    try:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise SessionError(
                f"another 'session finish' is already running for {active.session}; "
                "wait for it rather than starting a second one"
            )
        yield
    finally:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()
