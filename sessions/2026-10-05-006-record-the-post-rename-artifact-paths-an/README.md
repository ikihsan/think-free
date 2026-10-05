# Session 2026-10-05-006-record-the-post-rename-artifact-paths-an

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T07:33:13+00:00
- **Duration:** 59.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Record the post-rename artifact paths and the HYPOTHESES entry that the closed session could not

## Summary

Recorded the post-rename artifact paths and the HYPOTHESES entry the closed session could not write, after the reconciliation named five artifacts under their pre-rename path.

## Next

Rerun H2's low band from a host Sourcegraph will answer; the slice is declared mechanically.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/021-copied-artifact-serving/PROTOCOL.md | 95e7a0463dca | 9526 |
| EXPERIMENTS/021-copied-artifact-serving/results.json | a4626bdaaba7 | 10234 |
| EXPERIMENTS/021-copied-artifact-serving/coverage.json | 45d005318e39 | 10683 |
| EXPERIMENTS/021-copied-artifact-serving/copycount.json | 829a3e01a14e | 46013 |
| EXPERIMENTS/021-copied-artifact-serving/forkstatus.json | bea94793549d | 4763 |
| HYPOTHESES.md | 1d2b0d198c29 | 12921 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-05-004-measure-whether-the-young-vocabulary-is/events.jsonl |
|   error | FAILURES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 07:33:13 | session_start | Record the post-rename artifact paths and the HYPOTHESES entry that the closed session could not |
| 2 | 07:33:31 | artifact | wrote EXPERIMENTS/021-copied-artifact-serving/PROTOCOL.md |
| 3 | 07:33:31 | artifact | wrote EXPERIMENTS/021-copied-artifact-serving/results.json |
| 4 | 07:33:32 | artifact | wrote EXPERIMENTS/021-copied-artifact-serving/coverage.json |
| 5 | 07:33:32 | artifact | wrote EXPERIMENTS/021-copied-artifact-serving/copycount.json |
| 6 | 07:33:33 | artifact | wrote EXPERIMENTS/021-copied-artifact-serving/forkstatus.json |
| 7 | 07:33:53 | artifact | wrote HYPOTHESES.md |
| 8 | 07:33:53 | experiment_result | H1 dead at a ratio of 0.118: 1,026 indexed repositories hold a .claude/hooks/ directory against 8,676 monthly installs, so the channel the screen was  |
| 9 | 07:34:12 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-05-004-measure-whether-the-young-vocabulary-is/events.jsonl |
| 10 | 07:34:13 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 11 | 07:34:13 | doc_update | updated HYPOTHESES.md |
| 12 | 07:34:13 | session_end | Recorded the post-rename artifact paths and the HYPOTHESES entry the closed session could not write, after the reconciliation named five artifacts und |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-006-record-the-post-rename-artifact-paths-an/events.jsonl
```
