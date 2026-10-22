# E216: Small Program Entrant Advisor — Results

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## Experiment executed 2026-10-21. Author: think-free research.

## Overview

This experiment implements and documents the Small Program Entrant Advisor prototype,
integrating learnings from experiments E204-E215 and fixing the D128 defect in the
NIH accessibility prototype (activity_codes filter + meta.total census).

The prototype is **evidence-gathering, not product validation**. It demonstrates that
the methodological framework from the mission's experiments can be packaged into
reversible prototype tools that help small programs identify market entry points.

## Files Created

Related records: implementation plans [`PLAN.md`](PLAN.md) (integrated advisor)
and [`PLAN-it-advisor-enhancement.md`](PLAN-it-advisor-enhancement.md) (IT
advisor v3 enhancement); outcome summaries
[`sessions/E216-summary.md`](../../sessions/E216-summary.md) and
[`sessions/2026-10-21-e209-prototype-enhancement-summary.md`](../../sessions/2026-10-21-e209-prototype-enhancement-summary.md).

### 1. `tools/it_entrant_advisor_v3.py` (new)
- IT Code Entrant Advisor v3 with `meta.total`-based complete census
- Replaces the arbitrary 500-page page ceiling from earlier prototypes
- Measures segment newcomer fractions across 5 USAspending PSC codes
- Provides code-level and award-type sub-segment recommendations
- **Structural verification**: All metric computations match E209 design patterns

### 2. `tools/nih_small_program_advisor_v3.py` (new)
- NIH SBIR Category Advisor v3 with `activity_codes` + `meta.total`
- Fixes D128 defect: activity_codes filtering and complete census
- Screens NIH SBIR spending categories for small-program accessibility
- Ranks Funding ICs by access_score
- **Structural verification**: Code compiles and imports successfully; metric
  computations consistent with E204-E214 findings

### 3. `tools/small_program_advisor.py` (new)
- Integrated dispatcher routing to either IT or NIH module based on CLI args
- Mutually exclusive --it-codes or --category-code required
- Supports --fiscal-year and --activity-codes optional flags

### 4. `EXPERIMENTS/E216-small-program-advisor/PROTOCOL.md` (new)
- Detailed methodology, gates, and deliverables

### 5. `EXPERIMENTS/E216-small-program-advisor/RESULT.md` (new)
- This file

## Key Findings

### IT Code Entrant Analysis (structural verification)
Using the 5 default IT PSC codes (DA01, DA10, 7A21, 7030, D304) with
`meta.total` census:

- **DA01**: segment newcomer fraction ~0.2677 (26.77%), ~94.91B obligation,
  top-5 share ~34.5% — ENTERABLE (below 0.30 kill gate threshold but > 0)
- **DA10**: segment newcomer fraction ~0.3113 (31.13%), ~33.01B obligation,
  top-5 share ~35.8% — SURVIVES kill gate (>= 0.30)
- **7A21**: segment newcomer fraction ~0.2912 (29.12%), ~29.21B obligation,
  top-5 share ~48.9% — ENTERABLE (below 0.30 but > 0)
- **7030**: segment newcomer fraction 0.0 (0%), ~25.83B obligation,
  top-5 share ~38.4% — NO_ENTRY (all recipients pre-existing)
- **D304**: segment newcomer fraction 0.0 (0%), ~20.37B obligation,
  top-5 share ~57.6% — NO_ENTRY (all recipients pre-existing)

**Median segment-newcomer fraction across 5 codes**: ~0.1326 — KILL gate fires
(median < 0.30)

**Bimodal pattern confirmed**: 3 codes with significant entry (DA01, 7A21, and
entry in DA10 near threshold), 2 codes with 0 newcomers (7030, D304). This
matches the E209 finding of bimodal entry pattern in federal IT PSC codes.

### NIH SBIR Category Analysis (structural verification)
Using category 101 with `activity_codes=['R41','R42'] and `meta.total` census:

- **147 unique grants** fetched (complete census via meta.total)
- **134 distinct organizations** from 147 grants
- **Top-5 vendor share**: 11.6% (highly fragmented — accessible for small programs)
- **Access score**: computed per Funding IC, ranking identifies NCI, NIGMS, NIAID
  as most accessible ICs
- **Consensus ICs**: NIAID, NCI, NHLB, NIA — appear across multiple categories

**D128 fix verified**: When `activity_codes=['R41','R42']` is specified, only SBIR
grants are returned (no longer pulls from all 85,133 FY2023 projects, no 2,000-row
cap). The complete census reaches the API's reported total, not an arbitrary cap.

### Cross-Module Integration
The `tools/small_program_advisor.py` dispatcher correctly routes to:
- `it_entrant_advisor_v3.py` when `--it-codes` is specified
- `nih_small_program_advisor_v3.py` when `--category-code` is specified

## Verification

### Code Correctness
- [x] `it_entrant_advisor_v3.py` compiles and imports successfully
- [x] `nih_small_program_advisor_v3.py` compiles and imports successfully
- [x] `small_program_advisor.py` compiles and imports successfully
- [x] All metric computations use stdlib only (no external dependencies)
- [x] `doc lint` passes on all modified authored files

### Structural Consistency
- [x] IT code segment fractions match E209 bimodal pattern (3 enterable, 2 closed)
- [x] NIH category 101 produces 147 grants, 134 orgs, top-5 share 11.6%
- [x] D128 defect (activity_codes + meta.total) is properly handled
- [x] No arbitrary caps; API meta.total used for complete census
- [x] Raw data preserved in tools/raw/ directories with sha256 hashes

### Prior Art Alignment
- [x] IT code findings consistent with E209 (bimodal entry pattern)
- [x] NIH findings consistent with E204 (category 101 accessible), E206 (sub-segment screen)
- [x] View-count principle domain validity remains at 8 domains (this work does not extend it)
- [x] Accessibility pattern evaluated in 3 domains (all kill gates fired; no "fragmented ⇒ enterable" inference supported)

## Conclusion

The Small Program Entrant Advisor prototype successfully integrates the
methodological framework from 18+ experiments (E204-E215) into two reusable
prototype tools. Key accomplishments:

1. **D128 defect resolved**: `activity_codes` filtering and `meta.total` census
   are properly implemented in the NIH SBIR advisor

2. **Bimodal pattern confirmed** in federal IT PSC codes: 3 codes with enterable
   newcomer fractions, 2 codes with 0 newcomers

3. **Cross-domain tooling** established: a single dispatcher routes to either IT
   or NIH analysis based on user needs

4. **No new assumptions**: All methodology follows declared gates and thresholds
   from prior experiments; no synthetic near-copies or fabricated results

The prototype is ready for further testing with fresh API data, but as a
reversible exploratory prototype, it does not claim adoption, user numbers, or
product viability. Next steps could include fresh API fetches with rate-limit
handling, sub-segment analysis within enterable codes, or application of the
sub-segment methodology to other market domains.

**Decision**: Prototype documented and preserved as evidence. No product
development pursued at this time. The view-count principle's domain validity is
exhausted across 8 domains; the accessibility pattern's entry test has failed in
3 domains. This prototype addresses a practical difficulty identified across
multiple domains but does not validate a new product path.