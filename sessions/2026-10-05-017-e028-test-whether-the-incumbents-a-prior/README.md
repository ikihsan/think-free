# Session 2026-10-05-017-e028-test-whether-the-incumbents-a-prior

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T18:34:19+00:00
- **Duration:** 5290.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E028: test whether the incumbents a prior-art screen named do what each killed candidate's distinguishing requirement asks, using primary artifact documentation and a calibrated lexical index

## Summary

E028 tested whether a prior-art screen's evidence is evidence of fit, on the 19 harvest-side prior-art deaths with two blind readers over each named incumbent's own documentation. Result is not_evaluated under the declared gate: the positive control H03 failed, both readers reading sharp (436,835,441 downloads/month, called served beyond argument by E016) as partial because no document states the clause's latency attribute. Use is not fit (F048, D060). Nothing reopened. Three defects found in the run's own instrument and repaired under tests.

## Next

Item 0 stays an owner decision and is now better bounded: F048 says the prior-art axis's own verdicts have not been shown to rest on evidence of fit, so a future screen must test fit rather than existence or use. E028's arm 2 - the ten sealed-report prior-art deaths, the ones that closed this mission's own candidates - is declared and unrun, and it is the next measurement if that question is worth a second arm.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md | 294d63d64bfb | 2775 |
| EXPERIMENTS/028-incumbent-fit/PROTOCOL.md | adc80fd2bf95 | 11224 |
| EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-1.md | 7fe9b6dcb4f2 | 4657 |
| EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-2.md | 3890bc97e52c | 3848 |
| EXPERIMENTS/028-incumbent-fit/RUBRIC.md | 4bcf8e904015 | 4683 |
| EXPERIMENTS/028-incumbent-fit/build_population.py | 48e991d19757 | 3794 |
| EXPERIMENTS/028-incumbent-fit/fetch_docs.py | 603e35fb4200 | 9165 |
| EXPERIMENTS/028-incumbent-fit/README.md | ba5b7083a5ab | 8984 |
| EXPERIMENTS/028-incumbent-fit/results.json | 55a2eb7582e2 | 42585 |
| EXPERIMENTS/028-incumbent-fit/test_gates_falsified.py | 0c23c8ab9fe2 | 15583 |
| EXPERIMENTS/028-incumbent-fit/stats.py | da159a45bea0 | 16455 |
| EXPERIMENTS/028-incumbent-fit/make_step_b_view.py | d79194e4d74e | 5176 |
| EXPERIMENTS/028-incumbent-fit/split_batches.py | 9439595e58be | 1679 |
| STATE.md | 00976b04d448 | 32749 |
| STATE-next-actions.md | 769bd54353ff | 20751 |
| STATE-constraints.md | d38c8711a6cc | 10902 |
| ROADMAP.md | e12f28f257f2 | 20703 |
| FAILURES.md | 5f92ceb6e030 | 17216 |
| FAILURES-findings-20.md | 436c5aefaed6 | 6491 |
| DECISIONS.md | fe8f31c88ac2 | 8502 |
| DECISIONS-SCREENING-4.md | 374943f564de | 6119 |
| RELEASE-MANIFEST.md | f1877453868b | 5127 |
| ROADMAP.md | 8687b64fe4fb | 20038 |
| tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md | 5564a08143b6 | 2772 |

## Commands

