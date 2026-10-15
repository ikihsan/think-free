# Session 2026-10-14-035-fresh-observation-test-discriminating-ob

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T22:17:20+00:00
- **Duration:** 71.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Fresh observation: test discriminating-observation procedure on appliance diagnosis domain using EXPERIMENTS/092-appliance-diagnosis corpus

## Summary

Fresh observation: discriminating-observation procedure on appliance diagnosis (E092) already complete — population served by general assistant at 0.8108 (K1 pass, lower CI95 bound 0.6580), K2 FAIL (0 of 40 self-contained programs). Line closes for good: need is real and served, but no candidate needed. Also reviewed E150 SQL injection classification: structural classifier (93.8%) outperforms keyword-only (81.2%), but G2 FAILS (Δ=0.12 vs required 0.15). G3 PASS (93.8% ≥ 80%). Replicates E147 pattern: structural beats keyword but margin typically 10-12pp, below 15pp gate. Value canonicalizer 7-genre mapping: instrument genre-specific to Federal Register SUMMARY only, general claim F126 closed. All candidates across domains A-F closed. Food recall matching (E080): PASS on synthetic fixtures, real-world identifier linkage is the unaddressed bottleneck per HYPOTHESES.md. ArXiv reproducibility (E079): information-sufficiency bound confirmed — permitted inputs cannot distinguish between two repos needing different numpy versions. Key finding: across 15+ experiments, structural/feature-enhanced approaches consistently outperform pure keyword approaches, but the improvement margin typically falls short of predeclared gates. No candidates remain promising for product engineering. The mission's evidence base is comprehensive and ready for synthesis.

## Next

Consolidate evidence base and pursue fresh observation in new domain

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 90 |
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
| 1 | 22:17:20 | session_start | Fresh observation: test discriminating-observation procedure on appliance diagnosis domain using EXPERIMENTS/092-appliance-diagnosis corpus |
| 2 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 3 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 4 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 5 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 6 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 7 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 8 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
| 9 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/gates.json |
| 10 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
| 11 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 12 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 13 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 14 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 15 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 16 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 17 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 18 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 19 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 20 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 21 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 22 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 23 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 24 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 25 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 26 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 27 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/PROTOCOL.md |
| 28 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/RESULT.md |
| 29 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/analyze.py |
| 30 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/classify.py |
| 31 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/harvest.py |
| 32 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/raw_data.jsonl |
| 33 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/results.json |
| 34 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/PROTOCOL.md |
| 35 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/RESULT.md |
| 36 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/classifier.py |
| 37 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/fixtures.jsonl |
| 38 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/results.json |
| 39 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/147-postgres-deadlock-classification/run.py |
| 40 | 22:18:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/150-sql-injection-classification/PROTOCOL.md |
| 84 | 22:18:30 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-030-fresh-observation-hand-read-need-stateme/events.jsonl |
| 85 | 22:18:30 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-031-run-t-0093-test-discriminating-observati/events.jsonl |
| 86 | 22:18:31 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-032-summarize-fresh-observation-results-and/events.jsonl |
| 87 | 22:18:31 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-033-design-and-run-discriminating-observatio/events.jsonl |
| 88 | 22:18:31 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-034-check-state-next-actions-md-for-planned/events.jsonl |
| 89 | 22:18:31 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 90 | 22:18:31 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 91 | 22:18:31 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 92 | 22:18:31 | doc_update | updated STATE.md |
| 93 | 22:18:31 | session_end | Fresh observation: discriminating-observation procedure on appliance diagnosis (E092) already complete — population served by general assistant at 0.8 |

_43 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-035-fresh-observation-test-discriminating-ob/events.jsonl
```
