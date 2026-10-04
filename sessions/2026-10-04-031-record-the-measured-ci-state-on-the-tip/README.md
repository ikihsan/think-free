# Session 2026-10-04-031-record-the-measured-ci-state-on-the-tip

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T11:15:37+00:00
- **Duration:** 311.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Record the measured CI state on the tip, and the first red run whose cause was read off a filed annotation (T-0049)

## Summary

Recorded the measured CI state on the tip (green, 37198002763 at 09e18b0) and the run census: ten runs, seven red causes read off annotations with zero reproduction. Run 37197291442 is the first red run whose cause came off an annotation the annotator filed - the offending file at line 70. Found and repaired the fetcher's own rate-limit handling, which had written 403s over two captures it already held.

## Next

Fetch arms F-J of EXPERIMENTS/010 once the hourly unauthenticated limit resets; STATE-defects.md (299) and FAILURES-findings-4.md (297) need a split for their next entry, and STATE-defects.md cannot be split inside its numbered list without defectlist.py reading more than one file. Two open questions worth a look: the experiment_result doc obligation is 'all' of HYPOTHESES.md and FAILURES.md while session-protocol.md says 'the same applies' as the decision rule's 'any one' - a false positive on a correct session; and a taskless session publishing a code commit is red on the session step by construction.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/010-annotation-rendering/README.md | dcb414d627eb | 11526 |
| EXPERIMENTS/010-annotation-rendering/fetch_annotations.py | 03a751afcd93 | 8162 |
| EXPERIMENTS/010-annotation-rendering/raw/summary.json | fbd34fc425bc | 2359 |
| docs/operations/ci-diagnosis.md | 4f49b4b8f789 | 12140 |
| STATE.md | dfb7b6e4d771 | 23451 |

## Commands

2 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/010-annotation-rendering/fetch_annotations.py'] | 0 | 6379 |
| 3 | ['python3', 'EXPERIMENTS/010-annotation-rendering/fetch_annotations.py'] | 3 | 246 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | tasks/T-0049-record-the-measured-ci-state-on-the-tip-and-the.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:15:37 | session_start | Record the measured CI state on the tip, and the first red run whose cause was read off a filed annotation (T-0049) |
| 2 | 11:16:23 | command | $ python3 EXPERIMENTS/010-annotation-rendering/fetch_annotations.py |
| 3 | 11:17:01 | command | $ python3 EXPERIMENTS/010-annotation-rendering/fetch_annotations.py |
| 4 | 11:19:46 | artifact | wrote EXPERIMENTS/010-annotation-rendering/README.md |
| 5 | 11:19:47 | artifact | wrote EXPERIMENTS/010-annotation-rendering/fetch_annotations.py |
| 6 | 11:19:47 | artifact | wrote EXPERIMENTS/010-annotation-rendering/raw/summary.json |
| 7 | 11:19:48 | artifact | wrote docs/operations/ci-diagnosis.md |
| 8 | 11:19:48 | artifact | wrote STATE.md |
| 9 | 11:19:49 | milestone | census recorded: ten runs, seven red causes read from annotations, none reproduced; the fetcher's own limit handling found by running it |
| 10 | 11:20:09 | milestone | T-0049 committed |
| 11 | 11:20:48 | unlogged_change | changed but never declared as an artifact: tasks/T-0049-record-the-measured-ci-state-on-the-tip-and-the.md |
| 12 | 11:20:48 | doc_update | updated STATE.md |
| 13 | 11:20:48 | session_end | Recorded the measured CI state on the tip (green, 37198002763 at 09e18b0) and the run census: ten runs, seven red causes read off annotations with zer |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-031-record-the-measured-ci-state-on-the-tip/events.jsonl
```
