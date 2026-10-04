"""What an identifier definition is, and whether one number means two things.

Findings `F001…`, decisions `D001…` and tasks `T-0001…` are allocated by reading
the local tree, so two VMs working in the same hour take the same number. Seven
times on 2026-10-03 and 2026-10-04, each resolved by hand. The cost was
measured: resolving one rebase restored a file's *index* row to the renumbered
form while reverting its *body*, so one document and its own table disagreed
about the same two entries.

The collision that reached the shared base is commit `e6eb992`, which holds two
different findings both numbered `## F010` in `FAILURES-findings-2.md` and two
`| F010 |` rows in `FAILURES.md`. No gate said so. This module reads the property
those gates were not reading.

What counts as a definition, narrowly:

* a level-2 heading `## Fnnn — title` or `## Dnnn — title` in a root record
  (`FAILURES*.md`, `DECISIONS*.md`). Sub-headings, prose mentions, and session
  reports are not definitions, so a document that *talks about* `F010` cannot
  make this rule fire;
* a task file named `tasks/T-nnnn-*.md`.

This module owns that definition and the duplicate check built on it.
**Agreement between an index and the bodies it indexes lives in the module named
after each record**: `FAILURES.md` in `findingindex`, `DECISIONS.md` in
`decisionindex`, and each decision record's own `Decisions **…**` header in
`decisionheader`. All three are reached through `idcheck`, the one entry point
both publishing gates call, because a module wired into one gate is not thereby
read by the other. The split is by record rather than by size alone: two records
with the same shape and different tables are two rules, and one file holding
both is a file that grows by half each time a check is added to either.

Known limitations, stated rather than implied:

* This is a detector, not an allocator. It can refuse a commit that reuses an
  identifier; it cannot stop two VMs allocating at once, and it says nothing
  about a reference that points at the wrong entry.
* Hypothesis identifiers (`E001…` in `HYPOTHESES.md`) are out of scope. They
  have not collided, and a rule nobody has seen fire is a rule to distrust.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .finding import Finding

# `## F013 — subject`. Both dash spellings are accepted because the record uses
# an em dash throughout and a hand-typed hyphen is not a different convention.
DEFINITION = re.compile(r"^##\s+([FD]\d{3})\s+[—-]\s+(\S.*?)\s*$")
TASK_FILE = re.compile(r"^T-(\d{4})-\S+\.md$")
FINDINGS_GLOB = "FAILURES*.md"
DECISIONS_GLOB = "DECISIONS*.md"
TASKS_DIR = "tasks"


@dataclass(frozen=True)
class Definition:
    """One place that defines an identifier."""

    ident: str
    path: str
    line: int
    title: str

    def where(self) -> str:
        return f"{self.path}:{self.line}"


@dataclass(frozen=True)
class Issue:
    """One thing wrong with the identifier record.

    `path` and `line` are where a reader should look, and they are empty when
    the property spans more than one place: a number taken twice in two
    different files has no single file to open, and naming one of them would be
    a guess about which is the wrong one. `origin annotate` publishes them as
    the check-run annotation's `file` and `line`, so an honest absence here is
    an annotation on the run rather than an annotation pointing at the wrong
    document.
    """

    detail: str
    path: str = ""
    line: int = 0

    def render(self) -> str:
        return self.detail


def _read(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def _numbered(root: Path, pattern: str) -> list[Path]:
    try:
        return sorted(p for p in root.glob(pattern) if p.is_file())
    except OSError:
        return []


def definitions(root: Path) -> list[Definition]:
    """Every F and D definition in the root records, in file then line order."""
    found: list[Definition] = []
    for path in _numbered(root, FINDINGS_GLOB) + _numbered(root, DECISIONS_GLOB):
        rel = path.relative_to(root).as_posix()
        for number, line in enumerate(_read(path), start=1):
            match = DEFINITION.match(line)
            if match:
                found.append(Definition(match.group(1), rel, number, match.group(2)))
    return found


def task_definitions(root: Path) -> list[Definition]:
    """Every task identifier, defined by its file's name."""
    found: list[Definition] = []
    for path in _numbered(root, f"{TASKS_DIR}/*"):
        match = TASK_FILE.match(path.name)
        if match:
            rel = path.relative_to(root).as_posix()
            found.append(Definition(f"T-{match.group(1)}", rel, 1, ""))
    return found


def _duplicates(all_defs: list[Definition]) -> list[Issue]:
    grouped: dict[str, list[Definition]] = {}
    for item in all_defs:
        grouped.setdefault(item.ident, []).append(item)
    issues = []
    for ident in sorted(grouped):
        places = grouped[ident]
        if len(places) > 1:
            subjects = " / ".join(f"{p.where()} {p.title!r}" for p in places)
            # A file is named only when every definition is in it. Two files
            # taking one number have no single place to send a reader.
            paths = {p.path for p in places}
            where = next(iter(paths)) if len(paths) == 1 else ""
            issues.append(
                Issue(f"{ident}: defined more than once; an identifier must mean "
                      f"one thing: {subjects}", where)
            )
    return issues


def issues(root: Path) -> list[Issue]:
    """Everything wrong with the identifier record in this tree.

    The order is the order the checks are named in, and it is what both gates
    print: duplicates, then the findings index, then the decisions index.
    """
    from . import decisionindex, findingindex

    defs = definitions(root)
    tasks = task_definitions(root)
    found = _duplicates(defs + tasks)
    rows, indexed = findingindex.rows(root)
    found += findingindex.issues(defs, rows, indexed)
    found += decisionindex.issues(defs, decisionindex.rows(root))
    return found


def report(root: Path) -> list[str]:
    """Every identifier collision in the mission record, one per line.

    The lines are `Finding`s: the sentence has not changed, and each one now
    also carries the place a reader should open when they have no other way to
    see it (T-0040).
    """
    return [Finding(item.render(), item.path, item.line) for item in issues(root)]