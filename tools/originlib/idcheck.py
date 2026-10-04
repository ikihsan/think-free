"""One entry point for the identifier record, read by both publishing gates.

`doc lint` rule 7 and `sync land`'s refusal ask the same question — does one
number in this tree mean two things? — and T-0036 showed that a module wired
into one of them is not thereby read by the other: the defect list was added as
its own module precisely because it is a second source of definitions, and it
had to be routed through both. Two callers, two modules, one function: so that
adding a third source is a change to this file and nothing else.

The order is the modules' order, and neither is sorted against the other. A
reader who is renumbering wants findings before defect numbers, because that is
the order they collided in.
"""

from __future__ import annotations

from pathlib import Path

from . import defectlist, identifiers


def report(root: Path) -> list[str]:
    """Every identifier collision in the mission record, one per line."""
    return identifiers.report(root) + defectlist.report(root)