# Session 2026-10-14-034-complete-preflight-release-verify-doc-li

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T21:10:03+00:00
- **Duration:** 11706.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Complete preflight release: verify doc lint, release check, and ensure README accurately describes preflight

## Summary

Verified the preflight release gates on the current tree: full stdlib suite 837 tests, doc lint exit 0, release check exit 0. Found and repaired one real check weakening carried in the uncommitted tree: four new 'exempt: EXPERIMENTS/**/raw/*.json[l]' lines in vendor/MANIFEST.md were unnecessary (the cap's data-suffix exemption already covers them, so release check skipped them either way) but they made is_declared_exempt true for those paths, which is the question session finish reconciliation asks. Two recorded tests were red as a result. Removed the four lines; both tests and release check green again. Still unlanded: 26 session records and 5 experiment directories from sessions 009-033.

## Next

Land the uncommitted tree (sessions 009-033 records, EXPERIMENTS/117, 138, 139, 140, e139-cpan), then close D111 for the preflight line and pivot to a scorer false-negative measurement on the already-fetched HELM math rows.

## Artifacts

_none_

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['tools/origin', 'doc', 'lint'] | 0 | 190490 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 94 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | .pyprovides-ranked.json |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/results.json |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/collect.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:10:03 | session_start | Complete preflight release: verify doc lint, release check, and ensure README accurately describes preflight |
| 2 | 21:13:23 | command | $ tools/origin doc lint |
| 3 | 00:25:09 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 4 | 00:25:09 | unlogged_change | changed but never declared as an artifact: .pyprovides-ranked.json |
| 5 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
| 6 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
| 7 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 8 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 9 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
| 10 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
| 11 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
| 12 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |
| 13 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/E137-decision.txt |
| 14 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md |
| 15 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_gsm_yi6b_result.json |
| 16 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 17 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137.json |
| 18 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/138-viewcount-comparison-analysis |
| 19 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/PROTOCOL.md |
| 20 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/RESULT.md |
| 21 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/evalscope_adapter.py |
| 22 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/predictions_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 23 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/reviews_dir/qwen-7b/mmlu_abstract_algebra.jsonl |
| 24 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_f121_real.py |
| 25 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight.py |
| 26 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/test_preflight_failure.py |
| 27 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-github-actions-ci-failures/CLASSIFICATION_RULES.md |
| 28 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E130-viewcount-classifier-prototype-v3/results_continuation.json |
| 29 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-viewcount-prototype/results.json |
| 30 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e139-cpan-experiment/continue_e139.py |
| 31 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e139-cpan-experiment/continue_e139b.py |
| 32 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 33 | 00:25:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/preflight-adoption-interest.md |
| 34 | 00:25:09 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-experiments.md |
| 35 | 00:25:09 | unlogged_change | changed but never declared as an artifact: MISSION-OUTCOME.json |
| 36 | 00:25:09 | unlogged_change | changed but never declared as an artifact: NEXT-STEPS-SUMMARY.md |
| 37 | 00:25:09 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 38 | 00:25:09 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.json |
| 39 | 00:25:09 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 40 | 00:25:09 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOMES.json |
| 88 | 00:25:09 | unlogged_change | changed but never declared as an artifact: test_preflight_adapter.py |
| 89 | 00:25:09 | unlogged_change | changed but never declared as an artifact: test_preflight_adapter_success.py |
| 90 | 00:25:09 | unlogged_change | changed but never declared as an artifact: tools/originlib/docfiles.py |
| 91 | 00:25:09 | unlogged_change | changed but never declared as an artifact: tools/originlib/release.py |
| 92 | 00:25:09 | unlogged_change | changed but never declared as an artifact: tools/viewcount_cli.py |
| 93 | 00:25:09 | unlogged_change | changed but never declared as an artifact: tools/viewcount_core.py |
| 94 | 00:25:09 | unlogged_change | changed but never declared as an artifact: tools/viewcount_prototype.py |
| 95 | 00:25:09 | unlogged_change | changed but never declared as an artifact: vendor/MANIFEST.md |
| 96 | 00:25:09 | unlogged_change | changed but never declared as an artifact: viewcount_crates.py |
| 97 | 00:25:10 | session_end | Verified the preflight release gates on the current tree: full stdlib suite 837 tests, doc lint exit 0, release check exit 0. Found and repaired one r |

_47 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-034-complete-preflight-release-verify-doc-li/events.jsonl
```
