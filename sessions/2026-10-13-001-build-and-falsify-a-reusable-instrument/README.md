# Session 2026-10-13-001-build-and-falsify-a-reusable-instrument

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T00:23:59+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Build and falsify a reusable instrument-validity checker for LLM-output evaluations, using this repository's two committed defective harnesses (E114 verifier FPR=1.00, E116 scorer key mismatch) as real positive cases

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md | 41a2fb5feac2 | 8432 |
| FAILURES-findings-40.md | 155ea8c42346 | 13640 |
| DECISIONS-SCREENING-20.md | 64b14ab2ca93 | 11176 |
| FAILURES.md | 5b0d76578859 | 79325 |
| DECISIONS.md | 2b8988b2b451 | 25100 |
| EXPERIMENTS/124-eval-harness-preflight/AMENDMENT-1.md | fc58fb9d68d0 | 3883 |
| EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md | 41a2fb5feac2 | 8432 |
| EXPERIMENTS/124-eval-harness-preflight/README.md | c2be6d25df30 | 2785 |
| EXPERIMENTS/124-eval-harness-preflight/RESULT.md | e7a048454630 | 7233 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/__init__.py | c949ada34bd0 | 980 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/alternate_form.py | 1822df6567f6 | 4030 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/concordance.py | 657f088635e4 | 7748 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/control_arm.py | ff02dda9ba92 | 2624 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/report.py | 2fc6c218d782 | 2586 |
| EXPERIMENTS/124-eval-harness-preflight/preflight/stats.py | e1ae7208f7bf | 1059 |
| EXPERIMENTS/124-eval-harness-preflight/results.json | ed563f3fbc14 | 10944 |
| EXPERIMENTS/124-eval-harness-preflight/run.py | 967fc49e4f82 | 10201 |
| EXPERIMENTS/124-eval-harness-preflight/test_preflight.py | 33ce1c323e55 | 7629 |

## Commands

0 captured, 0 non-zero exit.

_none_

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
| 1 | 00:23:59 | session_start | Build and falsify a reusable instrument-validity checker for LLM-output evaluations, using this repository's two committed defective harnesses (E114 v |
| 2 | 00:29:49 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md |
| 3 | 00:37:57 | artifact | wrote FAILURES-findings-40.md |
| 4 | 00:38:08 | artifact | wrote DECISIONS-SCREENING-20.md |
| 5 | 00:38:20 | artifact | wrote FAILURES.md |
| 6 | 00:38:31 | artifact | wrote DECISIONS.md |
| 7 | 00:53:00 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/AMENDMENT-1.md |
| 8 | 00:53:14 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/PROTOCOL.md |
| 9 | 00:53:18 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/README.md |
| 10 | 00:53:20 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/RESULT.md |
| 11 | 00:53:21 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/__init__.py |
| 12 | 00:53:24 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/alternate_form.py |
| 13 | 00:53:26 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/concordance.py |
| 14 | 00:53:31 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/control_arm.py |
| 15 | 00:53:58 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/report.py |
| 16 | 00:54:11 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/preflight/stats.py |
| 17 | 00:54:43 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/results.json |
| 18 | 00:55:11 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/run.py |
| 19 | 00:55:23 | artifact | wrote EXPERIMENTS/124-eval-harness-preflight/test_preflight.py |
| 20 | 00:55:36 | milestone | E124 complete: preflight built (4 modules, 16 tests passing), run against six cases on committed harnesses; K1 4/5, K2 failed as declared, K3 and K4 p |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-001-build-and-falsify-a-reusable-instrument/events.jsonl
```
