<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0056
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers -q && tools/origin preflight
-->

# T-0056 — Hold a mission record's restated experiment number to the artifact it 

## Goal

Hold a mission record's restated experiment number to the artifact it names

## Why this matters

docs/process/experiment-protocol.md states 113/113 for 005-knitting-bounded-search; its own results.json says cases_with_oracle=115 and cases_tested=118, and the experiment's README says 115/115. The number was wrong in the very commit that published the artifact and no gate reads a prose number against the artifact it claims. Measured: a naive 'is the number somewhere in the JSON' check PASSES this defect, because 113 also occurs at patch_cost_sensitivity/*/cases -- D025's shape.

## Preconditions

The session gate and claim predicate are as committed on origin/research/origin; no task is in flight on either VM (task list --remote)

## Steps

Write tools/sweep_result_numbers.py: for each mission record naming one experiment, report every number that is not a headline value of that experiment's results.json, and print how many it read
Run the sweep through tools/x and record the measured count, replacing the hand-run measurement
Implement the rule as a new module read by one entry point both publishing gates call, so sync land sees what doc lint sees
Falsify both directions: the rule reports 113 on the committed protocol row, and is silent on the repaired 115 and on the tip
Falsify the tempting wrong rule too: assert that an 'is the number anywhere in the artifact' check reports nothing here, so the headline restriction is load-bearing
Repair the number in the protocol row to what the artifact says, and record the finding, defect, and decision

## Acceptance criteria

- [ ] A committed script reproduces the per-document verdict from the artifacts alone, with no network
- [ ] The rule reports the false 113/113 in docs/process/experiment-protocol.md and names the file and line
- [ ] The rule is silent on the repair and on the tip, and says so with a count of what it read
- [ ] The looser 'number occurs anywhere in the artifact' rule is shown to pass the defect, so the headline restriction is proven load-bearing
- [ ] The finding, the defect entry and the decision are recorded, and doc lint and preflight pass

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers -q && tools/origin preflight
```

## Rollback

The new module and its test; reverting the commit restores the previous gate set. The corrected number is independent of the gate.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
