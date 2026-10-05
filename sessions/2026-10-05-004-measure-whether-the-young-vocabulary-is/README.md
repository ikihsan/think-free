# Session 2026-10-05-004-measure-whether-the-young-vocabulary-is

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T02:44:46+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure whether the young vocabulary is served by copied directories rather than installations, using a code-search instrument the record says does not exist

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md | 1743f981724a | 9526 |

## Commands

23 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 6 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/coverage.py'] | 0 | 13711 |
| 7 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/coverage.py', '--delay', '8'] | 0 | 630670 |
| 8 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/copycount.py', 'context:global file:^\\.claude/hooks/ select:repo count:4000', 'context:global fi | 0 | 175230 |
| 9 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/copycount.py', 'context:global file:^CLAUDE\\.md$ select:repo count:20000', 'context:global file: | 0 | 46626 |
| 10 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/copycount.py', 'context:global file:^\\.claude/hooks/session-start\\.sh$ select:repo count:4000', | 0 | 81094 |
| 11 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/copycount.py', 'context:global file:^\\.claude/hooks/session-start\\.sh$ select:repo count:4000', | 0 | 80693 |
| 12 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/forkstatus.py'] | 0 | 102 |
| 13 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/forkstatus.py'] | 0 | 13641 |
| 14 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/forkstatus.py'] | 0 | 122 |
| 15 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/forkstatus.py'] | 0 | 83184 |
| 16 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/forkstatus.py'] | 0 | 118186 |
| 17 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/forkstatus.py'] | 1 | 676 |
| 18 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/forkstatus.py'] | 0 | 527061 |
| 19 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 8685 |
| 20 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 7585 |
| 21 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 11109 |
| 22 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 54131 |
| 23 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 46207 |
| 24 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 58094 |
| 25 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 60269 |
| 26 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 61089 |
| 27 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 442577 |
| 28 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 496420 |

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
| 1 | 02:44:46 | session_start | Measure whether the young vocabulary is served by copied directories rather than installations, using a code-search instrument the record says does no |
| 2 | 02:46:28 | task_rewrite | appended a create record for T-0064 |
| 3 | 02:46:51 | task_rewrite | rewrote tasks/T-0064-measure-whether-the-young-vocabulary-s-artifacts.md (status: claimed) |
| 4 | 02:46:51 | task_rewrite | appended a claim record for T-0064 |
| 5 | 02:49:10 | artifact | wrote EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md |
| 6 | 02:50:56 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/coverage.py |
| 7 | 03:05:46 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/coverage.py --delay 8 |
| 8 | 03:09:08 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/copycount.py context:global file:^\.claude/hooks/ select:repo count:4000 context:global file |
| 9 | 03:10:11 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/copycount.py context:global file:^CLAUDE\.md$ select:repo count:20000 context:global file:^\ |
| 10 | 03:11:58 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/copycount.py context:global file:^\.claude/hooks/session-start\.sh$ select:repo count:4000 c |
| 11 | 03:13:57 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/copycount.py context:global file:^\.claude/hooks/session-start\.sh$ select:repo count:4000 c |
| 12 | 03:14:40 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/forkstatus.py |
| 13 | 03:15:48 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/forkstatus.py |
| 14 | 03:16:45 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/forkstatus.py |
| 15 | 03:23:23 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/forkstatus.py |
| 16 | 03:26:09 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/forkstatus.py |
| 17 | 03:27:37 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/forkstatus.py |
| 18 | 03:36:41 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/forkstatus.py |
| 19 | 03:41:30 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 20 | 03:42:06 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 21 | 03:42:36 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 22 | 03:44:05 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 23 | 03:45:19 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 24 | 03:59:58 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 25 | 04:17:13 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 26 | 04:19:52 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 27 | 04:29:08 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 28 | 04:46:59 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
