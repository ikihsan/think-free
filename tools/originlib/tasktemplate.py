"""The document a task file is written from.

Split out of `tasks.py` because the template is a document shape rather than a
task model, and because the model has a 300-line cap that a 50-line string
constant should not spend. `docs/process/task-lifecycle.md` says what each
field is for; `taskops.create` fills it in.
"""

from __future__ import annotations

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
