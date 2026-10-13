# Session 2026-10-13-001-build-and-falsify-a-reusable-instrument

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T00:23:59+00:00
- **Duration:** 5619.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Build and falsify a reusable instrument-validity checker for LLM-output evaluations, using this repository's two committed defective harnesses (E114 verifier FPR=1.00, E116 scorer key mismatch) as real positive cases

## Summary

E124 built and falsified the proposal that this mission's own screens should be preflighted rather than trusted. Three results in three days (F118, F121, F122) were lost to harness defects that raised nothing and turned no declared gate red. preflight (4 stdlib-only modules) measures three properties of an evaluation harness -- key/output identifier concordance, the false-positive rate on correct output per arm, and whether a declared negative arm is negative -- and withholds the rate with exit 3 unless all three hold. Run against the committed harnesses it withholds on four of six cases (A, C, C', D, E) and is silent on B; on every firing case the harness's own declared gates were green. 16 tests pass, most of them trying to make the tool say OK when it should not, four of them injected defects on a sound fixture. Gates K1 4/5, K2 FAILED as declared, K3 pass, K4 pass -- K2 failed because the declared easy arm measured 0.9346 rather than 0.02, which produced the finding rather than a bug: ground.judge() scores context-word overlap, so a value present in the document still scores near zero inside a bare sentence. F123: one verifier, five arms, 0.0069 / 0.1970 / 0.6667 / 0.9346 / 1.0000 -- a false-positive rate belongs to an arm, not to an instrument, and a quoted one does not transfer. D109 makes the three answers an obligation before any future result over generated output. Prior art is partially-covered: no tool does all three, none does C3, and Anthropic's eval playbook already names two of the three in prose.

## Next

