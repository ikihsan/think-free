# Session 2026-10-13-026-continue-preflight-line-prototype-adapte

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T10:19:19+00:00
- **Duration:** 1115.6s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Continue preflight line - prototype adapter for third harness

## Summary

E132: Ran baseline view-count experiment on 700 Rust GitHub repos using base v2 classifier. Key findings: coverage 31.1% (need=108, generic=110), G0 passes, G1 passes, G2 delta=0.0689 p=0.3776 (negligible), G3 delta=0.2170 p=0.0054 (highly significant). Comparison with prior ecosystems: JavaScript G3 p=0.7358 (not significant, opposite sign), Java G3 p=0.0333 (significant), Rust G3 p=0.0054 (highly significant, strongest effect). This maps the view-count principle's ecosystem-dependent boundary conditions: classification methodology is ecosystem-invariant (G0,G1 pass consistently), but arrival-count effect (G3) is ecosystem-dependent, strongest for Rust, intermediate for Java, absent for JavaScript. Experiment complete, records updated.

## Next

Update mission state records and determine continuation per D083

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 50 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/analyze.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/classify_test.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/full_analyze.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/harvest.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/raw_pool.json |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/test_label.py |
|   undeclared | EXPERIMENTS/131-viewcount-java-repos-matched-harvest/RESULTS.md |
|   undeclared | EXPERIMENTS/131-viewcount-java-repos-matched-harvest/baseline.py |
|   undeclared | EXPERIMENTS/131-viewcount-java-repos-matched-harvest/harvest.py |
|   undeclared | EXPERIMENTS/131-viewcount-java-repos-matched-harvest/raw_pool.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:19:19 | session_start | Continue preflight line - prototype adapter for third harness |
| 2 | 10:21:06 | milestone | Design E131 Java GitHub repos experiment with adapted classifier |
| 3 | 10:21:31 | milestone | E131: Prototype preflight adapter for new harness format (8th structure) |
| 4 | 10:23:47 | milestone | Integrate E136 eighth harness adapter into preflight prototype |
| 5 | 10:25:44 | milestone | E131: Java GitHub repos matched-harvest experiment with adapted classifier |
| 6 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/analyze.py |
| 7 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/classify_test.py |
| 8 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/full_analyze.py |
| 9 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/harvest.py |
| 10 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/raw_pool.json |
| 11 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/test_label.py |
| 12 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/RESULTS.md |
| 13 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/baseline.py |
| 14 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/harvest.py |
| 15 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/131-viewcount-java-repos-matched-harvest/raw_pool.json |
| 16 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/RESULTS.md |
| 17 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/baseline.py |
| 18 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/harvest.py |
| 19 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/raw_pool.json |
| 20 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/134-preflight-prototype |
| 21 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/PROTOCOL.md |
| 22 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/README.md |
| 23 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/RESULT.md |
| 24 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/adapter.py |
| 25 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/harness.json |
| 26 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/key/ground_truth.json |
| 27 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/output/model_results.json |
| 28 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/adapter.py |
| 29 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/key/ground_truth.json |
| 30 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/output/model_results.json |
| 31 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/results.json |
| 32 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/adapters_catalog.json |
| 33 | 10:37:55 | unlogged_change | changed but never declared as an artifact: EXTENSIONS/js_viewcount_classifier.py |
| 34 | 10:37:55 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 35 | 10:37:55 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 36 | 10:37:55 | unlogged_change | changed but never declared as an artifact: SESSION_SUMMARY.md |
| 37 | 10:37:55 | unlogged_change | changed but never declared as an artifact: STATE-in-flight-10.md |
| 38 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-012-finish-e130-experiment-and-validate-reco/commands.log |
| 39 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-012-finish-e130-experiment-and-validate-reco/events.jsonl |
| 40 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-013-record-decisions-records-md-artifact-and/events.jsonl |
| 47 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-020-finish-logging-remaining-artifacts/events.jsonl |
| 48 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-021-declare-all-remaining-experiment-artifac/events.jsonl |
| 49 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-022-declare-last-2-unlogged-artifacts/events.jsonl |
| 50 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-023-finish-session-with-experiment-artifacts/events.jsonl |
| 51 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-024-promote-preflight-to-public-product-stat/events.jsonl |
| 52 | 10:37:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-025-run-e130-view-count-classifier-experimen/events.jsonl |
| 53 | 10:37:55 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 54 | 10:37:55 | unlogged_change | changed but never declared as an artifact: tasks/T-0094-harvest-public-issue-trackers-and-practitioner-d.md |
| 55 | 10:37:55 | unlogged_change | changed but never declared as an artifact: tasks/T-0095-improve-preflight-usability-and-documentation.md |
| 56 | 10:37:55 | session_end | E132: Ran baseline view-count experiment on 700 Rust GitHub repos using base v2 classifier. Key findings: coverage 31.1% (need=108, generic=110), G0 p |

_6 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-026-continue-preflight-line-prototype-adapte/events.jsonl
```
