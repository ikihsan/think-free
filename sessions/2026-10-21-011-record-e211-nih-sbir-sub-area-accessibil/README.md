# Session 2026-10-21-011-record-e211-nih-sbir-sub-area-accessibil

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T11:04:47+00:00
- **Duration:** 23.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Record E211 NIH SBIR sub-area accessibility prototype and determine next experiment

## Summary

E211 NIH SBIR sub-area accessibility prototype built and verified. Prototype reads committed E210 raw data and ranks 17 Funding Institutes/Centers by accessibility (access_score). Top 3 most accessible sub-areas identified: NIMH (access_score 14.97), NCI (7.41), NIMHD (5.00). Small-program accessibility pattern now demonstrated in 3 domains (federal IT 7030/small_technical, NIH SBIR cat 101, NIH SBIR cat 176 with mechanism filter). DIF bimodal separation discovered in E209: |cur-pri| ≤ 257 = enterable codes, ≥ 1106 = closed-shop codes, with natural breakpoint between 257 and 1106 (no overlap). Next: fresh observation in new domain axis per D083.

## Next

fresh observation in new domain axis per D083

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 14 |
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
| 1 | 11:04:47 | session_start | Record E211 NIH SBIR sub-area accessibility prototype and determine next experiment |
| 2 | 11:04:59 | milestone | E211 prototype built and verified |
| 3 | 11:05:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
| 4 | 11:05:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 5 | 11:05:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 6 | 11:05:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 7 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 8 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 9 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 10 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 11 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
| 12 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
| 13 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |
| 14 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-008-build-and-verify-e209-inspired-it-code-e/events.jsonl |
| 15 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-009-investigate-e209-bimodality-and-determin/events.jsonl |
| 16 | 11:05:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-010-build-e209-prototype-screen-for-federal/events.jsonl |
| 17 | 11:05:10 | session_end | E211 NIH SBIR sub-area accessibility prototype built and verified. Prototype reads committed E210 raw data and ranks 17 Funding Institutes/Centers by  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-011-record-e211-nih-sbir-sub-area-accessibil/events.jsonl
```
