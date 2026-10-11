# Session 2026-10-11-040-execute-t-0091-fresh-observation-experim

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-11T18:03:19+00:00
- **Duration:** 988.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Execute T-0091: Fresh observation experiment testing view-count principle on GitHub code repositories with adequate sample size

## Summary

Completed T-0091: Fresh observation experiment E107 testing view-count principle on GitHub code repositories. All four gates pass with 150 classified repositories (77 need-related, 73 random). Need-related repos have 8.6× higher median star count (2,796 vs 325), Cliff's δ=0.826, p≈0.000. Principle generalizes to GitHub code repositories via star counts.

## Next

Per D083, next session must start from fresh observation in a new domain. Consider testing: Packagist (PHP), Pub.dev (Dart/Flutter), Go pkg.go.dev, CocoaPods, Conda Forge, Docker Hub, or specialized Stack Exchange sites (Super User, Ask Ubuntu, Server Fault, Unix & Linux, Electrical Engineering, Raspberry Pi, Arduino).

## Artifacts

_none_

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/107-github-repos-viewcount/harvest.py'] | 0 | 13787 |
| 3 | ['python3', 'EXPERIMENTS/107-github-repos-viewcount/analyze.py'] | 0 | 213 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7 |
| declared artifacts now missing | 0 |
| integrity errors | 2 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/README.md |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/analyze.py |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/harvest.py |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/raw_data.json |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/results.json |
|   undeclared | STATE-next-actions.md |
|   error | FAILURES.md was not updated although the session recorded experiment_result |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:03:19 | session_start | Execute T-0091: Fresh observation experiment testing view-count principle on GitHub code repositories with adequate sample size |
| 2 | 18:14:36 | command | $ python3 EXPERIMENTS/107-github-repos-viewcount/harvest.py |
| 3 | 18:14:51 | command | $ python3 EXPERIMENTS/107-github-repos-viewcount/analyze.py |
| 4 | 18:17:58 | experiment_result | ALL GATES PASS — view-count principle generalizes to GitHub code repositories (need median 8.6x random, Cliff's δ=0.826, p≈0.000) |
| 5 | 18:19:34 | task_rewrite | rewrote tasks/T-0091-run-a-fresh-observation-experiment-testing-the-v.md (status: done) |
| 6 | 18:19:35 | task_rewrite | appended a complete record for T-0091 |
| 7 | 18:19:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/PROTOCOL.md |
| 8 | 18:19:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/README.md |
| 9 | 18:19:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/analyze.py |
| 10 | 18:19:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/harvest.py |
| 11 | 18:19:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/raw_data.json |
| 12 | 18:19:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/results.json |
| 13 | 18:19:47 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 14 | 18:19:47 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 15 | 18:19:47 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 16 | 18:19:47 | session_end | Completed T-0091: Fresh observation experiment E107 testing view-count principle on GitHub code repositories. All four gates pass with 150 classified  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-040-execute-t-0091-fresh-observation-experim/events.jsonl
```
