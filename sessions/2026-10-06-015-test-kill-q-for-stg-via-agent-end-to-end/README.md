# Session 2026-10-06-015-test-kill-q-for-stg-via-agent-end-to-end

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T20:18:53+00:00
- **Duration:** 1551.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test KILL-Q for stg via agent end-to-end experiment: measure whether a coding agent uses stg vs alternatives when asked to stage specific lines

## Summary

E042 agent end-to-end staging test completed. Confirmed mechanism parity (stg = shell_baseline = 100% success) and packaging advantage (1 vs 180 agent code lines). Naive approach has 38% silent failure rate. KILL-Q strongly supported for agent usability, not_evaluated for daily human adoption.

## Next

Consider whether to pursue stg as a product given: mechanism validated but not novel, packaging is differentiator, demand measured but low (0.016-0.066), agent usability strongly supported. Next: evaluate if packaging advantage is sufficient for product decision, or explore fresh candidates per owner decision on selection axis (STATE-selection.md item 0).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| HYPOTHESES-candidates.md | 58edec82d20e | 12701 |
| STATE.md | 793d3a6fa76f | 34268 |
| stage-lines/README.md | 0dad53843ebd | 3902 |
| EXPERIMENTS/042-agent-staging-e2e/DESIGN.md | f3375f459b1f | 3390 |
| EXPERIMENTS/042-agent-staging-e2e/run.py | 3e8cb6234f79 | 12017 |
| EXPERIMENTS/042-agent-staging-e2e/README.md | 47b9b2a27ba5 | 3670 |
| EXPERIMENTS/042-agent-staging-e2e/results.json | 3fa4cecbd101 | 7191 |
| HYPOTHESES-candidates.md | a4a330772a5f | 14860 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 2 |
| redactions applied to command output | 0 |
|   error | FAILURES.md was not updated although the session recorded experiment_result |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 20:18:53 | session_start | Test KILL-Q for stg via agent end-to-end experiment: measure whether a coding agent uses stg vs alternatives when asked to stage specific lines |
| 2 | 20:19:02 | artifact | wrote HYPOTHESES-candidates.md |
| 3 | 20:19:03 | artifact | wrote STATE.md |
| 4 | 20:19:03 | artifact | wrote stage-lines/README.md |
| 5 | 20:41:05 | artifact | wrote EXPERIMENTS/042-agent-staging-e2e/DESIGN.md |
| 6 | 20:41:06 | artifact | wrote EXPERIMENTS/042-agent-staging-e2e/run.py |
| 7 | 20:41:06 | artifact | wrote EXPERIMENTS/042-agent-staging-e2e/README.md |
| 8 | 20:41:06 | artifact | wrote EXPERIMENTS/042-agent-staging-e2e/results.json |
| 9 | 20:41:12 | experiment_result | Agent end-to-end test confirms mechanism parity (stg = shell_baseline = 100% success) and packaging advantage (1 vs 180 agent code lines). Naive appro |
| 10 | 20:44:28 | artifact | wrote HYPOTHESES-candidates.md |
| 11 | 20:44:44 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 12 | 20:44:44 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 13 | 20:44:44 | doc_update | updated STATE.md |
| 14 | 20:44:44 | session_end | E042 agent end-to-end staging test completed. Confirmed mechanism parity (stg = shell_baseline = 100% success) and packaging advantage (1 vs 180 agent |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-015-test-kill-q-for-stg-via-agent-end-to-end/events.jsonl
```
