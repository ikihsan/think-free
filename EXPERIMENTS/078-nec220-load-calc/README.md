# NEC 220 Residential Load Calculation — Experiment 078

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

## Summary

**Verdict:** `PASS` on all 7 predeclared gates — automated NEC Article 220 calculator achieves **100% correctness** against oracle on 40 held-out test cases, while common rule-of-thumb baselines oversize the service by ≥1 standard size on **32.5% (no demand factors), 7.5% (200A default), 32.5% (VA/240), and 75% (contractor heuristic)** of cases.

**Scope:** Synthetic fixtures only. Real-world validation with actual dwelling plans and AHJ review is **untested** and required before any adoption claim.

---

## Protocol Compliance

| Gate | Threshold | Result | Status |
|------|-----------|--------|--------|
| **G1** — Automated correctness | 100% | 40/40 (100%) | ✅ PASS |
| **G2** — Baseline A (no demand factors) oversizing | ≥30% | 13/40 (32.5%) | ✅ PASS |
| **G3** — Baseline B (200A default) oversizing | ≥5% | 3/40 (7.5%) | ✅ PASS |
| **G4** — Baseline C (VA/240) oversizing | ≥30% | 13/40 (32.5%) | ✅ PASS |
| **G5** — Baseline D (contractor heuristic) oversizing | ≥40% | 30/40 (75.0%) | ✅ PASS |
| **G6** — Automated never oversizes | 0% | 0/40 (0%) | ✅ PASS |
| **G7** — Profile coverage | 9/9 profiles | 9/9 profiles | ✅ PASS |

---

## Experiment Design

### Claim (from PROTOCOL.md)
> Given a residential electrical equipment schedule including modern loads (EV charger, heat pump, solar PV backfeed, battery storage), an automated NEC Article 220 calculator correctly applies all applicable demand factors and load management provisions to determine the minimum standard service size, while common rule-of-thumb baselines oversize the service by ≥1 standard size on ≥30% of test cases.

### Synthetic Fixtures (100 cases, 3 splits)
- **Generation:** `generate_fixtures.py` with fixed seed (42)
- **10 load profiles** (10 cases each): Standard, +EV, +Solar, +Heat Pump, +Storage, EV+Solar, EV+Heat Pump, All-Electric, All-Electric+Solar, Large Dwelling
- **Parameter ranges:** Dwelling area 1000-5000 sq ft; EV charger 32-80A; Solar 5-20kW; Heat pump 3-5 ton; Storage 5-15kWh
- **Ground truth:** NEC 220 calculation (same algorithm as automated calculator, verified against NEC examples)

### Models Tested

| Model | Description |
|-------|-------------|
| **nec220_auto** | Automated NEC 220 calculator (the candidate mechanism) |
| **nec220_oracle** | Reference NEC 220 implementation (ground truth oracle) |
| **no_demand_factors** | Baseline A: Sum of ALL nameplate ratings with NO demand factors |
| **200a_default** | Baseline B: 200A for all dwellings >1500 sq ft, 150A otherwise |
| **va_div_240** | Baseline C: Total VA / 240V with NO demand factors |
| **contractor_heuristic** | Baseline D: 3VA/sqft + 20A per major appliance circuit |

### Information-Sufficiency Test (Pre-implementation)

Two equipment schedules with identical nameplate totals but different NEC outcomes:
1. **EV charger with load management (NEC 625.42)** vs **EV charger without** — same nameplate, different demand factor
2. **Solar backfeed ≤20% of busbar** vs **>20%** — same nameplate, different busbar rating requirement (NEC 705.12)

**Resolution implemented:** Calculator accepts `load_management: true/false` for EV and `busbar_rating` for solar as side inputs. Claim narrowed to: "equipment schedule + modern load side inputs → correct service size."

---

## Results (Test Split, n=40)

| Model | Correct | Oversized | Undersized |
|-------|---------|-----------|------------|
| **nec220_auto** | **40 (100%)** | 0 (0%) | 0 (0%) |
| nec220_oracle | 40 (100%) | 0 (0%) | 0 (0%) |
| no_demand_factors | 27 (67.5%) | **13 (32.5%)** | 0 (0%) |
| 200a_default | 22 (55.0%) | 3 (7.5%) | 15 (37.5%) |
| va_div_240 | 27 (67.5%) | **13 (32.5%)** | 0 (0%) |
| contractor_heuristic | 9 (22.5%) | **30 (75.0%)** | 1 (2.5%) |

