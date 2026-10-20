# Session 2026-10-18-003-measure-whether-e177-s-ground-truth-is-c

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-18
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-18T01:34:09+00:00
- **Duration:** 6213.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure whether E177's ground truth is contestable where the assistant missed, using community vote margin rather than reader judgement (E182)

## Summary

E182 closed the last testable explanation of F136's SELF/EVID gap. The question had to be corrected first: 'is the accepted answer the best answer' names a field the population does not contain (0 of 60 accepted answers; the key is the top-voted answer). Two instruments were built: vote margin was 4 of 10 against hand-read labels and its null was withdrawn, not reported; raw prescriptive overlap was rejected at 0.6500 balanced accuracy against a declared 0.80 bar, which located the defect (shared problem vocabulary read as shared prescription), and residualising against the question reached 0.8000 at specificity 1.0000. On that accepted instrument G2 did not fire (Fisher p=1.0) and an exact continuous test gave p=1.0000 with U exactly at the midpoint. The EVID line closes as a capability limit. The run also measured a ceiling on the record's own headline numbers: 21.7% of the ground truth is contested and 26.7% uncorroborated, 48.3% combined. Repaired a pre-existing red test (defect 27) where two decision-log splits were never added to the three lists that name them. doc lint OK, 845 tests OK, 31 tieback claims 0 failed.

## Next

Run prior-art-check on the ground-truth-quality axis before any product code: answer-quality prediction on Stack Overflow is an established research area, so the question is not novelty but whether vote margin, corroboration count and residualised prescriptive divergence carry information a known quality predictor does not already carry. If the screen clears, measure precision and recall of the three-signal filter against a fresh draw of hand-read labels.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/182-ground-truth-contest/PROTOCOL.md | fa8fc4a93b6a | 8243 |
| EXPERIMENTS/182-ground-truth-contest/AMENDMENT-1.md | 3293b69d54f3 | 7953 |
| EXPERIMENTS/182-ground-truth-contest/AMENDMENT-2.md | 373d032cadc3 | 4722 |
| EXPERIMENTS/182-ground-truth-contest/PROTOCOL.md | fa8fc4a93b6a | 8243 |
| EXPERIMENTS/182-ground-truth-contest/RESULT.md | 2cf0ad88eed8 | 12162 |
| EXPERIMENTS/182-ground-truth-contest/analyse.py | 0de8dc5c47cd | 9685 |
| STATE.md | 6cdd712c07e4 | 26616 |
| STATE-next-actions.md | 12b569a80923 | 13239 |
| STATE-next-actions-closed-2.md | 1418c17fcd50 | 10416 |
| STATE-next-actions-closed-3.md | 80deacd4cafe | 20601 |
| FAILURES.md | a862adef0846 | 103266 |
| FAILURES-findings-44.md | 795173f0971a | 16336 |
| DECISIONS.md | f52afaf6da25 | 29753 |
| DECISIONS-RECORDS-4.md | badbed660e6a | 9397 |
| RELEASE-MANIFEST.md | fe7ab15e7a5c | 7884 |
| EXPERIMENTS/182-ground-truth-contest/AMENDMENT-1.md | 3293b69d54f3 | 7953 |
| EXPERIMENTS/182-ground-truth-contest/AMENDMENT-2.md | 373d032cadc3 | 4722 |
| EXPERIMENTS/182-ground-truth-contest/PROTOCOL.md | fa8fc4a93b6a | 8243 |
| EXPERIMENTS/182-ground-truth-contest/RESULT.md | 2cf0ad88eed8 | 12162 |
| EXPERIMENTS/182-ground-truth-contest/analyse.py | 0de8dc5c47cd | 9685 |
| EXPERIMENTS/182-ground-truth-contest/bodies.json | ebb63242d741 | 331896 |
| EXPERIMENTS/182-ground-truth-contest/bodies.py | d2c7145ecac2 | 6861 |
| EXPERIMENTS/182-ground-truth-contest/fetch.py | 4a43c6e2382f | 5936 |
| EXPERIMENTS/182-ground-truth-contest/g5-bodies.json | 52f10ab544e0 | 86283 |
| EXPERIMENTS/182-ground-truth-contest/g5_fetch.py | 2e49a739b3c6 | 3578 |
| EXPERIMENTS/182-ground-truth-contest/overlap.json | 506c14c0ef25 | 24183 |
| EXPERIMENTS/182-ground-truth-contest/overlap.py | d62581f3de75 | 16922 |
| EXPERIMENTS/182-ground-truth-contest/power.json | 8b4752fa9fcf | 1163 |
| EXPERIMENTS/182-ground-truth-contest/raw/se-bodies.jsonl | bcccda1e3f70 | 521461 |
| EXPERIMENTS/182-ground-truth-contest/raw/se.jsonl | 0c0ae2b64350 | 110627 |
| EXPERIMENTS/182-ground-truth-contest/scores.json | ecc1792f35a3 | 17616 |
| EXPERIMENTS/182-ground-truth-contest/states.json | 9f0574e0e87c | 16819 |
| EXPERIMENTS/182-ground-truth-contest/tieback.py | afa523818f5c | 5649 |
| STATE-defects.md | c974e3e44e12 | 21772 |
| tools/originlib/paths.py | bd06513f9976 | 4681 |
| tools/originlib/reconcile.py | 51caa109fcd6 | 8905 |
| tests/test_decision_files.py | 9424f05e9c91 | 5688 |
| STATE-defects.md | c974e3e44e12 | 21772 |
| tools/originlib/paths.py | bd06513f9976 | 4681 |
| tools/originlib/reconcile.py | 51caa109fcd6 | 8905 |
| tests/test_decision_files.py | 9424f05e9c91 | 5688 |

