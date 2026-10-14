# Session 2026-10-14-002-measure-valueset-py-unchanged-on-squad-v

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T01:49:54+00:00
- **Duration:** 1932.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Measure valueset.py unchanged on SQuAD v2.0 dev - a human-written genre with real ungrounded values - for the pre-pass operating point that decides whether it is a shippable first stage

## Summary

E141 ran valueset.py unchanged on SQuAD v2.0 dev - 11,873 human-written questions, 1,204 paragraphs, no item corrupted by the experiment - and the build trigger E140 fired does not survive a second population. Detection on real human value errors 0.2826 against a declared 0.95; false positives on correct human answers 0.0113, which passes; the pre-pass resolves 0.1647 of the corpus and 0.2763 of what it clears is genuinely unsupported. The 566 misses split into 460 binding misses, the blind spot E140 declared now confirmed at scale on text nobody built for the instrument, and 106 items where century and decade forms are not extracted at all. A hand-built positive control found a third defect in one run: canonical() keys by (kind, number), so $12,500,000 and 12500000 dollars are different keys. The baseline reverses E140's reading: ground.py detects 0.7174 against 0.2826 at 0.0940 false positives against 0.0113. F126, D111, D112 filed; both artifacts stay unreleased with a measured scope.

## Next

One measurement decides the line: run valueset.py unchanged on regulatory answers a person wrote, and read conditional coverage, the false-positive rate, and the value_present share of the misses. Mostly not_extracted means genre-limited and describable; mostly value_present at this run's rate closes the line for good.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/141-valueset-second-genre/PROTOCOL.md | 5494b34fefcc | 11772 |
| EXPERIMENTS/141-valueset-second-genre/AMENDMENT-1.md | 86e0660b3c74 | 4930 |
| EXPERIMENTS/141-valueset-second-genre/AMENDMENT-2.md | 377862be4ea9 | 3850 |
| EXPERIMENTS/141-valueset-second-genre/PROTOCOL.md | 5494b34fefcc | 11772 |
| EXPERIMENTS/141-valueset-second-genre/arms.jsonl | 12b77b771d35 | 14902603 |
| EXPERIMENTS/141-valueset-second-genre/build_arms.py | 1928e336b7f2 | 4514 |
| EXPERIMENTS/141-valueset-second-genre/explain_misses.py | c6b380afa13e | 3507 |
| EXPERIMENTS/141-valueset-second-genre/gates.json | bc616d10dbd8 | 15366 |
| EXPERIMENTS/141-valueset-second-genre/misses.json | ea7134e6c6e0 | 4874 |
| EXPERIMENTS/141-valueset-second-genre/population.json | 5c2bbcfc42f4 | 289 |
| EXPERIMENTS/141-valueset-second-genre/score.py | 26d878fa9eda | 11552 |
| EXPERIMENTS/141-valueset-second-genre/test_squad.py | 38db6f2dbcda | 7741 |
| EXPERIMENTS/141-valueset-second-genre/verdicts.jsonl | ccd9a2202fda | 2378072 |
| EXPERIMENTS/141-valueset-second-genre/AMENDMENT-1.md | 86e0660b3c74 | 4930 |
| EXPERIMENTS/141-valueset-second-genre/AMENDMENT-2.md | 377862be4ea9 | 3850 |
| EXPERIMENTS/141-valueset-second-genre/PROTOCOL.md | 5494b34fefcc | 11772 |
| EXPERIMENTS/141-valueset-second-genre/RESULT.md | 7704b9920130 | 10383 |
| EXPERIMENTS/141-valueset-second-genre/SOURCES.md | 81b0a0da30db | 2442 |
| EXPERIMENTS/141-valueset-second-genre/arms.jsonl | 12b77b771d35 | 14902603 |
| EXPERIMENTS/141-valueset-second-genre/build_arms.py | 5a44bcc4129e | 4597 |
| EXPERIMENTS/141-valueset-second-genre/explain_misses.py | c6b380afa13e | 3507 |
| EXPERIMENTS/141-valueset-second-genre/gates.json | bc616d10dbd8 | 15366 |
| EXPERIMENTS/141-valueset-second-genre/misses.json | ea7134e6c6e0 | 4874 |
| EXPERIMENTS/141-valueset-second-genre/population.json | 5c2bbcfc42f4 | 289 |
| EXPERIMENTS/141-valueset-second-genre/score.py | 26d878fa9eda | 11552 |
| EXPERIMENTS/141-valueset-second-genre/test_squad.py | 38db6f2dbcda | 7741 |
| EXPERIMENTS/141-valueset-second-genre/verdicts.jsonl | ccd9a2202fda | 2378072 |
| DECISIONS-SCREENING-22.md | 42f809250c51 | 5632 |
| FAILURES-findings-42.md | b510d75905b1 | 4492 |
| DECISIONS.md | 0e515ba803ba | 26228 |
| FAILURES.md | 5c738cdb94de | 83652 |
| EXPERIMENTS/141-valueset-second-genre/AMENDMENT-1.md | 86e0660b3c74 | 4930 |
| EXPERIMENTS/141-valueset-second-genre/AMENDMENT-2.md | 377862be4ea9 | 3850 |
| EXPERIMENTS/141-valueset-second-genre/PROTOCOL.md | 5494b34fefcc | 11772 |
| EXPERIMENTS/141-valueset-second-genre/RESULT.md | 7704b9920130 | 10383 |
| EXPERIMENTS/141-valueset-second-genre/SOURCES.md | 083d933d0f35 | 2792 |
| EXPERIMENTS/141-valueset-second-genre/arms.jsonl | 12b77b771d35 | 14902603 |
| EXPERIMENTS/141-valueset-second-genre/build_arms.py | 5a44bcc4129e | 4597 |
| EXPERIMENTS/141-valueset-second-genre/explain_misses.py | c6b380afa13e | 3507 |
| EXPERIMENTS/141-valueset-second-genre/gates.json | bc616d10dbd8 | 15366 |
| EXPERIMENTS/141-valueset-second-genre/misses.json | ea7134e6c6e0 | 4874 |
| EXPERIMENTS/141-valueset-second-genre/population.json | 5c2bbcfc42f4 | 289 |
| EXPERIMENTS/141-valueset-second-genre/score.py | 26d878fa9eda | 11552 |
| EXPERIMENTS/141-valueset-second-genre/test_squad.py | 38db6f2dbcda | 7741 |
| EXPERIMENTS/141-valueset-second-genre/verdicts.jsonl | ccd9a2202fda | 2378072 |
| DECISIONS-SCREENING-22.md | 10cae13f88a7 | 5629 |
| FAILURES-findings-42.md | a9b9895dde01 | 4489 |
| DECISIONS.md | 0e515ba803ba | 26228 |
| FAILURES.md | 5c738cdb94de | 83652 |
| STATE.md | 7e1a2fcd4809 | 38065 |
| STATE-next-actions.md | 641b9c9da3a3 | 19397 |
| STATE-next-actions-d083-sweep.md | 28e21b9435b5 | 15461 |

