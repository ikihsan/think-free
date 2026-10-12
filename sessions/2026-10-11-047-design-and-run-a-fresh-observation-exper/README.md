# Session 2026-10-11-047-design-and-run-a-fresh-observation-exper

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T20:12:54+00:00
- **Duration:** 2200.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Design and run a fresh observation experiment in a new domain per D083, testing view-count principle on an untested platform

## Summary

E109: Fresh observation on RubyGems (Ruby package registry). ALL FOUR GATES PASS. 100 need-related gems (queried by need verbs: fix, solve, resolve, handle, manage, process, convert, transform, validate, parse, extract, generate, create, build, deploy, monitor, track, analyze, report, notify, alert, schedule, queue, cache, store, backup, restore, sync, migrate, import, export, integrate, connect, bridge, automate, optimize, simplify, streamline, organize, filter, search, find, match, detect, identify, classify, categorize, encrypt, decrypt, secure, authenticate, authorize, protect, compress, decompress, encode, decode, serialize, deserialize) vs 100 random gems (queried by random letter combinations). G1: 100 need-related (PASS). G2: Mann-Whitney p=0.0045 (one-sided), Cliff's δ=0.214 (PASS). G3: 65% of need-related above random median, Wilson CI95 [0.553, 0.736], lower bound > 0.5 (PASS). G4: 100% download count coverage (PASS). Need median 29,330 vs random 14,404 (2.0× ratio). View-count principle generalizes to RubyGems — the 7th package registry where it holds (after PyPI, NPM, NuGet, Hex.pm, Packagist, and crates.io with caveats).

## Next

Update STATE.md and STATE-next-actions.md with E109 results. Continue fresh observation experiments per D083 in a new untested domain.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/109-rubygems-viewcount/results.json | 2bf12a90d3e1 | 1179 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 28 |
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
| 1 | 20:12:54 | session_start | Design and run a fresh observation experiment in a new domain per D083, testing view-count principle on an untested platform |
| 2 | 20:48:41 | milestone | E109 completed: Fresh observation on RubyGems (Ruby package registry). ALL GATES PASS — 100 need-related, 100 random gems. G2 p=0.0045 (Cliff's δ=0.21 |
| 3 | 20:48:52 | artifact | wrote EXPERIMENTS/109-rubygems-viewcount/results.json |
| 4 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/PROTOCOL.md |
| 5 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/README.md |
| 6 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/classifier.py |
| 7 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/needfind.py |
| 8 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/__init__.py |
| 9 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/github.py |
| 10 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/hex.py |
| 11 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/npm.py |
| 12 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/nuget.py |
| 13 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/pypi.py |
| 14 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/ranker.py |
| 15 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/PROTOCOL.md |
| 16 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/README.md |
| 17 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/analyze.py |
| 18 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/collect.py |
| 19 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/results.json |
| 20 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/109-rubygems-viewcount/need_gems.json |
| 21 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/109-rubygems-viewcount/random_gems.json |
| 22 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/PROTOCOL.md |
| 23 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/analyze.py |
| 24 | 20:49:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 25 | 20:49:34 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 26 | 20:49:34 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 27 | 20:49:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/commands.log |
| 28 | 20:49:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/events.jsonl |
| 29 | 20:49:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-044-fresh-observation-experiment-test-view-c/events.jsonl |
| 30 | 20:49:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-045-log-artifacts-from-e108-packagist-view-c/events.jsonl |
| 31 | 20:49:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-046-update-state-md-and-state-next-actions-m/events.jsonl |
| 32 | 20:49:35 | doc_update | updated STATE.md |
| 33 | 20:49:35 | session_end | E109: Fresh observation on RubyGems (Ruby package registry). ALL FOUR GATES PASS. 100 need-related gems (queried by need verbs: fix, solve, resolve, h |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-047-design-and-run-a-fresh-observation-exper/events.jsonl
```
