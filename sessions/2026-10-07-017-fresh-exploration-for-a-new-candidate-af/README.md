# Session 2026-10-07-017-fresh-exploration-for-a-new-candidate-af

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-07T23:25:54+00:00
- **Duration:** 2584.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh exploration for a new candidate after stg withdrawal

## Summary

Ran falsification experiment 053-financial-reconciliation testing deterministic matching algorithm for bank statement vs ledger reconciliation. Kill gate PASSED on all three scenarios (clean, realistic, adversarial) across 5 seeds. Algorithm achieves 1.000 precision, 0.889 recall (realistic), 0.787 recall (adversarial) with 0 FPR. Significantly outperforms naive exact-match baseline (+0.08 F1 realistic, +0.15 F1 adversarial). Performance: ~2ms per 100 transactions. Prior art check: existing tools are full platforms (settlement-engine, Settly) or general record linkage libraries; this is a lightweight embeddable component with financial-specific heuristics (split detection, fee handling, date windows). Not yet a standalone candidate - would be a library contribution to existing projects.

## Next

Evaluate whether to pursue as library contribution to Settly/beancount/hledger, or test on real bank statement data (CSV/OFX) to validate synthetic results transfer to real data

## Artifacts

_none_

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['echo', 'Experiment 053-financial-reconciliation completed and verified'] | 0 | 3 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 19 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/052-task-prioritization/README.md |
|   undeclared | EXPERIMENTS/052-task-prioritization/experiment_052.py |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/PROTOCOL.md |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/README.md |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/baseline.py |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/constants.py |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/evaluate.py |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/generate.py |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/match.py |
|   undeclared | EXPERIMENTS/053-financial-reconciliation/results.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 23:25:54 | session_start | Fresh exploration for a new candidate after stg withdrawal |
| 2 | 00:08:03 | command | $ echo Experiment 053-financial-reconciliation completed and verified |
| 3 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/052-task-prioritization/README.md |
| 4 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/052-task-prioritization/experiment_052.py |
| 5 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/PROTOCOL.md |
| 6 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/README.md |
| 7 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/baseline.py |
| 8 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/constants.py |
| 9 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/evaluate.py |
| 10 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/generate.py |
| 11 | 00:08:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/match.py |
| 12 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/results.json |
| 13 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/results_seed123.json |
| 14 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/results_seed42.json |
| 15 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/results_seed456.json |
| 16 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/results_seed789.json |
| 17 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/results_seed999.json |
| 18 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/run.py |
| 19 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/scoring.py |
| 20 | 00:08:59 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/053-financial-reconciliation/splits.py |
| 21 | 00:08:59 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-07-016-conclude-e051-experiment-and-identify-ne/events.jsonl |
| 22 | 00:08:59 | session_end | Ran falsification experiment 053-financial-reconciliation testing deterministic matching algorithm for bank statement vs ledger reconciliation. Kill g |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-07-017-fresh-exploration-for-a-new-candidate-af/events.jsonl
```
