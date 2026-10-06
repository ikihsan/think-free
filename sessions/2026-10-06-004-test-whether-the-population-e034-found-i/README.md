# Session 2026-10-06-004-test-whether-the-population-e034-found-i

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T06:31:15+00:00
- **Duration:** 2514.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test whether the population E034 found is reachable by the people who would act on it: enumerate the orderings the Stack Exchange UI actually offers, and measure whether the Unanswered surface -- the one the platform points answerers at -- is as blind to duplicates as Active.

## Summary

Ran E035, which replaced three sessions' worth of Stack Exchange rate measurement with a premise test. Four reads of E034's committed bytes cost zero quota and changed four things: the findability frame is falsified (duplicate rows in the tail are viewed MORE than their neighbours, median 251 against 193, at a median age of 8.49 years -- so this is an eight-year-old backlog, not a rescue); the Active and tail arms do not intersect for two of eight tags, so the 4.5x is about membership; no Stack Overflow page offers the ordering, read off 409,639 bytes of first-party rendered HTML with zero occurrences of order=asc, oldest or ascending; and D6's declared remedy, which item 0e ranked the mission's top action, was aimed at a constraint that was not binding, since between-tag excess variance inside stackoverflow alone equals the pooled figure. E035's own gates did not close it either: /questions/unanswered excludes the population by definition (0 of 224 known duplicate-closed ids, while 98 of 186 tail duplicates meet its advertised is_answered==false criterion), so the overlap gate's firing was definitional and its declared branch was not taken (D065), and the density gate is not_evaluated rather than zero because closed_reason is unreadable on that route and custom filters are refused unauthenticated. A prototype reader runs offline on committed bytes. 799 tests green, doc lint, preflight and release check OK.

## Next

Test the one alternative this line never measured: whether Stack Overflow's own search already returns the backlog. /search/advanced and /search/excerpts are reachable from this host while every stackoverflow.com page is not, they accept hasaccepted=no, and search is what a person with a problem actually types into. The tail's rate is already measured at 0.1653 CI95 [0.1448, 0.1882], so the question is not whether the backlog is dense but whether a good query already returns it. If it does, the candidate dies to the platform's own search, which is the kill worth having before anything is built. A quota reset also reopens U2, which needs an API key for the label rather than more requests.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/035-unanswered-surface/README.md | fe30f3418940 | 10082 |
| EXPERIMENTS/035-unanswered-surface/PROTOCOL.md | 94e4133bf781 | 16557 |
| EXPERIMENTS/035-unanswered-surface/raw/tally.json | 771a5f27da88 | 4842 |
| EXPERIMENTS/035-unanswered-surface/raw/u1.jsonl | ab23dc2767a9 | 1052590 |
| FAILURES-findings-23.md | 9de3ea7755ce | 11486 |
| DECISIONS-SCREENING-6.md | c2ebcc0989a7 | 8266 |
| STATE.md | 7817249a4fb8 | 34558 |
| STATE-next-actions.md | d097c5981496 | 21352 |
| STATE-in-flight-2.md | 7d39d2da9532 | 13625 |
| STATE-in-flight-3.md | 3de9e26baf7e | 8650 |

## Commands

