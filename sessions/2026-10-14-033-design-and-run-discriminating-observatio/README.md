# Session 2026-10-14-033-design-and-run-discriminating-observatio

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T22:12:22+00:00
- **Duration:** 133.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Design and run discriminating-observation experiment on SQL injection classification domain

## Summary

E150 SQL injection classification experiment: structural classifier (93.8%) outperforms keyword-only (81.2%), but G2 FAILS (Δ=0.12 vs required 0.15). G3 PASS (93.8% ≥ 80%). G1 FAILS (structural doesn't achieve 100% on 16/16 synthetic fixtures). Replicates E147 pattern: structural beats keyword but margin typically 10-12pp, below 15pp gate. Key finding: structural features (UNION detection, delay functions, boolean patterns, extractvalue/updatexml) provide meaningful classification improvement over pure keywords, but not enough for the 15pp gate. Per-fixture analysis shows structural correctly classifies 15/16 vs keyword-only 13/16. The 12pp margin is consistent across runs and below the gate threshold. Single most useful next action: consolidate experiment results and pursue fresh observation in different domain, rather than adjusting gates to manufacture success.

## Next

Consolidate all experiment results (E150, E147, value canonicalizer 7-genre) and pursue fresh observation in new domain

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 88 |
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
| 1 | 22:12:22 | session_start | Design and run discriminating-observation experiment on SQL injection classification domain |
| 2 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 3 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 4 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 5 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 6 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 7 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 8 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
| 9 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/gates.json |
| 10 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
| 11 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 12 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 13 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 14 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 15 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 16 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 17 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 18 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 19 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 20 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 21 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 22 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 23 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 24 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 25 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 26 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 27 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/PROTOCOL.md |
| 28 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/RESULT.md |
| 29 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/analyze.py |
| 30 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/classify.py |
| 31 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/harvest.py |
| 32 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/raw_data.jsonl |
| 33 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/results.json |
| 34 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/PROTOCOL.md |
| 35 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/RESULT.md |
| 36 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/classifier.py |
| 37 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/fixtures.jsonl |
| 38 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/results.json |
| 39 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/run.py |
| 40 | 22:14:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/150-sql-injection-classification/PROTOCOL.md |
| 82 | 22:14:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-028-extend-value-canonicalizer-experiment-to/events.jsonl |
| 83 | 22:14:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-029-fresh-observation-test-value-canonicaliz/events.jsonl |
| 84 | 22:14:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-030-fresh-observation-hand-read-need-stateme/events.jsonl |
| 85 | 22:14:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-031-run-t-0093-test-discriminating-observati/events.jsonl |
| 86 | 22:14:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-032-summarize-fresh-observation-results-and/events.jsonl |
| 87 | 22:14:34 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 88 | 22:14:34 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 89 | 22:14:35 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 90 | 22:14:35 | doc_update | updated STATE.md |
| 91 | 22:14:35 | session_end | E150 SQL injection classification experiment: structural classifier (93.8%) outperforms keyword-only (81.2%), but G2 FAILS (Δ=0.12 vs required 0.15).  |

_41 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-033-design-and-run-discriminating-observatio/events.jsonl
```
