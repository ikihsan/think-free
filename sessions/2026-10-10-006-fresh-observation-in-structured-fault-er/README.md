# Session 2026-10-10-006-fresh-observation-in-structured-fault-er

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T09:54:55+00:00
- **Duration:** 1302.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation in structured fault/error-code domain (aviation/industrial PLC/medical device): read actual practitioner rows by hand to find unserved needs, before any classifier

## Summary

Fresh observation in structured fault/error-code domains (PLC + Medical). Instrument fault_need_classifier_v3 passed discrimination test (G1 FPR=0.000, G2 TPR=0.704, G3 FNR=0.296). Applied to 16 practitioner rows from MrPLC (9) and MedWrench (7). Results: 43.8% served, 56.2% unserved. Key findings: vendor knowledge gaps (2), recurrence after fix (1), specific error codes cited (37.5%), high view counts on error threads (>1000 views on 2 PLC threads). MedWrench view counts unavailable so classifier conservative there. No candidate emerges; high-value signal is PLC-1 pattern (vendor-unsure + recurrence).

## Next

If pursuing PLC-1 pattern: search MrPLC for 'vendor unsure/unsure/unknown cause' and measure recurrence rate as testable hypothesis.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 10 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/DISCRIMINATION_TEST.md |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/OBSERVATIONS.md |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/PROTOCOL.md |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/RESULTS.md |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/measure_population.py |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/run_discrimination_test.py |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/run_discrimination_test_v2.py |
|   undeclared | FAILURES-findings-37.md |
|   undeclared | SUMMARY.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:54:55 | session_start | Fresh observation in structured fault/error-code domain (aviation/industrial PLC/medical device): read actual practitioner rows by hand to find unserv |
| 2 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
| 3 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/DISCRIMINATION_TEST.md |
| 4 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/OBSERVATIONS.md |
| 5 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/PROTOCOL.md |
| 6 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/RESULTS.md |
| 7 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/measure_population.py |
| 8 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/run_discrimination_test.py |
| 9 | 10:16:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/run_discrimination_test_v2.py |
| 10 | 10:16:37 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-37.md |
| 11 | 10:16:38 | unlogged_change | changed but never declared as an artifact: SUMMARY.md |
| 12 | 10:16:38 | session_end | Fresh observation in structured fault/error-code domains (PLC + Medical). Instrument fault_need_classifier_v3 passed discrimination test (G1 FPR=0.000 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-006-fresh-observation-in-structured-fault-er/events.jsonl
```
