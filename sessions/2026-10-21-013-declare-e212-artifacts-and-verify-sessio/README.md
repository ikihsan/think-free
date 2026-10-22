# Session 2026-10-21-013-declare-e212-artifacts-and-verify-sessio

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T11:31:25+00:00
- **Duration:** 29.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Declare E212 artifacts and verify session integrity

## Summary

E212 experiment: NIH SBIR category 108 sub-segment screen with DIF bimodal analysis. Key results: 76 R41/R42 grants across 19 ICs; all ICs classified as enterable (access_score ≤ 257); top 3 accessible: NIAID (130.81), NCI (48.40), NHLBI (12.16). STATE-next-actions.md updated with E212 results. Cross-category comparison confirms mechanism-dependent accessibility reversal.

## Next

Design follow-up experiment on remaining NIH SBIR consensus categories or fresh observation in new domain axis per D083

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py | ebb6e768957b | 13443 |
| EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json | 4ffbd3a73691 | 4904 |
| STATE-next-actions.md | d14ee754e699 | 15116 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 16 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
|   undeclared | EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
|   undeclared | EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
|   undeclared | EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
|   undeclared | sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
|   undeclared | sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
|   undeclared | sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
|   undeclared | sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:31:25 | session_start | Declare E212 artifacts and verify session integrity |
| 2 | 11:31:36 | artifact | wrote EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
| 3 | 11:31:38 | artifact | wrote EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
| 4 | 11:31:40 | artifact | wrote STATE-next-actions.md |
| 5 | 11:31:54 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
| 6 | 11:31:54 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 7 | 11:31:54 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 8 | 11:31:54 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 9 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 10 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 11 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 12 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 13 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
| 14 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
| 15 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |
| 16 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-008-build-and-verify-e209-inspired-it-code-e/events.jsonl |
| 17 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-009-investigate-e209-bimodality-and-determin/events.jsonl |
| 18 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-010-build-e209-prototype-screen-for-federal/events.jsonl |
| 19 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-011-record-e211-nih-sbir-sub-area-accessibil/events.jsonl |
| 20 | 11:31:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-012-run-e212-experiment-nih-sbir-category-10/events.jsonl |
| 21 | 11:31:54 | session_end | E212 experiment: NIH SBIR category 108 sub-segment screen with DIF bimodal analysis. Key results: 76 R41/R42 grants across 19 ICs; all ICs classified  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-013-declare-e212-artifacts-and-verify-sessio/events.jsonl
```
