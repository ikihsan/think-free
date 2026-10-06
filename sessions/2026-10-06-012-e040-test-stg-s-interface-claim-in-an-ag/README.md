# Session 2026-10-06-012-e040-test-stg-s-interface-claim-in-an-ag

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T11:58:06+00:00
- **Duration:** 934.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E040: test stg's interface claim in an agent-style tool-call loop against git plumbing

## Summary

E040 put the agent caller in the loop: stg exact+honest 5/5 (1 call, 10-33 bytes); hand-written plumbing silently over-staged 2/5; filterdiff exact 2/5 with opaque 128s. Correctness oracle (E037-E039) could not see this. Stale stg README bullet found and corrected. F065 recorded, D070 adopted, doc lint 0.

## Next

KILL-Q remains not_evaluated; the only open gate needs an external population, not a better oracle.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/040-agent-staging-loop/run.py | 622d60a66686 | 7418 |
| EXPERIMENTS/040-agent-staging-loop/README.md | 97512f0fd969 | 3991 |
| EXPERIMENTS/040-agent-staging-loop/raw/results.jsonl | e9a55eccd639 | 3555 |
| stage-lines/README.md | 8efa9acbbbaf | 3602 |
| FAILURES-findings-27.md | e8f42b4b6991 | 1306 |
| DECISIONS-SCREENING-10.md | b83df1b04c0f | 1733 |
| DECISIONS.md | 50a943aab1fb | 11442 |
| FAILURES.md | 957a6391cc41 | 35993 |
| STATE.md | 95f1f4b242ee | 37205 |
| docs/INDEX.md | f59332888690 | 40321 |

## Commands

3 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/040-agent-staging-loop/run.py'] | 1 | 1185 |
| 3 | ['python3', 'EXPERIMENTS/040-agent-staging-loop/run.py'] | 0 | 1976 |
| 4 | ['python3', 'EXPERIMENTS/040-agent-staging-loop/run.py'] | 0 | 1910 |

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
| 1 | 11:58:06 | session_start | E040: test stg's interface claim in an agent-style tool-call loop against git plumbing |
| 2 | 12:01:46 | command | $ python3 EXPERIMENTS/040-agent-staging-loop/run.py |
| 3 | 12:02:43 | command | $ python3 EXPERIMENTS/040-agent-staging-loop/run.py |
| 4 | 12:03:17 | command | $ python3 EXPERIMENTS/040-agent-staging-loop/run.py |
| 5 | 12:13:19 | artifact | wrote EXPERIMENTS/040-agent-staging-loop/run.py |
| 6 | 12:13:20 | artifact | wrote EXPERIMENTS/040-agent-staging-loop/README.md |
| 7 | 12:13:21 | artifact | wrote EXPERIMENTS/040-agent-staging-loop/raw/results.jsonl |
| 8 | 12:13:21 | artifact | wrote stage-lines/README.md |
| 9 | 12:13:22 | artifact | wrote FAILURES-findings-27.md |
| 10 | 12:13:23 | artifact | wrote DECISIONS-SCREENING-10.md |
| 11 | 12:13:24 | artifact | wrote DECISIONS.md |
| 12 | 12:13:25 | artifact | wrote FAILURES.md |
| 13 | 12:13:25 | artifact | wrote STATE.md |
| 14 | 12:13:26 | artifact | wrote docs/INDEX.md |
| 15 | 12:13:41 | doc_update | updated DECISIONS.md |
| 16 | 12:13:41 | doc_update | updated FAILURES.md |
| 17 | 12:13:41 | doc_update | updated STATE.md |
| 18 | 12:13:41 | session_end | E040 put the agent caller in the loop: stg exact+honest 5/5 (1 call, 10-33 bytes); hand-written plumbing silently over-staged 2/5; filterdiff exact 2/ |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-012-e040-test-stg-s-interface-claim-in-an-ag/events.jsonl
```
