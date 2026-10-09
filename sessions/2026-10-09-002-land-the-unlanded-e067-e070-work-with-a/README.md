# Session 2026-10-09-002-land-the-unlanded-e067-e070-work-with-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T00:16:21+00:00
- **Duration:** 9471.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Land the unlanded E067-E070 work with a source manifest for the 5.5GB CFPB input, then run E071: does the E066 recurring-expense detector survive real merchant-string noise?

## Summary

Landed the six unlanded 2026-10-08 sessions and E067-E070; ran E071 (neither the HN API, 0 of 60, nor the GitHub issues API, 0 of 8, returns any arrival field, while Stack Exchange returns a positive view_count on 80 of 80 - F101, D088, and E069's CONFIRMED is withdrawn) and E072 (E065's recurring-expense detector unmodified on 36 real modern bank exports, 34231 transactions, 29 public repositories, 2021-2026: recall 0.394, F1 0.160, G1 and G2 did not fire - F185, D090). E072's failure was not the merchant-name axis E066 named: it is worth 6 of 20 misses, while 14 come from an amount-CV ceiling nobody had questioned, so one price change makes a subscription invisible. Two reading results: Actual Budget's shipped findSchedules() scores F1 0.150 against E065's 0.160, so the engines are within noise and the merchant axis is the mechanism; and precision reads 0.100 against a positives-only watchlist where a hand-read stratified sample reads 0.91 on the same detections.

## Next

