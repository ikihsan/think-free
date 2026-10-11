# Session 2026-10-10-008-measure-import-error-population-asking-w

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T08:45:33+00:00
- **Duration:** 1373.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure import-error population asking 'which distribution provides this module' on Stack Overflow, GitHub issues, and CPython/library trackers to validate pyprovides resolver demand

## Summary

E091 import-error population experiment completed. ALL GATES PASS: 2.91% (25/858) of Python import-error reports on Stack Overflow and GitHub name a module but no distribution, exceeding the 1% kill gate. The pyprovides resolver has a measurable demand population.

## Next

Record the decision in DECISIONS.md and update STATE.md with the new finding. Consider building a query-time reverse index (module → distribution) as a service, or integrating with IDE/error-reporting tools.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/091-import-error-population/run.py | 5f646b754b4f | 3147 |
| EXPERIMENTS/091-import-error-population/PROTOCOL.md | cc601ca7859e | 5105 |
| EXPERIMENTS/091-import-error-population/classify.py | 7deab7b52f0e | 11767 |
| EXPERIMENTS/091-import-error-population/classified.jsonl | 9021dee19abf | 264517 |
| EXPERIMENTS/091-import-error-population/harvest.py | 693b865f5f46 | 7197 |
| EXPERIMENTS/091-import-error-population/README.md | 9a9c66c5b8c6 | 5473 |
| EXPERIMENTS/091-import-error-population/evaluate_gates.py | 7af968e29054 | 2459 |
| EXPERIMENTS/091-import-error-population/results.json | a03fe45fae78 | 567 |
| EXPERIMENTS/091-import-error-population/constants.py | 7774fb22ac8f | 4739 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   error | DECISIONS.md was not updated although the session recorded decision |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:45:33 | session_start | Measure import-error population asking 'which distribution provides this module' on Stack Overflow, GitHub issues, and CPython/library trackers to val |
| 2 | 08:45:40 | milestone | Session started. Now designing the import-error population measurement experiment. |
| 3 | 08:55:31 | artifact | wrote EXPERIMENTS/091-import-error-population/run.py |
| 4 | 08:55:31 | artifact | wrote EXPERIMENTS/091-import-error-population/PROTOCOL.md |
| 5 | 08:55:31 | artifact | wrote EXPERIMENTS/091-import-error-population/classify.py |
| 6 | 08:55:31 | artifact | wrote EXPERIMENTS/091-import-error-population/classified.jsonl |
| 7 | 08:55:31 | artifact | wrote EXPERIMENTS/091-import-error-population/harvest.py |
| 8 | 08:55:32 | artifact | wrote EXPERIMENTS/091-import-error-population/README.md |
| 9 | 08:55:33 | artifact | wrote EXPERIMENTS/091-import-error-population/evaluate_gates.py |
| 10 | 08:55:33 | artifact | wrote EXPERIMENTS/091-import-error-population/results.json |
| 11 | 08:55:55 | decision | E091 import-error population experiment: ALL GATES PASS. Population of Python import-error reports naming a module but no distribution is 2.91% (25/85 |
| 12 | 09:08:11 | artifact | wrote EXPERIMENTS/091-import-error-population/constants.py |
| 13 | 09:08:26 | integrity_error | DECISIONS.md was not updated although the session recorded decision |
| 14 | 09:08:26 | session_end | E091 import-error population experiment completed. ALL GATES PASS: 2.91% (25/858) of Python import-error reports on Stack Overflow and GitHub name a m |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-008-measure-import-error-population-asking-w/events.jsonl
```
