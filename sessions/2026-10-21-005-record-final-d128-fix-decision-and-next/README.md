# Session 2026-10-21-005-record-final-d128-fix-decision-and-next

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T09:30:13+00:00
- **Duration:** 30.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Record final D128 fix decision and next action - 3rd domain small-program accessibility

## Summary

D128 NIH SBIR prototype provenance fix: verified and committed. Key changes to tools/nih_accessibility_prototype.py and tools/nih_sbir_metrics.py: fetch_grants() now accepts activity_codes parameter (e.g. ['R41','R42'] for SBIR) and uses API meta.total as stopping condition instead of arbitrary 2000-row cap. This fixes provenance mismatch where IC-consensus recommendations rested on unfiltered 2000-row slice of 85,133 FY2023 projects instead of 368-grant SBIR census. E209 completed: median segment-newcomer fraction 0.2677 < 0.30 kill gate; three codes enterable (DA01/DA10/7A21 at 0.27-0.31), two closed shops (7030/D304 at 0.0); fragmentation positively correlates with entry (ρ=+0.6669, opposite sign from E208's -0.2456). Analysis verified against E207 census: category 101 reproduces E204 (147 grants, 134 orgs, top5 11.6%). E209: 'the uniform fragmented=>enterable reading is unsupported on federal IT codes too.' Single most useful next action: explore small-program accessibility in 3rd NIH SBIR spending category (category 176) using fixed prototype methodology, extending pattern from 2 to 3 domains and actualizing the D128 fix.

## Next

Implement 3rd domain small-program accessibility screen using fixed prototype

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 3 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
|   undeclared | sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
|   undeclared | sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:30:13 | session_start | Record final D128 fix decision and next action - 3rd domain small-program accessibility |
| 2 | 09:30:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 3 | 09:30:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 4 | 09:30:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl |
| 5 | 09:30:44 | session_end | D128 NIH SBIR prototype provenance fix: verified and committed. Key changes to tools/nih_accessibility_prototype.py and tools/nih_sbir_metrics.py: fet |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-005-record-final-d128-fix-decision-and-next/events.jsonl
```
