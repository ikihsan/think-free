# Session 2026-10-10-006-decide-by-measurement-whether-which-dist

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T02:50:22+00:00
- **Duration:** 13899.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Decide by measurement whether 'which distribution provides this module' is a real asked question, and if so test pyprovides head-to-head against the strongest alternative on real cases

## Summary

E090 (T-0089) ran to a recorded verdict: the module-to-distribution reverse index over the 15000 most-downloaded PyPI projects resolves 618 of 1970 real imported module names (0.3137) against a declared 0.70 kill gate, with a decelerating K-curve; pip install M plus the index together answer 0.3893. G0 discrimination passed first (19/21, 0/30, 9/10). G3 passed at 0.0589 but is an upper bound because the protocol named three baselines and ran one (D099). D098 retires the index at any K; F111 records the finding; DECISIONS-SCREENING-18.md and FAILURES-findings-37.md are written; pyprovides/README.md is corrected in place. analyze.py reproduces every gate figure offline. The second half of the session goal (the head-to-head on real failing imports) was not run: D099 promotes it to the next experiment, and T-0090 (E091, demand-side hand replication of E062 on Anova cooking Discourse) was created and claimed but not started.

## Next

1) E091 (T-0090, claimed here on this VM): hand-replicate E062's answerability sub-test on Anova cooking Discourse with pre-declared calibration gates, to test whether F096's 17-of-20 generalizes beyond Stack Exchange. 2) D099's head-to-head: real failing imports, three arms (pip install M, free general assistant, pyprovides forward mechanism) on the same cases, reusing E044's design. 3) Land this session's uncommitted artifacts in one commit.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/090-reverse-index/PROTOCOL.md | d8f221493918 | 8855 |
| EXPERIMENTS/090-reverse-index/harvest.py | d8fab7f023e0 | 8457 |
| EXPERIMENTS/090-reverse-index/build_index.py | 4b74a96eb916 | 6265 |
| EXPERIMENTS/090-reverse-index/VERDICT.md | 201ef6724edb | 8308 |
| DECISIONS-SCREENING-18.md | 08deda95f5a5 | 4719 |
| FAILURES-findings-37.md | 6435c725569e | 6181 |
| EXPERIMENTS/090-reverse-index/analyze.py | 1df973fd1beb | 9974 |
| EXPERIMENTS/090-reverse-index/leakage.py | ab2a8c83c97d | 8907 |
| EXPERIMENTS/090-reverse-index/transfer_cost.py | 43d47a1bbee8 | 5533 |
| EXPERIMENTS/090-reverse-index/report.py | 219708a8f5cc | 6359 |
| EXPERIMENTS/090-reverse-index/results.json | 097eeb33569a | 16684 |
| EXPERIMENTS/090-reverse-index/population.json | 4dc36125cf46 | 104554 |
| EXPERIMENTS/090-reverse-index/leakage.json | f2b6bc8e4abf | 221841 |
| EXPERIMENTS/090-reverse-index/leakage-v1-upper-bound.json | 3edcb8861f30 | 30593 |
| EXPERIMENTS/090-reverse-index/transfer-cost.json | 89a87a914ee3 | 13417 |
| EXPERIMENTS/090-reverse-index/g0-results.json | 4df7529ea6d8 | 6110 |
| EXPERIMENTS/090-reverse-index/raw-projects.jsonl | dea791860522 | 2808601 |
| EXPERIMENTS/090-reverse-index/top-pypi-packages.min.json | 55fee05ed02b | 787401 |

## Commands

