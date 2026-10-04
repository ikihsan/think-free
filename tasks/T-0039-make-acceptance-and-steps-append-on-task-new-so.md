<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0039
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0039 — Make --acceptance and --steps append on task new, so five criteria do 

## Goal

Make --acceptance and --steps append on task new, so five criteria do not become one

## Why this matters

Defect 11 in STATE-defects.md, found in T-0036 by using the documented workflow: five --acceptance flags left one line in the task file and printed nothing. The task file is the record of what 'done' means, so a truncated one makes a completed task look complete against a definition nobody can see - the same shape as F010's near-vacuous gate.

## Preconditions



## Steps

1. Write the test first and run it against the current parser: three --acceptance flags must produce three lines, and the same for --steps. It must fail before the change. 2. Declare both with action=append and default=[] in cli_args.py, and join them in cli_task.py so taskops.create keeps taking a string. 3. Check the single-flag path still renders one line, and that a task created with no flags still gets the placeholder. 4. Record the related reconciliation gap - two sessions in a row left the task file undeclared because task claim and task complete change it and nothing declares it.

## Acceptance criteria

STATE-defects.md defect 11 is closed with its ceiling, and the related reconciliation gap is recorded

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

git revert the two lines in cli_args.py and the join in cli_task.py; the tests then fail, which is the point

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
