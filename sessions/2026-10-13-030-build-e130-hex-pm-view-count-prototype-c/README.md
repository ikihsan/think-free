# Session 2026-10-13-030-build-e130-hex-pm-view-count-prototype-c

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T12:39:32+00:00
- **Duration:** 39.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Build E130 Hex.pm view-count prototype CLI to test view-count principle classification framework

## Summary

Built E130 Hex.pm view-count prototype CLI tool and gathered evidence on the view-count principle's practical utility under matched-harvest design. Prototype is a runnable Python CLI (stdlib only) that fetches Hex.pm packages, classifies them using NEED_INDICATORS/GENERIC_TERMS framework, and evaluates gates G1-G4. Key observation: random-mode run with 100 packages (52 need-related, 48 random) showed G1 pass but G2/G3 fail — cliff_delta = -0.0304 (negative, opposite to E103's positive effect), Wilson LB = 0.3689 (well below 0.60 threshold). This is consistent with E113's matched-harvest finding that the view-count effect is a harvest artifact driven by asymmetric topic selection and unanchored substring matching. When the same pool is used with only the classification label differing, the positive effect does not replicate. Prototype, CLI, protocol, and results all recorded.

## Next

run additional prototype queries with larger samples or pivot to new domain to advance practical invention

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/130-hex-viewcount-prototype/cli.py | 6c00ae9d536c | 13522 |
| EXPERIMENTS/130-hex-viewcount-prototype/PROTOCOL.md | 09d4d5bad06c | 3370 |
| EXPERIMENTS/130-hex-viewcount-prototype/README.md | 30d885de0902 | 2197 |
| EXPERIMENTS/130-hex-viewcount-prototype/results.json | 5463aea9529f | 699 |
| EXPERIMENTS/130-hex-viewcount-prototype/search_results.json | 4476d6a2cf6c | 675 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 92 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/124-eval-harness-preflight/preflight/__main__.py |
|   undeclared | EXPERIMENTS/128-github-discussions-viewcount/results_demo.json |
|   undeclared | EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_001.json |
|   undeclared | EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_002.json |
|   undeclared | EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_003.json |
|   undeclared | EXPERIMENTS/130-preflight-third-harness/PRIOR-ART.md |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/analyze.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/classify_test.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/full_analyze.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/harvest.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:39:32 | session_start | Build E130 Hex.pm view-count prototype CLI to test view-count principle classification framework |
| 2 | 12:39:37 | milestone | E130 prototype built and tested |
| 3 | 12:39:44 | artifact | wrote EXPERIMENTS/130-hex-viewcount-prototype/cli.py |
| 4 | 12:39:45 | artifact | wrote EXPERIMENTS/130-hex-viewcount-prototype/PROTOCOL.md |
| 5 | 12:39:48 | artifact | wrote EXPERIMENTS/130-hex-viewcount-prototype/README.md |
| 6 | 12:39:49 | artifact | wrote EXPERIMENTS/130-hex-viewcount-prototype/results.json |
| 7 | 12:39:51 | artifact | wrote EXPERIMENTS/130-hex-viewcount-prototype/search_results.json |
| 8 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/124-eval-harness-preflight/preflight/__main__.py |
| 9 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/128-github-discussions-viewcount/results_demo.json |
| 10 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_001.json |
| 11 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_002.json |
| 12 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_003.json |
| 13 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-third-harness/PRIOR-ART.md |
| 14 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/analyze.py |
| 15 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/classify_test.py |
| 16 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/full_analyze.py |
| 17 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/harvest.py |
| 18 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/raw_pool.json |
| 19 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/test_label.py |
| 20 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-preflight-fourth-harness/PRIOR-ART.md |
| 21 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/RESULTS.md |
| 22 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/baseline.py |
| 23 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/harvest.py |
| 24 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/raw_pool.json |
| 25 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-preflight-fifth-harness/PRIOR-ART.md |
| 26 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/RESULTS.md |
| 27 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/baseline.py |
| 28 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/harvest.py |
| 29 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/raw_pool.json |
| 30 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/133-preflight-sixth-harness/PRIOR-ART.md |
| 31 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/134-preflight-prototype |
| 32 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/PRIOR-ART.md |
| 33 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/PROTOCOL.md |
| 34 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/README.md |
| 35 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/RESULT.md |
| 36 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/adapter.py |
| 37 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/harness.json |
| 38 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/key/ground_truth.json |
| 39 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/output/model_results.json |
| 40 | 12:40:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-preflight-prototype-release/README.md |
| 91 | 12:40:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-024-promote-preflight-to-public-product-stat/events.jsonl |
| 92 | 12:40:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-025-run-e130-view-count-classifier-experimen/events.jsonl |
| 93 | 12:40:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-026-continue-preflight-line-prototype-adapte/events.jsonl |
| 94 | 12:40:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-027-update-mission-state-records-and-determi/events.jsonl |
| 95 | 12:40:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-028-finalize-e137-preflight-prototype-and-ve/events.jsonl |
| 96 | 12:40:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-029-complete-t-0095-improve-preflight-usabil/events.jsonl |
| 97 | 12:40:11 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 98 | 12:40:11 | unlogged_change | changed but never declared as an artifact: tasks/T-0094-harvest-public-issue-trackers-and-practitioner-d.md |
| 99 | 12:40:11 | unlogged_change | changed but never declared as an artifact: tasks/T-0095-improve-preflight-usability-and-documentation.md |
| 100 | 12:40:12 | session_end | Built E130 Hex.pm view-count prototype CLI tool and gathered evidence on the view-count principle's practical utility under matched-harvest design. Pr |

_50 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-030-build-e130-hex-pm-view-count-prototype-c/events.jsonl
```
