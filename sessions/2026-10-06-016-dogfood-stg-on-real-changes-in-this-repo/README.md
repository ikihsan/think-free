# Session 2026-10-06-016-dogfood-stg-on-real-changes-in-this-repo

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T23:19:22+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Dogfood stg on real changes in this repo; record observed friction vs git workflow alternatives

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/043-real-changes/README.md | 56acec038c70 | 9535 |
| EXPERIMENTS/043-real-changes/raw/results.jsonl | 52c59bf5afe5 | 835617 |
| EXPERIMENTS/043-real-changes/raw/manifest.jsonl | 961359bf22a2 | 70485 |
| EXPERIMENTS/043-real-changes/raw/run.log | 858d3d8fa0dc | 503 |
| EXPERIMENTS/043-real-changes/PROTOCOL.md | 69620661266e | 6760 |
| FAILURES-findings-29.md | 04efd4b8bd6f | 10692 |
| DECISIONS-SCREENING-12.md | 9b64e723423d | 6899 |
| EXPERIMENTS/046-real-changes/README.md | fc20bb817d30 | 9535 |
| EXPERIMENTS/046-real-changes/raw/results.jsonl | 52c59bf5afe5 | 835617 |
| FAILURES-findings-30.md | 7d010db63a69 | 10692 |
| DECISIONS-SCREENING-12.md | 08d0dc6522cc | 7706 |
| EXPERIMENTS/046-real-changes/PROTOCOL.md | a78b2f05c35b | 6760 |

## Commands

0 captured, 0 non-zero exit.

_none_

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
| 1 | 23:19:22 | session_start | Dogfood stg on real changes in this repo; record observed friction vs git workflow alternatives |
| 2 | 00:22:54 | task_rewrite | appended a create record for T-0082 |
| 3 | 00:23:44 | base_advance | sync land: base moved ab4faeb1fb30 -> 363c6b7c1183, 1 commit(s) arrived from the shared base |
| 4 | 00:23:51 | task_rewrite | rewrote tasks/T-0082-e043-measure-stg-on-real-repository-changes-rena.md (status: claimed) |
| 5 | 00:23:51 | task_rewrite | appended a claim record for T-0082 |
| 6 | 00:24:17 | milestone | T-0082 claimed and published; corpus sources chosen (this repo's history + two independent public clones); experiment declared before measurement |
| 7 | 01:38:16 | milestone | E043 run with three fixes: new-file rendering, duplicate anchors, no-op pairs; corpus re-run in progress |
| 8 | 02:06:29 | milestone | fourth defect found (silently merged lines on an unterminated file), fixed with a named refusal; 37 tests green; final corpus run in progress |
| 9 | 04:44:57 | artifact | wrote EXPERIMENTS/043-real-changes/README.md |
| 10 | 04:44:58 | artifact | wrote EXPERIMENTS/043-real-changes/raw/results.jsonl |
| 11 | 04:44:59 | artifact | wrote EXPERIMENTS/043-real-changes/raw/manifest.jsonl |
| 12 | 04:45:00 | artifact | wrote EXPERIMENTS/043-real-changes/raw/run.log |
| 13 | 04:45:00 | artifact | wrote EXPERIMENTS/043-real-changes/PROTOCOL.md |
| 14 | 04:45:01 | artifact | wrote FAILURES-findings-29.md |
| 15 | 04:45:02 | artifact | wrote DECISIONS-SCREENING-12.md |
| 16 | 04:47:05 | task_rewrite | rewrote tasks/T-0082-e043-measure-stg-on-real-repository-changes-rena.md (status: done) |
| 17 | 04:47:05 | task_rewrite | appended a complete record for T-0082 |
| 18 | 05:14:05 | artifact | wrote EXPERIMENTS/046-real-changes/README.md |
| 19 | 05:14:06 | artifact | wrote EXPERIMENTS/046-real-changes/raw/results.jsonl |
| 20 | 05:14:07 | artifact | wrote FAILURES-findings-30.md |
| 21 | 05:14:07 | artifact | wrote DECISIONS-SCREENING-12.md |
| 22 | 05:14:08 | artifact | wrote EXPERIMENTS/046-real-changes/PROTOCOL.md |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-016-dogfood-stg-on-real-changes-in-this-repo/events.jsonl
```
