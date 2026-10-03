<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0010
status: open
created: 2026-10-03
claim-agent:
claim-session:
claim-vm:
verify: test -f EXPERIMENTS/004-knitting-stage-a/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/004-knitting-stage-a/results.json'));assert d['cases_tested']>0 and 'all_local_optimal' in d"
-->

# T-0010 — Run the knitting Stage-A planner comparison: local planner vs exhausti

## Goal

Run the knitting Stage-A planner comparison: local planner vs exhaustive search on small graphs

## Why this matters

T-0009 repaired the input set; the candidate's own Stage A is the next test (HYPOTHESES.md kill gate). It checks whether a local intervention planner reproduces exhaustive-search repairs on enumerably small graphs, emits a checkable action sequence, refuses unsupported states, and avoids degenerating to full release. Untested, this is the cheapest way to falsify the algorithmic-advantage sub-claim.

## Preconditions

EXPERIMENTS/003-information-sufficiency/ complete; the knitting candidate's input set now includes orientation.

## Steps

1. Model a small stitched grid with per-cell stitch and mount, a column-above release dependency, and lateral (cable) coupling. 2. Define a valid intervention as a release set closed upward and across couplings, rebuilt to target. 3. Implement exhaustive minimum-cost search over subsets for tiny grids. 4. Implement a local closure planner. 5. Compare cost and validity over single, multi-column, and coupled-error cases; measure full-release degeneration. 6. Record raw results and limits.

## Acceptance criteria

- [ ] results.json holds the per-case comparison and aggregate agreement/optimality. - [ ] A checkable action sequence is emitted for at least one case. - [ ] Unsupported states are refused, not silently accepted. - [ ] README states claim, oracle, and limits. - [ ] task verify exit 0; doc lint OK.

## Verification

```bash
test -f EXPERIMENTS/004-knitting-stage-a/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/004-knitting-stage-a/results.json'));assert d['cases_tested']>0 and 'all_local_optimal' in d"
```

## Rollback

Delete EXPERIMENTS/004-knitting-stage-a/; no product depends on it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