Replace the CV ceiling with a piecewise-constant price model and measure it on E072's frozen corpus, with detect.py frozen as the baseline arm and a predeclared G1 recall >= 0.50, G2 unchanged. Evidence that it is a specification defect rather than a threshold to tune: a24's ChatGPT is 9 x 0.00, CV 0.000, interval regularity 0.922 and is detected today, while the identical mechanism with one price step is missed in four accounts. A pass closes the detector, not the domain: F185 closes one implementation on 36 public exports, and whether a person pays for this is open because Actual already ships the feature and E072's actual_raw 0.150 is a floor.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/071-viewcount-denominator/README.md | 65887dd4cd19 | 5079 |
| EXPERIMENTS/071-viewcount-denominator/results.json | 550537716ba1 | 3451 |
| tools/originlib/idalloc.py | 420f1cf7baf0 | 10926 |
| tests/test_idalloc.py | caaeb55a1209 | 8704 |
| STATE-in-flight-9.md | 3c9a8284130d | 6254 |
| EXPERIMENTS/071-viewcount-denominator/PROTOCOL.md | 206ba7fb09b2 | 4678 |
| tools/originlib/paths.py | f83248500a1b | 4388 |
| tools/originlib/reconcile.py | 6cdabd88694b | 8540 |
| tests/test_decision_files.py | 512e96a17802 | 5395 |
| tools/originlib/paths.py | f83248500a1b | 4388 |
| EXPERIMENTS/070-discourse-fresh-observation/raw/SOURCES.md | f5116226d956 | 2184 |
| .gitignore | e3b4ed37f5f1 | 3354 |
| MISSION-OUTCOME.json | 335fe03e8bf6 | 3244 |
| EXPERIMENTS/072-merchant-noise-raw/PROTOCOL.md | 82f97ecdda68 | 7560 |
| EXPERIMENTS/072-merchant-noise-raw/README.md | 5010344793c3 | 9835 |
| EXPERIMENTS/072-merchant-noise-raw/results.json | 0a8061fdfb6e | 31824 |
| EXPERIMENTS/072-merchant-noise-raw/verdict.json | 9f72ff28de9b | 2188 |
| EXPERIMENTS/072-merchant-noise-raw/raw/CORPUS.json | 57677f50a3e4 | 25097 |
| EXPERIMENTS/072-merchant-noise-raw/raw/SOURCES.json | fe0dc7711d2a | 23808 |
| EXPERIMENTS/072-merchant-noise-raw/watchlist.json | 66c80fa3f6ea | 14389 |
| EXPERIMENTS/072-merchant-noise-raw/precision_labels.json | da16909895d4 | 4523 |
| EXPERIMENTS/072-merchant-noise-raw/corpus.py | 8f217b7f4a5f | 9168 |
| EXPERIMENTS/072-merchant-noise-raw/finalize.py | e44fd1c4d4b9 | 8061 |
| EXPERIMENTS/072-merchant-noise-raw/eval_arms.py | 7fca2b996304 | 10247 |
| EXPERIMENTS/072-merchant-noise-raw/fire_gates.py | f11e5dd14e46 | 6712 |
| EXPERIMENTS/072-merchant-noise-raw/actual_find_schedules.py | 519fd1cc997c | 11767 |
| EXPERIMENTS/072-merchant-noise-raw/arm_sign.py | 3dbe36ba091e | 4679 |
| EXPERIMENTS/072-merchant-noise-raw/relabel.py | fada31a33ebb | 4911 |
| EXPERIMENTS/072-merchant-noise-raw/probe_undergroup.py | 31b3384c9703 | 5433 |
| EXPERIMENTS/072-merchant-noise-raw/inspect_errors.py | 3c891e2ecf54 | 4852 |
| EXPERIMENTS/072-merchant-noise-raw/test_no_descriptor_leaks.py | d2140afa67fb | 5012 |
| FAILURES-findings-35.md | 189ee07167af | 5122 |
| DECISIONS-SCREENING-16.md | 4827c759cc05 | 4124 |
| STATE.md | 20385e81be82 | 37118 |
| STATE-history.md | 1f1674c44327 | 21476 |
| STATE-history-2.md | bc3fc37b082a | 10476 |
| DECISIONS.md | eb01e62837b6 | 16243 |
| FAILURES.md | 4ff9def9711b | 63480 |
| .gitignore | 9fbda7de1e73 | 4219 |
| EXPERIMENTS/072-merchant-noise-raw/PROTOCOL.md | 82f97ecdda68 | 7560 |
| EXPERIMENTS/072-merchant-noise-raw/README.md | 5010344793c3 | 9835 |
| EXPERIMENTS/072-merchant-noise-raw/results.json | 0a8061fdfb6e | 31824 |
| EXPERIMENTS/072-merchant-noise-raw/verdict.json | 9f72ff28de9b | 2188 |
| EXPERIMENTS/072-merchant-noise-raw/raw/CORPUS.json | 57677f50a3e4 | 25097 |
| EXPERIMENTS/072-merchant-noise-raw/raw/SOURCES.json | fe0dc7711d2a | 23808 |
| EXPERIMENTS/072-merchant-noise-raw/watchlist.json | 66c80fa3f6ea | 14389 |
| EXPERIMENTS/072-merchant-noise-raw/precision_labels.json | da16909895d4 | 4523 |
| EXPERIMENTS/072-merchant-noise-raw/corpus.py | 8f217b7f4a5f | 9168 |
| EXPERIMENTS/072-merchant-noise-raw/finalize.py | e44fd1c4d4b9 | 8061 |
| EXPERIMENTS/072-merchant-noise-raw/eval_arms.py | 7fca2b996304 | 10247 |
| EXPERIMENTS/072-merchant-noise-raw/fire_gates.py | f11e5dd14e46 | 6712 |
| EXPERIMENTS/072-merchant-noise-raw/actual_find_schedules.py | 519fd1cc997c | 11767 |
| EXPERIMENTS/072-merchant-noise-raw/arm_sign.py | 3dbe36ba091e | 4679 |
| EXPERIMENTS/072-merchant-noise-raw/relabel.py | fada31a33ebb | 4911 |
| EXPERIMENTS/072-merchant-noise-raw/probe_undergroup.py | 31b3384c9703 | 5433 |
| EXPERIMENTS/072-merchant-noise-raw/inspect_errors.py | 3c891e2ecf54 | 4852 |
| EXPERIMENTS/072-merchant-noise-raw/test_no_descriptor_leaks.py | d2140afa67fb | 5012 |
| FAILURES-findings-35.md | 189ee07167af | 5122 |
| DECISIONS-SCREENING-16.md | 4827c759cc05 | 4124 |
| STATE.md | 20385e81be82 | 37118 |
| STATE-history.md | 1f1674c44327 | 21476 |
| STATE-history-2.md | bc3fc37b082a | 10476 |
| DECISIONS.md | eb01e62837b6 | 16243 |
| FAILURES.md | 4ff9def9711b | 63480 |
| .gitignore | 9fbda7de1e73 | 4219 |
| tools/originlib/paths.py | 8804369ca615 | 4421 |
| tools/originlib/reconcile.py | 1a57193b975d | 8581 |
| tests/test_decision_files.py | 22f836f8dc5c | 5428 |

## Commands

