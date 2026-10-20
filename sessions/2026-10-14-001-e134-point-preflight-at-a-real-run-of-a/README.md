# Session 2026-10-14-001-e134-point-preflight-at-a-real-run-of-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T00:38:41+00:00
- **Duration:** 13307.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E134: point preflight at a real run of a harness nobody here wrote, and measure the recomputations R1-R3 on its output

## Summary

E134 closed the preflight release question by running the experiment it had been validated around: a real lm-eval v0.4.4 run (committed raw) plus a third-party published run. R1 recomputes every printed rate from shipped inputs and agrees on all 9 metrics across both arms, so the declared failure condition fired and preflight is not released (D111). The run's real yield was three defects in preflight itself - two non-blocking OK verdicts for checks that measured nothing, and a recall field computing its complement - repaired with 9 regression tests, 4 falsified against the pre-fix code (F125, F126). Landing surfaced 467 doc lint violations on an inherited tree that STATE.md recorded as green, repaired in five named causes (F127, D112). Green: 837 tests, 25 preflight tests, doc lint OK; release check 55 to 53 with the remainder named.

## Next

Ask whether the six-line adapter and R1 reach the format a leaderboard publishes - the number people read without opening results.json. Declared in EXPERIMENTS/134-preflight-real-run/RESULT.md; not a second harness sweep.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/134-preflight-real-run/RESULT.md | 604a3fe31dcb | 9938 |
| EXPERIMENTS/134-preflight-real-run/results_e134.json | b808552f8914 | 90709 |
| EXPERIMENTS/134-preflight-real-run/PROTOCOL.md | 9d440a517a36 | 6863 |
| EXPERIMENTS/134-preflight-real-run/AMENDMENT-1.md | 350adb4d455c | 2267 |
| EXPERIMENTS/134-preflight-real-run/AMENDMENT-2.md | 0b6224c124e3 | 5230 |
| EXPERIMENTS/134-preflight-real-run/AMENDMENT-3.md | be3c31b73a55 | 3997 |
| EXPERIMENTS/134-preflight-real-run/handcheck.md | 085642819814 | 2262 |
| EXPERIMENTS/134-preflight-real-run/run_e134.py | af94ea895aad | 12659 |
| EXPERIMENTS/134-preflight-real-run/recompute.py | b7a51bb76cb0 | 13137 |
| EXPERIMENTS/134-preflight-real-run/lm_eval_adapter.py | 295249aa5115 | 3507 |
| EXPERIMENTS/134-preflight-real-run/dataset_key.py | ea2dfbe6dead | 6036 |
| preflight/test_vacuous_passes.py | 8c867f0b38b4 | 5780 |
| FAILURES-findings-41.md | 8630afe40b74 | 9034 |
| DECISIONS-RECORDS-2.md | fb7b83868b98 | 5606 |
| tools/originlib/doclint_links.py | 1858768958ac | 4480 |
| vendor/MANIFEST.md | e26b1ffdcf5d | 10585 |
| RELEASE-MANIFEST.md | f8f87700ae0c | 6759 |
| STATE.md | 2eb8893e4a6a | 40776 |
| DECISIONS-PUBLISHING.md | 49b53ba448e7 | 15994 |
| tools/originlib/doclint.py | 127510d36cc6 | 10010 |
| preflight/alternate_form.py | 2b45cbd84528 | 5278 |
| preflight/concordance.py | edfbd1cb2961 | 9350 |
| preflight/report.py | 4819d4b2f53d | 3027 |

## Commands

