# Session 2026-10-16-001-test-whether-need-type-stateless-questio

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-16T02:31:59+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test whether need-type (stateless question vs stateful/verifiable task) predicts assistant-served share, using already-harvested public corpora, as the population-selection rule 18 view-count experiments lacked

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/168-version-pinned-need/RESULT.md | aad0645abdd9 | 8219 |
| EXPERIMENTS/168-version-pinned-need/PROTOCOL.md | 7fcfb3ba7d93 | 7141 |
| EXPERIMENTS/168-version-pinned-need/grades-unaided.jsonl | c42440e7b21d | 8622 |
| EXPERIMENTS/168-version-pinned-need/classified.jsonl | 6752ddf43fa4 | 101591 |
| EXPERIMENTS/168-version-pinned-need/attempts_a.py | 366d9c15e770 | 5341 |
| EXPERIMENTS/168-version-pinned-need/attempts_b.py | d4a5b00e75b9 | 7723 |
| EXPERIMENTS/168-version-pinned-need/attempts_c.py | a990e27d56f6 | 3417 |
| EXPERIMENTS/168-version-pinned-need/threads.json | 74e5895f11e6 | 208023 |
| EXPERIMENTS/168-version-pinned-need/grades.py | db4e33123c86 | 11335 |
| EXPERIMENTS/168-version-pinned-need/classify.py | f98c06aa8d53 | 10664 |
| EXPERIMENTS/168-version-pinned-need/fetch_threads.py | 07dad0778edb | 3963 |
| EXPERIMENTS/168-version-pinned-need/make_view.py | eabe75605cde | 3724 |

## Commands

11 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/168-version-pinned-need/make_view.py'] | 0 | 203 |
| 3 | ['python3', 'EXPERIMENTS/168-version-pinned-need/make_view.py'] | 0 | 211 |
| 4 | ['python3', 'EXPERIMENTS/168-version-pinned-need/classify.py'] | 0 | 189 |
| 5 | ['python3', 'EXPERIMENTS/168-version-pinned-need/fetch_threads.py'] | 0 | 1888 |
| 6 | ['python3', 'EXPERIMENTS/168-version-pinned-need/fetch_threads.py'] | 0 | 38298 |
| 7 | ['python3', 'EXPERIMENTS/168-version-pinned-need/grades.py'] | 0 | 113 |
| 10 | ['python3', 'EXPERIMENTS/168-version-pinned-need/grades.py'] | 0 | 818 |
| 14 | ['python3', 'tools/origin', 'doc', 'lint'] | 1 | 4416 |
| 23 | ['tools/origin', 'doc', 'lint'] | 2 | 357563 |
| 24 | ['tools/origin', 'doc', 'lint'] | 2 | 788989 |
| 25 | ['tools/origin', 'doc', 'lint'] | 0 | 465306 |

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
| 1 | 02:31:59 | session_start | Test whether need-type (stateless question vs stateful/verifiable task) predicts assistant-served share, using already-harvested public corpora, as th |
| 2 | 02:34:05 | command | $ python3 EXPERIMENTS/168-version-pinned-need/make_view.py |
| 3 | 02:35:03 | command | $ python3 EXPERIMENTS/168-version-pinned-need/make_view.py |
| 4 | 02:36:00 | command | $ python3 EXPERIMENTS/168-version-pinned-need/classify.py |
| 5 | 02:38:14 | command | $ python3 EXPERIMENTS/168-version-pinned-need/fetch_threads.py |
| 6 | 02:39:23 | command | $ python3 EXPERIMENTS/168-version-pinned-need/fetch_threads.py |
| 7 | 02:40:37 | command | $ python3 EXPERIMENTS/168-version-pinned-need/grades.py |
| 8 | 02:41:22 | artifact | wrote EXPERIMENTS/168-version-pinned-need/RESULT.md |
| 9 | 02:41:25 | milestone | G1 and G2 pass: version-pinned class is 28.4% of the pool, assistant serves it 0.4583 vs 0.675 baseline |
| 10 | 02:46:30 | command | $ python3 EXPERIMENTS/168-version-pinned-need/grades.py |
| 11 | 02:46:34 | artifact | wrote EXPERIMENTS/168-version-pinned-need/PROTOCOL.md |
| 12 | 02:46:37 | artifact | wrote EXPERIMENTS/168-version-pinned-need/grades-unaided.jsonl |
| 13 | 02:46:40 | artifact | wrote EXPERIMENTS/168-version-pinned-need/classified.jsonl |
| 14 | 02:46:56 | command | $ python3 tools/origin doc lint |
| 15 | 02:50:31 | artifact | wrote EXPERIMENTS/168-version-pinned-need/attempts_a.py |
| 16 | 02:50:33 | artifact | wrote EXPERIMENTS/168-version-pinned-need/attempts_b.py |
| 17 | 02:50:35 | artifact | wrote EXPERIMENTS/168-version-pinned-need/attempts_c.py |
| 18 | 02:50:37 | artifact | wrote EXPERIMENTS/168-version-pinned-need/threads.json |
| 19 | 02:50:39 | artifact | wrote EXPERIMENTS/168-version-pinned-need/grades.py |
| 20 | 02:50:41 | artifact | wrote EXPERIMENTS/168-version-pinned-need/classify.py |
| 21 | 02:50:43 | artifact | wrote EXPERIMENTS/168-version-pinned-need/fetch_threads.py |
| 22 | 02:50:47 | artifact | wrote EXPERIMENTS/168-version-pinned-need/make_view.py |
| 23 | 02:56:47 | command | $ tools/origin doc lint |
| 24 | 03:15:22 | command | $ tools/origin doc lint |
| 25 | 03:23:42 | command | $ tools/origin doc lint |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-16-001-test-whether-need-type-stateless-questio/events.jsonl
```
