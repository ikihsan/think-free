# Session 2026-10-21-009-investigate-e209-bimodality-and-determin

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T10:26:25+00:00
- **Duration:** 45.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Investigate E209 bimodality and determine next action

## Summary

E209 bimodality investigation complete - identified turnover balance DIF as key distinguisher between enterable and closed-shop PSC codes. Kill gate fired (median 0.2677 < 0.30), but bimodal structure revealed: 3 codes enterable (DA01, DA10, 7A21, 0.27-0.31 newcomer fraction), 2 codes closed shops (7030, D304, 0.0 newcomer fraction). Critical distinguishing metric: DIF = | |cur-pri| - |pri-cur| | measures balanced turnover vs exit-only dynamics. Enterable codes have DIF 14-257 (balanced entry/exit); closed-shop codes have DIF 1106-4924 (exit-only, zero entry). View-count principle domain mapping complete across 8 domains. Small-program accessibility entry test failed in 2 domains (E208 NIH SBIR, E209 federal IT).

## Next

explore fresh observation in new domain/axis

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 9 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
|   undeclared | sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
|   undeclared | sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
|   undeclared | sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
|   undeclared | sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
|   undeclared | sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |
|   undeclared | sessions/2026-10-21-008-build-and-verify-e209-inspired-it-code-e/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:26:25 | session_start | Investigate E209 bimodality and determine next action |
| 2 | 10:26:52 | milestone | Completed E209 bimodality investigation - identified turnover balance DIF as key distinguisher between enterable and closed-shop PSC codes |
| 3 | 10:27:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/INVESTIGATION.md |
| 4 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 5 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 6 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 7 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 8 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
| 9 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
| 10 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |
| 11 | 10:27:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-008-build-and-verify-e209-inspired-it-code-e/events.jsonl |
| 12 | 10:27:10 | session_end | E209 bimodality investigation complete - identified turnover balance DIF as key distinguisher between enterable and closed-shop PSC codes. Kill gate f |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-009-investigate-e209-bimodality-and-determin/events.jsonl
```
