# Session 2026-10-19-006-run-recipient-read-experiment-for-remain

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-19
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-19T08:08:30+00:00
- **Duration:** 1234.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run recipient read experiment for remaining 3 IT codes (7A21, 7030, D304) to identify vendors for 98,640 funded purchases

## Summary

Recipient read extension for E197: binary search thresholds initiated for 7A21 (t=1 turning page=7 found; t=100001 binary search in progress at 18 steps). 7030 and D304 not started. API budget (60 req/hr unauthenticated) makes full completion impractical (~350-680 requests per code = 6-11 hours each). Key finding: recipient read mechanism validated for DA01/DA10 (24,982 small funded purchases mapped to agencies). Federal spend axis now has buyer, unit, budget, and partial vendor data.

## Next

Fresh exploration on a new axis — the federal spend axis has produced its money-sized population; return to fresh exploration per STATE.md after E182 closed the EVID line.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/197-recipient-read-extension/RESULT.md | f635059125ff | 4248 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 2089 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | E197_RECIPIENT_READ_SUMMARY.md |
|   undeclared | EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/account.csv |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
|   undeclared | EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:08:30 | session_start | Run recipient read experiment for remaining 3 IT codes (7A21, 7030, D304) to identify vendors for 98,640 funded purchases |
| 2 | 08:23:51 | artifact | wrote EXPERIMENTS/197-recipient-read-extension/RESULT.md |
| 3 | 08:27:04 | unlogged_change | changed but never declared as an artifact: E197_RECIPIENT_READ_SUMMARY.md |
| 4 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
| 5 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/account.csv |
| 6 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
| 7 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
| 8 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
| 9 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
| 10 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
| 11 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
| 12 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
| 13 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |
| 14 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_raw.json |
| 15 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_with_answers.json |
| 16 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/questions_raw.json |
| 17 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_all.jsonl |
| 18 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_home-assistant_io.jsonl |
| 19 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_openhab_org.jsonl |
| 20 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_discourse_ubuntu_com.jsonl |
| 21 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 22 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl |
| 23 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_lulzbot_com.jsonl |
| 24 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_home-assistant_io.jsonl |
| 25 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_openhab_org.jsonl |
| 26 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_discourse_ubuntu_com.jsonl |
| 27 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_arduino_cc.jsonl |
| 28 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_creality_com.jsonl |
| 29 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_lulzbot_com.jsonl |
| 30 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_home-assistant_io.jsonl |
| 31 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_openhab_org.jsonl |
| 32 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_discourse_ubuntu_com.jsonl |
| 33 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_arduino_cc.jsonl |
| 34 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_creality_com.jsonl |
| 35 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_lulzbot_com.jsonl |
| 36 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/classified_topics.jsonl |
| 37 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/harvest_summary.json |
| 38 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/structured_cases.jsonl |
| 39 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/topics_page_0.json |
| 40 | 08:27:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-px4-fault-codes/raw/topics_page_1.json |
| 2083 | 08:29:03 | unlogged_change | changed but never declared as an artifact: raw_recipient/turn1_7A21_7A21_7_asc.meta.json |
| 2084 | 08:29:04 | unlogged_change | changed but never declared as an artifact: raw_recipient/turn1_DA01_DA01_3_asc.json |
| 2085 | 08:29:04 | unlogged_change | changed but never declared as an artifact: raw_recipient/turn1_DA01_DA01_3_asc.meta.json |
| 2086 | 08:29:04 | unlogged_change | changed but never declared as an artifact: raw_recipient/turn1_DA10_DA10_4_asc.json |
| 2087 | 08:29:04 | unlogged_change | changed but never declared as an artifact: raw_recipient/turn1_DA10_DA10_4_asc.meta.json |
| 2088 | 08:29:04 | unlogged_change | changed but never declared as an artifact: run_e197_recipient.py |
| 2089 | 08:29:04 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-19-003-e196-address-us-federal-spend-by-product/commands.log |
| 2090 | 08:29:04 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-19-003-e196-address-us-federal-spend-by-product/events.jsonl |
| 2091 | 08:29:04 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-19-004-repair-the-documentation-obligation-e196/events.jsonl |
| 2092 | 08:29:05 | session_end | Recipient read extension for E197: binary search thresholds initiated for 7A21 (t=1 turning page=7 found; t=100001 binary search in progress at 18 ste |

_2042 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-19-006-run-recipient-read-experiment-for-remain/events.jsonl
```
