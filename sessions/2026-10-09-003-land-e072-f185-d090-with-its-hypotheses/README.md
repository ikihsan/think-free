# Session 2026-10-09-003-land-e072-f185-d090-with-its-hypotheses

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T02:58:46+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Land E072 (F185/D090) with its HYPOTHESES gap closed, then run E073: does a piecewise-constant price model replace the CV ceiling and recover recall on E072's frozen corpus?

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/073-piecewise-price/README.md | 061e00ad0e63 | 6887 |
| EXPERIMENTS/073-piecewise-price/verdict.json | d4201c863819 | 3547 |
| EXPERIMENTS/073-piecewise-price/added_labels.json | aa1ad6ad6f20 | 3747 |
| EXPERIMENTS/073-piecewise-price/results.json | 96ba72f51cb4 | 31727 |
| EXPERIMENTS/073-piecewise-price/added_groups.json | cf098589122e | 6645 |
| EXPERIMENTS/073-piecewise-price/dropped_groups.json | c20e030c295b | 14716 |
| EXPERIMENTS/073-piecewise-price/eval_arms.py | 9e8c9feaba1d | 14406 |
| EXPERIMENTS/073-piecewise-price/detect_pwc.py | ad071bcc31e9 | 5433 |
| EXPERIMENTS/073-piecewise-price/PROTOCOL.md | 161c5099afd5 | 7047 |

## Commands

5 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 1 | 51517 |
| 5 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 1 | 87803 |
| 7 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 0 | 33289 |
| 8 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 0 | 35796 |
| 19 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 0 | 43082 |

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
| 1 | 02:58:46 | session_start | Land E072 (F185/D090) with its HYPOTHESES gap closed, then run E073: does a piecewise-constant price model replace the CV ceiling and recover recall o |
| 2 | 06:40:26 | milestone | Resuming interrupted session 2026-10-09-003: E072 landing complete in-tree (uncommitted), E073 harness written (PROTOCOL.md, detect_pwc.py, eval_arms. |
| 3 | 06:42:16 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 4 | 06:44:26 | note | Pre-first-run harness repair (defect-class, no gate/arm/threshold/label change): run_pwc returned detector dicts where the census expects merchant str |
| 5 | 06:46:47 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 6 | 06:55:19 | note | Pre-first-run harness repair 2 (no gate/arm/threshold/label change): describe_group's census view included positive-credit rows the detector's amount< |
| 7 | 07:03:21 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 8 | 07:06:39 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 9 | 07:11:25 | milestone | E073 first full run complete: G0 passes (e065_raw reproduces E072 exactly after fixing a mixed-side filter defect), G1 and G2 fail (recall 0.455 < 0.5 |
| 10 | 07:20:47 | artifact | wrote EXPERIMENTS/073-piecewise-price/README.md |
| 11 | 07:20:48 | artifact | wrote EXPERIMENTS/073-piecewise-price/verdict.json |
| 12 | 07:20:48 | artifact | wrote EXPERIMENTS/073-piecewise-price/added_labels.json |
| 13 | 07:20:49 | artifact | wrote EXPERIMENTS/073-piecewise-price/results.json |
| 14 | 07:20:50 | artifact | wrote EXPERIMENTS/073-piecewise-price/added_groups.json |
| 15 | 07:20:50 | artifact | wrote EXPERIMENTS/073-piecewise-price/dropped_groups.json |
| 16 | 07:20:51 | artifact | wrote EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 17 | 07:20:52 | artifact | wrote EXPERIMENTS/073-piecewise-price/detect_pwc.py |
| 18 | 07:20:52 | artifact | wrote EXPERIMENTS/073-piecewise-price/PROTOCOL.md |
| 19 | 07:29:40 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-003-land-e072-f185-d090-with-its-hypotheses/events.jsonl
```
