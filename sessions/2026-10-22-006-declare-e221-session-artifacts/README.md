# Session 2026-10-22-006-declare-e221-session-artifacts

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-22
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-22T05:57:31+00:00
- **Duration:** 33.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Declare E221 session artifacts

## Summary

E221 PSC NAICS sub-segment analysis completed on cached data. Extended E220 prototype to all 25 PSC codes using cached USAspending data. Analysis of 34 sub-segments confirms E220 findings: NAICS 541511 and 541519 consistently HIGHLY ENTERABLE. Three enterable sub-segments identified. All 5 gates pass. Full API run pending 14+ hours.

## Next

Run full 25-PSC-code analysis via USAspending API (python3 tools/psc_naics_subsegment_analyzer.py --max-psc 25 --top-naics 8), estimated 14+ hours at 60 req/hour rate limit. Cache from this session can be reused for incremental execution.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E221-psc-naics-subsegment-extension/RESULT.md | ce69b4378722 | 8358 |
| EXPERIMENTS/E221-psc-naics-subsegment-extension/gates.json | 64b25bbf90ae | 248 |
| EXPERIMENTS/E221-psc-naics-subsegment-extension/manual_analysis_summary.txt | 9bfa9054ab24 | 685 |
| EXPERIMENTS/E221-psc-naics-subsegment-extension/ranked_subsegments.csv | 7fec0b768c57 | 1732 |
| EXPERIMENTS/E221-psc-naics-subsegment-extension/subsegment_metrics.csv | be8455118cbe | 2078 |
| analyze_cache.py | c2b2343acd87 | 11555 |

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
|   undeclared | DECISIONS-RECORDS-6.md |
|   undeclared | DECISIONS-SCREENING.md |
|   undeclared | EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
|   undeclared | EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
|   undeclared | EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
|   undeclared | EXPERIMENTS/E215-comtrade-entrant-accessibility/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E215-comtrade-entrant-accessibility/RESULT.md |
|   undeclared | EXPERIMENTS/E216-small-program-advisor/PLAN-it-advisor-enhancement.md |
|   undeclared | EXPERIMENTS/E216-small-program-advisor/PLAN.md |
|   undeclared | EXPERIMENTS/E216-small-program-advisor/PROTOCOL.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:57:31 | session_start | Declare E221 session artifacts |
| 2 | 05:57:41 | artifact | wrote EXPERIMENTS/E221-psc-naics-subsegment-extension/RESULT.md |
| 3 | 05:57:43 | artifact | wrote EXPERIMENTS/E221-psc-naics-subsegment-extension/gates.json |
| 4 | 05:57:45 | artifact | wrote EXPERIMENTS/E221-psc-naics-subsegment-extension/manual_analysis_summary.txt |
| 5 | 05:57:48 | artifact | wrote EXPERIMENTS/E221-psc-naics-subsegment-extension/ranked_subsegments.csv |
| 6 | 05:57:50 | artifact | wrote EXPERIMENTS/E221-psc-naics-subsegment-extension/subsegment_metrics.csv |
| 7 | 05:57:52 | artifact | wrote analyze_cache.py |
| 8 | 05:58:03 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-6.md |
| 9 | 05:58:03 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING.md |
| 10 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 11 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 12 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
| 13 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/PROTOCOL.md |
| 14 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/RESULT.md |
| 15 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/PLAN-it-advisor-enhancement.md |
| 16 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/PLAN.md |
| 17 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/PROTOCOL.md |
| 18 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/RESULT.md |
| 19 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E218-openalex-topic-entrant-share/PROTOCOL.md |
| 20 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E218-openalex-topic-entrant-share/RESULT.md |
| 21 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E218-openalex-topic-entrant-share/run_experiment.py |
| 22 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E218-openalex-topic-entrant-share/session_log.log |
| 23 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E219-wb-theme-entrant-share/RESULT.md |
| 24 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E220-it-subsegment-entrant-advisor/PROTOCOL.md |
| 25 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E220-it-subsegment-entrant-advisor/RESULT.md |
| 26 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E221-psc-naics-subsegment-extension/PROTOCOL.md |
| 27 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/analyze.py |
| 28 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/fetch_outcome.py |
| 29 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_334111_2024.json |
| 30 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_334111_2024.meta.json |
| 31 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_511210_2024.json |
| 32 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_511210_2024.meta.json |
| 33 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_513210_2024.json |
| 34 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_513210_2024.meta.json |
| 35 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_518210_2024.json |
| 36 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_518210_2024.meta.json |
| 37 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541330_2024.json |
| 38 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541330_2024.meta.json |
| 39 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541511_2024.json |
| 40 | 05:58:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541511_2024.meta.json |
| 97 | 05:58:04 | unlogged_change | changed but never declared as an artifact: tools/results/psc_naics_subsegment/ranked_subsegments.csv |
| 98 | 05:58:04 | unlogged_change | changed but never declared as an artifact: tools/results/psc_naics_subsegment/subsegment_metrics.csv |
| 99 | 05:58:04 | unlogged_change | changed but never declared as an artifact: tools/results/test_single_year/gates.json |
| 100 | 05:58:04 | unlogged_change | changed but never declared as an artifact: tools/results/test_single_year/ranked_subsegments.csv |
| 101 | 05:58:04 | unlogged_change | changed but never declared as an artifact: tools/results/test_single_year/subsegment_metrics.csv |
| 102 | 05:58:04 | doc_update | updated DECISIONS-RECORDS-6.md |
| 103 | 05:58:04 | doc_update | updated DECISIONS-SCREENING.md |
| 104 | 05:58:04 | doc_update | updated FAILURES.md |
| 105 | 05:58:04 | doc_update | updated STATE.md |
| 106 | 05:58:04 | session_end | E221 PSC NAICS sub-segment analysis completed on cached data. Extended E220 prototype to all 25 PSC codes using cached USAspending data. Analysis of 3 |

_56 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-22-006-declare-e221-session-artifacts/events.jsonl
```
