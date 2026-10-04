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
    META_KEY,
    STATUSES,
    Task,
    TaskError,
    active_claims,
    append_claim,
    find,
    load,
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

