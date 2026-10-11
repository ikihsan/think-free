# Session 2026-10-11-041-declare-artifacts-from-e107-experiment-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-11T18:20:07+00:00
- **Duration:** 79.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Declare artifacts from E107 experiment and finalize session

## Summary

Declared artifacts from E107 experiment and updated HYPOTHESES-results.md with GitHub repositories view-count principle test results.

## Next

Per D083, next session must start from fresh observation in a new domain. Consider testing: Packagist (PHP), Pub.dev (Dart/Flutter), Go pkg.go.dev, CocoaPods, Conda Forge, Docker Hub, or specialized Stack Exchange sites (Super User, Ask Ubuntu, Server Fault, Unix & Linux, Electrical Engineering, Raspberry Pi, Arduino).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/107-github-repos-viewcount/PROTOCOL.md | 240a660670bc | 6098 |
| EXPERIMENTS/107-github-repos-viewcount/README.md | 5e622ec61e7c | 2100 |
| EXPERIMENTS/107-github-repos-viewcount/analyze.py | f401a0153045 | 8381 |
| EXPERIMENTS/107-github-repos-viewcount/harvest.py | fef6aa50f90e | 9265 |
| EXPERIMENTS/107-github-repos-viewcount/raw_data.json | cf4454a8c2c5 | 994693 |
| EXPERIMENTS/107-github-repos-viewcount/results.json | b608b9d8876a | 2973 |
| STATE-next-actions.md | daeb1dd723c0 | 22735 |
| HYPOTHESES-results.md | b23b63f748f8 | 5289 |

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
|   undeclared | sessions/2026-10-11-040-execute-t-0091-fresh-observation-experim/commands.log |
|   undeclared | sessions/2026-10-11-040-execute-t-0091-fresh-observation-experim/events.jsonl |
|   undeclared | tasks/CLAIMS.jsonl |
|   undeclared | tasks/T-0091-run-a-fresh-observation-experiment-testing-the-v.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:20:07 | session_start | Declare artifacts from E107 experiment and finalize session |
| 2 | 18:20:14 | artifact | wrote EXPERIMENTS/107-github-repos-viewcount/PROTOCOL.md |
| 3 | 18:20:15 | artifact | wrote EXPERIMENTS/107-github-repos-viewcount/README.md |
| 4 | 18:20:15 | artifact | wrote EXPERIMENTS/107-github-repos-viewcount/analyze.py |
| 5 | 18:20:16 | artifact | wrote EXPERIMENTS/107-github-repos-viewcount/harvest.py |
| 6 | 18:20:18 | artifact | wrote EXPERIMENTS/107-github-repos-viewcount/raw_data.json |
| 7 | 18:20:18 | artifact | wrote EXPERIMENTS/107-github-repos-viewcount/results.json |
| 8 | 18:20:19 | artifact | wrote STATE-next-actions.md |
| 9 | 18:21:16 | artifact | wrote HYPOTHESES-results.md |
| 10 | 18:21:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-040-execute-t-0091-fresh-observation-experim/commands.log |
| 11 | 18:21:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-040-execute-t-0091-fresh-observation-experim/events.jsonl |
| 12 | 18:21:26 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 13 | 18:21:26 | unlogged_change | changed but never declared as an artifact: tasks/T-0091-run-a-fresh-observation-experiment-testing-the-v.md |
| 14 | 18:21:26 | session_end | Declared artifacts from E107 experiment and updated HYPOTHESES-results.md with GitHub repositories view-count principle test results. |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-041-declare-artifacts-from-e107-experiment-a/events.jsonl
```
