# Session 2026-10-11-012-log-experiment-094-artifacts-and-update

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T09:49:51+00:00
- **Duration:** 438.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Log Experiment 094 artifacts and update STATE documents with results

## Summary

Logged Experiment 094 artifacts (README.md, run.py, results.json, classification.log.json) and updated STATE-next-actions.md with E094 results. E094 tested view-count principle on Kubernetes Discourse forum: G2 PASS (view-count separation p=0.044), G1 FAIL (76 error, 93 non-error < 100), G3 FAIL (unserved 75% CI95 [64%, 83%] >> Discourse baseline 11-15%), G4 PASS (100% view coverage). Key finding: view-count separation effect generalizes to software-focused Discourse, but unserved fraction is drastically higher than other Discourse forums, suggesting community dynamics dominate the unserved metric.

## Next

Per D083, next session must start fresh observation in a new domain not yet tested. Consider: (1) ROS (Robot Operating System) Discourse forum, (2) PostgreSQL/DBA Stack Exchange, (3) Unity/Unreal game engine forums, (4) Docker/container error forums, (5) AWS/Azure/GCP cloud service error forums. Must avoid re-entering domains already covered.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/094-k8s-discourse-viewcount/README.md | 4cca80ab9936 | 6128 |
| EXPERIMENTS/094-k8s-discourse-viewcount/run.py | c99e01a27555 | 14896 |
| EXPERIMENTS/094-k8s-discourse-viewcount/results.json | 9e655f0cabf4 | 1444 |
| EXPERIMENTS/094-k8s-discourse-viewcount/classification.log.json | 33d8138ccd02 | 144223 |
| STATE-next-actions.md | 5cbbbcc3a033 | 18333 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 42 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
|   undeclared | EXPERIMENTS/090-maven-view-count/PROTOCOL.md |
|   undeclared | EXPERIMENTS/090-maven-view-count/README.md |
|   undeclared | EXPERIMENTS/090-maven-view-count/pom_utils.py |
|   undeclared | EXPERIMENTS/090-maven-view-count/probe.py |
|   undeclared | EXPERIMENTS/090-maven-view-count/raw/probe.json |
|   undeclared | EXPERIMENTS/090-maven-view-count/raw/results.json |
|   undeclared | EXPERIMENTS/093-discrimination-test |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:49:51 | session_start | Log Experiment 094 artifacts and update STATE documents with results |
| 2 | 09:50:00 | artifact | wrote EXPERIMENTS/094-k8s-discourse-viewcount/README.md |
| 3 | 09:50:04 | artifact | wrote EXPERIMENTS/094-k8s-discourse-viewcount/run.py |
| 4 | 09:50:10 | artifact | wrote EXPERIMENTS/094-k8s-discourse-viewcount/results.json |
| 5 | 09:50:15 | artifact | wrote EXPERIMENTS/094-k8s-discourse-viewcount/classification.log.json |
| 6 | 09:56:59 | artifact | wrote STATE-next-actions.md |
| 7 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
| 8 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/PROTOCOL.md |
| 9 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/README.md |
| 10 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/pom_utils.py |
| 11 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/probe.py |
| 12 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/raw/probe.json |
| 13 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/raw/results.json |
| 14 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-discrimination-test |
| 15 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
| 16 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |
| 17 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/collect_practitioner_rows.py |
| 18 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/deduplicate.py |
| 19 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/measure_population.py |
| 20 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/run_discrimination_test.py |
| 21 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/results.json |
| 22 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/run.py |
| 23 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-pyfix-prototype/prototype.py |
| 24 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-cran-r-keyword-activity/results.json |
| 25 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-need-class/results.json |
| 26 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-star-activity/results.json |
| 27 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-import-error-need-class/results.json |
| 28 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-pypi-keyword-activity/results.json |
| 29 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-import-resolvability/results.json |
| 30 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 31 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 32 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/phase-decision.json |
| 33 | 09:57:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/synthesis-view-count-final.md |
| 34 | 09:57:09 | unlogged_change | changed but never declared as an artifact: pyprovides_classify.py |
| 35 | 09:57:09 | unlogged_change | changed but never declared as an artifact: raw/discrimination_test_results.json |
| 36 | 09:57:09 | unlogged_change | changed but never declared as an artifact: raw/population_measurement_results.json |
| 37 | 09:57:09 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows.jsonl |
| 38 | 09:57:09 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows_dedup.jsonl |
| 39 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-005-run-pyfix-prototype-and-view-count-hacke/events.jsonl |
| 40 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-006-fresh-observation-in-a-new-domain-per-d0/events.jsonl |
| 41 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-007-design-and-run-a-fresh-observation-exper/events.jsonl |
| 42 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-008-build-and-evaluate-discrimination-test-p/events.jsonl |
| 43 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-009-run-a-fresh-observation-experiment-in-a/commands.log |
| 44 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-009-run-a-fresh-observation-experiment-in-a/events.jsonl |
| 45 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-010-record-e090-maven-central-experiment-res/events.jsonl |
| 46 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-011-design-and-run-a-fresh-observation-exper/commands.log |
| 47 | 09:57:09 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-011-design-and-run-a-fresh-observation-exper/events.jsonl |
| 48 | 09:57:09 | unlogged_change | changed but never declared as an artifact: viewcount_crates.py |
| 49 | 09:57:09 | session_end | Logged Experiment 094 artifacts (README.md, run.py, results.json, classification.log.json) and updated STATE-next-actions.md with E094 results. E094 t |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-012-log-experiment-094-artifacts-and-update/events.jsonl
```
