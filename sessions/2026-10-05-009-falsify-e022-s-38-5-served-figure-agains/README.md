# Session 2026-10-05-009-falsify-e022-s-38-5-served-figure-agains

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T11:27:34+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Falsify E022's 38.5% served figure against a control arm of ordinary comments in the same threads

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/023-served-baseline/PROTOCOL.md | 27b1d1e7696c | 4693 |
| EXPERIMENTS/023-served-baseline/README.md | e78d9310acf3 | 7389 |
| EXPERIMENTS/023-served-baseline/draw_arms.py | a70c3250594d | 10844 |
| EXPERIMENTS/023-served-baseline/analyse.py | be715614f0fa | 5643 |
| EXPERIMENTS/023-served-baseline/results.json | dca8ad6ca6eb | 1593 |
| EXPERIMENTS/023-served-baseline/raw/labels.tsv | 050970e54d92 | 8545 |
| EXPERIMENTS/023-served-baseline/raw/need_arm.jsonl | 8db17f7f9bd0 | 46372 |
| EXPERIMENTS/023-served-baseline/raw/control_arm.jsonl | 291db1b6f1cd | 53793 |
| EXPERIMENTS/023-served-baseline/raw/nonsense_control.json | e0020a81ae0f | 515 |
| EXPERIMENTS/023-served-baseline/raw/arm_pool_size.json | db47ef51ce1c | 49 |
| FAILURES-findings-17.md | 85fc439a1ccb | 8971 |
| FAILURES.md | 0d4858d77dfe | 10924 |
| DECISIONS-SCREENING.md | ce573a3f1976 | 12648 |
| DECISIONS.md | 24a547441142 | 7927 |
| STATE-next-actions.md | c5e4f511bc61 | 20644 |
| STATE-in-flight.md | 3f733fee9b69 | 16930 |
| HYPOTHESES.md | 37ddf4f94b01 | 13836 |
| EXPERIMENTS/README.md | 89acd70e0eab | 3887 |
| tasks/T-0067-falsify-e022-s-38-5-served-figure-against-a-cont.md | 89ced09be775 | 2318 |
| docs/INDEX.md | 7f4139fc35fd | 26533 |
| sessions/INDEX.md | 706496093c98 | 6784 |
| STATE.md | 2d55aafa29df | 31219 |

## Commands

8 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/023-served-baseline/draw_arms.py', '--verify'] | 3 | 3381 |
| 3 | ['python3', 'EXPERIMENTS/023-served-baseline/draw_arms.py', '--verify'] | 0 | 8112 |
| 5 | ['python3', 'EXPERIMENTS/023-served-baseline/analyse.py'] | 0 | 97 |
| 26 | ['./tools/origin', 'doc', 'lint'] | 2 | 11783 |
| 27 | ['./tools/origin', 'doc', 'lint'] | 2 | 11957 |
| 28 | ['./tools/origin', 'doc', 'lint'] | 0 | 12097 |
| 29 | ['./tools/origin', 'doc', 'lint'] | 0 | 13785 |
| 30 | ['./tools/origin', 'doc', 'lint'] | 0 | 10981 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:27:34 | session_start | Falsify E022's 38.5% served figure against a control arm of ordinary comments in the same threads |
| 2 | 11:29:11 | command | $ python3 EXPERIMENTS/023-served-baseline/draw_arms.py --verify |
| 3 | 11:30:09 | command | $ python3 EXPERIMENTS/023-served-baseline/draw_arms.py --verify |
| 4 | 11:30:16 | milestone | protocol written; nonsense control passes on both readers (Firebase answers 200-with-null, Algolia 404) |
| 5 | 11:37:43 | command | $ python3 EXPERIMENTS/023-served-baseline/analyse.py |
| 6 | 11:37:53 | milestone | E023 gates all decided: label agreement kappa=0.923 on 39 shared rows, need arm 0.395 vs control arm 0.368, intervals overlap -> not informative |
| 7 | 11:37:54 | decision | chose the control arm to be drawn from ANSWERED non-trigger comments in the same stories, not from all non-trigger comments, because served is conditi |
| 8 | 11:43:52 | artifact | wrote EXPERIMENTS/023-served-baseline/PROTOCOL.md |
| 9 | 11:43:52 | artifact | wrote EXPERIMENTS/023-served-baseline/README.md |
| 10 | 11:43:53 | artifact | wrote EXPERIMENTS/023-served-baseline/draw_arms.py |
| 11 | 11:43:54 | artifact | wrote EXPERIMENTS/023-served-baseline/analyse.py |
| 12 | 11:43:54 | artifact | wrote EXPERIMENTS/023-served-baseline/results.json |
| 13 | 11:43:55 | artifact | wrote EXPERIMENTS/023-served-baseline/raw/labels.tsv |
| 14 | 11:43:55 | artifact | wrote EXPERIMENTS/023-served-baseline/raw/need_arm.jsonl |
| 15 | 11:43:56 | artifact | wrote EXPERIMENTS/023-served-baseline/raw/control_arm.jsonl |
| 16 | 11:43:57 | artifact | wrote EXPERIMENTS/023-served-baseline/raw/nonsense_control.json |
| 17 | 11:43:57 | artifact | wrote EXPERIMENTS/023-served-baseline/raw/arm_pool_size.json |
| 18 | 11:43:58 | artifact | wrote FAILURES-findings-17.md |
| 19 | 11:43:58 | artifact | wrote FAILURES.md |
| 20 | 11:43:59 | artifact | wrote DECISIONS-SCREENING.md |
| 21 | 11:44:00 | artifact | wrote DECISIONS.md |
| 22 | 11:44:00 | artifact | wrote STATE-next-actions.md |
| 23 | 11:44:01 | artifact | wrote STATE-in-flight.md |
| 24 | 11:44:01 | artifact | wrote HYPOTHESES.md |
| 25 | 11:44:02 | artifact | wrote EXPERIMENTS/README.md |
| 26 | 11:44:20 | command | $ ./tools/origin doc lint |
| 27 | 11:45:06 | command | $ ./tools/origin doc lint |
| 28 | 11:46:33 | command | $ ./tools/origin doc lint |
| 29 | 11:46:52 | command | $ ./tools/origin doc lint |
| 30 | 11:48:25 | command | $ ./tools/origin doc lint |
| 31 | 12:07:11 | task_rewrite | appended a create record for T-0067 |
| 32 | 12:07:33 | artifact | wrote tasks/T-0067-falsify-e022-s-38-5-served-figure-against-a-cont.md |
| 33 | 12:07:34 | artifact | wrote docs/INDEX.md |
| 34 | 12:07:34 | artifact | wrote sessions/INDEX.md |
| 35 | 12:07:35 | artifact | wrote STATE.md |
| 36 | 12:08:08 | task_rewrite | rewrote tasks/T-0067-falsify-e022-s-38-5-served-figure-against-a-cont.md (status: claimed) |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-009-falsify-e022-s-38-5-served-figure-agains/events.jsonl
```
