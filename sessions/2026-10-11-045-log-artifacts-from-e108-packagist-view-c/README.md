# Session 2026-10-11-045-log-artifacts-from-e108-packagist-view-c

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T19:24:45+00:00
- **Duration:** 22.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Log artifacts from E108 Packagist view-count experiment

## Summary

Logged E108 Packagist experiment artifacts (PROTOCOL.md, collect.py, analyze.py, README.md, results.json). The experiment validated the view-count principle on Packagist: all 4 gates pass with massive effect size (Cliff's delta 0.9936).

## Next

Update STATE.md and STATE-next-actions.md with E108 results, then begin fresh observation in new domain per D083.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/108-packagist-viewcount/PROTOCOL.md | 55196b8dad1c | 6687 |
| EXPERIMENTS/108-packagist-viewcount/collect.py | f5b76ffbb910 | 8752 |
| EXPERIMENTS/108-packagist-viewcount/analyze.py | 56631dde466b | 6464 |
| EXPERIMENTS/108-packagist-viewcount/README.md | eb615bd8450e | 2871 |
| EXPERIMENTS/108-packagist-viewcount/results.json | 92d1b7768083 | 625 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 14 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/PROTOCOL.md |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/README.md |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/classifier.py |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/needfind.py |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/platforms/__init__.py |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/platforms/github.py |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/platforms/hex.py |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/platforms/npm.py |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/platforms/nuget.py |
|   undeclared | EXPERIMENTS/108-cross-platform-need-discovery/platforms/pypi.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 19:24:45 | session_start | Log artifacts from E108 Packagist view-count experiment |
| 2 | 19:24:55 | artifact | wrote EXPERIMENTS/108-packagist-viewcount/PROTOCOL.md |
| 3 | 19:24:56 | artifact | wrote EXPERIMENTS/108-packagist-viewcount/collect.py |
| 4 | 19:24:57 | artifact | wrote EXPERIMENTS/108-packagist-viewcount/analyze.py |
| 5 | 19:24:58 | artifact | wrote EXPERIMENTS/108-packagist-viewcount/README.md |
| 6 | 19:24:59 | artifact | wrote EXPERIMENTS/108-packagist-viewcount/results.json |
| 7 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/PROTOCOL.md |
| 8 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/README.md |
| 9 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/classifier.py |
| 10 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/needfind.py |
| 11 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/__init__.py |
| 12 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/github.py |
| 13 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/hex.py |
| 14 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/npm.py |
| 15 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/nuget.py |
| 16 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/pypi.py |
| 17 | 19:25:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/ranker.py |
| 18 | 19:25:08 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/commands.log |
| 19 | 19:25:08 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/events.jsonl |
| 20 | 19:25:08 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-044-fresh-observation-experiment-test-view-c/events.jsonl |
| 21 | 19:25:08 | session_end | Logged E108 Packagist experiment artifacts (PROTOCOL.md, collect.py, analyze.py, README.md, results.json). The experiment validated the view-count pri |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-045-log-artifacts-from-e108-packagist-view-c/events.jsonl
```
