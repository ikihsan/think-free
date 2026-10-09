# Manufacturing Cost Estimation from STEP Files — Experiment 074

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

## Summary

**Verdict:** `PASS` on synthetic validation — parametric feature-based cost model achieves **3.6% MAPE** and **r=0.982** on held-out test parts, significantly outperforming volume heuristic (252% MAPE) and all negative controls.

**Scope:** Synthetic fixtures only. Real-world validation with actual manufacturer quotes is **untested** and required before any adoption claim.

---

## Protocol Compliance

| Gate | Threshold | Result | Status |
|------|-----------|--------|--------|
| MAPE ≤ 20% | 20% | 3.6% | ✅ PASS |
| Pearson r ≥ 0.70 | 0.70 | 0.982 | ✅ PASS |
| Beats volume baseline by ≥5pp | 5pp | 248pp | ✅ PASS |
| Coverage ≥ 90% | 90% | 100% | ✅ PASS |
| Random weights control fails | MAPE > 50% | 3,533,802% | ✅ PASS |
| Shuffled labels control not significant | p > 0.05 | t=0.97, p>0.05 | ✅ PASS* |
| Ablation (no features) worse | MAPE increase | 252% vs 3.6% | ✅ PASS |
| Ablation (no material) worse | MAPE increase | 9.4% vs 3.6% | ✅ PASS |

*Shuffled control correlation (r=0.324) is **not statistically significant** (t=0.97, df=8, p>0.05), while parametric model correlation (r=0.982) is highly significant (t=14.7, p<0.001). Fisher z-test for difference: z=3.77, p<0.001.

---

## Experiment Design

### Claim (from PROTOCOL.md)
> Given a STEP file of a small metal part (≤ 300 mm envelope), a feature-based cost estimation pipeline can predict total prototype-run cost within ±20% MAPE with correlation ≥ 0.7.

### Synthetic Fixtures (30 parts, 3 splits)
- **Generation:** `generate_fixtures.py` with fixed seed (42)
- **Complexities:** simple (2-5 features), medium (5-12), complex (10-20)
- **Materials:** 6061 Al, 304 SS, mild steel, ABS plastic
- **Ground truth:** Parametric cost model with published rate cards ($75-150/hr machine, $50-100 setup)

### Models Tested
| Model | Description |
|-------|-------------|
| **parametric** | White-box: extracts features (pockets, holes, bends, threads) → applies parametric cost formulas |
| **volume_heuristic** | Baseline A: material cost + $50 setup + $0.50/cm³ machining |
| **random_weights** | Negative control: random feature weights |
| **shuffled_labels** | Negative control: permuted ground truth labels |
| **ablation_no_features** | Ablation: volume heuristic (feature extraction disabled) |
| **ablation_no_material** | Ablation: assumes aluminum for all parts |

### Information-Sufficiency Test (pre-implementation)
Two geometries with identical STEP boundary representation but different costs:
1. **Solid block vs. deep pockets** — same envelope, different machining time
2. **Same geometry, different material** — STEP may not encode material
3. **Same features, different tolerances** — STEP PMI may be absent

**Resolution implemented:** Pipeline requires `material` as side input (not in STEP). Tolerance class fixed to standard prototype (±0.1mm). Claim narrowed to: "geometry + material side input → cost estimate."

---

## Results (Test Split, n=10)

| Model | MAPE | Pearson r | RMSE | vs Parametric |
|-------|------|-----------|------|---------------|
| **parametric** | **3.6%** | **0.982** | $15.21 | — |
| volume_heuristic | 251.8% | 0.906 | $818.11 | +248pp |
| random_weights | 3,533,802% | 0.569 | $11.2M | — |
| shuffled_labels | 39.2% | 0.324† | $86.25 | — |
| ablation_no_features | 251.8% | 0.906 | $818.11 | +248pp |
| ablation_no_material | 9.4% | 0.921 | $30.91 | +5.8pp |

† Not statistically significant (t=0.97, df=8, p>0.05)

### Per-Part Test Predictions (Parametric)

| Part ID | Predicted | Actual | Error |
|---------|-----------|--------|-------|
| part_020 | $117.82 | $108.10 | +9.0% |
| part_021 | $127.53 | $127.86 | +0.3% |
| part_022 | $105.97 | $106.32 | +0.3% |
| part_023 | $280.00 | $283.86 | -1.4% |
| part_024 | $317.74 | $323.27 | -1.7% |
| part_025 | $150.12 | $151.58 | -1.0% |
| part_026 | $121.45 | $121.47 | +0.0% |
| part_027 | $235.99 | $234.88 | +0.5% |
| part_028 | $282.08 | $235.69 | **+19.7%** |
| part_029 | $157.38 | $161.43 | -2.5% |

**Largest error:** part_028 (complex stainless part with multiple bends) — bending cost model underestimates.

---

## Honest Limitations

| Limitation | Severity | Mitigation |
|------------|----------|------------|
| **Synthetic fixtures only** | Critical | Ground truth generator ≈ parametric model; circular validation |
| **No real STEP parsing** | High | Used simplified JSON fixtures; real STEP AP203/214 parsing needs CAD kernel |
| **No real manufacturer quotes** | Critical | Actual quotes include supplier-specific factors, capacity, urgency |
| **Fixed tolerance class** | Medium | Real parts have varying tolerance specs affecting cost 2-5× |
| **No assembly/fixture costs** | Medium | Real quotes include workholding, inspection, packaging |
| **Small test set (n=10)** | Medium | Confidence intervals wide; needs n≥30 for stable MAPE estimate |
| **Material side input required** | Design choice | STEP rarely encodes material; user must specify |

---

## What This Does NOT Establish

- ❌ Real-world accuracy on manufacturer quotes
- ❌ Adoption by design engineers or job shops
- ❌ Generalization to parts >300mm, welded assemblies, castings
- ❌ Superiority over commercial tools (aPriori, Costimator, Paperless Parts) — **unperformed comparison**
- ❌ Viability as a product (setup burden, UI, integration)

---

## Next Steps (if pursuing)

1. **Real STEP parsing:** Integrate `pythonocc` or `cadquery` for actual STEP AP203/214 feature recognition
2. **Pilot with 1-2 job shops:** Collect 20-30 real (STEP file, quote) pairs; measure MAPE
3. **Tolerance/PMI extraction:** Parse STEP PMI for tolerance-driven cost multipliers
4. **Supplier database:** Integrate material stock availability, machine capabilities, lead times
5. **Uncertainty quantification:** Output prediction intervals, not point estimates

---

## Artifacts

```
EXPERIMENTS/074-mfg-cost-estimation/
├── PROTOCOL.md              # Predeclared protocol (this file's source)
├── generate_fixtures.py     # Synthetic fixture generator (seed=42)
├── extract_features.py      # Feature extraction from JSON fixtures
├── cost_model.py            # Parametric + baseline cost models
├── evaluate.py              # Full evaluation with gates
├── fixtures/
│   ├── train.jsonl          # 10 parts with ground truth
│   ├── val.jsonl            # 10 parts
│   ├── test.jsonl           # 10 parts (held out)
│   ├── train_features.jsonl
│   ├── val_features.jsonl
│   └── test_features.jsonl
└── results.json             # Full results with gate verdicts
```

---

## Evidence Labels

- `observed`: Synthetic validation metrics (3.6% MAPE, 0.982 r)
- `inferred`: Feature-based approach adds value over volume heuristic
- `speculative`: Real-world performance, adoption, commercial viability
- `untested`: Commercial tool comparison, STEP parsing robustness, multi-shop pilot