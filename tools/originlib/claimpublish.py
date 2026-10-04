"""Getting a claim onto the shared base: the write half of `taskremote`.

Split out of `taskremote.py` on 2026-10-04 (T-0055), by the division that
module's own docstring already draws: reads come from the remote ref, writes go to
a working tree and are published by pushing. Adding the claim's own
preconditions pushed the file to 345 of the 300 permitted lines, and the split is
by invariant rather than by size — a reader asking "what does the remote think the
task list is" should not have to read how a claim is staged.

What lives here is the answer to one question: **what must be true of this
working tree for a claim to be publishable, and what does the claim's commit
carry?** Both halves of that were wrong in the same commit, and neither was
visible from the refusal, which is what made it a livelock (defect 21):

* the push refused the session's own uncommitted record, so the claim stayed local
  and the exclusivity it exists to provide was not in force on any other VM;
* the refusal's remedy — commit or revert the named paths — is the one action an
  agent must not take by hand on its own record.

So the session's record now travels with the claim, which is the invariant
[`multi-vm-coordination.md`](../../docs/process/multi-vm-coordination.md)
already stated and no code implemented, and foreign uncommitted work is refused
*before* anything is written, so a failed claim costs a message rather than a
commit and a line in the append-only ledger.
"""

from __future__ import annotations

from . import gitutil, sync, taskops
from . import tasks as tasks_module
from .tasks import TaskError


def catch_up() -> None:
    """Fast-forward onto the shared base before writing shared state."""
    try:
        sync.pull()
    except sync.SyncError as exc:
        raise TaskError(str(exc)) from exc


def require_at_base() -> str:
    """A claim commit must be the only thing between this branch and the base.

    Pushing `HEAD` to the base branch would otherwise land unrelated work along
    with the claim, which is how an agent publishes something it never reviewed.
    """
    remote = sync.remote_name()
    base = sync.base_branch()
    local = gitutil.text(["rev-parse", "HEAD"])
    upstream = gitutil.text(["rev-parse", f"{remote}/{base}"])
    if not upstream:
        raise TaskError(
            f"{remote}/{base} is unknown on this machine; run 'tools/origin sync pull' first"
        )
    if local != upstream:
        ahead, behind = sync._ahead_behind()
        if ahead:
            raise TaskError(
                f"this branch carries {ahead} unpublished commit(s) that are not on "
                f"{remote}/{base}; land them first ('tools/origin sync land') so the "
                "claim is published on its own"
            )
        raise TaskError(
            f"this branch is {behind} commit(s) behind {remote}/{base}; "
            "run 'tools/origin sync pull' so the claim is published on top of the current record"
        )
    return upstream


def commit_paths(paths_to_stage: list[str], message: str) -> bool:
    gitutil.run(["add", "--", *paths_to_stage])
    result = gitutil.run(["commit", "-q", "-m", message])
    return result.returncode == 0


def discard_claim_commit(base: str) -> None:
    """Undo a claim commit git refused, so the loser keeps a clean tree."""
    ahead = gitutil.text(["rev-list", "--count", f"{base}..HEAD"])
    if ahead == "1" and not gitutil.dirty_paths():
        gitutil.run(["reset", "--hard", "-q", base])
    else:
        raise TaskError(
            "the claim push was refused and this branch has other commits; "
            "rebase onto the base branch by hand, then claim again"
        )


def claim_paths(task) -> list[str]:
    """The paths a published claim must carry, indexes and session record included.

    A task file is a document, and `doc lint` calls a document no index mentions
    an orphan. The claim is the commit every other VM sees first, so if it leaves
    the regenerated indexes behind, the pushed tree is red: that is what runs
    `37163434868` and `37163438950` were (T-0025). Rebuild first, stage second.

    The open session's own record travels with it, for two reasons. The first is
    the invariant `multi-vm-coordination.md` already states: a claim must be
    published on the base branch, and publishing needs HEAD to equal the base, so
    a claiming VM pushes its session start first. The second is mechanical:
    `session start` writes the record and every later event dirties it again, so
    without this the push refuses the claim's own commit and the claim stays
    invisible to every other VM (defect 21, T-0055).

    The session paths are read from the module that owns that definition rather
    than written out here, so a path added to one and not the other is a path
    nobody stages — the second half of this repair was a first attempt that named
    the session directory and forgot `sessions/INDEX.md`, which the test caught
    with the same refusal the defect produced.
    """
    from . import sessionflow
    from .activestate import load_active

    taskops.refresh_indexes()
    staged = [f"tasks/{task.path.name}", "tasks/CLAIMS.jsonl"]
    active = load_active()
    if active is not None:
        staged.extend(sessionflow.session_owned_paths(active.session))
    for index in ("tasks/INDEX.md", "docs/INDEX.md"):
        if index not in staged:
            staged.append(index)
    return staged


def refuse_uncommitted_work() -> None:
    """Refuse before writing anything, so a refused claim leaves no trace.

    A claim is published by the same command that writes it, and `push` refuses a
    dirty tree. Asking that question after the writes is what left a claim commit
    on the branch and a line in the append-only ledger for a claim no other VM
    could see: three refusals on the shared base produced three identical `claim`
    lines and one commit stuck local, and the claim took thirty minutes to land by
    hand. Refusing first makes a failed claim cost a message and nothing else.

    The session's own record is not uncommitted work — that distinction is the
    whole repair, and it is the one `session finish --push` already draws through
    `sessionflow.uncommitted_work`. With no session open there is no record to
    distinguish, so every dirty path counts.
    """
    from . import sessionflow
    from .activestate import load_active

    active = load_active()
    foreign = (
        sessionflow.uncommitted_work(active.session)
        if active is not None
        else gitutil.dirty_paths()
    )
    if foreign:
        raise TaskError(
            "commit or revert this uncommitted work before claiming, so the claim is "
            "published on a tree that says what it says: " + ", ".join(foreign[:8])
        )


def write_claim(
    task,
    task_id: str,
    agent: str,
    vm: str,
    session: str,
    action: str,
    reason: str,
    superseded: str = "",
) -> None:
    """Rewrite the task's meta, append to the ledger, and stage the claim commit."""
    taskops._set_meta(
        task,
        {
            "status": "claimed",
            "claim-agent": agent,
            "claim-vm": vm,
            "claim-session": session,
        },
    )
    tasks_module.append_claim(
        task_id,
        action,
        agent=agent,
        vm=vm,
        session=session,
        reason=reason or None,
        superseded=superseded or None,
    )
    if not commit_paths(claim_paths(task), f"claim {task_id} by {agent} on {vm or 'unknown-vm'}"):
        raise TaskError(f"could not commit the claim for {task_id}")