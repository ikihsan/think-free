<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0007
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: test -f EXPERIMENTS/002-a1-masking/distance.json && grep -q gate EXPERIMENTS/002-a1-masking/distance.json
-->

# T-0007 — 002-a1-masking: distance-limited (fieldwork-cost) budget variant

## Goal

002-a1-masking: distance-limited (fieldwork-cost) budget variant

## Why this matters

T-0006 showed DD's advantage vanishes only at the K~budget corner; the open question is whether DD survives a realistic cost metric (meters walked), not more ranking heuristics

## Preconditions

002 masks and substrate available; session 017 green

## Steps

Implement distance-budget observation walk reusing masking.py; run 30 seeds x 2 masks x 3 distance budgets; record gate outcome

## Acceptance criteria

- [ ] distance.json exists with raw results and gate

## Verification

```bash
test -f EXPERIMENTS/002-a1-masking/distance.json && grep -q gate EXPERIMENTS/002-a1-masking/distance.json
```

## Rollback

discard EXPERIMENTS/002-a1-masking/distance.json and task T-0007

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
