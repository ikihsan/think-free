<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0014
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: test -f EXPERIMENTS/006-ventilation-measurement-design/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/006-ventilation-measurement-design/results.json'));assert d['pairs_tested']>0 and 'adaptive_better_than_fixed' in d and 'false_precise_rate' in d"
-->

# T-0014 — C2 ventilation kill gate: adaptive next-measurement selection vs a fix

## Goal

C2 ventilation kill gate: adaptive next-measurement selection vs a fixed door protocol on paired hypotheses

## Why this matters

RESEARCH/C.md hypothesis 2 names this as the smallest runnable falsification experiment and STATE.md ranks it first. Paired two-room parameter sets yield nearly identical passive traces; three protocols are compared at equal observation/intervention budget; changing-weather and poor-mixing holdouts violate the estimator model.

## Preconditions

EXPERIMENTS/005-knitting-bounded-search complete; W3 witness survives (the mechanism is information-sufficient given an askable observation); no product commitment.

## Steps

1. Two-room mass-balance simulator with outdoor and inter-room exchange, per-sensor offset, noise, occupancy source schedule, weather multiplier and a mixing-fidelity switch. 2. Paired parameter sets chosen so their room-A passive traces are nearly identical but their room-B traces differ. 3. One shared grid maximum-likelihood estimator used by every protocol, so only the measurement design differs. 4. Three protocols at equal budget: passive, fixed door open/closed, adaptive selection from a small action menu. 5. Metrics: pairwise discrimination accuracy, ventilation-rate error, 90% interval coverage, false-precise rate. 6. Holdout cases with changing weather and poor mixing that violate the estimator. 7. Record raw results, ceilings, and limits.

## Acceptance criteria

results.json holds per-pair and aggregate metrics for all three protocols on both specified and violating conditions; README states the claim, the estimator, the kill gate, and the limits; task verify exit 0; doc lint exit 0; tests green.

## Verification

```bash
test -f EXPERIMENTS/006-ventilation-measurement-design/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/006-ventilation-measurement-design/results.json'));assert d['pairs_tested']>0 and 'adaptive_better_than_fixed' in d and 'false_precise_rate' in d"
```

## Rollback

Delete EXPERIMENTS/006-ventilation-measurement-design/; no product depends on it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
