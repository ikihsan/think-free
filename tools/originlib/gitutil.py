"""Thin, defensive wrappers around the git CLI.

Every helper returns plain data and never raises for an ordinary git failure:
callers decide whether a missing HEAD or a dirty tree is fatal.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from . import paths

DEFAULT_TIMEOUT = 30


@dataclass
class GitState:
    head: str = ""
    branch: str = ""
    clean: bool = True
    porcelain: list[str] = field(default_factory=list)
    available: bool = True
    error: str = ""

    def as_dict(self) -> dict:
        return {
            "head": self.head,
            "branch": self.branch,
            "clean": self.clean,
            "available": self.available,
            "error": self.error,
        }


def run(
    args: list[str],
    root: Path | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    env: dict | None = None,
) -> subprocess.CompletedProcess:
    """Run one git command.

    `env` is merged over the inherited environment, which is how a child git is
    forced non-interactive even when the parent VM exports `GIT_EDITOR`.
    """
    merged = None
    if env:
        merged = {**os.environ, **env}
    return subprocess.run(
        ["git", *args],
        cwd=str(root or paths.repo_root()),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env=merged,
    )


def detail(result) -> str:
    """The first line git printed, for an error message that can be acted on.

    A message that says only what this repository's own code did leaves the
    reader needing the run log, which for CI means repository admin rights.
    """
    text = ((getattr(result, "stderr", "") or "") + " " + (getattr(result, "stdout", "") or "")).strip()
    if not text:
        return ""
    first = next((line.strip() for line in text.splitlines() if line.strip()), "")
    return f" (git said: {first[:160]})" if first else ""


def text(args: list[str], root: Path | None = None) -> str:
    result = run(args, root)
    return result.stdout.strip() if result.returncode == 0 else ""


def dirty_paths(root=None) -> list[str]:
    """Porcelain paths, one per file.

    `--untracked-files=all` matters: the default collapses a new directory into
    a single `dir/` entry, which would make a freshly created session directory
    look like unaccounted-for work.
    """
    out = []
    result = run(["status", "--porcelain", "--untracked-files=all"], root)
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        name = line[3:].strip()
        if " -> " in name:  # rename: keep the destination
            name = name.split(" -> ")[-1].strip()
        out.append(name.strip('"'))
    return out


def rebase_in_progress(root=None) -> bool:
    base = Path(root or paths.repo_root())
    for marker in ("rebase-merge", "rebase-apply"):
        relative = text(["rev-parse", "--git-path", marker], root)
        if not relative:
            continue
        candidate = Path(relative)
        if not candidate.is_absolute():
            candidate = base / candidate
        if candidate.exists():
            return True
    return False


def state(root: Path | None = None) -> GitState:
    head = text(["rev-parse", "HEAD"], root)
    if not head:
        return GitState(
            branch="(unborn)", available=False, error="no HEAD; repository has no commits yet"
        )
    branch = text(["rev-parse", "--abbrev-ref", "HEAD"], root) or "(detached)"
    result = run(["status", "--porcelain"], root)
    if result.returncode != 0:
        return GitState(head=head, branch=branch, available=False, error=result.stderr.strip())
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return GitState(head=head, branch=branch, clean=not lines, porcelain=lines)


def changed_paths(since: str) -> list[str]:
    """Tracked paths changed since a commit, plus untracked paths."""
    root = paths.repo_root()
    found: set[str] = set()
    if since:
        result = run(["diff", "--name-only", f"{since}", "--"], root)
        if result.returncode == 0:
            found.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    result = run(["ls-files", "--others", "--exclude-standard"], root)
    if result.returncode == 0:
        found.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    result = run(["diff", "--name-only", "--cached"], root)
    if result.returncode == 0:
        found.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(found)


def is_tracked(path: str) -> bool:
    return run(["ls-files", "--error-unmatch", "--", path]).returncode == 0


def is_ignored(path: str) -> bool:
    """True when git would not track this path.

    Declaring an ignored file is always a mistake: build output is reproducible
    from the source that is being declared, and recording it adds noise to the
    record without adding evidence.
    """
    return run(["check-ignore", "--quiet", "--", path]).returncode == 0


def host_identity() -> tuple[str, str]:
    """Return (hostname, username-ish) without importing os.path surprises."""
    import getpass
    import socket

    try:
        host = socket.gethostname()
    except OSError:
        host = "unknown-host"
    try:
        user = getpass.getuser()
    except Exception:
        user = "unknown-user"
    return host, user


def describe_commit(ref: str = "HEAD") -> str:
    out = text(["log", "-1", "--format=%h %s", ref])
    return out or "(no commits)"