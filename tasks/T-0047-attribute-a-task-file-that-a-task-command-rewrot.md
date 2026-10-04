<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0047
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_task_rewrite -q && tools/origin doc lint && tools/origin preflight
-->

# T-0047 — attribute a task file that a task command rewrote to that command, ver

## Goal

attribute a task file that a task command rewrote to that command, verified against the bytes it wrote

## Why this matters

Defect 12 is the one open defect in STATE-defects.md: task claim, task complete and task release rewrite the task file, and reconciliation reports every such file as an undeclared change, so three sessions closed with exit 4 on work the tooling itself did. The recorded fix was not made because an automatic declaration would weaken the signal; the answer is to make the declaration cover exactly the bytes the command wrote.

## Preconditions

Defect 12 in STATE-defects.md; D028 already sets the precedent of attributing a path by recorded evidence rather than authorship

## Steps

1. Reproduce the defect on a real task file: a session that runs task complete and then closes is reported for that file, and read the four committed instances from git so the shape is the record's own.
2. Record the rewrite in the appender, not the command: _set_meta is the single function that writes a task file's meta block, so the declaration goes there.
3. Bound the declaration with digests of the meta block and the body, so an agent's own later edit to the task file is reported again. This is the trade-off defect 12 refused to accept, and the digest check is the answer.
4. Read it in reconcile, so session finish stops reporting the file while every other undeclared change still reports.
5. Falsify: with the mechanism removed the new tests fail; with the digest check removed the hand-edit controls fail. Both directions, as D025 requires.
6. Record D037 in DECISIONS-SESSIONS.md, whose invariant is whose change a recorded path is; rewrite defect 12; then run the suite, doc lint and preflight.

## Acceptance criteria

- [ ] A session that runs task complete and closes reports no undeclared change for the task file, and the same session still reports every other file it changed.
- [ ] An edit to the task file after the command - to its body and to its meta block - is reported again, so the automatic declaration cannot cover the agent's own work.
- [ ] A task file changed with no command run at all is reported, and a task command run outside any session declares nothing.
- [ ] The mechanism is falsified in both directions: removing it fails the tests, and removing only the digest bound fails the hand-edit controls.
- [ ] Defect 12 is rewritten in STATE-defects.md, D037 is recorded in DECISIONS-SESSIONS.md with its rejected alternatives, and the three sources of a decision number agree.
- [ ] The full suite is green, doc lint exits 0 and preflight exits 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_task_rewrite -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit. The digests are recorded in the session event stream and nothing outside it changes shape, so an old stream simply declares nothing and reports as before.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
