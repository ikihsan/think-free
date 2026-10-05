# Session 2026-10-05-019-measure-whether-the-278-need-staters-who

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `opencode`
- **Started:** 2026-10-05T20:13:48+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure whether the 278 need-staters who shipped something shipped the thing they said was missing, against mismatched and thread-title controls

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/029-need-build-match/PROTOCOL.md | a97c5df55b20 | 8651 |
| EXPERIMENTS/029-need-build-match/RUBRIC.md | a09736e66de9 | 3710 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md | 12a69772ff78 | 4160 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md | 12a69772ff78 | 4160 |
| EXPERIMENTS/029-need-build-match/PROTOCOL.md | a97c5df55b20 | 8651 |
| EXPERIMENTS/029-need-build-match/RUBRIC.md | a09736e66de9 | 3710 |
| EXPERIMENTS/029-need-build-match/build_population.py | d56a868fc632 | 4912 |
| EXPERIMENTS/029-need-build-match/fetch_builds.py | eaf568a624fd | 5988 |
| EXPERIMENTS/029-need-build-match/make_reader_views.py | 6340aa1c26b8 | 6266 |
| EXPERIMENTS/029-need-build-match/raw/builds.jsonl | d736a3a68cd7 | 168568 |
| EXPERIMENTS/029-need-build-match/raw/gate_a2_controls.jsonl | 9ff639f69633 | 581 |
| EXPERIMENTS/029-need-build-match/raw/population.jsonl | f1d32b35d9db | 175291 |
| EXPERIMENTS/029-need-build-match/raw/stories.jsonl | fffb70d6e6f5 | 39726 |
| EXPERIMENTS/029-need-build-match/raw/view_key.json | aaa4ce202292 | 21790 |
| EXPERIMENTS/029-need-build-match/raw/view_r1.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/raw/view_r2.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-2.md | cd3839a2304c | 3716 |
| EXPERIMENTS/029-need-build-match/assemble_labels.py | 37538a92dfd7 | 3807 |
| EXPERIMENTS/029-need-build-match/stats.py | 02e1e077d189 | 13144 |
| EXPERIMENTS/029-need-build-match/test_claims.py | 15a4161c136f | 19588 |
| EXPERIMENTS/029-need-build-match/raw/view_r1_v1.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/raw/view_r2_v1.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/raw/view_r1_xonly.txt | a518d8ccd34b | 57643 |
| EXPERIMENTS/029-need-build-match/raw/view_r2_xonly.txt | a518d8ccd34b | 57643 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-3.md | a56005286144 | 5525 |

## Commands

11 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/029-need-build-match/build_population.py'] | 0 | 488 |
| 6 | ['python3', 'EXPERIMENTS/029-need-build-match/fetch_builds.py'] | 0 | 548256 |
| 7 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 1 | 106 |
| 8 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 1 | 114 |
| 9 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 0 | 192 |
| 25 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 0 | 192 |
| 35 | ['python3', 'EXPERIMENTS/029-need-build-match/repair_reader_ids.py'] | 0 | 115 |
| 36 | ['python3', 'EXPERIMENTS/029-need-build-match/assemble_labels.py'] | 0 | 99 |
| 37 | ['python3', 'EXPERIMENTS/029-need-build-match/stats.py'] | 1 | 848 |
| 38 | ['python3', 'EXPERIMENTS/029-need-build-match/stats.py'] | 0 | 181 |
| 39 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 0 | 115 |

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
| 1 | 20:13:48 | session_start | Measure whether the 278 need-staters who shipped something shipped the thing they said was missing, against mismatched and thread-title controls |
| 2 | 20:15:36 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL.md |
| 3 | 20:15:37 | artifact | wrote EXPERIMENTS/029-need-build-match/RUBRIC.md |
| 4 | 20:15:37 | milestone | E029 protocol and reader rubric declared before any fetch |
| 5 | 20:16:22 | command | $ python3 EXPERIMENTS/029-need-build-match/build_population.py |
| 6 | 20:26:06 | command | $ python3 EXPERIMENTS/029-need-build-match/fetch_builds.py |
| 7 | 20:27:57 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 8 | 20:28:18 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 9 | 20:29:16 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 10 | 20:29:38 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md |
| 11 | 20:29:39 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md |
| 12 | 20:29:39 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL.md |
| 13 | 20:29:39 | artifact | wrote EXPERIMENTS/029-need-build-match/RUBRIC.md |
| 14 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/build_population.py |
| 15 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/fetch_builds.py |
| 16 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 17 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/builds.jsonl |
| 18 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/gate_a2_controls.jsonl |
| 19 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/population.jsonl |
| 20 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/stories.jsonl |
| 21 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_key.json |
| 22 | 20:29:42 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r1.txt |
| 23 | 20:29:42 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r2.txt |
| 24 | 20:29:43 | milestone | E029 population built (241 -> 74 causally eligible), fetched, and two blind reader views written |
| 25 | 20:38:41 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 26 | 20:42:52 | milestone | mismatched-arm defect found by a test (45 of 74 rows rendered empty), repaired, X labels discarded, re-read launched |
| 27 | 20:43:06 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-2.md |
| 28 | 20:43:07 | artifact | wrote EXPERIMENTS/029-need-build-match/assemble_labels.py |
| 29 | 20:43:08 | artifact | wrote EXPERIMENTS/029-need-build-match/stats.py |
| 30 | 20:43:08 | artifact | wrote EXPERIMENTS/029-need-build-match/test_claims.py |
| 31 | 20:43:09 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r1_v1.txt |
| 32 | 20:43:11 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r2_v1.txt |
| 33 | 20:43:13 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r1_xonly.txt |
| 34 | 20:43:13 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r2_xonly.txt |
| 35 | 20:45:12 | command | $ python3 EXPERIMENTS/029-need-build-match/repair_reader_ids.py |
| 36 | 20:45:13 | command | $ python3 EXPERIMENTS/029-need-build-match/assemble_labels.py |
| 37 | 20:45:20 | command | $ python3 EXPERIMENTS/029-need-build-match/stats.py |
| 38 | 20:45:38 | command | $ python3 EXPERIMENTS/029-need-build-match/stats.py |
| 39 | 20:48:14 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 40 | 20:56:53 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-3.md |
| 41 | 20:56:53 | milestone | control arm found to be a relabelled replicate; view frozen at d604f1f9; all earlier labels superseded and retained |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-019-measure-whether-the-278-need-staters-who/events.jsonl
```
