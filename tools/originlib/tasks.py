"""Dispatchable tasks and their claim ledger.

Git is the only shared state between machines: each task is a Markdown file and
every claim is a line appended to `tasks/CLAIMS.jsonl`. Two VMs working on
different tasks therefore never touch the same file, and a task file's history
survives in git even if a claim is forgotten.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime

from . import events, paths
from .doclint import GENERATED_NOTE

STATUSES = ("open", "claimed", "blocked", "done", "cancelled")
META_KEY = re.compile(r"<!--\s*task-meta\s*(.*?)-->", re.DOTALL)
TASK_FILE = re.compile(r"^(T-\d{4})-(.+)\.md$")
MAX_INDEX_ROWS = 40

TEMPLATE = """<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: {date}
-->

<!-- task-meta
id: {task_id}
status: open
created: {date}
claim-agent:
claim-session:
claim-vm:
verify: {verify}
-->

# {task_id} — {title}

## Goal

{goal}

## Why this matters

{rationale}

## Preconditions

{preconditions}

## Steps

{steps}

## Acceptance criteria

{acceptance}

## Verification

```bash
{verify}
```

## Rollback

{rollback}

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
"""


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
    highest = 0
    for path in task_files():
        match = TASK_FILE.match(path.name)
        if match:
            highest = max(highest, int(match.group(1)[2:]))
    return f"T-{highest + 1:04d}"


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
    return entry


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


def index_stamp() -> str:
    """The date the newest claim was recorded, or the newest task's creation.

    The tasks index is a function of the ledger and the task files, never of the
    clock: a stamp taken from `now` would make the committed index "stale" on
    every day after the one it was generated on.
    """
    stamps = [str(entry.get("ts", ""))[:10] for entry in claims() if entry.get("ts")]
    if not stamps:
        stamps = [task.meta.get("created", "") for task in all_tasks()]
    return max([stamp for stamp in stamps if stamp], default="unknown")


def render_tasks_index() -> str:
    tasks = all_tasks()
    active = active_claims()
    rows = []
    for task in tasks:
        rows.append(
            [
                f"[`{task.path.name}`]({task.path.name})",
                task.status,
                (active.get(task.task_id) or {}).get("agent", ""),
                task.meta.get("verify", "")[:48],
                (task.meta.get("created", "")),
            ]
        )
    head = [
        "# Tasks index",
        "",
        "<!-- origin-meta",
        "owner: docs/INDEX.md",
        "status: active",
        f"last-verified: {index_stamp()}",
        "-->",
        "",
        GENERATED_NOTE,
        "",
        f"{len(tasks)} task(s). Every task file declares a runnable verification command;",
        "`tools/origin task verify <id>` executes it and records the exit code.",
        "",
    ]
    table = ["| Task | Status | Claimed by | Verify | Created |", "|---|---|---|---|---|"]
    table += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows[:MAX_INDEX_ROWS]]
    if len(rows) > MAX_INDEX_ROWS:
        table.append(f"| _… {len(rows) - MAX_INDEX_ROWS} more in `tasks/`_ | | | | |")
    table.append("")
    tail = [
        "## How tasks run on another machine",
        "",
        "```bash",
        "tools/origin doctor                       # verify the VM can do the work",
        "tools/origin session start --goal \"$TASK\" --task T-0001",
        "tools/origin task claim T-0001 --agent \"$AGENT\" --vm \"$HOSTNAME\"",
        "tools/origin task verify T-0001",
        "tools/origin task complete T-0001 --summary \"…\"",
        "tools/origin session finish --outcome worked --summary \"…\" --next \"…\"",
        "```",
        "",
        "Protocol: [`../docs/process/task-lifecycle.md`](../docs/process/task-lifecycle.md).",
        "",
    ]
    text = "\n".join(head + table + tail)
    return text if text.endswith("\n") else text + "\n"


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
    """Expose taskops mutations without a circular import at module load."""
    if name in {"create", "claim", "transition", "run_verification", "_set_meta"}:
        from . import taskops

        return getattr(taskops, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
