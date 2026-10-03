<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0009
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-021-repair-the-knitting-witness-input-set-by
claim-vm: instance-20260717-0947
verify: python3 EXPERIMENTS/003-information-sufficiency/witness.py && python3 -c "import json;d=json.load(open('EXPERIMENTS/003-information-sufficiency/results.json'));w=d['witnesses']['W2_knitting_repair'];assert w['permitted_encoding_can_represent_the_difference'] is True and w['system']=='passive' and w['repaired'] is True"
-->

# T-0009 — Repair the knitting witness input set by adding orientation, then re-r

## Goal

Repair the knitting witness input set by adding orientation, then re-run it to confirm sufficiency

## Why this matters

T-0008's witness W2 showed the knitting candidate's stated input set is information-insufficient: two stitch states with identical chart-level inputs need different repairs because orientation is absent (F007). STATE.md next action 1 is to repair the input and re-run. Until the witness shows the repaired input is sufficient, no Stage-A planner may be built.

## Preconditions

EXPERIMENTS/003-information-sufficiency/witnesses.py and README.md exist; F007 recorded.

## Steps

1. Extend the knitting witness to model two input sets: the original (chart symbols, connectivity, live stitches, side) and a repaired set that also carries each loop's mount/orientation. 2. Re-run the search: with orientation present, the two realities must become distinguishable, so no silent pair survives. 3. Assert the repaired input is sufficient (two realities no longer share identical inputs) and record the before/after. 4. Update README.md and HYPOTHESES.md/F007 with the repair and its residual limit.

## Acceptance criteria

- [ ] Witness reports both the insufficient original input set and the sufficient repaired one. - [ ] results.json shows permitted_encoding_can_represent_the_difference true for the repaired set. - [ ] README/HYPOTHESES/F007 note the repair and remaining limits. - [ ] task verify exit 0; doc lint OK.

## Verification

```bash
python3 EXPERIMENTS/003-information-sufficiency/witness.py && python3 -c "import json;d=json.load(open('EXPERIMENTS/003-information-sufficiency/results.json'));w=d['witnesses']['W2_knitting_repair'];assert w['permitted_encoding_can_represent_the_difference'] is True and w['system']=='passive' and w['repaired'] is True"
```

## Rollback

Revert the witness edit and doc changes; the original W2 finding stands.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
