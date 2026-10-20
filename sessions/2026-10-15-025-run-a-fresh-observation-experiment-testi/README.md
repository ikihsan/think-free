# Session 2026-10-15-025-run-a-fresh-observation-experiment-testi

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T20:15:40+00:00
- **Duration:** 3473.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run a fresh observation experiment testing the view-count principle on VS Code Marketplace, chosen by stated rule: largest untouched extension marketplace with exposable per-item install-count metadata

## Summary

Completed fresh observation experiment E151 testing the view-count principle on VS Code Marketplace (Open VSX). The Open VSX search API only returns top 100 results per query sorted by downloadCount with pagination returning identical results, making stratified sampling impossible. Population kill gate fired: only 24 general extensions (themes/icons/keymaps/snippets) could be sampled vs 4,519 need-related extensions (threshold: 30 per group). Cliff's delta = -0.055 (95% CI: [-0.24, 0.17]) shows no meaningful difference. The test is inconclusive due to API constraints, not a measured effect. Updated VIEW-COUNT-SUMMARY.md to document this boundary.

## Next

Choose next fresh observation domain per stated rule: largest untouched platform with exposable per-item metadata. Candidates from VIEW-COUNT-SUMMARY.md: Mozilla Add-ons, Chrome Web Store, GitLab code repositories, GitHub user/org follower counts.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/151-vscode-marketplace-viewcount/PROTOCOL.md | 38f51dfb9193 | 7106 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/run.py | cf4a4b78c1ca | 10378 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/classifier.py | ab6c2e6b91db | 7065 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/RESULT.md | 72549b15ff73 | 2047 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIER.md | 28af4b55ce5c | 3110 |
| docs/reference/VIEW-COUNT-SUMMARY.md | f1b272d3df73 | 5415 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/RAW_DATA.jsonl | fd8c705583af | 813551 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIED.jsonl | 513d4e5f18ea | 807255 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 90 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/PROTOCOL.md |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/RESULT.md |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/attempts.jsonl |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/classify.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/fetch-threads.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/fetch.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-probes.json |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-results.jsonl |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-run.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/grading-results.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 20:15:40 | session_start | Run a fresh observation experiment testing the view-count principle on VS Code Marketplace, chosen by stated rule: largest untouched extension marketp |
| 2 | 21:10:46 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/PROTOCOL.md |
| 3 | 21:10:54 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/run.py |
| 4 | 21:11:09 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/classifier.py |
| 5 | 21:11:20 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/RESULT.md |
| 6 | 21:11:33 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIER.md |
| 7 | 21:11:44 | artifact | wrote docs/reference/VIEW-COUNT-SUMMARY.md |
| 8 | 21:11:51 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/RAW_DATA.jsonl |
| 9 | 21:12:00 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIED.jsonl |
| 10 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/PROTOCOL.md |
| 11 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/RESULT.md |
| 12 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/attempts.jsonl |
| 13 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/classify.py |
| 14 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/fetch-threads.py |
| 15 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/fetch.py |
| 16 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/g0-probes.json |
| 17 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/g0-results.jsonl |
| 18 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/g0-run.py |
| 19 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/grading-results.jsonl |
| 20 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/make-sheet.py |
| 21 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/move-e141.py |
| 22 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/pool-raw.json |
| 23 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/screening-rows.json |
| 24 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/screening.jsonl |
| 25 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/threads-raw.json |
| 26 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/PROTOCOL.md |
| 27 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/RESULT.md |
| 28 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_a_raw.json |
| 29 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_a_unanswered.json |
| 30 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_b_raw.json |
| 31 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_b_unanswered.json |
| 32 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/attempt_sample.json |
| 33 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/attempts.jsonl |
| 34 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/fetch-log.json |
| 35 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/fetch.py |
| 36 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/fetch_threads.py |
| 37 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/g0_attempts.json |
| 38 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/g0_probes.json |
| 39 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/g0_probes.py |
| 40 | 21:13:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/g0_results.json |
| 91 | 21:13:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-021-document-continuation-decision-after-vie/events.jsonl |
| 92 | 21:13:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-022-run-view-count-principle-fresh-observati/events.jsonl |
| 93 | 21:13:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-023-declare-e162-experiment-artifacts-and-up/events.jsonl |
| 94 | 21:13:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-024-finalize-e162-experiment-and-update-miss/events.jsonl |
| 95 | 21:13:33 | unlogged_change | changed but never declared as an artifact: tasks/T-0094-run-a-fresh-observation-experiment-testing-the-view-count-principle.md |
| 96 | 21:13:33 | unlogged_change | changed but never declared as an artifact: tools/viewcount_experiment_module.py |
| 97 | 21:13:33 | unlogged_change | changed but never declared as an artifact: tools/viewcount_framework.py |
| 98 | 21:13:33 | unlogged_change | changed but never declared as an artifact: tools/vscode_adapter.py |
| 99 | 21:13:33 | unlogged_change | changed but never declared as an artifact: tools/vscode_experiment_module.py |
| 100 | 21:13:33 | session_end | Completed fresh observation experiment E151 testing the view-count principle on VS Code Marketplace (Open VSX). The Open VSX search API only returns t |

_50 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-025-run-a-fresh-observation-experiment-testi/events.jsonl
```
