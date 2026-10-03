"""Filesystem layout for the origin CLI.

Single source of truth for every path the tooling touches, so that zone layout
changes happen in one file. All functions return absolute paths.
"""

from __future__ import annotations

import os
from pathlib import Path

ENV_ROOT = "ORIGIN_ROOT"

# Zone directories, relative to the repository root.
ZONES = (
    "docs",
    "sessions",
    "tasks",
    "tools",
    "tests",
    "vendor",
    ".agents",
    ".claude",
    "RESEARCH",
    "EXPERIMENTS",
)

# Root-level mission records that a session may need to update.
# The decision log is split by invariant (see DECISIONS.md); all four files are
# listed so a change to any of them is logged as a doc update.
MISSION_RECORDS = (
    "STATE.md",
    "DECISIONS.md",
    "DECISIONS-FOUNDATION.md",
    "DECISIONS-PRACTICE.md",
    "DECISIONS-GATING.md",
    "HYPOTHESES.md",
    "FAILURES.md",
    "ROADMAP.md",
    "RESEARCH.md",
    "MISSION.md",
)

EVENT_SCHEMA = "origin.session.event/1"


def repo_root() -> Path:
    """Locate the repository root.

    Honours ORIGIN_ROOT, otherwise walks up from this file, otherwise from the
    working directory. Raises SystemExit when neither yields a git repository.
    """
    override = os.environ.get(ENV_ROOT)
    if override:
        candidate = Path(override).resolve()
        if not (candidate / ".git").exists():
            raise SystemExit(f"origin: ORIGIN_ROOT={candidate} is not a git repository")
        return candidate
    starts = [Path(__file__).resolve().parent, Path.cwd().resolve()]
    for start in starts:
        for candidate in (start, *start.parents):
            if (candidate / ".git").exists():
                return candidate
    raise SystemExit("origin: not inside a git repository; set ORIGIN_ROOT")


def sessions_dir() -> Path:
    return repo_root() / "sessions"


def session_dir(session: str) -> Path:
    return sessions_dir() / session


def events_file(session: str) -> Path:
    return session_dir(session) / "events.jsonl"


def commands_log(session: str) -> Path:
    return session_dir(session) / "commands.log"


def session_report(session: str) -> Path:
    return session_dir(session) / "README.md"


def active_file() -> Path:
    """Pointer to the single in-flight session in this working tree."""
    return sessions_dir() / "active.json"


def sessions_index() -> Path:
    return sessions_dir() / "INDEX.md"


def tasks_dir() -> Path:
    return repo_root() / "tasks"


def claims_file() -> Path:
    return tasks_dir() / "CLAIMS.jsonl"


def tasks_index() -> Path:
    return tasks_dir() / "INDEX.md"


def docs_dir() -> Path:
    return repo_root() / "docs"


def docs_index() -> Path:
    return docs_dir() / "INDEX.md"


def skills_dir() -> Path:
    return repo_root() / ".agents" / "skills"


def claude_skills_dir() -> Path:
    return repo_root() / ".claude" / "skills"


def vendor_manifest() -> Path:
    return repo_root() / "vendor" / "MANIFEST.md"


def origin_dir() -> Path:
    return repo_root() / "tools"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def paths_repo_relative(path: Path) -> str:
    """Repo-relative posix path when possible, absolute otherwise."""
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