Do not build another instrument for this repository's own screens -- that is the audit chain the brief warns about, and D109 already states what the three answers must be. The open question is external: preflight is a prototype with no user outside this repository. The single most useful next action is to point it at a harness this repository does not own -- find a real graded-eval repository with a committed key and published scores, run the three checks against its own artifacts, and record whether it fires on a harness nobody here wrote. A tool that stays quiet on other people's harnesses has no adoption case, and one that fires on all of them has no value either; that result decides whether this becomes a candidate or closes as a process obligation.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md | 41a2fb5feac2 | 8432 |
| FAILURES-findings-40.md | 155ea8c42346 | 13640 |
| DECISIONS-SCREENING-20.md | 64b14ab2ca93 | 11176 |
| FAILURES.md | 5b0d76578859 | 79325 |
| DECISIONS.md | 2b8988b2b451 | 25100 |
| EXPERIMENTS/124-eval-harness-preflight/AMENDMENT-1.md | fc58fb9d68d0 | 3883 |
| EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md | 41a2fb5feac2 | 8432 |
| EXPERIMENTS/124-eval-harness-preflight/README.md | c2be6d25df30 | 2785 |
| EXPERIMENTS/124-eval-harness-preflight/RESULT.md | e7a048454630 | 7233 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/__init__.py | c949ada34bd0 | 980 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/alternate_form.py | 1822df6567f6 | 4030 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/concordance.py | 657f088635e4 | 7748 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/control_arm.py | ff02dda9ba92 | 2624 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/report.py | 2fc6c218d782 | 2586 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/stats.py | e1ae7208f7bf | 1059 |
| EXPERIMENTS/124-eval-harness-preflight/results.json | ed563f3fbc14 | 10944 |
| EXPERIMENTS/124-eval-harness-preflight/run.py | 967fc49e4f82 | 10201 |
| EXPERIMENTS/124-eval-harness-preflight/test_preflight.py | 33ce1c323e55 | 7629 |
| EXPERIMENTS/124-eval-harness-preflight/AMENDMENT-1.md | fc58fb9d68d0 | 3883 |
| EXPERIMENTS/124-eval-harness-preflight/PRIOR-ART.md | 63263ef56d85 | 10733 |
| EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md | 41a2fb5feac2 | 8432 |
| EXPERIMENTS/124-eval-harness-preflight/README.md | 003f977fba73 | 3018 |
| EXPERIMENTS/124-eval-harness-preflight/RESULT.md | d34543a8612d | 8457 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/__init__.py | c949ada34bd0 | 980 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/alternate_form.py | 1822df6567f6 | 4030 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/concordance.py | 657f088635e4 | 7748 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/control_arm.py | ff02dda9ba92 | 2624 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/report.py | 2fc6c218d782 | 2586 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/stats.py | e1ae7208f7bf | 1059 |
| EXPERIMENTS/124-eval-harness-preflight/results.json | ed563f3fbc14 | 10944 |
| EXPERIMENTS/124-eval-harness-preflight/run.py | 967fc49e4f82 | 10201 |
| EXPERIMENTS/124-eval-harness-preflight/test_preflight.py | 33ce1c323e55 | 7629 |
| tests/test_split_equivalence.py | f6188db5e19e | 7952 |
| EXPERIMENTS/124-eval-harness-preflight/test_preflight.py | 33ce1c323e55 | 7629 |
| STATE.md | ff6abc03dbda | 32036 |
| DECISIONS.md | 6be83e4fe786 | 25163 |
| DECISIONS-SCREENING-20.md | 99b50b6a6da8 | 11317 |
| FAILURES.md | 5b0d76578859 | 79325 |
| FAILURES-findings-40.md | 155ea8c42346 | 13640 |
| THINK_FREE_SUMMARY.md | 4f2aaac13d96 | 7315 |
| tools/originlib/paths.py | b6328550cd01 | 4591 |
| tools/originlib/reconcile.py | 64f329e157aa | 8791 |
| tests/test_decision_files.py | 81a6756f0680 | 5598 |
| docs/INDEX.md | d827540112ce | 50252 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 22 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/116-viewcount-classifier-prototype/classify.py |
|   undeclared | EXPERIMENTS/116-viewcount-classifier-prototype/classify_core.py |
|   undeclared | EXPERIMENTS/116-viewcount-classifier-prototype/harvest.py |
|   undeclared | EXPERIMENTS/116-viewcount-classifier-prototype/stats.py |
|   undeclared | EXPERIMENTS/116-viewcount-classifier-prototype/vocab.py |
|   undeclared | EXPERIMENTS/118-pypi-viewcount-matched-harvest/classify.py |
|   undeclared | EXPERIMENTS/118-pypi-viewcount-matched-harvest/classify_core.py |
|   undeclared | EXPERIMENTS/118-pypi-viewcount-matched-harvest/harvest.py |
|   undeclared | EXPERIMENTS/118-pypi-viewcount-matched-harvest/stats.py |
|   undeclared | EXPERIMENTS/118-pypi-viewcount-matched-harvest/vocab.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:23:59 | session_start | Build and falsify a reusable instrument-validity checker for LLM-output evaluations, using this repository's two committed defective harnesses (E114 v |
| 2 | 00:29:49 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md |
| 3 | 00:37:57 | artifact | wrote FAILURES-findings-40.md |
| 4 | 00:38:08 | artifact | wrote DECISIONS-SCREENING-20.md |
| 5 | 00:38:20 | artifact | wrote FAILURES.md |
| 6 | 00:38:31 | artifact | wrote DECISIONS.md |
| 7 | 00:53:00 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/AMENDMENT-1.md |
| 8 | 00:53:14 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md |
| 9 | 00:53:18 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/README.md |
| 10 | 00:53:20 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/RESULT.md |
| 11 | 00:53:21 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/__init__.py |
| 12 | 00:53:24 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/alternate_form.py |
| 13 | 00:53:26 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/concordance.py |
| 14 | 00:53:31 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/control_arm.py |
| 15 | 00:53:58 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/report.py |
| 16 | 00:54:11 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/stats.py |
| 17 | 00:54:43 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/results.json |
| 18 | 00:55:11 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/run.py |
| 19 | 00:55:23 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/test_preflight.py |
| 20 | 00:55:36 | milestone | E124 complete: preflight built (4 modules, 16 tests passing), run against six cases on committed harnesses; K1 4/5, K2 failed as declared, K3 and K4 p |
| 21 | 01:56:57 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/AMENDMENT-1.md |
| 22 | 01:56:58 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/PRIOR-ART.md |
| 23 | 01:56:59 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md |
| 24 | 01:57:00 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/README.md |
| 25 | 01:57:01 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/RESULT.md |
| 26 | 01:57:02 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/__init__.py |
| 27 | 01:57:02 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/alternate_form.py |
| 28 | 01:57:04 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/concordance.py |
| 29 | 01:57:05 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/control_arm.py |
| 30 | 01:57:06 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/report.py |
| 31 | 01:57:07 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/stats.py |
| 32 | 01:57:08 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/results.json |
| 33 | 01:57:09 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/run.py |
| 34 | 01:57:11 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/test_preflight.py |
| 35 | 01:57:12 | artifact | wrote tests/test_split_equivalence.py |
| 36 | 01:57:13 | milestone | verification: doc lint OK (0 violations); full suite 837 tests OK; preflight 16/16; split equivalence 546-646 probes identical per experiment |
| 37 | 01:57:19 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/test_preflight.py |
| 38 | 01:57:20 | artifact | wrote STATE.md |
| 39 | 01:57:21 | artifact | wrote DECISIONS.md |
| 40 | 01:57:22 | artifact | wrote DECISIONS-SCREENING-20.md |
| 65 | 01:57:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-010-design-and-implement-a-fresh-observation/events.jsonl |
| 66 | 01:57:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-011-implement-and-run-e123-ci-cd-build-log-f/events.jsonl |
| 67 | 01:57:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-012-identify-and-design-a-fresh-observation/events.jsonl |
| 68 | 01:57:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-013-design-and-run-a-fresh-observation-exper/events.jsonl |
| 69 | 01:57:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-014-conduct-fresh-observation-experiment-in/events.jsonl |
| 70 | 01:57:39 | doc_update | updated DECISIONS-SCREENING-20.md |
| 71 | 01:57:39 | doc_update | updated DECISIONS.md |
| 72 | 01:57:39 | doc_update | updated FAILURES.md |
| 73 | 01:57:39 | doc_update | updated STATE.md |
| 74 | 01:57:39 | session_end | E124 built and falsified the proposal that this mission's own screens should be preflighted rather than trusted. Three results in three days (F118, F1 |

_24 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-001-build-and-falsify-a-reusable-instrument/events.jsonl
```
