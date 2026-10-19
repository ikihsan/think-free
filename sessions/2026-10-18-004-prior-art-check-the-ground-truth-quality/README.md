# Session 2026-10-18-004-prior-art-check-the-ground-truth-quality

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-18
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-18T03:19:47+00:00
- **Duration:** 1305.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Prior-art-check the ground-truth-quality axis: do vote margin, corroboration count, and residualised prescriptive divergence carry answer-quality information beyond known Stack Overflow quality predictors?

## Summary

Prior-art-check (E183) and experiment (E184) on ground-truth-quality axis complete. Three signals (vote margin, corroboration count, residualised prescriptive divergence) do NOT add predictive power beyond standard text+metadata features for answer quality prediction on Stack Overflow. Baseline AUC 0.9986, treatment AUC 0.9986, delta -0.0000. Kill gate FAILED. Axis closed.

## Next

Return to fresh exploration

## Artifacts

_none_

## Commands

11 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['ls', '/home/ubuntu/think-free/EXPERIMENTS/'] | 0 | 69 |
| 4 | ['ls', '/home/ubuntu/think-free/EXPERIMENTS/'] | 0 | 77 |
| 5 | ['python3', '-c', "import urllib.request; print('urllib OK')"] | 0 | 399 |
| 6 | ['python3', '-c', "import json; print('json OK')"] | 0 | 191 |
| 7 | ['python3', '-c', "import numpy; print('numpy', numpy.__version__)"] | 0 | 2581 |
| 8 | ['python3', '-c', "\nimport urllib.request, json\nurl = 'https://api.stackexchange.com/2.3/questions?site=stackoverflow&pagesize=1&order=desc&sort=vot | 0 | 745 |
| 10 | ['python3', 'EXPERIMENTS/183-prior-art-ground-truth-quality/e184_experiment.py'] | 0 | 161613 |
| 11 | ['git', 'status', '--short'] | 0 | 310 |
| 12 | ['git', 'add', 'STATE.md', 'STATE-next-actions.md', 'sessions/INDEX.md', 'EXPERIMENTS/183-prior-art-ground-truth-quality/'] | 0 | 101 |
| 13 | ['timeout', '180', 'tools/origin', 'doc', 'lint'] | 2 | 172498 |
| 14 | ['tools/origin', 'doc', 'index'] | 0 | 11423 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 138 |
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
| 1 | 03:19:47 | session_start | Prior-art-check the ground-truth-quality axis: do vote margin, corroboration count, and residualised prescriptive divergence carry answer-quality info |
| 2 | 03:23:17 | milestone | Prior-art-check complete: answer quality prediction on SO is established; vote-based and metadata features are standard; the three specific signals (v |
| 3 | 03:23:30 | command | $ ls /home/ubuntu/think-free/EXPERIMENTS/ |
| 4 | 03:23:38 | command | $ ls /home/ubuntu/think-free/EXPERIMENTS/ |
| 5 | 03:24:52 | command | $ python3 -c import urllib.request; print('urllib OK') |
| 6 | 03:24:53 | command | $ python3 -c import json; print('json OK') |
| 7 | 03:24:55 | command | $ python3 -c import numpy; print('numpy', numpy.__version__) |
| 8 | 03:25:08 | command | $ python3 -c  import urllib.request, json url = 'https://api.stackexchange.com/2.3/questions?site=stackoverflow&pagesize=1&order=desc&sort=vot |
| 9 | 03:25:44 | milestone | Prior-art-check cleared: three signals not in prior art. Building E184 experiment to test whether they add predictive power beyond standard text+metad |
| 10 | 03:31:47 | command | $ python3 EXPERIMENTS/183-prior-art-ground-truth-quality/e184_experiment.py |
| 11 | 03:34:23 | command | $ git status --short |
| 12 | 03:34:35 | command | $ git add STATE.md STATE-next-actions.md sessions/INDEX.md EXPERIMENTS/183-prior-art-ground-truth-quality/ |
| 13 | 03:40:04 | command | $ timeout 180 tools/origin doc lint |
| 14 | 03:40:36 | command | $ tools/origin doc index |
| 15 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
| 16 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/account.csv |
| 17 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
| 18 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
| 19 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
| 20 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
| 21 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
| 22 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
| 23 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |
| 24 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/raw/harvested_papers.jsonl |
| 25 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_raw.json |
| 26 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-automotive-obd2-diagnostics/raw/questions_with_answers.json |
| 27 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/questions_raw.json |
| 28 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_all.jsonl |
| 29 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_home-assistant_io.jsonl |
| 30 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_community_openhab_org.jsonl |
| 31 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_discourse_ubuntu_com.jsonl |
| 32 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 33 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl |
| 34 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_lulzbot_com.jsonl |
| 35 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_home-assistant_io.jsonl |
| 36 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_community_openhab_org.jsonl |
| 37 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_discourse_ubuntu_com.jsonl |
| 38 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_arduino_cc.jsonl |
| 39 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_creality_com.jsonl |
| 40 | 03:41:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-3dprint-fault-codes/raw/posts_forum_lulzbot_com.jsonl |
| 145 | 03:41:32 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 146 | 03:41:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-007-fresh-exploration-find-a-concrete-builda/commands.log |
| 147 | 03:41:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-007-fresh-exploration-find-a-concrete-builda/events.jsonl |
| 148 | 03:41:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-001-e181-test-whether-supplying-the-specific/commands.log |
| 149 | 03:41:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-001-e181-test-whether-supplying-the-specific/events.jsonl |
| 150 | 03:41:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-002-log-e181-s-two-undeclared-artifacts-that/events.jsonl |
| 151 | 03:41:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-003-measure-whether-e177-s-ground-truth-is-c/commands.log |
| 152 | 03:41:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-003-measure-whether-e177-s-ground-truth-is-c/events.jsonl |
| 153 | 03:41:32 | doc_update | updated STATE.md |
| 154 | 03:41:32 | session_end | Prior-art-check (E183) and experiment (E184) on ground-truth-quality axis complete. Three signals (vote margin, corroboration count, residualised pres |

_104 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-18-004-prior-art-check-the-ground-truth-quality/events.jsonl
```
