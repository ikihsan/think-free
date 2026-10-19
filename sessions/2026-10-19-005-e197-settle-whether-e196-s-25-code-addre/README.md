# Session 2026-10-19-005-e197-settle-whether-e196-s-25-code-addre

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-19
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-19T05:11:52+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E197: settle whether E196's 25 code-addressed federal cells hold real funded purchases or zero-amount records, by counting awards carrying money per code with two independent instruments

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/197-funded-award-count/RESULT.md | 4e4c99fc4e87 | 8374 |
| EXPERIMENTS/197-funded-award-count/raw/a1_4220_asc_p7_asc.json | 73fd481849b2 | 33528 |
| EXPERIMENTS/197-funded-award-count/raw/a1_4220_asc_p7_asc.meta.json | b13e36787a35 | 670 |
| EXPERIMENTS/197-funded-award-count/raw/a1_4470_asc_p1_asc.json | 6e4936fb5a1a | 31960 |
| EXPERIMENTS/197-funded-award-count/raw/a1_4470_asc_p2_asc.json | 33fa0e9d69a4 | 32114 |
| EXPERIMENTS/197-funded-award-count/raw/a1_4470_asc_p1_asc.meta.json | 89708b4ca0aa | 670 |

## Commands

7 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/197-funded-award-count/panel2.py'] | 0 | 340271 |
| 3 | ['python3', 'EXPERIMENTS/197-funded-award-count/analysis.py'] | 1 | 523 |
| 4 | ['python3', 'EXPERIMENTS/197-funded-award-count/analysis.py'] | 0 | 694 |
| 5 | ['python3', 'EXPERIMENTS/197-funded-award-count/recompute.py'] | 0 | 1403 |
| 6 | ['python3', 'EXPERIMENTS/197-funded-award-count/analysis.py'] | 0 | 221 |
| 7 | ['python3', 'EXPERIMENTS/197-funded-award-count/analysis.py'] | 0 | 269 |
| 8 | ['tools/origin', 'doc', 'lint'] | 2 | 318690 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 6488 |
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
| 1 | 05:11:52 | session_start | E197: settle whether E196's 25 code-addressed federal cells hold real funded purchases or zero-amount records, by counting awards carrying money per c |
| 2 | 06:13:54 | command | $ python3 EXPERIMENTS/197-funded-award-count/panel2.py |
| 3 | 06:14:09 | command | $ python3 EXPERIMENTS/197-funded-award-count/analysis.py |
| 4 | 06:14:46 | command | $ python3 EXPERIMENTS/197-funded-award-count/analysis.py |
| 5 | 06:15:43 | command | $ python3 EXPERIMENTS/197-funded-award-count/recompute.py |
| 6 | 06:15:55 | command | $ python3 EXPERIMENTS/197-funded-award-count/analysis.py |
| 7 | 06:18:48 | command | $ python3 EXPERIMENTS/197-funded-award-count/analysis.py |
| 8 | 06:30:32 | command | $ tools/origin doc lint |
| 9 | 06:38:23 | artifact | wrote EXPERIMENTS/197-funded-award-count/RESULT.md |
| 10 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
| 11 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/account.csv |
| 12 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
| 13 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
| 14 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
| 15 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
| 16 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
| 17 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
| 18 | 06:38:41 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
| 19 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |
| 20 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_raw.json |
| 21 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_with_answers.json |
| 22 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/questions_raw.json |
| 23 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_all.jsonl |
| 24 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_home-assistant_io.jsonl |
| 25 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_openhab_org.jsonl |
| 26 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_discourse_ubuntu_com.jsonl |
| 27 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 28 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl |
| 29 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_lulzbot_com.jsonl |
| 30 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_home-assistant_io.jsonl |
| 31 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_openhab_org.jsonl |
| 32 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_discourse_ubuntu_com.jsonl |
| 33 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_arduino_cc.jsonl |
| 34 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_creality_com.jsonl |
| 35 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_lulzbot_com.jsonl |
| 36 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_home-assistant_io.jsonl |
| 37 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_community_openhab_org.jsonl |
| 38 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_discourse_ubuntu_com.jsonl |
| 39 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_arduino_cc.jsonl |
| 40 | 06:38:42 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_creality_com.jsonl |
| 6493 | 08:06:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p14_asc.json |
| 6494 | 08:06:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p14_asc.meta.json |
| 6495 | 08:06:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p1_asc.json |
| 6496 | 08:06:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p1_asc.meta.json |
| 6497 | 08:06:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p29_asc.json |
| 6498 | 08:06:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p29_asc.meta.json |
| 6499 | 08:06:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p36_asc.json |
| 6500 | 08:06:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p36_asc.meta.json |
| 6501 | 08:06:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p39_asc.json |
| 6502 | 08:06:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/197-funded-award-count/raw/a1_5895_asc_p39_asc.meta.json |

_6452 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-19-005-e197-settle-whether-e196-s-25-code-addre/events.jsonl
```