13 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '-c', 'curl -s -o /dev/null -w "pypi:%{http_code} " https://pypi.org/simple/ ; curl -s -o /dev/null -w "github:%{http_code} " https://api.git | 0 | 14708 |
| 8 | ['python3', 'EXPERIMENTS/090-reverse-index/g0_discrimination.py'] | 1 | 3309 |
| 9 | ['python3', 'EXPERIMENTS/090-reverse-index/g0_discrimination.py'] | 0 | 11593 |
| 10 | ['python3', 'EXPERIMENTS/090-reverse-index/harvest.py'] | 1 | 726812 |
| 11 | ['python3', 'EXPERIMENTS/090-reverse-index/harvest.py'] | 1 | 685986 |
| 18 | ['python3', 'EXPERIMENTS/090-reverse-index/leakage.py'] | 0 | 492313 |
| 21 | ['python3', 'EXPERIMENTS/090-reverse-index/leakage.py'] | 0 | 436828 |
| 22 | ['python3', 'EXPERIMENTS/090-reverse-index/transfer_cost.py', '60'] | 0 | 63770 |
| 23 | ['python3', 'EXPERIMENTS/090-reverse-index/analyze.py'] | 0 | 136010 |
| 24 | ['python3', 'EXPERIMENTS/090-reverse-index/analyze.py'] | 0 | 2582 |
| 25 | ['python3', 'EXPERIMENTS/090-reverse-index/analyze.py'] | 1 | 5190 |
| 26 | ['python3', 'EXPERIMENTS/090-reverse-index/analyze.py'] | 1 | 2598 |
| 27 | ['python3', 'EXPERIMENTS/090-reverse-index/analyze.py'] | 0 | 2521 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 18 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/Pillow.json |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/PyMySQL.json |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/beautifulsoup4.json |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/matplotlib.json |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/numpy.json |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/pandas.json |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/pyzmq.json |
|   undeclared | EXPERIMENTS/090-reverse-index/cache-g0/requests.json |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:50:22 | session_start | Decide by measurement whether 'which distribution provides this module' is a real asked question, and if so test pyprovides head-to-head against the s |
| 2 | 02:51:26 | command | $ bash -c curl -s -o /dev/null -w "pypi:%{http_code} " https://pypi.org/simple/ ; curl -s -o /dev/null -w "github:%{http_code} " https://api.g |
| 3 | 02:58:00 | task_rewrite | appended a create record for T-0089 |
| 4 | 02:59:03 | task_rewrite | rewrote tasks/T-0089-e090-measure-whether-a-module-to-distribution-re.md (status: claimed) |
| 5 | 02:59:04 | task_rewrite | appended a claim record for T-0089 |
| 6 | 03:00:05 | artifact | wrote EXPERIMENTS/090-reverse-index/PROTOCOL.md |
| 7 | 03:00:08 | milestone | E090 protocol declared: G0 instrument discrimination first, G1 buildable, G2 coverage 0.70 kill gate, G3 value-over-pip 0.02 |
| 8 | 03:00:31 | command | $ python3 EXPERIMENTS/090-reverse-index/g0_discrimination.py |
| 9 | 03:00:53 | command | $ python3 EXPERIMENTS/090-reverse-index/g0_discrimination.py |
| 10 | 03:16:05 | command | $ python3 EXPERIMENTS/090-reverse-index/harvest.py |
| 11 | 03:23:29 | command | $ python3 EXPERIMENTS/090-reverse-index/harvest.py |
| 12 | 03:30:20 | task_rewrite | appended a create record for T-0090 |
| 13 | 04:14:42 | artifact | wrote EXPERIMENTS/090-reverse-index/harvest.py |
| 14 | 04:14:47 | artifact | wrote EXPERIMENTS/090-reverse-index/build_index.py |
| 15 | 04:14:49 | milestone | G0 PASS (18/20 positive, 0/30 negative, 10/10 forward). Fixed two bugs found in the interrupted run: harvest.py KeyError 'stratum' after a 12-min harv |
| 16 | 04:25:05 | milestone | E090 G0 confirmed PASS reading its own keys: positive 19/21 (threshold 18), negative 0/30 (threshold 0), forward 9/10 (threshold 8). Traced the forwar |
| 17 | 04:35:33 | milestone | resumed interrupted E090: index build 11942/15000 restarted in background; population contamination check declared (85.3% of the 1970 harvested names  |
| 18 | 04:44:24 | command | $ python3 EXPERIMENTS/090-reverse-index/leakage.py |
| 19 | 04:46:11 | milestone | leakage pass 1 measured 0.5635 of the population as repo-internal but conflated nested files with root-level providers, so it was an upper bound only; |
| 20 | 04:47:25 | milestone | E090 index build complete: 15000/15000 ranked projects read, 14387 distinct top-level modules indexed, 4962-project resume fetched 1302 MB in 1855 s |
| 21 | 04:53:03 | command | $ python3 EXPERIMENTS/090-reverse-index/leakage.py |
| 22 | 04:53:19 | command | $ python3 EXPERIMENTS/090-reverse-index/transfer_cost.py 60 |
| 23 | 04:55:50 | command | $ python3 EXPERIMENTS/090-reverse-index/analyze.py |
| 24 | 04:57:03 | command | $ python3 EXPERIMENTS/090-reverse-index/analyze.py |
| 25 | 05:04:14 | command | $ python3 EXPERIMENTS/090-reverse-index/analyze.py |
| 26 | 05:04:27 | command | $ python3 EXPERIMENTS/090-reverse-index/analyze.py |
| 27 | 05:04:38 | command | $ python3 EXPERIMENTS/090-reverse-index/analyze.py |
| 28 | 06:39:18 | milestone | E090 leakage control re-run complete: strict 13 of 1970 population rows (0.0066) are repo-internal providers; 1097 of 1110 broad hits classified neste |
| 29 | 06:39:19 | milestone | E090 transfer cost measured on 60 projects drawn at random with a fixed seed: mean 351 KB and 2 HTTP requests per project; scaled to 15000 projects =  |
| 30 | 06:39:20 | milestone | E090 gates read from results.json: G2 FAIL at 0.3137 (618 of 1970 against the declared 0.70 kill gate); K-curve 0.100/0.140/0.200/0.255/0.295/0.314, d |
| 31 | 06:39:50 | artifact | E090 verdict: G2 FAIL, G3 PASS, direction retired, head-to-head promoted |
| 32 | 06:39:51 | artifact | D098 (retire the reverse index) and D099 (baseline must be the strongest named alternative) written; F111 recorded |
| 33 | 06:39:51 | artifact | D098 (retire the reverse index) and D099 (baseline must be the strongest named alternative) written; F111 recorded |
| 34 | 06:39:53 | artifact | E090 pipeline: every gate figure recomputes offline from these files |
| 35 | 06:39:53 | artifact | E090 pipeline: every gate figure recomputes offline from these files |
| 36 | 06:39:54 | artifact | E090 pipeline: every gate figure recomputes offline from these files |
| 37 | 06:39:55 | artifact | E090 pipeline: every gate figure recomputes offline from these files |
| 38 | 06:39:56 | artifact | E090 pipeline: every gate figure recomputes offline from these files |
| 39 | 06:39:56 | artifact | E090 pipeline: every gate figure recomputes offline from these files |
| 40 | 06:39:57 | artifact | E090 pipeline: every gate figure recomputes offline from these files |
| 62 | 06:42:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-reverse-index/index/index.json |
| 63 | 06:42:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-reverse-index/raw-projects.jsonl.lock |
| 64 | 06:42:00 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 65 | 06:42:00 | unlogged_change | changed but never declared as an artifact: pyprovides/README.md |
| 66 | 06:42:00 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 67 | 06:42:00 | unlogged_change | changed but never declared as an artifact: tasks/T-0090-e091-hand-replicate-e062-s-answerability-sub-tes.md |
| 68 | 06:42:00 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 69 | 06:42:00 | doc_update | updated DECISIONS.md |
| 70 | 06:42:00 | doc_update | updated FAILURES.md |
| 71 | 06:42:00 | session_end | E090 (T-0089) ran to a recorded verdict: the module-to-distribution reverse index over the 15000 most-downloaded PyPI projects resolves 618 of 1970 re |

_21 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-006-decide-by-measurement-whether-which-dist/events.jsonl
```
