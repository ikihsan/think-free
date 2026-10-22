# Session 2026-10-21-010-build-e209-prototype-screen-for-federal

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T10:44:09+00:00
- **Duration:** 25.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Build E209 prototype screen for federal IT PSC code entrant classification and determine pattern generalizability

## Summary

E209 prototype screen completed and verified against committed E209 raw data. Prototype classifies 5 federal IT PSC codes: 3 enterable (DA01, DA10, 7A21) with active newcomer entry and balanced turnover, 2 closed shops (7030, D304) with zero newcomers and exit-only dynamics. Key finding: DIF (turnover balance) distinguishes enterable from closed-shop codes, not fragmentation. Bimodal pattern confirmed. Next: extend entrant measurement to additional PSC codes to test generalizability of the bimodal pattern.

## Next

Extend E209 entrant measurement to additional PSC codes to test whether the bimodal pattern generalizes beyond the top 5 codes

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
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
|   undeclared | SESSION_SUMMARY.md |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
|   undeclared | sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
|   undeclared | sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
|   undeclared | sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:44:09 | session_start | Build E209 prototype screen for federal IT PSC code entrant classification and determine pattern generalizability |
| 2 | 10:44:20 | milestone | E209 prototype screen completed and verified |
| 3 | 10:44:35 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
| 4 | 10:44:35 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
| 5 | 10:44:35 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
| 6 | 10:44:35 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
| 7 | 10:44:35 | unlogged_change | changed but never declared as an artifact: SESSION_SUMMARY.md |
| 8 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 9 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 10 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 11 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 12 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
| 13 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
| 14 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |
| 15 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-008-build-and-verify-e209-inspired-it-code-e/events.jsonl |
| 16 | 10:44:35 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-009-investigate-e209-bimodality-and-determin/events.jsonl |
| 17 | 10:44:35 | session_end | E209 prototype screen completed and verified against committed E209 raw data. Prototype classifies 5 federal IT PSC codes: 3 enterable (DA01, DA10, 7A |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-010-build-e209-prototype-screen-for-federal/events.jsonl
```
