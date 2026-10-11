<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E095: crates.io view-count principle test

## Objective
Test whether the view-count principle generalizes to crates.io (Rust package registry):
- Need-related crates (those with keywords indicating debugging, error handling, profiling, logging, monitoring, tracing, diagnostics, observability) have systematically higher download activity than random crates.

## Hypothesis
**H1**: Need-related crates on crates.io have significantly higher download activity (both total downloads and recent downloads) than random crates.

**H0**: No significant difference in download activity between need-related and random crates.

## Background
The view-count principle has been tested on:
- PyPI (E071): **SUPPORTED** — need-related 82.93% active vs random 57.50%, all gates met
- NPM (E072): **SUPPORTED** — 100% need-related active vs 0% random
- Maven Central (E090): **NOT SUPPORTED** — need-related 60% vs random 52.2%, difference 7.8 pp (CI95 LB −0.41 < 10 pp)
- Hugging Face Hub (E101): **NOT SUPPORTED** — need-related 12.4% vs random 8.6%, p=0.089

crates.io is a major package registry with download count metadata (total downloads and recent downloads), making it a suitable platform for testing the principle.

## Method

### Population Definition
- **Need-related crates**: Crates tagged with at least one of the following keywords:
  - `debugging` (324 crates)
  - `error-handling` (270 crates)
  - `profiling` (326 crates)
  - `logging` (1207 crates)
  - `monitoring` (601 crates)
  - `tracing` (936 crates)
  - `diagnostics` (386 crates)
  - `observability` (653 crates)
  - `benchmarking` (76 crates)
  - `error` (637 crates)
  - `panic` (122 crates)
  - `backtrace` (57 crates)

  Total unique need-related crates (union): ~estimated 3,000-5,000 (some overlap)

- **Random crates**: Random sample of crates from the general population (349,473 total) that do NOT have any of the above keywords.

### Sampling Strategy
1. Fetch all crates for each need-related keyword via the crates.io API (`/api/v1/keywords/{keyword}/crates`)
2. Deduplicate to get unique need-related crates
3. Sample N need-related crates (target N ≥ 100 for statistical power)
4. Sample N random crates from the general population (using `/api/v1/crates?page=X&per_page=Y` with random page offsets)
5. Filter random crates to exclude any with need-related keywords

### Activity Metrics
crates.io provides two download metrics:
- `downloads`: Total downloads since publication
- `recent_downloads`: Downloads in the last 90 days (per crates.io documentation)

We define "active" as having `recent_downloads > 0` (at least one download in the last 90 days), following the E071/E072 precedent where "active" meant having meaningful activity metadata.

### Gates (following E071/E072/E090 precedent)

**G1 (Retrieval)**: Need-related sample size ≥ 100 AND random sample size ≥ 100
- Rationale: Minimum sample for statistical comparison

**G2 (Significance)**: Two-sample proportion test (or t-test on log downloads) shows p < 0.05
- Rationale: Standard significance threshold

**G3 (Effect Size)**: Wilson CI95 lower bound for need-related active rate > 0.60 (or Cohen's d > 0.5 for continuous downloads)
- Rationale: Meaningful practical difference; E071 used Wilson CI95 LB > 0.60

**G4 (Arrival Field Rate)**: ≥ 95% of sampled crates have download metadata available
- Rationale: Data completeness; E090 required ≥ 95%

### Statistical Tests
1. **Proportion test**: Compare proportion of "active" crates (recent_downloads > 0) between need-related and random groups
2. **Continuous test**: Compare log(total downloads) and log(recent downloads) using Mann-Whitney U test (non-parametric, downloads are highly skewed)
3. **Effect size**: Cohen's d for log downloads, risk difference for active proportion

### Multiple Testing
We test two activity metrics (total downloads, recent downloads). Apply Bonferroni correction: α = 0.025 per test.

## Protocol Steps

1. **Fetch need-related crates**: For each keyword, fetch all crates via `/api/v1/keywords/{keyword}/crates?per_page=100` (paginate)
2. **Deduplicate**: Union of all crates across keywords
3. **Sample need-related**: Randomly sample min(200, total_unique) crates
4. **Fetch random crates**: Sample random pages from `/api/v1/crates?per_page=100` until we have ≥ 200 random crates without need-related keywords
5. **Compute metrics**: For each crate, record downloads, recent_downloads, keywords, categories
6. **Classify**: Mark as "active" if recent_downloads > 0
7. **Statistical analysis**: Run proportion test and Mann-Whitney U test
8. **Evaluate gates**: Check G1-G4
9. **Record results**: Save raw data, analysis, and gate evaluations

## API Details
- Base URL: `https://crates.io/api/v1`
- Keyword crates: `/keywords/{keyword}/crates?per_page=100&page={page}`
- General crates: `/crates?per_page=100&page={page}`
- Rate limit: Not explicitly documented; be respectful (add delays)
- User-Agent: Required (set to "ThinkFree/1.0")

## Success Criteria
All four gates (G1-G4) must PASS for the principle to be considered supported on crates.io.

## Deliverables
- `EXPERIMENTS/095-crates-io-viewcount/PROTOCOL.md` (this file)
- `EXPERIMENTS/095-crates-io-viewcount/README.md` (summary)
- `EXPERIMENTS/095-crates-io-viewcount/collect.py` (data collection script)
- `EXPERIMENTS/095-crates-io-viewcount/analyze.py` (analysis script)
- `EXPERIMENTS/095-crates-io-viewcount/raw/` (raw API responses)
- `EXPERIMENTS/095-crates-io-viewcount/results.json` (gate evaluations and statistics)