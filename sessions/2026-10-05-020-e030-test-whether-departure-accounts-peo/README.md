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

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/030-departure-recurrence/README.md | 4636a3e6bcb9 | 4374 |
| EXPERIMENTS/030-departure-recurrence/PROTOCOL-AMENDMENT-9.md | 4091e6b14d89 | 3470 |
| EXPERIMENTS/030-departure-recurrence/a8_separation.py | 54308b43181c | 1471 |
| EXPERIMENTS/030-departure-recurrence/raw/a8_separation.json | ba8b88338026 | 427 |
| FAILURES-findings-20.md | 7d13029c41c0 | 12534 |

## Commands

17 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/030-departure-recurrence/harvest.py'] | 0 | 49078 |
| 4 | ['python3', 'EXPERIMENTS/030-departure-recurrence/harvest.py'] | 0 | 56006 |
| 5 | ['python3', 'EXPERIMENTS/030-departure-recurrence/extract.py'] | 1 | 904 |
| 6 | ['python3', 'EXPERIMENTS/030-departure-recurrence/extract.py'] | 0 | 113534 |
| 7 | ['python3', 'EXPERIMENTS/030-departure-recurrence/extract.py'] | 0 | 117678 |
| 8 | ['python3', 'EXPERIMENTS/030-departure-recurrence/register_check.py'] | 0 | 251389 |
| 9 | ['python3', 'EXPERIMENTS/030-departure-recurrence/make_reader_views.py'] | 0 | 406 |
| 10 | ['python3', 'EXPERIMENTS/030-departure-recurrence/verify_labels.py', 'treatment'] | 0 | 194 |
| 11 | ['python3', 'EXPERIMENTS/030-departure-recurrence/verify_labels.py', 'control'] | 0 | 174 |
| 12 | ['python3', 'EXPERIMENTS/030-departure-recurrence/make_a8_views.py'] | 0 | 302 |
| 13 | ['python3', 'EXPERIMENTS/030-departure-recurrence/verify_labels.py', 'treatment'] | 0 | 196 |
| 14 | ['python3', 'EXPERIMENTS/030-departure-recurrence/verify_labels.py', 'control'] | 0 | 187 |
| 15 | ['python3', 'EXPERIMENTS/030-departure-recurrence/recurrence.py'] | 0 | 2485 |
| 16 | ['python3', 'EXPERIMENTS/030-departure-recurrence/recurrence.py'] | 0 | 2513 |
| 17 | ['python3', 'EXPERIMENTS/030-departure-recurrence/recurrence.py'] | 0 | 4105 |
| 18 | ['python3', 'EXPERIMENTS/030-departure-recurrence/permutation_control.py'] | 0 | 22784 |
| 19 | ['python3', 'EXPERIMENTS/030-departure-recurrence/a8_separation.py'] | 0 | 395 |

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
| 8 | 22:21:14 | command | $ python3 EXPERIMENTS/030-departure-recurrence/register_check.py |
| 9 | 22:21:58 | command | $ python3 EXPERIMENTS/030-departure-recurrence/make_reader_views.py |
| 10 | 22:23:26 | command | $ python3 EXPERIMENTS/030-departure-recurrence/verify_labels.py treatment |
| 11 | 22:23:27 | command | $ python3 EXPERIMENTS/030-departure-recurrence/verify_labels.py control |
| 12 | 22:24:15 | command | $ python3 EXPERIMENTS/030-departure-recurrence/make_a8_views.py |
| 13 | 22:25:22 | command | $ python3 EXPERIMENTS/030-departure-recurrence/verify_labels.py treatment |
| 14 | 22:25:23 | command | $ python3 EXPERIMENTS/030-departure-recurrence/verify_labels.py control |
| 15 | 22:26:50 | command | $ python3 EXPERIMENTS/030-departure-recurrence/recurrence.py |
| 16 | 22:27:56 | command | $ python3 EXPERIMENTS/030-departure-recurrence/recurrence.py |
| 17 | 22:29:21 | command | $ python3 EXPERIMENTS/030-departure-recurrence/recurrence.py |
| 18 | 22:30:58 | command | $ python3 EXPERIMENTS/030-departure-recurrence/permutation_control.py |
| 19 | 22:35:09 | command | $ python3 EXPERIMENTS/030-departure-recurrence/a8_separation.py |
| 20 | 22:39:24 | artifact | wrote EXPERIMENTS/030-departure-recurrence/README.md |
| 21 | 22:39:24 | artifact | wrote EXPERIMENTS/030-departure-recurrence/PROTOCOL-AMENDMENT-9.md |
| 22 | 22:39:24 | artifact | wrote EXPERIMENTS/030-departure-recurrence/a8_separation.py |
| 23 | 22:39:25 | artifact | wrote EXPERIMENTS/030-departure-recurrence/raw/a8_separation.json |
| 24 | 22:39:25 | artifact | wrote FAILURES-findings-20.md |
| 25 | 22:39:25 | milestone | A8 fired (0.64 vs 0.036); A9 null explains arm difference; length-matched sign flips; H1 not_evaluated third and final time |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-020-e030-test-whether-departure-accounts-peo/events.jsonl
```
