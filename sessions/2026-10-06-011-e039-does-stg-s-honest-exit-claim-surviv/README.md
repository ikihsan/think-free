# Session 2026-10-06-011-e039-does-stg-s-honest-exit-claim-surviv

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T11:11:16+00:00
- **Duration:** 451.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E039: does stg's honest-exit claim survive the failure modes an agent workflow produces

## Summary

E039 complete: stg's honest-exit claim holds on all 8 boundary failure modes; naive route exits 128 on 5 and silently stages on 3

## Next

KILL-Q remains not_evaluated by five experiments; candidate's capability, prior-art narrowing, and boundary honesty are now all measured

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/039-honest-exit/README.md | 3cc56015b8f7 | 3869 |
| EXPERIMENTS/039-honest-exit/run.py | 9029135c1624 | 6921 |
| EXPERIMENTS/039-honest-exit/raw/results.jsonl | 92c2a8c97b28 | 1649 |
| EXPERIMENTS/039-honest-exit/raw/naive.jsonl | f7b9885ce326 | 1105 |
| HYPOTHESES-candidates.md | be271a29c74a | 9182 |
| STATE.md | 170bb51fd544 | 37169 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/039-honest-exit/run.py'] | 0 | 2697 |

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
| 1 | 11:11:16 | session_start | E039: does stg's honest-exit claim survive the failure modes an agent workflow produces |
| 2 | 11:15:49 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/039-honest-exit/run.py |
| 3 | 11:17:45 | artifact | wrote EXPERIMENTS/039-honest-exit/README.md |
| 4 | 11:17:45 | artifact | wrote EXPERIMENTS/039-honest-exit/run.py |
| 5 | 11:17:46 | artifact | wrote EXPERIMENTS/039-honest-exit/raw/results.jsonl |
| 6 | 11:17:46 | artifact | wrote EXPERIMENTS/039-honest-exit/raw/naive.jsonl |
| 7 | 11:17:47 | artifact | wrote HYPOTHESES-candidates.md |
| 8 | 11:17:48 | artifact | wrote STATE.md |
| 9 | 11:18:48 | doc_update | updated STATE.md |
| 10 | 11:18:48 | session_end | E039 complete: stg's honest-exit claim holds on all 8 boundary failure modes; naive route exits 128 on 5 and silently stages on 3 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-011-e039-does-stg-s-honest-exit-claim-surviv/events.jsonl
```
