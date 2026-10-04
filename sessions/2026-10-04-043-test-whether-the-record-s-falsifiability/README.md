# Session 2026-10-04-043-test-whether-the-record-s-falsifiability

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T18:32:48+00:00
- **Duration:** 1397.6s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test whether the record's falsifiability-first screen is what starves candidate supply, and generate candidates from live primary sources instead of sealed model-prior reports

## Summary

Measured effort allocation (F025, D048): experiments got 1.3% of day-two commits; next-action list had no invention item. Candidate generation from live sources was not done. D048 body was left missing at interruption; this session's closer added it. 43 tests cover the measurement.

## Next

Pick one invention-bearing next action (STATE-next-actions.md), generated from live primary sources, and run its kill gate.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/measure_allocation.py | e62db15960a4 | 7237 |
| tests/test_allocation_measurement.py | fc2e0921f47e | 7948 |
| FAILURES-findings-5.md | c4999d1dab70 | 18151 |
| FAILURES.md | 8cec4c4c8b6c | 6070 |
| DECISIONS-SCREENING.md | 35205f4b8130 | 10850 |

## Commands

13 captured, 4 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '-c', '\ngit log --format="COMMIT\|%H\|%s" --name-only origin/research/origin \| python3 -c "\nimport sys,collections\nbuckets=collections.Co | 0 | 931 |
| 3 | ['bash', '-c', '\ngit log --format="COMMIT\|%ad\|%s" --date=short --name-only origin/research/origin \| python3 -c "\nimport sys,collections\nper_day= | 0 | 406 |
| 4 | ['bash', '-c', '\ngit log --format="COMMIT\|%ad" --date=short --name-only origin/research/origin \| python3 -c "\nimport sys,collections\nper_day=coll | 0 | 1095 |
| 5 | ['bash', '-c', '\npython3 - <<PY\nimport re,glob\ndef ids(pat, files):\n    out=set()\n    for f in files:\n        try: t=open(f,encoding="utf-8",err | 0 | 134 |
| 7 | ['bash', '-c', '\nloc() { find "$@" -type f \\( -name "*.py" -o -name "origin" -o -name "x" \\) 2>/dev/null \| grep -v __pycache__ \| xargs wc -l 2>/d | 0 | 417 |
| 9 | ['tools/measure_allocation.py'] | 1 | 1021 |
| 10 | ['tools/measure_allocation.py'] | 1 | 985 |
| 11 | ['tools/measure_allocation.py'] | 0 | 490 |
| 12 | ['tools/measure_allocation.py'] | 0 | 894 |
| 13 | ['tools/measure_allocation.py', '--json'] | 0 | 887 |
| 14 | ['python3', '-m', 'unittest', 'tests.test_allocation_measurement', '-v'] | 1 | 806 |
| 15 | ['python3', '-m', 'unittest', 'tests.test_allocation_measurement', '-v'] | 1 | 1037 |
| 16 | ['python3', '-m', 'unittest', 'tests.test_allocation_measurement', '-v'] | 0 | 1026 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:32:48 | session_start | Test whether the record's falsifiability-first screen is what starves candidate supply, and generate candidates from live primary sources instead of s |
| 2 | 18:33:08 | command | $ bash -c  git log --format="COMMIT\|%H\|%s" --name-only origin/research/origin \| python3 -c " import sys,collections buckets=collections.Counte |
| 3 | 18:33:15 | command | $ bash -c  git log --format="COMMIT\|%ad\|%s" --date=short --name-only origin/research/origin \| python3 -c " import sys,collections per_day=coll |
| 4 | 18:33:27 | command | $ bash -c  git log --format="COMMIT\|%ad" --date=short --name-only origin/research/origin \| python3 -c " import sys,collections per_day=collect |
| 5 | 18:33:28 | command | $ bash -c  python3 - <<PY import re,glob def ids(pat, files):     out=set()     for f in files:         try: t=open(f,encoding="utf-8",errors= |
| 6 | 18:34:18 | milestone | measured the drift mechanically from git: 375 commits, 19 (5.1%) touch EXPERIMENTS/; day 1 = 11.1% of commits measured the world, day 2 = 1.3%; machin |
| 7 | 18:35:20 | command | $ bash -c  loc() { find "$@" -type f \( -name "*.py" -o -name "origin" -o -name "x" \) 2>/dev/null \| grep -v __pycache__ \| xargs wc -l 2>/dev/ |
| 8 | 18:35:39 | milestone | drift measured three ways: (1) 19/375 commits (5.1%) touch EXPERIMENTS; day1 11.1% -> day2 1.3%; (2) ~7 of 24 findings are about the world, 17 about t |
| 9 | 18:36:16 | command | $ tools/measure_allocation.py |
| 10 | 18:36:25 | command | $ tools/measure_allocation.py |
| 11 | 18:36:35 | command | $ tools/measure_allocation.py |
| 12 | 18:36:49 | command | $ tools/measure_allocation.py |
| 13 | 18:36:51 | command | $ tools/measure_allocation.py --json |
| 14 | 18:37:25 | command | $ python3 -m unittest tests.test_allocation_measurement -v |
| 15 | 18:37:37 | command | $ python3 -m unittest tests.test_allocation_measurement -v |
| 16 | 18:37:52 | command | $ python3 -m unittest tests.test_allocation_measurement -v |
| 17 | 18:38:55 | artifact | wrote tools/measure_allocation.py |
| 18 | 18:38:55 | artifact | wrote tests/test_allocation_measurement.py |
| 19 | 18:38:56 | artifact | wrote FAILURES-findings-5.md |
| 20 | 18:38:57 | artifact | wrote FAILURES.md |
| 21 | 18:55:57 | artifact | wrote DECISIONS-SCREENING.md |
| 22 | 18:56:05 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 23 | 18:56:05 | doc_update | updated DECISIONS-SCREENING.md |
| 24 | 18:56:05 | doc_update | updated DECISIONS.md |
| 25 | 18:56:05 | doc_update | updated FAILURES.md |
| 26 | 18:56:05 | session_end | Measured effort allocation (F025, D048): experiments got 1.3% of day-two commits; next-action list had no invention item. Candidate generation from li |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-043-test-whether-the-record-s-falsifiability/events.jsonl
```
