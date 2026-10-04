<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0031
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0031 — Allocate F, D and T identifiers from the shared base instead of from t

## Goal

Allocate F, D and T identifiers from the shared base instead of from this working tree

## Why this matters

Defect 5 in STATE-defects.md is the one fleet defect still unfixed: 'task new' reads the local tree to pick the next number, so any second VM working in the same hour takes the same number. Twelve collisions in two days between instance-0944 and instance-0947, each costing a renumber commit; instance-0944's own T-0024 became T-0026, T-0027, T-0028 and finally T-0029 across four commits. T-0030 (instance-0947, in flight) builds the detector that refuses a colliding commit; this is the half that stops the race at the source.

## Preconditions

The collision bytes exist in history: 83aa9a4 and 569a7ce each added a different tasks/T-0024-*.md on 2026-10-03 and 2026-10-04, and e6eb992 carries two '## F010' definitions. tests/harness.py make_fleet builds a bare remote and two clones, so the two-VM case can be run for real rather than mocked.

## Steps

1. Write the falsification first: with the unfixed next_task_id, a second clone whose working tree is behind the base allocates a T number the base already defines. 2. Write tools/originlib/idalloc.py to read F, D and T identifiers from a git ref (task files, claim ledger, findings and decision files) and to report the next free number with the ref and commit it came from. 3. Route task new through it, and add 'origin id next F|D|T' so a finding or decision number is allocated the same way. 4. Falsify: the new tests must fail against the unfixed allocator and pass after it; the no-remote control must still work and must say it read the local tree only.

## Acceptance criteria

- [ ] A stale clone's 'task new' allocates an identifier the shared base does not define, and prints the ref and commit it allocated from - [ ] origin id next reports F, D and T numbers read from the shared base, and exits 1 on a kind it does not know - [ ] The new tests fail against the unfixed allocator on the fleet harness and pass after the repair - [ ] A control can fail: with no remote configured the allocation is local, and the command says so - [ ] STATE-defects.md records defect 5 as half solved, names T-0030 as the detector half, and states the ceiling: two VMs allocating between their own fetches still collide - [ ] doc lint is green and no tracked file passes 300 lines

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Delete tools/originlib/idalloc.py, the two-line hook in tasks.next_task_id, the 'id' group in cli.py and tests/test_idalloc.py; the task commands, the fleet claim lock and T-0030's detector are untouched by this change.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
