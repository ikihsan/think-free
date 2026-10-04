# Session 2026-10-04-050-test-whether-a-live-corpus-of-practition

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T20:41:03+00:00
- **Duration:** 182.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test whether a live corpus of practitioner needs generates candidates, and screen the answer against the mission's own records

## Summary

Tested D048's invention seat rather than filling it. A live corpus of 1401 practitioner need statements (Hacker News, since 2024-01-01) was harvested, 50 drawn by a stated rule so none was picked for looking promising, and 0 survived the screens: 38% prior art, 30% no mechanism, 24% not software needs, 8% needing hardware -- against the prior generator's own 3 of 16, none validated. F029, D049. The generator is refuted; the corpus is kept demoted to problem statements, because it cannot supply the one signal that matters: recurrence, where term frequency over 1273 clauses returns only function words. The constructive half: counted by repository the same cluster gives 5805 open issues across 28 repositories, so the missing input is obtainable. F030: one search query decides a prior-art verdict wrongly in both directions -- 502 hits that were awesome-go through in:readme, and 0 hits for an idea with 29-83 repositories behind it. The screening was falsified against itself: 10 of 19 prior-art verdicts re-checked, 6 supported, 4 unverified, and reversing all four still yields no survivor. Also repaired AGENTS.md, which told every agent to run a suite command that fails all 42 modules with ModuleNotFoundError. 588 tests pass, doc lint exits 0. Cost: a concurrent instance of session 044 closed that stream mid-session, so this work's commits predate this record; and the other VM took F025-F028 and EXPERIMENTS/011 first, so this side renumbered to F029/F030/F031 and experiment 012 on the unpushed side.

## Next

