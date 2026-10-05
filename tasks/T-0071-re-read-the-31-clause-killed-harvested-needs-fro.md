<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0071
status: claimed
created: 2026-10-05
claim-agent: opencode
claim-session: 2026-10-05-015-re-read-the-31-clause-killed-harvested-n
claim-vm: 
verify: python3 EXPERIMENTS/027-cause-of-death-reread/recheck.py --selftest && python3 EXPERIMENTS/027-cause-of-death-reread/stats.py
-->

# T-0071 — Re-read the 31 clause-killed harvested needs from their full comment t

## Goal

Re-read the 31 clause-killed harvested needs from their full comment text and test whether F029's 'vague' cause of death is an artefact of the clause-extraction rule

## Why this matters

F029's 0-of-50, the measurement that closed both candidate generators and emptied item 0d's seat, assigned 31 of 50 causes of death by reading a clause produced by a one-line regex (the text between a trigger phrase and the first sentence break, capped at 300 chars). Thirteen rows have >=20 words of comment text after the clause that the screen never saw, and three clauses are not even substrings of their own text. One recorded reason asserts 'no mechanism stated anywhere in the comment' - a claim about the whole comment made without reading it.

## Preconditions

No network. All text is already in EXPERIMENTS/012-candidate-harvest/raw/screened.jsonl.

## Steps

Write PROTOCOL.md with the gate before any classification. Extract the 31-row population with full text only. Two blind readers classify from full text, never seeing the original verdict; kappa computed. Compare. Report the restated cause table.

## Acceptance criteria

The 31 rows carry a second independent classification from full text, kappa is reported, and the restated cause table is computed from the captures by script.

## Verification

```bash
python3 EXPERIMENTS/027-cause-of-death-reread/recheck.py --selftest && python3 EXPERIMENTS/027-cause-of-death-reread/stats.py
```

## Rollback

New experiment directory only; no record is amended until the number is known.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
