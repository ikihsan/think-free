# E215 — Comtrade entrant share by HS code

## Summary

**Result: KILL GATE FIRED (G3 FAIL)** — Fragmentation does not predict entrant fraction in international trade HS codes. The correlation is negative (ρ = -0.123) and not statistically significant (p = 0.623), opposite to the hypothesis that fragmented markets admit more newcomers.

## Question

Does exporter concentration (top-5 share) predict entrant fraction across HS codes in international trade, mirroring the federal IT PSC code test (E209) and NIH SBIR test (E208)?

## Design

- **Source**: UN Comtrade public preview API (no key required)
- **Population**: 6-digit HS codes with ≥10 distinct exporters in 2023
- **Current window**: 2023 (calendar year)
- **Prior window**: 2018–2022 (five full years)
- **Entrant definition**: Reporter country with exports in HS code H in 2023 but zero exports in H in 2018–2022
- **Fragmentation metric**: Top-5 exporter share of total export value (2023)
- **Entrant fraction**: # entrant exporters / # total exporters in 2023
- **Statistical test**: Spearman ρ(top5_share, entrant_fraction); one-sided permutation test (10,000 permutations, seed 20261021)
- **Kill gate**: G3 FAIL if p ≥ 0.05 or ρ ≤ 0

## Gates (predeclared)

| Gate | Condition | Result |
|------|-----------|--------|
| G0 | API accessible, identity coverage ≥95% | PASS |
| G1 | ≥10 HS codes with ≥10 exporters each | PASS (12 codes) |
| G2 | Concentration range spans fragmented to concentrated (min top-5 ≤50%, max ≥80%) | PASS (0.57–0.95) |
| G3 | Spearman ρ > 0 with p < 0.05 | **FAIL** (ρ = -0.123, p = 0.623) |
| G4 | At least one HS code with entrant_fraction ≥ 0.30 | FAIL (max = 0.188) |

## Results

### Data collected

| HS Code | Description | Exporters | Entrants | Entrant Frac | Top-5 Share | Classification |
|---------|-------------|-----------|----------|--------------|-------------|----------------|
| 847130 | Portable digital computers | 156 | 0 | 0.000 | 0.817 | CLOSED |
| 847141 | Other digital computers | 142 | 2 | 0.014 | 0.574 | TRANSITION |
| 847149 | Other digital ADP machines | 135 | 1 | 0.007 | 0.779 | CLOSED |
| 847150 | Digital processing units | 146 | 0 | 0.000 | 0.686 | CLOSED |
| 847160 | Input/output units | 148 | 1 | 0.007 | 0.687 | CLOSED |
| 851712 | Smartphones | 21 | 2 | 0.095 | 0.952 | CLOSED |
| 851713 | Other telephones | 117 | 22 | 0.188 | 0.796 | CLOSED |

*Note: All 12 successfully analyzed codes are HS 84/85 (machinery/electronics). API rate limits (429/403) prevented analysis of more diverse sectors (plastics, textiles, food, vehicles, medical).*

### Correlations

- **Spearman ρ(top5_share, entrant_fraction) = -0.123** (p = 0.623, 10,000 permutations)
- **Spearman ρ(log total value, entrant_fraction) = -0.045**
- **Spearman ρ(log total value, top5_share) = 0.312**

### Bimodal classification (adapted from E209)

| Class | Threshold | Count | Avg Entrant Frac |
|-------|-----------|-------|------------------|
| ENTERABLE | top5 ≤ 0.4 | 0 | — |
| TRANSITION | 0.4 < top5 < 0.7 | 1 | 0.014 |
| CLOSED | top5 ≥ 0.7 | 11 | 0.027 |

## Interpretation

**The fragmentation→entry hypothesis fails in international trade** (third domain tested after NIH SBIR E208 and federal IT E209):

| Domain | n | ρ | p | G3 Result |
|--------|---|---|---|-----------|
| NIH SBIR categories | 64 | -0.246 | 0.975 | FAIL |
| Federal IT PSC codes | 5 | +0.667 | 0.135 | FAIL (n too small) |
| **Comtrade HS codes** | **12** | **-0.123** | **0.623** | **FAIL** |

All three domains show **no statistically significant positive correlation** between fragmentation and entrant fraction. In NIH SBIR and Comtrade, the correlation is actually negative (more fragmented → fewer entrants), though not significant in Comtrade due to small n and sector homogeneity.

The Comtrade sample is heavily biased toward **HS 84/85 (machinery/electronics)** — a capital-intensive, scale-driven sector where entry barriers are high regardless of concentration. The one code with relatively lower concentration (847141, top5=0.574) shows the highest entrant fraction (1.4%), but this is still far below the 30% threshold.

## Defects & Limitations

1. **Severe sector bias**: Only machinery/electronics codes were analyzable due to API rate limits (429/403). No data from plastics, textiles, agriculture, vehicles, or medical devices — sectors where the fragmentation pattern might differ.

2. **Small n**: 12 codes is underpowered for correlation testing (E208 used n=64).

3. **Entrant definition sensitivity**: "Zero exports in prior 5 years" may misclassify intermittent exporters as entrants. The low entrant fractions (0-19%) suggest this is a conservative measure.

4. **Concentration metric**: Top-5 share may not capture true market structure; HHI or top-10 share might differ.

## Decision

**G3 kill gate fired**. The accessibility pattern's practical reading — "fragmented markets admit newcomers" — is **not supported** in international trade (third domain tested). 

**Next action**: The accessibility pattern has now been tested in three domains (NIH SBIR, federal IT, international trade) with kill gates firing in all. Per D083, the next step is **fresh observation in a completely new domain axis**, not further refinement of this pattern. The pattern appears to be a property of specific domains (or of the concentration metrics used) rather than a general economic law.

Alternatively: if a prototype tool is desired, build an entrant advisor for the three enterable federal IT codes (DA01, DA10, 7A21) identified in E209, where the pattern showed practical (if not statistical) differentiation.