Build the repository-signal recurrence filter and re-harvest through it: count distinct repositories above a star threshold rather than raw issue counts, which are full-text self-selection and overstated the cluster badly. Then test the cluster with the strongest measured recurrence -- changes a coding agent makes that nobody asked for -- against its own stated falsification. Its cheap local corpus is this repository's own 375 commits with their task and session requirements, which also answers whether the repo's 22 recorded defects are instances of it. Alternative if that is blocked: STATE.md records the selection procedure itself as the suspect (twelve candidates, twelve prior-art deaths), and which axis replaces novelty is an owner decision, not a tooling one.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/012-candidate-harvest/README.md | 700e644d0f15 | 5527 |
| FAILURES-findings-9.md | 98552a920c44 | 6721 |
| FAILURES-findings-10.md | 44aa74bb472f | 3982 |
| FAILURES-findings-8.md | 07ad9997c24e | 4674 |
| FAILURES.md | 257029465704 | 7156 |
| DECISIONS-SCREENING.md | 59bc71ee8fa8 | 13331 |
| DECISIONS.md | feccf3c388ee | 6664 |
| STATE.md | acd556ef6ece | 26318 |
| STATE-next-actions.md | e18b3bc026f8 | 21669 |
| AGENTS.md | ab14d4be2b12 | 8293 |
| tests/README.md | 059763dbd0da | 30561 |
| EXPERIMENTS/012-candidate-harvest/harvest_needs.py | 438a9ca616ab | 2471 |
| EXPERIMENTS/012-candidate-harvest/sample_needs.py | 038e2483b0cd | 2592 |
| EXPERIMENTS/012-candidate-harvest/screen_sample.py | 599a06d355d3 | 6880 |
| EXPERIMENTS/012-candidate-harvest/prior_art_probe.py | a1cdc14887e9 | 4405 |
| EXPERIMENTS/012-candidate-harvest/prior_art_probe2.py | 84b7e98df7db | 3770 |
| EXPERIMENTS/012-candidate-harvest/recurrence_probe.py | f510bb2040fa | 3626 |
| EXPERIMENTS/012-candidate-harvest/verify_prior_art.py | 1a86915e558a | 4890 |
| EXPERIMENTS/012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl | c485f7f63892 | 929251 |
| EXPERIMENTS/012-candidate-harvest/raw/sample.jsonl | 2325a5023126 | 33230 |
| EXPERIMENTS/012-candidate-harvest/raw/screened.jsonl | b6c09470eb25 | 38918 |
| EXPERIMENTS/012-candidate-harvest/raw/prior_art_probe.json | 144dac9d74ed | 5714 |
| EXPERIMENTS/012-candidate-harvest/raw/prior_art_probe2.json | 2c000de082fb | 8186 |
| EXPERIMENTS/012-candidate-harvest/raw/recurrence_probe.json | 9982b55bffe0 | 2404 |
| EXPERIMENTS/012-candidate-harvest/raw/verify_prior_art.json | 89afd910e979 | 7037 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 3 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/011-candidate-harvest/README.md |
|   error | DECISIONS.md was not updated although the session recorded decision |
|   error | FAILURES.md was not updated although the session recorded experiment_result |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 20:41:03 | session_start | Test whether a live corpus of practitioner needs generates candidates, and screen the answer against the mission's own records |
| 2 | 20:41:19 | decision | The commits for this work predate this session's record: a concurrent instance of session 044 closed that stream at seq 20 while this work was in prog |
| 3 | 20:41:20 | decision | A need statement is not a candidate, and the pipeline's missing input is recurrence counted by repository (F029, D049): 0 of 50 mechanically drawn nee |
| 4 | 20:41:20 | decision | A prior-art verdict needs more than one phrasing on more than one corpus, with the phrasings written down; one query returned 502 irrelevant hits and  |
| 5 | 20:41:21 | experiment_result | kill gate declared before the sample was drawn and not met: 0 of 50 harvested need statements survived the screens; the generator is refuted and the c |
| 6 | 20:41:35 | artifact | wrote EXPERIMENTS/012-candidate-harvest/README.md |
| 7 | 20:41:41 | artifact | wrote FAILURES-findings-9.md |
| 8 | 20:41:42 | artifact | wrote FAILURES-findings-10.md |
| 9 | 20:41:42 | artifact | wrote FAILURES-findings-8.md |
| 10 | 20:41:43 | artifact | wrote FAILURES.md |
| 11 | 20:41:44 | artifact | wrote DECISIONS-SCREENING.md |
| 12 | 20:41:44 | artifact | wrote DECISIONS.md |
| 13 | 20:41:45 | artifact | wrote STATE.md |
| 14 | 20:41:45 | artifact | wrote STATE-next-actions.md |
| 15 | 20:41:46 | artifact | wrote AGENTS.md |
| 16 | 20:41:47 | artifact | wrote tests/README.md |
| 17 | 20:41:47 | milestone | E012 landed and pushed: 0 of 50 needs survived; F029, F030, D049 recorded; identifier collisions renumbered on the unpushed side |
| 18 | 20:43:25 | artifact | wrote EXPERIMENTS/012-candidate-harvest/harvest_needs.py |
| 19 | 20:43:25 | artifact | wrote EXPERIMENTS/012-candidate-harvest/sample_needs.py |
| 20 | 20:43:26 | artifact | wrote EXPERIMENTS/012-candidate-harvest/screen_sample.py |
| 21 | 20:43:27 | artifact | wrote EXPERIMENTS/012-candidate-harvest/prior_art_probe.py |
| 22 | 20:43:27 | artifact | wrote EXPERIMENTS/012-candidate-harvest/prior_art_probe2.py |
| 23 | 20:43:28 | artifact | wrote EXPERIMENTS/012-candidate-harvest/recurrence_probe.py |
| 24 | 20:43:28 | artifact | wrote EXPERIMENTS/012-candidate-harvest/verify_prior_art.py |
| 25 | 20:43:30 | artifact | wrote EXPERIMENTS/012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl |
| 26 | 20:43:30 | artifact | wrote EXPERIMENTS/012-candidate-harvest/raw/sample.jsonl |
| 27 | 20:43:31 | artifact | wrote EXPERIMENTS/012-candidate-harvest/raw/screened.jsonl |
| 28 | 20:43:31 | artifact | wrote EXPERIMENTS/012-candidate-harvest/raw/prior_art_probe.json |
| 29 | 20:43:32 | artifact | wrote EXPERIMENTS/012-candidate-harvest/raw/prior_art_probe2.json |
| 30 | 20:43:32 | artifact | wrote EXPERIMENTS/012-candidate-harvest/raw/recurrence_probe.json |
| 31 | 20:43:33 | artifact | wrote EXPERIMENTS/012-candidate-harvest/raw/verify_prior_art.json |
| 32 | 20:43:34 | milestone | consolidated E012 into one directory after the renumbering left two indexed copies |
| 33 | 20:44:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/011-candidate-harvest/README.md |
| 34 | 20:44:05 | integrity_error | DECISIONS.md was not updated although the session recorded decision |
| 35 | 20:44:05 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 36 | 20:44:05 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 37 | 20:44:05 | session_end | Tested D048's invention seat rather than filling it. A live corpus of 1401 practitioner need statements (Hacker News, since 2024-01-01) was harvested, |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-050-test-whether-a-live-corpus-of-practition/events.jsonl
```
