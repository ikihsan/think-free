# Session 2026-10-22-010-analyze-psc-naics-sub-segment-enterabili

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-22
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-22T08:31:03+00:00
- **Duration:** 47.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Analyze PSC NAICS sub-segment enterability from cached data and design fresh observation experiment

## Summary

Analyzed PSC NAICS sub-segment enterability from cached USAspending data; validated E221 prototype on 5 IT PSC codes (36 sub-segments from 25 PSC codes); confirmed key enterable sub-segments (541511, 541519 consistently enterable across IT codes; R425/541330 enterable); conducted fresh observation on 3 new PSC codes (all CLOSED, providing D083 evidence); multi-year window framework in code but no new data with current cache; all 5 gates pass on cached data. Total: 36 sub-segments analyzed, 11 HIGHLY ENTERABLE, 20 CLOSED, 5 MARGINAL. Fresh evidence: 3 new PSC codes analyzed with CLOSED classifications.

## Next

Continue fresh observation in new domain per D083, or run full 25-PSC-code API analysis on E221 tool

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 98 |
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
| 1 | 08:31:03 | session_start | Analyze PSC NAICS sub-segment enterability from cached data and design fresh observation experiment |
| 2 | 08:31:17 | milestone | Fresh observation experiment completed |
| 3 | 08:31:50 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-6.md |
| 4 | 08:31:50 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING.md |
| 5 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 6 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 7 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
| 8 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/PROTOCOL.md |
| 9 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/RESULT.md |
| 10 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/PLAN-it-advisor-enhancement.md |
| 11 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/PLAN.md |
| 12 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/PROTOCOL.md |
| 13 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E216-small-program-advisor/RESULT.md |
| 14 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E218-openalex-topic-entrant-share/PROTOCOL.md |
| 15 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E218-openalex-topic-entrant-share/RESULT.md |
| 16 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E218-openalex-topic-entrant-share/run_experiment.py |
| 17 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E219-wb-theme-entrant-share/RESULT.md |
| 18 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E220-it-subsegment-entrant-advisor/PROTOCOL.md |
| 19 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E220-it-subsegment-entrant-advisor/RESULT.md |
| 20 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/analyze.py |
| 21 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/fetch_outcome.py |
| 22 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_334111_2024.json |
| 23 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_334111_2024.meta.json |
| 24 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_511210_2024.json |
| 25 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_511210_2024.meta.json |
| 26 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_513210_2024.json |
| 27 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_513210_2024.meta.json |
| 28 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_518210_2024.json |
| 29 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_518210_2024.meta.json |
| 30 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541330_2024.json |
| 31 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541330_2024.meta.json |
| 32 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541511_2024.json |
| 33 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541511_2024.meta.json |
| 34 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541512_2024.json |
| 35 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541512_2024.meta.json |
| 36 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541519_2024.json |
| 37 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_7A21_541519_2024.meta.json |
| 38 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_DA01_511210_2024.json |
| 39 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_DA01_511210_2024.meta.json |
| 40 | 08:31:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E222-enterability-label-forward-outcome/raw/recipients_DA01_518210_2024.json |
| 96 | 08:31:50 | unlogged_change | changed but never declared as an artifact: tools/results/psc_naics_subsegment/ranked_subsegments.csv |
| 97 | 08:31:50 | unlogged_change | changed but never declared as an artifact: tools/results/psc_naics_subsegment/subsegment_metrics.csv |
| 98 | 08:31:50 | unlogged_change | changed but never declared as an artifact: tools/results/test_single_year/gates.json |
| 99 | 08:31:50 | unlogged_change | changed but never declared as an artifact: tools/results/test_single_year/ranked_subsegments.csv |
| 100 | 08:31:50 | unlogged_change | changed but never declared as an artifact: tools/results/test_single_year/subsegment_metrics.csv |
| 101 | 08:31:50 | doc_update | updated DECISIONS-RECORDS-6.md |
| 102 | 08:31:50 | doc_update | updated DECISIONS-SCREENING.md |
| 103 | 08:31:50 | doc_update | updated FAILURES.md |
| 104 | 08:31:50 | doc_update | updated STATE.md |
| 105 | 08:31:50 | session_end | Analyzed PSC NAICS sub-segment enterability from cached USAspending data; validated E221 prototype on 5 IT PSC codes (36 sub-segments from 25 PSC code |

_55 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-22-010-analyze-psc-naics-sub-segment-enterabili/events.jsonl
```
