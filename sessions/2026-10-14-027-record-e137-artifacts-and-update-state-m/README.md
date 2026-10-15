# Session 2026-10-14-027-record-e137-artifacts-and-update-state-m

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T17:13:41+00:00
- **Duration:** 144.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Record E137 artifacts and update STATE.md with cross-model agreement result

## Summary

Recorded E137 artifacts and updated STATE.md and STATE-next-actions.md with cross-model agreement result. E137 completed: calibrated R1 instrument achieved third exact AGREE on math_chain_of_thought cell for 01-ai/yi-6b (437/437 row verdicts, macro diff 0.0). One yi-6b-specific calibration fix (backslash stripping only before letters). D111 stands. Next action: E138 on gsm cell (#### parser, single run).

## Next

E138: point calibrated instrument at gsm cell for parser stressor test

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/137-leaderboard-cross-model-agreement/PROTOCOL.md | 2f3e7b55d410 | 4629 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/RESULT.md | 9677f65b50af | 6774 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/fetch_cells_yi6b.py | 56fa3363e638 | 3126 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/fetched-manifest.json | 2cd6b98a1c00 | 15600 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/inventory.json | d75057e84559 | 157881 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/manifest.json | 3f6a57750597 | 18158 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/manifest_fetched_yi6b.py | f45a86095cd3 | 2238 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/recompute_math_out.json | e79344355e16 | 516 |
| EXPERIMENTS/137-leaderboard-cross-model-agreement/recompute_math_yi6b.py | f6dbeaac37e8 | 9800 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 69 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/073-viewcount-prototype-v3/results.json |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/results.json |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/collect.py |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/results.json |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:13:41 | session_start | Record E137 artifacts and update STATE.md with cross-model agreement result |
| 2 | 17:14:00 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/PROTOCOL.md |
| 3 | 17:14:01 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/RESULT.md |
| 4 | 17:14:02 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/fetch_cells_yi6b.py |
| 5 | 17:14:03 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/fetched-manifest.json |
| 6 | 17:14:04 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/inventory.json |
| 7 | 17:14:05 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/manifest.json |
| 8 | 17:14:05 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/manifest_fetched_yi6b.py |
| 9 | 17:14:06 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/recompute_math_out.json |
| 10 | 17:14:07 | artifact | wrote EXPERIMENTS/137-leaderboard-cross-model-agreement/recompute_math_yi6b.py |
| 11 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/073-viewcount-prototype-v3/results.json |
| 12 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
| 13 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
| 14 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 15 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 16 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/results.json |
| 17 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
| 18 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
| 19 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
| 20 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |
| 21 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collected_packages.jsonl |
| 22 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/pool_metadata.json |
| 23 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/results.json |
| 24 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/E137-decision.txt |
| 25 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_gsm_yi6b_result.json |
| 26 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 27 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137.json |
| 28 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/138-viewcount-comparison-analysis |
| 29 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/PROTOCOL.md |
| 30 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/RESULT.md |
| 31 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/evalscope_adapter.py |
| 32 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/predictions_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 33 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/reviews_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 34 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_f121_real.py |
| 35 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight.py |
| 36 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight_failure.py |
| 37 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E130-viewcount-classifier-prototype-v3/results_continuation.json |
| 38 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-viewcount-prototype/results.json |
| 39 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e139-cpan-experiment/continue_e139.py |
| 40 | 17:16:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e139-cpan-experiment/continue_e139b.py |
| 72 | 17:16:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-024-finalize-preflight-tool-release-document/events.jsonl |
| 73 | 17:16:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-run-preflight-against-real-modelscope-ev/commands.log |
| 74 | 17:16:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-run-preflight-against-real-modelscope-ev/events.jsonl |
| 75 | 17:16:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-026-run-e137-point-calibrated-instrument-at/events.jsonl |
| 76 | 17:16:05 | unlogged_change | changed but never declared as an artifact: think_free_test.py |
| 77 | 17:16:05 | unlogged_change | changed but never declared as an artifact: tools/viewcount_cli.py |
| 78 | 17:16:05 | unlogged_change | changed but never declared as an artifact: tools/viewcount_core.py |
| 79 | 17:16:05 | unlogged_change | changed but never declared as an artifact: tools/viewcount_prototype.py |
| 80 | 17:16:05 | doc_update | updated STATE.md |
| 81 | 17:16:05 | session_end | Recorded E137 artifacts and updated STATE.md and STATE-next-actions.md with cross-model agreement result. E137 completed: calibrated R1 instrument ach |

_31 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-027-record-e137-artifacts-and-update-state-m/events.jsonl
```
