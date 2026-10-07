# Session 2026-10-07-003-e047-test-with-a-byte-level-oracle-wheth

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-07T07:17:04+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E047: test with a byte-level oracle whether any shipped git hook runner folds a partially-staged file's unstaged hunk into the commit, and decide whether the hook hazard is a candidate

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/047-hook-partial-stage/README.md | d6acdeacfc6a | 11466 |
| EXPERIMENTS/047-hook-partial-stage/raw/results.json | ad7aaf117e37 | 23840 |
| EXPERIMENTS/047-hook-partial-stage/harness.py | f87bb504de81 | 11709 |
| EXPERIMENTS/047-hook-partial-stage/fixture.py | 799e404f6b5d | 4757 |
| EXPERIMENTS/047-hook-partial-stage/arms.py | 45333db7908b | 9137 |
| EXPERIMENTS/047-hook-partial-stage/gitenv.py | 7254b25ccaf0 | 2825 |
| EXPERIMENTS/047-hook-partial-stage/versions.py | 81e7ecd7205f | 2940 |
| EXPERIMENTS/047-hook-partial-stage/setup.sh | 18f70ff35120 | 8050 |
| DECISIONS-SCREENING-13.md | 42576720b705 | 4628 |
| FAILURES-findings-31.md | 009191cb118a | 4570 |
| STATE.md | b0f7288e29a2 | 37407 |
| STATE-history.md | 76d0442405b5 | 12560 |
| STATE-next-actions.md | c101fa197f44 | 19099 |
| FAILURES.md | 25ddf348e372 | 46027 |
| DECISIONS.md | 5841207d06ec | 13138 |

## Commands

25 captured, 11 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '-c', 'echo "node: $(command -v node && node --version)"; echo "npm: $(command -v npm && npm --version)"; echo "go: $(command -v go && go ver | 0 | 3489 |
| 3 | ['bash', '-c', 'curl -s -o /dev/null -w "nodejs.org %{http_code}\\n" https://nodejs.org/dist/latest-v20.x/ ; curl -s https://nodejs.org/dist/index.jso | 0 | 297 |
| 4 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 3 | 27522 |
| 5 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 127 | 29317 |
| 7 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 1 | 26682 |
| 8 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 0 | 203146 |
| 9 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 0 | 29890 |
| 10 | ['timeout', '1200', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 1 | 1920 |
| 11 | ['timeout', '1500', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 0 | 3610 |
| 12 | ['timeout', '1500', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 0 | 5613 |
| 13 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 1 | 41586 |
| 15 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 2 | 404390 |
| 17 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 2 | 398791 |
| 18 | ['sh', 'EXPERIMENTS/047-hook-partial-stage/setup.sh'] | 0 | 432934 |
| 19 | ['timeout', '1500', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 0 | 11421 |
| 20 | ['timeout', '1500', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 0 | 22471 |
| 21 | ['timeout', '1500', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 0 | 23746 |
| 22 | ['timeout', '1500', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 0 | 22787 |
| 23 | ['timeout', '1500', 'python3', 'EXPERIMENTS/047-hook-partial-stage/harness.py'] | 0 | 23419 |
| 40 | ['tools/origin', 'doc', 'lint'] | 2 | 97507 |
| 41 | ['tools/origin', 'doc', 'lint'] | 0 | 55875 |
| 42 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 689403 |
| 43 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_decision_files', 'tests.test_decision_row_pattern', 'tests.test_decision_in | 1 | 306 |
| 44 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 674622 |
| 45 | ['tools/origin', 'sync', 'land'] | 1 | 2498 |

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
| 1 | 07:17:04 | session_start | E047: test with a byte-level oracle whether any shipped git hook runner folds a partially-staged file's unstaged hunk into the commit, and decide whet |
| 2 | 07:17:13 | command | $ bash -c echo "node: $(command -v node && node --version)"; echo "npm: $(command -v npm && npm --version)"; echo "go: $(command -v go && go v |
| 3 | 07:17:22 | command | $ bash -c curl -s -o /dev/null -w "nodejs.org %{http_code}\n" https://nodejs.org/dist/latest-v20.x/ ; curl -s https://nodejs.org/dist/index.js |
| 4 | 07:18:21 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 5 | 07:19:28 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 6 | 07:20:27 | milestone | Declared the experiment before measuring. Question: for a file with one staged hunk and one unstaged hunk, does any shipped hook runner's formatter ca |
| 7 | 07:20:45 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 8 | 07:29:31 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 9 | 07:31:12 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 10 | 07:31:18 | command | $ timeout 1200 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 11 | 07:32:02 | command | $ timeout 1500 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 12 | 07:32:40 | command | $ timeout 1500 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 13 | 07:34:09 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 14 | 07:48:03 | milestone | E047 first run: both controls behave as required -- C0 (naive hand-written hook) SWEEPS byte-exactly, so the harness can detect the hazard, and B0 (no |
| 15 | 07:50:30 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 16 | 07:55:06 | task_rewrite | appended a create record for T-0084 |
| 17 | 08:00:21 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 18 | 08:09:09 | command | $ sh EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 19 | 08:10:40 | command | $ timeout 1500 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 20 | 08:12:45 | command | $ timeout 1500 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 21 | 08:13:27 | command | $ timeout 1500 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 22 | 08:14:27 | command | $ timeout 1500 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 23 | 08:20:17 | command | $ timeout 1500 python3 EXPERIMENTS/047-hook-partial-stage/harness.py |
| 24 | 08:21:01 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/README.md |
| 25 | 08:21:02 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/raw/results.json |
| 26 | 08:21:03 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/harness.py |
| 27 | 08:21:03 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/fixture.py |
| 28 | 08:21:04 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/arms.py |
| 29 | 08:21:05 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/gitenv.py |
| 30 | 08:21:05 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/versions.py |
| 31 | 08:21:06 | artifact | wrote EXPERIMENTS/047-hook-partial-stage/setup.sh |
| 32 | 08:21:07 | artifact | wrote DECISIONS-SCREENING-13.md |
| 33 | 08:21:07 | artifact | wrote FAILURES-findings-31.md |
| 34 | 08:21:08 | artifact | wrote STATE.md |
| 35 | 08:21:09 | artifact | wrote STATE-history.md |
| 36 | 08:21:10 | artifact | wrote STATE-next-actions.md |
| 37 | 08:21:12 | artifact | wrote FAILURES.md |
| 38 | 08:21:13 | artifact | wrote DECISIONS.md |
| 39 | 08:21:23 | milestone | E047 measured, recorded and closed. Nine arms on real runners at current versions, both controls correct: the hazard is real and byte-exact (the naive |
| 40 | 08:32:35 | command | $ tools/origin doc lint |
| 41 | 08:39:28 | command | $ tools/origin doc lint |
| 42 | 08:55:10 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 43 | 08:59:58 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_decision_files tests.test_decision_row_pattern tests.test_decision_index |
| 44 | 09:11:39 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 45 | 09:19:30 | command | $ tools/origin sync land |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-07-003-e047-test-with-a-byte-level-oracle-wheth/events.jsonl
```