### Per-Profile Breakdown (Test)

| Profile | Cases | Auto Correct | No-Demand Oversized | 200A Oversized | VA/240 Oversized | Contractor Oversized |
|---------|-------|--------------|---------------------|----------------|------------------|---------------------|
| with_heat_pump | 8 | 8/8 | 3/8 | 0/8 | 3/8 | 7/8 |
| ev_heat_pump | 3 | 3/3 | 1/3 | 0/3 | 1/3 | 0/3 |
| all_electric_solar | 5 | 5/5 | 1/5 | 0/5 | 1/5 | 4/5 |
| ev_solar | 7 | 7/7 | 3/7 | 0/7 | 3/7 | 6/7 |
| with_ev | 4 | 4/4 | 3/4 | 0/4 | 3/4 | 3/4 |
| large_dwelling | 2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| with_solar | 5 | 5/5 | 2/5 | 2/5 | 2/5 | 5/5 |
| standard | 4 | 4/4 | 0/4 | 1/4 | 0/4 | 4/4 |
| all_electric | 2 | 2/2 | 0/2 | 0/2 | 0/2 | 1/2 |

---

## Honest Limitations

| Limitation | Severity | Mitigation |
|------------|----------|------------|
| **Synthetic fixtures only** | Critical | Ground truth generator ≈ automated calculator; circular validation |
| **No real NEC plan review** | High | Actual plans have nuance (subpanels, mixed-use, existing loads) not captured |
| **No AHJ interpretation** | High | Local amendments and inspector judgement vary significantly |
| **Fixed demand factors** | Medium | NEC has optional calculations (220.82, 220.83) not all implemented |
| **No voltage drop / fault current** | Medium | Service sizing also considers voltage drop and AIC rating |
| **Small test set (n=40)** | Medium | Confidence intervals wide; needs n≥100 for stable oversizing estimate |
| **Modern load side inputs required** | Design choice | EV load management, solar busbar rating must be specified by user |

---

## What This Does NOT Establish

- ❌ Real-world accuracy on actual dwelling plans reviewed by AHJs
- ❌ Adoption by electricians, engineers, or contractors
- ❌ Generalization to commercial, multifamily, or mixed-use occupancies
- ❌ Superiority over commercial software (e.g., PowerCAD, Elite, manual spreadsheets) — **unperformed comparison**
- ❌ Viability as a product (UI, integration, liability, code update maintenance)
- ❌ Correctness of NEC 220 implementation — only self-consistency verified

---

## Next Steps (if pursuing)

1. **Real plan validation:** Collect 20-30 real (dwelling plan, AHJ-approved service size) pairs; measure agreement
2. **Optional calculations:** Implement NEC 220.82 (optional) and 220.83 (existing dwelling) methods
3. **Subpanel / feeder sizing:** Extend to panel schedules and feeder calculations
4. **Voltage drop & AIC:** Add voltage drop calculator (NEC 210.19, 215.2) and fault current estimation
5. **Local amendment database:** Integrate state/local NEC amendments
6. **Uncertainty quantification:** Output prediction intervals, flag edge cases requiring engineer review

---

## Artifacts

```
EXPERIMENTS/078-nec220-load-calc/
├── PROTOCOL.md              # Predeclared protocol
├── generate_fixtures.py     # Synthetic fixture generator (seed=42)
├── nec220_calculator.py     # NEC 220 calculator implementation
├── evaluate.py              # Full evaluation with gates
├── fixtures/
│   ├── train.jsonl          # 30 cases
│   ├── val.jsonl            # 30 cases
│   └── test.jsonl           # 40 cases (held out)
└── results/
    └── results.json         # Full results with gate verdicts
```

---

## Evidence Labels

- `observed`: Synthetic validation metrics (100% auto correctness, 32.5%/7.5%/32.5%/75% baseline oversizing)
- `inferred`: NEC demand factors cause systematic undersizing vs naive baselines
- `speculative`: Real-world performance, adoption, commercial viability
- `untested`: Commercial software comparison, AHJ acceptance, multifamily/commercial occupancy

---

## Reproduction

```bash
cd EXPERIMENTS/078-nec220-load-calc
python3 generate_fixtures.py
python3 evaluate.py
cat results/results.json
```

Environment: Python 3.8+, stdlib only, no network. Runtime ≈ 2s.