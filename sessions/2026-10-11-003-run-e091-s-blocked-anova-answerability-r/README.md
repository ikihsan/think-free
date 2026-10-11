# Session 2026-10-11-003-run-e091-s-blocked-anova-answerability-r

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T01:26:03+00:00
- **Duration:** 2680.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run E091's blocked Anova answerability replication with a construct-valid discrimination gate, and record the false block

## Summary

E091 completed and landed: ran E062's construction on the Anova forum behind a false block; G0 discrimination passed (10/10, 10/10); served share 5/20=0.2500 rejects E062's 0.85 for this venue; cause is composition (13/20 vendor- or repair-bound, 4/7 answerable vs 1/13 elsewhere, p=0.0307); Arm A 0/20 program-shaped. Two analysis defects found and fixed before write-up (Fisher tail from wrong term fabricating 22x significance; comparison row built from population size). Recorded F114, D103 (Anova closed; unserved share redefined as ownership composition), repaired the FAILURES.md index violation, doc lint green.

## Next

E092: runnable test of appliance-fault diagnosis as a general need outside one vendor's forum (E091 RESULT.md section 6), with vendor/repair-bound rows screened out per D103 and pre-declared gates.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/091-anova-answerability/AMENDMENT-1.md | f08bb7dab336 | 6146 |
| EXPERIMENTS/091-anova-answerability/fetch.py | 83a8eaea6a1e | 4876 |
| EXPERIMENTS/091-anova-answerability/full.jsonl | f9c1ce155edf | 146154 |
| EXPERIMENTS/091-anova-answerability/g0_probes.py | 33a1aa97bb64 | 6624 |
| EXPERIMENTS/091-anova-answerability/g0_probes.json | 7e3f710be54a | 5579 |
| EXPERIMENTS/091-anova-answerability/G0.md | e39b1afdf412 | 6091 |
| EXPERIMENTS/091-anova-answerability/ATTEMPTS.md | baf6c433f5f8 | 5940 |
| EXPERIMENTS/091-anova-answerability/grades.py | 9be721dbf176 | 11978 |
| EXPERIMENTS/091-anova-answerability/compose.py | a0edf396ee69 | 7282 |
| EXPERIMENTS/091-anova-answerability/score.py | f0b9cb7d96e6 | 5018 |
| EXPERIMENTS/091-anova-answerability/test_fisher.py | 2fa2233d7674 | 3045 |
| EXPERIMENTS/091-anova-answerability/RESULT.md | 62e9202b99e4 | 9095 |
| EXPERIMENTS/091-anova-answerability/composition.json | ca37d4378350 | 2524 |
| EXPERIMENTS/091-anova-answerability/results.json | a0b9db69a37b | 9887 |
| EXPERIMENTS/091-anova-answerability/full.jsonl | f9c1ce155edf | 146154 |
| EXPERIMENTS/091-anova-answerability/AMENDMENT-1.md | 20f5388357ca | 7420 |
| EXPERIMENTS/091-anova-answerability/ATTEMPTS.md | c5edc1079f93 | 6031 |
| EXPERIMENTS/091-anova-answerability/G0.md | 62b4271572fb | 6182 |
| EXPERIMENTS/091-anova-answerability/PROTOCOL.md | a1870d70bbea | 6240 |
| EXPERIMENTS/091-anova-answerability/RESULT.md | 62e9202b99e4 | 9095 |
| EXPERIMENTS/091-anova-answerability/VERDICT.md | ec8a27d55b78 | 6508 |
| EXPERIMENTS/091-anova-answerability/assistant_query.py | c291ccefce20 | 1527 |
| EXPERIMENTS/091-anova-answerability/compose.py | a0edf396ee69 | 7282 |
| EXPERIMENTS/091-anova-answerability/composition.json | ca37d4378350 | 2524 |
| EXPERIMENTS/091-anova-answerability/fetch.py | 83a8eaea6a1e | 4876 |
| EXPERIMENTS/091-anova-answerability/full.jsonl | f9c1ce155edf | 146154 |
| EXPERIMENTS/091-anova-answerability/g0_probes.json | 7e3f710be54a | 5579 |
| EXPERIMENTS/091-anova-answerability/g0_probes.py | 33a1aa97bb64 | 6624 |
| EXPERIMENTS/091-anova-answerability/grades.py | 9be721dbf176 | 11978 |
| EXPERIMENTS/091-anova-answerability/population.jsonl | 572643e0d63f | 7094 |
| EXPERIMENTS/091-anova-answerability/probes.jsonl | 7750166735bc | 9653 |
| EXPERIMENTS/091-anova-answerability/results.json | a0b9db69a37b | 9887 |
| EXPERIMENTS/091-anova-answerability/score.py | f0b9cb7d96e6 | 5018 |
| EXPERIMENTS/091-anova-answerability/test_fisher.py | 2fa2233d7674 | 3045 |
| FAILURES-findings-37.md | 502a2d362e43 | 17573 |
| FAILURES.md | 78a3d5b4b76b | 68553 |
| STATE.md | d8bf370adec9 | 22638 |
| STATE-next-actions.md | 70a6cff1c483 | 10657 |
| DECISIONS-SCREENING-18.md | b474f560ba5d | 9552 |
| DECISIONS.md | 9be2894e502b | 20075 |
| docs/INDEX.md | eb250161c5c3 | 44712 |
| sessions/INDEX.md | 9d458320f401 | 6803 |
| EXPERIMENTS/091-anova-answerability/PROTOCOL.md | a1870d70bbea | 6240 |

