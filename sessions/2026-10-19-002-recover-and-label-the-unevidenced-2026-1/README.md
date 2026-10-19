# Session 2026-10-19-002-recover-and-label-the-unevidenced-2026-1

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-19
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-19T00:24:27+00:00
- **Duration:** 6050.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Recover and label the unevidenced 2026-10-18 record honestly, then run one declared fresh-observation experiment on an axis no prior experiment used

## Summary

Recovered the unevidenced 2026-10-18 record (F142: twelve of seventeen sessions captured zero commands and declared zero artifacts; six planner-shaped Stage-A gates discarded with a sha256 inventory; E180 and E147 artifacts recovered into git; D121 retires the Stage-A gate as a candidate screen). Opened the money axis no prior experiment had used: E193 measured that every price-bearing marketplace is hard-blocked from this host, E194 scanned twelve pre-declared consumer jobs (286 on-topic apps, 6 paid, the one apparent hit a PDF scanner), and E195 opened USAspending as a reachable spend source while showing a keyword's money belongs to a different industry (knitting returned $3.58M of combat uniforms). doc lint green.

## Next

Declare a spend scan addressed by product and service code (PSC/NAICS) rather than by keyword; every total reported beside its industry distribution, because E194's TurboScan and E195's combat uniforms are the same defect in two sources

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/193-source-capability-probe/probe.py | 694ca6b14906 | 4557 |
| EXPERIMENTS/193-source-capability-probe/probe2.py | 3f69c3f8f2ab | 4708 |
| EXPERIMENTS/193-source-capability-probe/raw/probe.json | 0185085586f7 | 6054 |
| EXPERIMENTS/193-source-capability-probe/raw/probe2.json | aef7221babba | 2691 |
| EXPERIMENTS/194-appstore-demand-scan/scan.py | 4550de9e5fec | 6680 |
| EXPERIMENTS/194-appstore-demand-scan/scan2.py | 5a2c38ca3bf5 | 7277 |
| EXPERIMENTS/195-spend-axis-probe/probe.py | 2911f54e3aff | 5631 |
| EXPERIMENTS/195-spend-axis-probe/probe2.py | f731c4951792 | 4523 |

## Commands

9 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/193-source-capability-probe/probe.py'] | 0 | 7360 |
| 3 | ['python3', 'EXPERIMENTS/193-source-capability-probe/probe2.py'] | 0 | 5260 |
| 8 | ['python3', 'EXPERIMENTS/194-appstore-demand-scan/scan.py'] | 0 | 66088 |
| 9 | ['python3', 'EXPERIMENTS/194-appstore-demand-scan/scan2.py'] | 0 | 14474 |
| 12 | ['python3', 'EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py'] | 1 | 1905 |
| 13 | ['python3', 'EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py'] | 0 | 195 |
| 14 | ['python3', 'EXPERIMENTS/185-knitting-repair-planner-stage-a/planner.py'] | 1 | 996 |
| 16 | ['python3', 'EXPERIMENTS/195-spend-axis-probe/probe.py'] | 0 | 6099 |
| 17 | ['python3', 'EXPERIMENTS/195-spend-axis-probe/probe2.py'] | 0 | 2491 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 198 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-RECORDS-5.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/account.csv |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:24:27 | session_start | Recover and label the unevidenced 2026-10-18 record honestly, then run one declared fresh-observation experiment on an axis no prior experiment used |
| 2 | 00:25:05 | command | $ python3 EXPERIMENTS/193-source-capability-probe/probe.py |
| 3 | 00:25:44 | command | $ python3 EXPERIMENTS/193-source-capability-probe/probe2.py |
| 4 | 00:26:01 | artifact | wrote EXPERIMENTS/193-source-capability-probe/probe.py |
| 5 | 00:26:02 | artifact | wrote EXPERIMENTS/193-source-capability-probe/probe2.py |
| 6 | 00:26:03 | artifact | wrote EXPERIMENTS/193-source-capability-probe/raw/probe.json |
| 7 | 00:26:04 | artifact | wrote EXPERIMENTS/193-source-capability-probe/raw/probe2.json |
| 8 | 00:27:40 | command | $ python3 EXPERIMENTS/194-appstore-demand-scan/scan.py |
| 9 | 00:28:37 | command | $ python3 EXPERIMENTS/194-appstore-demand-scan/scan2.py |
| 10 | 00:29:26 | artifact | wrote EXPERIMENTS/194-appstore-demand-scan/scan.py |
| 11 | 00:29:27 | artifact | wrote EXPERIMENTS/194-appstore-demand-scan/scan2.py |
| 12 | 00:38:41 | command | $ python3 EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py |
| 13 | 00:38:54 | command | $ python3 EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py |
| 14 | 00:39:19 | command | $ python3 EXPERIMENTS/185-knitting-repair-planner-stage-a/planner.py |
| 15 | 01:39:05 | milestone | F142 written: twelve of seventeen 2026-10-18 sessions captured zero commands and declared zero artifacts; six planner-shaped Stage-A gates discarded a |
| 16 | 01:39:41 | command | $ python3 EXPERIMENTS/195-spend-axis-probe/probe.py |
| 17 | 01:40:16 | command | $ python3 EXPERIMENTS/195-spend-axis-probe/probe2.py |
| 18 | 02:04:07 | artifact | wrote EXPERIMENTS/195-spend-axis-probe/probe.py |
| 19 | 02:04:10 | artifact | wrote EXPERIMENTS/195-spend-axis-probe/probe2.py |
| 20 | 02:05:16 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-5.md |
| 21 | 02:05:16 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 22 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
| 23 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/account.csv |
| 24 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
| 25 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
| 26 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
| 27 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
| 28 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
| 29 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
| 30 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
| 31 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |
| 32 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_raw.json |
| 33 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_with_answers.json |
| 34 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/questions_raw.json |
| 35 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_all.jsonl |
| 36 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_home-assistant_io.jsonl |
| 37 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_openhab_org.jsonl |
| 38 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_discourse_ubuntu_com.jsonl |
| 39 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 40 | 02:05:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl |
| 212 | 02:05:17 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-017-fresh-exploration-investigate-a-new-prob/events.jsonl |
| 213 | 02:05:17 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-018-log-artifacts-from-e186-experiment-and-r/events.jsonl |
| 214 | 02:05:17 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-019-log-e187-experiment-artifacts-and-update/events.jsonl |
| 215 | 02:05:17 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-020-decide-on-and-build-a-fresh-exploration/events.jsonl |
| 216 | 02:05:17 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-021-summarize-work-and-determine-continuatio/events.jsonl |
| 217 | 02:05:17 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-19-001-complete-e190-python-package-documentati/events.jsonl |
| 218 | 02:05:17 | doc_update | updated DECISIONS.md |
| 219 | 02:05:17 | doc_update | updated FAILURES.md |
| 220 | 02:05:17 | doc_update | updated STATE.md |
| 221 | 02:05:17 | session_end | Recovered the unevidenced 2026-10-18 record (F142: twelve of seventeen sessions captured zero commands and declared zero artifacts; six planner-shaped |

_171 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-19-002-recover-and-label-the-unevidenced-2026-1/events.jsonl
```
