# Session 2026-10-14-031-run-t-0093-test-discriminating-observati

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T21:36:03+00:00
- **Duration:** 1332.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Run T-0093: test discriminating-observation procedure against free general assistant on appliance diagnosis with correctly-filtered unanswered pool

## Summary

Designed and ran E147: fresh observation in PostgreSQL deadlock report classification domain. Created protocol with 5 predeclared kill gates, 27 synthetic fixtures (5 per category + G4 pair), structural and keyword-only classifiers. Claim falsified: keyword-only baseline achieves 100% accuracy on synthetic fixtures (categories have non-overlapping keyword signatures); structural classifier achieves 74.1% due to parsing conservatism. G2 (Δ≥15pp) FAIL, G3 (≥80%) FAIL, G5 (abstention≤20%) FAIL. Negative controls confirm keyword baseline beats structural. Experiment correctly falsifies claim per kill gate protocol. Artifacts recorded: PROTOCOL.md, fixtures.jsonl, classifier.py, run.py, results.json, RESULT.md.

## Next

Design next fresh observation experiment in a new domain with synthetic fixtures that force structural reasoning (overlapping keywords, ambiguous cases) per D083, or test a working instrument (valueset.py, pyfix, stg) against strongest accessible alternative on concrete real-world examples per brief §3.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/147-postgres-deadlock-classification/results.json | cef28bc906bc | 3314 |
| EXPERIMENTS/147-postgres-deadlock-classification/PROTOCOL.md | 1c4f5a447e0d | 6960 |
| EXPERIMENTS/147-postgres-deadlock-classification/fixtures.jsonl | a772df8b06ec | 15062 |
| EXPERIMENTS/147-postgres-deadlock-classification/classifier.py | 2c3ab6b9bd63 | 12900 |
| EXPERIMENTS/147-postgres-deadlock-classification/run.py | bd10d76c36b6 | 8128 |
| EXPERIMENTS/147-postgres-deadlock-classification/RESULT.md | 06ca48f44c52 | 5795 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 73 |
| declared artifacts now missing | 0 |
| integrity errors | 2 |
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
|   error | FAILURES.md was not updated although the session recorded experiment_result |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:36:03 | session_start | Run T-0093: test discriminating-observation procedure against free general assistant on appliance diagnosis with correctly-filtered unanswered pool |
| 2 | 21:45:07 | milestone | Completed state review: E141/E142/E143 value pre-pass genre limitation measured; T-0093 already done; view-count sweep stopped; preflight closed on de |
| 3 | 21:51:17 | artifact | wrote EXPERIMENTS/147-postgres-deadlock-classification/results.json |
| 4 | 21:51:24 | artifact | wrote EXPERIMENTS/147-postgres-deadlock-classification/PROTOCOL.md |
| 5 | 21:51:25 | artifact | wrote EXPERIMENTS/147-postgres-deadlock-classification/fixtures.jsonl |
| 6 | 21:51:27 | artifact | wrote EXPERIMENTS/147-postgres-deadlock-classification/classifier.py |
| 7 | 21:51:28 | artifact | wrote EXPERIMENTS/147-postgres-deadlock-classification/run.py |
| 8 | 21:51:50 | experiment_result | Claim falsified: keyword-only baseline achieves 100% accuracy on synthetic fixtures; structural classifier achieves 74.1%. G2 (Δ≥15pp) FAIL, G3 (≥80%) |
| 9 | 21:58:03 | artifact | wrote EXPERIMENTS/147-postgres-deadlock-classification/RESULT.md |
| 10 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 11 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 12 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 13 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 14 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 15 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 16 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
| 17 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/gates.json |
| 18 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
| 19 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 20 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 21 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 22 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 23 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 24 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 25 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 26 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 27 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 28 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 29 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 30 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 31 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 32 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 33 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 34 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 35 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/PROTOCOL.md |
| 36 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/RESULT.md |
| 37 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/analyze.py |
| 38 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/classify.py |
| 39 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/harvest.py |
| 40 | 21:58:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/raw_data.jsonl |
| 76 | 21:58:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-027-investigate-view-count-principle-classif/events.jsonl |
| 77 | 21:58:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-028-extend-value-canonicalizer-experiment-to/events.jsonl |
| 78 | 21:58:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-029-fresh-observation-test-value-canonicaliz/events.jsonl |
| 79 | 21:58:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-030-fresh-observation-hand-read-need-stateme/events.jsonl |
| 80 | 21:58:15 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 81 | 21:58:15 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 82 | 21:58:15 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 83 | 21:58:15 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 84 | 21:58:15 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 85 | 21:58:15 | session_end | Designed and ran E147: fresh observation in PostgreSQL deadlock report classification domain. Created protocol with 5 predeclared kill gates, 27 synth |

_35 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-031-run-t-0093-test-discriminating-observati/events.jsonl
```
