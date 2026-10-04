"""Cross-VM synchronisation: fetch, fast-forward, publish, land.

Git is the only shared state between VMs, so every rule here is expressed as a
git operation whose outcome git itself decides. The properties that matter:

- `pull` only ever fast-forwards, and refuses to start from a dirty tree,
  because a session that begins on stale or mixed state reconciles into a lie.
- `push` never forces. A rejected push means another VM got there first, which
  is information, not an obstacle to work around.
- `land` rebases a work branch onto the shared base and pushes it. Conflicts in
  generated indexes are resolved by regenerating them, because their content is
  a pure function of the tree; every other conflict stops the operation.
"""

from __future__ import annotations

import os
from pathlib import Path

from . import gitutil, paths

DEFAULT_REMOTE = "origin"
FALLBACK_BASE = "research/origin"
GENERATED_FILES = ("docs/INDEX.md", "sessions/INDEX.md", "tasks/INDEX.md")
RETRY_LIMIT = 3


class SyncError(RuntimeError):
    """Raised when a sync operation cannot proceed safely. Maps to exit 1."""


def remote_name() -> str:
    """The remote to synchronise with, or an empty string when offline."""
    configured = gitutil.text(["remote"])
    names = configured.split() if configured else []
    if DEFAULT_REMOTE in names:
        return DEFAULT_REMOTE
    return names[0] if names else ""


def base_branch(root=None) -> str:
    """The shared branch every VM integrates into.

    Resolution order: explicit override, the remote's default branch, the
    current branch's upstream, then the documented default. Getting this wrong
    is the difference between publishing work and losing it, so the value is
    printed by every sync command rather than hidden.
    """
    override = os.environ.get("ORIGIN_BASE_BRANCH", "").strip()
    if override:
        return override
    remote = remote_name()
    if remote:
        head = gitutil.text(["symbolic-ref", "--short", f"refs/remotes/{remote}/HEAD"])
        if head:
            return head.split("/", 1)[-1]
        current = gitutil.state().branch
        if current and current != "(detached)":
            upstream = gitutil.text(
                ["rev-parse", "--abbrev-ref", f"{current}@{{upstream}}"], root
            )
            if upstream.startswith(f"{remote}/"):
                return upstream.split("/", 1)[-1]
    return FALLBACK_BASE


def fetch(root=None) -> bool:
    """Fetch the remote. False when there is no remote to fetch from."""
    remote = remote_name()
    if not remote:
        return False
    gitutil.run(["fetch", "--quiet", remote], root)
    return True


def _ahead_behind(root=None) -> tuple[int, int]:
    remote = remote_name()
    if not remote:
        return 0, 0
    ref = f"{remote}/{base_branch(root)}"
    if not gitutil.text(["rev-parse", "--verify", "--quiet", ref], root):
        return 0, 0
    result = gitutil.run(
        ["rev-list", "--left-right", "--count", f"HEAD...{ref}"], root
    )
    if result.returncode != 0:
        return 0, 0
    parts = result.stdout.split()
    if len(parts) != 2:
        return 0, 0
    return int(parts[0]), int(parts[1])


def status(root=None, refresh: bool = True) -> dict:
    """Where this VM actually stands, including work pushed by other VMs.

    Fetches first by default: a divergence report computed against a stale
    remote-tracking ref is the one thing a fleet operator must never trust.
    """
    if refresh:
        fetch(root)
    state = gitutil.state(root)
    ahead, behind = _ahead_behind(root)
    return {
        "branch": state.branch,
        "head": state.head[:12],
        "remote": remote_name(),
        "base_branch": base_branch(root),
        "ahead": ahead,
        "behind": behind,
        "clean": state.clean,
        "dirty": gitutil.dirty_paths(root),
        "rebase_in_progress": gitutil.rebase_in_progress(root),
    }


def pull(root=None) -> dict:
    """Fetch and fast-forward onto the shared base. Never merges, never resets."""
    remote = remote_name()
    if not remote:
        raise SyncError("no git remote configured; nothing to pull from")
    fetch(root)
    report = status(root)
    outcome = {
        "remote": remote,
        "base_branch": report["base_branch"],
        "behind_before": report["behind"],
        "fast_forwarded": False,
    }
    if report["behind"] == 0:
        return outcome
    if report["dirty"]:
        raise SyncError(
            "working tree has uncommitted changes, refusing to fast-forward: "
            + ", ".join(report["dirty"][:8])
        )
    if report["ahead"]:
        raise SyncError(
            f"local branch is ahead of {remote}/{report['base_branch']} by "
            f"{report['ahead']} commit(s); publish it with 'tools/origin sync land' "
            "instead of discarding it"
        )
    before = gitutil.text(["rev-parse", "HEAD"], root)
    result = gitutil.run(
        ["merge", "--ff-only", f"{remote}/{report['base_branch']}"], root
    )
    if result.returncode != 0:
        raise SyncError(f"fast-forward failed: {result.stderr.strip() or result.stdout.strip()}")
    outcome["fast_forwarded"] = True
    outcome["head"] = gitutil.text(["rev-parse", "HEAD"], root)
    _record_arrival("sync pull", before, outcome["head"], root)
    return outcome


def _record_arrival(
    reason: str, before: str, after: str, root=None, arrived: list[str] | None = None
) -> None:
    """Note which commits the base move brought in, for the session open here.

    Reconciliation diffs a session against its starting commit, so without this
    the work another VM pushed looks like the session's own change and is
    reported as undeclared: session 029 closed with nine such reports, none of
    them its own. Recorded only when a session is open in this working tree,
    because there is nowhere else for the record to live.
    """
    from . import landed

    commits = arrived if arrived is not None else gitutil.rev_list(f"{before}..{after}", root)
    landed.record(reason, before, after, commits)