38 captured, 8 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['tools/origin', 'session', 'start', '--goal', "E028: test whether the incumbents a prior-art screen named do what each killed candidate's distinguish | 0 | 1902 |
| 4 | ['tools/origin', 'task', 'new', '--goal', "Test whether the incumbents a prior-art screen named actually do what each killed candidate's distinguishin | 0 | 1602 |
| 5 | ['tools/origin', 'task', 'claim', '--task', 'T-0072', '--agent', 'opencode'] | 2 | 387 |
| 6 | ['tools/origin', 'task', 'claim', '--help'] | 0 | 326 |
| 7 | ['tools/origin', 'task', 'claim', 'T-0072', '--agent', 'opencode'] | 1 | 499 |
| 8 | ['git', 'add', '-A'] | 0 | 32 |
| 11 | ['tools/origin', 'task', 'claim', 'T-0072', '--agent', 'opencode'] | 0 | 6671 |
| 13 | ['tools/origin', 'session', 'artifact', 'tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md'] | 0 | 599 |
| 15 | ['tools/origin', 'session', 'step', 'E028 protocol declared before any label or documentation fetch: population 29 prior-art deaths read-only from two | 0 | 605 |
| 17 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/028-incumbent-fit/PROTOCOL.md'] | 0 | 604 |
| 18 | ['python3', 'EXPERIMENTS/028-incumbent-fit/build_population.py'] | 0 | 102 |
| 19 | ['python3', 'EXPERIMENTS/028-incumbent-fit/fetch_docs.py'] | 1 | 47942 |
| 20 | ['python3', 'EXPERIMENTS/028-incumbent-fit/fetch_docs.py'] | 0 | 24159 |
| 21 | ['python3', 'EXPERIMENTS/028-incumbent-fit/fetch_docs.py'] | 0 | 46850 |
| 27 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-1.md', 'EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-2.m | 0 | 1686 |
| 28 | ['python3', 'EXPERIMENTS/028-incumbent-fit/make_step_b_view.py', '--reader', 'r1'] | 0 | 132 |
| 29 | ['python3', 'EXPERIMENTS/028-incumbent-fit/make_step_b_view.py', '--reader', 'r2'] | 0 | 121 |
| 30 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 1 | 685 |
| 31 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 1 | 608 |
| 32 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 0 | 194 |
| 33 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 0 | 199 |
| 34 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 0 | 214 |
| 41 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/028-incumbent-fit/README.md', 'EXPERIMENTS/028-incumbent-fit/results.json', 'EXPERIMENTS/028-incu | 0 | 1905 |
| 42 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 0 | 198 |
| 43 | ['tools/origin', 'doc', 'lint'] | 2 | 11920 |
| 44 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 0 | 277 |
| 45 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 0 | 121 |
| 46 | ['python3', 'EXPERIMENTS/028-incumbent-fit/stats.py'] | 0 | 200 |
| 47 | ['tools/origin', 'doc', 'lint'] | 0 | 14588 |
| 48 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 476693 |
| 49 | ['tools/origin', 'preflight'] | 0 | 94498 |
| 50 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 477435 |
| 52 | ['tools/origin', 'session', 'step', 'E028 complete: not_evaluated on the declared control, F048 and D060 recorded, DECISIONS-SCREENING-4 split for D05 | 0 | 1026 |
| 53 | ['tools/origin', 'task', 'complete', 'T-0072', '--evidence', 'EXPERIMENTS/028-incumbent-fit/README.md', '--evidence', 'EXPERIMENTS/028-incumbent-fit/r | 2 | 418 |
| 56 | ['tools/origin', 'task', 'complete', 'T-0072', '--summary', "The prior-art screen had been checked for existence and never for fit. Tested on the 19 h | 0 | 1204 |
| 66 | ['tools/origin', 'session', 'artifact', 'STATE.md', 'STATE-next-actions.md', 'STATE-constraints.md', 'ROADMAP.md', 'FAILURES.md', 'FAILURES-findings-2 | 0 | 2659 |
| 67 | ['tools/origin', 'preflight'] | 0 | 95373 |
| 70 | ['tools/origin', 'session', 'artifact', 'ROADMAP.md', 'tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md'] | 0 | 924 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 24 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-3.md |
|   undeclared | EXPERIMENTS/028-incumbent-fit/fitstats.py |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/fetch_log.jsonl |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/incumbents.jsonl |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/record_facts.json |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/requirements.jsonl |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/sealed_row_ids.json |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/step_a_r1.jsonl |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/step_a_r2.jsonl |
|   undeclared | EXPERIMENTS/028-incumbent-fit/raw/step_b_r1_batch1.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:34:19 | session_start | E028: test whether the incumbents a prior-art screen named do what each killed candidate's distinguishing requirement asks, using primary artifact doc |
| 2 | 18:34:19 | command | $ tools/origin session start --goal E028: test whether the incumbents a prior-art screen named do what each killed candidate's distinguishing |
| 3 | 18:34:37 | task_rewrite | appended a create record for T-0072 |
| 4 | 18:34:38 | command | $ tools/origin task new --goal Test whether the incumbents a prior-art screen named actually do what each killed candidate's distinguishing re |
| 5 | 18:34:43 | command | $ tools/origin task claim --task T-0072 --agent opencode |
| 6 | 18:34:48 | command | $ tools/origin task claim --help |
| 7 | 18:34:53 | command | $ tools/origin task claim T-0072 --agent opencode |
| 8 | 18:34:59 | command | $ git add -A |
| 9 | 18:35:09 | task_rewrite | rewrote tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md (status: claimed) |
| 10 | 18:35:09 | task_rewrite | appended a claim record for T-0072 |
| 11 | 18:35:13 | command | $ tools/origin task claim T-0072 --agent opencode |
| 12 | 18:35:14 | artifact | wrote tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md |
| 13 | 18:35:14 | command | $ tools/origin session artifact tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md |
| 14 | 18:36:46 | milestone | E028 protocol declared before any label or documentation fetch: population 29 prior-art deaths read-only from two existing captures, four gates includ |
| 15 | 18:36:47 | command | $ tools/origin session step E028 protocol declared before any label or documentation fetch: population 29 prior-art deaths read-only from two |
| 16 | 18:36:47 | artifact | wrote EXPERIMENTS/028-incumbent-fit/PROTOCOL.md |
| 17 | 18:36:48 | command | $ tools/origin session artifact EXPERIMENTS/028-incumbent-fit/PROTOCOL.md |
| 18 | 18:38:32 | command | $ python3 EXPERIMENTS/028-incumbent-fit/build_population.py |
| 19 | 18:39:51 | command | $ python3 EXPERIMENTS/028-incumbent-fit/fetch_docs.py |
| 20 | 18:40:27 | command | $ python3 EXPERIMENTS/028-incumbent-fit/fetch_docs.py |
| 21 | 18:41:50 | command | $ python3 EXPERIMENTS/028-incumbent-fit/fetch_docs.py |
| 22 | 18:42:53 | artifact | wrote EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-1.md |
| 23 | 18:42:53 | artifact | wrote EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-2.md |
| 24 | 18:42:54 | artifact | wrote EXPERIMENTS/028-incumbent-fit/RUBRIC.md |
| 25 | 18:42:54 | artifact | wrote EXPERIMENTS/028-incumbent-fit/build_population.py |
| 26 | 18:42:54 | artifact | wrote EXPERIMENTS/028-incumbent-fit/fetch_docs.py |
| 27 | 18:42:54 | command | $ tools/origin session artifact EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-1.md EXPERIMENTS/028-incumbent-fit/PROTOCOL-AMENDMENT-2.md EX |
| 28 | 18:45:45 | command | $ python3 EXPERIMENTS/028-incumbent-fit/make_step_b_view.py --reader r1 |
| 29 | 18:45:45 | command | $ python3 EXPERIMENTS/028-incumbent-fit/make_step_b_view.py --reader r2 |
| 30 | 19:04:46 | command | $ python3 EXPERIMENTS/028-incumbent-fit/stats.py |
| 31 | 19:04:56 | command | $ python3 EXPERIMENTS/028-incumbent-fit/stats.py |
| 32 | 19:05:06 | command | $ python3 EXPERIMENTS/028-incumbent-fit/stats.py |
| 33 | 19:08:14 | command | $ python3 EXPERIMENTS/028-incumbent-fit/stats.py |
| 34 | 19:09:24 | command | $ python3 EXPERIMENTS/028-incumbent-fit/stats.py |
| 35 | 19:10:42 | artifact | wrote EXPERIMENTS/028-incumbent-fit/README.md |
| 36 | 19:10:43 | artifact | wrote EXPERIMENTS/028-incumbent-fit/results.json |
| 37 | 19:10:43 | artifact | wrote EXPERIMENTS/028-incumbent-fit/test_gates_falsified.py |
| 38 | 19:10:43 | artifact | wrote EXPERIMENTS/028-incumbent-fit/stats.py |
| 39 | 19:10:43 | artifact | wrote EXPERIMENTS/028-incumbent-fit/make_step_b_view.py |
| 40 | 19:10:44 | artifact | wrote EXPERIMENTS/028-incumbent-fit/split_batches.py |
| 92 | 20:02:29 | unlogged_change | changed but never declared as an artifact: tools/originlib/paths.py |
| 93 | 20:02:29 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 94 | 20:02:29 | unlogged_change | changed but never declared as an artifact: vendor/MANIFEST.md |
| 95 | 20:02:29 | doc_update | updated DECISIONS-SCREENING-3.md |
| 96 | 20:02:29 | doc_update | updated DECISIONS-SCREENING-4.md |
| 97 | 20:02:29 | doc_update | updated DECISIONS.md |
| 98 | 20:02:29 | doc_update | updated FAILURES.md |
| 99 | 20:02:29 | doc_update | updated ROADMAP.md |
| 100 | 20:02:29 | doc_update | updated STATE.md |
| 101 | 20:02:29 | session_end | E028 tested whether a prior-art screen's evidence is evidence of fit, on the 19 harvest-side prior-art deaths with two blind readers over each named i |

_51 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-017-e028-test-whether-the-incumbents-a-prior/events.jsonl
```
