# Session 2026-10-04-015-stop-every-session-event-from-leaving-th

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T05:49:46+00:00
- **Duration:** 473.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Stop every session event from leaving the generated report stale, which reddened CI run 37180487906

## Summary

A third stale-generated-file defect, and the first repair of this family that generalises. Run 37180487906 was red on Documentation lint with all seven Tests jobs green: the session report is rendered from the event stream, so every append invalidates it, and only start and finish regenerated it. A commit between an append and the next write publishes a stale file. T-0026 and T-0027 fixed the same family for the task and docs indexes by rebuilding them in the task commands and did not reach this file, because the appender is not a task command. The repair is in the appenders, so the module API cannot break it - which the first attempt, in the CLI, could. Falsified by removing the two calls: 4 of 5 tests in the new file fail and the control stays green. 400 tests.

## Next

Both gaps from session 012 are still open in STATE-next-actions.md: rule 7 does not read STATE-defects.md's numbering, and a red CI run names a step rather than a test. No task is claimed on the base.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tests/test_report_freshness.py | aa53f0ae03ff | 4165 |
| tools/originlib/sessionlog.py | 73fc58181b48 | 4732 |
| tools/originlib/recorder.py | b16d846f81a0 | 4064 |
| STATE-defects.md | d59165eb5b77 | 15573 |
| docs/process/session-protocol.md | f3a4f670d7be | 9019 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 7 | ['bash', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests; echo "suite exit=$?"; tools/origin doc lint >/dev/null 2>&1; ec | 0 | 235685 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 4 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | STATE.md |
|   undeclared | tests/README.md |
|   undeclared | tests/test_session.py |
|   undeclared | tools/originlib/session.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:49:46 | session_start | Stop every session event from leaving the generated report stale, which reddened CI run 37180487906 |
| 2 | 05:52:57 | artifact | wrote tests/test_report_freshness.py |
| 3 | 05:52:58 | artifact | wrote tools/originlib/sessionlog.py |
| 4 | 05:52:58 | artifact | wrote tools/originlib/recorder.py |
| 5 | 05:52:59 | artifact | wrote STATE-defects.md |
| 6 | 05:52:59 | artifact | wrote docs/process/session-protocol.md |
| 7 | 05:57:02 | command | $ bash -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests; echo "suite exit=$?"; tools/origin doc lint >/dev/null 2>&1; |
| 8 | 05:57:39 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 9 | 05:57:39 | unlogged_change | changed but never declared as an artifact: tests/README.md |
| 10 | 05:57:39 | unlogged_change | changed but never declared as an artifact: tests/test_session.py |
| 11 | 05:57:39 | unlogged_change | changed but never declared as an artifact: tools/originlib/session.py |
| 12 | 05:57:39 | doc_update | updated STATE.md |
| 13 | 05:57:39 | session_end | A third stale-generated-file defect, and the first repair of this family that generalises. Run 37180487906 was red on Documentation lint with all seve |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-015-stop-every-session-event-from-leaving-th/events.jsonl
```
