# Session 2026-10-13-038-run-e137-demand-validation-for-preflight

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T16:04:57+00:00
- **Duration:** 689.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Run E137 demand validation for preflight: harvest practitioner reports of C1/C2/C3 defects across LLM evaluation frameworks

## Summary

E137 demand validation completed: harvested GitHub issues from evalscope and evals, plus Stack Overflow, Reddit, arXiv. Classification found 63 C1_credible (all from 2 frameworks: evalscope 40, evals 23), 0 C2_credible, 0 C3_credible. G1 gate FAILS (≥10 credible across ≥3 frameworks required, got 63 across 2). GATE_CLOSED - demand too weak for preflight candidate. Classification has false positives (keyword matching without defect understanding) but gate verdict stands.

## Next

No further action on preflight demand validation. The candidate is withdrawn on demand grounds per protocol.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 115 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/124-eval-harness-preflight/preflight/__main__.py |
|   undeclared | EXPERIMENTS/128-github-discussions-viewcount/results_demo.json |
|   undeclared | EXPERIMENTS/130-hex-viewcount-prototype/PROTOCOL.md |
|   undeclared | EXPERIMENTS/130-hex-viewcount-prototype/README.md |
|   undeclared | EXPERIMENTS/130-hex-viewcount-prototype/cli.py |
|   undeclared | EXPERIMENTS/130-hex-viewcount-prototype/results.json |
|   undeclared | EXPERIMENTS/130-hex-viewcount-prototype/search_results.json |
|   undeclared | EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_001.json |
|   undeclared | EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_002.json |
|   undeclared | EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_003.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:04:57 | session_start | Run E137 demand validation for preflight: harvest practitioner reports of C1/C2/C3 defects across LLM evaluation frameworks |
| 2 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/124-eval-harness-preflight/preflight/__main__.py |
| 3 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/128-github-discussions-viewcount/results_demo.json |
| 4 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-hex-viewcount-prototype/PROTOCOL.md |
| 5 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-hex-viewcount-prototype/README.md |
| 6 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-hex-viewcount-prototype/cli.py |
| 7 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-hex-viewcount-prototype/results.json |
| 8 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-hex-viewcount-prototype/search_results.json |
| 9 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_001.json |
| 10 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_002.json |
| 11 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-adapter-third-harness/mismatched_output/task_003.json |
| 12 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-preflight-third-harness/PRIOR-ART.md |
| 13 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-single-results-json-harness/adapter.py |
| 14 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-single-results-json-harness/results.json |
| 15 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/analyze.py |
| 16 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/classify_test.py |
| 17 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/full_analyze.py |
| 18 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/harvest.py |
| 19 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/raw_pool.json |
| 20 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/test_label.py |
| 21 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-preflight-fourth-harness/PRIOR-ART.md |
| 22 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/RESULTS.md |
| 23 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/baseline.py |
| 24 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/harvest.py |
| 25 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/raw_pool.json |
| 26 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-preflight-fifth-harness/PRIOR-ART.md |
| 27 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/RESULTS.md |
| 28 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/baseline.py |
| 29 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/harvest.py |
| 30 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/raw_pool.json |
| 31 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/133-preflight-sixth-harness/PRIOR-ART.md |
| 32 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/134-preflight-prototype |
| 33 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/PRIOR-ART.md |
| 34 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/PROTOCOL.md |
| 35 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/README.md |
| 36 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/RESULT.md |
| 37 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/adapter.py |
| 38 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/harness.json |
| 39 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/key/ground_truth.json |
| 40 | 16:16:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/output/model_results.json |
| 108 | 16:16:27 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-032-explore-preflight-experiment-e128-e129-a/events.jsonl |
| 109 | 16:16:27 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-033-prototype-and-measure-preflight-adapter/events.jsonl |
| 110 | 16:16:27 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-034-run-doc-lint-and-finalize-preflight-rele/events.jsonl |
| 111 | 16:16:27 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-035-verify-t-0095-completion-preflight-8-ada/events.jsonl |
| 112 | 16:16:27 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-036-harvest-demand-evidence-for-preflight-to/events.jsonl |
| 113 | 16:16:27 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-037-complete-t-0095-verify-preflight-adapter/events.jsonl |
| 114 | 16:16:27 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 115 | 16:16:27 | unlogged_change | changed but never declared as an artifact: tasks/T-0094-harvest-public-issue-trackers-and-practitioner-d.md |
| 116 | 16:16:27 | unlogged_change | changed but never declared as an artifact: tasks/T-0095-improve-preflight-usability-and-documentation.md |
| 117 | 16:16:27 | session_end | E137 demand validation completed: harvested GitHub issues from evalscope and evals, plus Stack Overflow, Reddit, arXiv. Classification found 63 C1_cre |

_67 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-038-run-e137-demand-validation-for-preflight/events.jsonl
```
