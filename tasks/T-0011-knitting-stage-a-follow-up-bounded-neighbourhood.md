<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0011
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-023-t-0011-bounded-neighbourhood-knitting-pl
claim-vm: instance-20260717-0947
verify: test -f EXPERIMENTS/005-knitting-bounded-search/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/005-knitting-bounded-search/results.json'));assert d['cases_tested']>0 and 'all_bounded_optimal' in d"
-->

# T-0011 — Knitting Stage A follow-up: bounded-neighbourhood planner vs the same 

## Goal

Knitting Stage A follow-up: bounded-neighbourhood planner vs the same exhaustive oracle

## Why this matters

T-0010 showed the naive per-error heuristic is valid but suboptimal on a shared-release case; the candidate is narrow-not-abandoned pending a planner that closes releases before deciding patches, checked against the same oracle

## Preconditions

EXPERIMENTS/004-knitting-stage-a complete; the knitting candidate's input set includes orientation.

## Steps

1. Group errors whose release closures overlap into shared-release neighbourhoods. 2. For each neighbourhood, enumerate patch/release choices locally and pick the minimum-cost valid option. 3. Compare against the exhaustive oracle on the same synthetic cases; refuse unsupported states. 4. Record raw results, agreement, and limits.

## Acceptance criteria

results.json holds the per-case comparison and aggregate agreement/optimality; unsupported states refused; README states claim, oracle, and limits; task verify exit 0; doc lint OK.

## Verification

```bash
test -f EXPERIMENTS/005-knitting-bounded-search/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/005-knitting-bounded-search/results.json'));assert d['cases_tested']>0 and 'all_bounded_optimal' in d"
```

## Rollback

Delete EXPERIMENTS/005-knitting-bounded-search/; no product depends on it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
