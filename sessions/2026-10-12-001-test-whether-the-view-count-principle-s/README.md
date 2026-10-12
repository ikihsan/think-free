# Session 2026-10-12-001-test-whether-the-view-count-principle-s

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode-space-bunny`
- **Started:** 2026-10-12T00:04:46+00:00
- **Duration:** 5088.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test whether the view-count principle's GitHub 'ALL GATES PASS' (E107, delta=0.826) survives a matched-harvest control, and decide the line on that measurement.

## Summary

E110 tested whether the view-count principle survives a matched harvest, and answered no. Reading committed bytes first: E107 drew its need arm from topic:web-framework and its random arm from topic:utils, both star-sorted, so its published Cliff's delta=0.826010 (reproduced exactly from its own data) compares the most-starred web frameworks to the most-starred utility libraries. Under a matched harvest on the same platform: within-stratum delta=+0.0746, stratified permutation p=0.183 over 20k iters, 5 of 7 strata negative or zero. A second defect is the binding obstacle: the shared classifier matches unanchored substrings (ai inside email, base inside database) and labels only 196 of 700 rows (28%), 458 matching neither vocabulary - so a 28 percent screen was reported as a 100 percent measurement, and no coverage gate existed on the line. G0 fired twice; AMENDMENT-2 and -3 record the substring bug, the vocabulary-nesting bug, and the one-word probe edit made after seeing it fail. E107's ALL GATES PASS withdrawn (F116, D105); E090/E095/E102/E103/E108 marked untested on a matched harvest, not confirmed; E109 (Pub.dev) marked superseded, never run. The screen is withdrawn, not the idea.

## Next

The line's binding obstacle is now named and is a buildable engineering problem, not a research one: a classifier that covers its population with a coverage floor declared before the run, a matched harvest as the default design, and a stratified reading beside the pooled one. If the mission wants a candidate rather than a repaired instrument, this line should stay closed and the next session should open a fresh observation in a domain chosen for a practical problem, not for platform coverage.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/110-viewcount-matched-harvest/PROTOCOL.md | 20fed4b53257 | 5880 |
| EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-1.md | e8b414351b61 | 2364 |
| EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-2.md | a1cc6ab01ca0 | 2996 |
| EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-3.md | 8c013e9f9e37 | 3507 |
| EXPERIMENTS/110-viewcount-matched-harvest/PROTOCOL.md | 20fed4b53257 | 5880 |
| EXPERIMENTS/110-viewcount-matched-harvest/README.md | 5122b0eb0878 | 5872 |
| EXPERIMENTS/110-viewcount-matched-harvest/analyze.py | ed4867a22a0b | 20208 |
| EXPERIMENTS/110-viewcount-matched-harvest/harvest.py | cd27a16da63e | 3551 |
| EXPERIMENTS/110-viewcount-matched-harvest/raw_pool.json | c4f041be62b1 | 453013 |
| EXPERIMENTS/110-viewcount-matched-harvest/results.json | 8f1ecc13b9d4 | 4525 |
| EXPERIMENTS/110-viewcount-matched-harvest/stratified.json | 1cbcd4bb8399 | 1076 |
| EXPERIMENTS/110-viewcount-matched-harvest/stratified.py | 6766e48bb0a6 | 5597 |
| EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-1.md | e8b414351b61 | 2364 |
| EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-2.md | a1cc6ab01ca0 | 2996 |
| EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-3.md | 8c013e9f9e37 | 3507 |
| EXPERIMENTS/110-viewcount-matched-harvest/PROTOCOL.md | 20fed4b53257 | 5880 |
| EXPERIMENTS/110-viewcount-matched-harvest/README.md | fd5a44b2c016 | 6340 |
| EXPERIMENTS/110-viewcount-matched-harvest/analyze.py | 8b574df9e98c | 12461 |
| EXPERIMENTS/110-viewcount-matched-harvest/harvest.py | cd27a16da63e | 3551 |
| EXPERIMENTS/110-viewcount-matched-harvest/labeling.py | 094dfa5670b8 | 7427 |
| EXPERIMENTS/110-viewcount-matched-harvest/raw_pool.json | c4f041be62b1 | 453013 |
| EXPERIMENTS/110-viewcount-matched-harvest/results.json | 3ffdfe6a0c81 | 9368 |
| EXPERIMENTS/110-viewcount-matched-harvest/stratified.json | 1cbcd4bb8399 | 1076 |
| EXPERIMENTS/110-viewcount-matched-harvest/stratified.py | 7267c2e4345d | 6582 |
| FAILURES-findings-39.md | c0b117cdbc98 | 4633 |
| FAILURES.md | 70eaae4ddd76 | 72846 |
| DECISIONS.md | c590a95f4b80 | 21267 |
| DECISIONS-SCREENING-18.md | c1d1f6eccea8 | 16528 |
| STATE.md | 69989dfa9e03 | 26885 |
| STATE-next-actions.md | b2edcc7111d8 | 27127 |
| EXPERIMENTS/100-lab-instrument-error-codes/README.md | b8d4b2fadc6c | 3777 |
| EXPERIMENTS/101-network-equipment-fault-codes/README.md | dbdbeb21de5f | 3559 |
| docs/INDEX.md | a3b3a6cc3ac9 | 48817 |
| STATE-next-actions.md | e79f9d364478 | 27736 |
| EXPERIMENTS/109-pubdev-viewcount/PROTOCOL.md | cc5c4f19a172 | 6724 |
| EXPERIMENTS/110-viewcount-matched-harvest/README.md | fd5a44b2c016 | 6340 |
| docs/INDEX.md | 952b0d7c2e16 | 48821 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-11-044-fresh-observation-test-view-count-princi/events.jsonl |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:04:46 | session_start | Test whether the view-count principle's GitHub 'ALL GATES PASS' (E107, delta=0.826) survives a matched-harvest control, and decide the line on that me |
| 2 | 00:05:40 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/PROTOCOL.md |
| 3 | 00:05:41 | milestone | E110 PROTOCOL.md declared before first fetch: matched-harvest control on E107's own platform, with age-controlled stars/year as the metric E107 never  |
| 4 | 00:15:57 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-1.md |
| 5 | 00:15:58 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-2.md |
| 6 | 00:15:59 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-3.md |
| 7 | 00:16:00 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/PROTOCOL.md |
| 8 | 00:16:01 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/README.md |
| 9 | 00:16:01 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/analyze.py |
| 10 | 00:16:02 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/harvest.py |
| 11 | 00:16:03 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/raw_pool.json |
| 12 | 00:16:04 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/results.json |
| 13 | 00:16:05 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/stratified.json |
| 14 | 00:16:06 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/stratified.py |
| 15 | 00:16:13 | milestone | E110 complete. Verdict: the view-count effect is a harvest artifact. E107 delta=0.826 reproduced exactly, collapses to +0.075 (stratified p=0.183) und |
| 16 | 00:16:27 | experiment_result | matched-harvest control of E107: effect is a harvest artifact, delta 0.826 to 0.075, stratified p=0.183; classifier coverage 28 percent |
| 17 | 01:25:31 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-1.md |
| 18 | 01:25:32 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-2.md |
| 19 | 01:25:32 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/AMENDMENT-3.md |
| 20 | 01:25:33 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/PROTOCOL.md |
| 21 | 01:25:34 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/README.md |
| 22 | 01:25:35 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/analyze.py |
| 23 | 01:25:35 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/harvest.py |
| 24 | 01:25:36 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/labeling.py |
| 25 | 01:25:38 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/raw_pool.json |
| 26 | 01:25:39 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/results.json |
| 27 | 01:25:39 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/stratified.json |
| 28 | 01:25:40 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/stratified.py |
| 29 | 01:25:41 | artifact | wrote FAILURES-findings-39.md |
| 30 | 01:25:43 | artifact | wrote FAILURES.md |
| 31 | 01:25:44 | artifact | wrote DECISIONS.md |
| 32 | 01:25:45 | artifact | wrote DECISIONS-SCREENING-18.md |
| 33 | 01:25:46 | artifact | wrote STATE.md |
| 34 | 01:25:47 | artifact | wrote STATE-next-actions.md |
| 35 | 01:25:49 | artifact | wrote EXPERIMENTS/100-lab-instrument-error-codes/README.md |
| 36 | 01:25:50 | artifact | wrote EXPERIMENTS/101-network-equipment-fault-codes/README.md |
| 37 | 01:25:51 | artifact | wrote docs/INDEX.md |
| 38 | 01:25:58 | decision | D105: the view-count domain sweep is STOPPED. E110's matched-harvest control of E107 shows the effect is a harvest artifact (delta 0.826 -> 0.075, str |
| 39 | 01:29:19 | artifact | wrote STATE-next-actions.md |
| 40 | 01:29:21 | artifact | wrote EXPERIMENTS/109-pubdev-viewcount/PROTOCOL.md |
| 41 | 01:29:22 | artifact | wrote EXPERIMENTS/110-viewcount-matched-harvest/README.md |
| 42 | 01:29:24 | artifact | wrote docs/INDEX.md |
| 43 | 01:29:25 | milestone | Records updated: F116 filed in FAILURES-findings-39.md, D105 in DECISIONS-SCREENING-18.md, STATE.md + STATE-next-actions.md carry the withdrawal, E109 |
| 44 | 01:29:34 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-044-fresh-observation-test-view-count-princi/events.jsonl |
| 45 | 01:29:34 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 46 | 01:29:35 | doc_update | updated DECISIONS-SCREENING-18.md |
| 47 | 01:29:35 | doc_update | updated DECISIONS.md |
| 48 | 01:29:35 | doc_update | updated FAILURES.md |
| 49 | 01:29:35 | doc_update | updated STATE.md |
| 50 | 01:29:35 | session_end | E110 tested whether the view-count principle survives a matched harvest, and answered no. Reading committed bytes first: E107 drew its need arm from t |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-001-test-whether-the-view-count-principle-s/events.jsonl
```
