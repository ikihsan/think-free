"""Task mutations and verification.

Mutating operations live apart from the task model so that `tasks.py` stays
the read path and this module stays the write path.
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime

from . import paths
from .tasktemplate import TEMPLATE
from .tasks import (
    DIGEST_KEYS,
    META_KEY,
    STATUSES,
    Task,
    TaskError,
    active_claims,
    append_claim,
    find,
    load,
    meta_digests,
    next_task_id,
    slugify,
    write_index,
)


def refresh_indexes() -> None:
    """Rebuild the generated indexes after a task row moved.

    `create` adds a document, so an index that predates it makes the new task an
    orphan and fails `doc lint` - observed as two red CI runs on 2026-10-03
    (`STATE-defects.md` defect 5). Both indexes are pure functions of the tree,
    so writing them here is a rebuild rather than an edit.
    """
    from . import docindex

    write_index()
    docindex.write_index()


def _set_meta(task: Task, updates: dict[str, str]) -> None:
    text = task.path.read_text(encoding="utf-8")
    match = META_KEY.search(text)
    if not match:
        raise TaskError(f"{task.path.name} has no task-meta block")
    block = match.group(1)
    for key, value in updates.items():
        pattern = re.compile(rf"^(\s*{re.escape(key)}\s*:)(.*)$", re.MULTILINE)
        if pattern.search(block):
            block = pattern.sub(lambda m: f"{m.group(1)} {value}", block, count=1)
        else:
            block = block.rstrip() + f"\n{key}: {value}\n"
    new_text = text[: match.start(1)] + block + text[match.end(1) :]
    task.path.write_text(new_text, encoding="utf-8")
    record_rewrite(task, updates.get("status", ""))


def record_rewrite(task: Task, status: str = "") -> None:
    """Declare the file this command just rewrote, and the bytes it wrote.

    `_set_meta` is the only function that rewrites a task file's meta block, so
    the declaration belongs here rather than in the four commands that call it:
    a rule attached to the command that happened to be running is a rule the
    next command misses.

    Why it is needed at all: reconciliation reports a file this session changed
    without declaring it, and `task claim`, `task complete` and `task release`
    all change the task file. Every one of them therefore closed its session
    with exit 4 naming the tooling's own write — 37 such reports across the 21
    sessions in this repository's history (`observed` 2026-10-04, defect 12).

    The digests are what make the declaration safe rather than a blanket
    exemption. A command that declared "this file" would silence every later
    edit to it, including the agent's own; declaring the bytes it wrote silences
    only the write it made, so ticking an acceptance checkbox afterwards is
    reported again. The trade-off defect 12 refused is answered here rather than
    assumed away.
    """
    from . import activestate, events, session

    active = activestate.load_active()
    if active is None:
        # Outside a session there is no record to write into, and inventing one
        # would be a worse lie than the missing entry.
        return
    digests = meta_digests(task.path)
    if any(
        event.kind == "task_rewrite"
        and event.data.get("path") == paths.paths_repo_relative(task.path)
        and all(event.data.get(key) == digests[key] for key in DIGEST_KEYS)
        for event in events.events_for(active.session)
    ):
        return
    rel = paths.paths_repo_relative(task.path)
    events.append(
        active.session,
        "task_rewrite",
        {
            "summary": f"rewrote {rel} (status: {status or 'unchanged'})",
            "path": rel,
            "task": task.task_id,
            "status": status,
            **digests,
        },
        actor=active.agent,
        host=active.host,
    )
    session.refresh_reports(active.session)


def create(goal: str, verify: str, **fields) -> Task:
    if not goal.strip():
        raise TaskError("--goal must not be empty")
    task_id = next_task_id()
    slug = slugify(goal)
    path = paths.tasks_dir() / f"{task_id}-{slug}.md"
    if path.exists():
        raise TaskError(f"refusing to overwrite {path.name}")
    body = TEMPLATE.format(
        date=datetime.now().astimezone().strftime("%Y-%m-%d"),
        task_id=task_id,
        title=fields.get("title") or goal.strip()[:70],
        goal=goal.strip(),
        rationale=fields.get("rationale", "_Why this is worth doing._"),
        preconditions=fields.get("preconditions", "_What must be true first._"),
        steps=fields.get("steps", "1. \n2. \n3. "),
        acceptance=fields.get("acceptance", "- [ ] "),
        verify=verify,
        rollback=fields.get("rollback", "_How to undo a bad outcome._"),
    )
    paths.ensure_dir(paths.tasks_dir())
    path.write_text(body, encoding="utf-8")
    append_claim(task_id, "create")
    refresh_indexes()
    return load(path)


def claim(task_id: str, agent: str, vm: str = "", session: str = "") -> Task:
    task = find(task_id)
    current = active_claims().get(task.task_id)
    if current and current.get("agent") != agent:
        raise TaskError(
            f"{task.task_id} is already claimed by {current.get('agent')} "
            f"since {current.get('ts')}; release it or pick another task"
        )
    _set_meta(task, {"status": "claimed", "claim-agent": agent, "claim-vm": vm, "claim-session": session})
    append_claim(task.task_id, "claim", agent=agent, vm=vm, session=session)
    refresh_indexes()
    return load(task.path)


def transition(task_id: str, status: str, reason: str = "", **fields) -> Task:
    if status not in STATUSES:
        raise TaskError(f"status must be one of {', '.join(STATUSES)}")
    task = find(task_id)
    _set_meta(task, {"status": status})
    action = {"done": "complete", "cancelled": "cancel"}.get(status, status)
    append_claim(task.task_id, action, reason=reason, **fields)
    refresh_indexes()
    return load(task.path)


def run_verification(task: Task, timeout: int = 900) -> dict:
    command = task.meta.get("verify", "").strip()
    if not command:
        return {"ran": False, "reason": "no verify command declared"}
    started = datetime.now()
    result = subprocess.run(
        command,
        shell=True,
        cwd=str(paths.repo_root()),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return {
        "ran": True,
        "command": command,
        "exit_code": result.returncode,
        "duration_s": round((datetime.now() - started).total_seconds(), 2),
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }

