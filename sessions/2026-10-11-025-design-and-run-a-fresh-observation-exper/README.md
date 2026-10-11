# Session 2026-10-11-025-design-and-run-a-fresh-observation-exper

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T16:19:15+00:00
- **Duration:** 1428.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Design and run a fresh observation experiment in a new domain per D083, testing view-count principle on an untested platform/category

## Summary

Designed and executed fresh observation experiment E103 on Hex.pm (Elixir/Erlang package registry) per D083. Collected 200 packages (100 need-related via keyword searches, 100 random via default listing). All four gates PASS: G1 (sample=200≥100), G2 (Mann-Whitney U p≈0.000, Cliff's δ=0.861), G3 (Wilson LB=0.946, 99/100 need-related above random median), G4 (both categories represented). Need-related packages show dramatically higher 30-day downloads: median 80,078 vs 365 (220×), mean 644K vs 37K (17×). View-count principle generalizes strongly to Hex.pm, joining PyPI, NPM, and NuGet as package registries where the principle holds. Updated STATE.md and STATE-next-actions.md with findings.

## Next

Continue fresh observation in a new domain per D083. Remaining untested package registries: Go pkg.go.dev, Pub.dev (Dart/Flutter), CocoaPods, CPAN, Docker Hub. Also consider VS Code Marketplace, Chrome Web Store, or other extension marketplaces with install metrics.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/103-hex-viewcount/PROTOCOL.md | 809f546a8a4e | 5901 |
| EXPERIMENTS/103-hex-viewcount/collect.py | d2f7bdc3f663 | 7886 |
| EXPERIMENTS/103-hex-viewcount/analyze.py | af5f616a3800 | 6444 |
| EXPERIMENTS/103-hex-viewcount/README.md | b77644fe1187 | 2822 |
| EXPERIMENTS/103-hex-viewcount/results.json | b1cb91f63656 | 621 |
| STATE.md | 66a9d4228949 | 25075 |
| STATE-next-actions.md | 526de6d776ed | 20909 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/0xx-maven-viewcount-dir/experiment.py |
|   undeclared | EXPERIMENTS/0xx-maven-viewcount-dir/results.json |
|   undeclared | EXPERIMENTS/0xx-packagist-viewcount/experiment.py |
|   undeclared | EXPERIMENTS/0xx-packagist-viewcount/results.json |
|   undeclared | EXPERIMENTS/0xx-rubygems-viewcount/experiment.py |
|   undeclared | EXPERIMENTS/0xx-rubygems-viewcount/results.json |
|   undeclared | EXPERIMENTS/0xx-viewcount-framework/viewcount_framework.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:19:15 | session_start | Design and run a fresh observation experiment in a new domain per D083, testing view-count principle on an untested platform/category |
| 2 | 16:41:10 | artifact | wrote EXPERIMENTS/103-hex-viewcount/PROTOCOL.md |
| 3 | 16:41:11 | artifact | wrote EXPERIMENTS/103-hex-viewcount/collect.py |
| 4 | 16:41:12 | artifact | wrote EXPERIMENTS/103-hex-viewcount/analyze.py |
| 5 | 16:41:13 | artifact | wrote EXPERIMENTS/103-hex-viewcount/README.md |
| 6 | 16:41:14 | artifact | wrote EXPERIMENTS/103-hex-viewcount/results.json |
| 7 | 16:41:15 | artifact | wrote STATE.md |
| 8 | 16:41:16 | artifact | wrote STATE-next-actions.md |
| 9 | 16:43:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-maven-viewcount-dir/experiment.py |
| 10 | 16:43:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-maven-viewcount-dir/results.json |
| 11 | 16:43:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-packagist-viewcount/experiment.py |
| 12 | 16:43:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-packagist-viewcount/results.json |
| 13 | 16:43:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-rubygems-viewcount/experiment.py |
| 14 | 16:43:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-rubygems-viewcount/results.json |
| 15 | 16:43:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-framework/viewcount_framework.py |
| 16 | 16:43:03 | doc_update | updated STATE.md |
| 17 | 16:43:03 | session_end | Designed and executed fresh observation experiment E103 on Hex.pm (Elixir/Erlang package registry) per D083. Collected 200 packages (100 need-related  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-025-design-and-run-a-fresh-observation-exper/events.jsonl
```
