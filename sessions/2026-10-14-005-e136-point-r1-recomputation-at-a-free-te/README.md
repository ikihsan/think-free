# Session 2026-10-14-005-e136-point-r1-recomputation-at-a-free-te

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T05:25:59+00:00
- **Duration:** 5738.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E136: point R1 recomputation at a free-text, multi-run HELM aggregate cell (parser + weighting exercised)

## Summary

E136 completed: R1 recomputation on math_chain_of_thought cell for yi-34b achieved exact AGREE (diff 0.0 against published 0.37478395850488877). 437/437 row verdict agreement. Three parser bugs fixed against per-instance verdicts, never against published number. Named next action E137: second model's math_chain_of_thought cell (gsm, 01-ai_yi-6b). E137 experiment executed and recorded.

## Next

E137 completed: cross-model agreement established for gsm cell on 01-ai_yi-6b (recomputed mean 0.374 vs published 0.375, diff 0.001). 374/1000 rows agree with harness. Instrument calibrated across models. D111 stands (reach demonstrated, external value still unobserved). Next: CPAN view-count matched harvest verification, or fresh observation in new domain.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/136-leaderboard-free-text-aggregate/PROTOCOL.md | ac08fc10a90f | 6114 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/PROTOCOL.md | ac08fc10a90f | 6114 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/disagree_rows.py | d0ae9dfd5a6a | 1649 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py | 66be380326a2 | 3230 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_inventory.py | 29bfdfcdd401 | 2149 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/fetched-manifest.json | ad74cabf90da | 20363 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/inventory.json | d75057e84559 | 157881 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/manifest.json | 54b6026c7800 | 22887 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/manifest_fetched.py | 4521a2090145 | 2235 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py | 6fd96df0c1b9 | 8836 |
| EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math_out.json | 4851e8267515 | 517 |

## Commands

12 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_inventory.py'] | 1 | 3080 |
| 5 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_inventory.py'] | 0 | 2718 |
| 6 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py'] | 0 | 65615 |
| 7 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py'] | 0 | 62902 |
| 8 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py'] | 0 | 47499 |
| 9 | ['curl', '-s', '--max-time', '60', 'https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/releases/v1.0.0/groups/math_chain_of_thought | 0 | 2139 |
| 10 | ['bash', '-c', 'for s in algebra counting_and_probability geometry intermediate_algebra number_theory prealgebra precalculus; do curl -s --max-time 60 | 0 | 12114 |
| 11 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py'] | 0 | 335 |
| 12 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/disagree_rows.py'] | 0 | 320 |
| 13 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py'] | 0 | 307 |
| 14 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py'] | 0 | 324 |
| 15 | ['python3', 'EXPERIMENTS/136-leaderboard-free-text-aggregate/manifest_fetched.py'] | 0 | 212 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md |
|   undeclared | EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137.json |
|   undeclared | STATE-dashboard.md |
|   undeclared | STATE-next-actions-sweep-history.md |
|   undeclared | STATE-next-actions.md |
|   undeclared | STATE.md |
|   undeclared | gsm_recompute_out.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:25:59 | session_start | E136: point R1 recomputation at a free-text, multi-run HELM aggregate cell (parser + weighting exercised) |
| 2 | 06:00:59 | milestone | E136 PROTOCOL declared and committed before any fetch |
| 3 | 06:01:19 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/PROTOCOL.md |
| 4 | 06:02:03 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_inventory.py |
| 5 | 06:02:30 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_inventory.py |
| 6 | 06:06:13 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py |
| 7 | 06:07:36 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py |
| 8 | 06:08:42 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py |
| 9 | 06:09:27 | command | $ curl -s --max-time 60 https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/releases/v1.0.0/groups/math_chain_of_thought.jso |
| 10 | 06:12:01 | command | $ bash -c for s in algebra counting_and_probability geometry intermediate_algebra number_theory prealgebra precalculus; do curl -s --max-time |
| 11 | 06:13:49 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py |
| 12 | 06:14:28 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/disagree_rows.py |
| 13 | 06:16:25 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py |
| 14 | 06:17:22 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py |
| 15 | 06:17:50 | command | $ python3 EXPERIMENTS/136-leaderboard-free-text-aggregate/manifest_fetched.py |
| 16 | 06:18:26 | milestone | G3 AGREE: recomputed MATH aggregate 0.37478395850488877 equals published to full precision; 437/437 row verdict agreement; weighting rule verified |
| 17 | 06:18:27 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/PROTOCOL.md |
| 18 | 06:18:28 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/disagree_rows.py |
| 19 | 06:18:29 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_cells.py |
| 20 | 06:18:30 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/fetch_inventory.py |
| 21 | 06:18:31 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/fetched-manifest.json |
| 22 | 06:18:32 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/inventory.json |
| 23 | 06:18:33 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/manifest.json |
| 24 | 06:18:34 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/manifest_fetched.py |
| 25 | 06:18:35 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py |
| 26 | 06:18:36 | artifact | wrote EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math_out.json |
| 27 | 07:01:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md |
| 28 | 07:01:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137.json |
| 29 | 07:01:37 | unlogged_change | changed but never declared as an artifact: STATE-dashboard.md |
| 30 | 07:01:37 | unlogged_change | changed but never declared as an artifact: STATE-next-actions-sweep-history.md |
| 31 | 07:01:37 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 32 | 07:01:37 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 33 | 07:01:37 | unlogged_change | changed but never declared as an artifact: gsm_recompute_out.json |
| 34 | 07:01:37 | doc_update | updated STATE.md |
| 35 | 07:01:37 | session_end | E136 completed: R1 recomputation on math_chain_of_thought cell for yi-34b achieved exact AGREE (diff 0.0 against published 0.37478395850488877). 437/4 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-005-e136-point-r1-recomputation-at-a-free-te/events.jsonl
```
