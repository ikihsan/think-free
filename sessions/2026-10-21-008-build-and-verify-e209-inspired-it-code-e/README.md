# Session 2026-10-21-008-build-and-verify-e209-inspired-it-code-e

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T10:17:26+00:00
- **Duration:** 13.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Build and verify E209-inspired IT code entrant measurement prototype

## Summary

Built and verified E209-inspired IT code entrant measurement prototype. Prototype tool tools/it_code_entrant.py queries USAspending API for PSC code recipient data and computes segment newcomer fractions, fragmentation, and obligation metrics. Verified against committed E209 results: all 5 codes match exactly (DA01: 0.2677, DA10: 0.3113, 7A21: 0.2912, 7030: 0.0, D304: 0.0), G3 kill gate fires (median 0.2677 < 0.30), bimodality pattern confirmed (3 codes ~0.27-0.31 enterable, 2 codes closed shops at 0.0). Build decision: committed prototype tool enabling reusable entrant fraction measurement across PSC codes, replacing ad-hoc experiment scripts. Raw evidence preserved in git commit 928fc489. Unknown: why 3 codes are borderline-enterable (~0.27-0.31) while 2 have exactly 0.0 newcomer fraction, and what code characteristics distinguish them. Most useful next action: refine enterable-market screen using measured entrant fractions rather than fragmentation, or apply measurement to NIH SBIR spending categories.

## Next

Refine enterable-market screen using measured entrant fractions rather than fragmentation, or apply measurement to NIH SBIR spending categories

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
|   undeclared | sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
|   undeclared | sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
|   undeclared | sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
|   undeclared | sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
|   undeclared | sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:17:26 | session_start | Build and verify E209-inspired IT code entrant measurement prototype |
| 2 | 10:17:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 3 | 10:17:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 4 | 10:17:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 5 | 10:17:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 6 | 10:17:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
| 7 | 10:17:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/commands.log |
| 8 | 10:17:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl |
| 9 | 10:17:40 | session_end | Built and verified E209-inspired IT code entrant measurement prototype. Prototype tool tools/it_code_entrant.py queries USAspending API for PSC code r |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-008-build-and-verify-e209-inspired-it-code-e/events.jsonl
```
