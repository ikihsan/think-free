<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-03
-->

# 002-a1-masking

Bounded A1 masking experiment over the PPNA Seattle crossings extract.

- Substrate: `OpenSidewalks/PLoS-cities-complex-systems` @
  `4f65e22b19576375b2b031b035631a20806da48e`, `data/seattle.geojson`
  (103,451 crossings; properties `curbramps`, `crossing`, `subclass`,
  `length`).
- Neighbourhood: densest ~955-crossing cluster of ~400 m grid cells.
- Ground truth decision: rank crossings by length of *unsafe-fixable*
  crossings (marked, no curb ramps); regret = full-information top-20 score
  minus chosen-set score at equal budget (150 observations).
- Masking: 50% of facts hidden, random and block-contiguous, 30 seeds each.

## Result (raw, `results.json`)

| policy | median regret, random mask | median regret, block mask |
|---|---|---|
| decision-directed | 64.1 | 64.1 |
| centrality | 109.9 | 109.9 |
| random | 118.2 | 113.5 |
| missingness | 134.6 | 113.5 |
| shortest-tour | 134.6 | 134.6 |

Provisional A1 step-5 gate (≥25% lower median regret than strongest
baseline in every masking mode): **met** (64.1 vs 109.9 ≈ 42% lower).

## Honest caveats

- Per-seed regrets are nearly constant; the design is close to
  deterministic and budget is one value (150 of 955). Sensitivity to
  budget, K, and block size is untested.
- Costs are synthetic; no field-time or planner-relevance validation.
- One neighbourhood, one city, one substrate. This is computational
  potential, not validation of A1 as a product hypothesis.

## Reproduce

```bash
python3 EXPERIMENTS/002-a1-masking/masking.py
```

Expected: `results.json` rewritten; the printed `gate_pass` is `true`.
