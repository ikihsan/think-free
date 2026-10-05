# Session 2026-10-05-002-test-whether-f033-s-project-level-denomi

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T01:24:48+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test whether F033's project-level denominator hid genuine cross-person recurrence in the need corpus (E019)

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/019-corpus-person-diversity/README.md | da719a8454d7 | 12895 |
| EXPERIMENTS/019-corpus-person-diversity/results.json | 3b67fe6e820c | 8863 |
| EXPERIMENTS/019-corpus-person-diversity/corpus_authors.py | 77cf6c8fe17d | 5247 |
| EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py | c458e73c99ca | 5956 |
| EXPERIMENTS/019-corpus-person-diversity/recurrence_probe.py | f531a0701db4 | 7585 |
| EXPERIMENTS/019-corpus-person-diversity/stats.py | 9fb5582213e1 | 8747 |
| FAILURES-findings-15.md | d2e0827953d1 | 7078 |
| DECISIONS-SCREENING-2.md | b6f6ea73e1d3 | 13749 |
| tools/originlib/decisionindex.py | f999fe05c8fc | 5361 |
| tests/test_decision_row_pattern.py | 6fe3180bd864 | 3069 |
| EXPERIMENTS/019-corpus-person-diversity/results.json | 3e19ee4a78a2 | 10982 |
| EXPERIMENTS/019-corpus-person-diversity/raw/arm_a2.json | e68413ac64ca | 3907 |
| DECISIONS-SCREENING-2.md | cb83e82e82e0 | 14752 |
| FAILURES-findings-15.md | ca34ac8ea167 | 8156 |

## Commands

10 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/corpus_authors.py'] | 0 | 73419 |
| 6 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/stats.py'] | 0 | 120 |
| 8 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/recurrence_probe.py'] | 0 | 32537 |
| 9 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py'] | 1 | 1079 |
| 10 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py'] | 0 | 229 |
| 11 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/stats.py'] | 0 | 124 |
| 12 | ['bash', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 \| tail -4'] | 0 | 342725 |
| 24 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py'] | 0 | 596 |
| 25 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/stats.py'] | 0 | 504 |
| 26 | ['python3', 'EXPERIMENTS/019-corpus-person-diversity/stats.py'] | 0 | 195 |

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
| 1 | 01:24:48 | session_start | Test whether F033's project-level denominator hid genuine cross-person recurrence in the need corpus (E019) |
| 2 | 01:24:56 | task_rewrite | appended a create record for T-0063 |
| 3 | 01:25:15 | task_rewrite | rewrote tasks/T-0063-test-whether-f033-s-project-level-denominator-hi.md (status: claimed) |
| 4 | 01:25:16 | task_rewrite | appended a claim record for T-0063 |
| 5 | 01:43:34 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/corpus_authors.py |
| 6 | 01:43:52 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/stats.py |
| 7 | 01:44:18 | milestone | arm A measured: 1401 comments carry 1250 distinct authors (median 1/author, max 8) over 466 days; gate A1 met at 100%, so the corpus is a wide audienc |
| 8 | 01:45:27 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/recurrence_probe.py |
| 9 | 01:46:38 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py |
| 10 | 01:46:47 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py |
| 11 | 01:48:10 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/stats.py |
| 12 | 02:00:20 | command | $ bash -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 \| tail -4 |
| 13 | 02:10:22 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/README.md |
| 14 | 02:10:23 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/results.json |
| 15 | 02:10:23 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/corpus_authors.py |
| 16 | 02:10:24 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py |
| 17 | 02:10:25 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/recurrence_probe.py |
| 18 | 02:10:25 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/stats.py |
| 19 | 02:10:26 | artifact | wrote FAILURES-findings-15.md |
| 20 | 02:10:26 | artifact | wrote DECISIONS-SCREENING-2.md |
| 21 | 02:10:27 | artifact | wrote tools/originlib/decisionindex.py |
| 22 | 02:10:27 | artifact | wrote tests/test_decision_row_pattern.py |
| 23 | 02:10:28 | milestone | E019 complete: 1250 distinct authors measured (gate A1 met), A2 inside its declared band so no verdict, arm B's instrument failed its own controls; F0 |
| 24 | 02:11:56 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/arm_a2_local.py |
| 25 | 02:13:57 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/stats.py |
| 26 | 02:14:12 | command | $ python3 EXPERIMENTS/019-corpus-person-diversity/stats.py |
| 27 | 02:14:13 | milestone | robustness check falsified this session's own headline (79.25% is single-word overlap, not request uniqueness); the claim is corrected in weaker form  |
| 28 | 02:20:11 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/results.json |
| 29 | 02:20:12 | artifact | wrote EXPERIMENTS/019-corpus-person-diversity/raw/arm_a2.json |
| 30 | 02:20:13 | artifact | wrote DECISIONS-SCREENING-2.md |
| 31 | 02:20:13 | artifact | wrote FAILURES-findings-15.md |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-002-test-whether-f033-s-project-level-denomi/events.jsonl
```
