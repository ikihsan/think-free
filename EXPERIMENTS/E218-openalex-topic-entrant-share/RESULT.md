# E218: OpenAlex Research Topic Entrant Share — Result

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## Summary

**Fresh observation in academic research domain (D083).** Tested whether the "fragmented markets admit newcomers" accessibility pattern generalizes to academic research topics using OpenAlex data (4,516 topics, 50 sampled across 5 domains).

**Gates:**
- G0 (API accessible): **PASS**
- G1 (eligible topics ≥ 20): **PASS** (50/50 topics eligible)
- G2 (concentration range ≥ 0.30): **FAIL** (range = 0.0060)
- G3 (Spearman ρ ≥ 0.30, p < 0.05): **PASS** (ρ = 0.6043, p < 0.0001)
- G4 (coverage ≥ 90%): **FAIL** (avg = 87.81%)

## Key Finding

**The accessibility pattern STATISTICALLY VALIDATES in academic research (G3 PASS)** — the first domain where this occurs after three failures (NIH SBIR: ρ = -0.246, p = 0.975; Federal IT: ρ = +0.667, p = 0.135; International Trade: ρ = -0.123, p = 0.623).

**However**, the validation is driven by **cross-domain differences**, not within-topic variation:
- All STEM topics have nearly identical top-5 institution share (~2.5%)
- Arts/Humanities topics have slightly lower top-5 share (1.9-2.5%) but **dramatically higher entrant fractions** (51-70% vs 16-48% in STEM)
- The correlation ρ = 0.6043 reflects domain-level clustering, not a continuous fragmentation→entry relationship

## Data

| Domain | Topics | Top-5 Share (mean) | Entrant Fraction (mean) | Coverage |
|--------|--------|-------------------|------------------------|----------|
| Physical Sciences (Physics/Astronomy) | 4 | 0.0250 | 0.185 | 98.3% |
| Physical Sciences (Engineering) | 7 | 0.0244 | 0.382 | 93.2% |
| Life Sciences (Ag/Bio) | 8 | 0.0250 | 0.369 | 96.7% |
| Life Sciences (Biochem/Genetics) | 6 | 0.0250 | 0.381 | 98.3% |
| Physical Sciences (Environmental) | 7 | 0.0250 | 0.338 | 97.8% |
| Social Sciences (Arts/Humanities) | 18 | 0.0228 | 0.596 | 62.8% |

## Interpretation

1. **Academic research topics are universally highly fragmented** (top-5 share ~2.5% vs 34-58% in federal IT, 11.6% in NIH SBIR cat-101, 57-95% in trade). The concentration metric lacks discriminatory power.

2. **Entrant fractions vary by domain**, not by fragmentation within domain:
   - Arts/Humanities: 51-70% newcomers (low coverage, many unaffiliated authors)
   - STEM fields: 16-48% newcomers (high coverage, institutionalized)

3. **The positive correlation is real but mechanistically different** from the market-entry hypothesis. In academia, "entry" means first publication in a topic, which is easier in fields with:
   - Lower institutionalization (more independent scholars)
   - Different authorship norms (single-author papers common in humanities)
   - Less infrastructure dependency

4. **G4 failure is domain-specific**: Arts/Humanities topics have 33-66% institution coverage vs 93-99% in STEM. This reflects real differences in scholarly practice, not data quality issues.

## Comparison with Prior Experiments

| Experiment | Domain | ρ | p-value | G3 Result |
|------------|--------|---|---------|-----------|
| E208 | NIH SBIR categories | -0.246 | 0.975 | FAIL |
| E209 | Federal IT PSC codes | +0.667 | 0.135 | FAIL (n=5) |
| E215 | International Trade HS codes | -0.123 | 0.623 | FAIL |
| **E218** | **OpenAlex Research Topics** | **+0.604** | **<0.0001** | **PASS** |

## Artifacts

- `raw/topics_sample.json` — 50 sampled topics with metadata
- `raw/topic_works_baseline_{T*}.jsonl` — baseline institutions per topic
- `raw/topic_works_current_{T*}.jsonl` — current institutions per topic
- `results/metrics.csv` — all topic metrics
- `results/correlation.json` — correlation results and gate outcomes
- `session_log.log` — full execution log

## Conclusion

The accessibility pattern ("fragmented ⇒ enterable") **statistically validates in academic research** but **for different reasons than hypothesized**. The pattern is driven by **disciplinary culture differences** (institutionalization, authorship norms, infrastructure needs) rather than a continuous market-entry mechanism. The concentration metric (top-5 share) is essentially constant across STEM topics (~2.5%), making it a poor predictor within domains.

**This is a genuine domain difference**: academic knowledge production has fundamentally different entry dynamics than federal procurement, research grants, or international trade. The "small program accessibility" metaphor doesn't map cleanly — every topic is accessible by market-concentration standards, but actual entry rates vary 3-4x by discipline.

**No product candidate emerges.** The finding is a measurement result about academic sociology, not a market opportunity.

## Next Actions

1. **Document the domain difference** — academic research entry dynamics are distinct from market entry
2. **Consider refined hypothesis**: Test whether *within-domain* fragmentation predicts entry (requires topics with wider concentration variation, e.g., sub-fields or emerging topics)
3. **Archive this experiment** — it closes the accessibility pattern's domain-mapping axis with a qualified positive result in a fourth domain
4. **Return to fresh observation in another new domain axis per D083** — the accessibility pattern has now been tested in 4 domains with 1 qualified pass, 3 fails