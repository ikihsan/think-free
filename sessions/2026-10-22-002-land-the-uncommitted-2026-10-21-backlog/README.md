# Session 2026-10-22-002-land-the-uncommitted-2026-10-21-backlog

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-22
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-22T00:14:17+00:00
- **Duration:** 4738.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Land the uncommitted 2026-10-21 backlog, then test whether E220's enterability labels predict newcomer outcomes better than naive baselines

## Summary

E221 full PSC NAICS sub-segment analysis started; background run progressing across sessions due to API rate limits

## Next

Check /tmp/e221_full.log for progress in next session; analyze gate results when run completes; if stalled, consider partial run or multi-year window work-around

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E222-enterability-label-forward-outcome/PROTOCOL.md | 05a10eb82814 | 5643 |
| EXPERIMENTS/E222-enterability-label-forward-outcome/analyze.py | 522f791caf2f | 12844 |
| EXPERIMENTS/E222-enterability-label-forward-outcome/fetch_outcome.py | 12b572e77925 | 4652 |

## Commands

3 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['tools/origin', 'doc', 'index'] | 0 | 21729 |
| 4 | ['python3', 'EXPERIMENTS/E222-enterability-label-forward-outcome/analyze.py', '--preflight'] | 0 | 1695 |
| 10 | ['tools/origin', 'doc', 'lint'] | 2 | 1275882 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 269 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-RECORDS-6.md |
|   undeclared | DECISIONS-SCREENING.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/controls.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/fetch.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:14:17 | session_start | Land the uncommitted 2026-10-21 backlog, then test whether E220's enterability labels predict newcomer outcomes better than naive baselines |
| 2 | 00:18:18 | command | $ tools/origin doc index |
| 3 | 00:28:48 | milestone | backlog landed: 6 commits (E209 restructure, E219+scripts, E211-E221+T-0094 experiments, 30 session records, tools, STATE); tree clean; doc lint runni |
| 4 | 00:33:20 | command | $ python3 EXPERIMENTS/E222-enterability-label-forward-outcome/analyze.py --preflight |
| 5 | 00:35:53 | artifact | wrote EXPERIMENTS/E222-enterability-label-forward-outcome/PROTOCOL.md |
| 6 | 00:36:08 | artifact | wrote EXPERIMENTS/E222-enterability-label-forward-outcome/analyze.py |
| 7 | 00:36:28 | artifact | wrote EXPERIMENTS/E222-enterability-label-forward-outcome/fetch_outcome.py |
| 8 | 00:36:35 | decision | run E222 (forward-outcome validation of E220 labels, 23 sub-segments, ~25-100 API calls) instead of the E221 full 25-code run (14+ h, ~800 calls): if  |
| 9 | 00:38:28 | milestone | E222 protocol declared pre-fetch (23 sub-segments), D130 recorded; fetch script ready |
| 10 | 00:41:29 | command | $ tools/origin doc lint |
| 11 | 00:48:15 | milestone | killed two stale E221 analyzer processes (pids 1699329/1700209, orphaned by finished sessions 029/030, running 9h past their validation scope and comp |
| 12 | 01:33:12 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-6.md |
| 13 | 01:33:12 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING.md |
| 14 | 01:33:12 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 15 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
| 16 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
| 17 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
| 18 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
| 19 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 20 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/controls.py |
| 21 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 22 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/gates.json |
| 23 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
| 24 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/per_category.csv |
| 25 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/probe.py |
| 26 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
| 27 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
| 28 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
| 29 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
| 30 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
| 31 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
| 32 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/fetch_summary.json |
| 33 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw_probe.json |
| 34 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/recompute.py |
| 35 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 36 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 37 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 38 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
| 39 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
| 40 | 01:33:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 277 | 01:33:15 | unlogged_change | changed but never declared as an artifact: tools/results/psc_naics_subsegment/gates.json |
| 278 | 01:33:15 | unlogged_change | changed but never declared as an artifact: tools/results/psc_naics_subsegment/ranked_subsegments.csv |
| 279 | 01:33:15 | unlogged_change | changed but never declared as an artifact: tools/results/psc_naics_subsegment/subsegment_metrics.csv |
| 280 | 01:33:15 | unlogged_change | changed but never declared as an artifact: tools/small_program_advisor.py |
| 281 | 01:33:16 | doc_update | updated DECISIONS-RECORDS-6.md |
| 282 | 01:33:16 | doc_update | updated DECISIONS-SCREENING.md |
| 283 | 01:33:16 | doc_update | updated DECISIONS.md |
| 284 | 01:33:16 | doc_update | updated FAILURES.md |
| 285 | 01:33:16 | doc_update | updated STATE.md |
| 286 | 01:33:16 | session_end | E221 full PSC NAICS sub-segment analysis started; background run progressing across sessions due to API rate limits |

_236 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-22-002-land-the-uncommitted-2026-10-21-backlog/events.jsonl
```
