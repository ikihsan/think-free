# Session 2026-10-11-002-restore-a-green-doc-lint-so-work-can-lan

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T00:38:12+00:00
- **Duration:** 2649.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Restore a green doc lint so work can land, then test whether a local-state import diagnosis beats the strongest accessible alternative on real failures

## Summary

Doc lint restored to exit 0 by splitting 3 oversized experiment scripts by invariant, un-namespacing an archived summary, and fixing 2 repo-escaping links; committed as b82bbcec. The session's second half (local-state import diagnosis vs the strongest alternative) is superseded: D102/F113 closed the package-name line on demand (0.23-0.47%, under the 1% gate), so the head-to-head has no population to measure.

## Next

Run the E091 Anova answerability replication, which recorded a false infrastructure block: its protocol accepts 'GPT-4o, Claude 3.5 Sonnet, or equivalent' and the mission's own instrument for E062/E066 is the reading model itself.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| SESSION_OUTCOME.md | 6258c55501c6 | 5388 |
| EXPERIMENTS/091-discrimination-instrument.py | 79c5cbaedd26 | 7854 |
| EXPERIMENTS/091-mrplc-parsers.py | 5b6ae0e7458c | 8675 |
| EXPERIMENTS/091-mrplc-fetch.py | 7f73f4be6e0e | 2630 |
| EXPERIMENTS/091-probe-sets.py | 50efc067b9e9 | 4541 |
| EXPERIMENTS/091-vendor-unsure-recurrence/baseline_threads.py | 816fdc174c8c | 3801 |
| EXPERIMENTS/092-comparison-forum-vs-websearch/e092_rubric.py | 794b61520d84 | 3028 |
| EXPERIMENTS/092-comparison-forum-vs-websearch/e092_rows.py | 745425d0c31a | 3235 |
| STATE-next-actions.md | b8137cfa7776 | 9642 |
| NEXT-STEPS-SUMMARY.md | 676ec428ded5 | 7700 |
| EXPERIMENTS/085-declared-not-provided/README.md | 3971333e50e2 | 10319 |
| EXPERIMENTS/091-discrimination-harness.py | fe7869922b5a | 10068 |
| EXPERIMENTS/091-vendor-unsure-recurrence/run_measurement.py | b1767e46e875 | 8411 |
| EXPERIMENTS/092-comparison-forum-vs-websearch/compare_data_formats.py | dd0f0e34e889 | 19259 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['python3', '/tmp/opencode/add_meta.py', 'EXPERIMENTS/091-vendor-unsure-recurrence/OBSERVATIONS.md', 'EXPERIMENTS/091-vendor-unsure-recurrence/RESULTS | 0 | 125 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 21 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-18.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/091-import-error-population/README.md |
|   undeclared | EXPERIMENTS/091-import-error-population/REREAD.md |
|   undeclared | EXPERIMENTS/091-import-error-population/reread.json |
|   undeclared | EXPERIMENTS/091-import-error-population/results.json |
|   undeclared | EXPERIMENTS/091-vendor-unsure-recurrence/OBSERVATIONS.md |
|   undeclared | EXPERIMENTS/091-vendor-unsure-recurrence/RESULTS.md |
|   undeclared | EXPERIMENTS/092-comparison-forum-vs-websearch/DISCRIMINATION_TEST.md |
|   undeclared | EXPERIMENTS/092-comparison-forum-vs-websearch/OBSERVATIONS.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:38:12 | session_start | Restore a green doc lint so work can land, then test whether a local-state import diagnosis beats the strongest accessible alternative on real failure |
| 2 | 00:38:17 | artifact | wrote SESSION_OUTCOME.md |
| 3 | 00:38:20 | milestone | Session started on instance-20260717-0947; baseline doc lint has 18 pre-existing violations that blocked session 001 from landing |
| 4 | 00:40:48 | command | $ python3 /tmp/opencode/add_meta.py EXPERIMENTS/091-vendor-unsure-recurrence/OBSERVATIONS.md EXPERIMENTS/091-vendor-unsure-recurrence/RESULTS. |
| 5 | 00:55:17 | milestone | doc lint green (exit 0): split 3 oversized experiment scripts by invariant, fixed 2 repo-escaping links, adopted the E085 orphan CLOSURE.md from its R |
| 6 | 01:11:51 | artifact | wrote EXPERIMENTS/091-discrimination-instrument.py |
| 7 | 01:11:52 | artifact | wrote EXPERIMENTS/091-mrplc-parsers.py |
| 8 | 01:11:54 | artifact | wrote EXPERIMENTS/091-mrplc-fetch.py |
| 9 | 01:11:55 | artifact | wrote EXPERIMENTS/091-probe-sets.py |
| 10 | 01:11:56 | artifact | wrote EXPERIMENTS/091-vendor-unsure-recurrence/baseline_threads.py |
| 11 | 01:11:57 | artifact | wrote EXPERIMENTS/092-comparison-forum-vs-websearch/e092_rubric.py |
| 12 | 01:11:58 | artifact | wrote EXPERIMENTS/092-comparison-forum-vs-websearch/e092_rows.py |
| 13 | 01:11:59 | artifact | wrote STATE-next-actions.md |
| 14 | 01:12:00 | artifact | wrote NEXT-STEPS-SUMMARY.md |
| 15 | 01:12:01 | artifact | wrote EXPERIMENTS/085-declared-not-provided/README.md |
| 16 | 01:12:02 | artifact | wrote EXPERIMENTS/091-discrimination-harness.py |
| 17 | 01:12:03 | artifact | wrote EXPERIMENTS/091-vendor-unsure-recurrence/run_measurement.py |
| 18 | 01:12:04 | artifact | wrote EXPERIMENTS/092-comparison-forum-vs-websearch/compare_data_formats.py |
| 19 | 01:12:05 | milestone | split 3 experiment scripts by invariant (5+2+1 new modules), renamed DECISIONS-NEXT-STEPS.md to NEXT-STEPS-SUMMARY.md (fixes the one red test), fixed  |
| 20 | 01:22:21 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-18.md |
| 21 | 01:22:21 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 22 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/README.md |
| 23 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/REREAD.md |
| 24 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/reread.json |
| 25 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/results.json |
| 26 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-vendor-unsure-recurrence/OBSERVATIONS.md |
| 27 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-vendor-unsure-recurrence/RESULTS.md |
| 28 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/DISCRIMINATION_TEST.md |
| 29 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/OBSERVATIONS.md |
| 30 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/RESULTS.md |
| 31 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-fresh-observation-lab-instrument-errors/DISCRIMINATION_TEST.md |
| 32 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-fresh-observation-lab-instrument-errors/OBSERVATIONS.md |
| 33 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-fresh-observation-lab-instrument-errors/RESULTS.md |
| 34 | 01:22:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-aviation-discrimination-test/VERDICT.md |
| 35 | 01:22:21 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-37.md |
| 36 | 01:22:21 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 37 | 01:22:21 | unlogged_change | changed but never declared as an artifact: README.md |
| 38 | 01:22:21 | unlogged_change | changed but never declared as an artifact: SUMMARY_EXPERIMENT_OVERVIEW.md |
| 39 | 01:22:21 | unlogged_change | changed but never declared as an artifact: THINK_FREE_SUMMARY.md |
| 40 | 01:22:21 | unlogged_change | changed but never declared as an artifact: pyprovides/README.md |
| 41 | 01:22:22 | doc_update | updated DECISIONS-SCREENING-18.md |
| 42 | 01:22:22 | doc_update | updated DECISIONS.md |
| 43 | 01:22:22 | doc_update | updated FAILURES.md |
| 44 | 01:22:22 | session_end | Doc lint restored to exit 0 by splitting 3 oversized experiment scripts by invariant, un-namespacing an archived summary, and fixing 2 repo-escaping l |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-002-restore-a-green-doc-lint-so-work-can-lan/events.jsonl
```
