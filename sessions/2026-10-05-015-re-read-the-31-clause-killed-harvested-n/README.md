# Session 2026-10-05-015-re-read-the-31-clause-killed-harvested-n

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-05T16:44:50+00:00
- **Duration:** 3368.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Re-read the 31 clause-killed harvested needs from their full text and test whether F029's largest falsifiable claim is an artefact of the clause-extraction rule

## Summary

E027: re-read the 31 clause-based cause-of-death verdicts of E012's 50-row screen from the full comment with two blind readers. Found that 6 of the 15 'vague' kills state a mechanism or a named artifact in the comment text the screen never read, because the cause of death was assigned from a regex-extracted clause rather than a comment. 'vague' withdrawn as a cause of death at its recorded size. F029's 0-of-50 stands: none of the 8 re-opened rows is a candidate, so the generator's closure is now confirmed by a re-read rather than carried forward. The declared six-category agreement gate failed (kappa 0.4627 against a floor of 0.6) and the restated table is reported inconclusive; the separately declared per-row gate fired on 8 of 31, and both gates were falsified against fabricated populations before their results were read. F047, D059, T-0071.

## Next

Item 0d's seat is still empty and this session closed its weakest prop rather than filling it. The live question is item 0: what the mission selects candidates on, which is still an owner decision and is not blocked on tooling. If that decision is deferred again, the one measurement never made is on the 19 prior_art rows F029 kept: E016 adjudicated them on three corpora but never against F029's own clause, so the remaining half of F029's table has been read by exactly one procedure.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/027-cause-of-death-reread/raw/reader_r.jsonl | 81709687a979 | 9730 |
| EXPERIMENTS/027-cause-of-death-reread/README.md | 7f4b6bd59170 | 8307 |
| EXPERIMENTS/027-cause-of-death-reread/PROTOCOL.md | 4be3f87a0528 | 6840 |
| EXPERIMENTS/027-cause-of-death-reread/results.json | f2aa0f76062f | 9519 |
| EXPERIMENTS/027-cause-of-death-reread/stats.py | f2fd79fe7b57 | 10640 |
| EXPERIMENTS/027-cause-of-death-reread/population.py | bda7a8d5c230 | 4592 |
| EXPERIMENTS/027-cause-of-death-reread/recheck.py | 89d142092549 | 4874 |
| EXPERIMENTS/027-cause-of-death-reread/raw/reader_r.jsonl | 81709687a979 | 9730 |
| EXPERIMENTS/027-cause-of-death-reread/raw/reader_s.jsonl | ea1908d5efaf | 8253 |
| EXPERIMENTS/027-cause-of-death-reread/raw/population.jsonl | a81c7dc134d6 | 23265 |
| FAILURES.md | b3f75286aa77 | 15273 |
| FAILURES-findings-19.md | 09f02d0a7dac | 12390 |
| DECISIONS.md | 4d36928332aa | 8255 |
| DECISIONS-SCREENING-3.md | 944a651ac46a | 17273 |
| HYPOTHESES.md | 82520d398225 | 18850 |
| EXPERIMENTS/README.md | cb5482f7e1d4 | 4732 |
| EXPERIMENTS/012-candidate-harvest/README.md | e2567930f168 | 6424 |
| STATE.md | 2d1783818e02 | 32317 |
| STATE-in-flight.md | c767f24ed4b2 | 17440 |
| STATE-history.md | 5a5b892834e4 | 19116 |
| STATE-history-2.md | c238d76155c8 | 19383 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 6 | ['python3', 'EXPERIMENTS/027-cause-of-death-reread/recheck.py', '--selftest'] | 0 | 113 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 2 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | ROADMAP.md |
|   undeclared | STATE-next-actions.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:44:50 | session_start | Re-read the 31 clause-killed harvested needs from their full text and test whether F029's largest falsifiable claim is an artefact of the clause-extra |
| 2 | 16:45:12 | task_rewrite | rewrote tasks/T-0071-re-read-the-31-clause-killed-harvested-needs-fro.md (status: claimed) |
| 3 | 16:45:12 | task_rewrite | appended a claim record for T-0071 |
| 4 | 16:46:07 | milestone | protocol and blind population written, gate declared before any classification |
| 5 | 16:47:57 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/raw/reader_r.jsonl |
| 6 | 16:58:43 | command | $ python3 EXPERIMENTS/027-cause-of-death-reread/recheck.py --selftest |
| 7 | 17:34:23 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/README.md |
| 8 | 17:34:25 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/PROTOCOL.md |
| 9 | 17:34:25 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/results.json |
| 10 | 17:34:26 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/stats.py |
| 11 | 17:34:27 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/population.py |
| 12 | 17:34:27 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/recheck.py |
| 13 | 17:34:28 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/raw/reader_r.jsonl |
| 14 | 17:34:29 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/raw/reader_s.jsonl |
| 15 | 17:34:29 | artifact | wrote EXPERIMENTS/027-cause-of-death-reread/raw/population.jsonl |
| 16 | 17:34:30 | artifact | wrote FAILURES.md |
| 17 | 17:34:30 | artifact | wrote FAILURES-findings-19.md |
| 18 | 17:34:31 | artifact | wrote DECISIONS.md |
| 19 | 17:34:32 | artifact | wrote DECISIONS-SCREENING-3.md |
| 20 | 17:34:32 | artifact | wrote HYPOTHESES.md |
| 21 | 17:34:33 | artifact | wrote EXPERIMENTS/README.md |
| 22 | 17:34:33 | artifact | wrote EXPERIMENTS/012-candidate-harvest/README.md |
| 23 | 17:34:34 | artifact | wrote STATE.md |
| 24 | 17:34:34 | artifact | wrote STATE-in-flight.md |
| 25 | 17:34:35 | artifact | wrote STATE-history.md |
| 26 | 17:34:36 | artifact | wrote STATE-history-2.md |
| 27 | 17:34:36 | milestone | E027 complete: 8 of 31 convergent flips, declared agreement gate failed at kappa 0.4627, F029's 0-of-50 confirmed by re-read |
| 28 | 17:35:18 | task_rewrite | rewrote tasks/T-0071-re-read-the-31-clause-killed-harvested-needs-fro.md (status: done) |
| 29 | 17:35:18 | task_rewrite | appended a complete record for T-0071 |
| 30 | 17:40:58 | unlogged_change | changed but never declared as an artifact: ROADMAP.md |
| 31 | 17:40:58 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 32 | 17:40:58 | doc_update | updated DECISIONS-SCREENING-3.md |
| 33 | 17:40:58 | doc_update | updated DECISIONS.md |
| 34 | 17:40:58 | doc_update | updated FAILURES.md |
| 35 | 17:40:58 | doc_update | updated HYPOTHESES.md |
| 36 | 17:40:58 | doc_update | updated ROADMAP.md |
| 37 | 17:40:58 | doc_update | updated STATE.md |
| 38 | 17:40:58 | session_end | E027: re-read the 31 clause-based cause-of-death verdicts of E012's 50-row screen from the full comment with two blind readers. Found that 6 of the 15 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-015-re-read-the-31-clause-killed-harvested-n/events.jsonl
```
