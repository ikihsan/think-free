<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0053
status: claimed
created: 2026-10-04
claim-agent: unknown-agent
claim-session: 2026-10-04-038-record-a-base-advance-when-a-paused-reba
claim-vm: 
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_land_hand_completed_rebase -q && tools/origin preflight
-->

# T-0053 — Record a base_advance when a paused rebase is completed by hand

## Goal

Record a base_advance when a paused rebase is completed by hand

## Why this matters

T-0048 made land finish a rebase it stopped on, but a human who completes one with plain 'git rebase --continue' still records no base_advance, so every arrived path is attributed to whichever session resolved the conflict. Git leaves ORIG_HEAD and the replay markers, so the arrival is recoverable.

## Preconditions



## Steps

Reproduce with the fleet harness: conflict, human 'git rebase --continue', then a land or reconcile records no base_advance
Distinguish a finished rebase from a merge or fast-forward using git's own state (no merge commits, replayed patches, arrival not already recorded)
Record base_advance with the arrived commits so attribution follows authorship
Falsify both directions: a merge or ff-pull must not be recorded, and without the repair nothing is recorded

## Acceptance criteria

A hand-completed rebase's arrival is recorded as a base_advance event naming its commits
A merge or fast-forward is not misrecorded as a rebase
The full suite, doc lint and preflight pass

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_land_hand_completed_rebase -q && tools/origin preflight
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
