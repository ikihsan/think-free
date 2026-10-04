"""The decisions index, held to the decisions it indexes.

Split out of `identifiers.py` on 2026-10-04 (T-0043) when that file reached 307
of the 300 permitted lines after T-0042 and T-0040 each added to it from a
different VM and the merge concatenated both. The invariant here is one record
whose index and bodies must agree: `DECISIONS.md`'s table says which decision
file holds which numbers, and each record's `## Dnnn — …` headings say which
numbers it holds. The findings index has the same shape and is
[`findingindex`](findingindex.html) — two records, two modules — while what
remains in `identifiers` is the part named after it: what a definition *is*, and
whether one number means two things.

**This check found a gap in itself on its first run.** It reported D030 missing
from its index row ten minutes after D030 was written, because the decision had
been recorded and the row had not. A table that describes a log is as much a
record as the log, and the same property applies to the third source of a
decision number, each record's own `Decisions **…**` header, which is
[`decisionheader`](decisionheader.html)'s.

**The regex allows a Markdown link, because the index writes its rows as one.**
A first version did not, and matched nothing in any commit of this repository's
history: every other check in the sweep passed while this one did nothing, which
is the silent-gate failure a control test exists to catch.

**Wording is deliberately not compared**, for the reason in
[`findingindex`](findingindex.html): two rows in the current tree are shortened
paraphrases of their headings on purpose.

**Ceiling.** A range is expanded to the numbers it covers, so a header or a row
that says `D011–D018` for a file that does not define D013 is reported — which
is the whole point, since T-0040's reversed split moved entries out of the middle
of such a range and nothing said so. This module reads the index table only; a
row's `Governs` prose is not compared with the invariant its file states.
"""

from __future__ import annotations

import re
from pathlib import Path

from .identifiers import Definition, Issue, _read

# `| [`DECISIONS-GATING.md`](DECISIONS-GATING.md) | D024–D029 | … |`. The link
# target appears twice, so a regex that did not allow it matched no row at all.
DECISION_ROW = re.compile(
    r"^\|\s*\[?`?(DECISIONS[A-Z-]*\.md)`?\]?(?:\([^)]*\))?\s*\|\s*(.+?)\s*\|"
)
RANGE = re.compile(r"D(\d{3})\s*[–-]\s*D?(\d{3})?")
SINGLE = re.compile(r"D(\d{3})")
DECISION_INDEX = "DECISIONS.md"


def declarations(spec: str) -> set[str]:
    """Identifiers named by one specification cell, expanding ranges.

    One implementation, read by this module's index check and by
    `decisionheader`, which parses the same `D011–D018, D027–D028` shape in a
    decision record's own header. Two parsers for one notation would be two
    things to teach a new spelling to.
    """
    ids: set[str] = set()
    for low, high in RANGE.findall(spec):
        ids.update(f"D{n:03d}" for n in range(int(low), int((high or low)) + 1))
    covered = {m.start() for m in RANGE.finditer(spec)}
    for match in SINGLE.finditer(spec):
        if match.start() not in covered:
            ids.add(f"D{match.group(1)}")
    return ids


def rows(root: Path) -> dict[str, set[str]]:
    """Per decision file, the identifiers `DECISIONS.md` says it holds."""
    index: dict[str, set[str]] = {}
    for line in _read(root / DECISION_INDEX):
        match = DECISION_ROW.match(line)
        if match:
            index[match.group(1)] = declarations(match.group(2))
    return index


def issues(defs: list[Definition], index: dict[str, set[str]]) -> list[Issue]:
    """Every disagreement between the decisions index and the decisions."""
    defined = {d.ident: d for d in defs if d.ident.startswith("D")}
    if not defined or not index:
        return []
    by_file: dict[str, set[str]] = {}
    for item in defs:
        if item.ident.startswith("D"):
            by_file.setdefault(item.path, set()).add(item.ident)
    found = []
    for path in sorted(by_file):
        declared = index.get(Path(path).name)
        if declared is None:
            found.append(
                Issue(f"{path}: {DECISION_INDEX} does not list this file at all", path)
            )
            continue
        for ident in sorted(by_file[path] - declared):
            found.append(
                Issue(f"{path}: {ident} is defined here but not listed for this "
                      f"file in {DECISION_INDEX}", path)
            )
    listed = {ident for ids in index.values() for ident in ids}
    for ident in sorted(listed - set(defined)):
        found.append(
            Issue(f"{DECISION_INDEX}: lists {ident} but no decision record defines it",
                  DECISION_INDEX)
        )
    return found