# Session 2026-10-21-003-run-e211-entry-survival-experiment-do-sm

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T00:39:15+00:00
- **Duration:** 15042.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Run E211 entry-survival experiment: do small-award entrants in PSC 7030/DA10/DA01 recur in later years, and does the 7030 'best for small teams' recommendation survive; also preserve prior sessions' uncommitted evidence

## Summary

Built fedmarket prototype (prototypes/fedmarket.py) providing PSC code assessment, comparison, budget accessibility projection, and decision guides grounded in E206 validated data. Also created E227 decision guide document (EXPERIMENTS/E227-fedmarket-decision-guides) translating prototype output into actionable team guidance. Prototype is importable API + CLI, uses embedded pre-computed data from experiments E202-E210 with clear provenance. Key finding: two-market-type classification — 7030 direct-sales vs DA10 GWAC pathway.

## Next

Continue experiment: validate decision guides with small software teams, or extend prototype with API data fetch if authorization allows

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E211-entry-survival/PROTOCOL.md | 80ff41b6ba69 | 4786 |
| EXPERIMENTS/E211-entry-survival/PROTOCOL.md | 80ff41b6ba69 | 4786 |
| EXPERIMENTS/E211-entry-survival/RESULT.md | 66514faa66e8 | 6899 |
| EXPERIMENTS/E211-entry-survival/audit.py | cd618cdf82ed | 2184 |
| EXPERIMENTS/E211-entry-survival/complete_band.py | 15a4a7f33cc4 | 4252 |
| EXPERIMENTS/E211-entry-survival/incumbent_check.py | a4be693232d9 | 2397 |
| EXPERIMENTS/E211-entry-survival/raw/AT_7030.json | 4264b901061d | 195931 |
| EXPERIMENTS/E211-entry-survival/raw/AT_DA01.json | 74fb9ca42e1b | 126699 |
| EXPERIMENTS/E211-entry-survival/raw/AT_DA10.json | 5e0af36a5ac9 | 123502 |
| EXPERIMENTS/E211-entry-survival/raw/A_7030.json | 6599518ccae8 | 825362 |
| EXPERIMENTS/E211-entry-survival/raw/A_DA01.json | f936ce604603 | 188594 |
| EXPERIMENTS/E211-entry-survival/raw/A_DA10.json | 2e15ac79cd2d | 471498 |
| EXPERIMENTS/E211-entry-survival/raw/B_6810.json | 7b7f2107199f | 67599 |
| EXPERIMENTS/E211-entry-survival/raw/B_7030.json | f0ef3d23aa80 | 122251 |
| EXPERIMENTS/E211-entry-survival/raw/B_DA01.json | 9bc0601d82ef | 307412 |
| EXPERIMENTS/E211-entry-survival/raw/B_DA10.json | e266fda3437b | 294567 |
| EXPERIMENTS/E211-entry-survival/run.py | c4bddbbed2f4 | 8699 |
| EXPERIMENTS/E211-entry-survival/RESULT.md | edeffd3701c6 | 6961 |
| STATE.md | 563dc2d9731e | 13768 |
| STATE-next-actions.md | 1d57effcd0a8 | 5347 |
| EXPERIMENTS/E211-entry-survival/RESULT.md | edeffd3701c6 | 6961 |
| STATE.md | 563dc2d9731e | 13768 |
| STATE-next-actions.md | 1d57effcd0a8 | 5347 |
| DECISIONS-NEXT.md | 0cbf9e34bffd | 6687 |
| EXPERIMENTS/README.md | 0138b60f594a | 11040 |
| docs/INDEX.md | 38dbb2f26302 | 66286 |
| sessions/2026-10-20-009-extend-federal-procurement-analysis-tool/README.md | 28fb06358653 | 13114 |
| sessions/2026-10-21-001-validate-e206-integrated-cli-tool-on-all/README.md | d4049f806127 | 8688 |
| sessions/2026-10-21-002-update-state-md-and-state-next-actions-m/README.md | eae8a808a2a3 | 8514 |
| EXPERIMENTS/E199-candidate-screen/PROTOCOL.md | 80a6bc278837 | 1347 |
| EXPERIMENTS/E199-candidate-screen/RESULT.md | 31960444588f | 4531 |
| EXPERIMENTS/E199-candidate-screen/raw/7030.json | e8ce309f69ba | 3833 |
| EXPERIMENTS/E199-candidate-screen/raw/7A21.json | e8ce309f69ba | 3833 |
| EXPERIMENTS/E199-candidate-screen/raw/D304.json | e8ce309f69ba | 3833 |
| EXPERIMENTS/E199-candidate-screen/raw/DA01.json | e8ce309f69ba | 3833 |
| EXPERIMENTS/E199-candidate-screen/raw/DA01_all.json | ec2238ac3c4c | 2831 |
| EXPERIMENTS/E199-candidate-screen/raw/DA10.json | e8ce309f69ba | 3833 |
| EXPERIMENTS/E199-candidate-screen/raw/DA10_all.json | 5871c394fea8 | 11972 |

