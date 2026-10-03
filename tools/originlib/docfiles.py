"""Which files in the tree count as repository content.

Split out of `doclint.py` so the linter stays under the repository's line cap.
The rule the whole documentation gate rests on: a path git would not track is not
a document, so it cannot fail the line cap, carry origin-meta, or be an orphan.

That rule is not a preference. `session artifact` already refuses to declare a
gitignored path, because build output is reproducible from the source that
declares it (F004), and an experiment that downloads its inputs pins them by hash
in `sources.json` rather than committing third-party tarballs. When the linter did
not agree, `008-build-timestamp-attribution` had to choose between committing four
sdists and failing the cap.
"""

from __future__ import annotations

from pathlib import Path

from . import paths

# Directories never walked: git's own, and the toolchain's build output.
SKIP_DIRS = {".git", "__pycache__", ".worktrees", "node_modules", ".claude"}


def _skip(path: Path, base: Path) -> bool:
    rel = path.relative_to(base)
    return any(part in SKIP_DIRS for part in rel.parts)


def _ignored_paths(relatives: list[str]) -> set[str]:
    """Which of these paths git would not track, in one subprocess.

    Batched rather than one call per file: the linter walks hundreds of paths and
    a subprocess each would cost more than the lint. A non-zero exit other than
    1 means the question could not be answered, and the answer is then "nothing is
    ignored" — the stricter reading, so a real violation cannot hide behind a
    broken git invocation.
    """
    import subprocess

    if not relatives:
        return set()
    try:
        done = subprocess.run(
            ["git", "check-ignore", "--stdin", "-z"],
            input="\0".join(relatives) + "\0",
            capture_output=True, text=True, cwd=str(paths.repo_root()),
        )
    except OSError:
        return set()
    if done.returncode not in (0, 1):
        return set()
    return {entry for entry in done.stdout.split("\0") if entry}


def tracked_files(root: Path | None = None) -> list[Path]:
    """Every file git would consider part of the repository."""
    base = root or paths.repo_root()
    candidates = [
        path for path in sorted(base.rglob("*"))
        if path.is_file() and not _skip(path, base)
    ]
    ignored = _ignored_paths([p.relative_to(base).as_posix() for p in candidates])
    return [
        path for path in candidates
        if path.relative_to(base).as_posix() not in ignored
    ]