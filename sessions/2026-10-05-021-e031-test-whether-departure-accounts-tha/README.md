# Session 2026-10-05-021-e031-test-whether-departure-accounts-tha

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T22:49:03+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E031: test whether departure accounts that name no successor state a requirement the departing artifact failed, and whether any such requirement recurs across independent authors

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/031-unfilled-requirement/README.md | 860e7b855848 | 9070 |
| EXPERIMENTS/031-unfilled-requirement/PROTOCOL.md | 74b0f965b402 | 10865 |
| EXPERIMENTS/031-unfilled-requirement/RUBRIC.md | 86147fd255c4 | 3034 |
| EXPERIMENTS/031-unfilled-requirement/raw/results.json | ae1c0969a115 | 4874 |
| EXPERIMENTS/031-unfilled-requirement/raw/agreement.json | 67bb5296a29a | 3084 |
| EXPERIMENTS/031-unfilled-requirement/raw/strata.json | 2b7b7bd4caa0 | 869 |
| EXPERIMENTS/031-unfilled-requirement/raw/pair_build.json | 44db6f6ec96b | 571 |
| EXPERIMENTS/031-unfilled-requirement/raw/poscontrol_build.json | eca65b1fe488 | 312 |
| FAILURES-findings-21.md | af68ac6b8e67 | 12389 |
| DECISIONS-SCREENING-5.md | 58de799ea60a | 4824 |
| EXPERIMENTS/031-unfilled-requirement/raw/e031_labels_seek__r1.tsv | 499a6c112e04 | 2055 |

## Commands

43 captured, 15 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/recount.py'] | 0 | 684 |
| 6 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/select_doubleread.py'] | 0 | 123 |
| 7 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r1'] | 3 | 107 |
| 8 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r2'] | 3 | 109 |
| 9 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r1'] | 3 | 103 |
| 10 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r2'] | 3 | 96 |
| 11 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r1'] | 3 | 114 |
| 12 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r2'] | 3 | 101 |
| 13 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r1'] | 0 | 165 |
| 14 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r2'] | 3 | 123 |
| 15 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r1'] | 3 | 108 |
| 16 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r2'] | 3 | 100 |
| 17 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r1'] | 0 | 105 |
| 18 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r2'] | 3 | 86 |
| 19 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r1'] | 0 | 104 |
| 20 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r2'] | 0 | 111 |
| 21 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r1'] | 0 | 111 |
| 22 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r2'] | 0 | 111 |
| 23 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r1'] | 0 | 110 |
| 24 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r2'] | 3 | 161 |
| 25 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r1'] | 0 | 192 |
| 26 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'seek', 'r2'] | 0 | 104 |
| 27 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r1'] | 0 | 158 |
| 28 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'move', 'r2'] | 0 | 102 |
| 29 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r1'] | 0 | 108 |
| 30 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'ordinary', 'r2'] | 0 | 116 |
| 31 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'reread', 'r2'] | 3 | 104 |
| 32 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'reread', 'r2'] | 3 | 103 |
| 33 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/recount.py'] | 0 | 427 |
| 34 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'reread', 'r2'] | 0 | 115 |
| 35 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/agreement.py'] | 0 | 100 |
| 36 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'nonsense', 'r1'] | 0 | 407 |
| 37 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'nonsense', 'r2'] | 3 | 188 |
| 38 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'nonsense', 'r1'] | 0 | 57 |
| 39 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/verify_labels.py', 'nonsense', 'r2'] | 0 | 109 |
| 40 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/recurrence.py'] | 0 | 203 |
| 41 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/build_pairs.py'] | 0 | 211 |
| 42 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/build_poscontrol.py'] | 0 | 119 |
| 43 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/stats.py'] | 1 | 906 |
| 44 | ['python3', 'EXPERIMENTS/031-unfilled-requirement/stats.py'] | 0 | 106 |

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
| 1 | 22:49:03 | session_start | E031: test whether departure accounts that name no successor state a requirement the departing artifact failed, and whether any such requirement recur |
| 2 | 22:49:16 | task_rewrite | appended a create record for T-0075 |
| 3 | 22:49:31 | task_rewrite | rewrote tasks/T-0075-e031-test-whether-public-accounts-of-leaving-a-n.md (status: claimed) |
| 4 | 22:49:31 | task_rewrite | appended a claim record for T-0075 |
| 5 | 23:00:02 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/recount.py |
| 6 | 23:01:20 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/select_doubleread.py |
| 7 | 23:07:34 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r1 |
| 8 | 23:07:34 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r2 |
| 9 | 23:07:35 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r1 |
| 10 | 23:07:35 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r2 |
| 11 | 23:07:36 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r1 |
| 12 | 23:07:36 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r2 |
| 13 | 23:07:54 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r1 |
| 14 | 23:07:55 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r2 |
| 15 | 23:07:55 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r1 |
| 16 | 23:07:56 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r2 |
| 17 | 23:07:56 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r1 |
| 18 | 23:07:57 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r2 |
| 19 | 23:08:39 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r1 |
| 20 | 23:08:39 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r2 |
| 21 | 23:08:40 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r1 |
| 22 | 23:08:40 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r2 |
| 23 | 23:08:41 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r1 |
| 24 | 23:08:41 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r2 |
| 25 | 23:09:20 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r1 |
| 26 | 23:09:20 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py seek r2 |
| 27 | 23:09:21 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r1 |
| 28 | 23:09:21 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move r2 |
| 29 | 23:09:22 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r1 |
| 30 | 23:09:22 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary r2 |
| 31 | 23:09:23 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py reread r2 |
| 32 | 23:09:36 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py reread r2 |
| 33 | 23:09:46 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/recount.py |
| 34 | 23:09:47 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py reread r2 |
| 35 | 23:10:00 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/agreement.py |
| 36 | 23:16:01 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py nonsense r1 |
| 37 | 23:16:02 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py nonsense r2 |
| 38 | 23:16:21 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py nonsense r1 |
| 39 | 23:16:21 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py nonsense r2 |
| 40 | 23:16:45 | command | $ python3 EXPERIMENTS/031-unfilled-requirement/recurrence.py |
| 52 | 00:27:14 | artifact | wrote EXPERIMENTS/031-unfilled-requirement/raw/agreement.json |
| 53 | 00:27:15 | artifact | wrote EXPERIMENTS/031-unfilled-requirement/raw/strata.json |
| 54 | 00:27:16 | artifact | wrote EXPERIMENTS/031-unfilled-requirement/raw/pair_build.json |
| 55 | 00:27:16 | artifact | wrote EXPERIMENTS/031-unfilled-requirement/raw/poscontrol_build.json |
| 56 | 00:27:17 | artifact | wrote FAILURES-findings-21.md |
| 57 | 00:27:17 | artifact | wrote DECISIONS-SCREENING-5.md |
| 58 | 00:27:23 | milestone | E031 run: H1 fails its margin (0.1667 vs 0.20) and the seek/move strata are identical at 0.347 each, so the 'unfilled' premise is retired by measureme |
| 59 | 00:27:35 | task_rewrite | rewrote tasks/T-0075-e031-test-whether-public-accounts-of-leaving-a-n.md (status: done) |
| 60 | 00:27:36 | task_rewrite | appended a complete record for T-0075 |
| 61 | 00:33:30 | artifact | wrote EXPERIMENTS/031-unfilled-requirement/raw/e031_labels_seek__r1.tsv |

_11 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-021-e031-test-whether-departure-accounts-tha/events.jsonl
```
