# Session 2026-10-08-005-fresh-observation-measure-whether-a-proj

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T02:10:26+00:00
- **Duration:** 5851.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation: measure whether a project's own tests, read statically, locate the code a real test run reports unexercised, and build a no-run worklist prototype if they agree

## Summary

E057 population gate for the no-run worklist idea fired on its own declared gate: 0 of 30 coveragepy, 0 of 1 vulture, 0 of 13 pytest-cov rows state 'tell me which code no test exercises without running the suite'. Prototype condition false, no prototype written, candidate not opened. Two of ten search arms returned HTTP 422 on a misspelled repo: owner and produced no observation, which is now D081 (a missing observation is never a zero and never a denominator) and was applied backwards to E056's own verdict (F087/F089).

## Next

Fresh observation for a new candidate; do not reopen the no-run worklist or the docs-drift line.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/057-no-run-worklist/README.md | d79698fdf6e5 | 7842 |
| EXPERIMENTS/057-no-run-worklist/harvest.py | 5e4270afbf74 | 3593 |
| EXPERIMENTS/057-no-run-worklist/harvest2.py | a9b5ac4f3830 | 2777 |
| EXPERIMENTS/057-no-run-worklist/raw/requests-2.jsonl | 294eaf281fe4 | 141237 |
| EXPERIMENTS/057-no-run-worklist/raw/requests.jsonl | e4b0f18858d7 | 182773 |
| FAILURES-findings-32.md | c2148fd2a962 | 5931 |
| EXPERIMENTS/056-docs-cli-drift/README.md | 15da5112b054 | 3964 |
| EXPERIMENTS/057-no-run-worklist/README.md | d79698fdf6e5 | 7842 |
| DECISIONS-SCREENING-13.md | 2440e384a94c | 9896 |
| FAILURES.md | d36b8f8f0fd9 | 52786 |
| DECISIONS.md | 05f21cd5d94d | 13485 |
| STATE.md | 5b85728f75c8 | 38329 |

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '/tmp/opencode/e057_pop/harvest.py'] | 0 | 62196 |
| 3 | ['python3', '/tmp/opencode/e057_pop/harvest2.py'] | 0 | 20083 |

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
| 1 | 02:10:26 | session_start | Fresh observation: measure whether a project's own tests, read statically, locate the code a real test run reports unexercised, and build a no-run wor |
| 2 | 02:31:22 | command | $ python3 /tmp/opencode/e057_pop/harvest.py |
| 3 | 02:36:18 | command | $ python3 /tmp/opencode/e057_pop/harvest2.py |
| 4 | 02:40:33 | milestone | E057 population gate for the no-run worklist idea: 0 of 30 rows in coveragepy, 0 of 1 in vulture, 0 of 13 in pytest-cov state the declared need; kill  |
| 5 | 02:40:39 | artifact | wrote EXPERIMENTS/057-no-run-worklist/README.md |
| 6 | 02:40:40 | artifact | wrote EXPERIMENTS/057-no-run-worklist/harvest.py |
| 7 | 02:40:42 | artifact | wrote EXPERIMENTS/057-no-run-worklist/harvest2.py |
| 8 | 02:40:44 | artifact | wrote EXPERIMENTS/057-no-run-worklist/raw/requests-2.jsonl |
| 9 | 02:40:47 | artifact | wrote EXPERIMENTS/057-no-run-worklist/raw/requests.jsonl |
| 10 | 02:55:29 | artifact | wrote FAILURES-findings-32.md |
| 11 | 02:55:31 | artifact | wrote EXPERIMENTS/056-docs-cli-drift/README.md |
| 12 | 02:55:36 | artifact | wrote EXPERIMENTS/057-no-run-worklist/README.md |
| 13 | 02:55:38 | artifact | wrote DECISIONS-SCREENING-13.md |
| 14 | 02:55:40 | artifact | wrote FAILURES.md |
| 15 | 02:55:43 | artifact | wrote DECISIONS.md |
| 16 | 02:56:46 | artifact | wrote STATE.md |
| 17 | 03:47:57 | doc_update | updated DECISIONS-SCREENING-13.md |
| 18 | 03:47:57 | doc_update | updated DECISIONS.md |
| 19 | 03:47:57 | doc_update | updated FAILURES.md |
| 20 | 03:47:57 | doc_update | updated STATE.md |
| 21 | 03:47:57 | session_end | E057 population gate for the no-run worklist idea fired on its own declared gate: 0 of 30 coveragepy, 0 of 1 vulture, 0 of 13 pytest-cov rows state 't |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-005-fresh-observation-measure-whether-a-proj/events.jsonl
```
