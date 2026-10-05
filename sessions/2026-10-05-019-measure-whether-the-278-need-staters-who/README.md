# Session 2026-10-05-019-measure-whether-the-278-need-staters-who

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `opencode`
- **Started:** 2026-10-05T20:13:48+00:00
- **Duration:** 6184.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure whether the 278 need-staters who shipped something shipped the thing they said was missing, against mismatched and thread-title controls

## Summary

Chose the one join nobody had made in the demand-side corpus and ran it end to end. The fetch alone produced the durable result: of 241 need-staters with a public Show HN item, 167 shipped BEFORE they stated the need and only 74 after, so 69% of the population was never askable and the first design would have manufactured its own null; the id-ordering proxy behind that split was falsified against real timestamps on 8 of 8 sampled authors from both sides. The reader arm came back not_evaluated on two pre-declared counts (kappa 0.5004 against a floor of 0.6; control separation 0.0405 against a required 0.20) and bounds the need-to-build link at CI95 [-0.0156, +0.1125], consistent with zero -- so F042's 0-of-24 is CONFIRMED on a 10x larger instrument rather than refuted, and item 0d's closure stands with a better description of what the corpus is. Three defects in the run's own instrument, none found by a result: 45 control rows rendered an empty SHIPPED section (caught by a test whose population was what hid it); the control was the treatment arm renamed, caught by the arm that feeds no gate printing byte-identical lexical means; and a label file with 222 correct ids and a wrong row-to-pair mapping, which my own repair script then made worse at a reassuring 221/222. No candidate and no validated claim; the generator seat stays empty.

## Next

