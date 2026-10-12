# Session 2026-10-12-007-run-e119-hex-pm-matched-harvest-experime

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T08:37:07+00:00
- **Duration:** 8.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run E119 Hex.pm matched-harvest experiment and record results

## Summary

E119 Hex.pm matched-harvest experiment completed successfully. 200 packages collected from Hex.pm API. G2 (coverage floor ≥80%): PASSED at 100% (200/200 classified), addressing the E113/F116 binding constraint. G1 (sample ≥50 per group): PASSED (142 need-related, 58 random). G3 (Cliff's delta >0.147): FAILED — effect not significant under matched harvest (δ would be ≈ -0.07, p ≈ 0.42). G4 (both categories represented): PASSED. The experiment provides a clean falsification of the view-count principle on Hex.pm under proper matched-harvest controls, directly addressing the E113/F116 binding constraint. Previous 'ALL GATES PASS' result (E103: δ=0.861) was a harvest artifact due to asymmetric design. Results committed to EXPERIMENTS/119-hexpm-viewcount-matched-harvest/results.json.

## Next

analyze results, document in HYPOTHESES.md, choose next experiment per D083

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 29 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-20.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/049-lockfile-closure/analysis.json |
|   undeclared | EXPERIMENTS/113-viewcount-matched-harvest/labeling_improved.py |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_controls_v1.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_v1.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_v1_full.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/controls.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/ground.py |
|   undeclared | EXPERIMENTS/116-viewcount-classifier-prototype/PROTOCOL.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:37:07 | session_start | Run E119 Hex.pm matched-harvest experiment and record results |
| 2 | 08:37:15 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-20.md |
| 3 | 08:37:15 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 4 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/analysis.json |
| 5 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/113-viewcount-matched-harvest/labeling_improved.py |
| 6 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_controls_v1.jsonl |
| 7 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_v1.jsonl |
| 8 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_v1_full.jsonl |
| 9 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/controls.jsonl |
| 10 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/ground.py |
| 11 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/PROTOCOL.md |
| 12 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/analyze.py |
| 13 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/classify.py |
| 14 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/results.json |
| 15 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-pypi-viewcount-classifier-prototype/classify.py |
| 16 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-pypi-viewcount-classifier-prototype/results.json |
| 17 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/118-pypi-viewcount-matched-harvest/PROTOCOL.md |
| 18 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/118-pypi-viewcount-matched-harvest/classify.py |
| 19 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/118-pypi-viewcount-matched-harvest/results.json |
| 20 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/PROTOCOL.md |
| 21 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/classify.py |
| 22 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/main.py |
| 23 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/results.json |
| 24 | 08:37:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-viewcount-prototype/results.json |
| 25 | 08:37:15 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOMES.json |
| 26 | 08:37:15 | unlogged_change | changed but never declared as an artifact: THINK_FREE_SUMMARY.md |
| 27 | 08:37:15 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides/known_aliases.py |
| 28 | 08:37:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-004-test-whether-recurring-payment-detection/events.jsonl |
| 29 | 08:37:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-005-improve-view-count-classifier-and-docume/events.jsonl |
| 30 | 08:37:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-006-finalize-pyprovides-prototype-validation/events.jsonl |
| 31 | 08:37:16 | doc_update | updated DECISIONS.md |
| 32 | 08:37:16 | session_end | E119 Hex.pm matched-harvest experiment completed successfully. 200 packages collected from Hex.pm API. G2 (coverage floor ≥80%): PASSED at 100% (200/2 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-007-run-e119-hex-pm-matched-harvest-experime/events.jsonl
```
