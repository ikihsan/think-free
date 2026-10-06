# Session 2026-10-06-002-e033-measure-the-rate-of-cross-author-re

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T02:42:10+00:00
- **Duration:** 7997.6s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E033: measure the rate of cross-author recurrence in public long-form questions against Stack Exchange's own duplicate-closure label, and test whether the mission's five recurrence zeros are a sampling artefact

## Summary

E033 refuted the mission's pooled recurrence bound of 0.0223 by reading recurrence off Stack Exchange's own duplicate-closure judgement over 1000 questions (0.0540, CI95 [0.0416, 0.0698]), and showed E032's population was drawn from the tertile where recurrence is 4.5x rarer (sort=votes selects answered questions; the top 60 by score contains 0 duplicate closures). Two things I got wrong and corrected rather than kept: the run's second claim (that repeats go unanswered) is mechanical -- 0 of 54 duplicates has an accepted answer -- and was withdrawn in PROTOCOL.md AMENDMENT-3; and AMENDMENT-1's own rationale for widening the window was false, since sort=creation with order=desc takes the 500 newest rather than a spread. A3 failed at 6 of 24, so the closure's canonical is treated as unreadable and the declared visibility product is not printed. No candidate was produced. F056: the per-day world-share gate asserted over every day of history that world-facing work stays a minority, and failed 2026-10-06 at exactly 50.0%; scoped to the days F025 measured and replaced with a floor, falsified in both directions. 799 tests green, preflight clean.

## Next

Item 0d has no measured handle left: E033 produced a method result and no candidate, and its candidate-facing claim was withdrawn as mechanical. The live question is what to measure recurrence on. Cheapest honest step is to test whether the convergent-but-unresolved population exists somewhere the closure label is not confounded with its own consequence -- an archive where duplicate resolution does not also decide the answer state, so that 'several people asked and nobody answered' is separable from 'several people asked and the duplicate was closed'. If no such archive is reachable within the API budget, say so and stop treating the need corpus as a generator.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/033-question-recurrence/PROTOCOL.md | 045953f24c73 | 15831 |
| EXPERIMENTS/033-question-recurrence/README.md | d16c084d9e01 | 8797 |
| EXPERIMENTS/033-question-recurrence/API.md | c6fb48aaec5e | 3762 |
| EXPERIMENTS/033-question-recurrence/harvest.py | ffc81bbeb4f6 | 6741 |
| EXPERIMENTS/033-question-recurrence/resolve.py | b3be7b04339b | 6757 |
| EXPERIMENTS/033-question-recurrence/sheet.py | 5e8120249c7e | 5445 |
| EXPERIMENTS/033-question-recurrence/tally.py | dbd245a172bd | 12332 |
| EXPERIMENTS/033-question-recurrence/descriptive.py | e06a9e35e6e9 | 6402 |
| EXPERIMENTS/033-question-recurrence/raw/harvest.jsonl | 2a74ad63f73e | 1193261 |
| EXPERIMENTS/033-question-recurrence/raw/fetch_log.jsonl | 608d5eca2832 | 9593 |
| EXPERIMENTS/033-question-recurrence/raw/resolve_log.jsonl | 5e799cb58068 | 11353 |
| EXPERIMENTS/033-question-recurrence/raw/edges.jsonl | 99b063f156e3 | 92352 |
| EXPERIMENTS/033-question-recurrence/raw/canonicals.jsonl | e3b0c44298fc | 0 |
| EXPERIMENTS/033-question-recurrence/raw/q2_key.jsonl | 54f1e26dc341 | 2500 |
| EXPERIMENTS/033-question-recurrence/raw/harvest-attempt1.jsonl | e40ebb0db6b0 | 732973 |
| EXPERIMENTS/033-question-recurrence/raw/tally.json | 6209ed888a2f | 4296 |
| EXPERIMENTS/033-question-recurrence/sheets/q2_pairs.tsv | 36698f068dc7 | 25645 |
| EXPERIMENTS/033-question-recurrence/sheets/MANIFEST.json | 04553eda6a75 | 293 |
| EXPERIMENTS/033-question-recurrence/labels/q2_pairs_r1.tsv | 00ba25f00718 | 743 |
| EXPERIMENTS/033-question-recurrence/labels/q2_pairs_r2.tsv | f50d802b1a26 | 754 |
| FAILURES-findings-22.md | 72314f350c8e | 13055 |
| FAILURES.md | 0efd27ac3186 | 23281 |
| STATE.md | 07124274a0f8 | 33899 |
| STATE-in-flight-2.md | 81a7bbfc3fae | 12597 |
| STATE-next-actions.md | 1eb569f9fdd7 | 15870 |
| STATE-next-actions-closed.md | 5f627f262909 | 6970 |
| STATE-constraints.md | ea8026736417 | 14945 |
| ROADMAP.md | 407ea83eb4f4 | 13612 |
| ROADMAP-infrastructure.md | ccdff92c9f44 | 8783 |
| EXPERIMENTS/README.md | 4c6d6f5d9d0b | 6562 |
| RELEASE-MANIFEST.md | 065a43931d90 | 5267 |
| docs/INDEX.md | 60ac76b6fe0b | 37375 |
| EXPERIMENTS/033-question-recurrence/API.md | 798c0fdb70d7 | 3974 |
| EXPERIMENTS/033-question-recurrence/README.md | b3db7df91c43 | 8826 |
| FAILURES-findings-22.md | 53462cd0a3c4 | 13069 |
| FAILURES.md | 3158e1b20660 | 23295 |
| STATE-in-flight-2.md | ec677e07d682 | 12611 |
| EXPERIMENTS/033-question-recurrence/README.md | 39deeffe9fc7 | 9833 |
| EXPERIMENTS/033-question-recurrence/PROTOCOL.md | 760b64aeb192 | 17809 |
| FAILURES-findings-22.md | d3a20d89d909 | 13389 |
| FAILURES.md | d0d0f3903609 | 23351 |
| STATE-in-flight-2.md | 9b740a54f973 | 12964 |
| STATE-next-actions.md | 55174c943acf | 15928 |
| EXPERIMENTS/README.md | 0939cc9436b7 | 6630 |
| ROADMAP.md | e0038d82a9b8 | 13859 |
| tests/test_allocation_world_share.py | 8fa70bbfc0d1 | 3443 |
| tests/test_allocation_measurement.py | 571c015613ea | 14668 |
| tests/README.md | e6aa5a8d5316 | 30964 |
| FAILURES-findings-22.md | 6650d71e04aa | 16922 |
| FAILURES.md | 81bcad70d4d1 | 24549 |
| STATE.md | f657e4589cf9 | 34222 |
| STATE-constraints.md | e04df7b7bafa | 16013 |
| EXPERIMENTS/033-question-recurrence/README.md | 199ec33eaf82 | 10599 |
| EXPERIMENTS/033-question-recurrence/PROTOCOL.md | 760b64aeb192 | 17809 |

