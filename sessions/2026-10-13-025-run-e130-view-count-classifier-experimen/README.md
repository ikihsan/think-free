# Session 2026-10-13-025-run-e130-view-count-classifier-experimen

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T10:02:29+00:00
- **Duration:** 26.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Run E130 view-count classifier experiment on JavaScript GitHub repositories with matched harvest design

## Summary

E130: Ran matched-harvest view-count experiment on 700 JavaScript GitHub repos using v2 classifier. Key findings: coverage 30% (need=95, generic=115, unlabelled=490), G0 passes (planted positive recovery), G1 fails (need<100 although generic≥100), G2 delta=0.0486 p=0.539 (negligible effect), G3 stars/year p=0.0846 (suggestive but not significant). Comparison with E113 Python: weaker effect and lower coverage on JS repos, indicating classifier vocabulary is ecosystem-specific. This closes the JavaScript GitHub repos domain for the view-count principle with the current classifier.

## Next

Consider whether to adapt classifier for JavaScript terminology or pursue a completely new domain per D083

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 37 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/analyze.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/harvest.py |
|   undeclared | EXPERIMENTS/130-viewcount-js-repos-matched-harvest/raw_pool.json |
|   undeclared | EXPERIMENTS/134-preflight-prototype |
|   undeclared | EXPERIMENTS/135-preflight-seventh-harness/PROTOCOL.md |
|   undeclared | EXPERIMENTS/135-preflight-seventh-harness/README.md |
|   undeclared | EXPERIMENTS/135-preflight-seventh-harness/RESULT.md |
|   undeclared | EXPERIMENTS/135-preflight-seventh-harness/adapter.py |
|   undeclared | EXPERIMENTS/135-preflight-seventh-harness/harness.json |
|   undeclared | EXPERIMENTS/135-preflight-seventh-harness/key/ground_truth.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:02:29 | session_start | Run E130 view-count classifier experiment on JavaScript GitHub repositories with matched harvest design |
| 2 | 10:02:36 | milestone | E130 JavaScript repos experiment complete: v2 classifier labels 30% of JS repo descriptions (vs 38.2% on Python), G0 passes, G1 fails, G2 delta neglig |
| 3 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/analyze.py |
| 4 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/harvest.py |
| 5 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/130-viewcount-js-repos-matched-harvest/raw_pool.json |
| 6 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/134-preflight-prototype |
| 7 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/PROTOCOL.md |
| 8 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/README.md |
| 9 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/RESULT.md |
| 10 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/adapter.py |
| 11 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/harness.json |
| 12 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/key/ground_truth.json |
| 13 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-seventh-harness/output/model_results.json |
| 14 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/adapter.py |
| 15 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/key/ground_truth.json |
| 16 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/output/model_results.json |
| 17 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E136-preflight-eighth-harness/results.json |
| 18 | 10:02:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/adapters_catalog.json |
| 19 | 10:02:55 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 20 | 10:02:55 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOME.md |
| 21 | 10:02:55 | unlogged_change | changed but never declared as an artifact: SESSION_SUMMARY.md |
| 22 | 10:02:55 | unlogged_change | changed but never declared as an artifact: STATE-in-flight-10.md |
| 23 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-012-finish-e130-experiment-and-validate-reco/commands.log |
| 24 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-012-finish-e130-experiment-and-validate-reco/events.jsonl |
| 25 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-013-record-decisions-records-md-artifact-and/events.jsonl |
| 26 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-014-identify-next-invention-direction-after/events.jsonl |
| 27 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-015-declare-session-artifacts-from-previous/events.jsonl |
| 28 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-016-preflight-adapter-prototyping-and-releas/events.jsonl |
| 29 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-017-record-preflight-session-artifacts/events.jsonl |
| 30 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-018-continue-preflight-adapter-pattern-to-7/events.jsonl |
| 31 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-019-declare-artifacts-from-preflight-line-co/events.jsonl |
| 32 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-020-finish-logging-remaining-artifacts/events.jsonl |
| 33 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-021-declare-all-remaining-experiment-artifac/events.jsonl |
| 34 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-022-declare-last-2-unlogged-artifacts/events.jsonl |
| 35 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-023-finish-session-with-experiment-artifacts/events.jsonl |
| 36 | 10:02:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-13-024-promote-preflight-to-public-product-stat/events.jsonl |
| 37 | 10:02:55 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 38 | 10:02:55 | unlogged_change | changed but never declared as an artifact: tasks/T-0094-harvest-public-issue-trackers-and-practitioner-d.md |
| 39 | 10:02:55 | unlogged_change | changed but never declared as an artifact: tasks/T-0095-improve-preflight-usability-and-documentation.md |
| 40 | 10:02:55 | session_end | E130: Ran matched-harvest view-count experiment on 700 JavaScript GitHub repos using v2 classifier. Key findings: coverage 30% (need=95, generic=115,  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-025-run-e130-view-count-classifier-experimen/events.jsonl
```
