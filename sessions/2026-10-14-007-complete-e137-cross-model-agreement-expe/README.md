# Session 2026-10-14-007-complete-e137-cross-model-agreement-expe

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T07:25:43+00:00
- **Duration:** 7.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Complete E137 cross-model agreement experiment and determine next action

## Summary

E137 cross-model agreement experiment completed. Math_chain_of_thought on yi-6b: R1 recomputation works (macro 0.1275) but calibration is model-specific, not model-general. GSM cell on yi-6b: R1 recomputation gives mean 0.359 vs published 0.375, diff -0.016. View-count principle: 11 domains tested, boundary conditions mapped, no candidate validated (candidate seat empty). E137 complete; D111 stands. Key finding: R1 instrument calibration is model-dependent. Next: explore fresh observation per brief §2.

## Next

Explore fresh observation or refine R1 instrument based on model-specific calibration finding

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 8 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_gsm_yi6b_result.json |
|   undeclared | EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
|   undeclared | EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137_v2.json |
|   undeclared | EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_yi6b_math_out.json |
|   undeclared | EXPERIMENTS/E137-summary.json |
|   undeclared | EXPERIMENTS/experiment-outcome-summary.json |
|   undeclared | session-outcome-E137.json |
|   undeclared | sessions/2026-10-14-006-finalize-e137-cpan-cran-experiment-evide/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 07:25:43 | session_start | Complete E137 cross-model agreement experiment and determine next action |
| 2 | 07:25:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_gsm_yi6b_result.json |
| 3 | 07:25:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 4 | 07:25:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137_v2.json |
| 5 | 07:25:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_yi6b_math_out.json |
| 6 | 07:25:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E137-summary.json |
| 7 | 07:25:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 8 | 07:25:50 | unlogged_change | changed but never declared as an artifact: session-outcome-E137.json |
| 9 | 07:25:50 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-finalize-e137-cpan-cran-experiment-evide/events.jsonl |
| 10 | 07:25:50 | session_end | E137 cross-model agreement experiment completed. Math_chain_of_thought on yi-6b: R1 recomputation works (macro 0.1275) but calibration is model-specif |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-007-complete-e137-cross-model-agreement-expe/events.jsonl
```
