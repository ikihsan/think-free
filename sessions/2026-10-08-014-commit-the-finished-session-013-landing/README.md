# Session 2026-10-08-014-commit-the-finished-session-013-landing

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T10:33:54+00:00
- **Duration:** 17760.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

commit the finished session 013 landing and choose the next experiment

## Summary

Landed the finished session 013 work and prepared for next experiment

## Next

Explore the installer guards gap from E064/F099

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/063-own-corpus-answerability/README.md | b44e0bb03c5c | 6898 |
| EXPERIMENTS/064-remedy-existence/README.md | 790984b7470f | 9054 |
| EXPERIMENTS/064-remedy-existence/PROTOCOL.md | 8160b87ac1cd | 5994 |
| EXPERIMENTS/064-remedy-existence/AMENDMENT-1.md | 5f69953195aa | 6472 |
| EXPERIMENTS/064-remedy-existence/registry.py | 49a562fb1ab1 | 6415 |
| EXPERIMENTS/064-remedy-existence/meta.py | 4fd5f602ae14 | 9969 |
| EXPERIMENTS/064-remedy-existence/control.py | 63146e950849 | 7142 |
| EXPERIMENTS/064-remedy-existence/mutate.py | af80abbf1d6e | 4466 |
| EXPERIMENTS/064-remedy-existence/extract.py | 146777e671e3 | 7299 |
| EXPERIMENTS/064-remedy-existence/outcome.py | 8dedefcfa926 | 7136 |
| EXPERIMENTS/064-remedy-existence/raw/verdicts-pypi.json | 1ac6f015a87a | 18614 |
| EXPERIMENTS/064-remedy-existence/raw/verdicts-npm.json | 89a2bee2fb72 | 13765 |
| EXPERIMENTS/064-remedy-existence/raw/verdicts-crates.json | b63c4053186a | 9428 |
| EXPERIMENTS/064-remedy-existence/raw/verdicts-gem.json | 08ebf692d318 | 9124 |
| EXPERIMENTS/064-remedy-existence/raw/verdicts-packagist.json | f857227b617d | 5346 |
| EXPERIMENTS/064-remedy-existence/raw/verdicts-seeds.json | a2f342fb8298 | 3347 |
| EXPERIMENTS/064-remedy-existence/raw/metadata-falseaccepts.json | 4ebab9273d1f | 25275 |
| EXPERIMENTS/064-remedy-existence/raw/metadata-real.json | 891afcc24357 | 9540 |
| EXPERIMENTS/064-remedy-existence/raw/mutations.json | 2c26cad23a9d | 88032 |
| EXPERIMENTS/064-remedy-existence/raw/refetch-real-12.json | 5c5cd58a29c6 | 3814 |
| DECISIONS-SCREENING-14.md | 9a0841277e89 | 4864 |
| EXPERIMENTS/064-remedy-existence/raw/controls-all.tsv | 8fdd114453e6 | 1976 |
| EXPERIMENTS/064-remedy-existence/raw/controls-invented.tsv | 24f642bddf23 | 826 |
| EXPERIMENTS/064-remedy-existence/raw/controls-real.tsv | ff2b3bc61bb4 | 741 |
| EXPERIMENTS/064-remedy-existence/raw/extracted-A.json | de2fe9af01d8 | 303593 |
| EXPERIMENTS/064-remedy-existence/raw/names-falseaccepts.tsv | bcd311e2bff7 | 1600 |
| EXPERIMENTS/064-remedy-existence/raw/names-pypi.tsv | 57c69793c2cb | 9018 |
| EXPERIMENTS/064-remedy-existence/raw/names-npm.tsv | 4fb4e15bd42a | 6474 |
| EXPERIMENTS/064-remedy-existence/raw/names-crates.tsv | a508bacd854e | 4506 |
| EXPERIMENTS/064-remedy-existence/raw/names-gem.tsv | 7c6b27515bb2 | 4170 |
| EXPERIMENTS/064-remedy-existence/raw/names-packagist.tsv | 328d03fe1efd | 3918 |
| EXPERIMENTS/064-remedy-existence/raw/needs-B.jsonl | 8f927ceb6822 | 13483 |
| EXPERIMENTS/064-remedy-existence/raw/verdicts-controls.json | 9ba4c312a104 | 6280 |
| EXPERIMENTS/064-remedy-existence/raw/refetch-real-12.tsv | a1c7d2568812 | 287 |
| EXPERIMENTS/064-remedy-existence/fetch_needs.py | 5a6ca87c71a9 | 3781 |
| EXPERIMENTS/064-remedy-existence/controls.py | 710b13c403e0 | 2475 |
| STATE.md | 1e198dbc7cef | 39118 |
| FAILURES.md | bf31b16f5eb6 | 61818 |
| FAILURES-findings-33.md | b0c531475a66 | 11689 |
| DECISIONS.md | eaecd1a98e35 | 15252 |
| EXPERIMENTS/README.md | 17cdc3334997 | 9426 |
| docs/INDEX.md | 04d01943223b | 34590 |

## Commands

