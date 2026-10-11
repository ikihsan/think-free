# Session 2026-10-11-017-design-and-run-fresh-observation-experim

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T10:28:13+00:00
- **Duration:** 5223.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Design and run fresh observation experiment on crates.io (Rust package registry) to test view-count principle on a new package registry domain

## Summary

Conducted fresh observation experiment E095 on crates.io (Rust package registry) to test view-count principle. Collected 346 need-related crates (by keyword search) and 200 random crates, verified 70 need-related and 476 random (substring matching). All crates had recent_downloads > 0 (100% active), eliminating binary discrimination. Threshold-based analysis showed inconsistent results (need-related higher at some thresholds, random at others). Mann-Whitney U tests: total downloads p=0.082, recent downloads p=0.139. Gates: G1 FAIL (70 < 100), G2 FAIL (p > 0.05), G3 MIXED (Wilson LB=0.92 but trivial), G4 PASS (100% arrival field). Conclusion: view-count principle does not robustly generalize to crates.io, consistent with failures on Maven Central and Hugging Face Hub. Also fixed 093-discrimination-test (split into classify.py + main.py), split 094-k8s-discourse-viewcount (stats.py + main.py), and added origin-meta blocks to new experiment files. Doc lint passes.

## Next

Choose a new domain for fresh observation per D083, avoiding previously tested domains (PyPI, NPM, Maven Central, crates.io, Hugging Face Hub, Discourse, Stack Exchange, GitHub issues, web search, Kubernetes Discourse, automotive OBD2, embedded fault codes, 3D printer faults, PX4 drone faults, appliance diagnosis, CFPB, Python import resolvability, GitHub repos). Candidate: CRAN R packages, RubyGems, Docker Hub, or non-software forums not yet tested.

## Artifacts

_none_

## Commands

6 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', 'https://crates.io/api/v1/crates?page=1&per_page=5'] | 0 | 276 |
| 3 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/collect.py'] | 0 | 477044 |
| 4 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/collect_v2.py'] | 0 | 340625 |
| 5 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/collect_v3.py'] | 0 | 518303 |
| 6 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/analyze.py'] | 1 | 520 |
| 7 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/analyze.py'] | 0 | 392 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 16 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/093-discrimination-test |
|   undeclared | EXPERIMENTS/093-discrimination-test/classify.py |
|   undeclared | EXPERIMENTS/093-discrimination-test/main.py |
|   undeclared | EXPERIMENTS/094-k8s-discourse-viewcount/main.py |
|   undeclared | EXPERIMENTS/094-k8s-discourse-viewcount/stats.py |
|   undeclared | EXPERIMENTS/095-crates-io-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/095-crates-io-viewcount/README.md |
|   undeclared | EXPERIMENTS/095-crates-io-viewcount/analyze.py |
|   undeclared | EXPERIMENTS/095-crates-io-viewcount/collect.py |
|   undeclared | EXPERIMENTS/095-crates-io-viewcount/collect_v2.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:28:13 | session_start | Design and run fresh observation experiment on crates.io (Rust package registry) to test view-count principle on a new package registry domain |
| 2 | 10:28:26 | command | $ curl -s https://crates.io/api/v1/crates?page=1&per_page=5 |
| 3 | 10:41:17 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/collect.py |
| 4 | 10:59:59 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/collect_v2.py |
| 5 | 11:11:51 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/collect_v3.py |
| 6 | 11:13:54 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/analyze.py |
| 7 | 11:15:25 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/analyze.py |
| 8 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-discrimination-test |
| 9 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-discrimination-test/classify.py |
| 10 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-discrimination-test/main.py |
| 11 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/094-k8s-discourse-viewcount/main.py |
| 12 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/094-k8s-discourse-viewcount/stats.py |
| 13 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/095-crates-io-viewcount/PROTOCOL.md |
| 14 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/095-crates-io-viewcount/README.md |
| 15 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/095-crates-io-viewcount/analyze.py |
| 16 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/095-crates-io-viewcount/collect.py |
| 17 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/095-crates-io-viewcount/collect_v2.py |
| 18 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/095-crates-io-viewcount/collect_v3.py |
| 19 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/095-crates-io-viewcount/results.json |
| 20 | 11:55:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/synthesis-view-count-final.md |
| 21 | 11:55:16 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 22 | 11:55:16 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 23 | 11:55:16 | unlogged_change | changed but never declared as an artifact: THINK_FREE_SUMMARY.md |
| 24 | 11:55:16 | session_end | Conducted fresh observation experiment E095 on crates.io (Rust package registry) to test view-count principle. Collected 346 need-related crates (by k |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-017-design-and-run-fresh-observation-experim/events.jsonl
```
