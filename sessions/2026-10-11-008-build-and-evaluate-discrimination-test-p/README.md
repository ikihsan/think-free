# Session 2026-10-11-008-build-and-evaluate-discrimination-test-p

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T08:12:15+00:00
- **Duration:** 27.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Build and evaluate discrimination test prototype for view-count principle in aviation maintenance domain

## Summary

Built E093 discrimination test prototype in EXPERIMENTS/093-discrimination-test. Tested 3 instruments against hand-classified ground truth from E083 aviation maintenance experiment (30 statements: 0 served, 6 partially_served, 24 unserved). All instruments failed G2 (≥0.85 accuracy on 5 known-served + 5 known-unserved): v1 (subject mention + guide): 1/10 accuracy, v2 (subject + step-by-step/part-info): 1/10 accuracy, original keyword classifier: 3/10 accuracy (confirming F109/E088 finding of 0.70 actual experiment accuracy). Key finding: no tested instrument passes G2. Per D088/D095, route must be re-entered through a discrimination test that passes on labels known by construction, not through another domain screen. Do not start from classify_served over Bing in a new domain.

## Next

Consider alternative instrument designs or fresh observation in new domain per D083

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/093-discrimination-test | d481b0f95f9d | 15319 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 29 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/collect_practitioner_rows.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/deduplicate.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/measure_population.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/run_discrimination_test.py |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/results.json |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/run.py |
|   undeclared | EXPERIMENTS/09X-pyfix-prototype/prototype.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:12:15 | session_start | Build and evaluate discrimination test prototype for view-count principle in aviation maintenance domain |
| 2 | 08:12:21 | artifact | wrote EXPERIMENTS/093-discrimination-test |
| 3 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
| 4 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
| 5 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |
| 6 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/collect_practitioner_rows.py |
| 7 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/deduplicate.py |
| 8 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/measure_population.py |
| 9 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/run_discrimination_test.py |
| 10 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/results.json |
| 11 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/run.py |
| 12 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-pyfix-prototype/prototype.py |
| 13 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-cran-r-keyword-activity/results.json |
| 14 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-need-class/results.json |
| 15 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-star-activity/results.json |
| 16 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-import-error-need-class/results.json |
| 17 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-pypi-keyword-activity/results.json |
| 18 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-import-resolvability/results.json |
| 19 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 20 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 21 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/phase-decision.json |
| 22 | 08:12:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/synthesis-view-count-final.md |
| 23 | 08:12:42 | unlogged_change | changed but never declared as an artifact: pyprovides_classify.py |
| 24 | 08:12:42 | unlogged_change | changed but never declared as an artifact: raw/discrimination_test_results.json |
| 25 | 08:12:42 | unlogged_change | changed but never declared as an artifact: raw/population_measurement_results.json |
| 26 | 08:12:42 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows.jsonl |
| 27 | 08:12:42 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows_dedup.jsonl |
| 28 | 08:12:42 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-005-run-pyfix-prototype-and-view-count-hacke/events.jsonl |
| 29 | 08:12:42 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-006-fresh-observation-in-a-new-domain-per-d0/events.jsonl |
| 30 | 08:12:42 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-007-design-and-run-a-fresh-observation-exper/events.jsonl |
| 31 | 08:12:42 | unlogged_change | changed but never declared as an artifact: viewcount_crates.py |
| 32 | 08:12:42 | session_end | Built E093 discrimination test prototype in EXPERIMENTS/093-discrimination-test. Tested 3 instruments against hand-classified ground truth from E083 a |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-008-build-and-evaluate-discrimination-test-p/events.jsonl
```
