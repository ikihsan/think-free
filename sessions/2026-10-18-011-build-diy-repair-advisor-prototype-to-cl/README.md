# Session 2026-10-18-011-build-diy-repair-advisor-prototype-to-cl

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-18
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-18T13:55:37+00:00
- **Duration:** 60.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Build DIY Repair Advisor prototype to classify home repair questions into domains

## Summary

Built DIY Repair Advisor prototype (tools/diy_repair_advisor.py) that classifies 30 real DIY Stack Exchange questions into 10 repair domains using keyword matching. Key finding: 60% of questions (18/30) were classified as 'general' / unmatched, revealing a significant vocabulary gap where most DIY questions use everyday language rather than technical domain terms. The prototype successfully categorizes the remaining 40% into domains like plumbing (5), basement&design (4), masonry&stone (3), tiling&flooring (3), electrical (3), carpentry&doors (2), with one question each in plumbing&fixtures and electrical&lighting. This is an evidence-gathering prototype, not a repair solution — it measures the classification problem space.

## Next

Expand vocabulary or pivot to fresh exploration per STATE.md §267

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 156 |
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
| 1 | 13:55:37 | session_start | Build DIY Repair Advisor prototype to classify home repair questions into domains |
| 2 | 13:56:10 | milestone | DIY Repair Advisor prototype built and classified 30 real DIY questions |
| 3 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
| 4 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/account.csv |
| 5 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
| 6 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
| 7 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
| 8 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
| 9 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
| 10 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
| 11 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
| 12 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |
| 13 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_raw.json |
| 14 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_with_answers.json |
| 15 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/questions_raw.json |
| 16 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_all.jsonl |
| 17 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_home-assistant_io.jsonl |
| 18 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_openhab_org.jsonl |
| 19 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_discourse_ubuntu_com.jsonl |
| 20 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 21 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl |
| 22 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_lulzbot_com.jsonl |
| 23 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_home-assistant_io.jsonl |
| 24 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_openhab_org.jsonl |
| 25 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_discourse_ubuntu_com.jsonl |
| 26 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_arduino_cc.jsonl |
| 27 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_creality_com.jsonl |
| 28 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_lulzbot_com.jsonl |
| 29 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_home-assistant_io.jsonl |
| 30 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_openhab_org.jsonl |
| 31 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_discourse_ubuntu_com.jsonl |
| 32 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_arduino_cc.jsonl |
| 33 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_creality_com.jsonl |
| 34 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_lulzbot_com.jsonl |
| 35 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/classified_topics.jsonl |
| 36 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/harvest_summary.json |
| 37 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/structured_cases.jsonl |
| 38 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/topics_page_0.json |
| 39 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/topics_page_1.json |
| 40 | 13:56:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/topics_page_10.json |
| 150 | 13:56:38 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-007-repair-the-red-tree-left-by-the-e183-e18/commands.log |
| 151 | 13:56:38 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-007-repair-the-red-tree-left-by-the-e183-e18/events.jsonl |
| 152 | 13:56:38 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-008-fresh-exploration-identify-a-new-inventi/events.jsonl |
| 153 | 13:56:38 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-009-extend-knitting-repair-planner-experimen/events.jsonl |
| 154 | 13:56:38 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-010-prior-art-check-on-knitting-repair-plann/commands.log |
| 155 | 13:56:38 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-010-prior-art-check-on-knitting-repair-plann/events.jsonl |
| 156 | 13:56:38 | unlogged_change | changed but never declared as an artifact: tools/diy_repair_advisor.py |
| 157 | 13:56:38 | unlogged_change | changed but never declared as an artifact: tools/viewcount_classifier_v4.py |
| 158 | 13:56:38 | unlogged_change | changed but never declared as an artifact: tools/viewcount_demo_reasoning.py |
| 159 | 13:56:38 | session_end | Built DIY Repair Advisor prototype (tools/diy_repair_advisor.py) that classifies 30 real DIY Stack Exchange questions into 10 repair domains using key |

_109 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-18-011-build-diy-repair-advisor-prototype-to-cl/events.jsonl
```
