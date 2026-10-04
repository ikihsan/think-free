"""The numbered defect list, read as the identifier record it is.

Why this module exists (defect 10 in `STATE-defects.md`, T-0036). `doc lint`
rule 7 reads findings definitions, findings index rows and decision spans. It
did not read the ordered list in `STATE-defects.md`, so T-0034 and T-0035 —
written on two VMs in the same hour — both took **defect 7** and nothing said
so. Both copies reached the shared base (`e53ca23`, `e701ad8`); the side that
had not been pushed renumbered 7 and 8 to 8 and 9 by hand in `157e463`. Until
then this file was the one document in the repository whose identifiers were
checked by reading them. Since T-0056 the list is two files and this module reads
every one of them (D046): a reader pointed at only the parent half would be blind to
a duplicate spanning the split, which is exactly the shape this rule exists to catch.

What counts as a definition: a numbered list item whose subject is bold —
`7. **A test fixture inherited the runner's environment** (solved in T-0035).`
The bold start is what distinguishes an entry from an ordinary numbered list,
and the file has no other one. Prose references ("defect 5 in
`STATE-defects.md`") are mentions, not definitions, in any document.

What the rule checks:

1. a number that defines more than one defect entry, in one file or across both;
2. a file of the list that exists and yields no entry at all. That second
   check is the load-bearing one: a parser that stops matching reports nothing
   and looks identical to a clean tree, which is how T-0030's decision-index
   check matched no row in 174 commits while the sweep was green (D025).

Known limitations, stated rather than implied:

* **A gap is not reported.** The file claims "numbering is continuous and never
  reused", so a missing number usually means an entry was dropped — but a
  withdrawn defect would produce the same shape, and the record does not
  distinguish them. Reporting the gap would be a rule whose false-positive case
  is indistinguishable from its true-positive case. Since T-0056 the list is two
  files, so a gap can straddle them as easily as sit inside one: this closes the
  *reader*, not the coverage (D046).
* Order is not checked. The list is deliberately not in ascending order:
  `7` sits in the split file while `6` is under `## Open`.
* The list is hand-maintained and has no allocator. This detects a number taken
  twice; nothing stops two VMs taking the next one at the same time.
* A numbered bold item inside a fenced code block would be read as an entry. The
  file has no such fence, and tracking fences would mean a rule that reads two
  shapes, one of which has never been needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .finding import Finding

DEFECT_FILES = ("STATE-defects.md", "STATE-defects-2.md")
# Kept for the callers and messages that speak of the list as one record.
DEFECT_FILE = DEFECT_FILES[0]

# `7. **A test fixture inherited the runner's environment** (solved in …)`. The
# closing `**` is optional so an entry whose subject wraps past its own line is
# still read: an unread entry is a number nothing checks.
ENTRY = re.compile(r"^(?P<number>\d+)\.\s+\*\*(?P<subject>\S.*?)(?:\*\*|$)")


@dataclass(frozen=True)
class Entry:
    """One place that defines a defect number."""

    number: int
    line: int
    subject: str
    source: str = DEFECT_FILE

    def where(self) -> str:
        return f"{self.source}:{self.line}"


def entries(text: str, source: str = DEFECT_FILE) -> list[Entry]:
    """Every defect entry in one file's text, in line order."""
    found: list[Entry] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = ENTRY.match(line)
        if match:
            found.append(
                Entry(
                    int(match.group("number")),
                    line_number,
                    match.group("subject").strip(),
                    source,
                )
            )
    return found


def read_all(root: Path) -> list[Entry]:
    """Every entry in every file of the list, with the file each came from.

    **The list is more than one file since T-0056**, and reading only the first
    would be the defect this rule exists to catch: the parent file's own record
    said the split could not be made without this change, and a rule that read
    one half would be blind to every entry in the other — a duplicate number
    spanning the two halves would go unreported, which is exactly what happened
    between two VMs over defect 7.
    """
    found: list[Entry] = []
    for name in DEFECT_FILES:
        path = root / name
        if not path.is_file():
            continue
        found.extend(entries(path.read_text(encoding="utf-8"), name))
    return found


def duplicate_issues(found: list[Entry]) -> list[Finding]:
    """One report per number that defines more than one entry.

    Each definition names its own file and line, so the report says which two
    entries collide. When both are in the same file that is still the honest
    report: picking one line would be a guess about which entry to renumber.
    When they span the two files the *newer* file is named, since that is where
    the entry a VM most recently added lives. `origin annotate` publishes it as a
    file-level annotation (T-0040).
    """
    grouped: dict[int, list[Entry]] = {}
    for entry in found:
        grouped.setdefault(entry.number, []).append(entry)
    issues = []
    for number in sorted(grouped):
        places = grouped[number]
        if len(places) > 1:
            where = " / ".join(f"{p.where()} {p.subject!r}" for p in places)
            newest = places[-1].source
            issues.append(
                Finding(
                    f"defect {number} defines {len(places)} defects; one number must mean "
                    f"one defect: {where}. Renumber the newer entry, on the side that has "
                    f"not been pushed",
                    newest,
                )
            )
    return issues


def unreadable_issues(present: list[str]) -> list[Finding]:
    """No entry could be read from any file of the list that exists.

    Only the files actually present are named: a tree that has one list file
    reports that one, and a tree with neither reports nothing at all, which is
    what the fixture repositories need and what `issues` decides before calling.
    """
    return [
        Finding(
            f"{name}: no defect entry could be read, so a repeated number in it "
            "would go unreported. Each entry is a numbered list item whose subject is "
            "bold, as in `7. **A defect** (solved in T-0000)`; teach this rule the new "
            "shape rather than deleting the entries (D025)",
            name,
        )
        for name in present
    ]


def issues(root: Path) -> list[Finding]:
    """Everything wrong with the defect list in this tree, as lint lines."""
    present = [name for name in DEFECT_FILES if (root / name).is_file()]
    if not present:
        # No list in this tree. The orphan and link rules read a missing
        # document; this rule reads one number meaning two defects.
        return []
    found = read_all(root)
    if not found:
        return unreadable_issues(present)
    return duplicate_issues(found)


def report(root: Path) -> list[Finding]:
    """The issues, in a stable order: by number, then by the lines that hold it."""
    return issues(root)
