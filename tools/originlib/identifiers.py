"""Identifier definitions in the mission record, and collisions between them.

Why this module exists (defect 5 in `STATE-defects.md`, T-0030). Findings
`F001…`, decisions `D001…` and tasks `T-0001…` are allocated by reading the
local tree, so two VMs working in the same hour take the same number. Seven
times on 2026-10-03 and 2026-10-04, each resolved by hand. The cost was
measured: resolving one rebase restored a file's *index* row to the renumbered
form while reverting its *body*, so one document and its own table disagreed
about the same two entries.

The collision that reached the shared base is commit `e6eb992`, which holds two
different findings both numbered `## F010` in `FAILURES-findings-2.md` and two
`| F010 |` rows in `FAILURES.md`. No gate said so. This rule reads the property
those gates were not reading.

What counts as a definition, narrowly:

* a level-2 heading `## Fnnn — title` or `## Dnnn — title` in a root record
  (`FAILURES*.md`, `DECISIONS*.md`). Sub-headings, prose mentions, and session
  reports are not definitions, so a document that *talks about* `F010` cannot
  make this rule fire;
* a task file named `tasks/T-nnnn-*.md`.

What the rule checks:

1. an identifier defined more than once;
2. a row in `FAILURES.md`'s findings index with no definition behind it, and a
   defined finding with no row — the index and the bodies are the two halves of
   the same record, and the recorded cost was one half moving without the other;
3. a decision heading in a file `DECISIONS.md` does not list, and an identifier
   `DECISIONS.md` lists that nothing defines.

Wording is deliberately **not** compared. Two rows in the current tree are
shortened paraphrases of their headings (`F009`, `F011`), which a
string-equality rule flags: an earlier draft of this check reported 83 of 162
commits, including the tip, and would have been a gate nobody ran.

Known limitations, stated rather than implied:

* This is a detector, not an allocator. It can refuse a commit that reuses an
  identifier; it cannot stop two VMs allocating at once, and it says nothing
  about a reference that points at the wrong entry.
* Hypothesis identifiers (`E001…` in `HYPOTHESES.md`) are out of scope. They
  have not collided, and a rule nobody has seen fire is a rule to distrust.
* An index row is matched on identifier alone. Renumbering every reference but
  the index row, or the reverse, is caught; a body that quotes another finding's
  subject is not.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .finding import Finding

# `## F013 — subject`. Both dash spellings are accepted because the record uses
# an em dash throughout and a hand-typed hyphen is not a different convention.
DEFINITION = re.compile(r"^##\s+([FD]\d{3})\s+[—-]\s+(\S.*?)\s*$")
FINDING_ROW = re.compile(r"^\|\s*(F\d{3})\s*\|\s*(\S.*?)\s*\|\s*$")
FINDING_INDEX_HEADER = re.compile(r"^\|\s*Id\s*\|\s*Subject\s*\|\s*$")
# The index writes its rows as Markdown links, so the path appears twice:
# `| [`DECISIONS-GATING.md`](DECISIONS-GATING.md) | D024–D029 | … |`. A regex
# that did not allow the link target matched nothing in any commit of this
# repository's history, which is the silent-gate failure a control test exists
# to catch: every other check in the sweep passed while this one did nothing.
DECISION_ROW = re.compile(
    r"^\|\s*\[?`?(DECISIONS[A-Z-]*\.md)`?\]?(?:\([^)]*\))?\s*\|\s*(.+?)\s*\|"
)
RANGE = re.compile(r"D(\d{3})\s*[–-]\s*D?(\d{3})?")
SINGLE = re.compile(r"D(\d{3})")
TASK_FILE = re.compile(r"^T-(\d{4})-\S+\.md$")
FINDINGS_GLOB = "FAILURES*.md"
DECISIONS_GLOB = "DECISIONS*.md"
TASKS_DIR = "tasks"
DECISION_INDEX = "DECISIONS.md"
FINDING_INDEX = "FAILURES.md"


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


def _finding_index(root: Path) -> tuple[dict[str, list[int]], bool]:
    """Identifier to the line numbers `FAILURES.md` indexes it at, and whether
    the index exists at all.

    The index arrived after the first findings, and this rule only compares a
    record against an index that is actually there: a sweep of all 172 commits
    on the shared base reports "F001 absent from the index" on every commit
    written before the index existed, which is a true statement about a
    different repository. A tree with findings and no index is a gap, but the
    orphan and link rules are what read that; this one reads collisions.
    """
    rows: dict[str, list[int]] = {}
    present = False
    for number, line in enumerate(_read(root / FINDING_INDEX), start=1):
        if FINDING_INDEX_HEADER.match(line):
            present = True
        match = FINDING_ROW.match(line)
        if match:
            rows.setdefault(match.group(1), []).append(number)
    return rows, present or bool(rows)


def _declared_ids(spec: str) -> set[str]:
    """Identifiers named by one `DECISIONS.md` cell, expanding ranges."""
    ids: set[str] = set()
    for low, high in RANGE.findall(spec):
        ids.update(f"D{n:03d}" for n in range(int(low), int((high or low)) + 1))
    covered = {m.start() for m in RANGE.finditer(spec)}
    for match in SINGLE.finditer(spec):
        if match.start() not in covered:
            ids.add(f"D{match.group(1)}")
    return ids


def _decision_index(root: Path) -> dict[str, set[str]]:
    """Per decision file, the identifiers `DECISIONS.md` says it holds."""
    index: dict[str, set[str]] = {}
    for line in _read(root / DECISION_INDEX):
        match = DECISION_ROW.match(line)
        if match:
            index[match.group(1)] = _declared_ids(match.group(2))
    return index


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


def _finding_index_issues(
    defs: list[Definition], rows: dict[str, list[int]], present: bool
) -> list[Issue]:
    defined = {d.ident: d for d in defs if d.ident.startswith("F")}
    if not defined or not present:
        # Nothing to compare: no findings record, or no index to compare it
        # against. See `_finding_index`.
        return []
    issues = []
    for ident in sorted(defined):
        if ident not in rows:
            item = defined[ident]
            issues.append(
                Issue(f"{ident}: defined at {item.where()} but absent from the "
                      f"{FINDING_INDEX} index", item.path, item.line)
            )
    for ident in sorted(rows):
        if ident not in defined:
            issues.append(
                Issue(f"{FINDING_INDEX}:{rows[ident][0]}: {ident} is indexed but "
                      f"nothing defines it", FINDING_INDEX, rows[ident][0])
            )
        elif len(rows[ident]) > 1:
            issues.append(
                Issue(f"{FINDING_INDEX}:{rows[ident][0]}: {ident} is indexed on "
                      f"{len(rows[ident])} lines", FINDING_INDEX, rows[ident][0])
            )
    return issues


def _decision_index_issues(defs: list[Definition], index: dict[str, set[str]]) -> list[Issue]:
    defined = {d.ident: d for d in defs if d.ident.startswith("D")}
    if not defined or not index:
        return []
    by_file: dict[str, set[str]] = {}
    for item in defs:
        if item.ident.startswith("D"):
            by_file.setdefault(item.path, set()).add(item.ident)
    issues = []
    for path in sorted(by_file):
        declared = index.get(Path(path).name)
        if declared is None:
            issues.append(Issue(f"{path}: {DECISION_INDEX} does not list this file "
                                "at all", path))
            continue
        for ident in sorted(by_file[path] - declared):
            issues.append(
                Issue(f"{path}: {ident} is defined here but not listed for this "
                      f"file in {DECISION_INDEX}", path)
            )
    listed = {ident for ids in index.values() for ident in ids}
    for ident in sorted(listed - set(defined)):
        issues.append(
            Issue(f"{DECISION_INDEX}: lists {ident} but no decision record "
                  f"defines it", DECISION_INDEX)
        )
    return issues


def issues(root: Path) -> list[Issue]:
    """Everything wrong with the identifier record in this tree."""
    defs = definitions(root)
    tasks = task_definitions(root)
    found = _duplicates(defs + tasks)
    rows, indexed = _finding_index(root)
    found += _finding_index_issues(defs, rows, indexed)
    found += _decision_index_issues(defs, _decision_index(root))
    return found


def report(root: Path) -> list[str]:
    """Every identifier collision in the mission record, one per line.

    The lines are `Finding`s: the sentence has not changed, and each one now
    also carries the place a reader should open when they have no other way to
    see it (T-0040).
    """
    return [Finding(item.render(), item.path, item.line) for item in issues(root)]