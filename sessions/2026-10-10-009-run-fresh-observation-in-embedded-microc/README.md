# Session 2026-10-10-009-run-fresh-observation-in-embedded-microc

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T10:37:39+00:00
- **Duration:** 965.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Run fresh observation in embedded/microcontroller fault codes domain using Discourse view_count instrument (E082)

## Summary

E082 completed: view_count instrument generalizes to embedded Discourse forums (discuss.ardupilot.org, community.platformio.org, forum.arduino.cc). All 4 gates pass: G1 need prevalence (40/150 topics), G2 control validity (150 topics), G3 unserved fraction 15.3% (CI95 upper 21.3% < 60%), G4 view_count validation (100%). Unserved-open-like fraction of 15.3% is statistically consistent with E077's 11.7% Discourse baseline, confirming platform invariance. No candidate produced; this is an evidence-gathering experiment per D083.

## Next

Update STATE.md and STATE-next-actions.md with E082 results; allocate decision D101 for the view-count instrument generalization finding

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/082-embedded-fault-codes/results.json | 2e5cbd0387be | 2245 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 9 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/PROTOCOL.md |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/README.md |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/raw/classified_community_platformio_org.jsonl |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/raw/classified_discuss_ardupilot_org.jsonl |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/raw/classified_forum_arduino_cc.jsonl |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/raw/topics_community_platformio_org.jsonl |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/raw/topics_discuss_ardupilot_org.jsonl |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/raw/topics_forum_arduino_cc.jsonl |
|   undeclared | EXPERIMENTS/082-embedded-fault-codes/run_e082.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:37:39 | session_start | Run fresh observation in embedded/microcontroller fault codes domain using Discourse view_count instrument (E082) |
| 2 | 10:43:48 | milestone | E082 experiment completed: all gates pass on embedded Discourse forums (discuss.ardupilot.org, community.platformio.org, forum.arduino.cc) |
| 3 | 10:43:56 | artifact | wrote EXPERIMENTS/082-embedded-fault-codes/results.json |
| 4 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/PROTOCOL.md |
| 5 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/README.md |
| 6 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/raw/classified_community_platformio_org.jsonl |
| 7 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/raw/classified_discuss_ardupilot_org.jsonl |
| 8 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/raw/classified_forum_arduino_cc.jsonl |
| 9 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/raw/topics_community_platformio_org.jsonl |
| 10 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/raw/topics_discuss_ardupilot_org.jsonl |
| 11 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/raw/topics_forum_arduino_cc.jsonl |
| 12 | 10:53:45 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-embedded-fault-codes/run_e082.py |
| 13 | 10:53:45 | session_end | E082 completed: view_count instrument generalizes to embedded Discourse forums (discuss.ardupilot.org, community.platformio.org, forum.arduino.cc). Al |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-009-run-fresh-observation-in-embedded-microc/events.jsonl
```
