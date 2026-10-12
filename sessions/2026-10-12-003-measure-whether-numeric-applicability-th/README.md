# Session 2026-10-12-003-measure-whether-numeric-applicability-th

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T02:37:52+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure whether numeric applicability thresholds in the eCFR are numerous and counting-rule-divergent enough to support a tool, before building anything

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/115-applicability-thresholds/PROTOCOL.md | a1f9d0b773da | 5842 |
| EXPERIMENTS/115-applicability-thresholds/M1.md | 4e29f2ea8189 | 6243 |
| EXPERIMENTS/115-applicability-thresholds/harvest.py | 06b577c7bd56 | 14003 |
| EXPERIMENTS/115-applicability-thresholds/m1-summary.json | 2ee3f4f6343e | 421 |
| EXPERIMENTS/115-applicability-thresholds/M2.md | 269c82fd02ab | 7126 |
| EXPERIMENTS/115-applicability-thresholds/M2B-AMENDMENT.md | 7ab71bf555e5 | 2875 |
| EXPERIMENTS/115-applicability-thresholds/M2-CASES.md | 5141d28371f2 | 9532 |
| EXPERIMENTS/115-applicability-thresholds/answers.jsonl | 5812f6fe7205 | 4664 |
| EXPERIMENTS/115-applicability-thresholds/answers-m2b.jsonl | 5cdd78039816 | 3985 |
| EXPERIMENTS/115-applicability-thresholds/answers-null-naive.jsonl | 7b5de772818f | 2118 |
| EXPERIMENTS/115-applicability-thresholds/score.py | 1f2312c6712f | 6264 |
| EXPERIMENTS/115-applicability-thresholds/test_score.py | 0faaf8ede313 | 3733 |
| EXPERIMENTS/115-applicability-thresholds/m2-result.json | 6fc4bda3868c | 2420 |
| EXPERIMENTS/115-applicability-thresholds/m2b-result.json | b5ff07db9f99 | 2425 |
| EXPERIMENTS/115-applicability-thresholds/nullnaive-result.json | 09829cb0f1e5 | 2458 |
| EXPERIMENTS/115-applicability-thresholds/parts-title29.jsonl | 502887cc6851 | 1323693 |
| FAILURES-findings-40.md | 0025b792f34d | 7284 |
| DECISIONS-SCREENING-20.md | e64642255fa2 | 5503 |
| FAILURES.md | 8b8557602cf7 | 76550 |
| DECISIONS.md | 553570aab577 | 23373 |
| EXPERIMENTS/115-applicability-thresholds/test_classify.py | 5b526acea31c | 5001 |

## Commands

