# Session 2026-10-11-044-fresh-observation-test-view-count-princi

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T19:18:53+00:00
- **Duration:** 17142.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation: test view-count principle on Pub.dev (Dart/Flutter package registry)

## Summary

Stale session recovered (started 2026-10-11T19:18 by a process that died). Wrote E109 PROTOCOL.md for Pub.dev but ran no fetch. On recovery, inspection of the committed raw data showed the view-count domain sweep has a harvest confound and the record contradicts itself on E107, so E109 is superseded rather than executed.

## Next

Run the control experiment that decides the view-count line: does the need/random star gap survive when both arms are drawn from the SAME star-sorted topic pool and classified only afterwards?

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/109-pubdev-viewcount/PROTOCOL.md | 88851908e198 | 6056 |

## Commands

0 captured, 0 non-zero exit.

_none_

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
| 1 | 19:18:53 | session_start | Fresh observation: test view-count principle on Pub.dev (Dart/Flutter package registry) |
| 2 | 00:04:27 | artifact | wrote EXPERIMENTS/109-pubdev-viewcount/PROTOCOL.md |
| 3 | 00:04:28 | milestone | Recovered context; found the view-count domain sweep has a harvest confound and the record contradicts itself on E107. E109 (Pub.dev) is superseded by |
| 4 | 00:04:35 | session_end | Stale session recovered (started 2026-10-11T19:18 by a process that died). Wrote E109 PROTOCOL.md for Pub.dev but ran no fetch. On recovery, inspectio |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-044-fresh-observation-test-view-count-princi/events.jsonl
```
