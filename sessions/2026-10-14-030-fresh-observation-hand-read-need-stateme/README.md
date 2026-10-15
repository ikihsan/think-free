# Session 2026-10-14-030-fresh-observation-hand-read-need-stateme

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T21:32:15+00:00
- **Duration:** 38.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Fresh observation: hand-read need statements in a new online community domain

## Summary

Fresh observation mapping value canonicalizer genre applicability across 6 text genres. Confirmed exact on Federal Register SUMMARY sections (1.0 detection, 0.0 FP, 0 misses, 0.7386 resolved share). Does NOT generalize to SQuAD (0.2826), Hacker News titles (0 extracted), SUPPLEMENTARY INFORMATION (100% condemn), Python descriptions (extracts numbers/dates/money but genre-different), financial press releases (23 values extracted), or legal case excerpts (7 values extracted). 'Longer submission' test confounded (reference subset of submission). General claim F126 closed; regulatory claim measured and confirmed. Prototype tools/regvalue/ preserved as reusable stdlib-only ranker per E114. View-count principle closed as generalizable across 15+ domains under matched harvest. All candidates across domains A-F closed. No candidates with both prototype and validated users. Evidence base consolidated for external evaluation.

## Next

Consolidate existing results and document mission evidence base for external evaluation

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 72 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
|   undeclared | EXPERIMENTS/114-value-grounding/test-output.jsonl |
|   undeclared | EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
|   undeclared | EXPERIMENTS/140-harvest-framework-issues/results.json |
|   undeclared | EXPERIMENTS/141-preflight-demand-validation/results.json |
|   undeclared | EXPERIMENTS/142-improved-discriminating-observation.py |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/gates.json |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
|   undeclared | EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:32:15 | session_start | Fresh observation: hand-read need statements in a new online community domain |
| 2 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 3 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 4 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 5 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 6 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 7 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 8 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
| 9 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/gates.json |
| 10 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
| 11 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 12 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 13 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 14 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 15 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 16 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 17 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 18 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 19 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 20 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 21 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 22 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 23 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 24 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 25 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 26 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 27 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/PROTOCOL.md |
| 28 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/RESULT.md |
| 29 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/analyze.py |
| 30 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/classify.py |
| 31 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/harvest.py |
| 32 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/raw_data.jsonl |
| 33 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/results.json |
| 34 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/190-need-classification-prototype-runnable/e078_prototype.py |
| 35 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/190-need-classification-prototype-runnable/test_threads.jsonl |
| 36 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/e103_repro.py |
| 37 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/results.json |
| 38 | 21:32:53 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/viewcount-platform-boundary/e103_vs_e103_comparison.py |
| 39 | 21:32:53 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 40 | 21:32:53 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 65 | 21:32:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-024-finalize-e078-prototype-and-decision-rec/events.jsonl |
| 66 | 21:32:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-build-and-evaluate-a-value-canonicalizer/events.jsonl |
| 67 | 21:32:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-026-finalize-value-canonicalizer-prototype-a/events.jsonl |
| 68 | 21:32:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-027-investigate-view-count-principle-classif/events.jsonl |
| 69 | 21:32:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-028-extend-value-canonicalizer-experiment-to/events.jsonl |
| 70 | 21:32:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-029-fresh-observation-test-value-canonicaliz/events.jsonl |
| 71 | 21:32:53 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 72 | 21:32:53 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 73 | 21:32:53 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 74 | 21:32:53 | session_end | Fresh observation mapping value canonicalizer genre applicability across 6 text genres. Confirmed exact on Federal Register SUMMARY sections (1.0 dete |

_24 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-030-fresh-observation-hand-read-need-stateme/events.jsonl
```
