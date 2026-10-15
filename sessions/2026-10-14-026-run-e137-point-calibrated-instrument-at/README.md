# Session 2026-10-14-026-run-e137-point-calibrated-instrument-at

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T16:55:51+00:00
- **Duration:** 997.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run E137: point calibrated instrument at second model's math_chain_of_thought cell for cross-model agreement

## Summary

E137 completed successfully. The calibrated R1 recomputation instrument (last-\boxed extraction, normalized-string equality, macro-mean-of-subject-means weighting) achieved exact AGREE on a second model's math_chain_of_thought cell (01-ai/yi-6b) in HELM lite v1.0.0: 437/437 row verdicts agree with harness, recomputed macro mean equals published macro mean (0.12585197340399298, diff 0.0). This is the third exact AGREE on the leaderboard reach line (E135: MMLU single-letter; E136: math_chain_of_thought yi-34b with parser+weighting stress; E137: math_chain_of_thought yi-6b cross-model). Cross-model agreement is now tested. D111 stands (reach demonstrated further, external value still unobserved). Named next action: E138 on the gsm cell (#### parser, single run).

## Next

E138: point calibrated instrument at gsm cell (free-text, #### parser, single run) for parser stressor test

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 77 |
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
| 1 | 16:55:51 | session_start | Run E137: point calibrated instrument at second model's math_chain_of_thought cell for cross-model agreement |
| 2 | 17:12:06 | milestone | E137 completed: cross-model agreement on math_chain_of_thought cell for yi-6b (437/437 row verdicts, macro diff 0.0) |
| 3 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/073-viewcount-prototype-v3/results.json |
| 4 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
| 5 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
| 6 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 7 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 8 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/results.json |
| 9 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
| 10 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
| 11 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
| 12 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |
| 13 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collected_packages.jsonl |
| 14 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/pool_metadata.json |
| 15 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/results.json |
| 16 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/E137-decision.txt |
| 17 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_gsm_yi6b_result.json |
| 18 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 19 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137.json |
| 20 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/PROTOCOL.md |
| 21 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/RESULT.md |
| 22 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/fetch_cells_yi6b.py |
| 23 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/fetched-manifest.json |
| 24 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/inventory.json |
| 25 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/manifest.json |
| 26 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/manifest_fetched_yi6b.py |
| 27 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/recompute_math_out.json |
| 28 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/137-leaderboard-cross-model-agreement/recompute_math_yi6b.py |
| 29 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/138-viewcount-comparison-analysis |
| 30 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/PROTOCOL.md |
| 31 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/RESULT.md |
| 32 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/evalscope_adapter.py |
| 33 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/predictions_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 34 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/reviews_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 35 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_f121_real.py |
| 36 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight.py |
| 37 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight_failure.py |
| 38 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E130-viewcount-classifier-prototype-v3/results_continuation.json |
| 39 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-viewcount-prototype/results.json |
| 40 | 17:12:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e139-cpan-experiment/continue_e139.py |
| 72 | 17:12:28 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-023-prepare-preflight-tool-for-public-releas/events.jsonl |
| 73 | 17:12:28 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-024-finalize-preflight-tool-release-document/events.jsonl |
| 74 | 17:12:28 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-run-preflight-against-real-modelscope-ev/commands.log |
| 75 | 17:12:28 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-run-preflight-against-real-modelscope-ev/events.jsonl |
| 76 | 17:12:28 | unlogged_change | changed but never declared as an artifact: think_free_test.py |
| 77 | 17:12:28 | unlogged_change | changed but never declared as an artifact: tools/viewcount_cli.py |
| 78 | 17:12:28 | unlogged_change | changed but never declared as an artifact: tools/viewcount_core.py |
| 79 | 17:12:28 | unlogged_change | changed but never declared as an artifact: tools/viewcount_prototype.py |
| 80 | 17:12:29 | doc_update | updated STATE.md |
| 81 | 17:12:29 | session_end | E137 completed successfully. The calibrated R1 recomputation instrument (last-\boxed extraction, normalized-string equality, macro-mean-of-subject-mea |

_31 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-026-run-e137-point-calibrated-instrument-at/events.jsonl
```
