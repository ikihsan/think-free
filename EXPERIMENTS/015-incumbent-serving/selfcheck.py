#!/usr/bin/env python3
"""Known-answer cases for the channels in `serving.py`.

Split out at the 300-line cap by invariant: a self-check is a *falsification* of
the instrument, not another channel, and it is the one part of that instrument
that is written before the instrument is trusted rather than after.

Six cases whose answers are known in advance, four in the registry channels and
two in the two channels this experiment added. Every defect this finds pushes the
whole measurement **towards zero**, which is the direction that flatters the
hypothesis under test -- so the self-check is run before any result is read, and
again whenever a channel changes.

The sixth case is the negative direction and the one that matters most: an
attribution that names a different repository must be refused. F032's fatal case
was crediting npm downloads for `please` to `thought-machine/please` because the
package of that name belongs to somebody else, which under-counts the incumbent
that decides a niche.

    python3 selfcheck.py        # exits non-zero if any case fails
    python3 serving.py --selfcheck
"""

import sys

from attribution import owned_by, metadata_repo


def declared_repo_for(registry, name):
    """The local name, kept because it reads better than metadata_repo here."""
    return metadata_repo(registry, name)
from serving import (brew_30d, crates_month, npm_month, pypi_month,
                     release_downloads)
from verdict import FLOOR_RATE, FLOOR_RELEASE


# Cases whose answer is known before any result is used. Every one of these is a
# tool that is certainly used, and every defect found here would push the whole
# measurement towards zero -- the direction that flatters the hypothesis.
SELFCHECK = [
    # (label, callable, must be a number at least this large)
    ("npm vite", lambda: npm_month("vite"), FLOOR_RATE),
    ("pypi requests", lambda: pypi_month("requests"), FLOOR_RATE),
    ("crates serde", lambda: crates_month("serde"), FLOOR_RATE),
    ("brew ripgrep 30d", lambda: brew_30d("ripgrep"), FLOOR_RATE),
    ("cli/cli release assets", lambda: (release_downloads("cli/cli") or {}).get("downloads"),
     FLOOR_RELEASE),
]


def run(verbose=True):
    """Run the known-answer cases. Returns the number that failed."""
    failed = 0
    for label, fn, floor in SELFCHECK:
        try:
            got = fn()
        except Exception as exc:                       # noqa: BLE001
            got = "raised %r" % (exc,)
        ok = isinstance(got, int) and got >= floor
        failed += 0 if ok else 1
        if verbose:
            print("  %-24s %-14s %s" % (label, got, "ok" if ok else "FAIL"))
    # The negative direction, which is the direction that matters: an attribution
    # that names a different repository must be refused, not counted.
    bad = owned_by(declared_repo_for("npm", "please"), "thought-machine/please")
    if bad:
        failed += 1
    if verbose:
        print("  %-24s %-14s %s" % ("npm:please not please",
                                    "refused" if not bad else "ACCEPTED",
                                    "ok" if not bad else "FAIL"))
    print("self-check: %d of %d failed" % (failed, len(SELFCHECK) + 1))
    return failed


