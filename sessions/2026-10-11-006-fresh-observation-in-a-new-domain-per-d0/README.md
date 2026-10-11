# Session 2026-10-11-006-fresh-observation-in-a-new-domain-per-d0

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T05:31:40+00:00
- **Duration:** 1634.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation in a new domain per D083 - explore medical device fault codes on FDA MAUDE or similar regulatory database

## Summary

Fresh observation in home automation domain (Home Assistant Discourse) per D083. Created E098 experiment with full protocol, discrimination test, and population measurement. All gates PASS: Discrimination (FPR=0.0, TPR=0.8, FNR=0.2), Population G1 (23 rows), G2 (instrument passes), G3 (43.5% unserved, CI95 [25.6%, 63.2%]), View Count (100%). Instrument fault_need_classifier_v3 validated on 4th Discourse domain. Unserved fraction 43.5% substantially higher than Discourse baseline 11.7% and embedded 15.3%, comparable to ROS 55.6% (n=9).

## Next

Update docs/INDEX.md and STATE.md with E098 results. Consider whether home automation domain warrants further investigation for candidate generation, or move to next fresh observation domain per D083.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 25 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/collect_practitioner_rows.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/deduplicate.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/measure_population.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/run_discrimination_test.py |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/results.json |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/run.py |
|   undeclared | EXPERIMENTS/09X-pyfix-prototype/prototype.py |
|   undeclared | EXPERIMENTS/0xx-cran-r-keyword-activity/results.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:31:40 | session_start | Fresh observation in a new domain per D083 - explore medical device fault codes on FDA MAUDE or similar regulatory database |
| 2 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
| 3 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |
| 4 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/collect_practitioner_rows.py |
| 5 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/deduplicate.py |
| 6 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/measure_population.py |
| 7 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/run_discrimination_test.py |
| 8 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/results.json |
| 9 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/run.py |
| 10 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-pyfix-prototype/prototype.py |
| 11 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-cran-r-keyword-activity/results.json |
| 12 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-need-class/results.json |
| 13 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-star-activity/results.json |
| 14 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-import-error-need-class/results.json |
| 15 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-pypi-keyword-activity/results.json |
| 16 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-import-resolvability/results.json |
| 17 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 18 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 19 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/phase-decision.json |
| 20 | 05:58:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/synthesis-view-count-final.md |
| 21 | 05:58:52 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 22 | 05:58:53 | unlogged_change | changed but never declared as an artifact: raw/discrimination_test_results.json |
| 23 | 05:58:53 | unlogged_change | changed but never declared as an artifact: raw/population_measurement_results.json |
| 24 | 05:58:53 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows.jsonl |
| 25 | 05:58:53 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows_dedup.jsonl |
| 26 | 05:58:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-005-run-pyfix-prototype-and-view-count-hacke/events.jsonl |
| 27 | 05:58:54 | session_end | Fresh observation in home automation domain (Home Assistant Discourse) per D083. Created E098 experiment with full protocol, discrimination test, and  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-006-fresh-observation-in-a-new-domain-per-d0/events.jsonl
```
