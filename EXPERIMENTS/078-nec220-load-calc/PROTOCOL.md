# NEC 220 Residential Load Calculation — Experiment 078

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

## Claim

Given a residential electrical equipment schedule including modern loads (EV charger, heat pump, solar PV backfeed, battery storage), an automated NEC Article 220 calculator correctly applies all applicable demand factors and load management provisions to determine the minimum standard service size, while common rule-of-thumb baselines (no demand factors, 200A default, contractor heuristic) oversize the service by ≥1 standard size on ≥30% of test cases.

## Scope

- **Domain**: Residential electrical service sizing per NEC Article 220 (2020/2023 editions)
- **Inputs**: Structured equipment schedule (JSON) with dwelling area, general lighting, small appliance, laundry, fixed appliances, HVAC, EV charger, solar PV, battery storage
- **Output**: Minimum standard service size in amperes (from {100, 125, 150, 200, 225, 300, 400})
- **Oracle**: NEC Article 220 calculation implemented as reference (same algorithm, independently verified)

## Synthetic Fixtures

- **100 test cases** across 10 load profiles (10 cases each):
  1. Standard (lighting, small appliance, laundry, range, dryer, HVAC)
  2. +EV charger (Level 2, 40-80A)
  3. +Solar PV (backfeed 20-100A)
  4. +Heat pump (replacing gas furnace + AC)
  5. +Battery storage (inverter 30-60A)
  6. +EV + Solar
  7. +EV + Heat pump
  8. All-electric (heat pump, electric range, electric dryer, electric water heater)
  9. All-electric + Solar
  10. Large dwelling (>3500 sq ft) with multiple HVAC zones

- **Generation**: `generate_fixtures.py` with fixed seed (42)
- **Parameter ranges**: Dwelling area 1000-5000 sq ft; EV charger 32-80A; Solar 5-20kW; Heat pump 3-5 ton; Storage 5-15kWh
- **Ground truth**: NEC 220 calculation (same algorithm as automated calculator, verified against NEC examples)

## Models Tested

| Model | Description |
|-------|-------------|
| **nec220_auto** | Automated NEC 220 calculator (the candidate mechanism) |
| **nec220_oracle** | Reference NEC 220 implementation (ground truth oracle) |
| **no_demand_factors** | Baseline A: Sum of ALL nameplate ratings with NO demand factors |
| **200a_default** | Baseline B: 200A for all dwellings >1500 sq ft, 150A otherwise |
| **va_div_240** | Baseline C: Total VA / 240V with NO demand factors |
| **contractor_heuristic** | Baseline D: 3VA/sqft + 20A per major appliance circuit |

## Kill Gates (Pre-declared)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** — Automated correctness | `nec220_auto` matches `nec220_oracle` on all test cases | 100% (40/40 test) |
| **G2** — Baseline A oversizing | `no_demand_factors` oversizes by ≥1 standard size | ≥30% of cases |
| **G3** — Baseline B oversizing | `200a_default` oversizes by ≥1 standard size | ≥5% of cases |
| **G4** — Baseline C oversizing | `va_div_240` oversizes by ≥1 standard size | ≥30% of cases |
| **G5** — Baseline D oversizing | `contractor_heuristic` oversizes by ≥1 standard size | ≥40% of cases |
| **G6** — Automated not oversized | `nec220_auto` never oversizes by ≥1 standard size vs oracle | 0% oversizing |
| **G7** — Profile coverage | All profiles have ≥80% cases passing G1 | 100% profiles |

## Negative Controls

- **Random schedule**: Equipment schedule with random loads — automated calculator should produce a valid service size (not crash)
- **Minimal schedule**: Only lighting + small appliance — should produce 100A or 125A
- **Empty modern loads**: Profile 1 with all modern loads set to 0 — should match standard calculation

## Information-Sufficiency Test (Pre-implementation)

Two equipment schedules with identical nameplate totals but different NEC outcomes:
1. **EV charger with load management (NEC 625.42)** vs **EV charger without** — same nameplate, different demand factor
2. **Solar backfeed ≤20% of busbar** vs **>20%** — same nameplate, different busbar rating requirement (NEC 705.12)

**Resolution**: Calculator must accept `load_management: true/false` for EV and `busbar_rating` for solar as side inputs. Claim narrowed to: "equipment schedule + modern load side inputs → correct service size."

## Resource Limits

- Python 3.8+, stdlib only
- No network access during evaluation
- Runtime < 30 seconds for full evaluation
- Synthetic fixtures generated once, committed to repo

## Reproduction

```bash
cd EXPERIMENTS/078-nec220-load-calc
python3 generate_fixtures.py
python3 nec220_calculator.py
python3 evaluate.py
cat results.json
```