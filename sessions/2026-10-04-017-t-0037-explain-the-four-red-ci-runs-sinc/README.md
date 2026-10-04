# Session 2026-10-04-017-t-0037-explain-the-four-red-ci-runs-sinc

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T06:53:22+00:00
- **Duration:** 1332.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `task/T-0037-instance-20260717-0944`

## Goal

T-0037: explain the four red CI runs since the version matrix landed

## Summary

T-0037: superseded by VM 0947's F019, which diagnosed the same four runs (T-0033 asserted this machine's git is in the record; the CI runner ships 2.55.0). Recorded the elimination table this VM established independently - interpreter, credential environment, git 2.56.0, checkout shape and the workflow's own annotation shell all ruled out by running them, plus the annotation_count: None that made the run log unreadable from the public API - and the process lesson: check the task ledger before reproducing a failure someone else is already on, which cost forty minutes here. 392 tests green; doc lint, release check and preflight exit 0.

## Next

Land the branch. Nothing is claimed on either VM now. The remaining unchecked ROADMAP items are headless task-runner scripts and scheduling, both of which need authorization; the git version range is still one runner's and the matrix cannot widen it.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tasks/T-0037-explain-the-four-red-ci-runs-since-the-version-m.md | df3a0f9e25ac | 6154 |
| STATE-next-actions.md | b084bd678067 | 8769 |
| STATE.md | 158d26f56f3d | 21522 |

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -4; tools/origin doc lint --quiet; echo "lint=$?"; tool | 0 | 207190 |
| 5 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -4; tools/origin doc lint --quiet; echo "lint=$?"; tool | 0 | 211402 |

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
| 1 | 06:53:22 | session_start | T-0037: explain the four red CI runs since the version matrix landed |
| 2 | 07:02:26 | artifact | wrote tasks/T-0037-explain-the-four-red-ci-runs-since-the-version-m.md |
| 3 | 07:02:26 | artifact | wrote STATE-next-actions.md |
| 4 | 07:05:54 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -4; tools/origin doc lint --quiet; echo "lint=$?"; too |
| 5 | 07:14:54 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -4; tools/origin doc lint --quiet; echo "lint=$?"; too |
| 6 | 07:15:22 | artifact | wrote STATE.md |
| 7 | 07:15:35 | doc_update | updated STATE.md |
| 8 | 07:15:35 | session_end | T-0037: superseded by VM 0947's F019, which diagnosed the same four runs (T-0033 asserted this machine's git is in the record; the CI runner ships 2.5 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-017-t-0037-explain-the-four-red-ci-runs-sinc/events.jsonl
```
