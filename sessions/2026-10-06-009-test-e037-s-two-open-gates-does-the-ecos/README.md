# Session 2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T09:58:26+00:00
- **Duration:** 4086.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test E037's two open gates - does the ecosystem already serve line-addressable git staging, and does a measurable population ask for it - with a search-based prior-art check and one documented public query

## Summary

E038 complete: prior-art search found filterdiff --lines=RANGE and VS Code git.stageSelectedRanges; stronger oracle found and fixed stg's over-staging bug (30/30 vs filterdiff 12/30, pty 12/30, naive 6/30); demand-side keyword classifier precision 0.033-0.067, 195 issues read

## Next

Reconcile record: split oversized harvest.py/stagelib.py, index F062-F064, then decide next step on KILL-Q

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/038-staging-prior-art/PROTOCOL.md | e99fb7bd346a | 6705 |
| EXPERIMENTS/038-staging-prior-art/harvest.py | d3084e455bb5 | 15651 |
| EXPERIMENTS/038-staging-prior-art/compare.py | 2c0440bbbb61 | 9250 |
| stage-lines/stagelib.py | e87b19aa5cd8 | 12071 |
| stage-lines/test_stage.py | 77575349ecc1 | 12312 |
| stage-lines/test_parser.py | e1aa960135f5 | 2595 |
| stage-lines/tests_support.py | 27dbbda30b6b | 3555 |
| EXPERIMENTS/037-line-staging/driver.py | 49ef684ca4e8 | 5482 |
| EXPERIMENTS/038-staging-prior-art/readout.py | faa73bbf9a1a | 5866 |
| EXPERIMENTS/038-staging-prior-art/precision.py | f4ea9b1dd7d6 | 4540 |
| EXPERIMENTS/038-staging-prior-art/score.py | 5cde1b8dc5ef | 7392 |
| EXPERIMENTS/038-staging-prior-art/README.md | eb0d5d26b849 | 12802 |

## Commands

