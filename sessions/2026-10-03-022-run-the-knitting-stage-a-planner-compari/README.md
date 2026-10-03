# Session 2026-10-03-022-run-the-knitting-stage-a-planner-compari

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T17:23:17+00:00
- **Duration:** 914.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run the knitting Stage-A planner comparison: local planner vs exhaustive search on small graphs

## Summary

T-0010: knitting Stage-A local-vs-exhaustive comparison complete; local heuristic valid 9/9, refuses unsupported state, suboptimal on shared-release case; narrow-not-abandon recorded.

## Next

Bounded-neighbourhood planner against the same oracle before Stage-B.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/004-knitting-stage-a/planner.py | 8a7872141568 | 11751 |
| EXPERIMENTS/004-knitting-stage-a/results.json | 1b875fd081ce | 11837 |
| EXPERIMENTS/004-knitting-stage-a/README.md | 92910bfac61b | 5175 |

## Commands

4 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/004-knitting-stage-a/planner.py'] | 0 | 491 |
| 4 | ['python3', 'EXPERIMENTS/004-knitting-stage-a/planner.py'] | 0 | 116 |
| 5 | ['python3', 'EXPERIMENTS/004-knitting-stage-a/planner.py'] | 0 | 100 |
| 6 | ['python3', 'EXPERIMENTS/004-knitting-stage-a/planner.py'] | 0 | 107 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 3 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | HYPOTHESES.md |
|   undeclared | STATE.md |
|   undeclared | tasks/T-0010-run-the-knitting-stage-a-planner-comparison-loca.md |
|   error | FAILURES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:23:17 | session_start | Run the knitting Stage-A planner comparison: local planner vs exhaustive search on small graphs |
| 2 | 17:24:25 | milestone | Created T-0010 (knitting Stage-A planner comparison); pushing before claim |
| 3 | 17:26:11 | command | $ python3 EXPERIMENTS/004-knitting-stage-a/planner.py |
| 4 | 17:27:30 | command | $ python3 EXPERIMENTS/004-knitting-stage-a/planner.py |
| 5 | 17:28:12 | command | $ python3 EXPERIMENTS/004-knitting-stage-a/planner.py |
| 6 | 17:30:04 | command | $ python3 EXPERIMENTS/004-knitting-stage-a/planner.py |
| 7 | 17:37:26 | experiment_result | 10 cases (9 solved, 1 refused). Local heuristic valid on all 9 solved cases and refuses unsupported_shaping; suboptimal on same_column_stack_4x4 (loca |
| 8 | 17:37:27 | artifact | wrote EXPERIMENTS/004-knitting-stage-a/planner.py |
| 9 | 17:37:27 | artifact | wrote EXPERIMENTS/004-knitting-stage-a/results.json |
| 10 | 17:37:27 | artifact | wrote EXPERIMENTS/004-knitting-stage-a/README.md |
| 11 | 17:38:31 | unlogged_change | changed but never declared as an artifact: HYPOTHESES.md |
| 12 | 17:38:31 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 13 | 17:38:31 | unlogged_change | changed but never declared as an artifact: tasks/T-0010-run-the-knitting-stage-a-planner-comparison-loca.md |
| 14 | 17:38:32 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 15 | 17:38:32 | doc_update | updated HYPOTHESES.md |
| 16 | 17:38:32 | doc_update | updated STATE.md |
| 17 | 17:38:32 | session_end | T-0010: knitting Stage-A local-vs-exhaustive comparison complete; local heuristic valid 9/9, refuses unsupported state, suboptimal on shared-release c |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-022-run-the-knitting-stage-a-planner-compari/events.jsonl
```
