# Session 2026-10-10-011-measure-real-python-import-error-reports

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T12:16:31+00:00
- **Duration:** 625.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure real Python import-error reports that name a module and no distribution (T-0088)

## Summary

E086 population measurement complete: discrimination test PASSED (G1 FPR=0.067, G2 TPR=1.000, G3 Precision=0.909). Measured 31 real ImportError reports from Stack Overflow and GitHub; 19.35% (6/31, CI95 [9.19%, 36.28%]) name a module and no distribution — 19x the 1% kill gate. Decision: BUILD — prototype resolver integration. Package-name line stays open.

## Next

Prototype pyprovides CLI integration for ModuleNotFoundError workflow; measure actual usage impact on time-to-fix.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 6 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/086-import-error-demand/PROTOCOL.md |
|   undeclared | EXPERIMENTS/086-import-error-demand/VERDICT.md |
|   undeclared | EXPERIMENTS/086-import-error-demand/measure_population.py |
|   undeclared | EXPERIMENTS/086-import-error-demand/results.json |
|   undeclared | EXPERIMENTS/086-import-error-demand/run_discrimination_test.py |
|   undeclared | EXPERIMENTS/090-hand-classification/README.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:16:31 | session_start | Measure real Python import-error reports that name a module and no distribution (T-0088) |
| 2 | 12:26:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/086-import-error-demand/PROTOCOL.md |
| 3 | 12:26:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/086-import-error-demand/VERDICT.md |
| 4 | 12:26:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/086-import-error-demand/measure_population.py |
| 5 | 12:26:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/086-import-error-demand/results.json |
| 6 | 12:26:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/086-import-error-demand/run_discrimination_test.py |
| 7 | 12:26:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-hand-classification/README.md |
| 8 | 12:26:56 | session_end | E086 population measurement complete: discrimination test PASSED (G1 FPR=0.067, G2 TPR=1.000, G3 Precision=0.909). Measured 31 real ImportError report |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-011-measure-real-python-import-error-reports/events.jsonl
```
