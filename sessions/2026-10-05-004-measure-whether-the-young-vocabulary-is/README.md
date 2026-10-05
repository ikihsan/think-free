# Session 2026-10-05-004-measure-whether-the-young-vocabulary-is

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T02:44:46+00:00
- **Duration:** 17168.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure whether the young vocabulary is served by copied directories rather than installations, using a code-search instrument the record says does not exist

## Summary

E021 measured the serving channel the prior-art screen was alleged to be blind to and found it 0.118x the channel it already read (1,026 indexed repos holding a .claude/hooks/ directory against 8,676 monthly installs), so F037's 'used and invisible' reading is withdrawn and the twelve prior-art deaths stand (F041, D053). C2 did not refuse the experiment -- young arm 17/18 in the index -- but read 0 of 13 placebos, so the instrument is blind where this mission's candidates live. H2 not_evaluated after this session's own retry loop destroyed five captures. The other VM took F040/D052 for a different experiment on the same reading and published first; renumbered on the unpushed side per the multi-VM rule, and recovered this session's work after an interrupted sync land.

## Next

Rerun H2's low band from a host Sourcegraph will answer -- the slice is declared mechanically, so it needs no new decisions.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md | 1743f981724a | 9526 |
| EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md | 1743f981724a | 9526 |
| EXPERIMENTS/020-copied-artifact-serving/results.json | 294377447b78 | 10234 |
| EXPERIMENTS/020-copied-artifact-serving/coverage.json | 45d005318e39 | 10683 |
| EXPERIMENTS/020-copied-artifact-serving/copycount.json | 829a3e01a14e | 46013 |
| EXPERIMENTS/020-copied-artifact-serving/forkstatus.json | bea94793549d | 4763 |
| STATE-in-flight.md | 7e5841c44d3d | 9820 |
| STATE.md | af93f0ba6b30 | 28852 |
| ROADMAP.md | e3c4745526a7 | 19957 |
| RELEASE-MANIFEST.md | 6e3739ed5e3f | 4969 |
| docs/INDEX.md | 36876264dddc | 25012 |
| docs/process/experiment-protocol.md | aeced4ec42c4 | 8340 |
| DECISIONS-SCREENING-3.md | 302e0fdb0331 | 4756 |
| FAILURES-findings-16.md | 524194667ba1 | 7239 |
| STATE.md | 2bf014364321 | 30088 |
| STATE-in-flight.md | 4bb43ca92156 | 11824 |
| FAILURES.md | 823dc8ccde07 | 9019 |
| DECISIONS.md | 1be2f857b329 | 7760 |

## Commands

33 captured, 6 non-zero exit.

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
| 29 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 57152 |
| 30 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 1 | 17290 |
| 31 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 1 | 680 |
| 32 | ['python3', 'EXPERIMENTS/020-copied-artifact-serving/tally.py'] | 0 | 62625 |
| 33 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 503220 |
| 34 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 500660 |
| 35 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 494721 |
| 43 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 529918 |
| 46 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 528239 |
| 55 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 521996 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 53 |
| declared artifacts now missing | 0 |
| integrity errors | 6 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-2.md |
|   undeclared | EXPERIMENTS/020-copied-config-drift/README.md |
|   undeclared | EXPERIMENTS/020-copied-config-drift/a5_structural.py |
|   undeclared | EXPERIMENTS/020-copied-config-drift/analyse.py |
|   undeclared | EXPERIMENTS/020-copied-config-drift/bodies.py |
|   undeclared | EXPERIMENTS/020-copied-config-drift/control.py |
|   undeclared | EXPERIMENTS/020-copied-config-drift/population.py |
|   undeclared | EXPERIMENTS/020-copied-config-drift/raw/bodies.json |
|   undeclared | EXPERIMENTS/020-copied-config-drift/raw/captured_bodies.json |
|   undeclared | EXPERIMENTS/020-copied-config-drift/raw/control.json |
|   error | declared artifact no longer exists: EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md |
|   error | declared artifact no longer exists: EXPERIMENTS/020-copied-artifact-serving/copycount.json |
|   error | declared artifact no longer exists: EXPERIMENTS/020-copied-artifact-serving/coverage.json |
|   error | declared artifact no longer exists: EXPERIMENTS/020-copied-artifact-serving/forkstatus.json |
|   error | declared artifact no longer exists: EXPERIMENTS/020-copied-artifact-serving/results.json |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

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
| 29 | 04:58:02 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 30 | 04:59:10 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 31 | 04:59:27 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 32 | 05:00:57 | command | $ python3 EXPERIMENTS/020-copied-artifact-serving/tally.py |
| 33 | 05:19:19 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 34 | 05:27:53 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 35 | 05:37:47 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 36 | 05:41:26 | artifact | wrote EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md |
| 37 | 05:41:27 | artifact | wrote EXPERIMENTS/020-copied-artifact-serving/results.json |
| 38 | 05:41:28 | artifact | wrote EXPERIMENTS/020-copied-artifact-serving/coverage.json |
| 39 | 05:41:30 | artifact | wrote EXPERIMENTS/020-copied-artifact-serving/copycount.json |
| 40 | 05:41:30 | artifact | wrote EXPERIMENTS/020-copied-artifact-serving/forkstatus.json |
| 117 | 07:30:55 | integrity_error | declared artifact no longer exists: EXPERIMENTS/020-copied-artifact-serving/forkstatus.json |
| 118 | 07:30:55 | integrity_error | declared artifact no longer exists: EXPERIMENTS/020-copied-artifact-serving/results.json |
| 119 | 07:30:55 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 120 | 07:30:55 | doc_update | updated DECISIONS-SCREENING-2.md |
| 121 | 07:30:55 | doc_update | updated DECISIONS-SCREENING-3.md |
| 122 | 07:30:55 | doc_update | updated DECISIONS.md |
| 123 | 07:30:55 | doc_update | updated FAILURES.md |
| 124 | 07:30:55 | doc_update | updated ROADMAP.md |
| 125 | 07:30:55 | doc_update | updated STATE.md |
| 126 | 07:30:55 | session_end | E021 measured the serving channel the prior-art screen was alleged to be blind to and found it 0.118x the channel it already read (1,026 indexed repos |

_76 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-004-measure-whether-the-young-vocabulary-is/events.jsonl
```
