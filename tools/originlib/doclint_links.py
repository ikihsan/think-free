"""Rule 3: a relative link resolves, and it resolves inside this repository.

Split out of `doclint.py` on 2026-10-14, when the exemption that lets a link rule
honour `vendor/MANIFEST.md` pushed that module to 312 of the 300 permitted
lines. The division is the one `doclint.py` and `doclint_tree.py` already draw —
what a rule may read — applied to the rule that has the most to say about what it
may not read. See [`doc-standards.md`](../../docs/policy/doc-standards.md).

Two things in here are not obvious and were both paid for:

* The existence check is the only filesystem read, and it is asked of a path that
  has already been shown to be inside the repository. Before T-0051 the
  candidates were tested for existence wherever they landed, so a link written as
  `../../docs/x.md` from `tasks/` was decided by whether the *checkout's parent
  directory* held `docs/x.md` — a green lint in `.worktrees/<name>/` and a red
  one in the main checkout, from identical bytes (D041, defect 19).
* Declared-exempt files are skipped. E125 committed 30 READMEs fetched from other
  people's repositories, and their internal links (`docs/`, `examples/`,
  `/aiopslab/...`) name *that* repository and can never resolve in this one. A
  rule that reads a third party's document as this repository's document reported
  402 violations that no edit to an authored file could ever clear, and clearing
  them would mean rewriting upstream bytes — which is the thing the evidence copy
  exists to prevent. The exemption is a declared glob, so it covers the class and
  nothing else.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from . import paths
from .doclint import LINK, FENCE, Finding, Result, declared_exemptions, is_exempt


def links(text: str) -> list[tuple[str, int]]:
    """Markdown links outside fenced code blocks, with the line each is on.

    Renamed from the private `_links` on 2026-10-14 because the control in
    `tests/test_link_escape.py` reads the tree through this function and a
    control that has to reach into a private is a control that does not get run.
    """
    found: list[tuple[str, int]] = []
    fenced = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        found.extend((target, number) for target in LINK.findall(line))
    return found


def inside_repository(candidate: Path, base: Path) -> bool:
    """Whether `candidate` names a path inside the repository, decided lexically.

    `os.path.relpath` is the right tool because it never touches the filesystem:
    containment is a question about the link and the root, and a question answered
    by `Path.resolve()` would follow symlinks and read the disk again, which is
    the property D041 exists to remove. A `ValueError` means the two paths share
    no root at all (a different drive on Windows), which is the same answer.
    """
    try:
        relative = os.path.relpath(str(candidate), str(base))
    except ValueError:
        return False
    return relative != os.pardir and not relative.startswith(os.pardir + os.sep)


def check_links(result: Result, files: list[Path], globs: list[str] | None = None) -> None:
    """A relative link resolves, and resolves to a document of this repository."""
    base = paths.repo_root()
    globs = globs if globs is not None else declared_exemptions()
    for path in files:
        if path.suffix != ".md":
            continue
        rel = path.relative_to(base).as_posix()
        if is_exempt(rel, globs):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for target, line in links(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            candidates = [(path.parent / clean), (base / clean)]
            inside = [one for one in candidates if inside_repository(one, base)]
            if not inside:
                result.violations.append(
                    Finding.at(rel, f"link leaves the repository -> {target}", line)
                )
            elif not any(one.exists() for one in inside):
                result.violations.append(
                    Finding.at(rel, f"broken link -> {target}", line)
                )
