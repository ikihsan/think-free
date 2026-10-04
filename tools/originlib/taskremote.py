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

from . import gitutil, paths, sync, taskops, tasks

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


def _require_at_base() -> str:
    """A claim commit must be the only thing between this branch and the base.

    Pushing `HEAD` to the base branch would otherwise land unrelated work along
    with the claim, which is how an agent publishes something it never reviewed.
    """
    remote = sync.remote_name()
    base = sync.base_branch()
    local = gitutil.text(["rev-parse", "HEAD"])
    upstream = gitutil.text(["rev-parse", f"{remote}/{base}"])
    if not upstream:
        raise tasks.TaskError(
            f"{remote}/{base} is unknown on this machine; run 'tools/origin sync pull' first"
        )
    if local != upstream:
        ahead, behind = sync._ahead_behind()
        if ahead:
            raise tasks.TaskError(
                f"this branch carries {ahead} unpublished commit(s) that are not on "
                f"{remote}/{base}; land them first ('tools/origin sync land') so the "
                "claim is published on its own"
            )
        raise tasks.TaskError(
            f"this branch is {behind} commit(s) behind {remote}/{base}; "
            "run 'tools/origin sync pull' so the claim is published on top of the current record"
        )
    return upstream


def _catch_up() -> None:
    """Fast-forward onto the shared base before writing shared state."""
    try:
        sync.pull()
    except sync.SyncError as exc:
        raise tasks.TaskError(str(exc)) from exc


def _commit_paths(paths_to_stage: list[str], message: str) -> bool:
    gitutil.run(["add", "--", *paths_to_stage])
    result = gitutil.run(["commit", "-q", "-m", message])
    return result.returncode == 0


def _discard_claim_commit(base: str) -> None:
    """Undo a claim commit git refused, so the loser keeps a clean tree."""
    ahead = gitutil.text(["rev-list", "--count", f"{base}..HEAD"])
    if ahead == "1" and not gitutil.dirty_paths():
        gitutil.run(["reset", "--hard", "-q", base])
    else:
        raise tasks.TaskError(
            "the claim push was refused and this branch has other commits; "
            "rebase onto the base branch by hand, then claim again"
        )


def _claim_paths(task) -> list[str]:
    """The paths a published claim must carry, indexes included.

    A task file is a document, and `doc lint` calls a document no index mentions
    an orphan. The claim is the commit every other VM sees first, so if it leaves
    the regenerated indexes behind, the pushed tree is red: that is what runs
    `37163434868` and `37163438950` were (T-0025). Rebuild first, stage second.
    """
    taskops.refresh_indexes()
    return [
        f"tasks/{task.path.name}",
        "tasks/CLAIMS.jsonl",
        "tasks/INDEX.md",
        "docs/INDEX.md",
    ]


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
    for attempt in range(1, RETRY_LIMIT + 1):
        _catch_up()
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
        _require_at_base()
        task = tasks.find(task_id)
        taskops._set_meta(
            task,
            {
                "status": "claimed",
                "claim-agent": agent,
                "claim-vm": vm,
                "claim-session": session,
            },
        )
        action = "takeover" if (takeover and current) else "claim"
        tasks.append_claim(
            task_id,
            action,
            agent=agent,
            vm=vm,
            session=session,
            reason=takeover or None,
            superseded=current.get("agent") if action == "takeover" else None,
        )
        if not _commit_paths(_claim_paths(task), f"claim {task_id} by {agent} on {vm or 'unknown-vm'}"):
            raise tasks.TaskError(f"could not commit the claim for {task_id}")
        result = sync.push(base)
        if result.get("pushed"):
            return tasks.load(task.path)
        fetch()
        _discard_claim_commit(ref)
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
    _catch_up()
    current = holder(task_id, ref)
    if current and current.get("agent") != agent and not reason:
        raise tasks.TaskError(
            f"{task_id} is held by {current.get('agent')}; releasing it needs a reason"
        )
    _require_at_base()
    task = tasks.find(task_id)
    taskops._set_meta(task, {"status": "open", "claim-agent": "", "claim-vm": "", "claim-session": ""})
    tasks.append_claim(task_id, "release", agent=agent, vm=vm, reason=reason or None)
    _commit_paths(_claim_paths(task), f"release {task_id} by {agent}")
    sync.push(base)
    return tasks.load(task.path)
