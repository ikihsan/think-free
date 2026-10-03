"""Test harness: an isolated throwaway repository per test.

Every test gets a real git repository with the tooling copied in, so tests
exercise the same code paths the CLI does, including `git` reconciliation. No
mocks of git, no shared state between tests.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent
TOOLS = SOURCE_ROOT / "tools"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def make_repo(test: unittest.TestCase, _existing: Path | None = None) -> Path:
    """Build a minimal repository that passes `origin doc lint`."""
    if _existing is not None:
        repo = Path(_existing)
    else:
        repo = Path(tempfile.mkdtemp(prefix="origin-test-"))
        test.addCleanup(shutil.rmtree, repo, ignore_errors=True)
    shutil.copytree(TOOLS / "originlib", repo / "tools" / "originlib")
    shutil.copy2(TOOLS / "origin", repo / "tools" / "origin")
    shutil.copy2(TOOLS / "x", repo / "tools" / "x")
    (repo / "tools" / "origin").chmod(0o755)
    (repo / "tools" / "x").chmod(0o755)
    shutil.rmtree(repo / "tools" / "originlib" / "__pycache__", ignore_errors=True)
    for name in ("docs", "docs/policy", "docs/process", "sessions", "tasks", "tests"):
        (repo / name).mkdir(parents=True, exist_ok=True)
    (repo / ".gitignore").write_text(
        "__pycache__/\n*.py[cod]\n.origin/\nsessions/active.json\n", encoding="utf-8"
    )
    git(repo, "init", "-q")
    # Name the branch explicitly: git's default differs by version and config,
    # and the fleet tests need clones that share one base branch.
    git(repo, "symbolic-ref", "HEAD", "refs/heads/research/origin")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "origin-test")
    write_doc(repo / "README.md", "Test repository", "docs/INDEX.md")
    write_doc(repo / "docs" / "INDEX.md", "Documentation index", "docs/INDEX.md")
    # The generated indexes link to these by name, so a consistent test
    # repository must contain them.
    for name, title in (
        ("AGENTS.md", "Agent contract"),
        ("STATE.md", "Verified state"),
        ("MISSION.md", "Mission"),
        ("RELEASE-MANIFEST.md", "Release manifest"),
        ("docs/policy/doc-standards.md", "Documentation standards"),
        ("docs/reference/skill-inventory.md", "Skill inventory"),
        ("docs/process/session-protocol.md", "Session protocol"),
        ("docs/process/task-lifecycle.md", "Task lifecycle"),
    ):
        write_doc(repo / name, title, "docs/INDEX.md")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "initial")
    return repo


def write_doc(path: Path, title: str, owner: str, extra: str = "") -> Path:
    body = (
        f"# {title}\n\n"
        "<!-- origin-meta\n"
        f"owner: {owner}\n"
        "status: active\n"
        "last-verified: 2026-10-03\n"
        "-->\n\n"
        "Placeholder for tests.\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body + extra, encoding="utf-8")
    return path


def make_fleet(test: unittest.TestCase, vm_names: tuple[str, ...] = ("vm-a", "vm-b")) -> Path:
    """Build a bare remote plus one clone per VM name.

    A local bare repository stands in for the GitHub remote: the code under test
    only ever runs `git fetch`/`git push`, so a file path exercises the same
    atomic ref update a real remote does, with no network.
    """
    base = Path(tempfile.mkdtemp(prefix="origin-fleet-"))
    test.addCleanup(shutil.rmtree, base, ignore_errors=True)
    remote = base / "remote.git"
    remote.mkdir()
    git(remote, "init", "-q", "--bare")
    # `git init -b` needs git 2.28; a fleet VM may be older than the dev box.
    git(remote, "symbolic-ref", "HEAD", "refs/heads/research/origin")
    seed = make_repo(test, _existing=base / "seed")
    git(seed, "remote", "add", "origin", str(remote))
    git(seed, "push", "-q", "-u", "origin", "research/origin")
    for name in vm_names:
        clone = base / name
        git(base, "clone", "-q", str(remote), str(clone))
        git(clone, "config", "user.email", f"{name}@example.invalid")
        git(clone, "config", "user.name", name)
    return base


class RepoTest(unittest.TestCase):
    """Base class wiring ORIGIN_ROOT to a fresh repository."""

    def setUp(self) -> None:
        self.repo = make_repo(self)
        self._previous_root = os.environ.get("ORIGIN_ROOT")
        os.environ["ORIGIN_ROOT"] = str(self.repo)
        self.addCleanup(self._restore_root)
        # The tooling resolves paths from ORIGIN_ROOT on every call, so the
        # already-imported modules need no reloading.

    def _restore_root(self) -> None:
        if self._previous_root is None:
            os.environ.pop("ORIGIN_ROOT", None)
        else:
            os.environ["ORIGIN_ROOT"] = self._previous_root

    def use(self, root: Path) -> Path:
        """Point ORIGIN_ROOT at another clone, the way a second VM would."""
        previous = os.environ.get("ORIGIN_ROOT")
        os.environ["ORIGIN_ROOT"] = str(root)

        def restore() -> None:
            if previous is None:
                os.environ.pop("ORIGIN_ROOT", None)
            else:
                os.environ["ORIGIN_ROOT"] = previous

        self.addCleanup(restore)
        return root

    def write(self, relative: str, content: str) -> Path:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def read(self, relative: str) -> str:
        return (self.repo / relative).read_text(encoding="utf-8")

    def cli(self, *args: str) -> int:
        """Run the CLI in-process, capturing stdout."""
        from originlib.cli import main

        captured: list[str] = []
        original = sys.stdout

        class Capture:
            def write(self, text: str) -> None:
                captured.append(text)

            def flush(self) -> None:
                return None

        sys.stdout = Capture()  # type: ignore[assignment]
        self._stdout = captured
        try:
            return main(list(args))
        finally:
            sys.stdout = original  # type: ignore[assignment]

    def output(self) -> str:
        return "".join(getattr(self, "_stdout", []))

    def write_generated(self) -> None:
        """Generate the three indexes in dependency order."""
        from originlib import docindex, report, tasks

        for target, render in (
            (self.repo / "sessions" / "INDEX.md", report.render_sessions_index),
            (self.repo / "tasks" / "INDEX.md", tasks.render_tasks_index),
            (self.repo / "docs" / "INDEX.md", docindex.render),
        ):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(), encoding="utf-8")

    def session_events(self, session: str) -> list[dict]:
        from originlib import events

        root = Path(os.environ.get("ORIGIN_ROOT", str(self.repo)))
        return events.read(root / "sessions" / session / "events.jsonl")

    def kinds(self, session: str) -> list[str]:
        return [event.get("kind", "") for event in self.session_events(session)]