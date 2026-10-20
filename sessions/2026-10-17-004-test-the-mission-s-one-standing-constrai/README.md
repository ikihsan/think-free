# Session 2026-10-17-004-test-the-mission-s-one-standing-constrai

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-17
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-17T06:45:42+00:00
- **Duration:** 4135.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test the mission's one standing constraint head-on: is a free general assistant actually worse when the deciding evidence is absent from the question, on a population where the key is automatic?

## Summary

E177 measured the mission's only standing constraint and it is supported. Same venue, key, treatment and blinded readers, with the only difference being whether the question contained the fact its own resolution depends on: SELF 26/30 = 0.8667 [0.7032, 0.9469] against EVID 12/30 = 0.4000 [0.2459, 0.5768], gap +0.4667, Fisher p = 0.000368, on a bar of gap>=0.25 and p<0.05 declared before any answer body was read. Four controls green. 0.4000 is the lowest rate a free general assistant has scored on a real question population in this record and it was inside all six closure pools, unmeasured. Six instrument defects declared (four before measurement); the Fisher tail summed ratios and left every control green while the p-value was wrong by 2,700x. A post-hoc pass flagged 7 of 30 EVID labels, so CLF precision is ~0.77-0.87 and the headline is not recomputed.

## Next

Run E178: of the 46 evidence-gated rows, is the missing evidence obtainable from something the asker already has. Two post-hoc leads move its centre of gravity - publishable drew 0 of 30 on one reader's guess, and in 18 of 18 misses the missing fact was load-bearing rather than absent. E178 should re-key its rows with its own rule and must not inherit E177's labels. Also: do not run two origin doc lint processes concurrently; they disagreed on unchanged bytes and the reported files were days old.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/177-evidence-gated-need/PROTOCOL.md | 8604eaf35d3c | 11479 |
| EXPERIMENTS/177-evidence-gated-need/RESULT.md | 174f86d3be48 | 9053 |
| EXPERIMENTS/177-evidence-gated-need/RESULT.md | d2ddcbdea276 | 13642 |

## Commands

