# Session 2026-10-19-002-recover-and-label-the-unevidenced-2026-1

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-19
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-19T00:24:27+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Recover and label the unevidenced 2026-10-18 record honestly, then run one declared fresh-observation experiment on an axis no prior experiment used

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/193-source-capability-probe/probe.py | 694ca6b14906 | 4557 |
| EXPERIMENTS/193-source-capability-probe/probe2.py | 3f69c3f8f2ab | 4708 |
| EXPERIMENTS/193-source-capability-probe/raw/probe.json | 0185085586f7 | 6054 |
| EXPERIMENTS/193-source-capability-probe/raw/probe2.json | aef7221babba | 2691 |
| EXPERIMENTS/194-appstore-demand-scan/scan.py | 4550de9e5fec | 6680 |
| EXPERIMENTS/194-appstore-demand-scan/scan2.py | 5a2c38ca3bf5 | 7277 |

## Commands

7 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/193-source-capability-probe/probe.py'] | 0 | 7360 |
| 3 | ['python3', 'EXPERIMENTS/193-source-capability-probe/probe2.py'] | 0 | 5260 |
| 8 | ['python3', 'EXPERIMENTS/194-appstore-demand-scan/scan.py'] | 0 | 66088 |
| 9 | ['python3', 'EXPERIMENTS/194-appstore-demand-scan/scan2.py'] | 0 | 14474 |
| 12 | ['python3', 'EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py'] | 1 | 1905 |
| 13 | ['python3', 'EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py'] | 0 | 195 |
| 14 | ['python3', 'EXPERIMENTS/185-knitting-repair-planner-stage-a/planner.py'] | 1 | 996 |

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
| 1 | 00:24:27 | session_start | Recover and label the unevidenced 2026-10-18 record honestly, then run one declared fresh-observation experiment on an axis no prior experiment used |
| 2 | 00:25:05 | command | $ python3 EXPERIMENTS/193-source-capability-probe/probe.py |
| 3 | 00:25:44 | command | $ python3 EXPERIMENTS/193-source-capability-probe/probe2.py |
| 4 | 00:26:01 | artifact | wrote EXPERIMENTS/193-source-capability-probe/probe.py |
| 5 | 00:26:02 | artifact | wrote EXPERIMENTS/193-source-capability-probe/probe2.py |
| 6 | 00:26:03 | artifact | wrote EXPERIMENTS/193-source-capability-probe/raw/probe.json |
| 7 | 00:26:04 | artifact | wrote EXPERIMENTS/193-source-capability-probe/raw/probe2.json |
| 8 | 00:27:40 | command | $ python3 EXPERIMENTS/194-appstore-demand-scan/scan.py |
| 9 | 00:28:37 | command | $ python3 EXPERIMENTS/194-appstore-demand-scan/scan2.py |
| 10 | 00:29:26 | artifact | wrote EXPERIMENTS/194-appstore-demand-scan/scan.py |
| 11 | 00:29:27 | artifact | wrote EXPERIMENTS/194-appstore-demand-scan/scan2.py |
| 12 | 00:38:41 | command | $ python3 EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py |
| 13 | 00:38:54 | command | $ python3 EXPERIMENTS/185-knitting-repair-planner-stage-a/knitting_graph.py |
| 14 | 00:39:19 | command | $ python3 EXPERIMENTS/185-knitting-repair-planner-stage-a/planner.py |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-19-002-recover-and-label-the-unevidenced-2026-1/events.jsonl
```
