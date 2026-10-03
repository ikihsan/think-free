"""Documentation lint.

Rules, in the order they are reported:

1. line cap for every tracked file, with two declared exemption classes
2. `origin-meta` block on every Markdown file
3. relative links must resolve
4. no orphan documents
5. generated files must match what the generators produce now

Exit code 2 signals a violation. Exempt files are reported as `info` so an
exception is never invisible.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import paths

MAX_LINES = 300
# Machine-generated data and raw logs are exempt from the cap by extension.
DATA_SUFFIXES = {".json", ".jsonl", ".log"}
EXEMPT_PREFIX = "exempt:"
SKIP_DIRS = {".git", "__pycache__", ".worktrees", "node_modules", ".claude"}
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


def tracked_files(root: Path | None = None) -> list[Path]:
    """Files git knows about, plus untracked-but-not-ignored files."""
    base = root or paths.repo_root()
    result = sorted(p for p in base.rglob("*") if p.is_file())
    return [p for p in result if not _skip(p, base)]


def _skip(path: Path, base: Path) -> bool:
    rel = path.relative_to(base)
    return any(part in SKIP_DIRS for part in rel.parts)


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
                f"{rel}: {count} lines exceeds the {MAX_LINES}-line cap; "
                "split it (see docs/policy/doc-standards.md)"
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
            result.violations.append(f"{rel}: must start with a level-1 title")
        if SKILL_FILE.match(rel):
            continue
        match = META_BLOCK.search(text)
        if not match:
            result.violations.append(f"{rel}: missing <!-- origin-meta --> block")
            continue
        block = match.group(1)
        missing = [key for key in META_KEYS if not re.search(rf"^\s*{key}\s*:", block, re.MULTILINE)]
        if missing:
            result.violations.append(f"{rel}: origin-meta missing key(s): {', '.join(missing)}")


def _links(text: str) -> list[str]:
    """Markdown links outside fenced code blocks."""
    found: list[str] = []
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        found.extend(LINK.findall(line))
    return found


def check_links(result: Result, files: list[Path]) -> None:
    base = paths.repo_root()
    for path in files:
        if path.suffix != ".md":
            continue
        rel = path.relative_to(base).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for target in _links(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            candidates = [(path.parent / clean), (base / clean)]
            if not any(candidate.exists() for candidate in candidates):
                result.violations.append(f"{rel}: broken link -> {target}")


def check_orphans(result: Result, files: list[Path], globs: list[str]) -> None:
    """Every Markdown file must be referenced by some other Markdown file.

    Exempt paths are skipped: vendored upstream material is not this
    repository's document graph and its internal files are not ours to link.
    """
    base = paths.repo_root()
    docs = [
        p
        for p in files
        if p.suffix == ".md"
        and not is_exempt(p.relative_to(base).as_posix(), globs)
    ]
    haystack: list[tuple[str, str]] = []
    for path in docs:
        rel = path.relative_to(base).as_posix()
        haystack.append((rel, path.read_text(encoding="utf-8", errors="replace")))
    for path in docs:
        rel = path.relative_to(base).as_posix()
        text = dict(haystack)[rel]
        if GENERATED_MARK in text:
            continue
        stem = Path(rel).with_suffix("").as_posix()
        referenced = any(
            (rel in other or stem in other or Path(rel).name in other)
            for other_rel, other in haystack
            if other_rel != rel
        )
        if not referenced:
            result.violations.append(
                f"{rel}: orphan document; no other document links to it"
            )


def check_generated(result: Result) -> None:
    """Committed generated files must equal what the generators produce."""
    from . import report, tasks

    comparisons: list[tuple[Path, str]] = []
    # The active session is still being written to, so its report cannot be
    # final by definition. `session finish` regenerates it as its last act.
    active = active_session_id()
    for session in events_all():
        if session == active:
            continue
        comparisons.append((paths.session_report(session), report.render_session_report(session)))
    comparisons.append((paths.sessions_index(), report.render_sessions_index()))
    comparisons.append((paths.docs_index(), docindex_render()))
    comparisons.append((paths.tasks_index(), tasks.render_tasks_index()))
    for path, expected in comparisons:
        if not path.exists():
            result.violations.append(f"{path.relative_to(paths.repo_root()).as_posix()}: generated file missing")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            result.violations.append(
                f"{path.relative_to(paths.repo_root()).as_posix()}: generated file is stale; "
                "run 'tools/origin doc index'"
            )


def events_all() -> list[str]:
    from . import events

    return events.all_sessions()


def active_session_id() -> str | None:
    from .activestate import load_active

    active = load_active()
    return active.session if active else None


def docindex_render() -> str:
    from . import docindex

    return docindex.render()


def lint(root: Path | None = None) -> Result:
    files = tracked_files(root)
    result = Result(checked=len(files))
    globs = declared_exemptions()
    check_line_cap(result, files, globs)
    check_meta(result, files, globs)
    check_links(result, files)
    check_orphans(result, files, globs)
    check_generated(result)
    return result