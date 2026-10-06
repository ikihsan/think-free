# Session 2026-10-06-006-apply-d067-forward-find-a-buildable-cand

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T08:43:45+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

apply D067 forward: find a buildable candidate from the one on-disk population nobody has read for buildability (the 589 never-answered HN need statements), check its mechanism against existing sources in ~2 requests, and build it

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| stage-lines/stg | 62168a089520 | 9951 |
| stage-lines/stagelib.py | 44f1a28adac5 | 10708 |
| stage-lines/README.md | 960e88eebacb | 3669 |
| stage-lines/test_stage.py | 07272451dd7d | 10922 |
| stage-lines/test_parser.py | d80769d6f941 | 2156 |
| stage-lines/tests_support.py | b87e87a9b253 | 3154 |
| stage-lines/stg | 62168a089520 | 9951 |
| stage-lines/stagelib.py | 44f1a28adac5 | 10708 |
| stage-lines/README.md | 960e88eebacb | 3669 |
| stage-lines/test_stage.py | 07272451dd7d | 10922 |
| stage-lines/test_parser.py | d80769d6f941 | 2156 |
| stage-lines/tests_support.py | b87e87a9b253 | 3154 |
| EXPERIMENTS/037-line-staging/README.md | b316af60b197 | 7530 |
| EXPERIMENTS/037-line-staging/compare.py | 0169c66e75f2 | 7069 |
| EXPERIMENTS/037-line-staging/driver.py | 7cd044b04e86 | 5089 |
| EXPERIMENTS/037-line-staging/raw/compare.jsonl | 477f884c13e0 | 7026 |
| HYPOTHESES-candidates.md | af60b1e4af70 | 4604 |
| FAILURES-findings-25.md | 736ce7e02af0 | 5024 |
| DECISIONS-SCREENING-8.md | 8cbb9acecbf7 | 3667 |

## Commands

7 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/037-line-staging/compare.py'] | 1 | 1130 |
| 4 | ['python3', 'EXPERIMENTS/037-line-staging/compare.py'] | 0 | 17446 |
| 5 | ['python3', 'EXPERIMENTS/037-line-staging/compare.py'] | 0 | 23106 |
| 6 | ['python3', 'EXPERIMENTS/037-line-staging/compare.py'] | 0 | 25412 |
| 7 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 501040 |
| 8 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 653486 |
| 9 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 604718 |

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
| 1 | 08:43:45 | session_start | apply D067 forward: find a buildable candidate from the one on-disk population nobody has read for buildability (the 589 never-answered HN need statem |
| 2 | 08:46:43 | milestone | D067 answered on the real mechanism: git add -p is TTY-only (piped keys stage 0 files, exit 0, silent), git apply --cached needs a hand-written header |
| 3 | 09:02:22 | command | $ python3 EXPERIMENTS/037-line-staging/compare.py |
| 4 | 09:03:00 | command | $ python3 EXPERIMENTS/037-line-staging/compare.py |
| 5 | 09:04:07 | command | $ python3 EXPERIMENTS/037-line-staging/compare.py |
| 6 | 09:06:45 | command | $ python3 EXPERIMENTS/037-line-staging/compare.py |
| 7 | 09:29:57 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 8 | 09:40:57 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 9 | 09:47:46 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 10 | 09:50:00 | artifact | wrote stage-lines/stg |
| 11 | 09:50:01 | artifact | wrote stage-lines/stagelib.py |
| 12 | 09:50:02 | artifact | wrote stage-lines/README.md |
| 13 | 09:50:03 | artifact | wrote stage-lines/test_stage.py |
| 14 | 09:50:05 | artifact | wrote stage-lines/test_parser.py |
| 15 | 09:50:06 | artifact | wrote stage-lines/tests_support.py |
| 16 | 09:50:14 | artifact | wrote stage-lines/stg |
| 17 | 09:50:15 | artifact | wrote stage-lines/stagelib.py |
| 18 | 09:50:15 | artifact | wrote stage-lines/README.md |
| 19 | 09:50:16 | artifact | wrote stage-lines/test_stage.py |
| 20 | 09:50:16 | artifact | wrote stage-lines/test_parser.py |
| 21 | 09:50:17 | artifact | wrote stage-lines/tests_support.py |
| 22 | 09:50:18 | artifact | wrote EXPERIMENTS/037-line-staging/README.md |
| 23 | 09:50:18 | artifact | wrote EXPERIMENTS/037-line-staging/compare.py |
| 24 | 09:50:19 | artifact | wrote EXPERIMENTS/037-line-staging/driver.py |
| 25 | 09:50:20 | artifact | wrote EXPERIMENTS/037-line-staging/raw/compare.jsonl |
| 26 | 09:50:21 | artifact | wrote HYPOTHESES-candidates.md |
| 27 | 09:50:22 | artifact | wrote FAILURES-findings-25.md |
| 28 | 09:50:22 | artifact | wrote DECISIONS-SCREENING-8.md |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-006-apply-d067-forward-find-a-buildable-cand/events.jsonl
```
