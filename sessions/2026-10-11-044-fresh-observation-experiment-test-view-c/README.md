# Session 2026-10-11-044-fresh-observation-experiment-test-view-c

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T19:10:09+00:00
- **Duration:** 840.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation experiment: test view-count principle on Packagist (PHP/Composer package registry) - a major untested package registry with download counts

## Summary

E108 completed: View-count principle tested on Packagist (PHP/Composer). ALL GATES PASS - need-related packages 100% active (monthly downloads > 0) vs random 26% active. Cliff's delta = 0.9936 (near-maximum separation). This is the 7th package registry tested and the 5th where the principle works strongly (PyPI, NPM, NuGet, Hex.pm, Packagist). Principle works on mature, infrastructure-heavy package ecosystems.

## Next

Continue fresh observation in new domain per D083. Candidate domains not yet tested: RubyGems (mentioned in E103 as 100% active both groups), Go pkg.go.dev, Docker Hub, Pub.dev (Dart/Flutter), Cargo (already tested as crates.io and failed), Anaconda/Conda, Homebrew, Linux package managers (apt, dnf, pacman).

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 18 |
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
| 1 | 19:10:09 | session_start | Fresh observation experiment: test view-count principle on Packagist (PHP/Composer package registry) - a major untested package registry with download |
| 2 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/PROTOCOL.md |
| 3 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/README.md |
| 4 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/classifier.py |
| 5 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/needfind.py |
| 6 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/__init__.py |
| 7 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/github.py |
| 8 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/hex.py |
| 9 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/npm.py |
| 10 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/nuget.py |
| 11 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/pypi.py |
| 12 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/ranker.py |
| 13 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/PROTOCOL.md |
| 14 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/README.md |
| 15 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/analyze.py |
| 16 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/collect.py |
| 17 | 19:24:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/results.json |
| 18 | 19:24:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/commands.log |
| 19 | 19:24:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/events.jsonl |
| 20 | 19:24:09 | session_end | E108 completed: View-count principle tested on Packagist (PHP/Composer). ALL GATES PASS - need-related packages 100% active (monthly downloads > 0) vs |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-044-fresh-observation-experiment-test-view-c/events.jsonl
```
