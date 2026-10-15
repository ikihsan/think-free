# Session 2026-10-14-025-build-and-evaluate-a-value-canonicalizer

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T20:47:59+00:00
- **Duration:** 47.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Build and evaluate a value canonicalizer prototype for regulatory text extraction

## Summary

Built tools/regvalue/regvalue_cli.py CLI prototype implementing ground.py+valueset.py canonicalizer for regulatory text extraction. Tested on 3 Federal Register documents: dates and CFR codes reliably grounded (75-60% grounded rates), money values variable (ungrounded_claim/ungrounded_value). Genre specificity confirmed per E114/E142. HTML normalization issue observed on one document. Single most useful next action: run on 20+ document corpus to establish applicability domain boundaries

## Next

Run prototype on larger Federal Register corpus to establish applicability domain boundaries

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 57 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
|   undeclared | EXPERIMENTS/114-value-grounding/test-output.jsonl |
|   undeclared | EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
|   undeclared | EXPERIMENTS/140-harvest-framework-issues/results.json |
|   undeclared | EXPERIMENTS/141-preflight-demand-validation/results.json |
|   undeclared | EXPERIMENTS/142-improved-discriminating-observation.py |
|   undeclared | EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 20:47:59 | session_start | Build and evaluate a value canonicalizer prototype for regulatory text extraction |
| 2 | 20:48:13 | milestone | value canonicalizer prototype built and evaluated |
| 3 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 4 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 5 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 6 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 7 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 8 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 9 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 10 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 11 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 12 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 13 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 14 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 15 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 16 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 17 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 18 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 19 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 20 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 21 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 22 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 23 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 24 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 25 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/190-need-classification-prototype-runnable/e078_prototype.py |
| 26 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/190-need-classification-prototype-runnable/test_threads.jsonl |
| 27 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/e103_repro.py |
| 28 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/results.json |
| 29 | 20:48:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/viewcount-platform-boundary/e103_vs_e103_comparison.py |
| 30 | 20:48:46 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 31 | 20:48:46 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 32 | 20:48:46 | unlogged_change | changed but never declared as an artifact: checked-output.jsonl |
| 33 | 20:48:46 | unlogged_change | changed but never declared as an artifact: experiment_t0094_results.json |
| 34 | 20:48:46 | unlogged_change | changed but never declared as an artifact: session-record-E142.json |
| 35 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/commands.log |
| 36 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/events.jsonl |
| 37 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-007-final-session-recording-and-continuation/events.jsonl |
| 38 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/commands.log |
| 39 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/events.jsonl |
| 40 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-regvalue-tool-creation-and-docu/commands.log |
| 51 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-019-record-continuation-decision-for-ventila/events.jsonl |
| 52 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-020-fresh-observation-view-count-principle-o/events.jsonl |
| 53 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-021-finish-e078-need-classification-prototyp/events.jsonl |
| 54 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-022-record-continuation-decision-for-e078-pr/events.jsonl |
| 55 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-023-record-continuation-decision-for-e078-pr/events.jsonl |
| 56 | 20:48:46 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-024-finalize-e078-prototype-and-decision-rec/events.jsonl |
| 57 | 20:48:46 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 58 | 20:48:46 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 59 | 20:48:46 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 60 | 20:48:46 | session_end | Built tools/regvalue/regvalue_cli.py CLI prototype implementing ground.py+valueset.py canonicalizer for regulatory text extraction. Tested on 3 Federa |

_10 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-025-build-and-evaluate-a-value-canonicalizer/events.jsonl
```
