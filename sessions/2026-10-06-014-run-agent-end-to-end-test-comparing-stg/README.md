# Session 2026-10-06-014-run-agent-end-to-end-test-comparing-stg

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T19:23:52+00:00
- **Duration:** 1521.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Run agent end-to-end test comparing stg vs alternatives for line-addressable staging

## Summary

Ran E042 agent end-to-end experiment comparing stg vs alternatives for line-addressable staging. stg achieves 6/6 first-try correctness with 0 silent failures. The strongest shell baseline (shell_baseline.py, ~180 lines) matches stg exactly, confirming the mechanism is replicable and not the differentiator. filterdiff achieves only 2/6 with 1 silent failure and 3 hard errors (exit 128). Naive git add -p achieves 2/6 with 4 silent failures. Kill gate 1 (stg better than filterdiff AND naive): PASSED. Kill gate 2 (shell_baseline matches stg): PASSED. The candidate stg survives as a useful tool (packaging value) but not as a mechanism invention. KILL-Q (adoption) remains not_evaluated.

## Next

Decide whether to pursue adoption measurement for stg (contact named requesters from E038: mcp-multi-root-git#3, sublime_merge#976, vim-gitgutter#446 — requires authorization) or pivot to a different candidate. The invention seat remains empty.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/042-stg-end-to-end/PROTOCOL.md | ae716b73dd7a | 2860 |
| EXPERIMENTS/042-stg-end-to-end/run_experiment.py | 4f5e6e9c5d29 | 9668 |
| EXPERIMENTS/042-stg-end-to-end/README.md | c0dd19f7e8ed | 4250 |
| EXPERIMENTS/042-stg-end-to-end/raw/compare.jsonl | bf975662b2c7 | 4994 |
| EXPERIMENTS/README.md | 07a6f3424406 | 7314 |
| FAILURES.md | 7caaf0b105b3 | 38439 |
| FAILURES-findings-26.md | f52cf371b684 | 7183 |
| FAILURES-findings-27.md | 1fb991aa044f | 1306 |
| docs/INDEX.md | e324fc889b08 | 41868 |

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport sys\nsys.path.insert(0, 'EXPERIMENTS/041-strongest-baseline')\nfrom shell_baseline import ShellBaseline\nimport subprocess | 0 | 368 |
| 3 | ['python3', 'EXPERIMENTS/042-stg-end-to-end/run_experiment.py'] | 0 | 5304 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/042-stg-end-to-end/results.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 19:23:52 | session_start | Run agent end-to-end test comparing stg vs alternatives for line-addressable staging |
| 2 | 19:28:13 | command | $ python3 -c  import sys sys.path.insert(0, 'EXPERIMENTS/041-strongest-baseline') from shell_baseline import ShellBaseline import subprocess i |
| 3 | 19:34:50 | command | $ python3 EXPERIMENTS/042-stg-end-to-end/run_experiment.py |
| 4 | 19:35:53 | artifact | wrote EXPERIMENTS/042-stg-end-to-end/PROTOCOL.md |
| 5 | 19:36:04 | artifact | wrote EXPERIMENTS/042-stg-end-to-end/run_experiment.py |
| 6 | 19:36:14 | artifact | wrote EXPERIMENTS/042-stg-end-to-end/README.md |
| 7 | 19:36:49 | artifact | wrote EXPERIMENTS/042-stg-end-to-end/raw/compare.jsonl |
| 8 | 19:37:16 | artifact | wrote EXPERIMENTS/README.md |
| 9 | 19:45:27 | artifact | wrote FAILURES.md |
| 10 | 19:46:21 | artifact | wrote FAILURES-findings-26.md |
| 11 | 19:46:28 | artifact | wrote FAILURES-findings-27.md |
| 12 | 19:46:34 | artifact | wrote docs/INDEX.md |
| 13 | 19:49:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/042-stg-end-to-end/results.jsonl |
| 14 | 19:49:13 | doc_update | updated FAILURES.md |
| 15 | 19:49:13 | session_end | Ran E042 agent end-to-end experiment comparing stg vs alternatives for line-addressable staging. stg achieves 6/6 first-try correctness with 0 silent  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-014-run-agent-end-to-end-test-comparing-stg/events.jsonl
```
