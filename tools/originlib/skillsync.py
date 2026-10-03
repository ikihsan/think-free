"""Skill layout: naming rules, cross-agent mirroring, and vendor drift.

Canonical skills live in `.agents/skills/<name>/SKILL.md`. `.claude/skills/`
holds one symlink per skill because Claude Code reads only that directory,
while Codex, Gemini, Cursor, and OpenCode read `.agents/skills/` directly.
Linking the whole directory is avoided: Codex writes internal files there.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import paths

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
# Claude Code refuses to load these, so they must never be used here.
RESERVED = {"synced", "anthropic-skills"}
# Fields the Agent Skills specification defines. Claude Code's packaging path
# rejects anything else, so unknown keys are reported rather than ignored.
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
LINK_TARGET = "../../.agents/skills"


@dataclass
class Report:
    problems: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    skills: int = 0

    @property
    def ok(self) -> bool:
        return not self.problems

    def render(self) -> str:
        lines = [f"skills: {self.skills} skill(s) in .agents/skills"]
        for warning in self.warnings:
            lines.append(f"  warn  {warning}")
        for problem in self.problems:
            lines.append(f"  FAIL  {problem}")
        lines.append("skills: OK" if self.ok else f"skills: {len(self.problems)} problem(s)")
        return "\n".join(lines)


def skill_dirs() -> list[Path]:
    root = paths.skills_dir()
    if not root.exists():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    key = None
    for line in match.group(1).splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        elif key and line.strip():
            fields[key] = f"{fields[key]} {line.strip()}".strip()
    return fields


def check() -> Report:
    report = Report()
    root = paths.skills_dir()
    if not root.exists():
        report.problems.append(".agents/skills does not exist")
        return report
    names: set[str] = set()
    for directory in skill_dirs():
        report.skills += 1
        name = directory.name
        rel = f".agents/skills/{name}"
        if name in RESERVED or name.startswith("anthropic-skills"):
            report.problems.append(f"{rel}: reserved skill name")
        if not NAME.match(name):
            report.problems.append(f"{rel}: name must match {NAME.pattern}")
        if len(name) > MAX_NAME:
            report.problems.append(f"{rel}: name longer than {MAX_NAME} characters")
        if name in names:
            report.problems.append(f"{rel}: duplicate skill name")
        names.add(name)
        fields = frontmatter(directory / "SKILL.md")
        if not fields:
            report.problems.append(f"{rel}/SKILL.md: missing YAML frontmatter")
            continue
        if fields.get("name") != name:
            report.problems.append(
                f"{rel}/SKILL.md: frontmatter name {fields.get('name')!r} != directory {name!r}"
            )
        description = fields.get("description", "")
        if not description:
            report.problems.append(f"{rel}/SKILL.md: description is required")
        elif len(description) > MAX_DESCRIPTION:
            report.problems.append(f"{rel}/SKILL.md: description exceeds {MAX_DESCRIPTION} characters")
        unknown = sorted(set(fields) - SPEC_FIELDS)
        if unknown:
            report.warnings.append(f"{rel}/SKILL.md: non-spec frontmatter key(s): {', '.join(unknown)}")
    report.problems.extend(_check_mirrors(names))
    return report


def _check_mirrors(names: set[str]) -> list[str]:
    problems: list[str] = []
    claude_dir = paths.claude_skills_dir()
    if not claude_dir.exists():
        return [".claude/skills does not exist; Claude Code will not find any skill"]
    entries = {p.name: p for p in claude_dir.iterdir() if p.is_dir() or p.is_symlink()}
    for name in sorted(names):
        path = entries.get(name)
        if path is None:
            problems.append(f".claude/skills/{name}: missing mirror for .agents/skills/{name}")
            continue
        if path.is_symlink():
            target = Path(path).resolve()
            expected = (paths.skills_dir() / name).resolve()
            if target != expected:
                problems.append(
                    f".claude/skills/{name}: symlink points at {target} instead of {expected}"
                )
        elif not (path / "SKILL.md").exists():
            problems.append(f".claude/skills/{name}: real directory without SKILL.md")
    for name in sorted(set(entries) - names):
        problems.append(f".claude/skills/{name}: mirror with no canonical skill in .agents/skills")
    return problems


def sync(use_copies: bool = False) -> Report:
    """Create missing mirrors. Symlinks by default; copies with use_copies."""
    claude_dir = paths.claude_skills_dir()
    claude_dir.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for directory in skill_dirs():
        target = claude_dir / directory.name
        if target.exists() or target.is_symlink():
            continue
        if use_copies:
            _copy_tree(directory, target)
        else:
            target.symlink_to(Path(LINK_TARGET) / directory.name, target_is_directory=True)
        created.append(directory.name)
    report = check()
    if created and report.ok:
        report.warnings.append(f"created {len(created)} mirror(s): {', '.join(sorted(created))}")
    return report


def _copy_tree(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for item in sorted(source.rglob("*")):
        relative = item.relative_to(source)
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(item.read_bytes())


# ----------------------------------------------------------------- vendoring


def hashes_path() -> Path:
    return paths.repo_root() / "vendor" / "hashes.json"


def digest_tree(root: Path) -> dict[str, str]:
    """sha256 per file, keyed by path relative to root, sorted by key."""
    out: dict[str, str] = {}
    if not root.exists():
        return out
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        out[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def write_hashes() -> Path:
    """Record hashes for declared vendored skills only.

    Authored skills are excluded on purpose: they are meant to change, and
    recording them would report every legitimate edit as tampering.
    """
    declared = sorted(declared_vendored() & {p.name for p in skill_dirs()})
    payload = {
        "schema": "origin.vendor.hashes/1",
        "generated": events_now(),
        "skills": {name: digest_tree(paths.skills_dir() / name) for name in declared},
    }
    target = hashes_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def events_now() -> str:
    from . import events

    return events.now_iso()


def verify_vendor() -> Report:
    """Compare current vendored skill contents against recorded hashes.

    Detects local modification of vendored files. Cannot detect upstream
    movement without network access; that check is documented as a separate
    manual step in vendor/MANIFEST.md.
    """
    report = Report()
    target = hashes_path()
    if not target.exists():
        report.problems.append("vendor/hashes.json missing; run 'tools/origin skills hash'")
        return report
    recorded = json.loads(target.read_text(encoding="utf-8")).get("skills", {})
    declared = declared_vendored()
    for name in sorted(recorded):
        if name not in declared:
            report.warnings.append(f"{name}: recorded as vendored upstream but not declared in MANIFEST.md")
            continue
        current = digest_tree(paths.skills_dir() / name)
        expected = recorded[name]
        for missing in sorted(set(expected) - set(current)):
            report.problems.append(f"{name}: vendored file removed: {missing}")
        for added in sorted(set(current) - set(expected)):
            report.warnings.append(f"{name}: local file added since hashing: {added}")
        for changed in sorted(set(current) & set(expected)):
            if current[changed] != expected[changed]:
                report.problems.append(f"{name}: vendored file modified: {changed}")
        report.skills += 1
    return report


def declared_vendored() -> set[str]:
    """Skill names declared as vendored via `vendored: <name>` in the manifest."""
    manifest = paths.vendor_manifest()
    if not manifest.exists():
        return set()
    names = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("vendored:"):
            names.add(stripped.split(":", 1)[1].strip())
    return names


def authored() -> set[str]:
    return {p.name for p in skill_dirs()} - declared_vendored()