<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0041
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0041 — Make sync land rebuild any generated file the rebase left stale, not o

## Goal

Make sync land rebuild any generated file the rebase left stale, not only the ones git reports as conflicted

## Why this matters

Commit e942225 was published with a stale sessions/INDEX.md: land regenerated only the generated files git reported as conflicted, and two VMs adding one session each produce two renders that merge cleanly. doc lint on that commit says 'generated file is stale'. Defect 13; the fourth arrival of the family whose first three repairs each fixed the layer that happened to be running.

## Preconditions



## Steps

1. Reproduce it: one VM records a session and regenerates the index, the other records one and does not, then land. The property asserted is that every generated file equals its renderer afterwards. 2. Add syncland._refresh_generated, which asks doc lint's question rather than git's, and commit the answer before the push refuses a dirty tree. 3. Falsify: with the call removed the new test fails and its control stays green. 4. Split test_sync.py into test_sync.py and test_land.py by operation, since the land tests passed the 300-line cap.

## Acceptance criteria

After land, all three generated files equal what their renderers produce, including the one git merged without a conflict
A missing generated file is rebuilt rather than skipped
With the repair removed the new test fails and the control that correct files are left alone stays green
A land that changes nothing commits nothing
STATE-defects.md, docs/process/multi-vm-coordination.md and tests/README.md record the defect, the layer it lived in, and the ceiling

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

git revert the syncland change; the two new tests then fail, which is the point

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
