# Session 2026-10-18-010-prior-art-check-on-knitting-repair-plann

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-18
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-18T11:42:38+00:00
- **Duration:** 156.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Prior-art check on knitting repair planning tools before deciding on Stage B physical validation

## Summary

Completed prior-art check on knitting repair planning tools. Found 7 relevant prior art pieces across three vocabularies: commercial (KnittingFix), academic (KnitPick, knit_graph, Stitch Maps, 2024 graph layout paper, 2026 laddering physics paper), and tutorial (TECHknitting). Key findings: (1) No existing tool computes constrained intervention plans for EXISTING hand-knit structures with known errors. (2) Stage A computational result survives (kill gate NOT FIRED: local planner beats full-row rollback on 6/8 fixtures, matches oracle on 2/2). (3) Algorithmic advantage claim is prior art (F009) - minimum-cost repair planning known 2007-2026. (4) Physical feasibility COMPLETELY UNTESTED - 2026 physics paper confirms topology alone insufficient (tension, friction, curvature matter). (5) Stage B physical validation requires 6-10 swatches, experienced knitter, physical resources not available in this environment. Decision: Knitting repair axis joins evidence base as computationally viable but physically unvalidated. Mission continues fresh exploration per STATE.md.

## Next

Return to fresh exploration for a completely different kind of need or invention axis. The unserved-need hypothesis is dead for all measured populations. The ground-truth-quality axis closed. Knitting repair Stage A passes computationally but Stage B physically unvalidated and algorithmic claim is prior art.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| /tmp/prior_art_knitting_repair.json | 01c8db57ad0c | 6295 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', '\nimport json\nfrom datetime import datetime\n\n# Record the prior-art check findings\nfindings = {\n    \'date\': \'2026-10-18\',\ | 0 | 101 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 151 |
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
| 1 | 11:42:38 | session_start | Prior-art check on knitting repair planning tools before deciding on Stage B physical validation |
| 2 | 11:44:56 | command | $ python3 -c  import json from datetime import datetime  # Record the prior-art check findings findings = {     'date': '2026-10-18',     'can |
| 3 | 11:45:04 | artifact | wrote /tmp/prior_art_knitting_repair.json |
| 4 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
| 5 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/account.csv |
| 6 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
| 7 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
| 8 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
| 9 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
| 10 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
| 11 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
| 12 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
| 13 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |
| 14 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_raw.json |
| 15 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_with_answers.json |
| 16 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/questions_raw.json |
| 17 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_all.jsonl |
| 18 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_home-assistant_io.jsonl |
| 19 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_openhab_org.jsonl |
| 20 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_discourse_ubuntu_com.jsonl |
| 21 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 22 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl |
| 23 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_lulzbot_com.jsonl |
| 24 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_home-assistant_io.jsonl |
| 25 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_openhab_org.jsonl |
| 26 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_discourse_ubuntu_com.jsonl |
| 27 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_arduino_cc.jsonl |
| 28 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_creality_com.jsonl |
| 29 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_lulzbot_com.jsonl |
| 30 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_home-assistant_io.jsonl |
| 31 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_openhab_org.jsonl |
| 32 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_discourse_ubuntu_com.jsonl |
| 33 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_arduino_cc.jsonl |
| 34 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_creality_com.jsonl |
| 35 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_lulzbot_com.jsonl |
| 36 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/classified_topics.jsonl |
| 37 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/harvest_summary.json |
| 38 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/structured_cases.jsonl |
| 39 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/topics_page_0.json |
| 40 | 11:45:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/topics_page_1.json |
| 146 | 11:45:14 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-005-fresh-exploration-find-a-concrete-proble/commands.log |
| 147 | 11:45:14 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-005-fresh-exploration-find-a-concrete-proble/events.jsonl |
| 148 | 11:45:14 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-006-build-classifier-v4-prototype/events.jsonl |
| 149 | 11:45:14 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-007-repair-the-red-tree-left-by-the-e183-e18/commands.log |
| 150 | 11:45:14 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-007-repair-the-red-tree-left-by-the-e183-e18/events.jsonl |
| 151 | 11:45:14 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-008-fresh-exploration-identify-a-new-inventi/events.jsonl |
| 152 | 11:45:14 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-009-extend-knitting-repair-planner-experimen/events.jsonl |
| 153 | 11:45:14 | unlogged_change | changed but never declared as an artifact: tools/viewcount_classifier_v4.py |
| 154 | 11:45:14 | unlogged_change | changed but never declared as an artifact: tools/viewcount_demo_reasoning.py |
| 155 | 11:45:15 | session_end | Completed prior-art check on knitting repair planning tools. Found 7 relevant prior art pieces across three vocabularies: commercial (KnittingFix), ac |

_105 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-18-010-prior-art-check-on-knitting-repair-plann/events.jsonl
```
