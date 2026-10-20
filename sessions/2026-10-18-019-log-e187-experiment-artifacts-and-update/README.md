# Session 2026-10-18-019-log-e187-experiment-artifacts-and-update

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-18
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-18T23:13:58+00:00
- **Duration:** 31.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Log E187 experiment artifacts and update STATE files

## Summary

E187 completed: Fresh exploration in healthcare/clinical trials domain testing matching/recommendation need type. ClinicalTrials.gov structured eligibility filtering funnel: condition (median 16.5) → age (16.0) → sex (16.0) → location (1.0) → exclusion (0.0). Only 35% patients have matches, median 0.0. Location filter is dominant bottleneck (94% reduction). Kill gate fired (G2, G3, G4, G5 all FAIL). Matching need not served by structured fields alone.

## Next

Continue fresh exploration in a different domain or need type per STATE.md standing instruction

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/187-clinical-trial-matching/README.md | d927db3ede0b | 6961 |
| EXPERIMENTS/187-clinical-trial-matching/run.py | 40ca0a15388a | 32652 |
| EXPERIMENTS/187-clinical-trial-matching/RESULT.md | ce4c776d0f9e | 5592 |
| STATE.md | ad08dc7c8baf | 28889 |
| STATE-next-actions.md | e7d954f56561 | 20602 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 192 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/account.csv |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
|   undeclared | EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 23:13:58 | session_start | Log E187 experiment artifacts and update STATE files |
| 2 | 23:14:10 | artifact | wrote EXPERIMENTS/187-clinical-trial-matching/README.md |
| 3 | 23:14:12 | artifact | wrote EXPERIMENTS/187-clinical-trial-matching/run.py |
| 4 | 23:14:15 | artifact | wrote EXPERIMENTS/187-clinical-trial-matching/RESULT.md |
| 5 | 23:14:17 | artifact | wrote STATE.md |
| 6 | 23:14:19 | artifact | wrote STATE-next-actions.md |
| 7 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
| 8 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/account.csv |
| 9 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
| 10 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
| 11 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
| 12 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
| 13 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
| 14 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
| 15 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
| 16 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |
| 17 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_raw.json |
| 18 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_with_answers.json |
| 19 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/questions_raw.json |
| 20 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_all.jsonl |
| 21 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_home-assistant_io.jsonl |
| 22 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_openhab_org.jsonl |
| 23 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_discourse_ubuntu_com.jsonl |
| 24 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 25 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl |
| 26 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_lulzbot_com.jsonl |
| 27 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_home-assistant_io.jsonl |
| 28 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_openhab_org.jsonl |
| 29 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_discourse_ubuntu_com.jsonl |
| 30 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_arduino_cc.jsonl |
| 31 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_creality_com.jsonl |
| 32 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_lulzbot_com.jsonl |
| 33 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_home-assistant_io.jsonl |
| 34 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_openhab_org.jsonl |
| 35 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_discourse_ubuntu_com.jsonl |
| 36 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_arduino_cc.jsonl |
| 37 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_creality_com.jsonl |
| 38 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_lulzbot_com.jsonl |
| 39 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/classified_topics.jsonl |
| 40 | 23:14:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/harvest_summary.json |
| 191 | 23:14:29 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-015-conduct-structured-fresh-exploration-of/events.jsonl |
| 192 | 23:14:29 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-016-build-knitting-repair-prototype-and-opti/events.jsonl |
| 193 | 23:14:29 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-017-fresh-exploration-investigate-a-new-prob/commands.log |
| 194 | 23:14:29 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-017-fresh-exploration-investigate-a-new-prob/events.jsonl |
| 195 | 23:14:29 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-018-log-artifacts-from-e186-experiment-and-r/events.jsonl |
| 196 | 23:14:29 | unlogged_change | changed but never declared as an artifact: tools/diy_repair_advisor.py |
| 197 | 23:14:29 | unlogged_change | changed but never declared as an artifact: tools/viewcount_classifier_v4.py |
| 198 | 23:14:29 | unlogged_change | changed but never declared as an artifact: tools/viewcount_demo_reasoning.py |
| 199 | 23:14:30 | doc_update | updated STATE.md |
| 200 | 23:14:30 | session_end | E187 completed: Fresh exploration in healthcare/clinical trials domain testing matching/recommendation need type. ClinicalTrials.gov structured eligib |

_150 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-18-019-log-e187-experiment-artifacts-and-update/events.jsonl
```
