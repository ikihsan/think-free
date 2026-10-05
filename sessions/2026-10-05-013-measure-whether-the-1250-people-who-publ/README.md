# Session 2026-10-05-013-measure-whether-the-1250-people-who-publ

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T14:30:22+00:00
- **Duration:** 5204.6s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure whether the 1250 people who publicly stated a need are people who build, using an instrument that does not depend on self-disclosure (T-0069)

## Summary

E025 (T-0069) read the disclosure floor under F042's 0-of-24 build arm. 278 of 1250 need-staters (0.222, CI [0.200,0.246]) have a public show_hn post against 139 of 500 (0.278, CI [0.241,0.319]) control commenters in the same stories: ratio 0.80x, intervals overlap, zero refusals, Gate A1 6 of 6. The hypothesis fails in the opposite direction, so item 0d's corpus closure is CONFIRMED by measurement rather than withdrawn by caveat. 'Need-staters are not builders' is false as an absolute - a fifth of them are builders of other things. F045, D057. Also found and recorded an instrument defect in the gate protecting the finding: two of Gate A1's four original controls had no Show HN post at all, so reading '4 of 4' as a pass would have been a false positive.

## Next

The corpus's remaining sub-population is the 589 statements that drew no reply (named in STATE-in-flight.md and still unrun). It needs its own falsifiable claim before it is worth the budget, and it would be a third read of a population already read three times - so prefer a population not yet read.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/025-need-staters-builderhood/PROTOCOL.md | 54b59dadce3e | 7977 |
| EXPERIMENTS/025-need-staters-builderhood/README.md | fb4b6d98cb6b | 7416 |
| EXPERIMENTS/025-need-staters-builderhood/fetch_authors.py | 5c8cf0ae166c | 8649 |
| EXPERIMENTS/025-need-staters-builderhood/fetch_control.py | 54f80950bcbd | 5376 |
| EXPERIMENTS/025-need-staters-builderhood/raw/control_arm.jsonl | 80137534c920 | 57019 |
| EXPERIMENTS/025-need-staters-builderhood/raw/control_authors.jsonl | 94c1f37a0d4d | 92578 |
| EXPERIMENTS/025-need-staters-builderhood/raw/gate_a1_controls.jsonl | 629780ed4c6f | 1161 |
| EXPERIMENTS/025-need-staters-builderhood/raw/need_arm.jsonl | 6b8b2e4ca1b8 | 128416 |
| EXPERIMENTS/025-need-staters-builderhood/results.json | 599b2cb813f8 | 5350 |
| EXPERIMENTS/025-need-staters-builderhood/stats.py | 5334cbad382f | 8861 |
| EXPERIMENTS/025-need-staters-builderhood/test_gates_falsified.py | 10cba02e52fa | 8191 |
| FAILURES-findings-19.md | d8d288e9d3ca | 5284 |
| DECISIONS-SCREENING-3.md | af02e4b75257 | 12510 |
| DECISIONS.md | 4cf27f336f00 | 8107 |
| FAILURES.md | 4a21dfb98f4e | 13284 |
| HYPOTHESES.md | 68aaa370545e | 16701 |
| RELEASE-MANIFEST.md | 1d092caa2c48 | 5073 |
| STATE-in-flight.md | c6487a801e98 | 16890 |
| STATE-next-actions.md | 20a39c70fc0c | 20908 |
| STATE.md | 426ff1911caa | 32405 |
| ROADMAP.md | 93ea4ea41452 | 20122 |

## Commands

