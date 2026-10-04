# Session 2026-10-04-019-t-0039-make-acceptance-and-steps-append

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T07:18:16+00:00
- **Duration:** 1031.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

T-0039: make --acceptance and --steps append on task new

## Summary

T-0039: --steps and --acceptance now accumulate, so five criteria reach the task file as five lines. Falsified first against the unmodified parser (3 flags wrote 1 line; only '3. third' of the steps survived), and a fourth control found taskops' unreachable placeholder default, which is now pinned as an empty section. Defect 11 closed; defect 12 recorded for the task-file declaration gap. 422 tests green, doc lint green.

## Next

The half of next-actions 2(b) that survives F020: make the doc lint, release manifest and session steps emit one ::error:: line naming their violation, with a gate that every gate step emits annotations - otherwise a red Documentation lint names a step and nothing else.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/cli_args.py | feadf21c01b7 | 11465 |
| tools/originlib/cli_task.py | e7e98a7a3a4f | 4032 |
| tests/test_tasks.py | 68aaf52e5a1b | 8366 |
| docs/process/task-lifecycle.md | faa11ffa87bc | 8534 |
| docs/reference/cli-reference.md | 081e1f206c30 | 8152 |
| STATE-defects.md | 4e90ce2890a6 | 19967 |
| tests/README.md | a8ac2224b217 | 15067 |

## Commands

5 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_tasks.py'] | 1 | 8307 |
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_tasks.py'] | 1 | 8336 |
| 4 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_tasks.RepeatedFlagTest', '-v'] | 1 | 2008 |
| 5 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_tasks.py'] | 0 | 8694 |
| 14 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 253308 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | tasks/T-0039-make-acceptance-and-steps-append-on-task-new-so.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 07:18:16 | session_start | T-0039: make --acceptance and --steps append on task new |
| 2 | 07:19:33 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_tasks.py |
| 3 | 07:21:08 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_tasks.py |
| 4 | 07:21:16 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_tasks.RepeatedFlagTest -v |
| 5 | 07:21:45 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_tasks.py |
| 6 | 07:23:08 | artifact | wrote tools/originlib/cli_args.py |
| 7 | 07:23:09 | artifact | wrote tools/originlib/cli_task.py |
| 8 | 07:23:09 | artifact | wrote tests/test_tasks.py |
| 9 | 07:23:10 | artifact | wrote docs/process/task-lifecycle.md |
| 10 | 07:23:10 | artifact | wrote docs/reference/cli-reference.md |
| 11 | 07:23:11 | artifact | wrote STATE-defects.md |
| 12 | 07:23:11 | artifact | wrote tests/README.md |
| 13 | 07:23:12 | milestone | T-0039: --steps and --acceptance append; falsified first (3 flags wrote 1 line, and only '3. third' of the steps); a fourth control found taskops' unr |
| 14 | 07:27:25 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 15 | 07:35:28 | unlogged_change | changed but never declared as an artifact: tasks/T-0039-make-acceptance-and-steps-append-on-task-new-so.md |
| 16 | 07:35:28 | session_end | T-0039: --steps and --acceptance now accumulate, so five criteria reach the task file as five lines. Falsified first against the unmodified parser (3  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-019-t-0039-make-acceptance-and-steps-append/events.jsonl
```
