# Session 2026-10-16-001-test-whether-need-type-stateless-questio

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-16T02:31:59+00:00
- **Duration:** 3971.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test whether need-type (stateless question vs stateful/verifiable task) predicts assistant-served share, using already-harvested public corpora, as the population-selection rule 18 view-count experiments lacked

## Summary

E168: found the first positive structural reading of why the strongest alternative wins. E126's 13 unserved rows were never characterised; they all fail on version-pinned facts. Stratifying the same 299-row pool on that property gives 85/299 = 0.2843 version-pinned (Wilson 0.2361-0.3379), 14x E126's program-shaped residue; the assistant serves the high-arrival end at 11/24 = 0.4583 vs E126's pool-level 0.675 (Fisher p 0.1168, not significant). G1 and G2 pass as declared; G3 (does version-history grounding recover the failures) is unrun and is the gate that would license a build. D113 requires future service screens to stratify on version-dependence.

## Next

Run E168's G3 on a fresh blinded version_pinned sample, grounded arm allowed only the post plus the component's published release notes/migration guide; then the prior-art screen against the class before any product code. Two instrument defects this session were caught by arithmetic, not code: a str/int question_id collision that would have silently dropped the blinding for 20 rows, and filter=withbody not populating answers, which returned 0 answers for all 24 threads.

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
| undeclared file changes | 24 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-RECORDS-2.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/165-golang-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/165-golang-viewcount/RESULT.md |
|   undeclared | EXPERIMENTS/165-golang-viewcount/classified.json |
|   undeclared | EXPERIMENTS/165-golang-viewcount/classify.py |
|   undeclared | EXPERIMENTS/165-golang-viewcount/gate_results.json |
|   undeclared | EXPERIMENTS/165-golang-viewcount/harvest.py |
|   undeclared | EXPERIMENTS/165-golang-viewcount/measure.py |
|   undeclared | EXPERIMENTS/165-golang-viewcount/raw_harvest.json |

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
| 26 | 03:38:10 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-2.md |
| 27 | 03:38:10 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 28 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/PROTOCOL.md |
| 29 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/RESULT.md |
| 30 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/classified.json |
| 31 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/classify.py |
| 32 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/gate_results.json |
| 33 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/harvest.py |
| 34 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/measure.py |
| 35 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/raw_harvest.json |
| 36 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/run.py |
| 37 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md |
| 38 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-vscode-marketplace-viewcount/fetch_extensions.py |
| 39 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-vscode-marketplace-viewcount/raw_data.json |
| 40 | 03:38:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/168-version-pinned-need/attempts_written_before_fetch.json |
| 45 | 03:38:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-028-fresh-observation-test-view-count-princi/commands.log |
| 46 | 03:38:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-028-fresh-observation-test-view-count-princi/events.jsonl |
| 47 | 03:38:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-029-fresh-observation-in-a-new-domain-test-t/commands.log |
| 48 | 03:38:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-029-fresh-observation-in-a-new-domain-test-t/events.jsonl |
| 49 | 03:38:11 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-030-log-remaining-artifacts-from-e165-experi/events.jsonl |
| 50 | 03:38:11 | doc_update | updated DECISIONS-RECORDS-2.md |
| 51 | 03:38:11 | doc_update | updated DECISIONS.md |
| 52 | 03:38:11 | doc_update | updated FAILURES.md |
| 53 | 03:38:11 | doc_update | updated STATE.md |
| 54 | 03:38:11 | session_end | E168: found the first positive structural reading of why the strongest alternative wins. E126's 13 unserved rows were never characterised; they all fa |

_4 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-16-001-test-whether-need-type-stateless-questio/events.jsonl
```
