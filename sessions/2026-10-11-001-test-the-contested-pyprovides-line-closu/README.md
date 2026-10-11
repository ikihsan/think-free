# Session 2026-10-11-001-test-the-contested-pyprovides-line-closu

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T00:11:22+00:00
- **Duration:** 889.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test the contested pyprovides line-closure by hand-reading E091's 25 module-only rows

## Summary

Hand re-read all 25 E091 module-only rows: 2 genuine + 2 borderline of 858 (0.23-0.47%), under the 1% gate. Package-name line closed with committed evidence (F113, D102); session 009's same verdict corrected from assertion to measurement. All dependent records updated (STATE-next-actions, README front door, SESSION_OUTCOME, pyprovides README, DECISIONS, FAILURES). Uncommitted: doc lint red at baseline (18 pre-existing violations, other VMs' files), so per exit-0 rule nothing was committed.

## Next

Fresh observation in a new domain per D083 (FDA MAUDE medical-device alarms was the standing recommendation); land this session's uncommitted line-closure once doc lint is green

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/091-import-error-population/reread.json | a194ed52a60f | 5878 |
| EXPERIMENTS/091-import-error-population/REREAD.md | f9d5e83243f4 | 4334 |
| EXPERIMENTS/091-import-error-population/results.json | b121943bf9a3 | 1000 |
| FAILURES.md | 01a4fe2d11f7 | 66833 |
| FAILURES-findings-37.md | 8252c1cffd06 | 12166 |
| DECISIONS.md | 1d49b92fc26a | 19535 |
| DECISIONS-SCREENING-18.md | 1e60c8cbeec2 | 6547 |
| STATE-next-actions.md | e6ff1829cb0c | 8687 |
| README.md | 1ee4153657a9 | 4733 |
| SESSION_OUTCOME.md | 6258c55501c6 | 5388 |
| pyprovides/README.md | 9134c52292dc | 6215 |
| EXPERIMENTS/091-import-error-population/README.md | 6796d0a26336 | 6234 |

## Commands

2 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport json, math\nlab=json.load(open('EXPERIMENTS/091-import-error-population/reread.json'))\nrows=[json.loads(l) for l in open( | 0 | 217 |
| 4 | ['python3', '-m', 'unittest', 'tests.test_result_numbers', 'tests.test_result_numbers_falsified', 'tests.test_decision_files', 'tests.test_decision_he | 1 | 492 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:11:22 | session_start | Test the contested pyprovides line-closure by hand-reading E091's 25 module-only rows |
| 2 | 00:14:23 | command | $ python3 -c  import json, math lab=json.load(open('EXPERIMENTS/091-import-error-population/reread.json')) rows=[json.loads(l) for l in open(' |
| 3 | 00:14:27 | milestone | Re-read all 25 E091 module-only rows: 2 genuine + 2 borderline of 858, gate fails, line closes |
| 4 | 00:24:25 | command | $ python3 -m unittest tests.test_result_numbers tests.test_result_numbers_falsified tests.test_decision_files tests.test_decision_header tests |
| 5 | 00:25:58 | artifact | wrote EXPERIMENTS/091-import-error-population/reread.json |
| 6 | 00:25:58 | artifact | wrote EXPERIMENTS/091-import-error-population/REREAD.md |
| 7 | 00:25:59 | artifact | wrote EXPERIMENTS/091-import-error-population/results.json |
| 8 | 00:26:00 | artifact | wrote FAILURES.md |
| 9 | 00:26:00 | artifact | wrote FAILURES-findings-37.md |
| 10 | 00:26:01 | artifact | wrote DECISIONS.md |
| 11 | 00:26:02 | artifact | wrote DECISIONS-SCREENING-18.md |
| 12 | 00:26:02 | artifact | wrote STATE-next-actions.md |
| 13 | 00:26:03 | artifact | wrote README.md |
| 14 | 00:26:04 | artifact | wrote SESSION_OUTCOME.md |
| 15 | 00:26:04 | artifact | wrote pyprovides/README.md |
| 16 | 00:26:05 | artifact | wrote EXPERIMENTS/091-import-error-population/README.md |
| 17 | 00:26:06 | milestone | Records updated: F113/D102 close the package-name line; 6 lint violations fixed, 0 added; targeted tests green except pre-existing orphan |
| 18 | 00:26:11 | doc_update | updated DECISIONS-SCREENING-18.md |
| 19 | 00:26:11 | doc_update | updated DECISIONS.md |
| 20 | 00:26:11 | doc_update | updated FAILURES.md |
| 21 | 00:26:11 | session_end | Hand re-read all 25 E091 module-only rows: 2 genuine + 2 borderline of 858 (0.23-0.47%), under the 1% gate. Package-name line closed with committed ev |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-001-test-the-contested-pyprovides-line-closu/events.jsonl
```
