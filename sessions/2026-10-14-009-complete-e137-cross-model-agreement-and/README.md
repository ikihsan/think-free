# Session 2026-10-14-009-complete-e137-cross-model-agreement-and

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T08:39:05+00:00
- **Duration:** 17.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Complete E137 cross-model agreement and verify preflight package

## Summary

E137 completed: cross-model agreement on math_chain_of_thought for model 01-ai_yi-6b (published aggregate 0.12585197340399298 vs recomputed 0.1275131029720993, diff 0.00166, AGREE). 437 rows, 56 hits, 95 no-\boxed completions. Preflight package verified (25/25 tests pass). D111 standing: external value unobserved, preflight fires on 4/6 committed harnesses (E124). Updated e137_math_yi6b_result.json with published value comparison. Preflight on real committed harnesses: fired on 4/6, harness gates green on all. K2 FP rate gate premise wrong (arm-specific per F123/D109). C3 consistently finds control arm contamination (F122).

## Next

Attempt preflight on new evaluation harness to advance D111. If suitable harness with committed key/output pairs available, run python -m preflight <file> and document check results (C1 concordance, C2 alternate-form FP, C3 control arm). If no suitable harness immediately available, document current state: preflight verified on 6 formats, 25 tests pass; on 6 committed harnesses (E124): fired on 4/6, harness gates green on all; K2 FP rate gate premise wrong (arm-specific, not transferable per F123/D109); C3 consistently finds control arm contamination (F122); D111 stands as protocol's stated outcome unless external value observed on new harness. Continue preflight line with adapter pattern validated across 6 formats (3-4 lines stdlib Python per format), and R1 instrument calibrated across models (E135/E136/E137 all AGREE).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json | 2ecf002c91a7 | 1263 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 4 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/collect.py |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/results.json |
|   undeclared | SYNTHESIS_VIEW_COUNT_RUBYGEMS.md |
|   undeclared | session-summary-E138.txt |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:39:05 | session_start | Complete E137 cross-model agreement and verify preflight package |
| 2 | 08:39:12 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 3 | 08:39:22 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 4 | 08:39:22 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/results.json |
| 5 | 08:39:22 | unlogged_change | changed but never declared as an artifact: SYNTHESIS_VIEW_COUNT_RUBYGEMS.md |
| 6 | 08:39:22 | unlogged_change | changed but never declared as an artifact: session-summary-E138.txt |
| 7 | 08:39:23 | session_end | E137 completed: cross-model agreement on math_chain_of_thought for model 01-ai_yi-6b (published aggregate 0.12585197340399298 vs recomputed 0.12751310 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-009-complete-e137-cross-model-agreement-and/events.jsonl
```
