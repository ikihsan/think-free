# Session 2026-10-21-027-fresh-observation-in-a-new-domain-axis-t

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T18:36:32+00:00
- **Duration:** 2006.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Fresh observation in a new domain axis: test accessibility pattern entry hypothesis on USPTO patent assignee data

## Summary

Ran E219: accessibility pattern entry test on World Bank project themes (new domain axis). Fetched 1,583 current-window (FY2020-2024) and 380 prior-window (FY2015-2019) single-theme projects via World Bank API. Measured segment newcomer fractions for 10 major themes using implementing agencies as identity. All 10 themes show extremely high newcomer fractions (94.5%-98.6%) regardless of concentration (top-5 share 12.5%-18.4%). Spearman ρ = -0.100, p = 0.770. G3 kill gate fired. The accessibility pattern's entry test has now failed in four market domains (NIH SBIR, Federal IT, International Trade, World Bank). Updated STATE.md and STATE-next-actions.md with E219 results.

## Next

Fresh observation in another completely new domain axis per D083, or prototype tool for enterable IT sub-segments (DA01, DA10, 7A21 from E209), or refined FDA recall hypothesis (Class I recall → product discontinuation via NDC linkage from E217).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E219-wb-theme-entrant-share/RESULT.md | b1f4229f9163 | 4893 |
| EXPERIMENTS/E219-wb-theme-entrant-share/raw_current.json | 891cf3ebf1d5 | 2877617 |
| EXPERIMENTS/E219-wb-theme-entrant-share/raw_prior.json | 729502c5f8de | 1978768 |
| STATE.md | 3c8b53520935 | 40137 |
| STATE-next-actions.md | ba13424ef8e9 | 33569 |
| run_e219.py | 7a51b95486ec | 5813 |
| fetch_wb.py | 3acea2d52c15 | 963 |
| fetch_wb2.py | b759527022c1 | 1101 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 85 |
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
| 1 | 18:36:32 | session_start | Fresh observation in a new domain axis: test accessibility pattern entry hypothesis on USPTO patent assignee data |
| 2 | 19:06:27 | artifact | wrote EXPERIMENTS/E219-wb-theme-entrant-share/RESULT.md |
| 3 | 19:06:39 | artifact | wrote EXPERIMENTS/E219-wb-theme-entrant-share/raw_current.json |
| 4 | 19:06:49 | artifact | wrote EXPERIMENTS/E219-wb-theme-entrant-share/raw_prior.json |
| 5 | 19:07:07 | artifact | wrote STATE.md |
| 6 | 19:07:15 | artifact | wrote STATE-next-actions.md |
| 7 | 19:07:26 | artifact | wrote run_e219.py |
| 8 | 19:07:35 | artifact | wrote fetch_wb.py |
| 9 | 19:07:37 | artifact | wrote fetch_wb2.py |
| 10 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
| 11 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
| 12 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
| 13 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
| 14 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 15 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/controls.py |
| 16 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 17 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/gates.json |
| 18 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
| 19 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/per_category.csv |
| 20 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/probe.py |
| 21 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
| 22 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
| 23 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
| 24 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
| 25 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
| 26 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
| 27 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/fetch_summary.json |
| 28 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw_probe.json |
| 29 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/recompute.py |
| 30 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 31 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 32 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 33 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
| 34 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
| 35 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 36 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/raw/analysis.json |
| 37 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
| 38 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/raw/analysis.json |
| 39 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/PROTOCOL.md |
| 40 | 19:09:57 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E215-comtrade-entrant-accessibility/RESULT.md |
| 87 | 19:09:58 | unlogged_change | changed but never declared as an artifact: tools/it_entrant_advisor.py |
| 88 | 19:09:58 | unlogged_change | changed but never declared as an artifact: tools/it_entrant_advisor_v3.py |
| 89 | 19:09:58 | unlogged_change | changed but never declared as an artifact: tools/nih_accessibility_prototype.py |
| 90 | 19:09:58 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_advisor_v3.py |
| 91 | 19:09:58 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_entry_advisor.py |
| 92 | 19:09:58 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_screener.py |
| 93 | 19:09:58 | unlogged_change | changed but never declared as an artifact: tools/small_program_advisor.py |
| 94 | 19:09:58 | unlogged_change | changed but never declared as an artifact: writing-plan-small-program-advisor.md |
| 95 | 19:09:58 | doc_update | updated STATE.md |
| 96 | 19:09:59 | session_end | Ran E219: accessibility pattern entry test on World Bank project themes (new domain axis). Fetched 1,583 current-window (FY2020-2024) and 380 prior-wi |

_46 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-027-fresh-observation-in-a-new-domain-axis-t/events.jsonl
```
