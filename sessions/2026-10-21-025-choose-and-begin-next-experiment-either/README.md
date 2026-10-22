# Session 2026-10-21-025-choose-and-begin-next-experiment-either

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T17:40:49+00:00
- **Duration:** 1110.6s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Choose and begin next experiment: either fresh observation in new domain axis per D083, or prototype tool for enterable federal IT sub-segments

## Summary

E217: Fresh observation in FDA drug recalls (new domain axis per D083). Tested hypothesis that compounding pharmacies have higher Class I recall rates than commercial manufacturers. Complete census of 18,043 FDA enforcement reports via openFDA API. Result: hypothesis directionally wrong (commercial manufacturers 6.4× higher Class I rate: 12.1% vs 1.9%). Kill gates G2 (p=1.0) and G3 (OR=0.14) fired. No candidate. Updated STATE.md and STATE-next-actions.md.

## Next

Fresh observation in another new domain axis per D083, or prototype tool for enterable IT sub-segments, or refined FDA recall hypothesis (e.g., Class I recall → product discontinuation via NDC linkage).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E217-fda-recall-compounding/PROTOCOL.md | 9e42bab00232 | 2636 |
| EXPERIMENTS/E217-fda-recall-compounding/run.py | 9af2db29529c | 9297 |
| EXPERIMENTS/E217-fda-recall-compounding/RESULT.md | 3607f5a55d88 | 3368 |
| EXPERIMENTS/E217-fda-recall-compounding/raw/gate-results.json | 28275b8e99e3 | 486 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 81 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/controls.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/gates.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/per_category.csv |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:40:49 | session_start | Choose and begin next experiment: either fresh observation in new domain axis per D083, or prototype tool for enterable federal IT sub-segments |
| 2 | 17:56:30 | artifact | wrote EXPERIMENTS/E217-fda-recall-compounding/PROTOCOL.md |
| 3 | 17:56:33 | artifact | wrote EXPERIMENTS/E217-fda-recall-compounding/run.py |
| 4 | 17:56:35 | artifact | wrote EXPERIMENTS/E217-fda-recall-compounding/RESULT.md |
| 5 | 17:57:10 | artifact | wrote EXPERIMENTS/E217-fda-recall-compounding/raw/gate-results.json |
| 6 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
| 7 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
| 8 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
| 9 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
| 10 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 11 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/controls.py |
| 12 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 13 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/gates.json |
| 14 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
| 15 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/per_category.csv |
| 16 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/probe.py |
| 17 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
| 18 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
| 19 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
| 20 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
| 21 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
| 22 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
| 23 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/fetch_summary.json |
| 24 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw_probe.json |
| 25 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/recompute.py |
| 26 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 27 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 28 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 29 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
| 30 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
| 31 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 32 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/raw/analysis.json |
| 33 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
| 34 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/raw/analysis.json |
| 35 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/PROTOCOL.md |
| 36 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/RESULT.md |
| 37 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/results_partial.json |
| 38 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/run.py |
| 39 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/PROTOCOL.md |
| 40 | 17:59:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/RESULT.md |
| 79 | 17:59:19 | unlogged_change | changed but never declared as an artifact: tools/it_entrant_advisor.py |
| 80 | 17:59:19 | unlogged_change | changed but never declared as an artifact: tools/it_entrant_advisor_v3.py |
| 81 | 17:59:19 | unlogged_change | changed but never declared as an artifact: tools/nih_accessibility_prototype.py |
| 82 | 17:59:19 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_advisor_v3.py |
| 83 | 17:59:19 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_entry_advisor.py |
| 84 | 17:59:19 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_screener.py |
| 85 | 17:59:19 | unlogged_change | changed but never declared as an artifact: tools/small_program_advisor.py |
| 86 | 17:59:19 | unlogged_change | changed but never declared as an artifact: writing-plan-small-program-advisor.md |
| 87 | 17:59:20 | doc_update | updated STATE.md |
| 88 | 17:59:20 | session_end | E217: Fresh observation in FDA drug recalls (new domain axis per D083). Tested hypothesis that compounding pharmacies have higher Class I recall rates |

_38 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-025-choose-and-begin-next-experiment-either/events.jsonl
```
