# E215 — Comtrade entrant share by HS code

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## Question

Does exporter concentration (top-5 share) predict entrant fraction across HS codes in international trade, mirroring the federal IT PSC code test (E209) and NIH SBIR test (E208)?

## Design

- **Source**: UN Comtrade public preview API (no key required, answers 200 from this host)
- **Population**: All 6-digit HS codes with ≥10 distinct exporters in 2023 (world imports, partner=World)
- **Current window**: 2023 (single year, calendar)
- **Prior window**: 2018–2022 (five full years)
- **Entrant definition**: A reporter country that appears as an exporter (partner=World, flow=M for imports into reporter, so reporter is importer; wait — need exporters) — **correction**: For exporters, we need flow=X (exports) with reporter=country, partner=0 (World). An entrant is a reporter country that has exports in HS code H in 2023 but had zero exports in H in 2018–2022.
- **Fragmentation metric**: Top-5 exporter share of total export value for that HS code in 2023 (analogous to E209 top-10 vendor share)
- **Entrant fraction**: # entrant exporters / # total exporters in 2023 for that HS code
- **Statistical test**: Spearman ρ(top5_share, entrant_fraction) over HS codes with ≥10 exporters; one-sided permutation test p-value (10,000 permutations, seed 20261021)
- **Kill gate**: G3 FAIL if p ≥ 0.05 or ρ ≤ 0 (negative correlation means fragmented→fewer entrants, opposite of hypothesis)

## Gates (predeclared)

| Gate | Condition | Source |
|------|-----------|--------|
| G0 | API accessible, identity coverage ≥95% (reporter ISO codes) | E209 G0 pattern |
| G1 | ≥20 HS codes with ≥10 exporters each | E209 G1 pattern |
| G2 | Concentration range spans fragmented to concentrated (min top-5 ≤50%, max ≥80%) | E209 G2 pattern |
| G3 | Spearman ρ > 0 with p < 0.05 (fragmented → more entrants) | E209 G3 kill gate |
| G4 | At least one HS code with entrant_fraction ≥ 0.30 | E209 G4 pattern |

## Controls

- **Volume confound**: Log total export value per HS code measured alongside; report ρ(volume, entrant_fraction) and ρ(volume, top5_share)
- **Identity stability**: UN Comtrade uses ISO country codes (stable)
- **Prior window completeness**: Verify all 5 prior years have data for sampled codes

## Resource limits

- Comtrade public preview: no documented rate limit but be respectful
- Target: ~100 HS codes sampled across concentration spectrum
- Timeout: 30s per request, max 3 retries

## Baseline comparison

Strongest existing alternative: E209 (federal IT PSC codes, n=5, ρ=+0.667, p=0.135) and E208 (NIH SBIR categories, n=64, ρ=−0.246, p=0.975). Comtrade provides n≈100–500 HS codes — first adequately powered test of the fragmentation→entry hypothesis.

## What would change a decision

- **G3 PASS**: Fragmentation predicts entry in trade → accessibility pattern has cross-domain validity; build entrant advisor prototype for trade
- **G3 FAIL**: Pattern fails in third domain → accessibility pattern is domain-specific; pivot to fresh observation per D083
- **G0/G1 FAIL**: Instrument or population problem; debug, don't conclude