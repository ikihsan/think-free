# Session 2026-10-11-011-design-and-run-a-fresh-observation-exper

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T09:30:59+00:00
- **Duration:** 1105.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Design and run a fresh observation experiment in a new domain per D083 - testing view-count principle on Kubernetes error codes via Discourse forum

## Summary

Ran Experiment 094 testing view-count principle on Kubernetes Discourse forum (discuss.kubernetes.io). Fetched 500 topics from General Discussions category, classified 76 as error-related and 93 as non-error. G1 (population ≥100 each) FAILED - keyword rules too narrow (328 unclassified). G2 (view-count separation) PASSED - error topics have higher median views (282.5 vs 180), MWU p=0.044. G3 (unserved fraction CI95 upper <60%) FAILED - error unserved fraction 75% (CI95 [64%, 83%]), far above Discourse baseline of 11-15%. G4 (view-count coverage) PASSED at 100%. The view-count separation effect generalizes but forum dynamics differ drastically - most topics go unanswered.

## Next

Analyze why unserved fraction is so high on Kubernetes Discourse vs other Discourse forums. Consider expanding classification keywords to capture more error topics, or test a different Discourse forum with more active answering culture.

## Artifacts

_none_

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['tools/origin', 'session', 'step', 'Experiment 094 completed: G1 FAIL (76 error, 93 non-error), G2 PASS (p=0.044), G3 FAIL (75% unserved), G4 PASS. V | 0 | 1217 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 45 |
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
|   undeclared | EXPERIMENTS/094-k8s-discourse-viewcount/README.md |
|   undeclared | EXPERIMENTS/094-k8s-discourse-viewcount/classification.log.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:30:59 | session_start | Design and run a fresh observation experiment in a new domain per D083 - testing view-count principle on Kubernetes error codes via Discourse forum |
| 2 | 09:49:10 | milestone | Experiment 094 completed: G1 FAIL (76 error, 93 non-error), G2 PASS (p=0.044), G3 FAIL (75% unserved), G4 PASS. View-count separation holds but unserv |
| 3 | 09:49:11 | command | $ tools/origin session step Experiment 094 completed: G1 FAIL (76 error, 93 non-error), G2 PASS (p=0.044), G3 FAIL (75% unserved), G4 PASS. Vi |
| 4 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
| 5 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/PROTOCOL.md |
| 6 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/README.md |
| 7 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/pom_utils.py |
| 8 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/probe.py |
| 9 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/raw/probe.json |
| 10 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-maven-view-count/raw/results.json |
| 11 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-discrimination-test |
| 12 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/094-k8s-discourse-viewcount/README.md |
| 13 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/094-k8s-discourse-viewcount/classification.log.json |
| 14 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/094-k8s-discourse-viewcount/results.json |
| 15 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/094-k8s-discourse-viewcount/run.py |
| 16 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
| 17 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |
| 18 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/collect_practitioner_rows.py |
| 19 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/deduplicate.py |
| 20 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/measure_population.py |
| 21 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-home-assistant-fresh/run_discrimination_test.py |
| 22 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/results.json |
| 23 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/run.py |
| 24 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-pyfix-prototype/prototype.py |
| 25 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-cran-r-keyword-activity/results.json |
| 26 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-need-class/results.json |
| 27 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-star-activity/results.json |
| 28 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-import-error-need-class/results.json |
| 29 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-pypi-keyword-activity/results.json |
| 30 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-import-resolvability/results.json |
| 31 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 32 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 33 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/phase-decision.json |
| 34 | 09:49:24 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/synthesis-view-count-final.md |
| 35 | 09:49:24 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 36 | 09:49:24 | unlogged_change | changed but never declared as an artifact: pyprovides_classify.py |
| 37 | 09:49:24 | unlogged_change | changed but never declared as an artifact: raw/discrimination_test_results.json |
| 38 | 09:49:24 | unlogged_change | changed but never declared as an artifact: raw/population_measurement_results.json |
| 39 | 09:49:24 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows.jsonl |
| 40 | 09:49:24 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows_dedup.jsonl |
| 41 | 09:49:24 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-005-run-pyfix-prototype-and-view-count-hacke/events.jsonl |
| 42 | 09:49:24 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-006-fresh-observation-in-a-new-domain-per-d0/events.jsonl |
| 43 | 09:49:24 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-007-design-and-run-a-fresh-observation-exper/events.jsonl |
| 44 | 09:49:24 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-008-build-and-evaluate-discrimination-test-p/events.jsonl |
| 45 | 09:49:24 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-009-run-a-fresh-observation-experiment-in-a/commands.log |
| 46 | 09:49:24 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-009-run-a-fresh-observation-experiment-in-a/events.jsonl |
| 47 | 09:49:24 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-010-record-e090-maven-central-experiment-res/events.jsonl |
| 48 | 09:49:24 | unlogged_change | changed but never declared as an artifact: viewcount_crates.py |
| 49 | 09:49:24 | session_end | Ran Experiment 094 testing view-count principle on Kubernetes Discourse forum (discuss.kubernetes.io). Fetched 500 topics from General Discussions cat |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-011-design-and-run-a-fresh-observation-exper/events.jsonl
```