## Commands

11 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/build_arms.py'] | 0 | 1310 |
| 5 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/build_arms.py'] | 0 | 1506 |
| 6 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/test_squad.py'] | 1 | 2714 |
| 7 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/test_squad.py'] | 0 | 3574 |
| 8 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/score.py'] | 1 | 2690 |
| 9 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/score.py'] | 1 | 23384 |
| 10 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/score.py'] | 1 | 20883 |
| 11 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/score.py'] | 0 | 22710 |
| 12 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/explain_misses.py'] | 0 | 848 |
| 13 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/test_squad.py'] | 1 | 3307 |
| 14 | ['python3', 'EXPERIMENTS/141-valueset-second-genre/test_squad.py'] | 0 | 3274 |

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
| 1 | 01:49:54 | session_start | Measure valueset.py unchanged on SQuAD v2.0 dev - a human-written genre with real ungrounded values - for the pre-pass operating point that decides wh |
| 2 | 01:50:27 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/PROTOCOL.md |
| 3 | 01:50:29 | milestone | E141 protocol predeclared before the corpus was fetched into the repository and before any instrument ran on any item |
| 4 | 01:50:47 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/build_arms.py |
| 5 | 01:52:38 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/build_arms.py |
| 6 | 01:53:05 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/test_squad.py |
| 7 | 01:54:03 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/test_squad.py |
| 8 | 01:54:07 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/score.py |
| 9 | 01:54:42 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/score.py |
| 10 | 01:55:13 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/score.py |
| 11 | 01:55:46 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/score.py |
| 12 | 01:56:42 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/explain_misses.py |
| 13 | 01:56:52 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/test_squad.py |
| 14 | 01:57:04 | command | $ python3 EXPERIMENTS/141-valueset-second-genre/test_squad.py |
| 15 | 01:57:19 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/AMENDMENT-1.md |
| 16 | 01:57:20 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/AMENDMENT-2.md |
| 17 | 01:57:21 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/PROTOCOL.md |
| 18 | 01:57:33 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/arms.jsonl |
| 19 | 01:57:34 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/build_arms.py |
| 20 | 01:57:35 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/explain_misses.py |
| 21 | 01:57:36 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/gates.json |
| 22 | 01:57:37 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/misses.json |
| 23 | 01:57:38 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/population.json |
| 24 | 01:57:38 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/score.py |
| 25 | 01:57:39 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/test_squad.py |
| 26 | 01:57:42 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/verdicts.jsonl |
| 27 | 01:57:44 | milestone | E141 scored: K1 0.2826 FAIL, K2 0.9887 PASS, K3 0.2146 FAIL, K4 PASS, K5 0.9379 PASS; triage resolves 0.1647 of the corpus; 460 of 566 K1 misses are t |
| 28 | 01:59:44 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/AMENDMENT-1.md |
| 29 | 01:59:45 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/AMENDMENT-2.md |
| 30 | 01:59:46 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/PROTOCOL.md |
| 31 | 01:59:47 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/RESULT.md |
| 32 | 01:59:48 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/SOURCES.md |
| 33 | 01:59:59 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/arms.jsonl |
| 34 | 02:00:00 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/build_arms.py |
| 35 | 02:00:01 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/explain_misses.py |
| 36 | 02:00:02 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/gates.json |
| 37 | 02:00:03 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/misses.json |
| 38 | 02:00:04 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/population.json |
| 39 | 02:00:06 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/score.py |
| 40 | 02:00:07 | artifact | wrote EXPERIMENTS/141-valueset-second-genre/test_squad.py |
| 61 | 02:21:38 | artifact | wrote FAILURES-findings-42.md |
| 62 | 02:21:39 | artifact | wrote DECISIONS.md |
| 63 | 02:21:41 | artifact | wrote FAILURES.md |
| 64 | 02:21:42 | artifact | wrote STATE.md |
| 65 | 02:21:43 | artifact | wrote STATE-next-actions.md |
| 66 | 02:21:45 | artifact | wrote STATE-next-actions-d083-sweep.md |
| 67 | 02:22:07 | doc_update | updated DECISIONS.md |
| 68 | 02:22:07 | doc_update | updated FAILURES.md |
| 69 | 02:22:07 | doc_update | updated STATE.md |
| 70 | 02:22:07 | session_end | E141 ran valueset.py unchanged on SQuAD v2.0 dev - 11,873 human-written questions, 1,204 paragraphs, no item corrupted by the experiment - and the bui |

_20 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-002-measure-valueset-py-unchanged-on-squad-v/events.jsonl
```
