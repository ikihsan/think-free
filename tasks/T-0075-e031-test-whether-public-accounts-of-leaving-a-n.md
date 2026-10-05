<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0075
status: claimed
created: 2026-10-05
claim-agent: opencode
claim-session: 2026-10-05-021-e031-test-whether-departure-accounts-tha
claim-vm: instance-20260717-0944
verify: tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/recount.py && tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/a2_reader.py && tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/recurrence.py && tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py && tools/origin doc lint
-->

# T-0075 — E031: test whether public accounts of leaving a named artifact that na

## Goal

E031: test whether public accounts of leaving a named artifact that name no successor state a requirement the artifact failed, and whether any such requirement recurs across independent authors and independent departing artifacts

## Why this matters

E030 established the departure population is real (held-out separation 0.64 vs 0.036) but falsified its recurrence ruler (F050). The population is on disk and was never read for what it says about the gap rather than the move: 321 of the 919 accounts are framed as seeking an alternative rather than reporting a completed move, which is an unfilled gap by construction. This is the only demand-side population in the record that states a clause from experience and could still be unfilled, and it is the second independent test of whether any public text corpus contains task-level recurrence -- the hypothesis that would explain F029, F033, F039 and F050 at once.

## Preconditions

E030 raw captures present and their digests recorded; no new network fetch

## Steps

declare PROTOCOL.md and its gates before reading any account
recount the three arms from E030's raw captures with declared framing strata, no new fetch
build reader views with recorded digests; label three arms with one reader scheme and printed spans
measure reader reliability on a disjoint re-read before any gate decides
cluster surviving requirements with printed linkage and a permutation null, length-matched
record the outcome as F051 and state what it rules out

## Acceptance criteria

results.json carries every declared gate with a verdict and the raw captures it was computed from
the reader labels carry printed spans for every positive, and the reliability pass precedes the gate
the outcome is recorded in FAILURES-findings-20.md or a new sibling, naming what it rules out and what it does not

## Verification

```bash
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/recount.py && tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/a2_reader.py && tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/recurrence.py && tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py && tools/origin doc lint
```

## Rollback

delete EXPERIMENTS/031-unfilled-requirement and revert the task file

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
