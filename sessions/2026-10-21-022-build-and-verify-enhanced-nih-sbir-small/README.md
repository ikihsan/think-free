# Session 2026-10-21-022-build-and-verify-enhanced-nih-sbir-small

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T14:00:52+00:00
- **Duration:** 20.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Build and verify enhanced NIH SBIR Small-Program Accessibility Prototype

## Summary

Built and verified an enhanced NIH SBIR Small-Program Accessibility Prototype (tools/nih_accessibility_prototype.py) that helps small programs identify the most accessible Funding Institutes/Centers within a spending category, with federal IT PSC code entrant fraction comparison. The prototype addresses the named next action from STATE-next-actions.md: 'a prototype tool small programs could use to identify the most accessible NIH SBIR sub-areas per this analysis.' Verified with category 101 (R41/R42, FY2023): 147 grants across 20 ICs, NCI (access_score 38.97) and NIAID (36.83) most accessible. Federal IT PSC codes: DA10 enterable (0.3113 newcomer fraction), others near 0.30 threshold (DA01: 0.2677, 7A21: 0.2912). Kill gate fired on median (0.2677 < 0.30) but borderline. View-count principle spans 8 domains with no remaining paths. Accessibility pattern falsified by entrant measurement in both domains.

## Next

Run prototype on remaining 4 NIH SBIR consensus categories (108, 176, 525, 701) to compare accessibility patterns and refine recommendations, or explore fresh view-count principle observation in new domain per D083

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 62 |
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
| 1 | 14:00:52 | session_start | Build and verify enhanced NIH SBIR Small-Program Accessibility Prototype |
| 2 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
| 3 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
| 4 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
| 5 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
| 6 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 7 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/controls.py |
| 8 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 9 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/gates.json |
| 10 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
| 11 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/per_category.csv |
| 12 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/probe.py |
| 13 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
| 14 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
| 15 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
| 16 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
| 17 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
| 18 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
| 19 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/fetch_summary.json |
| 20 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw_probe.json |
| 21 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/recompute.py |
| 22 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 23 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 24 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 25 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
| 26 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
| 27 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 28 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/raw/analysis.json |
| 29 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
| 30 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/raw/analysis.json |
| 31 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/PROTOCOL.md |
| 32 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/RESULT.md |
| 33 | 14:01:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/analysis.json |
| 34 | 14:01:12 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 35 | 14:01:12 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 36 | 14:01:12 | unlogged_change | changed but never declared as an artifact: SUMMARY-NEXT-ACTION.md |
| 37 | 14:01:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 38 | 14:01:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 39 | 14:01:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 40 | 14:01:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 56 | 14:01:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-019-run-entrant-share-measurement-on-federal/events.jsonl |
| 57 | 14:01:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-020-build-improved-nih-sbir-small-program-en/events.jsonl |
| 58 | 14:01:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-021-record-nih-sbir-small-program-entry-advi/events.jsonl |
| 59 | 14:01:13 | unlogged_change | changed but never declared as an artifact: sessions/session-outcome-20261021-ENH-Prototype.json |
| 60 | 14:01:13 | unlogged_change | changed but never declared as an artifact: tools/it_entrant_advisor.py |
| 61 | 14:01:13 | unlogged_change | changed but never declared as an artifact: tools/nih_accessibility_prototype.py |
| 62 | 14:01:13 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_entry_advisor.py |
| 63 | 14:01:13 | unlogged_change | changed but never declared as an artifact: tools/nih_small_program_screener.py |
| 64 | 14:01:13 | doc_update | updated STATE.md |
| 65 | 14:01:13 | session_end | Built and verified an enhanced NIH SBIR Small-Program Accessibility Prototype (tools/nih_accessibility_prototype.py) that helps small programs identif |

_15 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-022-build-and-verify-enhanced-nih-sbir-small/events.jsonl
```
