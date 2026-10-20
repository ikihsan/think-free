# Session 2026-10-14-008-run-e138-view-count-discrimination-exper

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T07:46:07+00:00
- **Duration:** 9.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run E138 view-count discrimination experiment on HA Discourse corpus and record results

## Summary

Ran E138 view-count discrimination experiment on 23-topic HA Discourse corpus. Kill gate fired (G1 not met: 13 served + 10 control = 23 topics, below >=20 per arm threshold). Experiment produced clean negative result: corpus too small for view-count measurement suite G1 gate. Results recorded in EXPERIMENTS/e138-viewcount-discrimination/ with protocol, script, and results.json. Key finding: G1 gate (≥20 per arm) appears to be a practical minimum for the view-count principle, as all prior positive results (E077, E082, E101) had ≥50 topics per arm. Next action: fresh view-count experiment on new domain with sufficient scale.

## Next

design fresh view-count experiment on new domain with ≥50 topics per arm and proper matched harvest

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 5 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/e138-viewcount-discrimination/DECISION_MD |
|   undeclared | EXPERIMENTS/e138-viewcount-discrimination/EXPERIMENT_SUMMARY.md |
|   undeclared | EXPERIMENTS/e138-viewcount-discrimination/results.json |
|   undeclared | EXPERIMENTS/e138-viewcount-discrimination/run_e138.py |
|   undeclared | EXPERIMENTS/experiment-outcome-summary.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 07:46:07 | session_start | Run E138 view-count discrimination experiment on HA Discourse corpus and record results |
| 2 | 07:46:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e138-viewcount-discrimination/DECISION_MD |
| 3 | 07:46:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e138-viewcount-discrimination/EXPERIMENT_SUMMARY.md |
| 4 | 07:46:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e138-viewcount-discrimination/results.json |
| 5 | 07:46:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e138-viewcount-discrimination/run_e138.py |
| 6 | 07:46:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 7 | 07:46:16 | session_end | Ran E138 view-count discrimination experiment on 23-topic HA Discourse corpus. Kill gate fired (G1 not met: 13 served + 10 control = 23 topics, below  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-008-run-e138-view-count-discrimination-exper/events.jsonl
```