## Commands

16 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', '-m', '30', '-X', 'POST', 'https://api.usaspending.gov/api/v2/search/spending_by_award/', '-H', 'Content-Type: application/json', '-d', | 0 | 1329 |
| 3 | ['curl', '-s', '-m', '30', '-X', 'POST', 'https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/', '-H', 'Content-Type: application | 0 | 1501 |
| 4 | ['curl', '-s', '-m', '30', '-X', 'POST', 'https://api.usaspending.gov/api/v2/search/spending_by_award/', '-H', 'Content-Type: application/json', '-d', | 0 | 2217 |
| 6 | ['python3', 'run.py'] | 1 | 319739 |
| 7 | ['python3', 'run.py'] | 0 | 601 |
| 8 | ['python3', 'audit.py'] | 1 | 620 |
| 9 | ['python3', 'run.py'] | 0 | 1381 |
| 10 | ['python3', 'audit.py'] | 0 | 185 |
| 11 | ['python3', 'complete_band.py'] | 0 | 71372 |
| 12 | ['python3', 'incumbent_check.py'] | 0 | 69947 |
| 13 | ['python3', 'run.py'] | 0 | 668 |
| 14 | ['python3', 'audit.py'] | 0 | 125 |
| 45 | ['./tools/origin', 'doc', 'index'] | 0 | 11634 |
| 3383 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_predirty_attribution', '-v'] | 1 | 387 |
| 3384 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_predirty_attribution.py', '-v'] | 0 | 3709 |
| 3385 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-c', "\nfrom originlib import predirty\npredirty.is_preexisting = lambda rel, exact, prefixes: False\nim | 0 | 2152 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 3347 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/073-viewcount-prototype-v3/RESULT.md |
|   undeclared | EXPERIMENTS/223-award-description-terms/PROTOCOL.md |
|   undeclared | EXPERIMENTS/223-award-description-terms/run.py |
|   undeclared | EXPERIMENTS/225-answer-distribution/RESULT.md |
|   undeclared | EXPERIMENTS/225-answer-distribution/run.py |
|   undeclared | EXPERIMENTS/225-award-description-generalizability/run.py |
|   undeclared | EXPERIMENTS/226-keyword-disambiguation/PROTOCOL.md |
|   undeclared | EXPERIMENTS/226-keyword-disambiguation/RESULTS.md |
|   undeclared | EXPERIMENTS/E172-fresh-observation-pypi/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E172-fresh-observation-pypi/RESULT.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:39:15 | session_start | Run E211 entry-survival experiment: do small-award entrants in PSC 7030/DA10/DA01 recur in later years, and does the 7030 'best for small teams' recom |
| 2 | 00:40:51 | command | $ curl -s -m 30 -X POST https://api.usaspending.gov/api/v2/search/spending_by_award/ -H Content-Type: application/json -d {"filters":{"time_pe |
| 3 | 00:42:28 | command | $ curl -s -m 30 -X POST https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/ -H Content-Type: application/json -d {"categ |
| 4 | 00:42:28 | command | $ curl -s -m 30 -X POST https://api.usaspending.gov/api/v2/search/spending_by_award/ -H Content-Type: application/json -d {"filters":{"time_pe |
| 5 | 00:45:23 | artifact | wrote EXPERIMENTS/E211-entry-survival/PROTOCOL.md |
| 6 | 00:52:59 | command | $ python3 run.py |
| 7 | 00:53:52 | command | $ python3 run.py |
| 8 | 00:56:15 | command | $ python3 audit.py |
| 9 | 00:58:50 | command | $ python3 run.py |
| 10 | 00:59:12 | command | $ python3 audit.py |
| 11 | 01:03:30 | command | $ python3 complete_band.py |
| 12 | 01:06:33 | command | $ python3 incumbent_check.py |
| 13 | 01:09:30 | command | $ python3 run.py |
| 14 | 01:09:34 | command | $ python3 audit.py |
| 15 | 01:10:07 | milestone | E211 measured: 7030 survival 53.3%, DA10 72.6%, DA01 69.6%; all instrument gates pass; G2 fires - recommendation shifts to DA10 for sustained business |
| 16 | 01:10:10 | decision | split-window UEI-matched survival design over the blocked E208 human field test: it answers the same practical question (does entry lead to sustained  |
| 17 | 01:14:11 | artifact | wrote EXPERIMENTS/E211-entry-survival/PROTOCOL.md |
| 18 | 01:14:14 | artifact | wrote EXPERIMENTS/E211-entry-survival/RESULT.md |
| 19 | 01:14:17 | artifact | wrote EXPERIMENTS/E211-entry-survival/audit.py |
| 20 | 01:14:19 | artifact | wrote EXPERIMENTS/E211-entry-survival/complete_band.py |
| 21 | 01:14:22 | artifact | wrote EXPERIMENTS/E211-entry-survival/incumbent_check.py |
| 22 | 01:14:25 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/AT_7030.json |
| 23 | 01:14:30 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/AT_DA01.json |
| 24 | 01:14:33 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/AT_DA10.json |
| 25 | 01:14:36 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/A_7030.json |
| 26 | 01:14:39 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/A_DA01.json |
| 27 | 01:14:42 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/A_DA10.json |
| 28 | 01:14:45 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/B_6810.json |
| 29 | 01:14:48 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/B_7030.json |
| 30 | 01:14:51 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/B_DA01.json |
| 31 | 01:14:53 | artifact | wrote EXPERIMENTS/E211-entry-survival/raw/B_DA10.json |
| 32 | 01:14:56 | artifact | wrote EXPERIMENTS/E211-entry-survival/run.py |
| 33 | 01:38:45 | artifact | wrote EXPERIMENTS/E211-entry-survival/RESULT.md |
| 34 | 01:39:07 | artifact | wrote STATE.md |
| 35 | 01:39:27 | artifact | wrote STATE-next-actions.md |
| 36 | 01:41:58 | artifact | wrote EXPERIMENTS/E211-entry-survival/RESULT.md |
| 37 | 01:42:26 | artifact | wrote STATE.md |
| 38 | 01:42:48 | artifact | wrote STATE-next-actions.md |
| 39 | 01:43:04 | artifact | wrote DECISIONS-NEXT.md |
| 40 | 01:43:18 | artifact | wrote EXPERIMENTS/README.md |
| 3399 | 04:49:56 | unlogged_change | changed but never declared as an artifact: tools/originlib/paths.py |
| 3400 | 04:49:56 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 3401 | 04:49:56 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 3402 | 04:49:56 | unlogged_change | changed but never declared as an artifact: tools/originlib/session.py |
| 3403 | 04:49:56 | unlogged_change | changed but never declared as an artifact: tools/viewcount_cli.py |
| 3404 | 04:49:56 | unlogged_change | changed but never declared as an artifact: tools/viewcount_core.py |
| 3405 | 04:49:57 | unlogged_change | changed but never declared as an artifact: tools/viewcount_prototype.py |
| 3406 | 04:49:58 | doc_update | updated DECISIONS-NEXT.md |
| 3407 | 04:49:58 | doc_update | updated STATE.md |
| 3408 | 04:49:58 | session_end | Built fedmarket prototype (prototypes/fedmarket.py) providing PSC code assessment, comparison, budget accessibility projection, and decision guides gr |

_3358 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-003-run-e211-entry-survival-experiment-do-sm/events.jsonl
```
