"""The rule that a document does not contain the same table row twice.

Split out of `doclint.py` on 2026-10-04 (T-0052), when that module reached 308 of
the 300 permitted lines with this rule in it. The division is the one
`doclint.py` and `doclint_tree.py` already draw — what a rule may read — applied
one level finer, and for the same reason as the other three splits in this
repository: a file at its cap cannot take the next rule, and the next agent should
find that fact here rather than in a lint failure.

This rule is a single-file rule, so it belongs on `doclint.py`'s side of that
line, and it is separate anyway for a second reason. Its exemption is *not* a
path prefix or a file extension: it is the `generated-by: origin` marker inside
the document, because a generated session report lists an artifact once per event
and repeating it is what it is for. That is a property of the file's own first
2 KiB, which is the same thing `doclint.check_meta` reads, and keeping the rule
with its own reasoning makes the exemption visible rather than a clause someone
has to find.

What it is for, concretely: commit `eff1126` reached the shared base carrying
`STATE.md` with a byte-identical second copy of its `Implemented (2)` dashboard
row — one copy from each VM, the two branches concatenated by a rebase — and every
gate passed. A cold session reads `STATE.md` first, so the reload point showed two
rows that are one fact, and the next session removed one by hand. Defect 20 in
`STATE-defects.md`; the method is in
`../../../docs/policy/gate-falsification.md`.

**Ceiling.** Rows are compared as their exact Markdown text, so a row differing in
one cell is a different row; only pipes-delimited tables in `.md` files are read;
and the rule reads the working tree, not what a renderer would produce, so a
stale generated file is `doclint_tree`'s subject rather than this one.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import paths
from .finding import Finding

TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
# `|---|---|` is a table's structure rather than one of its rows, so two of them
# in one document is not a repeated row.
TABLE_RULE = re.compile(r"[\s:|-]+")


def _first_cell(cells: str) -> str:
    return cells.strip().strip("|").split("|")[0].strip()


def check_table_rows(result, files: list[Path]) -> None:
    """Report each row a hand-authored document already contains.

    Skips code fences (a row shown as an example is not a row), a table's
    separator line, and every generated document. A line that is not a row ends
    the table, so the same row in two tables of one document is two rows of two
    tables rather than one row twice.
    """
    from .doclint import FENCE, GENERATED_MARK

    base = paths.repo_root()
    for path in files:
        if path.suffix != ".md":
            continue
    from .doclint import FENCE, GENERATED_MARK

    base = paths.repo_root()
    for path in files:
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if GENERATED_MARK in text[:2048]:
            continue
        rel = path.relative_to(base).as_posix()
        fenced = False
        seen: dict[str, int] = {}
        for number, line in enumerate(text.splitlines(), start=1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            match = None if fenced else TABLE_ROW.match(line)
            if not match:
                seen = {}
                continue
            cells = match.group(1)
            if TABLE_RULE.fullmatch(cells):
                continue
            if cells in seen:
                result.violations.append(
                    Finding.at(
                        rel,
                        f"table row repeated from line {seen[cells]}, which makes this "
                        f"one fact shown twice; delete one ({_first_cell(cells)})",
                        number,
                    )
                )
            seen[cells] = number
