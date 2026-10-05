# Session 2026-10-05-010-test-whether-twelve-candidates-twelve-pr

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T12:55:55+00:00
- **Duration:** 3738.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Test whether 'twelve candidates, twelve prior-art deaths' is a fact about the candidates or an artefact of counting

## Summary

T-0068/E024 complete: counted what actually killed the candidates, a claim four summaries carried without a gate. Prior art is 10 of 18 eligible = 0.556 over a population of 20, so the plurality reading survives and 'twelve' is false -- by a one-row margin, since every prior-art row moved to another category puts the share at 0.500. Seven of the 18 died of something else, which gives item 0 a second option with a count behind it: promote fewer claims and price each gate before promoting. Nothing reopens. F044, D056.

## Next

A second reader labelling E024's same 18 rows, given the deciding sentences and no category vocabulary: at a one-row margin, kappa there decides whether the record's sentence is a fact or a coin-flip. Item 0 remains the owner's decision, now over a plurality rather than a majority.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/024-kill-reason-causes/results.json | 6a784a9428a1 | 3561 |
| EXPERIMENTS/024-kill-reason-causes/README.md | c393839ee1ee | 9819 |
| EXPERIMENTS/024-kill-reason-causes/PROTOCOL.md | 8eb476d49d46 | 7069 |
| EXPERIMENTS/024-kill-reason-causes/CONTROL.md | 8058856d1e2b | 4749 |
| FAILURES-findings-18.md | 3511dd987569 | 6738 |
| EXPERIMENTS/024-kill-reason-causes/rowcheck.py | e79c8570e391 | 6049 |
| EXPERIMENTS/024-kill-reason-causes/classify.py | b6aea5ebe9f5 | 10326 |
| STATE-in-flight-2.md | c04688eeccd4 | 4635 |
| EXPERIMENTS/024-kill-reason-causes/results.json | 05c24a00c1be | 3496 |

## Commands

7 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['git', 'add', 'EXPERIMENTS/024-kill-reason-causes/'] | 0 | 81 |
| 9 | ['git', 'commit', '-q', '-m', "E024: prior art is the plurality of kill reasons, and the population is 20 rows rather than twelve\n\nT-0068. 'Twelve c | 0 | 20 |
| 10 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 511241 |
| 16 | ['git', 'commit', '-q', '-m', "F044 and D056: correct the four summaries that carried the count, and record what the counting changed\n\nThe populatio | 0 | 175 |
| 18 | ['git', 'push', '-q', 'origin', 'research/origin'] | 0 | 3575 |
| 21 | ['git', 'commit', '-q', '-m', "STATE.md: the two uncounted claims as one entry, and the session and lint counts from the tree\n\nSTATE.md was at the c | 0 | 115 |
| 22 | ['git', 'push', '-q', 'origin', 'research/origin'] | 0 | 3731 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 10 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/024-kill-reason-causes/control_rows.json |
|   undeclared | EXPERIMENTS/024-kill-reason-causes/rows.json |
|   undeclared | FAILURES-findings-6.md |
|   undeclared | FAILURES.md |
|   undeclared | HYPOTHESES.md |
|   undeclared | STATE-in-flight.md |
|   undeclared | STATE-next-actions.md |
|   undeclared | STATE.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:55:55 | session_start | Test whether 'twelve candidates, twelve prior-art deaths' is a fact about the candidates or an artefact of counting |
| 2 | 12:59:41 | task_rewrite | rewrote tasks/T-0068-classify-what-killed-each-candidate-from-its-p.md (status: claimed) |
| 3 | 12:59:41 | task_rewrite | appended a claim record for T-0068 |
| 4 | 13:20:01 | command | $ git add EXPERIMENTS/024-kill-reason-causes/ |
| 5 | 13:20:11 | artifact | wrote EXPERIMENTS/024-kill-reason-causes/results.json |
| 6 | 13:20:12 | artifact | wrote EXPERIMENTS/024-kill-reason-causes/README.md |
| 7 | 13:20:13 | artifact | wrote EXPERIMENTS/024-kill-reason-causes/PROTOCOL.md |
| 8 | 13:20:13 | artifact | wrote EXPERIMENTS/024-kill-reason-causes/CONTROL.md |
| 9 | 13:20:27 | command | $ git commit -q -m E024: prior art is the plurality of kill reasons, and the population is 20 rows rather than twelve  T-0068. 'Twelve candida |
| 10 | 13:47:40 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 11 | 13:50:54 | artifact | wrote FAILURES-findings-18.md |
| 12 | 13:50:54 | artifact | wrote EXPERIMENTS/024-kill-reason-causes/rowcheck.py |
| 13 | 13:50:55 | artifact | wrote EXPERIMENTS/024-kill-reason-causes/classify.py |
| 14 | 13:50:56 | artifact | wrote STATE-in-flight-2.md |
| 15 | 13:50:56 | artifact | wrote EXPERIMENTS/024-kill-reason-causes/results.json |
| 16 | 13:51:28 | command | $ git commit -q -m F044 and D056: correct the four summaries that carried the count, and record what the counting changed  The population is 2 |
| 17 | 13:51:55 | milestone | E024 complete: F044 recorded, D056 recorded, four summaries corrected, doc lint OK, 790 tests pass |
| 18 | 13:52:07 | command | $ git push -q origin research/origin |
| 19 | 13:52:44 | task_rewrite | rewrote tasks/T-0068-classify-what-killed-each-candidate-from-its-p.md (status: done) |
| 20 | 13:52:45 | task_rewrite | appended a complete record for T-0068 |
| 21 | 13:57:58 | command | $ git commit -q -m STATE.md: the two uncounted claims as one entry, and the session and lint counts from the tree  STATE.md was at the cap, so |
| 22 | 13:58:12 | command | $ git push -q origin research/origin |
| 23 | 13:58:13 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING.md |
| 24 | 13:58:13 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 25 | 13:58:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/024-kill-reason-causes/control_rows.json |
| 26 | 13:58:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/024-kill-reason-causes/rows.json |
| 27 | 13:58:13 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-6.md |
| 28 | 13:58:13 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 29 | 13:58:13 | unlogged_change | changed but never declared as an artifact: HYPOTHESES.md |
| 30 | 13:58:13 | unlogged_change | changed but never declared as an artifact: STATE-in-flight.md |
| 31 | 13:58:13 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 32 | 13:58:13 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 33 | 13:58:13 | doc_update | updated DECISIONS-SCREENING.md |
| 34 | 13:58:13 | doc_update | updated DECISIONS.md |
| 35 | 13:58:13 | doc_update | updated FAILURES.md |
| 36 | 13:58:13 | doc_update | updated HYPOTHESES.md |
| 37 | 13:58:13 | doc_update | updated STATE.md |
| 38 | 13:58:13 | session_end | T-0068/E024 complete: counted what actually killed the candidates, a claim four summaries carried without a gate. Prior art is 10 of 18 eligible = 0.5 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-010-test-whether-twelve-candidates-twelve-pr/events.jsonl
```
