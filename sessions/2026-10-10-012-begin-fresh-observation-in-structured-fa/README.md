# Session 2026-10-10-012-begin-fresh-observation-in-structured-fa

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T13:14:41+00:00
- **Duration:** 3278.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Begin fresh observation in structured fault/error-code domains by reading actual practitioner rows on Discourse forums to validate the view_count instrument's discrimination before any classifier

## Summary

Fresh observation in robotics/ROS error codes domain (E097): Collected 10 practitioner rows from Open Robotics Discourse forum across Nav2, Gazebo, and Open-RMF categories. Discrimination test PASSED (FPR=0.000, TPR=0.800, FNR=0.200) on 10 probes with labels known by construction. Population measurement: 9 need statements, unserved-open-like fraction 55.6% (Wilson CI95 [26.7%, 81.1%]), higher than Discourse baseline 11.7% (E077) and embedded Discourse 15.3% (E082). View count instrument generalizes (100% view_positive_rate). Sample size insufficient for protocol G3 threshold (need ≥15). No candidate produced; evidence-gathering per D083.

## Next

Expand practitioner sample to ≥20 rows by harvesting more Discourse categories and pages, then re-measure population with validated instrument. Alternatively, test instrument on medical device alarm codes (E082 protocol) or industrial PLC fault codes (E084 protocol) for cross-domain validation.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/097-ros-error-codes-fresh/PROTOCOL.md | 8bad35a8ca2a | 9270 |
| EXPERIMENTS/097-ros-error-codes-fresh/RESULTS.md | 435826a1ea92 | 7268 |
| EXPERIMENTS/097-ros-error-codes-fresh/collect_practitioner_rows.py | 5099107b4d99 | 7203 |
| EXPERIMENTS/097-ros-error-codes-fresh/run_discrimination_test.py | 28436285d082 | 9137 |
| EXPERIMENTS/097-ros-error-codes-fresh/measure_population.py | 3dfad94b063d | 6747 |
| EXPERIMENTS/097-ros-error-codes-fresh/deduplicate.py | 877816d41d7c | 1041 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 13:14:41 | session_start | Begin fresh observation in structured fault/error-code domains by reading actual practitioner rows on Discourse forums to validate the view_count inst |
| 2 | 13:18:04 | milestone | Reviewed current state: 6 invention claims tested, none validated; view_count principle validated on multiple platforms; 4 structured-fault domains te |
| 3 | 13:54:03 | milestone | Completed fresh observation in robotics/ROS error codes domain (E097): discrimination test PASS (FPR=0.0, TPR=0.8, FNR=0.2); population measurement sh |
| 4 | 13:54:10 | artifact | wrote EXPERIMENTS/097-ros-error-codes-fresh/PROTOCOL.md |
| 5 | 13:54:28 | artifact | wrote EXPERIMENTS/097-ros-error-codes-fresh/RESULTS.md |
| 6 | 13:55:32 | artifact | wrote EXPERIMENTS/097-ros-error-codes-fresh/collect_practitioner_rows.py |
| 7 | 13:55:38 | artifact | wrote EXPERIMENTS/097-ros-error-codes-fresh/run_discrimination_test.py |
| 8 | 13:55:45 | artifact | wrote EXPERIMENTS/097-ros-error-codes-fresh/measure_population.py |
| 9 | 13:56:00 | artifact | wrote EXPERIMENTS/097-ros-error-codes-fresh/deduplicate.py |
| 10 | 14:09:20 | session_end | Fresh observation in robotics/ROS error codes domain (E097): Collected 10 practitioner rows from Open Robotics Discourse forum across Nav2, Gazebo, an |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-012-begin-fresh-observation-in-structured-fa/events.jsonl
```
