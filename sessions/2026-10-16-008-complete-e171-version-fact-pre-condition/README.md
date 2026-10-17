# Session 2026-10-16-008-complete-e171-version-fact-pre-condition

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-16T17:31:06+00:00
- **Duration:** 74.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Complete E171 version_fact pre-condition screen for E168's G3 experiment

## Summary

E171 experiment completed: version_fact pre-condition screen for E168's G3. G1 FAILED (2/13=0.1538<0.40), withdrawing E168's G3. Version-pinned line closes as served-by-thread with measured reason. Experiment reused existing E168/E169 data, no new Stack Exchange quota consumed. G0 PASSED (10/10 probe). G2: 4/11=0.3636. RESULT.md documents classification of 24 rows into 6 mutually exclusive classes. AMENDMENT 1 fixed 'accepted answer has no referent' defect; AMENDMENT 2 fixed probe construction (was 10/10 version_fact, repaired to 5+5 split).

## Next

E172 discourse view-count already complete; consider fresh observation in untouched domain per STATE-next-actions.md or continue with E171's recorded next action

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/171-resolution-fact-locus/RESULT.md | 3b235dc25885 | 3725 |
| EXPERIMENTS/171-resolution-fact-locus/PROTOCOL.md | 7a47098093c1 | 7789 |
| EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-1.md | 5fa730791f41 | 4297 |
| EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-2.md | ae6def035149 | 2644 |

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
|   undeclared | CLASSIFICATION-PROTOTYPE.md |
|   undeclared | EXPERIMENTS/171-resolution-fact-locus/g0_probe.py |
|   undeclared | EXPERIMENTS/E172-discourse-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E172-discourse-viewcount/RESULT.md |
|   undeclared | EXPERIMENTS/E173-github-discussions-viewcount/PROTOCOL-E173.md |
|   undeclared | EXPERIMENTS/E173-github-discussions-viewcount/RESULT.md |
|   undeclared | PROTOCOL-E172.md |
|   undeclared | SESSION_OUTCOME.json |
|   undeclared | sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/commands.log |
|   undeclared | sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:31:06 | session_start | Complete E171 version_fact pre-condition screen for E168's G3 experiment |
| 2 | 17:31:27 | artifact | wrote EXPERIMENTS/171-resolution-fact-locus/RESULT.md |
| 3 | 17:31:59 | artifact | wrote EXPERIMENTS/171-resolution-fact-locus/PROTOCOL.md |
| 4 | 17:32:00 | artifact | wrote EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-1.md |
| 5 | 17:32:01 | artifact | wrote EXPERIMENTS/171-resolution-fact-locus/PROTOCOL-AMENDMENT-2.md |
| 6 | 17:32:20 | unlogged_change | changed but never declared as an artifact: CLASSIFICATION-PROTOTYPE.md |
| 7 | 17:32:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/171-resolution-fact-locus/g0_probe.py |
| 8 | 17:32:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E172-discourse-viewcount/PROTOCOL.md |
| 9 | 17:32:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E172-discourse-viewcount/RESULT.md |
| 10 | 17:32:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E173-github-discussions-viewcount/PROTOCOL-E173.md |
| 11 | 17:32:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E173-github-discussions-viewcount/RESULT.md |
| 12 | 17:32:20 | unlogged_change | changed but never declared as an artifact: PROTOCOL-E172.md |
| 13 | 17:32:20 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.json |
| 14 | 17:32:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/commands.log |
| 15 | 17:32:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/events.jsonl |
| 16 | 17:32:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-16-007-e171-finish-the-pre-condition-screen-on/commands.log |
| 17 | 17:32:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-16-007-e171-finish-the-pre-condition-screen-on/events.jsonl |
| 18 | 17:32:20 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 19 | 17:32:20 | unlogged_change | changed but never declared as an artifact: tasks/T-0095-e172-fresh-observation-view-count-principle-and.md |
| 20 | 17:32:20 | unlogged_change | changed but never declared as an artifact: test_prototype.py |
| 21 | 17:32:20 | unlogged_change | changed but never declared as an artifact: tools/viewcount_framework.py |
| 22 | 17:32:21 | session_end | E171 experiment completed: version_fact pre-condition screen for E168's G3. G1 FAILED (2/13=0.1538<0.40), withdrawing E168's G3. Version-pinned line c |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-16-008-complete-e171-version-fact-pre-condition/events.jsonl
```
