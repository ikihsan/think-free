# E218: OpenAlex Research Topic Entrant Share — Fresh Observation in Academic Research Domain

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## Objective

Test whether the "fragmented markets admit newcomers" accessibility pattern generalizes to academic research topics. This is a fresh observation in a completely new domain axis (academic knowledge production) per D083, distinct from federal spending (E208-E209), international trade (E215), NIH grants (E204-E214), FDA recalls (E217), Q&A platforms, package registries, and fault-code domains.

## Hypothesis

**H0 (null)**: Institutional concentration in a research topic (baseline period) does not predict the segment-newcomer fraction (current period).  
**H1 (alternative)**: Lower institutional concentration (higher fragmentation) predicts higher segment-newcomer fractions — i.e., fragmented topics are more enterable.

## Domain and Population

- **Domain**: Academic research topics from OpenAlex (4,516 topics across all fields)
- **Unit of analysis**: OpenAlex topic (e.g., "Musicology and Musical Analysis", "Particle accelerators and beam dynamics")
- **Baseline period**: 2018–2022 (5 years)
- **Current period**: 2023–2024 (2 years)
- **Identity**: Institution (OpenAlex institution ID, e.g., `https://openalex.org/I121847817`)
- **Eligibility**: Topics with ≥ 100 works in baseline period AND ≥ 10 distinct institutions in baseline period

## Metrics

### Concentration (baseline period)
- **Top-5 institution share**: Fraction of baseline-period works authored by the top 5 institutions by work count
- **HHI**: Herfindahl-Hirschman Index of institution work shares in baseline period
- **Fragmentation proxy**: `1 - top5_share` (higher = more fragmented)

### Entry (current period)
- **Segment newcomer**: Institution with ≥ 1 work in current period AND 0 works in baseline period
- **Segment newcomer fraction**: `segment_newcomers / current_period_institutions`

## Gates (predeclared)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| G0 | API accessible; topics and works fetchable | PASS/FAIL |
| G1 | Eligible topics (baseline works ≥ 100, baseline institutions ≥ 10) | n ≥ 20 topics |
| G2 | Concentration range sufficient for correlation test | top-5 share range ≥ 0.30 (max - min) |
| G3 | **Kill gate**: Spearman ρ(fragmentation, entrant_fraction) | ρ ≥ 0.30, one-sided p < 0.05 |
| G4 | Coverage: institution identity coverage in both periods | ≥ 90% of works have ≥ 1 institution |

## Analysis Plan

1. Fetch all topics (4,516) → filter to those with works_count ≥ 500 (to ensure baseline eligibility)
2. Sample up to 50 topics stratified by field/domain to ensure diversity
3. For each sampled topic:
   - Fetch works in baseline period (2018-2022), max 200 per year → extract institutions
   - Fetch works in current period (2023-2024), max 200 per year → extract institutions
   - Compute top-5 share (baseline), entrant fraction (current)
4. Run Spearman correlation between fragmentation (1 - top5_share) and entrant_fraction
5. Report all gates, correlation, p-value, and scatter plot data

## Falsification Criteria

The accessibility pattern claim ("fragmented ⇒ enterable") is **falsified** if:
- G3 kills (ρ < 0.30 or p ≥ 0.05), OR
- G1 fails (insufficient eligible topics), OR
- G2 fails (insufficient concentration variation)

A PASS on G3 with ρ ≥ 0.30 and p < 0.05 would be the first domain where the pattern survives statistical validation (E208: ρ = -0.246, p = 0.975; E209: ρ = +0.667, p = 0.135; E215: ρ = -0.123, p = 0.623).

## Sampling Strategy

- Use `topics?filter=works_count:>500&per-page=200` to get candidate topics
- Stratify by `domain` (Physical Sciences, Life Sciences, Social Sciences, Health Sciences) and `field`
- Target 10-15 topics per domain, up to 50 total
- This ensures field diversity and sufficient n for correlation

## Rate Limit Management

- OpenAlex free tier: ~1000 requests/day per IP ($0.10/day budget)
- Each topic requires ~8 requests (4 baseline years × 200/page, 2 current years × 200/page, but using cursor pagination)
- With 50 topics × ~8 requests = 400 requests, well within daily budget
- Use `select=id,authorships.institutions.id,publication_year` to minimize payload

## Output

- `raw/topics_sample.json` — sampled topics with metadata
- `raw/topic_works_baseline_{topic_id}.jsonl` — baseline period works (institution IDs only)
- `raw/topic_works_current_{topic_id}.jsonl` — current period works (institution IDs only)
- `results/metrics.csv` — topic_id, display_name, domain, field, baseline_works, baseline_institutions, top5_share, hhi, current_works, current_institutions, segment_newcomers, entrant_fraction
- `results/correlation.json` — Spearman ρ, p-value, n, gate results
- `RESULT.md` — full experiment write-up

## Pre-registration

This protocol is written BEFORE any data fetch for this experiment. Gates G0-G4 are declared above. The kill gate G3 uses one-sided Spearman test (alternative: greater) with α = 0.05.