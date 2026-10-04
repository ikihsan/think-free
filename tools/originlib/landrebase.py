"""The state of a rebase `land` stopped on, and how to finish it.

Split out of `syncland.py` on 2026-10-04 (T-0048) when that file reached 310 of the
300 permitted lines, and by the same division `doclint.py` used: what a step is
allowed to *read* about git's state, separated from what it does about it.

`land` is the one operation here that stops on a real conflict and asks a human to
resolve it. Until T-0048 that left the reader with an instruction its own tooling
could not carry out: the second `land` refuses on a dirty tree, and resolving the
conflict is what makes the tree dirty. So the only way out was
`git rebase --continue` by hand, which records no `base_advance`, and every path the
base brought was attributed to the session that resolved the conflict. That is
defect 2's stated ceiling — reconciliation cannot see a hand-run rebase — and it was
reached through a refusal message rather than by anybody's mistake.

Three questions have to be answered before continuing, and each has a wrong answer
that looks like a working one:

* **Is a rebase in progress?** Both git backends are checked, and the marker
  directory differs by version: this VM's 2.25 writes `rebase-apply` where 2.26
  writes `rebase-merge`. Reading only one of them is a check that passes on half the
  machines and looks deliberate.
* **Is a path still conflicted?** Until none is, the continuation is not ours to
  run. The refusal names the path, because a reader who cannot tell which file
  disagrees is left with `git status` and nothing else.
* **What was this branch's tip before the rebase began?** Not `HEAD`: mid-rebase,
  `HEAD` is the base with this branch's earlier commits already on it, so
  `before..base` computed from it names nothing and every arriving path looks like
  this session's own change. Git recorded the real tip in `orig-head` when the
  rebase started, and that file is deleted when it finishes — so it is read *before*
  the continuation, not after.

**Ceiling.** Nothing here decides *whether* a rebase was land's to begin: a rebase
the operator started by hand is resumed just the same, because the state git
records is indistinguishable from one this flow started. And a dirty path that is
staged but not committed is the resolution itself, so it is taken; a path that is
dirty and *not* staged is refused, because the continuation commits the whole index
and would sweep it into the rebase's commit rather than the one that names it.
"""

from __future__ import annotations

from pathlib import Path

from . import gitutil, paths
from .sync import SyncError

# The environment the continuation must run under. `git rebase --continue` opens
# an editor for the commit message on git 2.26 and later, so without this a VM
# whose stdin is an inherited pipe blocks until the timeout and CI fails the step
# outright — which is what stopped `land` from publishing at all on git >= 2.26
# (FAILURES.md F011). Forcing the child's editor to a no-op outranks any
# `GIT_EDITOR` the VM exports.
NON_INTERACTIVE = {
    "GIT_EDITOR": "true",
    "GIT_SEQUENCE_EDITOR": "true",
    "GIT_MERGE_AUTOEDIT": "no",
}


def _repo_path(git_path: str, root=None) -> Path:
    """Resolve what `git rev-parse --git-path` printed against the right clone.

    The relative path it prints is relative to the repository, not to the process,
    and a fleet test drives a clone that is not the process's own working
    directory — so resolving it against the cwd reads another VM's rebase state,
    or none.
    """
    candidate = Path(git_path)
    if candidate.is_absolute():
        return candidate
    return Path(root or paths.repo_root()) / candidate


def unresolved_paths(root=None) -> list[str]:
    """The paths git still reports as conflicted, in either rebase flavour."""
    return gitutil.run(["diff", "--name-only", "--diff-filter=U"], root).stdout.split()


def unstaged_paths(root=None) -> list[str]:
    """Dirty paths that are *not* staged, which a continuation would not take."""
    out = []
    result = gitutil.run(["status", "--porcelain", "--untracked-files=all"], root)
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        # Porcelain's first column is the index and its second the worktree. `MM`
        # is dirty in both, so it belongs in both lists.
        if line[1] != " ":
            out.append(line[3:].strip())
    return out


def orig_head(root=None) -> str:
    """The tip a paused rebase started from, which git recorded when it began."""
    for directory in ("rebase-merge", "rebase-apply"):
        relative = gitutil.text(["rev-parse", "--git-path", directory], root)
        if not relative:
            continue
        marker = _repo_path(relative.strip(), root) / "orig-head"
        if marker.is_file():
            return marker.read_text(encoding="utf-8").strip()
    return ""


def resume(root=None) -> str:
    """Finish a rebase whose conflicts the reader has resolved.

    Returns the pre-rebase tip when a rebase was completed and `""` when there was
    nothing to resume, so the caller can use it as the branch's own tip for
    attribution. Every refusal is a `SyncError`: each names what to do, because the
    alternative is a reader left with `git status`.
    """
    if not gitutil.rebase_in_progress(root):
        return ""
    conflicted = unresolved_paths(root)
    if conflicted:
        raise SyncError(
            "rebase stopped on a real content conflict in "
            + ", ".join(conflicted[:8])
            + "; resolve it (or 'git rebase --abort') and land again"
        )
    unstaged = unstaged_paths(root)
    if unstaged:
        raise SyncError(
            "rebase is resolved but not committed, and "
            + ", ".join(unstaged[:8])
            + " is dirty and not staged; commit or revert it first, so the "
            "continuation does not sweep it into the rebase's commit"
        )
    # Read before the continuation: git removes the directory it lives in when the
    # rebase finishes, so afterwards the tip it names is unreadable.
    before = orig_head(root)
    finished = gitutil.run(["rebase", "--continue"], root, timeout=60, env=NON_INTERACTIVE)
    if gitutil.rebase_in_progress(root):
        raise SyncError(
            "rebase could not be completed"
            + gitutil.detail(finished)
            + "; run 'git rebase --abort'"
        )
    return before