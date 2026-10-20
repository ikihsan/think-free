# Session 2026-10-14-028-e138-run-r1-recomputation-on-helm-lite-v

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T17:21:41+00:00
- **Duration:** 885.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E138: Run R1 recomputation on HELM lite v1.0.0 gsm cell for yi-34b, exercising #### number-extraction parser on free-text completions

## Summary

E138 completed: R1 recomputation on HELM lite v1.0.0 GSM cell for yi-34b achieved exact AGREE (0.648000 vs 0.648, diff 0.0) with 1000/1000 row-level agreement. The #### number-extraction parser stressor was exercised via fallback (last number in text) on 1000/1000 rows since HELM's GSM8K format lacks #### markers. This is the fourth exact AGREE on the leaderboard reach line (E135: single-letter, E136: math free-text aggregate with weighting, E137: cross-model, E138: GSM #### parser). Kill gate not fired; D111 stands (reach demonstrated further, external value still unobserved).

## Next

Decide whether to continue leaderboard reach testing on other leaderboards (C1/C3 failed G2 at probe time) or accept D111 as final state and pivot to preflight release decision (Option C: document and release with limitations per STATE-next-actions.md recommendation).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md | 3dfa45c1af79 | 5604 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 71 |
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
| 1 | 17:21:41 | session_start | E138: Run R1 recomputation on HELM lite v1.0.0 gsm cell for yi-34b, exercising #### number-extraction parser on free-text completions |
| 2 | 17:33:02 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md |
| 3 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/073-viewcount-prototype-v3/results.json |
| 4 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
| 5 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
| 6 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 7 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 8 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/results.json |
| 9 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
| 10 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
| 11 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
| 12 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |
| 13 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collected_packages.jsonl |
| 14 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/pool_metadata.json |
| 15 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/results.json |
| 16 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/E137-decision.txt |
| 17 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_gsm_yi6b_result.json |
| 18 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 19 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137.json |
| 20 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_gsm.py |
| 21 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/138-viewcount-comparison-analysis |
| 22 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/PROTOCOL.md |
| 23 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/RESULT.md |
| 24 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/evalscope_adapter.py |
| 25 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/predictions_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 26 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/reviews_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 27 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_f121_real.py |
| 28 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight.py |
| 29 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight_failure.py |
| 30 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E130-viewcount-classifier-prototype-v3/results_continuation.json |
| 31 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-viewcount-prototype/results.json |
| 32 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e139-cpan-experiment/continue_e139.py |
| 33 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e139-cpan-experiment/continue_e139b.py |
| 34 | 17:36:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 35 | 17:36:26 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-experiments.md |
| 36 | 17:36:26 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.json |
| 37 | 17:36:26 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 38 | 17:36:26 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 39 | 17:36:26 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 40 | 17:36:26 | unlogged_change | changed but never declared as an artifact: collected_packages.jsonl |
| 66 | 17:36:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-run-preflight-against-real-modelscope-ev/commands.log |
| 67 | 17:36:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-run-preflight-against-real-modelscope-ev/events.jsonl |
| 68 | 17:36:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-026-run-e137-point-calibrated-instrument-at/events.jsonl |
| 69 | 17:36:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-027-record-e137-artifacts-and-update-state-m/events.jsonl |
| 70 | 17:36:26 | unlogged_change | changed but never declared as an artifact: think_free_test.py |
| 71 | 17:36:26 | unlogged_change | changed but never declared as an artifact: tools/viewcount_cli.py |
| 72 | 17:36:26 | unlogged_change | changed but never declared as an artifact: tools/viewcount_core.py |
| 73 | 17:36:26 | unlogged_change | changed but never declared as an artifact: tools/viewcount_prototype.py |
| 74 | 17:36:26 | doc_update | updated STATE.md |
| 75 | 17:36:26 | session_end | E138 completed: R1 recomputation on HELM lite v1.0.0 GSM cell for yi-34b achieved exact AGREE (0.648000 vs 0.648, diff 0.0) with 1000/1000 row-level a |

_25 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-028-e138-run-r1-recomputation-on-helm-lite-v/events.jsonl
```
