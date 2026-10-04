"""The findings index, held to the findings it indexes.

Split out of `identifiers.py` on 2026-10-04 (T-0043) when that file reached 307
of the 300 permitted lines after T-0042 and T-0040 each added to it from a
different VM and the merge concatenated both. The invariant here is one record
whose index and bodies must agree: `FAILURES.md`'s table says which findings
exist, and each finding's `## Fnnn — …` heading says what it is called. The
decisions index has the same shape and is
[`decisionindex`](decisionindex.html) — two records, two modules — while what
remains in `identifiers` is the part named after it: what a definition *is*, and
whether one number means two things.

What this reports, in both directions: a defined finding with no index row, an
index row nothing defines, and an identifier indexed on more than one line.

**The index arrived after the first findings, and this rule only compares a
record against an index that is actually there.** A sweep of all 172 commits on
the shared base reports "F001 absent from the index" on every commit written
before the index existed, which is a true statement about a different
repository. A tree with findings and no index is a gap, and the orphan and link
rules are what read that; this one reads agreement.

**Wording is deliberately not compared.** Two rows in the current tree are
shortened paraphrases of their headings (`F009`, `F011`), which a
string-equality rule flags: an earlier draft of that check reported 83 of 162
commits, including the tip, and would have been a gate nobody ran.

**Ceiling.** An index row is matched on identifier alone, so renumbering every
reference but the index row is caught and the reverse is caught too, while a
body that quotes another finding's subject is not. This is bookkeeping hygiene
with a measured cost; it says nothing about any candidate.
"""

from __future__ import annotations

import re
from pathlib import Path

from .identifiers import Definition, Issue, _read

FINDING_ROW = re.compile(r"^\|\s*(F\d{3})\s*\|\s*(\S.*?)\s*\|\s*$")
FINDING_INDEX_HEADER = re.compile(r"^\|\s*Id\s*\|\s*Subject\s*\|\s*$")
FINDING_INDEX = "FAILURES.md"


def rows(root: Path) -> tuple[dict[str, list[int]], bool]:
    """Identifier to the line numbers `FAILURES.md` indexes it at, and whether
    the index exists at all.
    """
    indexed: dict[str, list[int]] = {}
    present = False
    for number, line in enumerate(_read(root / FINDING_INDEX), start=1):
        if FINDING_INDEX_HEADER.match(line):
            present = True
        match = FINDING_ROW.match(line)
        if match:
            indexed.setdefault(match.group(1), []).append(number)
    return indexed, present or bool(indexed)


def issues(defs: list[Definition], indexed: dict[str, list[int]], present: bool) -> list[Issue]:
    """Every disagreement between the findings index and the findings."""
    defined = {d.ident: d for d in defs if d.ident.startswith("F")}
    if not defined or not present:
        return []
    found = []
    for ident in sorted(defined):
        if ident not in indexed:
            found.append(
                Issue(
                    f"{ident}: defined at {defined[ident].where()} but absent from the "
                    f"{FINDING_INDEX} index",
                    defined[ident].path,
                    defined[ident].line,
                )
            )
    for ident in sorted(indexed):
        if ident not in defined:
            found.append(
                Issue(
                    f"{FINDING_INDEX}:{indexed[ident][0]}: {ident} is indexed but nothing defines it",
                    FINDING_INDEX,
                    indexed[ident][0],
                )
            )
        elif len(indexed[ident]) > 1:
            found.append(
                Issue(
                    f"{FINDING_INDEX}:{indexed[ident][0]}: {ident} is indexed on "
                    f"{len(indexed[ident])} lines",
                    FINDING_INDEX,
                    indexed[ident][0],
                )
            )
    return found