# Session 2026-10-04-002-t-0026-make-task-new-regenerate-tasks-in

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T00:43:21+00:00
- **Duration:** 560.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

T-0026: make task new regenerate tasks/INDEX.md so a created task is never an orphan

## Summary

T-0026 done: task new/claim/complete/release rebuild the generated indexes, so a created task is never an orphan - the cause of two red CI runs on 2026-10-03. Falsified first (4 of 5 new tests fail without it; the negative control does not move). 274 tests green; task verified and completed.

## Next

Read the pushed CI runs for T-0025 and T-0026 before claiming them green: neither has run on the runner yet, and this record has just been wrong about a run once. Then the two open defects in STATE-defects.md: identifier allocation (a detector, not an allocator) and the missing Python-versions record named in docs/operations/vm-execution.md. STATE.md is at 263 lines and STATE-history.md at 300, so the next session that adds detail to either must split rather than append.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/taskops.py | e776d0966c6b | 4464 |
| tools/originlib/tasks.py | d2dac0980aa6 | 8613 |
| tools/originlib/docindex.py | b7f6cffb1158 | 6832 |
| tools/originlib/cli_repo.py | c8aa2f4c7403 | 4233 |
| tests/test_task_index_freshness.py | 39bc18f99efc | 3184 |
| STATE-defects.md | 574410cafb5d | 4579 |
| ROADMAP.md | 3d51d911e63f | 11251 |
| docs/process/task-lifecycle.md | f277ed0c8b19 | 5569 |
| docs/reference/cli-reference.md | b5a9c5ab8d80 | 7000 |
| tests/README.md | 75ab383fd65c | 4544 |
| tasks/T-0026-make-task-new-leave-no-orphan-a-new-task-file-re.md | 1d121698bdec | 4255 |
| docs/INDEX.md | 8ffee7432473 | 14218 |
| tasks/INDEX.md | 340ae84b9ce7 | 6108 |
| sessions/INDEX.md | 8b763e238ae4 | 6665 |
| STATE.md | f397eda14f1c | 19981 |

## Commands

6 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'TaskIndexFreshness', '-v'] | 1 | 2014 |
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'TaskIndexFreshness', '-v'] | 0 | 4202 |
| 4 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'TaskIndexFreshness', '-v'] | 1 | 2102 |
| 5 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'TaskIndexFreshness'] | 0 | 2308 |
| 12 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 145534 |
| 23 | ['tools/origin', 'task', 'verify', 'T-0026'] | 0 | 148393 |

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
| 1 | 00:43:21 | session_start | T-0026: make task new regenerate tasks/INDEX.md so a created task is never an orphan |
| 2 | 00:43:39 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k TaskIndexFreshness -v |
| 3 | 00:44:56 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k TaskIndexFreshness -v |
| 4 | 00:45:03 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k TaskIndexFreshness -v |
| 5 | 00:45:10 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k TaskIndexFreshness |
| 6 | 00:45:16 | milestone | orphan defect falsified (4 of 5 tests fail without the rebuild) and repaired: create/claim/transition rebuild the generated indexes |
| 7 | 00:45:17 | artifact | wrote tools/originlib/taskops.py |
| 8 | 00:45:17 | artifact | wrote tools/originlib/tasks.py |
| 9 | 00:45:17 | artifact | wrote tools/originlib/docindex.py |
| 10 | 00:45:17 | artifact | wrote tools/originlib/cli_repo.py |
| 11 | 00:45:17 | artifact | wrote tests/test_task_index_freshness.py |
| 12 | 00:47:43 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 13 | 00:48:48 | artifact | wrote STATE-defects.md |
| 14 | 00:48:48 | artifact | wrote ROADMAP.md |
| 15 | 00:48:48 | artifact | wrote docs/process/task-lifecycle.md |
| 16 | 00:48:48 | artifact | wrote docs/reference/cli-reference.md |
| 17 | 00:48:48 | artifact | wrote tests/README.md |
| 18 | 00:48:48 | artifact | wrote tasks/T-0026-make-task-new-leave-no-orphan-a-new-task-file-re.md |
| 19 | 00:48:48 | artifact | wrote docs/INDEX.md |
| 20 | 00:48:48 | artifact | wrote tasks/INDEX.md |
| 21 | 00:48:48 | artifact | wrote sessions/INDEX.md |
| 22 | 00:49:39 | artifact | wrote STATE.md |
| 23 | 00:52:08 | command | $ tools/origin task verify T-0026 |
| 24 | 00:52:42 | doc_update | updated ROADMAP.md |
| 25 | 00:52:42 | doc_update | updated STATE.md |
| 26 | 00:52:42 | session_end | T-0026 done: task new/claim/complete/release rebuild the generated indexes, so a created task is never an orphan - the cause of two red CI runs on 202 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-002-t-0026-make-task-new-regenerate-tasks-in/events.jsonl
```
