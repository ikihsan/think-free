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
reached through a refusal message rather than by anybody's mistake. T-0048 made `land`
complete such a rebase itself; T-0053's `recover()` additionally records the arrival
of a rebase still finished with raw git, from `ORIG_HEAD` and the reflog.

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


def recover(root=None) -> dict | None:
    """Record the base move of a rebase a human completed with raw git.

    `land` used to refuse a dirty tree and ask the reader to resolve and land
    again — which made `git rebase --continue` by hand the only way out, and
    that records no `base_advance`. `land` now resumes the rebase itself, but
    a hand-run continuation is still possible, and the arrival is then
    attributed to the session that resolved the conflict. Git leaves the
    evidence behind: `ORIG_HEAD` names the pre-rebase tip, and HEAD's reflog
    names the upstream the rebase checked out, so the arrival is recoverable
    after the fact.

    A merge also writes `ORIG_HEAD`, but its history carries a merge commit
    and its arrival is the merging operation's to record; a fast-forward has
    no replays. Both are refused, so only a replayed history is recovered, and
    an arrival higher-level reporting already recorded is not duplicated.

    Returns the recorded event data, or `None` when there is nothing to record.
    """
    from . import landed
    from .activestate import load_active

    if gitutil.rebase_in_progress(root):
        return None
    orig = gitutil.text(["rev-parse", "--verify", "--quiet", "ORIG_HEAD"], root)
    if not orig:
        return None
    head = gitutil.text(["rev-parse", "HEAD"], root)
    if not head or orig == head:
        return None
    base = gitutil.text(["merge-base", orig, head], root)
    if not base or base == head:
        return None
    # A merge and a fast-forward also write `ORIG_HEAD`, but there the old tip
    # stays an ancestor of the new head; a rebase replaces it. Both shapes are
    # the merging operation's to record, not this one.
    if gitutil.run(["merge-base", "--is-ancestor", orig, head], root).returncode == 0:
        return None
    if gitutil.run(["rev-list", "--merges", f"{base}..{head}"], root).stdout.strip():
        return None
    upstream = _rebase_upstream(root)
    if not upstream or upstream == base:
        return None
    if gitutil.run(["merge-base", "--is-ancestor", upstream, head], root).returncode != 0:
        return None
    arrived = gitutil.rev_list(f"{base}..{upstream}", root)
    if not arrived:
        return None
    active = load_active()
    if active is None:
        return None
    if set(arrived) <= set(landed.landed_commits(active.session)):
        return None
    # A rebase whose arrival already sits under this session's starting commit
    # is a previous session's history, not this one's arrival: without this the
    # same ORIG_HEAD entry would be re-recorded into every later session.
    if active.start_head and gitutil.run(
        ["merge-base", "--is-ancestor", upstream, active.start_head], root
    ).returncode == 0:
        return None
    return landed.record("rebase completed outside land", base, upstream, arrived)


def _rebase_upstream(root=None) -> str:
    """The upstream tip the last rebase checked out, from HEAD's reflog.

    Every rebase rewinds the branch onto its upstream, and records that as a
    `rebase ...: checkout <upstream>` entry on HEAD. The entry's new value is
    the upstream sha at the moment the rebase began, which afterwards names
    exactly the tip the replayed work was stacked on — even though the branch
    ref has since moved. Returns "" when no such entry is readable (an expired
    reflog, a hand-edited history, a client without reflogs).
    """
    out = gitutil.run(["reflog", "--format=%H\t%gs", "HEAD"], root).stdout
    for line in out.splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        sha, subject = parts
        if "checkout" not in subject:
            continue
        if subject.startswith(("rebase:", "rebase (")) or "rebase:" in subject:
            return sha.strip()
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