Stop reading the need corpus -- it has now been read three times and each reading narrows it. The open question item 0 cannot settle is what the mission selects candidates on now that no axis can carry it; the cheapest untried move is to name one concrete selection rule, apply it to the one untested mechanism line left (E2's lockfile claim, side A already banked and needing a weeks-later side B), and see whether it selects anything.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/029-need-build-match/PROTOCOL.md | a97c5df55b20 | 8651 |
| EXPERIMENTS/029-need-build-match/RUBRIC.md | a09736e66de9 | 3710 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md | 12a69772ff78 | 4160 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md | 12a69772ff78 | 4160 |
| EXPERIMENTS/029-need-build-match/PROTOCOL.md | a97c5df55b20 | 8651 |
| EXPERIMENTS/029-need-build-match/RUBRIC.md | a09736e66de9 | 3710 |
| EXPERIMENTS/029-need-build-match/build_population.py | d56a868fc632 | 4912 |
| EXPERIMENTS/029-need-build-match/fetch_builds.py | eaf568a624fd | 5988 |
| EXPERIMENTS/029-need-build-match/make_reader_views.py | 6340aa1c26b8 | 6266 |
| EXPERIMENTS/029-need-build-match/raw/builds.jsonl | d736a3a68cd7 | 168568 |
| EXPERIMENTS/029-need-build-match/raw/gate_a2_controls.jsonl | 9ff639f69633 | 581 |
| EXPERIMENTS/029-need-build-match/raw/population.jsonl | f1d32b35d9db | 175291 |
| EXPERIMENTS/029-need-build-match/raw/stories.jsonl | fffb70d6e6f5 | 39726 |
| EXPERIMENTS/029-need-build-match/raw/view_key.json | aaa4ce202292 | 21790 |
| EXPERIMENTS/029-need-build-match/raw/view_r1.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/raw/view_r2.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-2.md | cd3839a2304c | 3716 |
| EXPERIMENTS/029-need-build-match/assemble_labels.py | 37538a92dfd7 | 3807 |
| EXPERIMENTS/029-need-build-match/stats.py | 02e1e077d189 | 13144 |
| EXPERIMENTS/029-need-build-match/test_claims.py | 15a4161c136f | 19588 |
| EXPERIMENTS/029-need-build-match/raw/view_r1_v1.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/raw/view_r2_v1.txt | 607590ffbfb1 | 125878 |
| EXPERIMENTS/029-need-build-match/raw/view_r1_xonly.txt | a518d8ccd34b | 57643 |
| EXPERIMENTS/029-need-build-match/raw/view_r2_xonly.txt | a518d8ccd34b | 57643 |
| EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-3.md | a56005286144 | 5525 |
| EXPERIMENTS/029-need-build-match/intervalstats.py | a658cd6b004e | 4572 |
| EXPERIMENTS/029-need-build-match/test_reader_blindness.py | fd271896b84c | 12272 |
| EXPERIMENTS/029-need-build-match/test_label_provenance.py | 5bb1c329c4b0 | 4983 |
| EXPERIMENTS/029-need-build-match/test_claims.py | 64bb2c6ad1e0 | 9388 |
| EXPERIMENTS/029-need-build-match/stats.py | 0520a4e0e3e5 | 12881 |
| EXPERIMENTS/README.md | 9ba4177b1516 | 5151 |
| vendor/MANIFEST.md | ffb2167f0e7d | 6437 |
| EXPERIMENTS/029-need-build-match/verify_chronology.py | 363249963842 | 4954 |
| EXPERIMENTS/029-need-build-match/raw/chronology_verification.jsonl | 155502228961 | 4138 |
| EXPERIMENTS/029-need-build-match/README.md | cb33929d675c | 9046 |
| EXPERIMENTS/029-need-build-match/results.json | 26135383f6a6 | 14299 |
| EXPERIMENTS/029-need-build-match/raw/labels_r1.tsv | b8f419084bd6 | 22869 |
| EXPERIMENTS/029-need-build-match/raw/labels_r2.tsv | 7d9199f464d8 | 21725 |
| EXPERIMENTS/029-need-build-match/raw/view_r1.txt | ee2d4b0c2fcb | 138017 |
| EXPERIMENTS/029-need-build-match/raw/view_r2.txt | ee2d4b0c2fcb | 138017 |
| FAILURES-findings-20.md | 04c31b02cf89 | 10388 |
| FAILURES.md | ccd42e0d4efb | 17786 |
| DECISIONS-SCREENING-4.md | 0b25d47ae1ea | 8717 |
| DECISIONS.md | 976754534199 | 8576 |
| STATE.md | cbda63a7299e | 33592 |
| STATE-next-actions.md | 33dd8fba6bc0 | 21048 |
| STATE-constraints.md | 9a210d452816 | 13250 |
| ROADMAP.md | f764a130b266 | 20383 |
| EXPERIMENTS/029-need-build-match/superseded/labels_r1.tsv | 54a3c72b14c8 | 26209 |
| EXPERIMENTS/029-need-build-match/superseded/labels_r1_final.tsv | a593678ef24e | 3046 |
| EXPERIMENTS/029-need-build-match/superseded/labels_r1_x.tsv | fb4c11124723 | 8508 |
| EXPERIMENTS/029-need-build-match/superseded/labels_r2.tsv | 7a5bd5c31b86 | 23413 |
| EXPERIMENTS/029-need-build-match/superseded/labels_r2_final.tsv | 6fdd050f2746 | 3066 |
| EXPERIMENTS/029-need-build-match/superseded/labels_r2_firstpass_4_duplicates.tsv | da6798f73d02 | 25657 |
| EXPERIMENTS/029-need-build-match/superseded/labels_r2_x.tsv | 63f286b3fac4 | 9290 |
| EXPERIMENTS/029-need-build-match/superseded/view_key.json | 866e4c73c7cd | 21835 |
| EXPERIMENTS/029-need-build-match/superseded/view_r1.txt | 178827b1b12a | 138017 |
| EXPERIMENTS/029-need-build-match/superseded/view_r1_xonly.txt | a518d8ccd34b | 57643 |
| EXPERIMENTS/029-need-build-match/superseded/view_r2.txt | 178827b1b12a | 138017 |
| EXPERIMENTS/029-need-build-match/superseded/view_r2_xonly.txt | a518d8ccd34b | 57643 |

## Commands

18 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/029-need-build-match/build_population.py'] | 0 | 488 |
| 6 | ['python3', 'EXPERIMENTS/029-need-build-match/fetch_builds.py'] | 0 | 548256 |
| 7 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 1 | 106 |
| 8 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 1 | 114 |
| 9 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 0 | 192 |
| 25 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 0 | 192 |
| 35 | ['python3', 'EXPERIMENTS/029-need-build-match/repair_reader_ids.py'] | 0 | 115 |
| 36 | ['python3', 'EXPERIMENTS/029-need-build-match/assemble_labels.py'] | 0 | 99 |
| 37 | ['python3', 'EXPERIMENTS/029-need-build-match/stats.py'] | 1 | 848 |
| 38 | ['python3', 'EXPERIMENTS/029-need-build-match/stats.py'] | 0 | 181 |
| 39 | ['python3', 'EXPERIMENTS/029-need-build-match/make_reader_views.py'] | 0 | 115 |
| 50 | ['python3', 'EXPERIMENTS/029-need-build-match/verify_chronology.py'] | 0 | 23461 |
| 54 | ['python3', 'EXPERIMENTS/029-need-build-match/stats.py'] | 0 | 192 |
| 55 | ['python3', 'EXPERIMENTS/029-need-build-match/stats.py'] | 0 | 209 |
| 56 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 487918 |
| 57 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'EXPERIMENTS/029-need-build-match', '-p', 'test_*.py', '-t', 'EXPERIM | 0 | 2011 |
| 58 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 913611 |
| 59 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 852798 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 3 |
| redactions applied to command output | 0 |
|   error | declared artifact no longer exists: EXPERIMENTS/029-need-build-match/assemble_labels.py |
|   error | declared artifact no longer exists: EXPERIMENTS/029-need-build-match/raw/view_r1_xonly.txt |
|   error | declared artifact no longer exists: EXPERIMENTS/029-need-build-match/raw/view_r2_xonly.txt |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 20:13:48 | session_start | Measure whether the 278 need-staters who shipped something shipped the thing they said was missing, against mismatched and thread-title controls |
| 2 | 20:15:36 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL.md |
| 3 | 20:15:37 | artifact | wrote EXPERIMENTS/029-need-build-match/RUBRIC.md |
| 4 | 20:15:37 | milestone | E029 protocol and reader rubric declared before any fetch |
| 5 | 20:16:22 | command | $ python3 EXPERIMENTS/029-need-build-match/build_population.py |
| 6 | 20:26:06 | command | $ python3 EXPERIMENTS/029-need-build-match/fetch_builds.py |
| 7 | 20:27:57 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 8 | 20:28:18 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 9 | 20:29:16 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 10 | 20:29:38 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md |
| 11 | 20:29:39 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-1.md |
| 12 | 20:29:39 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL.md |
| 13 | 20:29:39 | artifact | wrote EXPERIMENTS/029-need-build-match/RUBRIC.md |
| 14 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/build_population.py |
| 15 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/fetch_builds.py |
| 16 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 17 | 20:29:40 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/builds.jsonl |
| 18 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/gate_a2_controls.jsonl |
| 19 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/population.jsonl |
| 20 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/stories.jsonl |
| 21 | 20:29:41 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_key.json |
| 22 | 20:29:42 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r1.txt |
| 23 | 20:29:42 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r2.txt |
| 24 | 20:29:43 | milestone | E029 population built (241 -> 74 causally eligible), fetched, and two blind reader views written |
| 25 | 20:38:41 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 26 | 20:42:52 | milestone | mismatched-arm defect found by a test (45 of 74 rows rendered empty), repaired, X labels discarded, re-read launched |
| 27 | 20:43:06 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-2.md |
| 28 | 20:43:07 | artifact | wrote EXPERIMENTS/029-need-build-match/assemble_labels.py |
| 29 | 20:43:08 | artifact | wrote EXPERIMENTS/029-need-build-match/stats.py |
| 30 | 20:43:08 | artifact | wrote EXPERIMENTS/029-need-build-match/test_claims.py |
| 31 | 20:43:09 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r1_v1.txt |
| 32 | 20:43:11 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r2_v1.txt |
| 33 | 20:43:13 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r1_xonly.txt |
| 34 | 20:43:13 | artifact | wrote EXPERIMENTS/029-need-build-match/raw/view_r2_xonly.txt |
| 35 | 20:45:12 | command | $ python3 EXPERIMENTS/029-need-build-match/repair_reader_ids.py |
| 36 | 20:45:13 | command | $ python3 EXPERIMENTS/029-need-build-match/assemble_labels.py |
| 37 | 20:45:20 | command | $ python3 EXPERIMENTS/029-need-build-match/stats.py |
| 38 | 20:45:38 | command | $ python3 EXPERIMENTS/029-need-build-match/stats.py |
| 39 | 20:48:14 | command | $ python3 EXPERIMENTS/029-need-build-match/make_reader_views.py |
| 40 | 20:56:53 | artifact | wrote EXPERIMENTS/029-need-build-match/PROTOCOL-AMENDMENT-3.md |
| 89 | 21:56:17 | task_rewrite | appended a complete record for T-0073 |
| 90 | 21:56:52 | integrity_error | declared artifact no longer exists: EXPERIMENTS/029-need-build-match/assemble_labels.py |
| 91 | 21:56:52 | integrity_error | declared artifact no longer exists: EXPERIMENTS/029-need-build-match/raw/view_r1_xonly.txt |
| 92 | 21:56:52 | integrity_error | declared artifact no longer exists: EXPERIMENTS/029-need-build-match/raw/view_r2_xonly.txt |
| 93 | 21:56:52 | doc_update | updated DECISIONS-SCREENING-4.md |
| 94 | 21:56:52 | doc_update | updated DECISIONS.md |
| 95 | 21:56:52 | doc_update | updated FAILURES.md |
| 96 | 21:56:52 | doc_update | updated ROADMAP.md |
| 97 | 21:56:52 | doc_update | updated STATE.md |
| 98 | 21:56:53 | session_end | Chose the one join nobody had made in the demand-side corpus and ran it end to end. The fetch alone produced the durable result: of 241 need-staters w |

_48 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-019-measure-whether-the-278-need-staters-who/events.jsonl
```
