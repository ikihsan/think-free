# Session 2026-10-08-003-fresh-observation-to-find-a-testable-pra

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T00:58:13+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation to find a testable practical difficulty: name the population, evidence and strongest incumbent before any build

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/055-index-postcondition/PROTOCOL.md | 567b493984ce | 6900 |
| EXPERIMENTS/055-index-postcondition/indexcheck.py | f710f74229bf | 6515 |
| EXPERIMENTS/055-index-postcondition/gitenv.py | bf8d1386f553 | 3265 |
| EXPERIMENTS/055-index-postcondition/arms.py | 332a44599c0f | 6558 |
| EXPERIMENTS/055-index-postcondition/run.py | 536b018e1696 | 14089 |
| EXPERIMENTS/055-index-postcondition/test_gates_falsified.py | b7fd08ca3df9 | 8287 |
| EXPERIMENTS/055-index-postcondition/provenance.py | e90d269660a0 | 4118 |
| EXPERIMENTS/055-index-postcondition/raw/ceiling-run1.json | 8b58884a441d | 7921 |
| EXPERIMENTS/055-index-postcondition/PROTOCOL.md | e333e7f45916 | 16486 |
| EXPERIMENTS/055-index-postcondition/PROTOCOL-AMENDMENT-1.md | edf830ec539f | 3810 |
| EXPERIMENTS/055-index-postcondition/PROTOCOL-AMENDMENT-2.md | ca822e870f93 | 2954 |
| EXPERIMENTS/055-index-postcondition/PROTOCOL-AMENDMENT-3.md | aa019548ed53 | 3690 |
| EXPERIMENTS/055-index-postcondition/README.md | d76d046ff2c5 | 10408 |
| EXPERIMENTS/055-index-postcondition/run.py | 4fc504defa2f | 13132 |
| EXPERIMENTS/055-index-postcondition/ceiling.py | 3b0d8d3761b0 | 11380 |
| EXPERIMENTS/055-index-postcondition/controls.py | 77845b1a8eee | 8657 |
| EXPERIMENTS/055-index-postcondition/probecontrols.py | a1d71a2c8a81 | 8186 |
| EXPERIMENTS/055-index-postcondition/patchwalk.py | 0f42691cac03 | 5066 |
| EXPERIMENTS/055-index-postcondition/k3probe.py | 97813656aaf0 | 4826 |
| EXPERIMENTS/055-index-postcondition/arms.py | e24621af302a | 6952 |
| EXPERIMENTS/055-index-postcondition/gitenv.py | bf8d1386f553 | 3265 |
| EXPERIMENTS/055-index-postcondition/indexcheck.py | f710f74229bf | 6515 |
| EXPERIMENTS/055-index-postcondition/provenance.py | e90d269660a0 | 4118 |
| EXPERIMENTS/055-index-postcondition/testharness.py | 5c65e981c52a | 1770 |
| EXPERIMENTS/055-index-postcondition/test_gates_falsified.py | d91eeebc58d4 | 7676 |
| EXPERIMENTS/055-index-postcondition/test_probe_controls_falsified.py | 71f6fe2fe272 | 8923 |
| EXPERIMENTS/055-index-postcondition/test_probe_order_falsified.py | a9192c89019d | 5719 |
| EXPERIMENTS/055-index-postcondition/test_probe_readers_falsified.py | a38ad2329eb5 | 8675 |
| EXPERIMENTS/055-index-postcondition/test_verdict_falsified.py | 8399297e692e | 9856 |
| EXPERIMENTS/055-index-postcondition/raw/results.json | b83fe26dda05 | 130787 |
| EXPERIMENTS/055-index-postcondition/raw/results-run1.json | d73dc0b27d3a | 84973 |
| EXPERIMENTS/055-index-postcondition/raw/results-run2.json | a2ebe4f3e567 | 123659 |
| EXPERIMENTS/055-index-postcondition/raw/results-run3.json | 82d4f8842eee | 127763 |
| EXPERIMENTS/055-index-postcondition/raw/ceiling.json | d55fd577a93f | 13669 |
| EXPERIMENTS/055-index-postcondition/raw/ceiling-run1.json | 8b58884a441d | 7921 |
| EXPERIMENTS/055-index-postcondition/PROTOCOL.md | 67824912b333 | 8697 |
| STATE-in-flight-8.md | 482770ee257e | 7074 |
| FAILURES-findings-31.md | 2cf5b1c44a81 | 15466 |
| DECISIONS-SCREENING-13.md | ffc01f89cab0 | 10909 |
| STATE.md | 2886f70d739e | 37318 |
| DECISIONS.md | 1e8302c81255 | 13647 |
| FAILURES.md | 91da9e40197e | 52017 |
| RELEASE-MANIFEST.md | 463a9af15319 | 6263 |
| docs/INDEX.md | 0a9a76bb173f | 33151 |

## Commands

