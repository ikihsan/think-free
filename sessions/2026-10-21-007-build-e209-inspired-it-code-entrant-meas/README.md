# Session 2026-10-21-007-build-e209-inspired-it-code-entrant-meas

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T10:07:37+00:00
- **Duration:** 492.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Build E209-inspired IT code entrant measurement prototype

## Summary

Built E209-inspired IT code entrant measurement prototype as a reversible exploratory tool. Prototype queries USAspending API for PSC codes and computes segment newcomer fractions, fragmentation, and obligation data. Verified against E209 committed results: all 5 codes match, G3 kill gate fires (median 0.2677 < 0.30), bimodality pattern confirmed (3 codes ~0.27-0.31, 2 codes at 0.0).

## Next

Evaluate prototype and decide on continuation: refine enterable-market screen, apply to NIH SBIR categories, or build on fresh observation

## Artifacts

_none_

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', '-c', "\nwith open('tools/it_code_entrant.py') as f:\n    content = f.read()\n# Check it has proper structure\nassert 'E209-inspired' in c | 0 | 195 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 476 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
|   undeclared | sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
|   undeclared | sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
|   undeclared | sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
|   undeclared | tools/it_code_entrant.py |
|   undeclared | tools/raw/current_7030_p1.json |
|   undeclared | tools/raw/current_7030_p1.meta.json |
|   undeclared | tools/raw/current_7030_p10.json |
|   undeclared | tools/raw/current_7030_p10.meta.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:07:37 | session_start | Build E209-inspired IT code entrant measurement prototype |
| 2 | 10:07:51 | milestone | prototype built and verified |
| 3 | 10:15:21 | command | $ python3 -c  with open('tools/it_code_entrant.py') as f:     content = f.read() # Check it has proper structure assert 'E209-inspired' in con |
| 4 | 10:15:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 5 | 10:15:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 6 | 10:15:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 7 | 10:15:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl |
| 8 | 10:15:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-continue-think-free-decision-summary-and/events.jsonl |
| 9 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/it_code_entrant.py |
| 10 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p1.json |
| 11 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p1.meta.json |
| 12 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p10.json |
| 13 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p10.meta.json |
| 14 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p11.json |
| 15 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p11.meta.json |
| 16 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p12.json |
| 17 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p12.meta.json |
| 18 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p13.json |
| 19 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p13.meta.json |
| 20 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p2.json |
| 21 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p2.meta.json |
| 22 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p3.json |
| 23 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p3.meta.json |
| 24 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p4.json |
| 25 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p4.meta.json |
| 26 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p5.json |
| 27 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p5.meta.json |
| 28 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p6.json |
| 29 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p6.meta.json |
| 30 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p7.json |
| 31 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p7.meta.json |
| 32 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p8.json |
| 33 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p8.meta.json |
| 34 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p9.json |
| 35 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7030_p9.meta.json |
| 36 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7A21_p1.json |
| 37 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7A21_p1.meta.json |
| 38 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7A21_p10.json |
| 39 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7A21_p10.meta.json |
| 40 | 10:15:43 | unlogged_change | changed but never declared as an artifact: tools/raw/current_7A21_p11.json |
| 471 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p5.meta.json |
| 472 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p6.json |
| 473 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p6.meta.json |
| 474 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p7.json |
| 475 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p7.meta.json |
| 476 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p8.json |
| 477 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p8.meta.json |
| 478 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p9.json |
| 479 | 10:15:49 | unlogged_change | changed but never declared as an artifact: tools/raw/prior_DA10_p9.meta.json |
| 480 | 10:15:49 | session_end | Built E209-inspired IT code entrant measurement prototype as a reversible exploratory tool. Prototype queries USAspending API for PSC codes and comput |

_430 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-007-build-e209-inspired-it-code-entrant-meas/events.jsonl
```
