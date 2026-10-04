"""Documentation lint.

Rules, in the order they are reported:

1. line cap for every tracked file, with two declared exemption classes
2. `origin-meta` block on every Markdown file
3. relative links must resolve, and inside this repository (rule extended in
   T-0051 after a link that escaped the root was judged by what sat above the
   checkout; D041, defect 19 in `STATE-defects.md`)
4. no orphan documents
5. generated files must match what the generators produce now
6. no unresolved merge-conflict marker (rule added in T-0021 after three
   mission records reached the shared base with one; `FAILURES.md` F013)
7. no identifier defined twice, and no index row or decision entry that the
   body does not back (rule added in T-0030 after commit `e6eb992` reached the
   shared base with two findings numbered F010; defect 5 in `STATE-defects.md`)

Rules 1–3 decide from one file and live here; rules 4–7 decide from the
repository as a whole and live in `doclint_tree`, split out on 2026-10-04
(T-0040) when this module reached 299 of the 300 permitted lines. Which side a
rule is on tells you what it may read, and therefore whether it can be run on
its own — a property that matters here, because a rule reading the wrong thing
is the recorded cause of defect 10.

Every violation is a `finding.Finding`: the text this linter has always printed,
plus the file and line the rule that found it knows. The location is what
`origin annotate` publishes as a check-run annotation, and it is carried
structurally because parsing it back out of the text is the shape of mistake
D025 describes.

Exit code 2 signals a violation. Exempt files are reported as `info` so an
exception is never invisible.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import paths
from .docfiles import tracked_files
from .finding import Finding

MAX_LINES = 300
# Machine-generated data and raw logs are exempt from the cap by extension.
DATA_SUFFIXES = {".json", ".jsonl", ".log"}
EXEMPT_PREFIX = "exempt:"
META_KEYS = ("owner", "status", "last-verified")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")
META_BLOCK = re.compile(r"<!--\s*origin-meta\s*(.*?)-->", re.DOTALL)
COMMENT_BLOCK = re.compile(r"<!--.*?-->", re.DOTALL)
YAML_FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
# Skill documents use Agent Skills YAML frontmatter, which origin-meta
# must not precede: agents parse the frontmatter from the first line.
SKILL_FILE = re.compile(r"^\.agents/skills/[^/]+/SKILL\.md$")
GENERATED_MARK = "<!-- generated-by:"
GENERATED_NOTE = "<!-- generated-by: origin; do not edit by hand -->"


@dataclass
class Result:
    violations: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)
    checked: int = 0

    @property
    def ok(self) -> bool:
        return not self.violations

    def render(self) -> str:
        lines = [f"doc lint: {self.checked} file(s) checked"]
        for info in self.infos:
            lines.append(f"  info  {info}")
        for problem in self.violations:
            lines.append(f"  FAIL  {problem}")
        lines.append("doc lint: OK" if self.ok else f"doc lint: {len(self.violations)} violation(s)")
        return "\n".join(lines)


def declared_exemptions() -> list[str]:
    """Globs declared in vendor/MANIFEST.md as `exempt: <glob>` lines."""
    manifest = paths.vendor_manifest()
    if not manifest.exists():
        return []
    globs: list[str] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(EXEMPT_PREFIX):
            globs.append(stripped[len(EXEMPT_PREFIX) :].strip())
    return globs


def is_exempt(rel: str, globs: list[str]) -> bool:
    if Path(rel).suffix in DATA_SUFFIXES:
        return True
    for glob in globs:
        if _glob_match(rel, glob):
            return True
    return False


def _glob_match(rel: str, pattern: str) -> bool:
    import fnmatch

    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return rel == prefix or rel.startswith(prefix + "/")
    return fnmatch.fnmatch(rel, pattern)


def check_line_cap(result: Result, files: list[Path], globs: list[str]) -> None:
    for path in files:
        rel = path.relative_to(paths.repo_root()).as_posix()
        try:
            count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            continue
        if is_exempt(rel, globs):
            if count > MAX_LINES:
                result.infos.append(f"{rel}: {count} lines (exempt from cap)")
            continue
        if count > MAX_LINES:
            result.violations.append(
                Finding.at(
                    rel,
                    f"{count} lines exceeds the {MAX_LINES}-line cap; "
                    "split it (see docs/policy/doc-standards.md)",
                )
            )


def check_meta(result: Result, files: list[Path], globs: list[str]) -> None:
    """Every Markdown document has a title, and declares origin-meta.

    Two exemptions, both structural rather than discretionary:

    * Vendored skills are exempt from both rules because their frontmatter is
      Agent Skills YAML, which must come first, and because their document
      shape belongs to upstream.
    * `SKILL.md` files are exempt from origin-meta for the same frontmatter
      reason, and are still required to have a level-1 title.
    """
    base = paths.repo_root()
    for path in files:
        if path.suffix != ".md":
            continue
        rel = path.relative_to(base).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if is_exempt(rel, globs):
            continue
        stripped = COMMENT_BLOCK.sub("", YAML_FRONTMATTER.sub("", text))
        first = next((line.strip() for line in stripped.splitlines() if line.strip()), "")
        if not first.startswith("# "):
            result.violations.append(Finding.at(rel, "must start with a level-1 title"))
        if SKILL_FILE.match(rel):
            continue
        match = META_BLOCK.search(text)
        if not match:
            result.violations.append(Finding.at(rel, "missing <!-- origin-meta --> block"))
            continue
        block = match.group(1)
        missing = [key for key in META_KEYS if not re.search(rf"^\s*{key}\s*:", block, re.MULTILINE)]
        if missing:
            result.violations.append(
                Finding.at(rel, f"origin-meta missing key(s): {', '.join(missing)}")
            )


def _links(text: str) -> list[tuple[str, int]]:
    """Markdown links outside fenced code blocks, with the line each is on."""
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


def _inside_repository(candidate: Path, base: Path) -> bool:
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


def check_links(result: Result, files: list[Path]) -> None:
    """Rule 3: a relative link resolves, and resolves to a document of this repository.

    The existence check is the only filesystem read, and it is asked of a path
    that has already been shown to be inside the repository. Before T-0051 the
    candidates were tested for existence wherever they landed, so a link written
    as `../../docs/x.md` from `tasks/` was decided by whether the *checkout's
    parent directory* held `docs/x.md` — a green lint in `.worktrees/<name>/` and
    a red one in the main checkout, from identical bytes (D041, defect 19).
    """
    base = paths.repo_root()
    for path in files:
        if path.suffix != ".md":
            continue
        rel = path.relative_to(base).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for target, line in _links(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            candidates = [(path.parent / clean), (base / clean)]
            inside = [one for one in candidates if _inside_repository(one, base)]
            if not inside:
                result.violations.append(
                    Finding.at(rel, f"link leaves the repository -> {target}", line)
                )
            elif not any(one.exists() for one in inside):
                result.violations.append(
                    Finding.at(rel, f"broken link -> {target}", line)
                )


def lint(root: Path | None = None) -> Result:
    from . import doclint_tree

    files = tracked_files(root)
    result = Result(checked=len(files))
    globs = declared_exemptions()
    check_line_cap(result, files, globs)
    check_meta(result, files, globs)
    check_links(result, files)
    doclint_tree.check_orphans(result, files, globs)
    doclint_tree.check_generated(result)
    doclint_tree.check_conflicts(result, files)
    doclint_tree.check_identifiers(result)
    return result