10 captured, 4 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 7 | ['python3', 'EXPERIMENTS/055-index-postcondition/run.py', '--verify'] | 3 | 194 |
| 50 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_decision_files', 'tests.test_decision_header', 'tests.test_decision_row_pat | 1 | 10801 |
| 51 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_decision_files', 'tests.test_decision_header', 'tests.test_decision_row_pat | 1 | 10963 |
| 52 | ['python3', 'EXPERIMENTS/049-lockfile-closure/harness.py', '--verify'] | 0 | 1885 |
| 53 | ['python3', 'EXPERIMENTS/045-demand-evidence/read.py'] | 0 | 13414 |
| 54 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 847244 |
| 61 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_decision_files', 'tests.test_decision_header', 'tests.test_decision_row_pat | 0 | 12681 |
| 62 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 1936587 |
| 63 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 2340206 |
| 64 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 1234217 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 36 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS-SCREENING-13.md |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/AMENDMENT-1.md |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/PROTOCOL.md |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/outcome.py |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/raw/control-key.json |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/raw/controls.tsv |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/raw/labels-pass1.tsv |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/raw/queue-unique.tsv |
|   undeclared | EXPERIMENTS/063-own-corpus-answerability/raw/queue.tsv |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:33:54 | session_start | commit the finished session 013 landing and choose the next experiment |
| 2 | 10:58:20 | artifact | wrote EXPERIMENTS/063-own-corpus-answerability/README.md |
| 3 | 10:58:25 | milestone | recovered context; orphan suite processes from aborted calls killed; relaunched one suite run detached |
| 4 | 11:41:25 | milestone | resumed session 014 after interruption; E064 has a prototype and 2 of 30 invented control names resolved to real packages — verifying that first |
| 5 | 11:56:09 | milestone | resumed 014 after restart; verified remote quiet (origin at 7a9da7d), landing 013 (E063/F098/D085/defect-24) before running E064-A1 mutations |
| 6 | 12:05:31 | milestone | landed session 013 as 779bddd: E063/F098/D085 record + defect-24 repair + 13 tests; E064 and session-014 stream left uncommitted |
| 7 | 12:44:30 | command | $ python3 EXPERIMENTS/055-index-postcondition/run.py --verify |
| 8 | 13:18:37 | artifact | wrote EXPERIMENTS/064-remedy-existence/README.md |
| 9 | 13:18:38 | artifact | wrote EXPERIMENTS/064-remedy-existence/PROTOCOL.md |
| 10 | 13:18:39 | artifact | wrote EXPERIMENTS/064-remedy-existence/AMENDMENT-1.md |
| 11 | 13:18:40 | artifact | wrote EXPERIMENTS/064-remedy-existence/registry.py |
| 12 | 13:18:41 | artifact | wrote EXPERIMENTS/064-remedy-existence/meta.py |
| 13 | 13:18:42 | artifact | wrote EXPERIMENTS/064-remedy-existence/control.py |
| 14 | 13:18:43 | artifact | wrote EXPERIMENTS/064-remedy-existence/mutate.py |
| 15 | 13:18:44 | artifact | wrote EXPERIMENTS/064-remedy-existence/extract.py |
| 16 | 13:18:45 | artifact | wrote EXPERIMENTS/064-remedy-existence/outcome.py |
| 17 | 13:18:46 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/verdicts-pypi.json |
| 18 | 13:18:47 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/verdicts-npm.json |
| 19 | 13:18:48 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/verdicts-crates.json |
| 20 | 13:18:49 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/verdicts-gem.json |
| 21 | 13:18:50 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/verdicts-packagist.json |
| 22 | 13:18:51 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/verdicts-seeds.json |
| 23 | 13:18:52 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/metadata-falseaccepts.json |
| 24 | 13:18:53 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/metadata-real.json |
| 25 | 13:18:55 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/mutations.json |
| 26 | 13:18:56 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/refetch-real-12.json |
| 27 | 13:18:57 | artifact | wrote DECISIONS-SCREENING-14.md |
| 28 | 13:19:09 | milestone | E064-A1 verdict recorded: G5 fired (93/576 near-miss mutations resolve, 0.1615 CI95 0.134-0.194); G6 recall arm failed (0.742 vs 0.90), specificity pa |
| 29 | 13:19:31 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/controls-all.tsv |
| 30 | 13:19:32 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/controls-invented.tsv |
| 31 | 13:19:33 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/controls-real.tsv |
| 32 | 13:19:34 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/extracted-A.json |
| 33 | 13:19:35 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/names-falseaccepts.tsv |
| 34 | 13:19:36 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/names-pypi.tsv |
| 35 | 13:19:37 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/names-npm.tsv |
| 36 | 13:19:38 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/names-crates.tsv |
| 37 | 13:19:39 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/names-gem.tsv |
| 38 | 13:19:40 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/names-packagist.tsv |
| 39 | 13:19:41 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/needs-B.jsonl |
| 40 | 13:19:42 | artifact | wrote EXPERIMENTS/064-remedy-existence/raw/verdicts-controls.json |
| 97 | 15:29:54 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 98 | 15:29:54 | unlogged_change | changed but never declared as an artifact: tools/originlib/recorder.py |
| 99 | 15:29:54 | unlogged_change | changed but never declared as an artifact: tools/originlib/session.py |
| 100 | 15:29:55 | unlogged_change | changed but never declared as an artifact: tools/originlib/sessionlock.py |
| 101 | 15:29:55 | doc_update | updated DECISIONS-SCREENING-13.md |
| 102 | 15:29:55 | doc_update | updated DECISIONS-SCREENING-14.md |
| 103 | 15:29:55 | doc_update | updated DECISIONS.md |
| 104 | 15:29:55 | doc_update | updated FAILURES.md |
| 105 | 15:29:55 | doc_update | updated STATE.md |
| 106 | 15:29:55 | session_end | Landed the finished session 013 work and prepared for next experiment |

_56 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-014-commit-the-finished-session-013-landing/events.jsonl
```