## Commands

9 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/033-question-recurrence/harvest.py'] | 0 | 5276 |
| 6 | ['python3', 'EXPERIMENTS/033-question-recurrence/harvest.py'] | 0 | 7775 |
| 7 | ['python3', 'EXPERIMENTS/033-question-recurrence/resolve.py'] | 0 | 15176 |
| 8 | ['python3', 'EXPERIMENTS/033-question-recurrence/sheet.py'] | 0 | 303 |
| 9 | ['python3', 'EXPERIMENTS/033-question-recurrence/tally.py', '--check'] | 1 | 917 |
| 10 | ['python3', 'EXPERIMENTS/033-question-recurrence/tally.py', '--check'] | 0 | 167 |
| 11 | ['python3', 'EXPERIMENTS/033-question-recurrence/tally.py', '--check'] | 0 | 135 |
| 12 | ['python3', 'EXPERIMENTS/033-question-recurrence/tally.py', '--check'] | 0 | 195 |
| 13 | ['python3', 'EXPERIMENTS/033-question-recurrence/tally.py', '--check'] | 0 | 278 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:42:10 | session_start | E033: measure the rate of cross-author recurrence in public long-form questions against Stack Exchange's own duplicate-closure label, and test whether |
| 2 | 02:42:39 | task_rewrite | appended a create record for T-0077 |
| 3 | 02:42:52 | task_rewrite | rewrote tasks/T-0077-e033-measure-the-rate-at-which-a-question-in-pub.md (status: claimed) |
| 4 | 02:42:52 | task_rewrite | appended a claim record for T-0077 |
| 5 | 02:44:44 | command | $ python3 EXPERIMENTS/033-question-recurrence/harvest.py |
| 6 | 02:46:25 | command | $ python3 EXPERIMENTS/033-question-recurrence/harvest.py |
| 7 | 02:47:20 | command | $ python3 EXPERIMENTS/033-question-recurrence/resolve.py |
| 8 | 02:50:44 | command | $ python3 EXPERIMENTS/033-question-recurrence/sheet.py |
| 9 | 02:53:28 | command | $ python3 EXPERIMENTS/033-question-recurrence/tally.py --check |
| 10 | 02:53:41 | command | $ python3 EXPERIMENTS/033-question-recurrence/tally.py --check |
| 11 | 02:54:29 | command | $ python3 EXPERIMENTS/033-question-recurrence/tally.py --check |
| 12 | 02:55:22 | command | $ python3 EXPERIMENTS/033-question-recurrence/tally.py --check |
| 13 | 02:58:14 | command | $ python3 EXPERIMENTS/033-question-recurrence/tally.py --check |
| 14 | 03:27:28 | artifact | wrote EXPERIMENTS/033-question-recurrence/PROTOCOL.md |
| 15 | 03:27:29 | artifact | wrote EXPERIMENTS/033-question-recurrence/README.md |
| 16 | 03:27:29 | artifact | wrote EXPERIMENTS/033-question-recurrence/API.md |
| 17 | 03:27:30 | artifact | wrote EXPERIMENTS/033-question-recurrence/harvest.py |
| 18 | 03:27:31 | artifact | wrote EXPERIMENTS/033-question-recurrence/resolve.py |
| 19 | 03:27:32 | artifact | wrote EXPERIMENTS/033-question-recurrence/sheet.py |
| 20 | 03:27:32 | artifact | wrote EXPERIMENTS/033-question-recurrence/tally.py |
| 21 | 03:27:33 | artifact | wrote EXPERIMENTS/033-question-recurrence/descriptive.py |
| 22 | 03:27:34 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/harvest.jsonl |
| 23 | 03:27:35 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/fetch_log.jsonl |
| 24 | 03:27:36 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/resolve_log.jsonl |
| 25 | 03:27:36 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/edges.jsonl |
| 26 | 03:27:37 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/canonicals.jsonl |
| 27 | 03:27:38 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/q2_key.jsonl |
| 28 | 03:27:40 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/harvest-attempt1.jsonl |
| 29 | 03:27:40 | artifact | wrote EXPERIMENTS/033-question-recurrence/raw/tally.json |
| 30 | 03:27:41 | artifact | wrote EXPERIMENTS/033-question-recurrence/sheets/q2_pairs.tsv |
| 31 | 03:27:41 | artifact | wrote EXPERIMENTS/033-question-recurrence/sheets/MANIFEST.json |
| 32 | 03:27:42 | artifact | wrote EXPERIMENTS/033-question-recurrence/labels/q2_pairs_r1.tsv |
| 33 | 03:27:43 | artifact | wrote EXPERIMENTS/033-question-recurrence/labels/q2_pairs_r2.tsv |
| 34 | 03:27:43 | artifact | wrote FAILURES-findings-22.md |
| 35 | 03:27:44 | artifact | wrote FAILURES.md |
| 36 | 03:27:44 | artifact | wrote STATE.md |
| 37 | 03:27:45 | artifact | wrote STATE-in-flight-2.md |
| 38 | 03:27:47 | artifact | wrote STATE-next-actions.md |
| 39 | 03:27:48 | artifact | wrote STATE-next-actions-closed.md |
| 40 | 03:27:48 | artifact | wrote STATE-constraints.md |
| 67 | 04:53:14 | artifact | wrote FAILURES.md |
| 68 | 04:53:15 | artifact | wrote STATE.md |
| 69 | 04:53:15 | artifact | wrote STATE-constraints.md |
| 70 | 04:53:16 | artifact | wrote EXPERIMENTS/033-question-recurrence/README.md |
| 71 | 04:53:17 | artifact | wrote EXPERIMENTS/033-question-recurrence/PROTOCOL.md |
| 72 | 04:53:18 | milestone | 799 tests green; F056 recorded: the per-day world-share gate measured the calendar and had the wrong direction |
| 73 | 04:55:27 | doc_update | updated FAILURES.md |
| 74 | 04:55:27 | doc_update | updated ROADMAP.md |
| 75 | 04:55:27 | doc_update | updated STATE.md |
| 76 | 04:55:27 | session_end | E033 refuted the mission's pooled recurrence bound of 0.0223 by reading recurrence off Stack Exchange's own duplicate-closure judgement over 1000 ques |

_26 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-002-e033-measure-the-rate-of-cross-author-re/events.jsonl
```
