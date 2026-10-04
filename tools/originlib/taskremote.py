"""Task state as the remote sees it, and claims that only one VM can win.

A local claim is a note to oneself: two VMs that both read `status: open` from
their own working trees both believe they own the task, and the second one to
push silently wins. So a claim here is committed *and* pushed, and git's ref
update is the lock. The loser of a race is told who won and changes nothing.

All reads come from the remote ref rather than the working tree, so a VM never
acts on a stale copy of the task list.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from . import claimpublish, gitutil, paths, sync, taskops, tasks

RETRY_LIMIT = 3


@dataclass
class RemoteTask:
    task_id: str
    name: str
    meta: dict = field(default_factory=dict)

    @property
    def status(self) -> str:
        return self.meta.get("status", "open")


def _read(ref: str, path: str) -> str:
    return gitutil.text(["show", f"{ref}:{path}"])


def remote_tasks(ref: str = "") -> dict[str, RemoteTask]:
    """Task id -> task, as recorded at `ref` (default: the remote base branch)."""
    ref = ref or base_ref()
    if not ref:
        return {}
    names = gitutil.run(["ls-tree", "-r", "--name-only", ref, "--", "tasks/"]).stdout.split()
    found: dict[str, RemoteTask] = {}
    for name in names:
        if not tasks.TASK_FILE.match(name.rsplit("/", 1)[-1]):
            continue
        match = tasks.META_KEY.search(_read(ref, name))
        meta: dict[str, str] = {}
        if match:
            for line in match.group(1).splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip()
        stem = name.rsplit("/", 1)[-1]
        task_id = meta.get("id") or tasks.TASK_FILE.match(stem).group(1)
        found[task_id] = RemoteTask(task_id=task_id, name=stem, meta=meta)
    return found


def remote_claims(ref: str = "") -> list[dict]:
    """The claim ledger as recorded at `ref`, parsed defensively."""
    ref = ref or base_ref()
    text = _read(ref, "tasks/CLAIMS.jsonl") if ref else ""
    out: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            out.append({"malformed": line})
    return out


def remote_active(ref: str = "") -> dict[str, dict]:
    """Task id -> the claim currently in force at `ref`."""
    state: dict[str, dict] = {}
    for entry in remote_claims(ref):
        task_id = entry.get("task")
        if not task_id or "malformed" in entry:
            continue
        if entry.get("action") in {"claim", "takeover"}:
            state[task_id] = entry
        elif entry.get("action") in {"release", "complete", "cancel"}:
            state.pop(task_id, None)
    return state


def base_ref(ref: str = "") -> str:
    if ref:
        return ref
    remote = sync.remote_name()
    return f"{remote}/{sync.base_branch()}" if remote else ""


def holder(task_id: str, ref: str = "") -> dict:
    """The claim in force for a task. Fetches first when `ref` is empty."""
    if not ref:
        fetch()
    return remote_active(ref).get(task_id, {})


def fetch() -> None:
    sync.fetch()


def render_remote_list(status_filter: str = "") -> str:
    ref = base_ref()
    if not ref:
        return "no git remote configured; showing local tasks only"
    fetch()
    remote = remote_active(ref)
    rows = []
    for task in sorted(remote_tasks(ref).values(), key=lambda t: t.task_id):
        if status_filter and task.status != status_filter:
            continue
        claim = remote.get(task.task_id, {})
        holder_text = "-"
        if claim:
            holder_text = f"{claim.get('agent', '?')}@{claim.get('vm', '?')}"
        rows.append(f"{task.task_id:<8} {task.status:<10} {holder_text:<22} {task.name}")
    if not rows:
        return f"no tasks at {ref}"
    header = f"tasks at {ref}\n{'TASK':<8} {'STATUS':<10} {'HOLDER':<22} FILE"
    return "\n".join([header, *rows])


def claim(
    task_id: str,
    agent: str,
    vm: str = "",
    session: str = "",
    takeover: str = "",
    push: bool = True,
) -> object:
    """Claim a task so that exactly one VM can hold it.

    `push=False` keeps the old local-only behaviour, which is correct only in a
    repository with no remote: there, no other machine can observe the claim, so
    the exclusivity is real but the durability is not.
    """
    remote = sync.remote_name()
    if not push or not remote:
        return taskops.claim(task_id, agent, vm, session)
    base = sync.base_branch()
    ref = f"{remote}/{base}"
    # Before the loop, and before any write: a claim that cannot be published must
    # not reach the ledger or the branch at all (defect 21, `claimpublish`).
    claimpublish.refuse_uncommitted_work()
    for attempt in range(1, RETRY_LIMIT + 1):
        claimpublish.catch_up()
        remote_task = remote_tasks(ref).get(task_id)
        if remote_task is None:
            raise tasks.TaskError(
                f"{task_id} does not exist at {ref}; run 'tools/origin sync pull' first"
            )
        current = holder(task_id, ref)
        if current and current.get("agent") != agent:
            if not takeover:
                raise tasks.TaskError(
                    f"{task_id} is already claimed by {current.get('agent')} on "
                    f"{current.get('vm', '?')} since {current.get('ts', '?')}; "
                    "choose another task, or record a takeover with --takeover \"reason\""
                )
        claimpublish.require_at_base()
        action = "takeover" if (takeover and current) else "claim"
        claimpublish.write_claim(
            tasks.find(task_id),
            task_id,
            agent,
            vm,
            session,
            action,
            takeover,
            superseded=current.get("agent") if action == "takeover" else None,
        )
        result = sync.push(base)
        if result.get("pushed"):
            return tasks.load(tasks.find(task_id).path)
        fetch()
        claimpublish.discard_claim_commit(ref)
        if holder(task_id, ref).get("agent") not in (None, agent):
            raise tasks.TaskError(
                f"{task_id} was claimed by another VM while this claim was in flight"
            )
    raise tasks.TaskError(f"could not claim {task_id} after {RETRY_LIMIT} attempts; run 'tools/origin sync status'")


def release(task_id: str, agent: str, vm: str = "", reason: str = "", push: bool = True) -> object:
    """Return a claimed task to the pool, visibly and with a reason."""
    remote = sync.remote_name()
    if not push or not remote:
        task = tasks.find(task_id)
        taskops.transition(task_id, "open", reason or "released")
        return tasks.load(task.path)
    base = sync.base_branch()
    ref = f"{remote}/{base}"
    # The same precondition as `claim`, and for the same reason: a release is
    # published by the command that writes it, so a tree it cannot push from must
    # be refused before the ledger grows. A rule attached to the command that
    # happened to be running is a rule the next command misses (D040).
    claimpublish.refuse_uncommitted_work()
    claimpublish.catch_up()
    current = holder(task_id, ref)
    if current and current.get("agent") != agent and not reason:
        raise tasks.TaskError(
            f"{task_id} is held by {current.get('agent')}; releasing it needs a reason"
        )
    claimpublish.require_at_base()
    task = tasks.find(task_id)
    taskops._set_meta(task, {"status": "open", "claim-agent": "", "claim-vm": "", "claim-session": ""})
    tasks.append_claim(task_id, "release", agent=agent, vm=vm, reason=reason or None)
    claimpublish.commit_paths(claimpublish.claim_paths(task), f"release {task_id} by {agent}")
    sync.push(base)
    return tasks.load(task.path)
