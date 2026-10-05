# Session 2026-10-05-020-e030-test-whether-departure-accounts-peo

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T22:03:03+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E030: test whether departure accounts (people publicly leaving a tool) supply a recurring, unmet, capability clause that the need corpus could not -- and whether a use account adjudicates fit where counts do not

## Summary

_(none recorded)_

## Artifacts

_none_

## Commands

5 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/030-departure-recurrence/harvest.py'] | 0 | 49078 |
| 4 | ['python3', 'EXPERIMENTS/030-departure-recurrence/harvest.py'] | 0 | 56006 |
| 5 | ['python3', 'EXPERIMENTS/030-departure-recurrence/extract.py'] | 1 | 904 |
| 6 | ['python3', 'EXPERIMENTS/030-departure-recurrence/extract.py'] | 0 | 113534 |
| 7 | ['python3', 'EXPERIMENTS/030-departure-recurrence/extract.py'] | 0 | 117678 |

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
| 1 | 22:03:03 | session_start | E030: test whether departure accounts (people publicly leaving a tool) supply a recurring, unmet, capability clause that the need corpus could not --  |
| 2 | 22:04:17 | task_rewrite | appended a create record for T-0074 |
| 3 | 22:08:42 | command | $ python3 EXPERIMENTS/030-departure-recurrence/harvest.py |
| 4 | 22:10:55 | command | $ python3 EXPERIMENTS/030-departure-recurrence/harvest.py |
| 5 | 22:11:28 | command | $ python3 EXPERIMENTS/030-departure-recurrence/extract.py |
| 6 | 22:13:38 | command | $ python3 EXPERIMENTS/030-departure-recurrence/extract.py |
| 7 | 22:15:55 | command | $ python3 EXPERIMENTS/030-departure-recurrence/extract.py |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-020-e030-test-whether-departure-accounts-peo/events.jsonl
```
