# Session 2026-10-05-008-measure-the-outcome-distribution-of-e012

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `opencode`
- **Started:** 2026-10-05T07:58:43+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Measure the outcome distribution of E012's 1401 publicly stated unmet needs: answered in thread, built by the requester, or unanswered

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/022-need-outcomes/results.json | 5d2cf9ea3953 | 3369 |
| EXPERIMENTS/022-need-outcomes/raw/need_depth.jsonl | f456dceb6697 | 158904 |
| EXPERIMENTS/022-need-outcomes/raw/lift_stratified.json | 9093933ac95d | 5195 |
| EXPERIMENTS/022-need-outcomes/README.md | f7dcce9e5c0f | 7557 |
| tests/test_need_depth_gate.py | 17a32aac04da | 9046 |
| FAILURES-findings-17.md | 13dd0be74b33 | 4387 |

## Commands

48 captured, 6 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['python3', 'EXPERIMENTS/022-need-outcomes/run.py', '--limit', '40'] | 0 | 5984 |
| 5 | ['python3', 'EXPERIMENTS/022-need-outcomes/run.py'] | 0 | 90801 |
| 6 | ['python3', 'EXPERIMENTS/022-need-outcomes/nonsense_control.py'] | 0 | 2014 |
| 8 | ['python3', 'EXPERIMENTS/022-need-outcomes/nonsense_control.py'] | 0 | 4221 |
| 9 | ['python3', 'EXPERIMENTS/022-need-outcomes/nonsense_control.py'] | 0 | 3906 |
| 10 | ['python3', 'EXPERIMENTS/022-need-outcomes/run.py'] | 0 | 234 |
| 11 | ['python3', 'EXPERIMENTS/022-need-outcomes/control.py', '--limit', '30'] | 0 | 24809 |
| 12 | ['python3', 'EXPERIMENTS/022-need-outcomes/control.py'] | 0 | 1080704 |
| 13 | ['python3', 'EXPERIMENTS/022-need-outcomes/lift.py'] | 1 | 1009 |
| 14 | ['python3', 'EXPERIMENTS/022-need-outcomes/lift.py'] | 1 | 901 |
| 15 | ['python3', 'EXPERIMENTS/022-need-outcomes/lift.py'] | 0 | 323 |
| 16 | ['python3', 'EXPERIMENTS/022-need-outcomes/control_depth.py', '--limit', '12'] | 0 | 52615 |
| 17 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth.py'] | 0 | 65989 |
| 18 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth.py'] | 0 | 75582 |
| 19 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth.py'] | 0 | 719068 |
| 20 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth.py'] | 0 | 60197 |
| 21 | ['python3', 'EXPERIMENTS/022-need-outcomes/lift_stratified.py'] | 0 | 193 |
| 22 | ['python3', 'EXPERIMENTS/022-need-outcomes/control_depth.py', '--limit', '12'] | 0 | 18087 |
| 23 | ['python3', 'EXPERIMENTS/022-need-outcomes/serve_sample.py'] | 0 | 62987 |
| 24 | ['python3', 'EXPERIMENTS/022-need-outcomes/serve_sample.py', '--verify'] | 0 | 312 |
| 25 | ['python3', 'EXPERIMENTS/022-need-outcomes/author_build.py'] | 0 | 35753 |
| 26 | ['python3', 'EXPERIMENTS/022-need-outcomes/author_build.py'] | 0 | 36909 |
| 27 | ['python3', 'EXPERIMENTS/022-need-outcomes/author_build.py', '--verify'] | 0 | 1198 |
| 28 | ['python3', 'EXPERIMENTS/022-need-outcomes/combine.py'] | 0 | 378 |
| 29 | ['python3', 'EXPERIMENTS/022-need-outcomes/lift_stratified.py'] | 0 | 598 |
| 30 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_length.py'] | 0 | 88289 |
| 31 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_length.py', '--verify'] | 0 | 394 |
| 32 | ['python3', 'EXPERIMENTS/022-need-outcomes/lift_length.py'] | 0 | 1592 |
| 33 | ['python3', 'EXPERIMENTS/022-need-outcomes/run.py', '--verify'] | 0 | 498 |
| 34 | ['python3', 'EXPERIMENTS/022-need-outcomes/control_depth.py', '--verify'] | 0 | 579 |
| 35 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth.py', '--verify'] | 1 | 498 |
| 36 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth_walk.py'] | 0 | 23405 |
| 37 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth_walk.py'] | 0 | 596 |
| 39 | ['tools/origin', 'session', 'step', 'Resumed after interruption. E022 measured: 1401/1401 readable (gate A1 met), 812 answered (0.580), depth-stratifi | 0 | 1128 |
| 40 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth_walk.py'] | 0 | 83112 |
| 41 | ['python3', 'EXPERIMENTS/022-need-outcomes/need_depth.py', '--verify'] | 0 | 423 |
| 42 | ['python3', 'EXPERIMENTS/022-need-outcomes/lift_stratified.py'] | 0 | 781 |
| 43 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_need_depth_gate', '-v'] | 1 | 2801 |
| 44 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_need_depth_gate'] | 1 | 2590 |
| 45 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_need_depth_gate'] | 0 | 2816 |

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
| 1 | 07:58:43 | session_start | Measure the outcome distribution of E012's 1401 publicly stated unmet needs: answered in thread, built by the requester, or unanswered |
| 2 | 07:58:48 | task_rewrite | rewrote tasks/T-0066-measure-what-happens-to-a-publicly-stated-unmet.md (status: claimed) |
| 3 | 07:58:48 | task_rewrite | appended a claim record for T-0066 |
| 4 | 08:00:36 | command | $ python3 EXPERIMENTS/022-need-outcomes/run.py --limit 40 |
| 5 | 08:02:21 | command | $ python3 EXPERIMENTS/022-need-outcomes/run.py |
| 6 | 08:03:01 | command | $ python3 EXPERIMENTS/022-need-outcomes/nonsense_control.py |
| 7 | 08:08:10 | milestone | nonsense control C3 passes: the reader reports absence for a fabricated id and invents nothing |
| 8 | 08:08:27 | command | $ python3 EXPERIMENTS/022-need-outcomes/nonsense_control.py |
| 9 | 08:08:56 | command | $ python3 EXPERIMENTS/022-need-outcomes/nonsense_control.py |
| 10 | 08:08:57 | command | $ python3 EXPERIMENTS/022-need-outcomes/run.py |
| 11 | 08:09:29 | command | $ python3 EXPERIMENTS/022-need-outcomes/control.py --limit 30 |
| 12 | 08:27:37 | command | $ python3 EXPERIMENTS/022-need-outcomes/control.py |
| 13 | 08:28:00 | command | $ python3 EXPERIMENTS/022-need-outcomes/lift.py |
| 14 | 08:28:13 | command | $ python3 EXPERIMENTS/022-need-outcomes/lift.py |
| 15 | 08:28:30 | command | $ python3 EXPERIMENTS/022-need-outcomes/lift.py |
| 16 | 08:30:23 | command | $ python3 EXPERIMENTS/022-need-outcomes/control_depth.py --limit 12 |
| 17 | 09:12:06 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth.py |
| 18 | 09:14:30 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth.py |
| 19 | 09:26:59 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth.py |
| 20 | 09:28:25 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth.py |
| 21 | 09:28:48 | command | $ python3 EXPERIMENTS/022-need-outcomes/lift_stratified.py |
| 22 | 09:29:47 | command | $ python3 EXPERIMENTS/022-need-outcomes/control_depth.py --limit 12 |
| 23 | 09:31:35 | command | $ python3 EXPERIMENTS/022-need-outcomes/serve_sample.py |
| 24 | 09:32:59 | command | $ python3 EXPERIMENTS/022-need-outcomes/serve_sample.py --verify |
| 25 | 09:34:14 | command | $ python3 EXPERIMENTS/022-need-outcomes/author_build.py |
| 26 | 09:39:08 | command | $ python3 EXPERIMENTS/022-need-outcomes/author_build.py |
| 27 | 09:39:41 | command | $ python3 EXPERIMENTS/022-need-outcomes/author_build.py --verify |
| 28 | 09:40:04 | command | $ python3 EXPERIMENTS/022-need-outcomes/combine.py |
| 29 | 09:40:23 | command | $ python3 EXPERIMENTS/022-need-outcomes/lift_stratified.py |
| 30 | 09:42:55 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_length.py |
| 31 | 09:43:03 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_length.py --verify |
| 32 | 09:43:32 | command | $ python3 EXPERIMENTS/022-need-outcomes/lift_length.py |
| 33 | 09:43:41 | command | $ python3 EXPERIMENTS/022-need-outcomes/run.py --verify |
| 34 | 09:43:42 | command | $ python3 EXPERIMENTS/022-need-outcomes/control_depth.py --verify |
| 35 | 09:43:43 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth.py --verify |
| 36 | 09:44:59 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth_walk.py |
| 37 | 09:45:27 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth_walk.py |
| 38 | 09:53:58 | milestone | Resumed after interruption. E022 measured: 1401/1401 readable (gate A1 met), 812 answered (0.580), depth-stratified MH OR 0.692, build arm 0/24 hand-j |
| 39 | 09:53:58 | command | $ tools/origin session step Resumed after interruption. E022 measured: 1401/1401 readable (gate A1 met), 812 answered (0.580), depth-stratifie |
| 40 | 09:56:32 | command | $ python3 EXPERIMENTS/022-need-outcomes/need_depth_walk.py |
| 53 | 10:30:49 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_need_depth_gate |
| 54 | 10:40:28 | artifact | wrote EXPERIMENTS/022-need-outcomes/results.json |
| 55 | 10:40:29 | artifact | wrote EXPERIMENTS/022-need-outcomes/raw/need_depth.jsonl |
| 56 | 10:40:29 | artifact | wrote EXPERIMENTS/022-need-outcomes/raw/lift_stratified.json |
| 57 | 10:40:30 | artifact | wrote EXPERIMENTS/022-need-outcomes/README.md |
| 58 | 10:40:31 | artifact | wrote tests/test_need_depth_gate.py |
| 59 | 10:40:31 | artifact | wrote FAILURES-findings-17.md |
| 60 | 10:40:48 | task_rewrite | rewrote tasks/T-0066-measure-what-happens-to-a-publicly-stated-unmet.md (status: done) |
| 61 | 10:40:49 | task_rewrite | appended a complete record for T-0066 |
| 62 | 11:04:04 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |

_12 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-008-measure-the-outcome-distribution-of-e012/events.jsonl
```