## Commands

21 captured, 4 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/fetch.py', '--limit', '20'] | 0 | 1805 |
| 4 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/fetch.py'] | 0 | 8695 |
| 5 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/analyse.py'] | 0 | 202 |
| 6 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/g5_fetch.py'] | 0 | 16442 |
| 7 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/bodies.py'] | 0 | 5092 |
| 8 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py'] | 1 | 912 |
| 9 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py'] | 1 | 624 |
| 10 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py'] | 0 | 224 |
| 11 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py'] | 0 | 207 |
| 12 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py', '--power'] | 0 | 9157 |
| 13 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py', '--power'] | 1 | 9593 |
| 14 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py', '--power'] | 0 | 10531 |
| 16 | ['python3', '-c', "\nimport subprocess\nfor f in ['STATE.md','STATE-next-actions.md','FAILURES.md','FAILURES-findings-44.md','DECISIONS.md','DECISIONS | 0 | 151 |
| 17 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/tieback.py'] | 0 | 276 |
| 33 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/bodies.py', '--rebuild-from-raw'] | 0 | 286 |
| 34 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/bodies.py', '--rebuild-from-raw'] | 0 | 275 |
| 35 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py'] | 0 | 210 |
| 36 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py', '--power'] | 0 | 10800 |
| 57 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/overlap.py'] | 0 | 216 |
| 58 | ['python3', 'EXPERIMENTS/182-ground-truth-contest/power.py'] | 0 | 9700 |
| 62 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 786763 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 132 |
| declared artifacts now missing | 0 |
| integrity errors | 2 |
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
|   error | refused artifact EXPERIMENTS/182-ground-truth-contest/bodies.json: secret pattern(s) assigned-credential |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 01:34:09 | session_start | Measure whether E177's ground truth is contestable where the assistant missed, using community vote margin rather than reader judgement (E182) |
| 2 | 01:35:26 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/PROTOCOL.md |
| 3 | 01:35:41 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/fetch.py --limit 20 |
| 4 | 01:36:15 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/fetch.py |
| 5 | 01:36:43 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/analyse.py |
| 6 | 01:37:23 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/g5_fetch.py |
| 7 | 01:38:37 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/bodies.py |
| 8 | 01:39:00 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py |
| 9 | 01:39:12 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py |
| 10 | 01:39:24 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py |
| 11 | 01:40:19 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py |
| 12 | 01:41:03 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py --power |
| 13 | 01:41:38 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py --power |
| 14 | 01:41:59 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py --power |
| 15 | 01:42:51 | milestone | E182: both instruments run; vote margin rejected by G5 at 4/10, residualised prescriptive overlap accepted at 0.8000 balanced accuracy; G2 does not fi |
| 16 | 01:45:16 | command | $ python3 -c  import subprocess for f in ['STATE.md','STATE-next-actions.md','FAILURES.md','FAILURES-findings-44.md','DECISIONS.md','DECISIONS |
| 17 | 01:57:47 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/tieback.py |
| 18 | 01:58:00 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/AMENDMENT-1.md |
| 19 | 01:58:02 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/AMENDMENT-2.md |
| 20 | 01:58:04 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/PROTOCOL.md |
| 21 | 01:58:06 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/RESULT.md |
| 22 | 01:58:08 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/analyse.py |
| 23 | 01:58:11 | integrity_error | refused artifact EXPERIMENTS/182-ground-truth-contest/bodies.json: secret pattern(s) assigned-credential |
| 24 | 01:58:12 | artifact | wrote STATE.md |
| 25 | 01:58:14 | artifact | wrote STATE-next-actions.md |
| 26 | 01:58:16 | artifact | wrote STATE-next-actions-closed-2.md |
| 27 | 01:58:18 | artifact | wrote STATE-next-actions-closed-3.md |
| 28 | 01:58:20 | artifact | wrote FAILURES.md |
| 29 | 01:58:22 | artifact | wrote FAILURES-findings-44.md |
| 30 | 01:58:25 | artifact | wrote DECISIONS.md |
| 31 | 01:58:28 | artifact | wrote DECISIONS-RECORDS-4.md |
| 32 | 01:58:31 | artifact | wrote RELEASE-MANIFEST.md |
| 33 | 02:01:26 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/bodies.py --rebuild-from-raw |
| 34 | 02:01:43 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/bodies.py --rebuild-from-raw |
| 35 | 02:01:49 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py |
| 36 | 02:02:01 | command | $ python3 EXPERIMENTS/182-ground-truth-contest/overlap.py --power |
| 37 | 02:02:36 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/AMENDMENT-1.md |
| 38 | 02:02:37 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/AMENDMENT-2.md |
| 39 | 02:02:38 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/PROTOCOL.md |
| 40 | 02:02:39 | artifact | wrote EXPERIMENTS/182-ground-truth-contest/RESULT.md |
| 199 | 03:17:42 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-007-fresh-exploration-find-a-concrete-builda/events.jsonl |
| 200 | 03:17:42 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-001-e181-test-whether-supplying-the-specific/commands.log |
| 201 | 03:17:42 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-001-e181-test-whether-supplying-the-specific/events.jsonl |
| 202 | 03:17:42 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-18-002-log-e181-s-two-undeclared-artifacts-that/events.jsonl |
| 203 | 03:17:42 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 204 | 03:17:42 | doc_update | updated DECISIONS-RECORDS-4.md |
| 205 | 03:17:42 | doc_update | updated DECISIONS.md |
| 206 | 03:17:42 | doc_update | updated FAILURES.md |
| 207 | 03:17:42 | doc_update | updated STATE.md |
| 208 | 03:17:43 | session_end | E182 closed the last testable explanation of F136's SELF/EVID gap. The question had to be corrected first: 'is the accepted answer the best answer' na |

_158 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-18-003-measure-whether-e177-s-ground-truth-is-c/events.jsonl
```
