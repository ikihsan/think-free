<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0066
status: claimed
created: 2026-10-05
claim-agent: opencode
claim-session: 2026-10-05-008-measure-the-outcome-distribution-of-e012
claim-vm: 
verify: python3 EXPERIMENTS/022-need-outcomes/run.py --verify
-->

# T-0066 — Measure what happens to a publicly stated unmet software need: is it a

## Goal

Measure what happens to a publicly stated unmet software need: is it answered in-thread, built by the requester, or left unanswered.

## Why this matters

The mission's last untouched asset is 1250 named people who each wrote down what was missing (STATE-next-actions item 0). No failure in the record has measured the OUTCOME of those statements. Every prior measurement counted the statement or its supply. This measures what became of them, which is the base rate the candidate question actually needs.

## Preconditions

Algolia HN API readable unauthenticated; corpus_authors.jsonl has 1401 recovered authors (E019)

## Steps

declare the kill gate in PROTOCOL.md before observing any outcome
fetch reply tree + author history for the 1401 corpus rows
hand-label a calibration sample so the served-cell oracle is not a guess
report base rates with the calibration sample's size attached

## Acceptance criteria

results.json carries all three outcome classes with counts, the hand-labelled calibration sample, and a refusal class for any unreadable row
no rate is reported without the denominator it was measured over

## Verification

```bash
python3 EXPERIMENTS/022-need-outcomes/run.py --verify
```

## Rollback

the experiment adds one directory and touches no existing record except the index and STATE

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
