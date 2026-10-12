# Session 2026-10-12-002-measure-whether-a-free-general-assistant

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T01:42:43+00:00
- **Duration:** 3060.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure whether a free general assistant's answers to real-document questions contain values absent from the source, with a programmatic grounding checker as the instrument

## Summary

E114 ran the prototype-first route end to end and closed the value-grounding line. A free general assistant read five real Federal Register final rules in full and answered for every dollar amount, date and citation: 0 of 374 values fabricated, Wilson 95% upper bound 0.0098 against a declared 2% kill gate, so the widely repeated claim that models invent numbers when reading a document is withdrawn for this population. The verifier built to catch them is what failed - it passed recall 1.0000 on corrupted answers (22/22, both flavours) and 0.0069 false alarms on verbatim document spans, then flagged 0.3717 of real values with a false-positive rate of 1.00: 24 of 24 ungrounded_value verdicts have every digit group and token present in the document, and 50 of 50 hand-read ungrounded_claim flags are correct. Both controls were too easy; faithful paraphrase with nothing invented was the arm never built. F118 and D106 record it. Landing also surfaced a three-way identifier collision with another VM (two Docker Hub runs under E108 with opposite signs, plus E110), resolved by renumbering the unpushed side to E112/E113 and recorded as F117. doc lint was red on work landed from another session; repaired at the invariant and now exits 0. 836 tests green.

## Next

Reopen the verifier line only by building the arm this run never had: a faithful-paraphrase positive control whose values are all correct and differently worded, and measure the false-positive rate of an LLM-based paraphrase step against it. That number is the only thing standing between E114's dead checker and a working attestation, and it is cheap to get wrong - so write the control first, from documents and not from the treatment arm.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/114-value-grounding/AMENDMENT-1.md | 6d172518724b | 2031 |
| EXPERIMENTS/114-value-grounding/AMENDMENT-2.md | 4cf3ea6502f9 | 2920 |
| EXPERIMENTS/114-value-grounding/PROTOCOL.md | 3e89f5950403 | 4920 |
| EXPERIMENTS/114-value-grounding/RESULT.md | 594a24ee7098 | 5678 |
| EXPERIMENTS/114-value-grounding/answers.jsonl | 31c818621c1e | 17416 |
| EXPERIMENTS/114-value-grounding/checked-controls-v1.jsonl | 7a16e0ef0dae | 121776 |
| EXPERIMENTS/114-value-grounding/checked-v0.jsonl | a75256f01b2e | 100925 |
| EXPERIMENTS/114-value-grounding/checked.jsonl | d3dd05a9c902 | 47973 |
| EXPERIMENTS/114-value-grounding/controls-checked.jsonl | 6511f048f77f | 119397 |
| EXPERIMENTS/114-value-grounding/controls.jsonl | 14f88ea87737 | 47111 |
| EXPERIMENTS/114-value-grounding/controls.py | f11fc25224f1 | 6415 |
| EXPERIMENTS/114-value-grounding/fetch.py | eb3e442e54c3 | 4294 |
| EXPERIMENTS/114-value-grounding/flags-verified.jsonl | 6386747844ee | 2770 |
| EXPERIMENTS/114-value-grounding/gates.json | 505b2568664f | 32668 |
| EXPERIMENTS/114-value-grounding/ground.py | 9b3c0c84afbc | 9878 |
| EXPERIMENTS/114-value-grounding/sample-flagged.json | 6d2f0582cbf5 | 28718 |
| EXPERIMENTS/114-value-grounding/score.py | a1632741c26d | 4409 |
| EXPERIMENTS/114-value-grounding/verify_flags.py | 61d1ddeaca33 | 2287 |
| STATE.md | edd9e439c273 | 28041 |
| tools/viewcount_core.py | 2c8089a16780 | 9377 |
| tools/viewcount_cli.py | 5b16c5ce1e4d | 7597 |
| DECISIONS-SCREENING-19.md | d600fae11101 | 6037 |
| tools/originlib/paths.py | 981ba9943b6a | 4558 |
| tools/originlib/reconcile.py | 713640813f63 | 8750 |
| tests/test_decision_files.py | 0cfc064c88be | 5565 |
| EXPERIMENTS/0xx-viewcount-prototype/vocabulary.py | 0dc2c587955e | 1990 |
| EXPERIMENTS/105-viewcount-synthesis/analysers.py | b824f140b1fc | 13991 |
| FAILURES.md | cd552416ce2a | 74205 |
| FAILURES-findings-39.md | 51f98e5e2f2e | 10041 |
| DECISIONS.md | 3f492b8d2f04 | 22259 |
| STATE-next-actions.md | 2b65523f9fef | 30014 |

