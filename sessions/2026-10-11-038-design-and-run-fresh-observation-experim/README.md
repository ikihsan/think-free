# Session 2026-10-11-038-design-and-run-fresh-observation-experim

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T17:51:21+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Design and run fresh observation experiment testing view-count principle on GitHub code repositories using star counts and issue activity as arrival metrics

## Summary

_(none recorded)_

## Artifacts

_none_

## Commands

1 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/107-github-repos-viewcount/run.py'] | 3 | 81357 |

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
| 1 | 17:51:21 | session_start | Design and run fresh observation experiment testing view-count principle on GitHub code repositories using star counts and issue activity as arrival m |
| 2 | 17:55:56 | command | $ python3 EXPERIMENTS/107-github-repos-viewcount/run.py |
| 3 | 18:00:14 | milestone | E107 experiment completed: G1 FAIL (68.2% arrival), G2 PASS (15.4% need prevalence), G3 FAIL (54% unserved, Wilson upper 65.7%), G4 PASS (16 repos wit |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-038-design-and-run-fresh-observation-experim/events.jsonl
```
