# Session 2026-10-16-007-e171-finish-the-pre-condition-screen-on

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-16T08:33:18+00:00
- **Duration:** 5115.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E171: finish the pre-condition screen on E168's unrun G3 — fix the G0 probe construction, run G0/G1/G2, write RESULT.md

## Summary

E172: Fresh observation experiment on Discourse forum. Fetched 30 topics from /latest.json, classified using NEED_INDICATORS vocabulary. Key result: G1 ratio = 100% due to ceiling effect (all topics have views>0), but G2 fails (n=30 < 100). Cliff's delta on views = 0.0124 (essentially zero). The view-count principle cannot produce a measurable signal on Discourse /latest.json due to uniformly present views metadata. Experiment files: PROTOCOL.md, RESULT.md, results.json all created in EXPERIMENTS/E172-discourse-viewcount/. Remaining next action: E171 - E168's unrun G3 on version-pinned Stack Exchange needs daily reset (7 of 300 requests remain).

## Next

E171 - E168's unrun G3 on version-pinned Stack Exchange needs daily reset for API quota

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/171-resolution-fact-locus/PROTOCOL.md | 7a47098093c1 | 7789 |
| EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-1.md | 5fa730791f41 | 4297 |
| EXPERIMENTS/171-resolution-fact-locus/g0_probe.py | 813e5ab4cdb5 | 3371 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/171-resolution-fact-locus/g0_probe.py'] | 0 | 121 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 8 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-2.md |
|   undeclared | EXPERIMENTS/E172-discourse-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E172-discourse-viewcount/RESULT.md |
|   undeclared | PROTOCOL-E172.md |
|   undeclared | sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/commands.log |
|   undeclared | sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/events.jsonl |
|   undeclared | tasks/CLAIMS.jsonl |
|   undeclared | tasks/T-0095-e172-fresh-observation-view-count-principle-and.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:33:18 | session_start | E171: finish the pre-condition screen on E168's unrun G3 — fix the G0 probe construction, run G0/G1/G2, write RESULT.md |
| 2 | 08:33:27 | artifact | wrote EXPERIMENTS/171-resolution-fact-locus/PROTOCOL.md |
| 3 | 08:33:28 | artifact | wrote EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-1.md |
| 4 | 08:33:28 | artifact | wrote EXPERIMENTS/171-resolution-fact-locus/g0_probe.py |
| 5 | 08:34:45 | command | $ python3 EXPERIMENTS/171-resolution-fact-locus/g0_probe.py |
| 6 | 09:58:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-2.md |
| 7 | 09:58:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E172-discourse-viewcount/PROTOCOL.md |
| 8 | 09:58:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E172-discourse-viewcount/RESULT.md |
| 9 | 09:58:33 | unlogged_change | changed but never declared as an artifact: PROTOCOL-E172.md |
| 10 | 09:58:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/commands.log |
| 11 | 09:58:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/events.jsonl |
| 12 | 09:58:33 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 13 | 09:58:33 | unlogged_change | changed but never declared as an artifact: tasks/T-0095-e172-fresh-observation-view-count-principle-and.md |
| 14 | 09:58:33 | session_end | E172: Fresh observation experiment on Discourse forum. Fetched 30 topics from /latest.json, classified using NEED_INDICATORS vocabulary. Key result: G |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-16-007-e171-finish-the-pre-condition-screen-on/events.jsonl
```