20 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', '-o', '/dev/null', '-w', 'ecfr-titles:%{http_code}\\n', 'https://www.ecfr.gov/api/versioner/v1/titles.json'] | 0 | 767 |
| 3 | ['curl', '-s', 'https://www.ecfr.gov/api/versioner/v1/structure/2026-01-01/title-29.json', '-o', '/tmp/opencode/t29.json', '-w', 't29:%{http_code} siz | 0 | 2288 |
| 4 | ['curl', '-s', '-o', '/dev/null', '-w', 'dol-flsa:%{http_code}\\n', 'https://www.dol.gov/agencies/whd/flsa/misclassification'] | 0 | 540 |
| 5 | ['curl', '-s', '-o', '/dev/null', '-w', 'irs-aca:%{http_code}\\n', 'https://www.irs.gov/affordable-care-act/employers'] | 0 | 1742 |
| 6 | ['curl', '-s', '-o', '/dev/null', '-w', 'dol-fmla:%{http_code}\\n', 'https://www.dol.gov/agencies/whd/fmla'] | 0 | 271 |
| 7 | ['tools/origin', 'id', 'next', 'E'] | 1 | 331 |
| 8 | ['tools/origin', 'id', 'next', 'F'] | 0 | 1595 |
| 15 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py'] | 1 | 502 |
| 16 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py'] | 1 | 492 |
| 17 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py'] | 0 | 96 |
| 19 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers-m2b.jsonl', '--arm', 'M2b'] | 0 | 112 |
| 20 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers-null-naive.jsonl', '--arm', 'NULL-naive'] | 0 | 299 |
| 21 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers.jsonl', '--arm', 'M2'] | 0 | 90 |
| 22 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers-m2b.jsonl', '--arm', 'M2b'] | 0 | 118 |
| 23 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers-null-naive.jsonl', '--arm', 'NULL-naive'] | 0 | 106 |
| 24 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers.jsonl', '--arm', 'M2'] | 0 | 124 |
| 25 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers-m2b.jsonl', '--arm', 'M2b'] | 0 | 109 |
| 26 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/score.py', '--answers', 'answers-null-naive.jsonl', '--arm', 'NULL-naive'] | 0 | 106 |
| 27 | ['python3', 'EXPERIMENTS/115-applicability-thresholds/test_score.py'] | 0 | 314 |
| 45 | ['tools/origin', 'doc', 'index'] | 0 | 7386 |

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
| 1 | 02:37:52 | session_start | Measure whether numeric applicability thresholds in the eCFR are numerous and counting-rule-divergent enough to support a tool, before building anythi |
| 2 | 02:38:09 | command | $ curl -s -o /dev/null -w ecfr-titles:%{http_code}\n https://www.ecfr.gov/api/versioner/v1/titles.json |
| 3 | 02:38:12 | command | $ curl -s https://www.ecfr.gov/api/versioner/v1/structure/2026-01-01/title-29.json -o /tmp/opencode/t29.json -w t29:%{http_code} size:%{size_d |
| 4 | 02:38:37 | command | $ curl -s -o /dev/null -w dol-flsa:%{http_code}\n https://www.dol.gov/agencies/whd/flsa/misclassification |
| 5 | 02:38:40 | command | $ curl -s -o /dev/null -w irs-aca:%{http_code}\n https://www.irs.gov/affordable-care-act/employers |
| 6 | 02:38:41 | command | $ curl -s -o /dev/null -w dol-fmla:%{http_code}\n https://www.dol.gov/agencies/whd/fmla |
| 7 | 02:38:58 | command | $ tools/origin id next E |
| 8 | 02:39:01 | command | $ tools/origin id next F |
| 9 | 02:39:35 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/PROTOCOL.md |
| 10 | 02:39:36 | milestone | E115 protocol declared before any regulation text read |
| 11 | 02:49:54 | milestone | M1 harvest of CFR title 29 running; extractor validated on parts 0/1904/825/1910 |
| 12 | 03:00:25 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/M1.md |
| 13 | 03:00:26 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/harvest.py |
| 14 | 03:00:26 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/m1-summary.json |
| 15 | 03:02:09 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py |
| 16 | 03:02:22 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py |
| 17 | 03:02:40 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py |
| 18 | 03:03:06 | milestone | E115 M2 scored 14/14; M2b ablation declared as an amendment |
| 19 | 03:03:45 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers-m2b.jsonl --arm M2b |
| 20 | 03:03:54 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers-null-naive.jsonl --arm NULL-naive |
| 21 | 03:04:37 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers.jsonl --arm M2 |
| 22 | 03:04:38 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers-m2b.jsonl --arm M2b |
| 23 | 03:04:39 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers-null-naive.jsonl --arm NULL-naive |
| 24 | 03:04:51 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers.jsonl --arm M2 |
| 25 | 03:04:52 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers-m2b.jsonl --arm M2b |
| 26 | 03:04:53 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/score.py --answers answers-null-naive.jsonl --arm NULL-naive |
| 27 | 03:05:14 | command | $ python3 EXPERIMENTS/115-applicability-thresholds/test_score.py |
| 28 | 03:05:24 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/M2.md |
| 29 | 03:05:25 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/M2B-AMENDMENT.md |
| 30 | 03:05:26 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/M2-CASES.md |
| 31 | 03:05:27 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/answers.jsonl |
| 32 | 03:05:28 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/answers-m2b.jsonl |
| 33 | 03:05:29 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/answers-null-naive.jsonl |
| 34 | 03:05:31 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/score.py |
| 35 | 03:05:32 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/test_score.py |
| 36 | 03:05:33 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/m2-result.json |
| 37 | 03:05:33 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/m2b-result.json |
| 38 | 03:05:34 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/nullnaive-result.json |
| 39 | 03:05:36 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/parts-title29.jsonl |
| 40 | 03:07:42 | decision | E115 applicability-threshold line closes on a served population (6/6 counting-rule cases with no clause supplied, 0/6 for the naive reading); the CFR  |
| 41 | 03:07:44 | artifact | wrote FAILURES-findings-40.md |
| 42 | 03:07:45 | artifact | wrote DECISIONS-SCREENING-20.md |
| 43 | 03:07:45 | artifact | wrote FAILURES.md |
| 44 | 03:07:46 | artifact | wrote DECISIONS.md |
| 45 | 03:07:55 | command | $ tools/origin doc index |
| 46 | 03:33:04 | artifact | wrote EXPERIMENTS/115-applicability-thresholds/test_classify.py |
| 47 | 03:33:07 | milestone | landing completed: test_classify.py written, both pinned defect shapes reproduce, 8+6 tests green |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-003-measure-whether-numeric-applicability-th/events.jsonl
```
