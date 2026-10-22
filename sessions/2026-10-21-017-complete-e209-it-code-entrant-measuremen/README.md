# Session 2026-10-21-017-complete-e209-it-code-entrant-measuremen

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T12:19:18+00:00
- **Duration:** 26.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Complete E209 IT code entrant measurement and declare artifacts

## Summary

E209 IT code entrant measurement completed successfully. Prototype tools/it_code_entrant_v2.py and tools/it_entrant_advisor.py measure segment newcomer fractions for 5 USAspending PSC codes using FY2023 current vs FY2018-2022 prior window comparison via the API's meta.total for complete census. Key finding: bimodal entry pattern unlike NIH SBIR's unimodal common-entry pattern. Federal IT shows 2 codes with significant sub-threshold entry (DA01: 0.2677, 7A21: 0.2912), 1 surviving the 0.30 kill gate (DA10: 0.3113), and 2 with 0 newcomers (7030, D304). This closes the 'fragmented ⇒ entry' inference transfer from NIH SBIR to federal IT. Experiment result recorded at EXPERIMENTS/E209-it-code-entrant/RESULT.md. Artifacts declared: tools/it_code_entrant_v2.py, tools/it_entrant_advisor.py, EXPERIMENTS/E209-it-code-entrant/RESULT.md. Next action: validate bimodal pattern robustness across additional PSC codes, or pursue fresh observation in new domain per D083.

## Next

validate bimodal pattern robustness or fresh observation per D083

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/it_code_entrant_v2.py | 5c0bbec2e70f | 10872 |
| tools/it_entrant_advisor.py | 32fc9af61baa | 12893 |
| EXPERIMENTS/E209-it-code-entrant/RESULT.md | ffe9b9df2f22 | 7367 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 30 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
|   undeclared | EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
|   undeclared | EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
|   undeclared | EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
|   undeclared | EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
|   undeclared | EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
|   undeclared | EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
|   undeclared | EXPERIMENTS/E213-nih-sbir-category701-subsegment/raw/analysis.json |
|   undeclared | EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
|   undeclared | EXPERIMENTS/E214-nih-sbir-category525-subsegment/raw/analysis.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:19:18 | session_start | Complete E209 IT code entrant measurement and declare artifacts |
| 2 | 12:19:28 | artifact | wrote tools/it_code_entrant_v2.py |
| 3 | 12:19:29 | artifact | wrote tools/it_entrant_advisor.py |
| 4 | 12:19:31 | artifact | wrote EXPERIMENTS/E209-it-code-entrant/RESULT.md |
| 5 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
| 6 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 7 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 8 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 9 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
| 10 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
| 11 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 12 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/raw/analysis.json |
| 13 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
| 14 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/raw/analysis.json |
| 15 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/PROTOCOL.md |
| 16 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/RESULT.md |
| 17 | 12:19:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/analysis.json |
| 18 | 12:19:43 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 19 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 20 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 21 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 22 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 23 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
| 24 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
| 25 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |
| 26 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-008-build-and-verify-e209-inspired-it-code-e/events.jsonl |
| 27 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-009-investigate-e209-bimodality-and-determin/events.jsonl |
| 28 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-010-build-e209-prototype-screen-for-federal/events.jsonl |
| 29 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-011-record-e211-nih-sbir-sub-area-accessibil/events.jsonl |
| 30 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-012-run-e212-experiment-nih-sbir-category-10/events.jsonl |
| 31 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-013-declare-e212-artifacts-and-verify-sessio/events.jsonl |
| 32 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-014-finalize-mission-documentation-and-evide/events.jsonl |
| 33 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-015-complete-t-0094-view-count-principle-tie/events.jsonl |
| 34 | 12:19:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-016-complete-e209-it-code-entrant-measuremen/events.jsonl |
| 35 | 12:19:44 | session_end | E209 IT code entrant measurement completed successfully. Prototype tools/it_code_entrant_v2.py and tools/it_entrant_advisor.py measure segment newcome |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-017-complete-e209-it-code-entrant-measuremen/events.jsonl
```
