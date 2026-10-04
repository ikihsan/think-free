# Session 2026-10-04-003-t-0027-the-published-claim-commit-must-c

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T00:56:54+00:00
- **Duration:** 402.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

T-0027: the published claim commit must carry the regenerated indexes, and task new must say how to publish without orphaning

## Summary

T-0027 done: a published claim stages the regenerated indexes, so the commit every other VM reads first is lintable. T-0026's verification had passed over a live defect because a lint on the author's own tree cannot see what a pushed commit contains; the new test lints a fetched tree on a second clone. 276 tests green; task verified and completed.

## Next

Read the pushed CI run for T-0027 before claiming it green, and check that the claim commit d3e3a90/580ad67 carried the indexes - that is the first commit in this repository where the claim path did it for itself. Then the two open defects in STATE-defects.md: identifier allocation (a detector, not an allocator) and the missing Python-versions record named in docs/operations/vm-execution.md. STATE.md is at 267 lines and STATE-history.md at 300, so the next session that adds detail to either must split rather than append.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/taskremote.py | b1b9b8450b7c | 10495 |
| tools/originlib/cli_task.py | 3b0b288ebcc4 | 3400 |
| tests/test_task_index_freshness.py | b783f25d10dd | 5012 |
| STATE-defects.md | 8a38cd1bdc69 | 4934 |
| ROADMAP.md | 32e8d4d0dc9b | 11272 |
| docs/process/task-lifecycle.md | 2dfb18d26bc8 | 6096 |
| tasks/T-0027-make-the-published-claim-commit-carry-the-regene.md | 16eadbb42de1 | 3522 |
| docs/INDEX.md | b3761be9a08f | 14411 |
| tasks/INDEX.md | 2b4cae2add53 | 6309 |
| sessions/INDEX.md | e3890d63854a | 6692 |
| STATE.md | f9f792e9d521 | 20257 |

## Commands

3 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'TaskIndexFreshness', '-v'] | 0 | 4808 |
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 148136 |
| 14 | ['tools/origin', 'task', 'verify', 'T-0027'] | 0 | 154273 |

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
| 1 | 00:56:54 | session_start | T-0027: the published claim commit must carry the regenerated indexes, and task new must say how to publish without orphaning |
| 2 | 00:57:13 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k TaskIndexFreshness -v |
| 3 | 01:00:16 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 4 | 01:00:23 | artifact | wrote tools/originlib/taskremote.py |
| 5 | 01:00:23 | artifact | wrote tools/originlib/cli_task.py |
| 6 | 01:00:23 | artifact | wrote tests/test_task_index_freshness.py |
| 7 | 01:00:23 | artifact | wrote STATE-defects.md |
| 8 | 01:00:23 | artifact | wrote ROADMAP.md |
| 9 | 01:00:23 | artifact | wrote docs/process/task-lifecycle.md |
| 10 | 01:00:23 | artifact | wrote tasks/T-0027-make-the-published-claim-commit-carry-the-regene.md |
| 11 | 01:00:23 | artifact | wrote docs/INDEX.md |
| 12 | 01:00:23 | artifact | wrote tasks/INDEX.md |
| 13 | 01:00:23 | artifact | wrote sessions/INDEX.md |
| 14 | 01:02:58 | command | $ tools/origin task verify T-0027 |
| 15 | 01:03:25 | artifact | wrote STATE.md |
| 16 | 01:03:37 | doc_update | updated ROADMAP.md |
| 17 | 01:03:37 | doc_update | updated STATE.md |
| 18 | 01:03:37 | session_end | T-0027 done: a published claim stages the regenerated indexes, so the commit every other VM reads first is lintable. T-0026's verification had passed  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-003-t-0027-the-published-claim-commit-must-c/events.jsonl
```
