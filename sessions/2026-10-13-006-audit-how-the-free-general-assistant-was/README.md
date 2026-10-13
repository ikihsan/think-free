# Session 2026-10-13-006-audit-how-the-free-general-assistant-was

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T02:42:26+00:00
- **Duration:** 6586.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Audit how the 'free general assistant' was run in the service-closure experiments, then choose and run the next fresh observation or prototype

## Summary

E126 completed: Stack Overflow closes like all other venue classes (27/40 = 0.675, Wilson LB 0.5202 >= 0.50). The venue sweep is complete — every venue class is served. The one residue is 6 program-shaped rows.

## Next

Test whether the 6 program-shaped rows from E126 can be served by a self-contained program

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/126-stackoverflow-service-test/RESULT.md | 94d8f205acb6 | 4188 |

## Commands

11 captured, 4 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/fetch.py'] | 1 | 4530 |
| 4 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/fetch.py'] | 0 | 1910 |
| 5 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/make-sheet.py'] | 1 | 590 |
| 6 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/make-sheet.py'] | 0 | 231 |
| 7 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/screen.py'] | 0 | 110 |
| 8 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/g0.py'] | 0 | 199 |
| 9 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/threads.py'] | 1 | 515 |
| 10 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/threads.py'] | 1 | 596 |
| 11 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/threads.py'] | 0 | 1666 |
| 12 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/grading-sheet.py'] | 0 | 104 |
| 13 | ['python3', 'EXPERIMENTS/126-stackoverflow-service-test/grading-sheet.py'] | 0 | 116 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 24 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/AMENDMENT-1.md |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/PROTOCOL.md |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/attempts.jsonl |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/fetch.py |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/g0-probes.json |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/g0-results.jsonl |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/g0.json |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/g0.py |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/grading-results.jsonl |
|   undeclared | EXPERIMENTS/126-stackoverflow-service-test/grading-sheet.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:42:26 | session_start | Audit how the 'free general assistant' was run in the service-closure experiments, then choose and run the next fresh observation or prototype |
| 2 | 03:00:35 | milestone | D077 incumbent check done: Firefly III and Actual Budget recurring transactions are user-declared templates; no import-driven detection. E126 protocol |
| 3 | 03:03:43 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/fetch.py |
| 4 | 03:06:17 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/fetch.py |
| 5 | 03:10:31 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/make-sheet.py |
| 6 | 03:12:23 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/make-sheet.py |
| 7 | 03:22:18 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/screen.py |
| 8 | 03:26:21 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/g0.py |
| 9 | 03:30:07 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/threads.py |
| 10 | 03:34:24 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/threads.py |
| 11 | 03:35:31 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/threads.py |
| 12 | 03:37:23 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/grading-sheet.py |
| 13 | 03:39:28 | command | $ python3 EXPERIMENTS/126-stackoverflow-service-test/grading-sheet.py |
| 14 | 04:20:39 | milestone | E126 complete: 27/40 served (Wilson LB 0.5202 >= 0.50), Stack Overflow closes like other venues |
| 15 | 04:20:39 | artifact | wrote EXPERIMENTS/126-stackoverflow-service-test/RESULT.md |
| 16 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/AMENDMENT-1.md |
| 17 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/PROTOCOL.md |
| 18 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/attempts.jsonl |
| 19 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/fetch.py |
| 20 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/g0-probes.json |
| 21 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/g0-results.jsonl |
| 22 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/g0.json |
| 23 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/g0.py |
| 24 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/grading-results.jsonl |
| 25 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/grading-sheet.py |
| 26 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/grading-sheet.txt |
| 27 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/make-sheet.py |
| 28 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/pool-raw.json |
| 29 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/screen.py |
| 30 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/screening-map.json |
| 31 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/screening-sheet.json |
| 32 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/screening-sheet.txt |
| 33 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/screening-summary.json |
| 34 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/screening.jsonl |
| 35 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/threads.json |
| 36 | 04:32:12 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/126-stackoverflow-service-test/threads.py |
| 37 | 04:32:12 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 38 | 04:32:12 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 39 | 04:32:12 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 40 | 04:32:12 | doc_update | updated FAILURES.md |
| 41 | 04:32:12 | doc_update | updated STATE.md |
| 42 | 04:32:12 | session_end | E126 completed: Stack Overflow closes like all other venue classes (27/40 = 0.675, Wilson LB 0.5202 >= 0.50). The venue sweep is complete — every venu |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-006-audit-how-the-free-general-assistant-was/events.jsonl
```
