# Session 2026-10-17-003-run-e174-test-whether-a-mechanical-answe

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-17
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-17T05:42:13+00:00
- **Duration:** 3701.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run E174: test whether a mechanical answer-vocabulary query bridge retrieves a fix document that failure-vocabulary queries miss

## Summary

E175 completed and its kill fired (0 of 21 correct repositories, 20 confident wrong); D117 and F135 recorded. Session was cut mid-doc-lint: lint was red on 6 violations (3 missing origin-meta blocks on other sessions' files, 3 root-level ../ links), the repair was made but never committed. That repair is now committed as e1613583 so the gate every commit runs is green.

## Next

Lint has not been re-run since the repair; re-run doc lint before any commit that depends on it. Next action is E176 or a fresh observation, per STATE-next-actions.md.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E172-discourse-viewcount/RESULT.md | 79fde48313fb | 5926 |
| EXPERIMENTS/E173-github-discussions-viewcount/RESULT.md | c5a8dd4185b8 | 3767 |
| EXPERIMENTS/E172-experiment-results.json | 71e7dc08afe8 | 2594 |
| EXPERIMENTS/E173-experiment-results.json | 7fb1716dbba3 | 3252 |
| FAILURES-findings-42.md | 1e1fbb3bec49 | 13270 |
| FAILURES.md | e01c693b84d6 | 91226 |
| EXPERIMENTS/174-scoped-reach-recompute/PROTOCOL.md | 9cdcbdd47ffe | 2998 |
| EXPERIMENTS/174-scoped-reach-recompute/recompute.py | a14638c8db25 | 9539 |
| EXPERIMENTS/174-scoped-reach-recompute/RESULT.md | 341c21b3520c | 6720 |
| EXPERIMENTS/170-fix-reachability-rank/RESULT.md | 3816012382f9 | 9212 |
| EXPERIMENTS/175-repo-from-report/PROTOCOL-AMENDMENT-1.md | be1cf8d8f0b1 | 2140 |
| EXPERIMENTS/175-repo-from-report/PROTOCOL-AMENDMENT-2.md | d7a99701de0e | 5828 |
| EXPERIMENTS/175-repo-from-report/sample.py | 5d45d3adc391 | 8860 |
| EXPERIMENTS/175-repo-from-report/derive.py | a59e4ba4abd9 | 8792 |
| EXPERIMENTS/175-repo-from-report/qtext.py | 6b48aafa1bdc | 2138 |
| EXPERIMENTS/175-repo-from-report/run.py | 521f8373fb74 | 9318 |
| EXPERIMENTS/175-repo-from-report/sample.json | 4a2228724458 | 189577 |
| EXPERIMENTS/175-repo-from-report/queries.json | ae2c0a5f4cb8 | 2716 |
| EXPERIMENTS/175-repo-from-report/derivation.json | 9ddeb33d716e | 26885 |
| EXPERIMENTS/175-repo-from-report/RESULT.md | 66beb5319980 | 7858 |
| FAILURES-findings-43.md | 673fa4efa305 | 3864 |
| HYPOTHESES.md | e63225b80f88 | 27354 |
| STATE.md | 97c9e5d6e85e | 21531 |
| DECISIONS-RECORDS-3.md | fa1a0cd1f69b | 6475 |
| DECISIONS.md | d7ef4b788a45 | 27068 |
| STATE-next-actions.md | bf98986407bd | 20904 |

## Commands

19 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 9 | ['git', 'commit', '-q', '-m', 'F133: two identifiers, four contradictory records, none reproducible\n\nE172 and E173 were written twice each, on diffe | 0 | 397 |
| 10 | ['python3', 'EXPERIMENTS/174-scoped-reach-recompute/recompute.py'] | 0 | 479 |
| 11 | ['python3', 'EXPERIMENTS/174-scoped-reach-recompute/recompute.py'] | 0 | 200 |
| 12 | ['python3', 'EXPERIMENTS/174-scoped-reach-recompute/recompute.py'] | 0 | 297 |
| 13 | ['python3', 'EXPERIMENTS/174-scoped-reach-recompute/recompute.py'] | 0 | 215 |
| 14 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 1 | 4108 |
| 15 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 0 | 3283 |
| 16 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 1 | 18293 |
| 17 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 0 | 17690 |
| 18 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 0 | 16574 |
| 19 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 1 | 15614 |
| 20 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 1 | 16786 |
| 21 | ['python3', 'EXPERIMENTS/175-repo-from-report/sample.py'] | 0 | 17377 |
| 22 | ['python3', 'EXPERIMENTS/175-repo-from-report/run.py'] | 0 | 40526 |
| 23 | ['python3', 'EXPERIMENTS/175-repo-from-report/run.py'] | 0 | 41295 |
| 24 | ['python3', 'EXPERIMENTS/175-repo-from-report/run.py'] | 0 | 52310 |
| 25 | ['python3', 'EXPERIMENTS/175-repo-from-report/run.py'] | 0 | 43425 |
| 45 | ['./tools/origin', 'doc', 'index'] | 0 | 11711 |
| 49 | ['./tools/origin', 'doc', 'lint'] | 2 | 908866 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 19 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | CLASSIFICATION-PROTOTYPE.md |
|   undeclared | EXPERIMENTS/171-resolution-fact-locus/RESULT.md |
|   undeclared | EXPERIMENTS/175-repo-from-report/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E172-discourse-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E173-github-discussions-viewcount/PROTOCOL-E173.md |
|   undeclared | PROTOCOL-E172.md |
|   undeclared | sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/commands.log |
|   undeclared | sessions/2026-10-16-006-e171-test-whether-the-component-s-publis/events.jsonl |
|   undeclared | sessions/2026-10-16-007-e171-finish-the-pre-condition-screen-on/commands.log |
|   undeclared | sessions/2026-10-16-007-e171-finish-the-pre-condition-screen-on/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:42:13 | session_start | Run E174: test whether a mechanical answer-vocabulary query bridge retrieves a fix document that failure-vocabulary queries miss |
| 2 | 05:44:17 | artifact | wrote EXPERIMENTS/E172-discourse-viewcount/RESULT.md |
| 3 | 05:44:19 | artifact | wrote EXPERIMENTS/E173-github-discussions-viewcount/RESULT.md |
| 4 | 05:44:20 | artifact | wrote EXPERIMENTS/E172-experiment-results.json |
| 5 | 05:44:22 | artifact | wrote EXPERIMENTS/E173-experiment-results.json |
| 6 | 05:44:23 | artifact | wrote FAILURES-findings-42.md |
| 7 | 05:44:25 | artifact | wrote FAILURES.md |
| 8 | 05:44:26 | milestone | reconciled the uncommitted E172/E173 record: F133 records that two identifiers carry four mutually contradictory records with no raw data, and E172/E1 |
| 9 | 05:44:46 | command | $ git commit -q -m F133: two identifiers, four contradictory records, none reproducible  E172 and E173 were written twice each, on different v |
| 10 | 05:45:45 | command | $ python3 EXPERIMENTS/174-scoped-reach-recompute/recompute.py |
| 11 | 05:46:26 | command | $ python3 EXPERIMENTS/174-scoped-reach-recompute/recompute.py |
| 12 | 05:46:53 | command | $ python3 EXPERIMENTS/174-scoped-reach-recompute/recompute.py |
| 13 | 05:47:04 | command | $ python3 EXPERIMENTS/174-scoped-reach-recompute/recompute.py |
| 14 | 05:50:09 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 15 | 05:50:20 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 16 | 05:51:06 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 17 | 05:51:29 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 18 | 05:52:04 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 19 | 05:52:36 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 20 | 05:52:57 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 21 | 05:53:21 | command | $ python3 EXPERIMENTS/175-repo-from-report/sample.py |
| 22 | 05:54:25 | command | $ python3 EXPERIMENTS/175-repo-from-report/run.py |
| 23 | 05:55:59 | command | $ python3 EXPERIMENTS/175-repo-from-report/run.py |
| 24 | 05:57:13 | command | $ python3 EXPERIMENTS/175-repo-from-report/run.py |
| 25 | 05:58:12 | command | $ python3 EXPERIMENTS/175-repo-from-report/run.py |
| 26 | 05:58:47 | artifact | wrote EXPERIMENTS/174-scoped-reach-recompute/PROTOCOL.md |
| 27 | 05:58:48 | artifact | wrote EXPERIMENTS/174-scoped-reach-recompute/recompute.py |
| 28 | 05:58:50 | artifact | wrote EXPERIMENTS/174-scoped-reach-recompute/RESULT.md |
| 29 | 05:58:52 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/RESULT.md |
| 30 | 05:58:53 | artifact | wrote EXPERIMENTS/175-repo-from-report/PROTOCOL-AMENDMENT-1.md |
| 31 | 05:58:56 | artifact | wrote EXPERIMENTS/175-repo-from-report/PROTOCOL-AMENDMENT-2.md |
| 32 | 05:58:58 | artifact | wrote EXPERIMENTS/175-repo-from-report/sample.py |
| 33 | 05:58:59 | artifact | wrote EXPERIMENTS/175-repo-from-report/derive.py |
| 34 | 05:59:01 | artifact | wrote EXPERIMENTS/175-repo-from-report/qtext.py |
| 35 | 05:59:02 | artifact | wrote EXPERIMENTS/175-repo-from-report/run.py |
| 36 | 05:59:04 | artifact | wrote EXPERIMENTS/175-repo-from-report/sample.json |
| 37 | 05:59:05 | artifact | wrote EXPERIMENTS/175-repo-from-report/queries.json |
| 38 | 05:59:07 | artifact | wrote EXPERIMENTS/175-repo-from-report/derivation.json |
| 39 | 05:59:08 | artifact | wrote EXPERIMENTS/175-repo-from-report/RESULT.md |
| 40 | 05:59:11 | artifact | wrote FAILURES-findings-43.md |
| 64 | 06:43:54 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-002-continue-think-free-mission-design-and-r/events.jsonl |
| 65 | 06:43:54 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 66 | 06:43:54 | unlogged_change | changed but never declared as an artifact: tasks/T-0095-e172-fresh-observation-view-count-principle-and.md |
| 67 | 06:43:54 | unlogged_change | changed but never declared as an artifact: test_prototype.py |
| 68 | 06:43:54 | unlogged_change | changed but never declared as an artifact: tools/viewcount_framework.py |
| 69 | 06:43:55 | doc_update | updated DECISIONS.md |
| 70 | 06:43:55 | doc_update | updated FAILURES.md |
| 71 | 06:43:55 | doc_update | updated HYPOTHESES.md |
| 72 | 06:43:55 | doc_update | updated STATE.md |
| 73 | 06:43:55 | session_end | E175 completed and its kill fired (0 of 21 correct repositories, 20 confident wrong); D117 and F135 recorded. Session was cut mid-doc-lint: lint was r |

_23 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-17-003-run-e174-test-whether-a-mechanical-answe/events.jsonl
```