29 captured, 9 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 13 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 105027 |
| 14 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 103622 |
| 15 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 104686 |
| 16 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', 'EXPERIMENTS/ | 0 | 18603 |
| 17 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', '-m', 'unitte | 0 | 25213 |
| 18 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', 'EXPERIMENTS/ | 0 | 108111 |
| 19 | ['bash', '/tmp/opencode/e055_manual.sh'] | 0 | 291 |
| 20 | ['bash', '/tmp/opencode/e055_manual2.sh'] | 0 | 123 |
| 21 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 4897 |
| 22 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 2921 |
| 23 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', 'EXPERIMENTS/ | 0 | 18601 |
| 26 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', 'EXPERIMENTS/ | 0 | 3131 |
| 28 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 18816 |
| 29 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 108589 |
| 30 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 17584 |
| 31 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 26004 |
| 33 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 1 | 720 |
| 34 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 0 | 2714 |
| 36 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 1 | 23067 |
| 37 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 1 | 26504 |
| 38 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 1 | 25498 |
| 39 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 1 | 1805 |
| 40 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/game | 1 | 25707 |
| 41 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', '-m', 'unitte | 1 | 25222 |
| 42 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', '-m', 'unitte | 1 | 26627 |
| 43 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', 'EXPERIMENTS/ | 0 | 113598 |
| 44 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', '-m', 'unitte | 0 | 28914 |
| 45 | ['env', 'PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'python3', 'EXPERIMENTS/ | 0 | 16575 |
| 46 | ['tools/origin', 'doc', 'lint'] | 2 | 76715 |

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
| 1 | 00:58:13 | session_start | Fresh observation to find a testable practical difficulty: name the population, evidence and strongest incumbent before any build |
| 2 | 01:20:02 | task_rewrite | appended a create record for T-0087 |
| 3 | 01:21:54 | task_rewrite | rewrote tasks/T-0087-e055-build-a-tool-neutral-git-index-postconditio.md (status: claimed) |
| 4 | 01:21:55 | task_rewrite | appended a claim record for T-0087 |
| 5 | 01:39:41 | artifact | wrote EXPERIMENTS/055-index-postcondition/PROTOCOL.md |
| 6 | 01:39:45 | artifact | wrote EXPERIMENTS/055-index-postcondition/indexcheck.py |
| 7 | 01:39:49 | artifact | wrote EXPERIMENTS/055-index-postcondition/gitenv.py |
| 8 | 01:39:51 | artifact | wrote EXPERIMENTS/055-index-postcondition/arms.py |
| 9 | 01:39:54 | artifact | wrote EXPERIMENTS/055-index-postcondition/run.py |
| 10 | 01:39:57 | artifact | wrote EXPERIMENTS/055-index-postcondition/test_gates_falsified.py |
| 11 | 01:40:27 | milestone | E055 declared (PROTOCOL.md, KILL-C), indexcheck built, C1/C2/C4 controls fire, 16 gate-falsification tests green; git 2.56.0 still building so arms no |
| 12 | 01:53:10 | milestone | resumed session on instance-20260717-0947: read PROTOCOL, indexcheck, arms, run.py and E038 oracle; git 2.56.0 is built at /tmp/opencode/gitenv; run 1 |
| 13 | 02:02:51 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 14 | 02:08:43 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 15 | 02:17:38 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 16 | 02:21:31 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin python3 EXPERIMENTS/0 |
| 17 | 02:22:13 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin python3 -m unittest d |
| 18 | 02:24:14 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin python3 EXPERIMENTS/0 |
| 19 | 02:29:46 | command | $ bash /tmp/opencode/e055_manual.sh |
| 20 | 02:29:57 | command | $ bash /tmp/opencode/e055_manual2.sh |
| 21 | 02:34:43 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 22 | 02:35:49 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 23 | 02:39:33 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin python3 EXPERIMENTS/0 |
| 24 | 02:48:12 | artifact | wrote EXPERIMENTS/055-index-postcondition/provenance.py |
| 25 | 02:48:13 | artifact | wrote EXPERIMENTS/055-index-postcondition/raw/ceiling-run1.json |
| 26 | 02:48:17 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin python3 EXPERIMENTS/0 |
| 27 | 02:53:41 | milestone | resumed session 2026-10-08-003 on instance-20260717-0947: E055 runs 1-4 and the ceiling probe exist; PROTOCOL.md amended twice, results.json and ceili |
| 28 | 02:54:06 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 29 | 02:57:51 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 30 | 02:58:15 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 31 | 02:58:49 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 32 | 03:05:28 | milestone | E055 re-run on current bytes reproduces the tallies exactly and run.py --verify now reports 'written by the current bytes'; 43 gate-falsification test |
| 33 | 03:07:09 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 34 | 03:08:26 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 35 | 03:08:45 | milestone | Amendment 3 declared and run: patchwalk.py reads the arm's primary output; ceiling.py rewritten with C11 (walk == git, 16/16 agree) and C12 (exact sel |
| 36 | 03:10:24 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 37 | 03:11:12 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 38 | 03:12:19 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 39 | 03:14:34 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 40 | 03:24:09 | command | $ env PATH=/tmp/opencode/gitenv/bin:/tmp/opencode/py312/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local |
| 75 | 04:04:05 | artifact | wrote EXPERIMENTS/055-index-postcondition/PROTOCOL.md |
| 76 | 04:04:08 | milestone | E055 closed: KILL-C do_not_build with all 12 controls fired and no not_evaluated; PROTOCOL.md split at the cap (amendments to siblings), doc index reg |
| 77 | 04:19:02 | artifact | wrote STATE-in-flight-8.md |
| 78 | 04:19:03 | artifact | wrote FAILURES-findings-31.md |
| 79 | 04:19:04 | artifact | wrote DECISIONS-SCREENING-13.md |
| 80 | 04:19:05 | artifact | wrote STATE.md |
| 81 | 04:19:06 | artifact | wrote DECISIONS.md |
| 82 | 04:19:07 | artifact | wrote FAILURES.md |
| 83 | 04:19:10 | artifact | wrote RELEASE-MANIFEST.md |
| 84 | 04:19:11 | artifact | wrote docs/INDEX.md |

_34 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-003-fresh-observation-to-find-a-testable-pra/events.jsonl
```