## Commands

8 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['git', 'add', '-A'] | 0 | 192 |
| 3 | ['git', 'commit', '-q', '-m', "Renumber the unpushed D083 experiments to E112/E113 after landing a three-way identifier collision with E108/E110\n\nsy | 0 | 103 |
| 5 | ['python3', 'EXPERIMENTS/114-value-grounding/fetch.py', '30'] | 0 | 22090 |
| 7 | ['python3', 'EXPERIMENTS/114-value-grounding/ground.py', 'EXPERIMENTS/114-value-grounding/raw', 'EXPERIMENTS/114-value-grounding/answers.jsonl', '0.6' | 0 | 224 |
| 8 | ['python3', 'EXPERIMENTS/114-value-grounding/ground.py', 'EXPERIMENTS/114-value-grounding/raw', 'EXPERIMENTS/114-value-grounding/answers.jsonl', '0.6' | 0 | 380 |
| 9 | ['python3', 'EXPERIMENTS/114-value-grounding/ground.py', 'EXPERIMENTS/114-value-grounding/raw', 'EXPERIMENTS/114-value-grounding/answers.jsonl', '0.6' | 0 | 386 |
| 10 | ['python3', 'EXPERIMENTS/114-value-grounding/ground.py', 'EXPERIMENTS/114-value-grounding/raw', 'EXPERIMENTS/114-value-grounding/answers.jsonl', '0.6' | 0 | 686 |
| 11 | ['python3', 'EXPERIMENTS/114-value-grounding/verify_flags.py'] | 0 | 122 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 44 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-PYTESTIVE-SUMMARY.md |
|   undeclared | DECISIONS-SCREENING-18.md |
|   undeclared | EXPERIMENTS/092-viewcount-maven/README.md |
|   undeclared | EXPERIMENTS/093-viewcount-docker/README.md |
|   undeclared | EXPERIMENTS/094-viewcount-kubernetes/README.md |
|   undeclared | EXPERIMENTS/095-viewcount-discussions/README.md |
|   undeclared | EXPERIMENTS/096-viewcount-aws/README.md |
|   undeclared | EXPERIMENTS/097-pyproject-toml/README.md |
|   undeclared | EXPERIMENTS/098-viewcount-sf/README.md |
|   undeclared | EXPERIMENTS/099-viewcount-superuser/README.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 01:42:43 | session_start | Measure whether a free general assistant's answers to real-document questions contain values absent from the source, with a programmatic grounding che |
| 2 | 01:44:19 | command | $ git add -A |
| 3 | 01:44:20 | command | $ git commit -q -m Renumber the unpushed D083 experiments to E112/E113 after landing a three-way identifier collision with E108/E110  sync lan |
| 4 | 01:44:37 | milestone | landed the E112/E113 renumbering and F117; starting the value-grounding experiment |
| 5 | 01:46:35 | command | $ python3 EXPERIMENTS/114-value-grounding/fetch.py 30 |
| 6 | 01:48:13 | milestone | arm A answers written and committed for 5 documents (15 triples) before any checker code exists |
| 7 | 01:51:29 | command | $ python3 EXPERIMENTS/114-value-grounding/ground.py EXPERIMENTS/114-value-grounding/raw EXPERIMENTS/114-value-grounding/answers.jsonl 0.6 chec |
| 8 | 01:52:18 | command | $ python3 EXPERIMENTS/114-value-grounding/ground.py EXPERIMENTS/114-value-grounding/raw EXPERIMENTS/114-value-grounding/answers.jsonl 0.6 chec |
| 9 | 01:52:45 | command | $ python3 EXPERIMENTS/114-value-grounding/ground.py EXPERIMENTS/114-value-grounding/raw EXPERIMENTS/114-value-grounding/answers.jsonl 0.6 chec |
| 10 | 01:53:07 | command | $ python3 EXPERIMENTS/114-value-grounding/ground.py EXPERIMENTS/114-value-grounding/raw EXPERIMENTS/114-value-grounding/answers.jsonl 0.6 chec |
| 11 | 01:54:10 | command | $ python3 EXPERIMENTS/114-value-grounding/verify_flags.py |
| 12 | 01:54:49 | artifact | wrote EXPERIMENTS/114-value-grounding/AMENDMENT-1.md |
| 13 | 01:54:51 | artifact | wrote EXPERIMENTS/114-value-grounding/AMENDMENT-2.md |
| 14 | 01:54:52 | artifact | wrote EXPERIMENTS/114-value-grounding/PROTOCOL.md |
| 15 | 01:54:53 | artifact | wrote EXPERIMENTS/114-value-grounding/RESULT.md |
| 16 | 01:54:57 | artifact | wrote EXPERIMENTS/114-value-grounding/answers.jsonl |
| 17 | 01:54:58 | artifact | wrote EXPERIMENTS/114-value-grounding/checked-controls-v1.jsonl |
| 18 | 01:55:00 | artifact | wrote EXPERIMENTS/114-value-grounding/checked-v0.jsonl |
| 19 | 01:55:01 | artifact | wrote EXPERIMENTS/114-value-grounding/checked.jsonl |
| 20 | 01:55:02 | artifact | wrote EXPERIMENTS/114-value-grounding/controls-checked.jsonl |
| 21 | 01:55:03 | artifact | wrote EXPERIMENTS/114-value-grounding/controls.jsonl |
| 22 | 01:55:05 | artifact | wrote EXPERIMENTS/114-value-grounding/controls.py |
| 23 | 01:55:06 | artifact | wrote EXPERIMENTS/114-value-grounding/fetch.py |
| 24 | 01:55:07 | artifact | wrote EXPERIMENTS/114-value-grounding/flags-verified.jsonl |
| 25 | 01:55:09 | artifact | wrote EXPERIMENTS/114-value-grounding/gates.json |
| 26 | 01:55:10 | artifact | wrote EXPERIMENTS/114-value-grounding/ground.py |
| 27 | 01:55:11 | artifact | wrote EXPERIMENTS/114-value-grounding/sample-flagged.json |
| 28 | 01:55:12 | artifact | wrote EXPERIMENTS/114-value-grounding/score.py |
| 29 | 01:55:14 | artifact | wrote EXPERIMENTS/114-value-grounding/verify_flags.py |
| 30 | 01:55:15 | artifact | wrote STATE.md |
| 31 | 01:55:16 | milestone | E114 complete: KG-A 0/374, verifier FP rate 1.00; writing records |
| 32 | 02:33:18 | decision | E114's value-grounding line closes on the verifier, not the subject: the checker passed recall 1.0000 and 0.0069 false alarms on its declared controls |
| 33 | 02:33:20 | artifact | wrote tools/viewcount_core.py |
| 34 | 02:33:21 | artifact | wrote tools/viewcount_cli.py |
| 35 | 02:33:22 | artifact | wrote DECISIONS-SCREENING-19.md |
| 36 | 02:33:24 | artifact | wrote tools/originlib/paths.py |
| 37 | 02:33:25 | artifact | wrote tools/originlib/reconcile.py |
| 38 | 02:33:26 | artifact | wrote tests/test_decision_files.py |
| 39 | 02:33:27 | artifact | wrote EXPERIMENTS/0xx-viewcount-prototype/vocabulary.py |
| 40 | 02:33:28 | artifact | wrote EXPERIMENTS/105-viewcount-synthesis/analysers.py |
| 87 | 02:33:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/113-viewcount-matched-harvest/stratified.json |
| 88 | 02:33:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/113-viewcount-matched-harvest/stratified.py |
| 89 | 02:33:43 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-results.md |
| 90 | 02:33:43 | doc_update | updated DECISIONS-PYTESTIVE-SUMMARY.md |
| 91 | 02:33:43 | doc_update | updated DECISIONS-SCREENING-18.md |
| 92 | 02:33:43 | doc_update | updated DECISIONS-SCREENING-19.md |
| 93 | 02:33:43 | doc_update | updated DECISIONS.md |
| 94 | 02:33:43 | doc_update | updated FAILURES.md |
| 95 | 02:33:43 | doc_update | updated STATE.md |
| 96 | 02:33:43 | session_end | E114 ran the prototype-first route end to end and closed the value-grounding line. A free general assistant read five real Federal Register final rule |

_46 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-002-measure-whether-a-free-general-assistant/events.jsonl
```
