# Session 2026-10-17-006-complete-the-evid-class-picture-via-cros

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-17
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-17T09:16:14+00:00
- **Duration:** 5503.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Complete the EVID class picture via cross-tab analysis, record the exploratory finding, and pivot to fresh exploration in a new domain

## Summary

Cross-tab (F137) closed the automated-ask route: round trip fails uniformly across buckets, unserved residue 7/30 all eventually answered. Money SE fresh observation (F138): round trip is 0.9000 on money SE vs 0.6739 on SO — stronger, not weaker, when missing facts are personal. EVID line closed on two venues. SE API sort parameter bug (sort=views invalid) diagnosed and fixed.

## Next

Return to fresh exploration; EVID class is served by the venue's round trip across two venues

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/178-evidence-where-does-it-live/RESULT.md | 57117ee3f33a | 8610 |
| FAILURES-findings-43.md | 1bf568272223 | 14835 |

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
|   undeclared | STATE-next-actions.md |
|   undeclared | sessions/2026-10-17-005-e178-for-the-46-evidence-gated-rows-of-e/commands.log |
|   undeclared | sessions/2026-10-17-005-e178-for-the-46-evidence-gated-rows-of-e/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:16:14 | session_start | Complete the EVID class picture via cross-tab analysis, record the exploratory finding, and pivot to fresh exploration in a new domain |
| 2 | 09:20:13 | milestone | F137 recorded: cross-tab shows round trip fails uniformly (15/46), unserved residue 7/30 all eventually answered — automated-ask route closed |
| 3 | 09:24:04 | artifact | wrote EXPERIMENTS/178-evidence-where-does-it-live/RESULT.md |
| 4 | 09:24:05 | artifact | wrote FAILURES-findings-43.md |
| 5 | 09:33:43 | milestone | API flaky (1015 request_denied). Cross-tab + SELF-failure analysis done locally. Pivoting to local-data exploration and GitHub API check |
| 6 | 10:12:23 | milestone | SE API confirmed working (earlier failures were invalid sort=votes + transient 1015). Cross-tab F137 recorded. SELF-failure analysis: 4 misses heterog |
| 7 | 10:47:57 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 8 | 10:47:57 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-005-e178-for-the-46-evidence-gated-rows-of-e/commands.log |
| 9 | 10:47:57 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-005-e178-for-the-46-evidence-gated-rows-of-e/events.jsonl |
| 10 | 10:47:57 | session_end | Cross-tab (F137) closed the automated-ask route: round trip fails uniformly across buckets, unserved residue 7/30 all eventually answered. Money SE fr |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-17-006-complete-the-evid-class-picture-via-cros/events.jsonl
```
