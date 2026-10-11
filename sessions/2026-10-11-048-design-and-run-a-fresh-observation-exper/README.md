# Session 2026-10-11-048-design-and-run-a-fresh-observation-exper

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T21:04:31+00:00
- **Duration:** 1482.6s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Design and run a fresh observation experiment testing the view-count principle on Docker Hub container images using pull counts as arrival metric

## Summary

E111 completed: View-count principle validated on Docker Hub container image registry. ALL GATES PASS — 3,850 images (3,313 need-related, 537 random), G2 p≈6.8e-47 (Cliff's δ=0.386), G3 Wilson LB=0.785 (2,648/3,313 above random median). Need median 50,070 vs random 5,319 (9.4×). This is the 8th platform where the principle holds (PyPI, NPM, NuGet, Hex.pm, Packagist, RubyGems, GitHub repos, Docker Hub). Updated STATE.md and STATE-next-actions.md with results.

## Next

Per D083, next session must start fresh observation in a new domain. Candidates: Terraform Registry, VS Code Marketplace, Chrome/Firefox extension stores, Homebrew, AUR, Chocolatey, Pub.dev, CocoaPods, Swift Package Index, Go module proxy, GitLab repos, CPAN, Hackage, Quicklisp, OPAM, Melpa, CTAN, Stack Overflow/Server Fault/Super User/Ask Ubuntu, Reddit programming communities, Dev.to/Hashnode/Medium, Arduino/Raspberry Pi/ESP32 forums.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 38 |
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
| 1 | 21:04:31 | session_start | Design and run a fresh observation experiment testing the view-count principle on Docker Hub container images using pull counts as arrival metric |
| 2 | 21:20:41 | milestone | E111 completed: ALL GATES PASS on Docker Hub (3,313 need-related vs 537 random, p≈6.8e-47, Cliff's δ=0.386, Wilson LB=0.785). View-count principle gen |
| 3 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/PROTOCOL.md |
| 4 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/README.md |
| 5 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/classifier.py |
| 6 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/needfind.py |
| 7 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/__init__.py |
| 8 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/github.py |
| 9 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/hex.py |
| 10 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/npm.py |
| 11 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/nuget.py |
| 12 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/platforms/pypi.py |
| 13 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-cross-platform-need-discovery/ranker.py |
| 14 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/PROTOCOL.md |
| 15 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/README.md |
| 16 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/analyze.py |
| 17 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/collect.py |
| 18 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-packagist-viewcount/results.json |
| 19 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/109-rubygems-viewcount/need_gems.json |
| 20 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/109-rubygems-viewcount/random_gems.json |
| 21 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/109-rubygems-viewcount/results.json |
| 22 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/PROTOCOL.md |
| 23 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/analyze.py |
| 24 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 25 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/PROTOCOL.md |
| 26 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/README.md |
| 27 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/analyze.py |
| 28 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/classified_data.json |
| 29 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/classify.py |
| 30 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/harvest.py |
| 31 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/raw_data.json |
| 32 | 21:29:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/111-dockerhub-viewcount/results.json |
| 33 | 21:29:13 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 34 | 21:29:13 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 35 | 21:29:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/commands.log |
| 36 | 21:29:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-043-build-a-cross-platform-need-discovery-pr/events.jsonl |
| 37 | 21:29:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-044-fresh-observation-experiment-test-view-c/events.jsonl |
| 38 | 21:29:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-045-log-artifacts-from-e108-packagist-view-c/events.jsonl |
| 39 | 21:29:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-046-update-state-md-and-state-next-actions-m/events.jsonl |
| 40 | 21:29:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-047-design-and-run-a-fresh-observation-exper/events.jsonl |
| 41 | 21:29:13 | doc_update | updated STATE.md |
| 42 | 21:29:13 | session_end | E111 completed: View-count principle validated on Docker Hub container image registry. ALL GATES PASS — 3,850 images (3,313 need-related, 537 random), |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-048-design-and-run-a-fresh-observation-exper/events.jsonl
```
