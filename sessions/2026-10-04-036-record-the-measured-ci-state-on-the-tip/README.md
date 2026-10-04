# Session 2026-10-04-036-record-the-measured-ci-state-on-the-tip

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T13:53:06+00:00
- **Duration:** 49.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Record the measured CI state on the tip and T-0050's one red run, from its annotations

## Summary

Recorded T-0050's measured CI state: run 37206580954 green on all seven rows at 3c49642, and run 37206132901's cause read off its own annotation rather than reproduced.

## Next

Unclaimed work: T-0053 for sync land recording the base move of a rebase a human completed (named in STATE.md and T-0050's Notes); and the gate that would read a closed stream's task_rewrite events, which is what decides whether the 50 sessions owing a CLAIMS.jsonl declaration stay a permanent debt.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| STATE.md | 50035c72deaf | 28341 |

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['tools/origin', 'preflight'] | 0 | 8617 |
| 5 | ['tools/origin', 'sync', 'push'] | 0 | 3847 |

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
| 1 | 13:53:06 | session_start | Record the measured CI state on the tip and T-0050's one red run, from its annotations |
| 2 | 13:53:23 | artifact | wrote STATE.md |
| 3 | 13:53:24 | milestone | run 37206580954 green on all seven rows at 3c49642; run 37206132901 red for the recorded expected case |
| 4 | 13:53:33 | command | $ tools/origin preflight |
| 5 | 13:53:47 | command | $ tools/origin sync push |
| 6 | 13:53:55 | doc_update | updated STATE.md |
| 7 | 13:53:55 | session_end | Recorded T-0050's measured CI state: run 37206580954 green on all seven rows at 3c49642, and run 37206132901's cause read off its own annotation rathe |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-036-record-the-measured-ci-state-on-the-tip/events.jsonl
```
