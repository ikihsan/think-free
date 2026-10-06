# Session 2026-10-06-013-package-stage-lines-for-real-use-and-rec

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T12:24:42+00:00
- **Duration:** 5133.6s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Package stage-lines for real use and record the KILL-Q evaluation

## Summary

stage-lines packaged (pyproject, console script, stg wrapper, README install/tests corrected in db622b2); full suite run failed once for the same reason as F018, never re-run; the KILL-Q record was not written

## Next

E041: strongest honest shell baseline vs stg; then record KILL-Q as not_evaluated-by-design with reasons

## Artifacts

_none_

## Commands

2 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 0 | 6614 |
| 3 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 476454 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | stage-lines/README.md |
|   undeclared | stage-lines/pyproject.toml |
|   undeclared | stage-lines/stg |
|   undeclared | stage-lines/stg_cli.py |
|   undeclared | tests/test_decision_files.py |
|   undeclared | tools/originlib/paths.py |
|   undeclared | tools/originlib/reconcile.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:24:42 | session_start | Package stage-lines for real use and record the KILL-Q evaluation |
| 2 | 12:29:13 | command | $ python3 -m unittest discover -s stage-lines |
| 3 | 12:37:10 | command | $ python3 -m unittest discover -s tests -t tests |
| 4 | 12:44:32 | milestone | packaging committed db622b2: pyproject, console script, README fixes, decision lists; tests.test_decision_files green |
| 5 | 13:50:15 | unlogged_change | changed but never declared as an artifact: stage-lines/README.md |
| 6 | 13:50:15 | unlogged_change | changed but never declared as an artifact: stage-lines/pyproject.toml |
| 7 | 13:50:15 | unlogged_change | changed but never declared as an artifact: stage-lines/stg |
| 8 | 13:50:15 | unlogged_change | changed but never declared as an artifact: stage-lines/stg_cli.py |
| 9 | 13:50:15 | unlogged_change | changed but never declared as an artifact: tests/test_decision_files.py |
| 10 | 13:50:15 | unlogged_change | changed but never declared as an artifact: tools/originlib/paths.py |
| 11 | 13:50:15 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 12 | 13:50:15 | session_end | stage-lines packaged (pyproject, console script, stg wrapper, README install/tests corrected in db622b2); full suite run failed once for the same reas |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-013-package-stage-lines-for-real-use-and-rec/events.jsonl
```
