"""The generated tasks index.

Split out of `tasks.py` on 2026-10-04 (T-0050), when declaring the claim ledger
pushed that file past the 300-line cap. The division is the file's own: `tasks.py`
is the task model and the claim ledger, this is the generated table that is a
pure function of both. `tasks` re-exports these three names so no caller has to
know which module holds them.
"""

from __future__ import annotations

from . import paths, tasks
from .doclint import GENERATED_NOTE

MAX_INDEX_ROWS = 40


def index_stamp() -> str:
    """The date the newest claim was recorded, or the newest task's creation.

    The tasks index is a function of the ledger and the task files, never of the
    clock: a stamp taken from `now` would make the committed index "stale" on
    every day after the one it was generated on.
    """
    stamps = [str(entry.get("ts", ""))[:10] for entry in tasks.claims() if entry.get("ts")]
    if not stamps:
        stamps = [task.meta.get("created", "") for task in tasks.all_tasks()]
    return max([stamp for stamp in stamps if stamp], default="unknown")


def write_index() -> bool:
    """Write `tasks/INDEX.md` if the render differs. True when it wrote.

    Called by `origin doc index` and by the task commands themselves: every
    path that changes a row in this table rewrites it, so a task cannot be
    created, claimed or completed without the index following it.
    """
    from .report import write_if_changed

    return write_if_changed(paths.tasks_index(), render_tasks_index())


def render_tasks_index() -> str:
    found = tasks.all_tasks()
    active = tasks.active_claims()
    rows = []
    for task in found:
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
        f"{len(found)} task(s). Every task file declares a runnable verification command;",
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
