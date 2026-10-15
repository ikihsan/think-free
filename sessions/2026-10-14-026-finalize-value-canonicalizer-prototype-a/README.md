# Session 2026-10-14-026-finalize-value-canonicalizer-prototype-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T20:49:44+00:00
- **Duration:** 26.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Finalize value canonicalizer prototype and decide continuation

## Summary

Value canonicalizer prototype finalized. CLI tool tools/regvalue/regvalue_cli.py implements ground.py+valueset.py for extracting and grounding named values (dates, money, codes, pct, qty, num) from regulatory text. Tested on 3 Federal Register documents (E114/E142 corpus): Doc 2026-21031—4 values, 3 grounded (75%), 1 ungrounded_claim (25%); Doc 2026-21019—5 values, 3 grounded (60%), 1 ungrounded_value (20%), 1 ungrounded_claim (20%); Doc 2026-21020—3 values, 0 grounded (0%), 3 ungrounded_value (100%) HTML normalization issue. Genre specificity confirmed per E114/E142 (works on Federal Register, fails on SQuAD/Hacker News). HTML normalization issue observed on one doc. Single most useful next action: run prototype on 20+ document Federal Register corpus to establish baseline grounded/ungrounded rates and further delineate applicability domain, producing evidence for decision: refine for regulatory compliance use, apply to new domain, or close line.

## Next

Run regvalue_cli.py on larger Federal Register corpus (20+ documents) to establish statistically reliable grounded rates and delineate instrument applicability domain. If grounded rate ≥70% on dates+codes+≥50% on money, instrument has viable niche as ranked human-review prioritizer (per E114: worthless as gate but worth reusing as ranker). If grounded rate <50% on 20 documents, instrument confirmed as not practical for general regulatory value extraction.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 58 |
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
| 1 | 20:49:44 | session_start | Finalize value canonicalizer prototype and decide continuation |
| 2 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 3 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 4 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 5 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 6 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 7 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 8 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 9 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 10 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 11 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 12 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 13 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 14 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 15 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 16 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 17 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 18 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 19 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 20 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 21 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 22 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 23 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 24 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/190-need-classification-prototype-runnable/e078_prototype.py |
| 25 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/190-need-classification-prototype-runnable/test_threads.jsonl |
| 26 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/e103_repro.py |
| 27 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/results.json |
| 28 | 20:50:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/viewcount-platform-boundary/e103_vs_e103_comparison.py |
| 29 | 20:50:10 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 30 | 20:50:10 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 31 | 20:50:10 | unlogged_change | changed but never declared as an artifact: checked-output.jsonl |
| 32 | 20:50:10 | unlogged_change | changed but never declared as an artifact: experiment_t0094_results.json |
| 33 | 20:50:10 | unlogged_change | changed but never declared as an artifact: session-record-E142.json |
| 34 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/commands.log |
| 35 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/events.jsonl |
| 36 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-007-final-session-recording-and-continuation/events.jsonl |
| 37 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/commands.log |
| 38 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/events.jsonl |
| 39 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-regvalue-tool-creation-and-docu/commands.log |
| 40 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-regvalue-tool-creation-and-docu/events.jsonl |
| 51 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-020-fresh-observation-view-count-principle-o/events.jsonl |
| 52 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-021-finish-e078-need-classification-prototyp/events.jsonl |
| 53 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-022-record-continuation-decision-for-e078-pr/events.jsonl |
| 54 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-023-record-continuation-decision-for-e078-pr/events.jsonl |
| 55 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-024-finalize-e078-prototype-and-decision-rec/events.jsonl |
| 56 | 20:50:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-build-and-evaluate-a-value-canonicalizer/events.jsonl |
| 57 | 20:50:10 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 58 | 20:50:10 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 59 | 20:50:10 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 60 | 20:50:11 | session_end | Value canonicalizer prototype finalized. CLI tool tools/regvalue/regvalue_cli.py implements ground.py+valueset.py for extracting and grounding named v |

_10 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-026-finalize-value-canonicalizer-prototype-a/events.jsonl
```
