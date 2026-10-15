# Session 2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T17:56:43+00:00
- **Duration:** 1459.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Evaluate the regulatory value pre-pass as a candidate tool and test whether an improved discriminating-observation procedure can beat the baseline on appliance diagnosis

## Summary

Evaluated regulatory value pre-pass as candidate tool; discovered ground truth problem in discriminating-observation line. Created standalone regvalue tool with CLI, tests, and Federal Register API integration. Tool achieves 1.0 detection, 0.0 FP, 0.90 resolved share on Federal Register SUMMARY sections (E142 confirmed). Discriminating-observation line cannot be evaluated without grading the F116 genuinely unanswered pool (E092 40-row sample is 100% answered).

## Next

Decide whether to pursue regvalue as a candidate tool (demand validation needed) or close with measured scope per E143 recommendation. If pursuing regvalue, run prior-art check on regulatory compliance verification tools.

## Artifacts

_none_

## Commands

3 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/142-improved-discriminating-observation.py'] | 0 | 884 |
| 3 | ['python3', '-c', "\nimport json\n\n# Load the valueset.py and ground.py from E140/E142\nimport sys\nsys.path.insert(0, 'EXPERIMENTS/114-value-groundi | 1 | 709 |
| 4 | ['python3', '-c', "\nimport sys\nsys.path.insert(0, 'EXPERIMENTS/140-judge-form-invariance')\nfrom valueset import canonical, compare, numeric_multise | 0 | 189 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 28 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
|   undeclared | EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
|   undeclared | EXPERIMENTS/140-harvest-framework-issues/results.json |
|   undeclared | EXPERIMENTS/141-discriminating-observation-procedure/RESULT.md |
|   undeclared | EXPERIMENTS/142-improved-discriminating-observation.py |
|   undeclared | EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:56:43 | session_start | Evaluate the regulatory value pre-pass as a candidate tool and test whether an improved discriminating-observation procedure can beat the baseline on  |
| 2 | 17:56:56 | command | $ python3 EXPERIMENTS/142-improved-discriminating-observation.py |
| 3 | 18:00:02 | command | $ python3 -c  import json  # Load the valueset.py and ground.py from E140/E142 import sys sys.path.insert(0, 'EXPERIMENTS/114-value-grounding' |
| 4 | 18:01:16 | command | $ python3 -c  import sys sys.path.insert(0, 'EXPERIMENTS/140-judge-form-invariance') from valueset import canonical, compare, numeric_multiset |
| 5 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 6 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 7 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 8 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-discriminating-observation-procedure/RESULT.md |
| 9 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 10 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 11 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 12 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 13 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 14 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 15 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 16 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 17 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 18 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 19 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 20 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 21 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 22 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 23 | 18:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 24 | 18:21:01 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 25 | 18:21:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-005-implement-t-0093-test-discriminating-obs/events.jsonl |
| 26 | 18:21:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/commands.log |
| 27 | 18:21:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/events.jsonl |
| 28 | 18:21:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-007-final-session-recording-and-continuation/events.jsonl |
| 29 | 18:21:01 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 30 | 18:21:01 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 31 | 18:21:01 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue.py |
| 32 | 18:21:01 | unlogged_change | changed but never declared as an artifact: tools/regvalue/test_regvalue.py |
| 33 | 18:21:02 | session_end | Evaluated regulatory value pre-pass as candidate tool; discovered ground truth problem in discriminating-observation line. Created standalone regvalue |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/events.jsonl
```
