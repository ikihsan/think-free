"""Integration: rebase this branch onto the shared base, then publish it.

Split out of `sync.py` on 2026-10-04 (T-0030) when that file reached 297 of the
300 permitted lines and the identifier-collision refusal did not fit. The
division is by role: `sync.py` holds the primitives — where the remote is, what
the base is, what this VM stands relative to it, and how to fast-forward or push
— while this module holds the one operation that *combines* two machines' work.

That combination is why the identifier check lives here. A collision between two
VMs is created by the merge: each branch is internally consistent, and each VM's
own `doc lint` sees nothing wrong with its own tree. `push` and `task claim` are
deliberately not gated — refusing them would block a VM from publishing the
session record it needs in order to renumber its way out of the collision (D031).
"""

from __future__ import annotations

from . import gitutil, paths
from .sync import (
    SyncError,
    record_arrival,
    base_branch,
    fetch,
    push,
    remote_name,
)

GENERATED_FILES = ("docs/INDEX.md", "sessions/INDEX.md", "tasks/INDEX.md")
RETRY_LIMIT = 3


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


def _refuse_identifier_collision() -> None:
    """Refuse to publish a tree that gives one identifier two definitions.

    Only `land` is gated. A collision is created by the *merge* — both branches
    are internally consistent, and each VM's own `doc lint` sees nothing wrong —
    so the operation that combines them is the only place where the property
    exists to be read. `push` and `task claim` are left alone deliberately:
    refusing them would block a VM from publishing the session record it needs
    in order to renumber its way out of the collision.
    """
    from . import identifiers

    found = identifiers.report(paths.repo_root())
    if found:
        raise SyncError(
            "refusing to land: the identifier record collides, so one number means "
            "two things. Renumber the newer entries, then land again:\n  "
            + "\n  ".join(found[:8])
        )


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
        _refuse_identifier_collision()
        try:
            pushed = push(target, root=root)
        except SyncError as exc:
            if "non-fast-forward" not in str(exc) or attempt >= retries:
                raise
            continue
        # After the push, never before: writing the event dirties the tree, and
        # `push` refuses a dirty tree on purpose. The session's own commit takes
        # the record to the base with the work.
        record_arrival("sync land", before, after, root, arrived=arrived)
        outcome.update(pushed)
        outcome["resolved"] = outcome["resolved"] or resolved
        return outcome
    raise SyncError(f"base branch {target} kept moving after {retries} attempts; run it again")