23 captured, 6 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['./tools/origin', 'doc', 'lint'] | 0 | 276346 |
| 3 | ['git', 'commit', '-q', '-am', 'E177 PROTOCOL + fetch + census: measure the standing constraint D107 rests on'] | 0 | 399 |
| 5 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/fetch.py'] | 1 | 17515 |
| 6 | ['git', 'commit', '-q', '-am', 'E177 AMENDMENT 1: accept both tag shapes; the withbody filter returns strings'] | 1 | 295 |
| 7 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/fetch.py'] | 0 | 18302 |
| 8 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/fetch.py'] | 0 | 20189 |
| 9 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/census.py'] | 0 | 278 |
| 10 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/roles.py'] | 1 | 835 |
| 11 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/roles.py'] | 0 | 312 |
| 12 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/roles.py'] | 0 | 319 |
| 13 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/arms.py'] | 1 | 608 |
| 14 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/arms.py'] | 0 | 198 |
| 16 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/repair.py'] | 0 | 99 |
| 17 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/score_inputs.py'] | 0 | 131 |
| 18 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/score_inputs.py'] | 0 | 137 |
| 19 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/score.py'] | 0 | 109 |
| 20 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/score.py'] | 0 | 199 |
| 22 | ['./tools/origin', 'doc', 'index'] | 0 | 12799 |
| 23 | ['./tools/origin', 'doc', 'lint'] | 2 | 156738 |
| 24 | ['./tools/origin', 'doc', 'index'] | 0 | 10618 |
| 25 | ['./tools/origin', 'doc', 'lint'] | 2 | 157116 |
| 26 | ['./tools/origin', 'doc', 'lint'] | 0 | 828898 |
| 27 | ['./tools/origin', 'doc', 'lint'] | 0 | 846018 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 36 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-RECORDS-3.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/AMENDMENT-1.md |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/AMENDMENT-2.md |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/AMENDMENT-3.md |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/AMENDMENT-4.md |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/AMENDMENT-5.md |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/AMENDMENT-6.md |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/ans/answers.jsonl |
|   undeclared | EXPERIMENTS/177-evidence-gated-need/ans/order.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 06:45:42 | session_start | Test the mission's one standing constraint head-on: is a free general assistant actually worse when the deciding evidence is absent from the question, |
| 2 | 06:50:28 | command | $ ./tools/origin doc lint |
| 3 | 06:50:55 | command | $ git commit -q -am E177 PROTOCOL + fetch + census: measure the standing constraint D107 rests on |
| 4 | 06:50:58 | artifact | wrote EXPERIMENTS/177-evidence-gated-need/PROTOCOL.md |
| 5 | 06:51:20 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/fetch.py |
| 6 | 06:51:34 | command | $ git commit -q -am E177 AMENDMENT 1: accept both tag shapes; the withbody filter returns strings |
| 7 | 06:51:59 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/fetch.py |
| 8 | 06:53:21 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/fetch.py |
| 9 | 06:53:27 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/census.py |
| 10 | 06:53:53 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/roles.py |
| 11 | 06:54:03 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/roles.py |
| 12 | 06:59:40 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/roles.py |
| 13 | 07:06:04 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/arms.py |
| 14 | 07:06:17 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/arms.py |
| 15 | 07:06:31 | milestone | CLF arms committed before any answer: SELF 52, EVID 46, UNCLEAR 2 of the 100 highest-arrival keyed rows |
| 16 | 07:15:20 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/repair.py |
| 17 | 07:15:38 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/score_inputs.py |
| 18 | 07:15:51 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/score_inputs.py |
| 19 | 07:19:33 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/score.py |
| 20 | 07:20:05 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/score.py |
| 21 | 07:20:40 | artifact | wrote EXPERIMENTS/177-evidence-gated-need/RESULT.md |
| 22 | 07:23:02 | command | $ ./tools/origin doc index |
| 23 | 07:25:47 | command | $ ./tools/origin doc lint |
| 24 | 07:26:50 | command | $ ./tools/origin doc index |
| 25 | 07:29:30 | command | $ ./tools/origin doc lint |
| 26 | 07:43:30 | command | $ ./tools/origin doc lint |
| 27 | 07:45:48 | command | $ ./tools/origin doc lint |
| 28 | 07:54:16 | artifact | wrote EXPERIMENTS/177-evidence-gated-need/RESULT.md |
| 29 | 07:54:25 | milestone | RESULT, F136, D118, STATE.md, STATE-next-actions.md and the addendum all committed; doc lint green on a single run |
| 30 | 07:54:37 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-3.md |
| 31 | 07:54:37 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 32 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/AMENDMENT-1.md |
| 33 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/AMENDMENT-2.md |
| 34 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/AMENDMENT-3.md |
| 35 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/AMENDMENT-4.md |
| 36 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/AMENDMENT-5.md |
| 37 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/AMENDMENT-6.md |
| 38 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/ans/answers.jsonl |
| 39 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/ans/order.json |
| 40 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/arms.json |
| 60 | 07:54:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/177-evidence-gated-need/score_inputs.py |
| 61 | 07:54:37 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-43.md |
| 62 | 07:54:37 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 63 | 07:54:37 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 64 | 07:54:37 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 65 | 07:54:37 | unlogged_change | changed but never declared as an artifact: vendor/MANIFEST.md |
| 66 | 07:54:37 | doc_update | updated DECISIONS.md |
| 67 | 07:54:37 | doc_update | updated FAILURES.md |
| 68 | 07:54:37 | doc_update | updated STATE.md |
| 69 | 07:54:37 | session_end | E177 measured the mission's only standing constraint and it is supported. Same venue, key, treatment and blinded readers, with the only difference bei |

_19 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-17-004-test-the-mission-s-one-standing-constrai/events.jsonl
```