26 captured, 8 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/038-staging-prior-art/harvest.py', '--probe'] | 0 | 5775 |
| 3 | ['python3', '-'] | 0 | 5359 |
| 4 | ['python3', 'EXPERIMENTS/038-staging-prior-art/harvest.py', '--probe'] | 0 | 9557 |
| 5 | ['python3', 'EXPERIMENTS/038-staging-prior-art/harvest.py', 'poola'] | 1 | 809 |
| 6 | ['python3', 'EXPERIMENTS/038-staging-prior-art/harvest.py', 'poola'] | 0 | 39708 |
| 7 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/038-staging-prior-art/compare.py'] | 0 | 54224 |
| 8 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/038-staging-prior-art/compare.py'] | 0 | 47409 |
| 9 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 1 | 7083 |
| 10 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 1 | 6682 |
| 11 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 1 | 8797 |
| 12 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 1 | 7706 |
| 13 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 1 | 7740 |
| 14 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 1 | 9391 |
| 15 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 1 | 7475 |
| 16 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 0 | 9431 |
| 17 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/038-staging-prior-art/compare.py'] | 0 | 41209 |
| 18 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 0 | 6797 |
| 19 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/038-staging-prior-art/compare.py'] | 0 | 38992 |
| 20 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 0 | 7434 |
| 21 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/038-staging-prior-art/compare.py'] | 0 | 39410 |
| 22 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/038-staging-prior-art/compare.py'] | 0 | 44110 |
| 32 | ['python3', 'EXPERIMENTS/038-staging-prior-art/harvest.py', '--budget'] | 0 | 1202 |
| 33 | ['python3', 'EXPERIMENTS/038-staging-prior-art/harvest.py', 'poolc'] | 0 | 18538 |
| 34 | ['python3', 'EXPERIMENTS/038-staging-prior-art/readout.py', 'issues'] | 0 | 2312 |
| 35 | ['python3', 'EXPERIMENTS/038-staging-prior-art/precision.py'] | 0 | 521 |
| 36 | ['python3', 'EXPERIMENTS/038-staging-prior-art/score.py', '--score'] | 0 | 500 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 20 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-9.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/038-staging-prior-art/harvest_core.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/harvest_pools.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/harvest_pools_tmp.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/pools.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/raw/compare.jsonl |
|   undeclared | EXPERIMENTS/038-staging-prior-art/raw/requests.jsonl |
|   undeclared | FAILURES-findings-25.md |
|   undeclared | FAILURES-findings-26.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:58:26 | session_start | Test E037's two open gates - does the ecosystem already serve line-addressable git staging, and does a measurable population ask for it - with a searc |
| 2 | 09:59:22 | command | $ python3 EXPERIMENTS/038-staging-prior-art/harvest.py --probe |
| 3 | 09:59:44 | command | $ python3 - |
| 4 | 10:00:26 | command | $ python3 EXPERIMENTS/038-staging-prior-art/harvest.py --probe |
| 5 | 10:00:28 | command | $ python3 EXPERIMENTS/038-staging-prior-art/harvest.py poola |
| 6 | 10:01:19 | command | $ python3 EXPERIMENTS/038-staging-prior-art/harvest.py poola |
| 7 | 10:06:57 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py |
| 8 | 10:08:36 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py |
| 9 | 10:11:13 | command | $ python3 -m unittest discover -s stage-lines |
| 10 | 10:11:25 | command | $ python3 -m unittest discover -s stage-lines |
| 11 | 10:12:08 | command | $ python3 -m unittest discover -s stage-lines |
| 12 | 10:12:22 | command | $ python3 -m unittest discover -s stage-lines |
| 13 | 10:12:35 | command | $ python3 -m unittest discover -s stage-lines |
| 14 | 10:12:48 | command | $ python3 -m unittest discover -s stage-lines |
| 15 | 10:13:59 | command | $ python3 -m unittest discover -s stage-lines |
| 16 | 10:14:25 | command | $ python3 -m unittest discover -s stage-lines |
| 17 | 10:15:30 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py |
| 18 | 10:16:37 | command | $ python3 -m unittest discover -s stage-lines |
| 19 | 10:17:16 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py |
| 20 | 10:17:52 | command | $ python3 -m unittest discover -s stage-lines |
| 21 | 10:18:32 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py |
| 22 | 10:19:51 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py |
| 23 | 10:19:57 | milestone | E038 head-to-head complete: stg 30/30, filterdiff 12/30, pty_driver 12/30, naive 6/30; two real parser bugs in stg found and fixed (adjacent insertion |
| 24 | 10:19:58 | artifact | wrote EXPERIMENTS/038-staging-prior-art/PROTOCOL.md |
| 25 | 10:19:58 | artifact | wrote EXPERIMENTS/038-staging-prior-art/harvest.py |
| 26 | 10:19:58 | artifact | wrote EXPERIMENTS/038-staging-prior-art/compare.py |
| 27 | 10:19:58 | artifact | wrote stage-lines/stagelib.py |
| 28 | 10:19:59 | artifact | wrote stage-lines/test_stage.py |
| 29 | 10:19:59 | artifact | wrote stage-lines/test_parser.py |
| 30 | 10:19:59 | artifact | wrote stage-lines/tests_support.py |
| 31 | 10:19:59 | artifact | wrote EXPERIMENTS/037-line-staging/driver.py |
| 32 | 10:20:07 | command | $ python3 EXPERIMENTS/038-staging-prior-art/harvest.py --budget |
| 33 | 10:20:25 | command | $ python3 EXPERIMENTS/038-staging-prior-art/harvest.py poolc |
| 34 | 10:20:45 | command | $ python3 EXPERIMENTS/038-staging-prior-art/readout.py issues |
| 35 | 10:21:00 | command | $ python3 EXPERIMENTS/038-staging-prior-art/precision.py |
| 36 | 10:21:37 | command | $ python3 EXPERIMENTS/038-staging-prior-art/score.py --score |
| 37 | 10:21:43 | milestone | E038 demand side: keyword classifier precision 0.067 (2 of 30 in-population rows are real), so readout.py's 100/195 was noise; hand labels find 3 yes- |
| 38 | 10:21:43 | artifact | wrote EXPERIMENTS/038-staging-prior-art/readout.py |
| 39 | 10:21:43 | artifact | wrote EXPERIMENTS/038-staging-prior-art/precision.py |
| 40 | 10:21:44 | artifact | wrote EXPERIMENTS/038-staging-prior-art/score.py |
| 57 | 11:06:31 | unlogged_change | changed but never declared as an artifact: stage-lines/stagelib_split.py |
| 58 | 11:06:31 | unlogged_change | changed but never declared as an artifact: tests/test_decision_files.py |
| 59 | 11:06:32 | unlogged_change | changed but never declared as an artifact: tools/originlib/paths.py |
| 60 | 11:06:32 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 61 | 11:06:32 | unlogged_change | changed but never declared as an artifact: vendor/MANIFEST.md |
| 62 | 11:06:32 | doc_update | updated DECISIONS-SCREENING-9.md |
| 63 | 11:06:32 | doc_update | updated DECISIONS.md |
| 64 | 11:06:32 | doc_update | updated FAILURES.md |
| 65 | 11:06:32 | doc_update | updated STATE.md |
| 66 | 11:06:32 | session_end | E038 complete: prior-art search found filterdiff --lines=RANGE and VS Code git.stageSelectedRanges; stronger oracle found and fixed stg's over-staging |

_16 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos/events.jsonl
```