3 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/025-need-staters-builderhood/fetch_control.py'] | 0 | 971294 |
| 4 | ['python3', 'EXPERIMENTS/025-need-staters-builderhood/stats.py'] | 0 | 121 |
| 6 | ['python3', '-m', 'unittest', 'discover', '-s', 'EXPERIMENTS/025-need-staters-builderhood', '-p', 'test_*.py', '-t', 'EXPERIMENTS/025-need-staters-bui | 0 | 689 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 14:30:22 | session_start | Measure whether the 1250 people who publicly stated a need are people who build, using an instrument that does not depend on self-disclosure (T-0069) |
| 2 | 14:42:49 | milestone | E025 protocol declared before any fetch; Gate A1 instrument controls run first (6 of 6 verified positives recovered, nonsense 0, two originally-believ |
| 3 | 15:14:05 | command | $ python3 EXPERIMENTS/025-need-staters-builderhood/fetch_control.py |
| 4 | 15:14:34 | command | $ python3 EXPERIMENTS/025-need-staters-builderhood/stats.py |
| 5 | 15:14:41 | milestone | E025 complete: need arm 278/1250 = 0.222 vs control arm 139/500 = 0.278, intervals overlap, H1 fails. Need-staters announce builds LOWER than ordinary |
| 6 | 15:29:48 | command | $ python3 -m unittest discover -s EXPERIMENTS/025-need-staters-builderhood -p test_*.py -t EXPERIMENTS/025-need-staters-builderhood |
| 7 | 15:41:40 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/PROTOCOL.md |
| 8 | 15:41:41 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/README.md |
| 9 | 15:41:41 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/fetch_authors.py |
| 10 | 15:41:41 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/fetch_control.py |
| 11 | 15:41:41 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/raw/control_arm.jsonl |
| 12 | 15:41:41 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/raw/control_authors.jsonl |
| 13 | 15:41:42 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/raw/gate_a1_controls.jsonl |
| 14 | 15:41:42 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/raw/need_arm.jsonl |
| 15 | 15:41:42 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/results.json |
| 16 | 15:41:42 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/stats.py |
| 17 | 15:41:43 | artifact | wrote EXPERIMENTS/025-need-staters-builderhood/test_gates_falsified.py |
| 18 | 15:41:44 | artifact | wrote FAILURES-findings-19.md |
| 19 | 15:41:44 | artifact | wrote DECISIONS-SCREENING-3.md |
| 20 | 15:41:45 | artifact | wrote DECISIONS.md |
| 21 | 15:41:45 | artifact | wrote FAILURES.md |
| 22 | 15:41:46 | artifact | wrote HYPOTHESES.md |
| 23 | 15:41:47 | artifact | wrote RELEASE-MANIFEST.md |
| 24 | 15:41:47 | artifact | wrote STATE-in-flight.md |
| 25 | 15:41:48 | artifact | wrote STATE-next-actions.md |
| 26 | 15:41:48 | artifact | wrote STATE.md |
| 27 | 15:43:14 | task_rewrite | appended a create record for T-0069 |
| 28 | 15:44:32 | task_rewrite | rewrote tasks/T-0069-measure-whether-the-people-who-publicly-stated-a.md (status: claimed) |
| 29 | 15:44:32 | task_rewrite | appended a claim record for T-0069 |
| 30 | 15:44:56 | task_rewrite | rewrote tasks/T-0069-measure-whether-the-people-who-publicly-stated-a.md (status: done) |
| 31 | 15:44:56 | task_rewrite | appended a complete record for T-0069 |
| 32 | 15:56:20 | artifact | wrote ROADMAP.md |
| 33 | 15:57:07 | doc_update | updated DECISIONS-SCREENING-3.md |
| 34 | 15:57:07 | doc_update | updated DECISIONS.md |
| 35 | 15:57:07 | doc_update | updated FAILURES.md |
| 36 | 15:57:07 | doc_update | updated HYPOTHESES.md |
| 37 | 15:57:07 | doc_update | updated ROADMAP.md |
| 38 | 15:57:07 | doc_update | updated STATE.md |
| 39 | 15:57:07 | session_end | E025 (T-0069) read the disclosure floor under F042's 0-of-24 build arm. 278 of 1250 need-staters (0.222, CI [0.200,0.246]) have a public show_hn post  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-013-measure-whether-the-1250-people-who-publ/events.jsonl
```
