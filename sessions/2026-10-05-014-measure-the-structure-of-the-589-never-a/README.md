# Session 2026-10-05-014-measure-the-structure-of-the-589-never-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T16:02:10+00:00
- **Duration:** 639.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure the structure of the 589 never-answered need statements (the corpus's last open reading)

## Summary

E026: the unserved tail of the E022 corpus is diffuse in length and trigger; B2 fired on 9 rows and is withdrawn by sensitivity (F046, D058). The corpus's last open reading is closed.

## Next

E2 side C is time-gated to ~2026-10-10; otherwise the inventory holds no live agent-side candidate.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tasks/CLAIMS.jsonl | 8ab074dc011b | 72445 |
| tasks/T-0070-classify-the-589-never-answered-need-statements.md | 19c47d43fcde | 1254 |
| DECISIONS-SCREENING-3.md | 30cdc983e86d | 13743 |
| DECISIONS.md | 7e989a3aa2a9 | 8190 |
| EXPERIMENTS/026-unserved-need-structure/PROTOCOL.md | 550c2ab73235 | 3279 |
| EXPERIMENTS/026-unserved-need-structure/README.md | 7000aec33edf | 2520 |
| EXPERIMENTS/026-unserved-need-structure/fetch_texts.py | abbf05f3dc9a | 2000 |
| EXPERIMENTS/026-unserved-need-structure/raw/texts.jsonl | 19b4bb4de66a | 868298 |
| EXPERIMENTS/026-unserved-need-structure/results.json | 3c9078c750fc | 1705 |
| EXPERIMENTS/026-unserved-need-structure/stats.py | 953dbea92ae0 | 3020 |
| FAILURES-findings-19.md | c7a0b9ac8b79 | 7375 |
| FAILURES.md | b365dd98055a | 14073 |
| HYPOTHESES.md | 2a53a127bc9b | 17423 |

## Commands

3 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 6 | ['python3', 'EXPERIMENTS/026-unserved-need-structure/fetch_texts.py'] | 0 | 109177 |
| 7 | ['python3', 'EXPERIMENTS/026-unserved-need-structure/stats.py'] | 0 | 401 |
| 8 | ['python3', 'EXPERIMENTS/026-unserved-need-structure/stats.py'] | 0 | 199 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 11 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-3.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/026-unserved-need-structure/PROTOCOL.md |
|   undeclared | EXPERIMENTS/026-unserved-need-structure/README.md |
|   undeclared | EXPERIMENTS/026-unserved-need-structure/fetch_texts.py |
|   undeclared | EXPERIMENTS/026-unserved-need-structure/raw/texts.jsonl |
|   undeclared | EXPERIMENTS/026-unserved-need-structure/results.json |
|   undeclared | EXPERIMENTS/026-unserved-need-structure/stats.py |
|   undeclared | FAILURES-findings-19.md |
|   undeclared | FAILURES.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:02:10 | session_start | Measure the structure of the 589 never-answered need statements (the corpus's last open reading) |
| 2 | 16:02:17 | task_rewrite | appended a create record for T-0070 |
| 3 | 16:02:32 | task_rewrite | appended a create record for T-0071 |
| 4 | 16:03:13 | task_rewrite | rewrote tasks/T-0070-classify-the-589-never-answered-need-statements.md (status: claimed) |
| 5 | 16:03:13 | task_rewrite | appended a claim record for T-0070 |
| 6 | 16:06:06 | command | $ python3 EXPERIMENTS/026-unserved-need-structure/fetch_texts.py |
| 7 | 16:06:40 | command | $ python3 EXPERIMENTS/026-unserved-need-structure/stats.py |
| 8 | 16:07:32 | command | $ python3 EXPERIMENTS/026-unserved-need-structure/stats.py |
| 9 | 16:10:47 | milestone | E026 measured and F046/D058 recorded |
| 10 | 16:11:01 | experiment_result | the 589 unanswered need statements are diffuse in length (ratio 0.948) and trigger (chi2 p~0.06); the one gate that fired (B2, two triggers at >=2x sh |
| 11 | 16:11:32 | task_rewrite | rewrote tasks/T-0070-classify-the-589-never-answered-need-statements.md (status: done) |
| 12 | 16:11:32 | task_rewrite | appended a complete record for T-0070 |
| 13 | 16:12:49 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-3.md |
| 14 | 16:12:49 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 15 | 16:12:49 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/026-unserved-need-structure/PROTOCOL.md |
| 16 | 16:12:49 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/026-unserved-need-structure/README.md |
| 17 | 16:12:49 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/026-unserved-need-structure/fetch_texts.py |
| 18 | 16:12:49 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/026-unserved-need-structure/raw/texts.jsonl |
| 19 | 16:12:49 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/026-unserved-need-structure/results.json |
| 20 | 16:12:49 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/026-unserved-need-structure/stats.py |
| 21 | 16:12:49 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-19.md |
| 22 | 16:12:49 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 23 | 16:12:49 | unlogged_change | changed but never declared as an artifact: HYPOTHESES.md |
| 24 | 16:12:49 | doc_update | updated DECISIONS-SCREENING-3.md |
| 25 | 16:12:49 | doc_update | updated DECISIONS.md |
| 26 | 16:12:49 | doc_update | updated FAILURES.md |
| 27 | 16:12:49 | doc_update | updated HYPOTHESES.md |
| 28 | 16:12:49 | session_end | E026: the unserved tail of the E022 corpus is diffuse in length and trigger; B2 fired on 9 rows and is withdrawn by sensitivity (F046, D058). The corp |
| 29 | 16:14:37 | artifact | wrote tasks/CLAIMS.jsonl |
| 30 | 16:14:37 | artifact | wrote tasks/T-0070-classify-the-589-never-answered-need-statements.md |
| 31 | 16:14:38 | artifact | wrote DECISIONS-SCREENING-3.md |
| 32 | 16:14:38 | artifact | wrote DECISIONS.md |
| 33 | 16:14:39 | artifact | wrote EXPERIMENTS/026-unserved-need-structure/PROTOCOL.md |
| 34 | 16:14:40 | artifact | wrote EXPERIMENTS/026-unserved-need-structure/README.md |
| 35 | 16:14:40 | artifact | wrote EXPERIMENTS/026-unserved-need-structure/fetch_texts.py |
| 36 | 16:14:41 | artifact | wrote EXPERIMENTS/026-unserved-need-structure/raw/texts.jsonl |
| 37 | 16:14:42 | artifact | wrote EXPERIMENTS/026-unserved-need-structure/results.json |
| 38 | 16:14:43 | artifact | wrote EXPERIMENTS/026-unserved-need-structure/stats.py |
| 39 | 16:14:43 | artifact | wrote FAILURES-findings-19.md |
| 40 | 16:14:44 | artifact | wrote FAILURES.md |
| 41 | 16:14:44 | artifact | wrote HYPOTHESES.md |
| 42 | 16:14:45 | doc_update | updated DECISIONS-SCREENING-3.md |
| 43 | 16:14:45 | doc_update | updated DECISIONS.md |
| 44 | 16:14:45 | doc_update | updated FAILURES.md |
| 45 | 16:14:45 | doc_update | updated HYPOTHESES.md |
| 46 | 16:14:45 | session_end | E026: the unserved tail of the E022 corpus is diffuse in length and trigger; B2 fired on 9 rows and is withdrawn by sensitivity (F046, D058). The corp |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-014-measure-the-structure-of-the-589-never-a/events.jsonl
```