7 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 7 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 970020 |
| 8 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'decision_files', '-v'] | 1 | 785 |
| 9 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'decision_files'] | 1 | 801 |
| 10 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'decision'] | 0 | 7201 |
| 23 | ['tools/origin', 'doc', 'lint'] | 0 | 242410 |
| 24 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'decision'] | 1 | 10812 |
| 86 | ['tools/origin', 'doc', 'lint'] | 2 | 1238072 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 35 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-15.md |
|   undeclared | EXPERIMENTS/067-viewcount-framework/README.md |
|   undeclared | EXPERIMENTS/067-viewcount-framework/classify.py |
|   undeclared | EXPERIMENTS/067-viewcount-framework/outcome.py |
|   undeclared | EXPERIMENTS/067-viewcount-framework/viewcount.py |
|   undeclared | EXPERIMENTS/067b-did-you-mean-test/EXPERIMENT-RESULT.json |
|   undeclared | EXPERIMENTS/067b-did-you-mean-test/README.md |
|   undeclared | EXPERIMENTS/067b-did-you-mean-test/results-raw.json |
|   undeclared | EXPERIMENTS/069-false-accept-confusion/PROTOCOL.md |
|   undeclared | EXPERIMENTS/069-false-accept-confusion/README.md |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:16:21 | session_start | Land the unlanded E067-E070 work with a source manifest for the 5.5GB CFPB input, then run E071: does the E066 recurring-expense detector survive real |
| 2 | 01:28:40 | artifact | wrote EXPERIMENTS/071-viewcount-denominator/README.md |
| 3 | 01:28:42 | artifact | wrote EXPERIMENTS/071-viewcount-denominator/results.json |
| 4 | 01:28:44 | artifact | wrote tools/originlib/idalloc.py |
| 5 | 01:28:46 | artifact | wrote tests/test_idalloc.py |
| 6 | 01:28:48 | artifact | wrote STATE-in-flight-9.md |
| 7 | 01:44:40 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 8 | 01:45:59 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k decision_files -v |
| 9 | 01:46:19 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k decision_files |
| 10 | 01:47:01 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k decision |
| 11 | 01:49:13 | decision | D088 view_count is an arrival measure only where a platform publishes one; the E069 CONFIRMED contrast is withdrawn (F101) |
| 12 | 01:49:15 | decision | D089 a landing carries the correction not the summary; third-party bulk input is recorded by hash and never committed; an allocator's output is checke |
| 13 | 01:49:16 | artifact | wrote EXPERIMENTS/071-viewcount-denominator/PROTOCOL.md |
| 14 | 01:49:17 | artifact | wrote tools/originlib/paths.py |
| 15 | 01:49:18 | artifact | wrote tools/originlib/reconcile.py |
| 16 | 01:49:18 | artifact | wrote tests/test_decision_files.py |
| 17 | 01:49:30 | note | Suite: 832 tests, one failure on arrival -- DECISIONS-SCREENING-15.md was on disk but named in none of the three decision-file lists. Repaired in path |
| 18 | 01:49:31 | artifact | wrote tools/originlib/paths.py |
| 19 | 01:49:32 | artifact | wrote EXPERIMENTS/070-discourse-fresh-observation/raw/SOURCES.md |
| 20 | 01:49:32 | artifact | wrote .gitignore |
| 21 | 01:49:33 | artifact | wrote MISSION-OUTCOME.json |
| 22 | 01:50:02 | experiment_result | Neither the HN API (0 of 60) nor the GitHub issues API (0 of 8) returns an arrival field; Stack Exchange returns a positive view_count on 80 of 80. E0 |
| 23 | 01:56:44 | command | $ tools/origin doc lint |
| 24 | 02:30:56 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k decision |
| 25 | 02:31:02 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/PROTOCOL.md |
| 26 | 02:31:04 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/README.md |
| 27 | 02:31:05 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/results.json |
| 28 | 02:31:06 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/verdict.json |
| 29 | 02:31:08 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/raw/CORPUS.json |
| 30 | 02:31:09 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/raw/SOURCES.json |
| 31 | 02:31:10 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/watchlist.json |
| 32 | 02:31:12 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/precision_labels.json |
| 33 | 02:31:17 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/corpus.py |
| 34 | 02:31:20 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/finalize.py |
| 35 | 02:31:21 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/eval_arms.py |
| 36 | 02:31:23 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/fire_gates.py |
| 37 | 02:31:42 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/actual_find_schedules.py |
| 38 | 02:31:46 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/arm_sign.py |
| 39 | 02:31:47 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/relabel.py |
| 40 | 02:31:52 | artifact | wrote EXPERIMENTS/072-merchant-noise-raw/probe_undergroup.py |
| 119 | 02:54:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-08-027-explore-the-existence-checking-false-acc/events.jsonl |
| 120 | 02:54:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-08-028-fresh-observation-in-a-new-non-software/events.jsonl |
| 121 | 02:54:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-001-declare-remaining-artifacts-from-e070-se/events.jsonl |
| 122 | 02:54:13 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 123 | 02:54:13 | doc_update | updated DECISIONS-SCREENING-15.md |
| 124 | 02:54:13 | doc_update | updated DECISIONS-SCREENING-16.md |
| 125 | 02:54:13 | doc_update | updated DECISIONS.md |
| 126 | 02:54:13 | doc_update | updated FAILURES.md |
| 127 | 02:54:13 | doc_update | updated STATE.md |
| 128 | 02:54:13 | session_end | Landed the six unlanded 2026-10-08 sessions and E067-E070; ran E071 (neither the HN API, 0 of 60, nor the GitHub issues API, 0 of 8, returns any arriv |

_78 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-002-land-the-unlanded-e067-e070-work-with-a/events.jsonl
```
