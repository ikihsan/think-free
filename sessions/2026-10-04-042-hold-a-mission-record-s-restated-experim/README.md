# Session 2026-10-04-042-hold-a-mission-record-s-restated-experim

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T16:34:13+00:00
- **Duration:** 5192.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `task/T-0056-instance-20260717-0944`

## Goal

Hold a mission record's restated experiment number to the artifact it names

## Summary

T-0056: docs/process/experiment-protocol.md claimed 113/115 -> 113/113 checked cases for an artifact whose cases_with_oracle is 115, wrong in the commit that published the artifact. Found by hand, priced with a committed sweep, and closed by resultnumbers.py, a rule that decides the property from the number's shape because the obvious rule is green on the defect (113 also sits at patch_cost_sensitivity/*/cases). Falsified three ways by mutation; the blindness of the rejected rule is asserted. STATE-defects.md split at its cap with defectlist.py reading both files. 575 tests, doc lint and preflight green.

## Next

The coverage this leaves is stated rather than hidden: STATE.md's dashboard row names all nine experiments and is not attributable, and a count restated in prose is unread. D045 names requiring a citation as the design that would generalise, which is a change to the index's shape rather than a gate.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/sweep_result_numbers.py | 874fd9c59b3b | 9332 |
| tools/originlib/resultnumbers.py | 1c4af6d16308 | 9214 |
| tools/mutate_result_rule.py | bde1f214f407 | 5376 |
| tests/test_result_numbers.py | d24fa4fc492d | 11511 |
| tools/originlib/defectlist.py | 9f23507c7d79 | 7157 |
| tests/test_defectlist.py | 1e2f6abe8390 | 14289 |
| STATE-defects-2.md | f4a342db897a | 7781 |
| STATE-defects.md | c07ad5224aaa | 18164 |
| docs/policy/gate-falsification.md | ca3d55edb2a9 | 8725 |
| docs/operations/ci.md | 8f74b4ba7bad | 17935 |
| RELEASE-MANIFEST.md | fc4ed4c71955 | 4586 |
| STATE.md | f5a1ec5f80d9 | 26457 |
| ROADMAP.md | fe3f8eb99690 | 20081 |
| STATE-next-actions.md | fe53ac2dde56 | 18091 |
| STATE-history-2.md | 194b7b4066bb | 20512 |
| STATE-defects.md | c07ad5224aaa | 18164 |
| STATE-defects-2.md | f4a342db897a | 7781 |
| tests/README.md | 61674c0582da | 29645 |
| docs/policy/gate-falsification.md | 4b3d4875478a | 10394 |
| docs/operations/ci.md | 8f74b4ba7bad | 17935 |
| RELEASE-MANIFEST.md | fc4ed4c71955 | 4586 |
| DECISIONS-RECORDS.md | 4fd9f02b2fe9 | 19595 |
| DECISIONS.md | 5545ec0389c0 | 5623 |
| tools/originlib/defectlist.py | a156bb45b8cc | 7323 |
| tools/originlib/defectlist.py | f6cf40acb308 | 7551 |
| tasks/T-0056-hold-a-mission-record-s-restated-experiment-numb.md | e757f725f1f9 | 2943 |

## Commands

