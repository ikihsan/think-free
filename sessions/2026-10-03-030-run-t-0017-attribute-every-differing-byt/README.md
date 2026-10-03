# Session 2026-10-03-030-run-t-0017-attribute-every-differing-byt

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `opencode`
- **Started:** 2026-10-03T21:41:36+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Run T-0017: attribute every differing byte between repeated builds of one source under different SOURCE_DATE_EPOCH values, with the kill gate written before the run

## Summary

_(none recorded)_

## Artifacts

_none_

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport setuptools, wheel, sys\nprint('python', sys.version.split()[0])\nprint('setuptools', setuptools.__version__)\nprint('wheel | 0 | 695 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:41:36 | session_start | Run T-0017: attribute every differing byte between repeated builds of one source under different SOURCE_DATE_EPOCH values, with the kill gate written  |
| 2 | 21:42:42 | command | $ python3 -c  import setuptools, wheel, sys print('python', sys.version.split()[0]) print('setuptools', setuptools.__version__) print('wheel', |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/events.jsonl
```
