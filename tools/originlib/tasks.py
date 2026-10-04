"""Dispatchable tasks and their claim ledger.

Git is the only shared state between machines: each task is a Markdown file and
every claim is a line appended to `tasks/CLAIMS.jsonl`. Two VMs working on
different tasks therefore never touch the same file, and a task file's history
survives in git even if a claim is forgotten.

The generated table over these files is `taskindex`, and the write path is
`taskops`; both are reachable as attributes of this module.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime

from . import events, idalloc, paths

STATUSES = ("open", "claimed", "blocked", "done", "cancelled")
META_KEY = re.compile(r"<!--\s*task-meta\s*(.*?)-->", re.DOTALL)
TASK_FILE = re.compile(r"^(T-\d{4})-(.+)\.md$")


class TaskError(RuntimeError):
    """Raised for task misuse. Maps to exit code 1."""


@dataclass
class Task:
    task_id: str
    slug: str
    path: object
    meta: dict

    @property
    def status(self) -> str:
        return self.meta.get("status", "open")


def slugify(text: str, limit: int = 48) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)[:limit].rstrip("-") or "task"


def next_task_id() -> str:
    """The next free task number, read from the shared base when there is one.

    This used to list `tasks/` and add one, which is how two VMs took the same
    number twelve times in two days: the directory is one VM's opinion of the
    task list, and nothing said how old that opinion was. The allocation now
    reads the remote and prints where it read from, so a stale tree is visible
    at the moment the number is handed out rather than at the moment the push is
    rejected. `idalloc` owns the numbering rules for all three kinds.
    """
    return idalloc.next_identifier("T")


def task_files() -> list:
    directory = paths.tasks_dir()
    if not directory.exists():
        return []
    return sorted(p for p in directory.iterdir() if TASK_FILE.match(p.name))


def load(path) -> Task:
    text = path.read_text(encoding="utf-8")
    match = META_FILE_PATTERN = META_KEY.search(text)
    meta: dict[str, str] = {}
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
    name_match = TASK_FILE.match(path.name)
    return Task(
        task_id=meta.get("id") or (name_match.group(1) if name_match else path.stem),
        slug=name_match.group(2) if name_match else path.stem,
        path=path,
        meta=meta,
    )


def find(task_id: str) -> Task:
    for task in (load(p) for p in task_files()):
        if task.task_id == task_id or task.path.name == f"{task_id}.md":
            return task
    raise TaskError(f"no such task: {task_id}")


# ---------------------------------------------------------------- file bytes


def meta_digests(path) -> dict:
    """sha256 of a task file's meta block and of everything outside it.

    Two digests, because the two halves have different owners: a task command
    rewrites the meta block, and an agent rewrites the body. Naming both is what
    lets a caller say "this file still holds exactly the bytes that command
    wrote", which is the whole basis of the `task_rewrite` declaration —
    reconciliation reads it so a command's own write is not reported as an
    undeclared change, and so an agent's later edit to the same file is
    (defect 12).
    """
    text = path.read_text(encoding="utf-8")
    match = META_KEY.search(text)
    if not match:
        raise TaskError(f"{path.name} has no task-meta block")
    body = text[: match.start(1)] + text[match.end(1) :]
    return {
        "meta_sha256": hashlib.sha256(match.group(1).encode("utf-8")).hexdigest(),
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }


def digests_match(path, recorded: dict) -> bool:
    """True when `path` still holds exactly the bytes `recorded` names.

    False rather than raising for a file that is gone or unreadable: the caller
    is asking whether a claim about the past still describes the tree, and a
    missing or unparseable file does not.
    """
    if not recorded or not path.is_file():
        return False
    try:
        current = meta_digests(path)
    except (TaskError, OSError, UnicodeDecodeError):
        return False
    return all(current.get(key) == recorded.get(key) for key in DIGEST_KEYS)


DIGEST_KEYS = ("meta_sha256", "body_sha256")


def all_tasks() -> list[Task]:
    return [load(p) for p in task_files()]


# ------------------------------------------------------------------- ledger


def append_claim(task_id: str, action: str, **fields) -> dict:
    entry = {
        "schema": "origin.task.claim/1",
        "ts": events.now_iso(),
        "task": task_id,
        "action": action,
    }
    entry.update({k: v for k, v in fields.items() if v})
    path = paths.claims_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    _declare_claim_append(task_id, action, path)
    return entry


def _declare_claim_append(task_id: str, action: str, path) -> None:
    """Declare the ledger append this function just made, by its bytes.

    Every task command ends here, and reconciliation reports a file a session
    changed without declaring — so before this the ledger was a data file that no
    session could declare and no report could name, and the 50 sessions in this
    repository's history that appended to it are exactly the number of reports
    that would appear if it were fixed without being declared (T-0050's sweep).

    Declaring the bytes, not the name, is what keeps this safe: a hand edit to
    the ledger after the append changes the digest and is reported, while the
    command's own line stays silent. One function owns the append, so one
    function owns the declaration — a rule attached to the command that happened
    to be running is a rule the next command misses.
    """
    from . import declaredwrite
    from .activestate import load_active

    try:
        digests = declaredwrite.whole_file(path)
    except OSError:
        return
    rel = paths.paths_repo_relative(path)
    declaredwrite.record(
        load_active(),
        rel,
        {**digests, "action": action},
        f"appended a {action} record for {task_id}",
        task_id=task_id,
    )


def claims() -> list[dict]:
    path = paths.claims_file()
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            out.append({"malformed": line})
    return out


def active_claims() -> dict[str, dict]:
    """Task id -> the claim currently in force.

    `takeover` opens a claim exactly as `claim` does. It used to be ignored
    here while `taskremote.remote_active` honoured it, so the local and remote
    views of who holds a task disagreed after every takeover — which is the
    view that decides whether an unfinished session is still live.
    """
    state: dict[str, dict] = {}
    for entry in claims():
        task_id = entry.get("task")
        if not task_id or "malformed" in entry:
            continue
        if entry.get("action") in {"claim", "takeover"}:
            state[task_id] = entry
        elif entry.get("action") in {"release", "complete", "cancel"}:
            state.pop(task_id, None)
    return state


def print_list(status_filter: str = "") -> None:
    tasks = all_tasks()
    if status_filter:
        tasks = [t for t in tasks if t.status == status_filter]
    if not tasks:
        print("no tasks")
        return
    active = active_claims()
    for task in tasks:
        holder = (active.get(task.task_id) or {}).get("agent", "-")
        print(f"{task.task_id:<8} {task.status:<10} {holder:<14} {task.path.name}")



def __getattr__(name: str):
    """Expose the write path and the index renderer without a circular import.

    Both are lazily reachable rather than imported: `taskops` imports this
    module, and `taskindex` reads the model here, so either one at module load
    would be a cycle. Callers keep writing `tasks.render_tasks_index`.
    """
    if name in {"create", "claim", "transition", "run_verification", "_set_meta"}:
        from . import taskops

        return getattr(taskops, name)
    if name in {"index_stamp", "write_index", "render_tasks_index", "MAX_INDEX_ROWS"}:
        from . import taskindex

        return getattr(taskindex, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
