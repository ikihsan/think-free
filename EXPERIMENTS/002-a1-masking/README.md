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

## Sensitivity sweep (`sensitivity.json`, T-0006)

Grid over K∈{10,20,40}, budget∈{75,150,300}, masking∈{random,block},
10 seeds, 5 policies. Decision-directed passes the ≥25%-regret-reduction
gate in 14 of 18 configurations. All four failures are the same corner:
**K=40 with budget ≤150** — when the repair set is nearly as large as the
observation budget, DD and the baselines converge (equal-information
regime). Under generous budgets (300) DD's advantage reappears.
Conclusion: the A1 mechanism helps in the realistic regime (budget-limited,
moderate K) and disappears in the degenerate corner; this is a boundary
result, not a contradiction.

## Distance-budget variant (`distance.json`, T-0007)

Same substrate and masking, but the budget is *walking distance* D from the
southwest corner (nearest-neighbour full tour ≈ 190 km). A policy's
observations are whatever it reaches within D metres along the walk it
proposes. 30 seeds × 2 masks × D ∈ {40, 80, 160} km, K=20.

| D | strongest baseline | decision-directed | dd-walk |
|---|---|---|---|
| 40 km | centrality, 16.3 | 85.2 | 134.6 |
| 80 km | centrality, 0 | 85.2 | 85.2 |
| 160 km | centrality, 0 | 85.2 | 85.2 |

Gate (DD within 25% of strongest baseline in every config): **fails in 6 of
6**. Under the realistic cost metric the A1 decision-directed advantage does
not transfer — its scattered marginal-value picks exhaust the walk after
~17–60 hops, while space-filling baselines cover the neighbourhood. See
F006. Reproduce: `python3 EXPERIMENTS/002-a1-masking/distance.py`.

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
