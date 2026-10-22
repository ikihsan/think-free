<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E217: FDA Drug Recall Patterns — Compounding Pharmacy vs Commercial Manufacturer Risk Profile

## Hypothesis

Compounding pharmacies (firms with "Pharmacy" or "Compounding" in their name) have a higher proportion of Class I (most serious) recalls compared to commercial manufacturers.

## Rationale

This is a fresh observation in a completely new domain axis (FDA drug safety/recalls) per D083. The accessibility pattern (fragmentation → entry) was tested in federal spending (E196-E198), NIH SBIR (E204-E214), and international trade (E215) and falsified. This experiment tests a different pattern in a regulatory safety domain: whether firm type predicts recall severity.

## Population

FDA drug enforcement reports (recalls) from 2018-2024, fetched via openFDA API.

## Classification

- **Compounding pharmacy**: `recalling_firm` contains "Pharmacy", "Compounding", "Apothecary", "Wellness Pharmacy"
- **Commercial manufacturer**: all other firms

## Predeclared Kill Gates

| Gate | Condition | Threshold |
|------|-----------|-----------|
| G1   | Sample size per group | ≥ 50 recalls each |
| G2   | Statistical significance | Fisher's exact p < 0.05 (one-sided: compounding > commercial) |
| G3   | Effect magnitude | Odds ratio > 2.0 |
| G4   | Classification coverage | ≥ 95% of sampled recalls have non-null classification |

## Methodology

1. Fetch recall data from `https://api.fda.gov/drug/enforcement.json` (paginated, max 1000 per page)
2. Filter to recalls with non-null `classification` and `recalling_firm`
3. Classify each firm as compounding pharmacy or commercial manufacturer
4. Compute 2×2 contingency table: (Compounding/Commercial) × (Class I / Not Class I)
5. Apply Fisher's exact test (one-sided)
6. Compute odds ratio with 95% CI
7. Evaluate kill gates

## Expected Outcomes

- **If all gates PASS**: Compounding pharmacies have statistically higher Class I recall rates — a measurable safety signal in a new domain.
- **If G2/G3 FAIL**: No evidence that firm type predicts recall severity in this population.
- **If G1 FAIL**: Insufficient compounding pharmacy recalls in the sample.

## Controls

- Negative control: Random 50/50 split of commercial manufacturers should show no difference (p ≈ 0.5)
- Positive control: Known high-risk firm (King Bio) vs low-risk firm should show difference if sample permits

## Artifacts

- `raw/recalls.jsonl` — raw recall records
- `results.json` — gate evaluations, contingency table, odds ratio, p-value
- `RESULT.md` — final narrative with evidence labels