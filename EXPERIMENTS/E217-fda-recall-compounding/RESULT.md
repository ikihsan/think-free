<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E217 Result: FDA Drug Recall Patterns — Compounding Pharmacy vs Commercial Manufacturer Risk Profile

## Summary

**VERDICT: KILL GATE FIRED** — The hypothesis that compounding pharmacies have higher Class I recall proportions than commercial manufacturers is **not supported**. The data shows the opposite: compounding pharmacies have substantially **lower** Class I recall rates (odds ratio = 0.14, 95% CI [0.11, 0.17], one-sided Fisher's exact p = 1.000).

## Data

- **Population**: 18,043 FDA drug enforcement reports (complete census from openFDA API, 2016-2024)
- **Classification**: 100% coverage (all records had non-null `classification` and `recalling_firm`)
- **Compounding pharmacies**: 4,260 recalls (23.6%), identified by firm name keywords ("pharmacy", "compounding", "apothecary", "wellness pharmacy")
- **Commercial manufacturers**: 13,783 recalls (76.4%)

## Contingency Table

| | Class I | Not Class I | Total |
|---|---|---|---|
| Compounding | 80 (1.88%) | 4,180 (98.12%) | 4,260 |
| Commercial | 1,670 (12.12%) | 12,113 (87.88%) | 13,783 |
| **Total** | 1,750 (9.70%) | 16,293 (90.30%) | 18,043 |

## Gate Evaluation

| Gate | Condition | Result |
|------|-----------|--------|
| G1 | Sample size ≥ 50 per group | **PASS** (4,260 / 13,783) |
| G2 | Fisher's exact p < 0.05 (one-sided) | **FAIL** (p = 1.000) |
| G3 | Odds ratio > 2.0 | **FAIL** (OR = 0.14) |
| G4 | Classification coverage ≥ 95% | **PASS** (100%) |

**Overall: KILL GATE FIRED** (G2 and G3 failed)

## Interpretation

The hypothesis was **directionally wrong**. Commercial manufacturers have a **6.4× higher** Class I recall rate (12.1% vs 1.9%) than compounding pharmacies in this population.

Possible explanations (speculative, not tested):
1. **Reporting bias**: Compounding pharmacies may under-report Class I events, or their recalls are classified differently.
2. **Product mix**: Compounding pharmacies produce sterile injectables (high risk) but in small batches; a single contamination affects few units, possibly leading to Class II classification.
3. **Regulatory scrutiny**: Commercial manufacturers' products are distributed nationally; defects trigger broader Class I recalls.
4. **Firm classification noise**: Some "pharmacy" firms may be retail pharmacies repackaging, not true compounding operations.

## Evidence Labels

- Contingency table counts: `observed` (computed from fetched data)
- Odds ratio / p-value: `observed` (computed from counts)
- Directional interpretation: `observed` (data contradicts hypothesis)
- Explanatory hypotheses: `speculative` (not tested)

## Artifacts

- `raw/recalls.jsonl` — 18,043 raw recall records (sha256 per line in meta)
- `raw/results.json` — gate evaluations, contingency table, statistics
- `PROTOCOL.md` — predeclared protocol (committed before fetch)

## Conclusion

This fresh observation in the FDA drug recall domain (a completely new domain axis per D083) **does not support** the tested hypothesis. The negative result is clear and statistically decisive. No candidate emerges from this experiment.

**Next action**: Per D083, continue fresh observation in another new domain axis, or refine hypothesis within FDA domain (e.g., test whether Class I recalls predict product discontinuation via NDC linkage).