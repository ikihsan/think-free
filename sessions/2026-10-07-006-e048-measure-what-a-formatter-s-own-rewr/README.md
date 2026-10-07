# Session 2026-10-07-006-e048-measure-what-a-formatter-s-own-rewr

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-07T12:32:45+00:00
- **Duration:** 986.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E048: measure what a formatter's own rewrite does to a partially-staged file's unstaged hunks

## Summary

E048 measured the user-visible disagreement between a formatted worktree and an unformatted commit: loud in 8 of 9 configurations, silent only for lefthook without stage_fixed (whose remedy ships in the same tool and whose commit a CI format gate fails). Nothing to build; F085. F085 indexed in FAILURES.md. Doc lint OK.

## Next

Owner decision on item 0; the seat for a candidate remains empty, measured seven ways.

## Artifacts

_none_

## Commands

8 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/048-formatter-review/harness.py'] | 0 | 32212 |
| 3 | ['python3', 'EXPERIMENTS/048-formatter-review/harness.py'] | 0 | 32470 |
| 4 | ['python3', '-c', "print('ok')"] | 0 | 99 |
| 5 | ['tools/origin', 'doc', 'lint'] | 2 | 153995 |
| 6 | ['tools/origin', 'doc', 'lint'] | 2 | 266483 |
| 7 | ['python3', 'EXPERIMENTS/048-formatter-review/harness.py'] | 0 | 32482 |
| 8 | ['tools/origin', 'doc', 'lint'] | 0 | 53433 |
| 9 | ['tools/origin', 'doc', 'lint'] | 0 | 45334 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 12 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/048-formatter-review/README.md |
|   undeclared | EXPERIMENTS/048-formatter-review/arms.py |
|   undeclared | EXPERIMENTS/048-formatter-review/fixture.py |
|   undeclared | EXPERIMENTS/048-formatter-review/gitenv.py |
|   undeclared | EXPERIMENTS/048-formatter-review/harness.py |
|   undeclared | EXPERIMENTS/048-formatter-review/raw/results.json |
|   undeclared | EXPERIMENTS/048-formatter-review/review.py |
|   undeclared | EXPERIMENTS/048-formatter-review/setup.sh |
|   undeclared | EXPERIMENTS/048-formatter-review/versions.py |
|   undeclared | FAILURES-findings-31.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:32:45 | session_start | E048: measure what a formatter's own rewrite does to a partially-staged file's unstaged hunks |
| 2 | 12:36:00 | command | $ python3 EXPERIMENTS/048-formatter-review/harness.py |
| 3 | 12:37:32 | command | $ python3 EXPERIMENTS/048-formatter-review/harness.py |
| 4 | 12:41:02 | command | $ python3 -c print('ok') |
| 5 | 12:45:02 | command | $ tools/origin doc lint |
| 6 | 12:45:31 | command | $ tools/origin doc lint |
| 7 | 12:46:59 | command | $ python3 EXPERIMENTS/048-formatter-review/harness.py |
| 8 | 12:48:02 | command | $ tools/origin doc lint |
| 9 | 12:49:10 | command | $ tools/origin doc lint |
| 10 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/README.md |
| 11 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/arms.py |
| 12 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/fixture.py |
| 13 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/gitenv.py |
| 14 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/harness.py |
| 15 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/raw/results.json |
| 16 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/review.py |
| 17 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/setup.sh |
| 18 | 12:49:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/048-formatter-review/versions.py |
| 19 | 12:49:11 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-31.md |
| 20 | 12:49:11 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 21 | 12:49:11 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 22 | 12:49:11 | doc_update | updated FAILURES.md |
| 23 | 12:49:11 | doc_update | updated STATE.md |
| 24 | 12:49:11 | session_end | E048 measured the user-visible disagreement between a formatted worktree and an unformatted commit: loud in 8 of 9 configurations, silent only for lef |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-07-006-e048-measure-what-a-formatter-s-own-rewr/events.jsonl
```
