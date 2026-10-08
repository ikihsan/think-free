#!/usr/bin/env python3
"""E055's shared test scaffolding: one temporary root per control run, cleaned up.

Split out so the five test modules do not each carry their own copy. A control is
called as `fn(root, cases)` and owns its own repositories under `root`; the only
thing the harness owes it is a fresh directory that is removed afterwards, so one
control's leftovers cannot make the next one's numbers look different.

Kept here rather than in any one test module because the split is by *what a test
binds* — the grader, the probes, the readers, the ordering, the verdict — and this
belongs to none of those.

**Import this before `compare`.** The oracle that every control is pinned to lives
in E038's directory, a sibling of this one, so this module also puts it on
`sys.path`. `run.py` and `ceiling.py` each carry their own copy of that line
because they are not test modules; the four test modules that do import `compare`
must come through here, and they must import it *first*. Splitting this suite into
per-invariant modules left all four of them importing `compare` with nothing on
`sys.path`, and the failure read as four unrelated import errors rather than as one
missing line.
"""

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
ORACLE_DIR = os.path.normpath(os.path.join(HERE, os.pardir, "038-staging-prior-art"))
if ORACLE_DIR not in sys.path:
    sys.path.insert(0, ORACLE_DIR)


def scratch(fn, *args):
    """Run `fn(root, *args)` against a fresh temporary root and clean up after."""
    root = tempfile.mkdtemp(prefix="e055-test-")
    try:
        return fn(root, *args)
    finally:
        shutil.rmtree(root, ignore_errors=True)