85 captured, 48 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'tools/sweep_result_numbers.py', '--verbose'] | 0 | 204 |
| 4 | ['python3', 'tools/sweep_result_numbers.py', '--verbose'] | 0 | 499 |
| 5 | ['python3', 'tools/sweep_result_numbers.py'] | 0 | 492 |
| 6 | ['tools/origin', 'doc', 'lint'] | 2 | 2920 |
| 10 | ['python3', '-m', 'unittest', 'tests.test_result_numbers', '-v'] | 1 | 324 |
| 11 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers', '-v'] | 1 | 1090 |
| 12 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers', '-v'] | 1 | 3824 |
| 13 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers'] | 1 | 5311 |
| 14 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers'] | 0 | 4402 |
| 15 | ['python3', 'tools/mutate_result_rule.py'] | 0 | 18996 |
| 19 | ['tools/origin', 'doc', 'lint'] | 0 | 3232 |
| 20 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 310516 |
| 21 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers', '-v'] | 1 | 6402 |
| 22 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers'] | 0 | 4396 |
| 23 | ['python3', 'tools/mutate_result_rule.py'] | 1 | 5831 |
| 24 | ['python3', 'tools/mutate_result_rule.py'] | 1 | 5518 |
| 25 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers'] | 0 | 7720 |
| 26 | ['python3', 'tools/mutate_result_rule.py'] | 0 | 20330 |
| 27 | ['tools/origin', 'doc', 'lint'] | 2 | 2695 |
| 28 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_result_numbers', 'tests.test_result_numbers_falsified'] | 0 | 5224 |
| 29 | ['python3', 'tools/mutate_result_rule.py'] | 0 | 21415 |
| 30 | ['tools/origin', 'doc', 'lint'] | 0 | 2521 |
| 31 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 305323 |
| 32 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_defectlist'] | 1 | 4387 |
| 33 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_defectlist'] | 1 | 4189 |
| 34 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_defectlist'] | 0 | 4303 |
| 35 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_defectlist'] | 1 | 5304 |
| 36 | ['tools/origin', 'doc', 'lint'] | 0 | 2693 |
| 37 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_defectlist'] | 1 | 4398 |
| 38 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_defectlist'] | 0 | 4322 |
| 39 | ['tools/origin', 'doc', 'lint'] | 2 | 4395 |
| 40 | ['tools/origin', 'doc', 'lint'] | 2 | 2700 |
| 41 | ['tools/origin', 'doc', 'lint'] | 2 | 2620 |
| 42 | ['tools/origin', 'doc', 'lint'] | 2 | 4295 |
| 43 | ['tools/origin', 'doc', 'lint'] | 2 | 2763 |
| 44 | ['tools/origin', 'doc', 'lint'] | 2 | 2694 |
| 45 | ['tools/origin', 'doc', 'lint'] | 2 | 2623 |
| 46 | ['tools/origin', 'doc', 'lint'] | 2 | 2794 |
| 47 | ['tools/origin', 'doc', 'lint'] | 0 | 3088 |
| 48 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 310921 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 5 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | FAILURES-findings-5.md |
|   undeclared | FAILURES.md |
|   undeclared | docs/process/experiment-protocol.md |
|   undeclared | tests/test_result_numbers_falsified.py |
|   undeclared | tools/originlib/doclint.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:34:13 | session_start | Hold a mission record's restated experiment number to the artifact it names |
| 2 | 16:34:19 | milestone | confirmed the defect by hand: 113/113 in the protocol row against cases_with_oracle=115 in the artifact; a naive anywhere-in-JSON check passes it beca |
| 3 | 16:34:49 | command | $ python3 tools/sweep_result_numbers.py --verbose |
| 4 | 16:35:17 | command | $ python3 tools/sweep_result_numbers.py --verbose |
| 5 | 16:35:40 | command | $ python3 tools/sweep_result_numbers.py |
| 6 | 16:38:55 | command | $ tools/origin doc lint |
| 7 | 16:39:02 | artifact | wrote tools/sweep_result_numbers.py |
| 8 | 16:39:03 | artifact | wrote tools/originlib/resultnumbers.py |
| 9 | 16:39:04 | milestone | gate wired into doc lint and firing on the committed row: docs/process/experiment-protocol.md reports 113/113 against the artifact's declared counts [ |
| 10 | 16:39:45 | command | $ python3 -m unittest tests.test_result_numbers -v |
| 11 | 16:39:51 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers -v |
| 12 | 16:40:28 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers -v |
| 13 | 16:41:51 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers |
| 14 | 16:42:19 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers |
| 15 | 16:43:04 | command | $ python3 tools/mutate_result_rule.py |
| 16 | 16:43:12 | artifact | wrote tools/mutate_result_rule.py |
| 17 | 16:43:12 | artifact | wrote tests/test_result_numbers.py |
| 18 | 16:43:13 | milestone | falsified three ways with mutation: the declared-count restriction removed, the fraction clause removed, and the unreadable-artifact report removed ea |
| 19 | 16:43:54 | command | $ tools/origin doc lint |
| 20 | 16:49:10 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 21 | 16:49:49 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers -v |
| 22 | 16:50:13 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers |
| 23 | 16:50:19 | command | $ python3 tools/mutate_result_rule.py |
| 24 | 16:50:37 | command | $ python3 tools/mutate_result_rule.py |
| 25 | 16:51:28 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers |
| 26 | 16:51:48 | command | $ python3 tools/mutate_result_rule.py |
| 27 | 16:54:52 | command | $ tools/origin doc lint |
| 28 | 16:56:10 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_result_numbers tests.test_result_numbers_falsified |
| 29 | 16:57:01 | command | $ python3 tools/mutate_result_rule.py |
| 30 | 16:57:04 | command | $ tools/origin doc lint |
| 31 | 17:02:15 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 32 | 17:07:07 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_defectlist |
| 33 | 17:07:28 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_defectlist |
| 34 | 17:07:43 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_defectlist |
| 35 | 17:08:07 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_defectlist |
| 36 | 17:08:10 | command | $ tools/origin doc lint |
| 37 | 17:08:23 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_defectlist |
| 38 | 17:08:50 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_defectlist |
| 39 | 17:11:14 | command | $ tools/origin doc lint |
| 40 | 17:12:15 | command | $ tools/origin doc lint |
| 122 | 18:00:46 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 123 | 18:00:46 | unlogged_change | changed but never declared as an artifact: docs/process/experiment-protocol.md |
| 124 | 18:00:46 | unlogged_change | changed but never declared as an artifact: tests/test_result_numbers_falsified.py |
| 125 | 18:00:46 | unlogged_change | changed but never declared as an artifact: tools/originlib/doclint.py |
| 126 | 18:00:46 | doc_update | updated DECISIONS-RECORDS.md |
| 127 | 18:00:46 | doc_update | updated DECISIONS.md |
| 128 | 18:00:46 | doc_update | updated FAILURES.md |
| 129 | 18:00:46 | doc_update | updated ROADMAP.md |
| 130 | 18:00:46 | doc_update | updated STATE.md |
| 131 | 18:00:46 | session_end | T-0056: docs/process/experiment-protocol.md claimed 113/115 -> 113/113 checked cases for an artifact whose cases_with_oracle is 115, wrong in the comm |

_81 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-042-hold-a-mission-record-s-restated-experim/events.jsonl
```