27 captured, 16 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '/tmp/opencode/g/armA.sh'] | 0 | 135556 |
| 4 | ['python3', 'run_e134.py', '--armA', 'armA', '--cache', '/tmp/opencode/hfcache', '--armB', 'armB', '--out', 'results_e134.json'] | 1 | 2343 |
| 5 | ['python3', 'run_e134.py', '--armA', 'armA', '--cache', '/tmp/opencode/hfcache', '--armB', 'armB', '--out', 'results_e134.json'] | 1 | 2041 |
| 6 | ['python3', 'run_e134.py', '--armA', 'armA', '--cache', '/tmp/opencode/hfcache', '--armB', 'armB', '--out', 'results_e134.json'] | 1 | 1894 |
| 7 | ['python3', 'run_e134.py', '--armA', 'armA', '--cache', '/tmp/opencode/hfcache', '--armB', 'armB', '--out', 'results_e134.json'] | 1 | 2018 |
| 8 | ['python3', 'run_e134.py', '--armA', 'armA', '--cache', '/tmp/opencode/hfcache', '--armB', 'armB', '--out', 'results_e134.json'] | 1 | 2130 |
| 9 | ['python3', 'run_e134.py', '--armA', 'armA', '--cache', '/tmp/opencode/hfcache', '--armB', 'armB', '--out', 'results_e134.json'] | 0 | 1912 |
| 11 | ['python3', '-m', 'unittest', 'preflight.test_vacuous_passes', '-v'] | 1 | 294 |
| 12 | ['python3', '-m', 'unittest', 'preflight.test_vacuous_passes', '-v'] | 1 | 232 |
| 13 | ['python3', '-m', 'unittest', 'preflight.test_vacuous_passes.AlternateFormMissingArm.test_both_arms_present_still_passes_when_the_flagger_is_clean'] | 1 | 238 |
| 14 | ['python3', '-m', 'unittest', 'preflight.test_vacuous_passes'] | 1 | 306 |
| 15 | ['python3', '-m', 'unittest', 'preflight.test_vacuous_passes'] | 1 | 296 |
| 16 | ['python3', '-m', 'unittest', 'preflight.test_vacuous_passes'] | 0 | 223 |
| 17 | ['python3', '-m', 'unittest', 'discover', '-s', 'preflight', '-t', '.', '-p', 'test_*.py'] | 1 | 295 |
| 18 | ['python3', '-m', 'unittest', 'discover', '-s', 'preflight', '-t', '.', '-p', 'test_*.py'] | 0 | 293 |
| 19 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 865887 |
| 20 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 852022 |
| 21 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'test_ci_annotations', 'test_identifier_enforcement'] | 1 | 3887 |
| 22 | ['tools/origin', 'doc', 'index'] | 0 | 9568 |
| 24 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 832588 |
| 25 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 841490 |
| 26 | ['tools/origin', 'doc', 'index'] | 0 | 5568 |
| 43 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 702797 |
| 44 | ['python3', '-m', 'unittest', 'discover', '-s', 'preflight', '-t', '.', '-p', 'test_*.py'] | 0 | 303 |
| 45 | ['tools/origin', 'release', 'check'] | 2 | 421357 |
| 54 | ['tools/origin', 'doc', 'lint'] | 0 | 146881 |
| 55 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 866009 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 22 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-RECORDS.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/130-preflight-adapter-prototype/RESULT.md |
|   undeclared | EXPERIMENTS/130-preflight-third-harness/RESULT.md |
|   undeclared | EXPERIMENTS/131-preflight-fourth-harness/RESULT.md |
|   undeclared | EXPERIMENTS/132-preflight-fifth-harness/RESULT.md |
|   undeclared | EXPERIMENTS/133-preflight-sixth-harness/RESULT.md |
|   undeclared | EXPERIMENTS/134-preflight-real-run/armA/results_2026-10-14T00-52-55.068909.json |
|   undeclared | EXPERIMENTS/134-preflight-real-run/armA/samples_openbookqa_2026-10-14T00-52-55.068909.jsonl |
|   undeclared | EXPERIMENTS/134-preflight-real-run/armA/samples_piqa_2026-10-14T00-52-55.068909.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:38:41 | session_start | E134: point preflight at a real run of a harness nobody here wrote, and measure the recomputations R1-R3 on its output |
| 2 | 00:53:06 | command | $ bash /tmp/opencode/g/armA.sh |
| 3 | 01:19:38 | milestone | E134 runner written; Arm A raw output committed to the experiment directory |
| 4 | 01:19:48 | command | $ python3 run_e134.py --armA armA --cache /tmp/opencode/hfcache --armB armB --out results_e134.json |
| 5 | 01:20:23 | command | $ python3 run_e134.py --armA armA --cache /tmp/opencode/hfcache --armB armB --out results_e134.json |
| 6 | 01:20:42 | command | $ python3 run_e134.py --armA armA --cache /tmp/opencode/hfcache --armB armB --out results_e134.json |
| 7 | 01:21:09 | command | $ python3 run_e134.py --armA armA --cache /tmp/opencode/hfcache --armB armB --out results_e134.json |
| 8 | 01:21:21 | command | $ python3 run_e134.py --armA armA --cache /tmp/opencode/hfcache --armB armB --out results_e134.json |
| 9 | 01:21:51 | command | $ python3 run_e134.py --armA armA --cache /tmp/opencode/hfcache --armB armB --out results_e134.json |
| 10 | 01:24:18 | milestone | E134 gates scored: G1/G2/G3 PASS, G4 FAIL, G5 PARTIAL; R1 agrees on all 9 metrics across two arms; two vacuous passes found in preflight itself |
| 11 | 01:24:51 | command | $ python3 -m unittest preflight.test_vacuous_passes -v |
| 12 | 01:24:57 | command | $ python3 -m unittest preflight.test_vacuous_passes -v |
| 13 | 01:25:04 | command | $ python3 -m unittest preflight.test_vacuous_passes.AlternateFormMissingArm.test_both_arms_present_still_passes_when_the_flagger_is_clean |
| 14 | 01:26:06 | command | $ python3 -m unittest preflight.test_vacuous_passes |
| 15 | 01:26:27 | command | $ python3 -m unittest preflight.test_vacuous_passes |
| 16 | 01:26:37 | command | $ python3 -m unittest preflight.test_vacuous_passes |
| 17 | 01:26:38 | command | $ python3 -m unittest discover -s preflight -t . -p test_*.py |
| 18 | 01:26:57 | command | $ python3 -m unittest discover -s preflight -t . -p test_*.py |
| 19 | 01:41:24 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 20 | 01:55:46 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 21 | 01:56:01 | command | $ env PYTHONPATH=tools:tests python3 -m unittest test_ci_annotations test_identifier_enforcement |
| 22 | 02:25:17 | command | $ tools/origin doc index |
| 23 | 02:30:50 | milestone | doc lint repaired from 467 violations to 0: four named causes (E125 evidence globs, E130 stubs, six named files that were never written, D046 collisio |
| 24 | 02:44:44 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 25 | 02:59:08 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 26 | 03:20:40 | command | $ tools/origin doc index |
| 27 | 03:20:42 | artifact | wrote EXPERIMENTS/134-preflight-real-run/RESULT.md |
| 28 | 03:20:43 | artifact | wrote EXPERIMENTS/134-preflight-real-run/results_e134.json |
| 29 | 03:20:44 | artifact | wrote EXPERIMENTS/134-preflight-real-run/PROTOCOL.md |
| 30 | 03:20:45 | artifact | wrote EXPERIMENTS/134-preflight-real-run/AMENDMENT-1.md |
| 31 | 03:20:47 | artifact | wrote EXPERIMENTS/134-preflight-real-run/AMENDMENT-2.md |
| 32 | 03:20:48 | artifact | wrote EXPERIMENTS/134-preflight-real-run/AMENDMENT-3.md |
| 33 | 03:20:49 | artifact | wrote EXPERIMENTS/134-preflight-real-run/handcheck.md |
| 34 | 03:20:50 | artifact | wrote EXPERIMENTS/134-preflight-real-run/run_e134.py |
| 35 | 03:20:52 | artifact | wrote EXPERIMENTS/134-preflight-real-run/recompute.py |
| 36 | 03:20:53 | artifact | wrote EXPERIMENTS/134-preflight-real-run/lm_eval_adapter.py |
| 37 | 03:20:56 | artifact | wrote EXPERIMENTS/134-preflight-real-run/dataset_key.py |
| 38 | 03:20:57 | artifact | wrote preflight/test_vacuous_passes.py |
| 39 | 03:20:58 | artifact | wrote FAILURES-findings-41.md |
| 40 | 03:21:00 | artifact | wrote DECISIONS-RECORDS-2.md |
| 75 | 04:20:28 | unlogged_change | changed but never declared as an artifact: tests/test_link_escape.py |
| 76 | 04:20:28 | unlogged_change | changed but never declared as an artifact: tools/originlib/paths.py |
| 77 | 04:20:28 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 78 | 04:20:28 | doc_update | updated DECISIONS-PUBLISHING.md |
| 79 | 04:20:28 | doc_update | updated DECISIONS-RECORDS-2.md |
| 80 | 04:20:28 | doc_update | updated DECISIONS-RECORDS.md |
| 81 | 04:20:28 | doc_update | updated DECISIONS.md |
| 82 | 04:20:28 | doc_update | updated FAILURES.md |
| 83 | 04:20:28 | doc_update | updated STATE.md |
| 84 | 04:20:28 | session_end | E134 closed the preflight release question by running the experiment it had been validated around: a real lm-eval v0.4.4 run (committed raw) plus a th |

_34 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-001-e134-point-preflight-at-a-real-run-of-a/events.jsonl
```
