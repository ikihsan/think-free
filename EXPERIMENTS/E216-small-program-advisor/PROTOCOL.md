# E216: Small Program Entrant Advisor — Protocol

## Overview

This experiment implements a reversible exploratory prototype (Small Program Entrant
Advisor) that helps small government contracting and NIH SBIR program applicants
identify the best market entry points. The prototype integrates learnings from all
prior experiments (E204-E215) and fixes the known D128 defect in the NIH
accessibility prototype (missing `activity_codes` filter and 2,000-row cap).

## Goal

Build and document a prototype tool that:
1. Helps small government contracting programs identify the best PSC codes and award
   types for market entry
2. Helps small NIH SBIR programs identify the most accessible Funding Institutes/Centers
3. Uses complete census via API `meta.total` (no arbitrary caps)
4. Supports `activity_codes` filtering per D128

## Architecture

Two integrated modules:

### 1. IT Code Entrant Advisor v3 (`tools/it_entrant_advisor_v3.py`)
- Measures segment newcomer fractions across USAspending PSC codes
- Computes award-type sub-segment analysis (A, B, C, D)
- Uses `meta.total` for complete census (replaces arbitrary 500-page ceiling)
- Provides code-level and award-type-level recommendations

### 2. NIH SBIR Category Advisor v3 (`tools/nih_small_program_advisor_v3.py`)
- Screens NIH SBIR spending categories for small-program accessibility
- Filters by `activity_codes` (e.g. `['R41', 'R42']` for SBIR)
- Uses NIH RePORTER API `meta.total` for complete census
- Ranks Funding ICs by `access_score` (higher = more accessible for small programs)
- Identifies consensus ICs across categories

## Methodology

### IT Code Analysis (per PSC code)
- **Current window**: FY2023 (2023-01-01 to 2023-12-31)
- **Prior window**: FY2018-2022 (2018-01-01 to 2022-12-31)
- **Segment newcomer fraction** = |current recipient IDs absent from prior| / |current recipient IDs|
- **Kill gate threshold**: 0.30 (codes with segment fraction >= 0.30 survive)
- **Fragmentation** = 1 - top-5 obligation share
- **Attractiveness score** = segment_newcomer_fragmentation * obligation_billions

### NIH SBIR Analysis (per spending category)
- **Spending category filter**: e.g. category 101
- **Activity codes filter**: `['R41', 'R42']` for SBIR (per D128)
- **Complete census**: stops when `len(all_results) >= reported_total` (meta.total)
- **Access score** = project_count / (top5_share_fraction) — higher = more accessible
- **Top-5 concentration**: sum of top 5 org amounts / total amount * 100%

## Gates and Thresholds

### IT Code Gates (per E209 design)
- G1: Sample size >= 5 codes (always satisfied with default codes)
- G2: Top-5 vendor concentration <= 80% (computed per code)
- G3: Median segment-newcomer fraction >= 0.30 (kill gate; below = "KILL")
- G4: 100% arrival field coverage (all recipients fetchable via API)

### NIH SBIR Gates (per E204/E206 pattern)
- G1: Sample size >= Funding ICs in category (varies by category)
- G2: Top-5 vendor concentration <= 80% across ICs (varies by category)
- G3: Effect magnitude — differentiation across sub-areas (access_score range)
- G4: Arrival field coverage (100%: all grants fetchable via API)

## Deliverables

1. `tools/it_entrant_advisor_v3.py` — IT code entrant advisor v3
2. `tools/nih_small_program_advisor_v3.py` — NIH SBIR category advisor v3
3. `tools/small_program_advisor.py` — integrated dispatcher
4. `EXPERIMENTS/E216-small-program-advisor/RESULT.md` — experiment results
5. Raw API response data in `tools/raw/` directories
6. Session records via `tools/origin session` workflow

## Risks and Constraints

- Prototype is evidence-gathering, not product validation
- API rate limits may restrict complete censuses for some codes/categories
- D128 defect fix: activity_codes must be properly filtered; meta.total must be used
- No new dependencies: stdlib only (urllib.request)
- Session logging required via `tools/origin session` workflow
- `doc lint` must exit 0 after changes