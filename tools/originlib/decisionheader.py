"""A decision record's own header, held to the decisions that file defines.

Why this module exists (defect 14 in `STATE-defects.md`, T-0042). The identifier
rule reads three sources and used to read two. A decision number lives in three
places that must agree: the `## Dnnn — …` heading that defines it, the row in
`DECISIONS.md`'s index that says which file holds it, and the `Decisions **…**`
line each decision record opens with — the one a reader lands on first, because
it is under the title and above everything else. T-0030 added the index row in
both directions and T-0036 added the numbered defect list; neither read the
header, so the header went stale in two of the five files while every gate
passed.

What was actually false on the shared base, before this rule existed:

* `DECISIONS-GATING.md` said `Decisions **D013, D024–D029**`. It defines D024,
  D025, D026, D029, D030, D032 and D035 — so it named D013, which lives in
  `DECISIONS-SESSIONS.md`, and omitted three of its own entries.
* `DECISIONS-PRACTICE.md` said `Decisions **D011–D018, D027–D028**`. It defines
  D011, D012, D014–D018, D031, D033 and D034 — so the range named D013 and the
  pair D027–D028, all three of which moved to `DECISIONS-SESSIONS.md` when that
  split was reversed on 2026-10-04, and it omitted D031, D033 and D034.

What counts as a header, narrowly: a line of the form `Decisions **…**` in a
file that defines at least one decision. A decision record with no readable
header is **reported**, not skipped: a parser that quietly stops matching is
indistinguishable from a clean tree, which is the second obligation D025 records
and the one defect 10's control failure was about.

What the rule does not do, stated rather than implied:

* It does not compare wording. It compares identifier sets, so a range that
  expands to the right numbers passes however the range is spelled.
* It does not read `DECISIONS.md`'s index; `decisionindex` already holds that
  row to the headings in both directions. This module reads the *third* source.
* It does not care about the order of the identifiers or their case. A header
  that lists a decision twice is not reported, because the duplicate-number rule
  is `identifiers`' and a header cannot define a number.
"""

from __future__ import annotations

import re
from pathlib import Path

from .decisionindex import declarations
from .identifiers import definitions

# `Decisions **D013, D024–D029**. Each entry records …`. The bold span is
# non-greedy so the trailing prose after the closing `**` is not swallowed.
HEADER = re.compile(r"^Decisions\s+\*\*(.+?)\*\*")


def _read(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def header(path: Path) -> tuple[set[str], int] | None:
    """The identifiers a decision record's own header claims, and its line.

    `None` when no line reads as a header, which is a reported state rather
    than an absent one: see the module docstring and D025.
    """
    for number, line in enumerate(_read(path), start=1):
        match = HEADER.match(line)
        if match:
            return declarations(match.group(1)), number
    return None


def _defined_by_file(root: Path) -> dict[str, set[str]]:
    """Decision identifiers grouped by the file that defines them."""
    grouped: dict[str, set[str]] = {}
    for item in definitions(root):
        if item.ident.startswith("D"):
            grouped.setdefault(item.path, set()).add(item.ident)
    return grouped


def report(root: Path) -> list[str]:
    """Every decision record whose own header disagrees with its contents."""
    found: list[str] = []
    grouped = _defined_by_file(root)
    for path in sorted(grouped):
        defined = grouped[path]
        claim = header(root / path)
        if claim is None:
            found.append(
                f"{path}: defines {len(defined)} decision(s) and names none in its own "
                f"header, so a reader who opens the file is told nothing about what it holds"
            )
            continue
        declared, line = claim
        for ident in sorted(defined - declared):
            found.append(
                f"{path}:{line}: {ident} is defined in this file but its own header "
                f"does not name it"
            )
        for ident in sorted(declared - defined):
            found.append(
                f"{path}:{line}: header names {ident}, which this file does not define"
            )
    return found