## Commands

16 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/091-anova-answerability/fetch.py', '--verify'] | 0 | 194 |
| 3 | ['python3', 'EXPERIMENTS/091-anova-answerability/fetch.py'] | 0 | 37014 |
| 4 | ['python3', 'EXPERIMENTS/091-anova-answerability/fetch.py'] | 0 | 37065 |
| 5 | ['python3', 'EXPERIMENTS/091-anova-answerability/fetch.py'] | 0 | 37174 |
| 10 | ['python3', 'EXPERIMENTS/091-anova-answerability/g0_probes.py'] | 0 | 41 |
| 15 | ['python3', 'EXPERIMENTS/091-anova-answerability/score.py'] | 1 | 104 |
| 16 | ['python3', 'EXPERIMENTS/091-anova-answerability/score.py'] | 0 | 191 |
| 18 | ['python3', 'EXPERIMENTS/091-anova-answerability/score.py'] | 0 | 101 |
| 19 | ['python3', 'EXPERIMENTS/091-anova-answerability/compose.py'] | 0 | 212 |
| 20 | ['python3', 'EXPERIMENTS/091-anova-answerability/compose.py'] | 0 | 105 |
| 21 | ['python3', 'EXPERIMENTS/091-anova-answerability/compose.py'] | 0 | 114 |
| 22 | ['python3', '-m', 'unittest', 'discover', '-s', 'EXPERIMENTS/091-anova-answerability', '-t', 'EXPERIMENTS/091-anova-answerability', '-p', 'test_*.py', | 0 | 416 |
| 32 | ['python3', 'EXPERIMENTS/091-anova-answerability/fetch.py', '--verify'] | 0 | 262 |
| 33 | ['python3', 'EXPERIMENTS/091-anova-answerability/score.py'] | 0 | 95 |
| 34 | ['python3', 'EXPERIMENTS/091-anova-answerability/compose.py'] | 0 | 90 |
| 35 | ['python3', '-m', 'unittest', 'discover', '-s', 'EXPERIMENTS/091-anova-answerability', '-t', 'EXPERIMENTS/091-anova-answerability', '-p', 'test_*.py', | 0 | 462 |

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
| 1 | 01:26:03 | session_start | Run E091's blocked Anova answerability replication with a construct-valid discrimination gate, and record the false block |
| 2 | 01:26:55 | command | $ python3 EXPERIMENTS/091-anova-answerability/fetch.py --verify |
| 3 | 01:27:36 | command | $ python3 EXPERIMENTS/091-anova-answerability/fetch.py |
| 4 | 01:28:47 | command | $ python3 EXPERIMENTS/091-anova-answerability/fetch.py |
| 5 | 01:29:43 | command | $ python3 EXPERIMENTS/091-anova-answerability/fetch.py |
| 6 | 01:29:49 | milestone | E091's stated block is false: its own protocol accepts 'or equivalent' and E062/E066 used this model as the instrument. Two instrument defects found a |
| 7 | 01:29:50 | artifact | wrote EXPERIMENTS/091-anova-answerability/AMENDMENT-1.md |
| 8 | 01:29:51 | artifact | wrote EXPERIMENTS/091-anova-answerability/fetch.py |
| 9 | 01:29:52 | artifact | wrote EXPERIMENTS/091-anova-answerability/full.jsonl |
| 10 | 01:30:31 | command | $ python3 EXPERIMENTS/091-anova-answerability/g0_probes.py |
| 11 | 01:31:20 | artifact | wrote EXPERIMENTS/091-anova-answerability/g0_probes.py |
| 12 | 01:31:21 | artifact | wrote EXPERIMENTS/091-anova-answerability/g0_probes.json |
| 13 | 01:31:22 | artifact | wrote EXPERIMENTS/091-anova-answerability/G0.md |
| 14 | 01:31:22 | artifact | wrote EXPERIMENTS/091-anova-answerability/ATTEMPTS.md |
| 15 | 01:31:52 | command | $ python3 EXPERIMENTS/091-anova-answerability/score.py |
| 16 | 01:33:50 | command | $ python3 EXPERIMENTS/091-anova-answerability/score.py |
| 17 | 01:34:54 | milestone | Inherited session recovered after worker process death: score.py on disk (mtime 01:32:39) postdates the failed run (01:31:52), so the earlier exit 1 w |
| 18 | 01:35:58 | command | $ python3 EXPERIMENTS/091-anova-answerability/score.py |
| 19 | 01:36:03 | command | $ python3 EXPERIMENTS/091-anova-answerability/compose.py |
| 20 | 01:36:18 | command | $ python3 EXPERIMENTS/091-anova-answerability/compose.py |
| 21 | 01:39:01 | command | $ python3 EXPERIMENTS/091-anova-answerability/compose.py |
| 22 | 01:39:16 | command | $ python3 -m unittest discover -s EXPERIMENTS/091-anova-answerability -t EXPERIMENTS/091-anova-answerability -p test_*.py -v |
| 23 | 01:40:01 | artifact | wrote EXPERIMENTS/091-anova-answerability/grades.py |
| 24 | 01:40:02 | artifact | wrote EXPERIMENTS/091-anova-answerability/compose.py |
| 25 | 01:40:03 | artifact | wrote EXPERIMENTS/091-anova-answerability/score.py |
| 26 | 01:40:04 | artifact | wrote EXPERIMENTS/091-anova-answerability/test_fisher.py |
| 27 | 01:40:05 | artifact | wrote EXPERIMENTS/091-anova-answerability/RESULT.md |
| 28 | 01:40:07 | artifact | wrote EXPERIMENTS/091-anova-answerability/composition.json |
| 29 | 01:40:08 | artifact | wrote EXPERIMENTS/091-anova-answerability/results.json |
| 30 | 01:40:09 | artifact | wrote EXPERIMENTS/091-anova-answerability/full.jsonl |
| 31 | 01:40:10 | milestone | Arm B: K1 FAILS (5/20 = 0.2500, CI95 [0.1119, 0.4687]); K2 GENERALIZATION REJECTED (upper 0.4687 < E062 lower 0.6396). Arm A: 0 of 20 tool-shaped. Com |
| 32 | 01:41:47 | command | $ python3 EXPERIMENTS/091-anova-answerability/fetch.py --verify |
| 33 | 01:41:55 | command | $ python3 EXPERIMENTS/091-anova-answerability/score.py |
| 34 | 01:42:00 | command | $ python3 EXPERIMENTS/091-anova-answerability/compose.py |
| 35 | 01:42:02 | command | $ python3 -m unittest discover -s EXPERIMENTS/091-anova-answerability -t EXPERIMENTS/091-anova-answerability -p test_*.py -v |
| 36 | 02:09:57 | artifact | E091 Anova answerability replication: protocol, G0 gate evidence, raw attempts, grades, scores, composition, Fisher tests |
| 37 | 02:09:57 | artifact | E091 Anova answerability replication: protocol, G0 gate evidence, raw attempts, grades, scores, composition, Fisher tests |
| 38 | 02:09:58 | artifact | E091 Anova answerability replication: protocol, G0 gate evidence, raw attempts, grades, scores, composition, Fisher tests |
| 39 | 02:09:59 | artifact | E091 Anova answerability replication: protocol, G0 gate evidence, raw attempts, grades, scores, composition, Fisher tests |
| 40 | 02:09:59 | artifact | E091 Anova answerability replication: protocol, G0 gate evidence, raw attempts, grades, scores, composition, Fisher tests |
| 59 | 02:10:16 | artifact | E091 record-keeping: F114 finding, D103 Anova closure decision, index updates |
| 60 | 02:10:17 | artifact | E091 record-keeping: F114 finding, D103 Anova closure decision, index updates |
| 61 | 02:10:17 | artifact | E091 record-keeping: F114 finding, D103 Anova closure decision, index updates |
| 62 | 02:10:18 | artifact | E091 record-keeping: F114 finding, D103 Anova closure decision, index updates |
| 63 | 02:10:19 | artifact | E091 record-keeping: F114 finding, D103 Anova closure decision, index updates |
| 64 | 02:10:44 | doc_update | updated DECISIONS-SCREENING-18.md |
| 65 | 02:10:44 | doc_update | updated DECISIONS.md |
| 66 | 02:10:44 | doc_update | updated FAILURES.md |
| 67 | 02:10:44 | doc_update | updated STATE.md |
| 68 | 02:10:44 | session_end | E091 completed and landed: ran E062's construction on the Anova forum behind a false block; G0 discrimination passed (10/10, 10/10); served share 5/20 |

_18 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-003-run-e091-s-blocked-anova-answerability-r/events.jsonl
```