def push(branch: str = "", set_upstream: bool = False, root=None) -> dict:
    """Publish the current branch. Never force-pushes, by design."""
    remote = remote_name()
    if not remote:
        raise SyncError("no git remote configured; nothing to push to")
    dirty = gitutil.dirty_paths(root)
    if dirty:
        raise SyncError(
            "refusing to push a dirty tree; commit or revert: " + ", ".join(dirty[:8])
        )
    current = gitutil.state(root).branch
    target = branch or current
    if not target or target in {"(detached)", "(unborn)"}:
        raise SyncError("cannot push a detached HEAD; name the branch explicitly")
    args = ["push", "--quiet"]
    if set_upstream:
        args.append("--set-upstream")
    args += [remote, f"HEAD:refs/heads/{target}"]
    result = gitutil.run(args, root)
    if result.returncode != 0:
        combined = (result.stderr + result.stdout).strip()
        if "non-fast-forward" in combined or "fetch first" in combined:
            raise SyncError(
                f"push rejected as non-fast-forward: another VM pushed {target} first; "
                "fetch and rebase with 'tools/origin sync land'"
            )
        raise SyncError(f"push failed: {combined}")
    return {"remote": remote, "branch": target, "pushed": True, "head": gitutil.text(["rev-parse", "HEAD"], root)}


def _resolve_generated_conflicts() -> list[str]:
    """Regenerate the generated indexes and stage them.

    Their content is a pure function of the merged tree, so regeneration is a
    resolution rather than a guess. Only files git actually reports as
    conflicted are touched.
    """
    from . import docindex, report, tasks

    unmerged = gitutil.run(["diff", "--name-only", "--diff-filter=U"]).stdout.split()
    resolved: list[str] = []
    for name in unmerged:
        if name not in GENERATED_FILES:
            continue
        if name == "docs/INDEX.md":
            paths.docs_index().write_text(docindex.render(), encoding="utf-8")
        elif name == "sessions/INDEX.md":
            paths.sessions_index().write_text(report.render_sessions_index(), encoding="utf-8")
        else:
            paths.tasks_index().write_text(tasks.render_tasks_index(), encoding="utf-8")
        gitutil.run(["add", "--", name])
        resolved.append(name)
    return resolved


def land(branch: str = "", retries: int = RETRY_LIMIT, root=None) -> dict:
    """Rebase this branch onto the shared base and push it there.

    This is the integration step: the one operation that moves work from a
    private work branch into the history every other VM reads.
    """
    remote = remote_name()
    if not remote:
        raise SyncError("no git remote configured; nothing to land")
    dirty = gitutil.dirty_paths(root)
    if dirty:
        raise SyncError("commit or revert before landing: " + ", ".join(dirty[:8]))
    target = branch or base_branch(root)
    outcome: dict = {"remote": remote, "branch": target, "resolved": [], "rebased": False}
    for attempt in range(1, max(1, retries) + 1):
        resolved: list[str] = []
        fetch(root)
        base_ref = f"{remote}/{target}"
        if not gitutil.text(["rev-parse", "--verify", "--quiet", base_ref], root):
            raise SyncError(f"{base_ref} does not exist; check the branch name")
        before = gitutil.text(["rev-parse", "HEAD"], root)
        result = gitutil.run(["rebase", base_ref], root)
        if result.returncode != 0:
            resolved = _resolve_generated_conflicts()
            unfinished = result
            if resolved:
                # `git rebase --continue` opens an editor for the commit message
                # on git 2.5x. Nothing in this flow may be interactive: a VM
                # whose stdin is an open pipe blocks until the timeout, and CI
                # fails outright. Forcing the child's editor to a no-op outranks
                # any GIT_EDITOR the VM exports, which `-c core.editor` does not.
                unfinished = gitutil.run(
                    ["rebase", "--continue"],
                    root,
                    timeout=60,
                    env={"GIT_EDITOR": "true", "GIT_SEQUENCE_EDITOR": "true", "GIT_MERGE_AUTOEDIT": "no"},
                )
            conflicted = gitutil.run(["diff", "--name-only", "--diff-filter=U"]).stdout.split()
            if conflicted:
                raise SyncError(
                    "rebase stopped on a real content conflict in "
                    + ", ".join(conflicted[:8])
                    + "; resolve it (or 'git rebase --abort') and land again"
                )
            if gitutil.rebase_in_progress(root):
                raise SyncError(
                    "rebase could not be completed"
                    + gitutil.detail(unfinished)
                    + "; run 'git rebase --abort'"
                )
        outcome["rebased"] = True
        # What arrived is what the new base holds and the pre-rebase tip did
        # not: `base..HEAD` after a rebase is this branch's own rewritten work,
        # which is the opposite of the arrival. Read before the push, because the
        # push moves the tracking ref onto this branch.
        after = gitutil.text(["rev-parse", "HEAD"], root)
        arrived = gitutil.rev_list(f"{before}..{base_ref}", root)
        try:
            pushed = push(target, root=root)
        except SyncError as exc:
            if "non-fast-forward" not in str(exc) or attempt >= retries:
                raise
            continue
        # After the push, never before: writing the event dirties the tree, and
        # `push` refuses a dirty tree on purpose. The session's own commit takes
        # the record to the base with the work.
        _record_arrival("sync land", before, after, root, arrived=arrived)
        outcome.update(pushed)
        outcome["resolved"] = outcome["resolved"] or resolved
        return outcome
    raise SyncError(f"base branch {target} kept moving after {retries} attempts; run it again")
