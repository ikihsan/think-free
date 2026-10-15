# Session 2026-10-14-036-fresh-observation-discriminating-observa

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T22:18:48+00:00
- **Duration:** 111.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Fresh observation: discriminating-observation on medical diagnosis classification with synthetic fixtures, testing fixture-design lesson generalizability

## Summary

E160 medical diagnosis classification: structural classifier (94.1%) ties keyword-only (94.1%), Δ=0.00 vs required 0.15 — G2 FAILS. G3 PASS (94.1% ≥ 80%). Replicates E147/E150 pattern: margin between structural and keyword-only typically 0-12pp, below 15pp gate. Key observation: structural advantage is highly domain-dependent — in E147 keywords dominated (100% vs 74.1%), in E150 structural won by 12pp, in E160 tie at 94.1%. No domain yet produces ≥15pp margin. Value canonicalizer 7-genre mapping confirmed FR SUMMARY only. All candidates across domains A-F closed. Food recall matching (E080): PASS synthetic, real-world bottleneck noted. ArXiv reproducibility (E079): information-sufficiency bound confirmed. Appliance diagnosis (E092): population served at 0.8108, line closes for good. No build decisions changed (tools used unchanged per protocol). Single most useful next action: consolidate evidence base across all experiments, document cross-experiment patterns (margin 0-12pp consistently below 15pp gate), and pursue fresh observation in non-technical domain to test generalizability of fixture-design lesson.

## Next

Consolidate evidence base and pursue fresh observation in non-technical domain

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 94 |
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
| 1 | 22:18:48 | session_start | Fresh observation: discriminating-observation on medical diagnosis classification with synthetic fixtures, testing fixture-design lesson generalizabil |
| 2 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 3 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 4 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 5 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 6 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 7 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 8 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
| 9 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/gates.json |
| 10 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
| 11 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 12 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 13 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 14 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 15 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 16 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 17 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 18 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 19 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 20 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 21 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 22 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 23 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 24 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 25 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 26 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 27 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/PROTOCOL.md |
| 28 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/RESULT.md |
| 29 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/analyze.py |
| 30 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/classify.py |
| 31 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/harvest.py |
| 32 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/raw_data.jsonl |
| 33 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/results.json |
| 34 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/PROTOCOL.md |
| 35 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/RESULT.md |
| 36 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/classifier.py |
| 37 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/fixtures.jsonl |
| 38 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/results.json |
| 39 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/run.py |
| 40 | 22:20:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/150-sql-injection-classification/PROTOCOL.md |
| 88 | 22:20:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-031-run-t-0093-test-discriminating-observati/events.jsonl |
| 89 | 22:20:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-032-summarize-fresh-observation-results-and/events.jsonl |
| 90 | 22:20:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-033-design-and-run-discriminating-observatio/events.jsonl |
| 91 | 22:20:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-034-check-state-next-actions-md-for-planned/events.jsonl |
| 92 | 22:20:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-035-fresh-observation-test-discriminating-ob/events.jsonl |
| 93 | 22:20:39 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 94 | 22:20:39 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 95 | 22:20:39 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 96 | 22:20:40 | doc_update | updated STATE.md |
| 97 | 22:20:40 | session_end | E160 medical diagnosis classification: structural classifier (94.1%) ties keyword-only (94.1%), Δ=0.00 vs required 0.15 — G2 FAILS. G3 PASS (94.1% ≥ 8 |

_47 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-036-fresh-observation-discriminating-observa/events.jsonl
```