6 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/035-unanswered-surface/harvest.py', '--pages', '3'] | 0 | 18413 |
| 3 | ['python3', 'EXPERIMENTS/035-unanswered-surface/tally.py'] | 0 | 340 |
| 4 | ['python3', 'EXPERIMENTS/035-unanswered-surface/harvest.py', '--attempt', '2', '--pages', '3'] | 0 | 3983 |
| 5 | ['python3', 'EXPERIMENTS/035-unanswered-surface/relabel.py'] | 0 | 634 |
| 6 | ['python3', 'EXPERIMENTS/035-unanswered-surface/relabel.py'] | 0 | 19346 |
| 7 | ['python3', 'EXPERIMENTS/035-unanswered-surface/tally.py'] | 0 | 364 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 16 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/035-unanswered-surface/analyse.py |
|   undeclared | EXPERIMENTS/035-unanswered-surface/harvest.py |
|   undeclared | EXPERIMENTS/035-unanswered-surface/raw/attempts1.json |
|   undeclared | EXPERIMENTS/035-unanswered-surface/raw/attempts2.json |
|   undeclared | EXPERIMENTS/035-unanswered-surface/raw/pages1.jsonl |
|   undeclared | EXPERIMENTS/035-unanswered-surface/raw/pages2.jsonl |
|   undeclared | EXPERIMENTS/035-unanswered-surface/raw/relabel.jsonl |
|   undeclared | EXPERIMENTS/035-unanswered-surface/raw/relabel_attempts.json |
|   undeclared | EXPERIMENTS/035-unanswered-surface/raw/u2.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 06:31:15 | session_start | Test whether the population E034 found is reachable by the people who would act on it: enumerate the orderings the Stack Exchange UI actually offers,  |
| 2 | 06:35:43 | command | $ python3 EXPERIMENTS/035-unanswered-surface/harvest.py --pages 3 |
| 3 | 06:35:59 | command | $ python3 EXPERIMENTS/035-unanswered-surface/tally.py |
| 4 | 06:36:54 | command | $ python3 EXPERIMENTS/035-unanswered-surface/harvest.py --attempt 2 --pages 3 |
| 5 | 06:38:14 | command | $ python3 EXPERIMENTS/035-unanswered-surface/relabel.py |
| 6 | 06:38:57 | command | $ python3 EXPERIMENTS/035-unanswered-surface/relabel.py |
| 7 | 06:40:32 | command | $ python3 EXPERIMENTS/035-unanswered-surface/tally.py |
| 8 | 07:11:26 | task_rewrite | appended a create record for T-0079 |
| 9 | 07:11:34 | milestone | E035 declared, fetched, tallied: F058, D065, T-0079; prototype runs offline on committed bytes |
| 10 | 07:12:09 | task_rewrite | rewrote tasks/T-0079-e035-establish-whether-the-score-tail-population.md (status: claimed) |
| 11 | 07:12:09 | task_rewrite | appended a claim record for T-0079 |
| 12 | 07:12:38 | task_rewrite | rewrote tasks/T-0079-e035-establish-whether-the-score-tail-population.md (status: done) |
| 13 | 07:12:38 | task_rewrite | appended a complete record for T-0079 |
| 14 | 07:12:44 | artifact | wrote EXPERIMENTS/035-unanswered-surface/README.md |
| 15 | 07:12:45 | artifact | wrote EXPERIMENTS/035-unanswered-surface/PROTOCOL.md |
| 16 | 07:12:46 | artifact | wrote EXPERIMENTS/035-unanswered-surface/raw/tally.json |
| 17 | 07:12:47 | artifact | wrote EXPERIMENTS/035-unanswered-surface/raw/u1.jsonl |
| 18 | 07:12:48 | artifact | wrote FAILURES-findings-23.md |
| 19 | 07:12:48 | artifact | wrote DECISIONS-SCREENING-6.md |
| 20 | 07:12:49 | artifact | wrote STATE.md |
| 21 | 07:12:49 | artifact | wrote STATE-next-actions.md |
| 22 | 07:12:50 | artifact | wrote STATE-in-flight-2.md |
| 23 | 07:12:51 | artifact | wrote STATE-in-flight-3.md |
| 24 | 07:13:09 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 25 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/analyse.py |
| 26 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/harvest.py |
| 27 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/attempts1.json |
| 28 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/attempts2.json |
| 29 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/pages1.jsonl |
| 30 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/pages2.jsonl |
| 31 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/relabel.jsonl |
| 32 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/relabel_attempts.json |
| 33 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/u2.jsonl |
| 34 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/raw/u_labelled.jsonl |
| 35 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/readout.py |
| 36 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/relabel.py |
| 37 | 07:13:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/035-unanswered-surface/tally.py |
| 38 | 07:13:09 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 39 | 07:13:09 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 40 | 07:13:09 | doc_update | updated DECISIONS-SCREENING-6.md |
| 41 | 07:13:09 | doc_update | updated DECISIONS.md |
| 42 | 07:13:09 | doc_update | updated FAILURES.md |
| 43 | 07:13:09 | doc_update | updated STATE.md |
| 44 | 07:13:09 | session_end | Ran E035, which replaced three sessions' worth of Stack Exchange rate measurement with a premise test. Four reads of E034's committed bytes cost zero  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-004-test-whether-the-population-e034-found-i/events.jsonl
```
