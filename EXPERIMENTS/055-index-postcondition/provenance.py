#!/usr/bin/env python3
"""E055: bind each raw artifact to the bytes of the scripts that produced it.

This exists because of a defect found in this experiment's own evidence. `ceiling.py`
was edited ten seconds **after** it wrote `raw/ceiling.json`, and the edit added a
field the recorded rows do not have. Nothing failed: the artifact parsed, the controls
had fired, the verdict read `partial`, and the recorded file was produced by bytes
that no longer existed in the tree. A later reader — including this experiment's own
author, twenty minutes later — could not tell from `raw/` which code produced it.

Two earlier instances of the shape are in the record and neither was this one:
F029's `raw/` files and F0xx's summary prose both drifted from the code that produced
them, and in both cases the artifact was right and the prose was what moved. Here the
artifact and the code were both right at the time and only their *relationship* went
unrecorded.

So every artifact this experiment writes carries the sha256 of every script in this
directory, and `--verify` recomputes them. `run.py --verify` is the command the task's
verify step points at, which is the place a check has to live to actually run
(D025, F013: the problem is not gates that are missing but gates that are never run).

    python3 provenance.py --check raw/results.json

Exits 0 when the artifact was written by the current bytes, 3 when it was not or was
written before this existed, and 2 on usage error. It is a *report*, not a gate: it
never changes a verdict, because a verdict computed from evidence whose provenance is
unknown is still the run's answer — it is just not one that can be reproduced.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def scripts(directory=None):
    """Every script in this directory that can affect a result, sorted by name.

    `__pycache__` is a directory and is not one. `test_*.py` is excluded because it
    writes no artifact — including it would make editing a test look like a change to
    the measurement.
    """
    d = directory or HERE
    return sorted(f for f in os.listdir(d)
                  if f.endswith(".py") and not f.startswith("test_")
                  and os.path.isfile(os.path.join(d, f)))


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def stamp(directory=None):
    """{script name: sha256} for the current bytes."""
    d = directory or HERE
    return {name: digest(os.path.join(d, name)) for name in scripts(d)}


def compare(recorded, current):
    """Names whose bytes differ, added, or removed. Empty means the same code.

    Symmetric on purpose. A script that was *added* after the run changes nothing
    about that run, and reporting it as a difference would train the reader to
    ignore the check; it is reported so the caller can see it and decide, not so the
    check cries wolf on every new file.
    """
    if not recorded:
        return sorted(current)
    names = set(recorded) | set(current)
    return sorted(n for n in names if recorded.get(n) != current.get(n))


def check(path, directory=None):
    """(ok, [differing names], note). Reads an artifact's own provenance block."""
    if not os.path.exists(path):
        return False, [], "no artifact at %s" % path
    with open(path) as fh:
        doc = json.load(fh)
    recorded = (doc.get("provenance") or {}).get("scripts") or {}
    if not recorded:
        return False, [], "artifact carries no provenance block; it predates this check"
    diff = compare(recorded, stamp(directory))
    return (not diff), diff, ("%d script(s) differ" % len(diff) if diff
                              else "written by the current bytes")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    ok, diff, note = check(argv[0])
    print("%s: %s" % (argv[0], note))
    for name in diff:
        print("  differs: %s" % name)
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
