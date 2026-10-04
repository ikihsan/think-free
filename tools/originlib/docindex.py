"""Generated document index.

Covers the repository's own documentation. Vendored skill bodies are
deliberately excluded: there are far too many of them to be useful in a map,
and `docs/reference/skill-inventory.md` is their index instead.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import paths
from .doclint import GENERATED_MARK, GENERATED_NOTE, META_BLOCK

# Top-level zones summarised rather than expanded.
COLLAPSED = (".agents", ".claude", "vendor", ".git", "tools", "tests")

ZONE_ORDER = [
    ("Root records", lambda p: p.parent == paths.repo_root()),
    ("docs/policy", lambda p: p.parts[:2] == ("docs", "policy")),
    ("docs/process", lambda p: p.parts[:2] == ("docs", "process")),
    ("docs/operations", lambda p: p.parts[:2] == ("docs", "operations")),
    ("docs/reference", lambda p: p.parts[:2] == ("docs", "reference")),
    ("docs (other)", lambda p: p.parts[:1] == ("docs",) and len(p.parts) == 2),
    ("sessions", lambda p: p.parts[0] == "sessions"),
    ("tasks", lambda p: p.parts[0] == "tasks"),
    ("RESEARCH", lambda p: p.parts[0] == "RESEARCH"),
    ("EXPERIMENTS", lambda p: p.parts[0] == "EXPERIMENTS"),
]

HEAD = """# Documentation index

<!-- origin-meta
owner: docs/README.md
status: active
last-verified: {date}
-->

{GENERATED}

Every document in the repository, grouped by zone, with the index that owns it.
Regenerate with `tools/origin doc index`. Policies that govern these documents
are in [`policy/doc-standards.md`](policy/doc-standards.md).

Skill bodies under `.agents/skills/` are indexed by
[`reference/skill-inventory.md`](reference/skill-inventory.md) instead.
"""

SECTIONS = """## Start here

| Document | Purpose |
|---|---|
| [`../AGENTS.md`](../AGENTS.md) | Canonical agent contract. Read first. |
| [`../STATE.md`](../STATE.md) | Verified current state and next actions. The reload point. |
| [`../MISSION.md`](../MISSION.md) | Objective, boundaries, stopping rules. |
| [`../RELEASE-MANIFEST.md`](../RELEASE-MANIFEST.md) | What is public and what is internal. |
| [`../README.md`](../README.md) | Human front door. |
"""


def _documents() -> list[Path]:
    """Hand-written documents. Generated files are listed separately.

    Generated files are excluded on purpose: a summary of this index would
    describe content the index itself is about to replace, so rendering would
    never reach a fixed point and `doc index --check` could not be a pure read.
    """
    root = paths.repo_root()
    found: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part in rel.parts for part in COLLAPSED):
            continue
        if path.name == "INDEX.md":
            continue
        if GENERATED_MARK in path.read_text(encoding="utf-8", errors="replace"):
            continue
        found.append(path)
    return sorted(found, key=lambda p: p.relative_to(root).as_posix())


GENERATED_MAPS = (
    ("docs/INDEX.md", "This map."),
    ("sessions/INDEX.md", "Every recorded session and its outcome."),
    ("tasks/INDEX.md", "Dispatchable tasks and their claims."),
)


def _meta_of(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = META_BLOCK.search(text)
    if not match:
        return {}
    out: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


def _first_paragraph(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("#"):
            continue
        for follow in lines[index + 1 :]:
            stripped = follow.strip()
            if not stripped or stripped.startswith(("<!--", "|", "```")):
                continue
            return re.sub(r"[*`_]", "", stripped)[:96]
    return ""


def _link(root: Path, path: Path, index_file: Path) -> str:
    """Markdown link valid from the index file's own directory."""
    import os

    rel = path.relative_to(root).as_posix()
    target = os.path.relpath(rel, start=str(index_file.parent.relative_to(root)))
    return f"[`{rel}`]({target})"


def index_stamp(docs: list[Path]) -> str:
    """The newest `last-verified` among the documents this index lists.

    Taken from the tree rather than from the clock, so regenerating the index on
    a later day produces the same bytes and `doc lint` does not call every
    committed index stale the morning after it was written.
    """
    stamps = [_meta_of(path).get("last-verified", "") for path in docs]
    return max([stamp for stamp in stamps if stamp], default="unknown")


def write_index() -> bool:
    """Write `docs/INDEX.md` if the render differs. True when it wrote.

    Called by `origin doc index` and by the task commands, because a new task
    file is a new document: without a rebuilt index the orphan rule rejects the
    tree, which reddened two CI runs on 2026-10-03 (`STATE-defects.md` defect 5).
    """
    from .report import write_if_changed

    return write_if_changed(paths.docs_index(), render())


def render() -> str:
    index_file = paths.docs_index()
    root = paths.repo_root()
    docs = _documents()
    lines = [HEAD.format(date=index_stamp(docs), GENERATED=GENERATED_NOTE), SECTIONS]
    for title, predicate in ZONE_ORDER:
        group = [p for p in docs if predicate(p.relative_to(root))]
        if not group:
            continue
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| Document | Owner index | Status | Verified | Summary |")
        lines.append("|---|---|---|---|---|")
        for path in group:
            meta = _meta_of(path)
            lines.append(
                "| "
                + " | ".join(
                    [
                        _link(root, path, index_file),
                        f"`{meta.get('owner', '—')}`",
                        meta.get("status", "—"),
                        meta.get("last-verified", "—"),
                        _first_paragraph(path),
                    ]
                )
                + " |"
            )
        lines.append("")
    lines += ["## Generated maps", ""]
    lines += ["| Map | Purpose |", "|---|---|"]
    lines += [f"| `{name}` | {purpose} |" for name, purpose in GENERATED_MAPS]
    lines += [""]
    lines += [
        "## Adding a document",
        "",
        "1. Give it an `origin-meta` block with its owning index.",
        "2. Link it from exactly one index; orphans fail `doc lint`.",
        "3. Keep it under 300 lines. Split at 250.",
        "",
    ]
    text = "\n".join(lines)
    return text if text.endswith("\n") else text + "\n"
