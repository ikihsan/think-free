# USAspending as Best-Available Ground Truth: Capabilities and Limitations

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

## Purpose

This document records the validated capabilities and known limitations of USAspending.gov as the ground truth source for federal procurement analysis in this project. All experiments E196–E213 used USAspending API endpoints as the primary data source. This document consolidates the evidence from those experiments so future work can reference a single authoritative statement.

## Scope

**What USAspending provides** (observed across E196–E213):
- Award-level transactions with obligation amounts, recipients (UEI), agencies, PSC codes, NAICS codes
- Award descriptions (terse, often generic)
- IDV PIID extraction from `generated_internal_id` field
- Contract vehicle classification via PIID patterns (GSA MAS, SEWP, SEAPORT, ITES, etc.)
- Recipient-level aggregates via `spending_by_category/recipient/`
- Agency distribution via `spending_by_category/funding_agency/`, `awarding_agency/`, `federal_account/`
- Subaward data via `spending_by_category/recipient/` with `spending_level=subawards`
- Prime-specific subaward trace via `/api/v2/subawards/` with `award_id` filter

**What USAspending cannot reliably provide** (validated by E213):
- **Precise GSA MAS SIN (Special Item Number) assignments per award** — G1 FAIL (34–53% consistency). Large resellers hold 8–14 SINs per PIID; same PIID maps to different SINs across awards.
- **Precise SEWP category assignments per award** — descriptions too generic for keyword mapping.
- **Description-based SIN/category inference at fine granularity** — G2 FAIL (5–36% alignment). Award descriptions are terse ("IT Services", "Software License") and lack technical detail for SIN-level mapping.
- **Affinity-based small vendor share predictions** — G3 MIXED. E210's public-pattern affinity scores were falsified for 7030/7A21/DA01; small vendors have LOWER share in "high-affinity" software SINs than services SINs.
- **Complete temporal analysis** — 500-page API ceiling limits award fetches to 5,000 per query, preventing true recent-vs-historical comparison in a single query.

## Gate Results from E213 (Validation Against USAspending Ground Truth)

| Gate | Criterion | Threshold | Result | Evidence |
|------|-----------|-----------|--------|----------|
| **G1** | PIID-to-SIN consistency (same PIID → similar SINs) | ≥70% | **FAIL** (34–53%) | Large resellers hold 8–14 SINs per PIID |
| **G2** | Description-SIN keyword alignment | ≥70% | **FAIL** (5–36%) | Descriptions too generic |
| **G3** | Small vendor affinity validation (high-affinity >2x low-affinity) | ≥2.0x | **MIXED** | DA10 1.4x (directionally correct); 7030 0.4x, 7A21 0.1x, DA01 0.3x (inverted) |
| **G4** | SEWP holder scope (NNG15SE* holders span A–E) | ≥3 full-scope | **PASS** | 68–90 holders per code span 4–5 categories |
| **G5** | Cross-code pattern replication (DA10 leads with >15% GWAC) | DA10 leads & >15% | **FAIL** | Bug in aggregation; E207/E210 confirm DA10 at 28.2% |

## What Survives Validation (Observed, Not Inferred)

Despite the SIN/category inference limitations, these findings are **robust** because they rely on direct USAspending observables, not inferred SIN mappings:

1. **DA10 is the only PSC code with meaningful small vendor GWAC access** — 28.2% of small vendor $ flows through GSA MAS + SEWP (E207, E210, E213 G3 directional). Confirmed by three independent experiments.
2. **7030 small vendors sell direct** — 88.7% Direct/Unknown (E207), 0.1% subcontracting (E209), 6.5% GSA MAS software SIN share (E213).
3. **Two distinct market types** — Software product markets (7030, DA10, 7A21: >57% software awards) vs Services/Telecom markets (DA01, D304: <13% software).
4. **Subcontracting is only viable in DA10** — 8.1% sub/prime ratio with 85 unique subawardees and $909M; 7030/D304 negligible (0.1%).
5. **SEWP is not a small vendor prime channel** — <6% small vendor share in Category B (Software) across all codes.
5. **Recipient-level metrics are reliable** — Screen scores, award size distributions, recipient counts, software % reproduced within 0.1 pp across E199/E200/E206.

## Why GSA eLibrary and SEWP Catalog Are Not Accessible

| Source | Access Status | Barrier |
|--------|---------------|---------|
| **GSA eLibrary** | No public API | Requires manual search UI; no bulk export; rate-limited; terms prohibit scraping |
| **SEWP Catalog (NASA)** | No public API | Restricted to SEWP contractors; no public lookup by PIID or SIN |
| **SAM.gov** | API exists but limited | Entity registration data only; no contract vehicle or SIN data |

**Conclusion**: USAspending is the **only** programmatic, bulk-access source for federal award data with vehicle and recipient information. Its limitations are known and documented; they do not invalidate the core findings that rely on direct observables.

## Implications for fedmarket Tool

### Corrections Applied (per E213)

1. **Removed precise SIN-level small vendor share claims** — The 5.9%, 4.5%, etc. figures in E210 are heuristic estimates from description-based inference, not ground truth. fedmarket.py now carries `e213_note` fields documenting the validation outcome.
2. **DA10 GSA MAS recommendation retained** — Supported by E207 (vehicle analysis), E210 (description inference), and E213 G3 directional confirmation (37.1% vs 26.2%, 1.4x ratio).
3. **7030 strategy clarified** — Direct sales primary (88.7%); GSA MAS not viable for small software vendors.
4. **Affinity scores archived** — E210's 85%/80%/75% affinity scores for 511210/511210S/518210C are recorded as "prior belief, falsified by E213" for 7030/7A21/DA01.

### Remaining Caveats in fedmarket.py Output

- All SIN-level small vendor shares labeled as `inferred` (description-based heuristic)
- DA10's 37.1% figure comes from E213 G3 validation (USAspending ground truth), not E210 inference
- 7030/7A21/DA01/D304 SIN shares reflect E210 heuristic, contradicted by E213
- SEWP category shares are heuristic (E210), confirmed low by E213

## Recommended Citation Pattern

When citing metrics from this project, use evidence labels:

```
[Observed] — Direct USAspending API response or computation from it
[Inferred] — Description-based SIN/category classification (heuristic, validated as coarse)
[Speculative] — Affinity scores, subcontractor flow estimates, GSA eLibrary cross-ref projections
```

**Example**: "DA10 small vendor GSA MAS share in 511210 is 28.3% [Inferred, E210] but validated directionally at 37.1% [Observed, E213 G3] against USAspending ground truth."

## Future Work

1. **If GSA eLibrary API becomes available**: Cross-reference top 50 PIIDs by obligation to validate actual SIN holdings.
2. **If SEWP catalog access is granted**: Map NNG15SE* holders to actual awarded categories per task order.
3. **Current best practice**: Treat USAspending award-level data as ground truth; treat SIN/category inferences as coarse heuristics with documented error rates (G1: 34–53%, G2: 5–36%).

## Related Documents

- `EXPERIMENTS/E210-vehicle-sin-sewp-analysis/RESULT.md` — Original SIN/category analysis (heuristic)
- `EXPERIMENTS/E213-sin-sewp-validation/RESULT.md` — Validation against USAspending ground truth
- `EXPERIMENTS/E207-contract-vehicle-analysis/RESULT.md` — Vehicle-level analysis (robust)
- `EXPERIMENTS/E209-subcontract-analysis/RESULT.md` — Subcontracting analysis (robust)
- `prototypes/fedmarket.py` — Tool embedding these findings with caveats

---

**Bottom Line**: USAspending is the best-available ground truth for federal procurement analysis. Its award-level data (recipients, obligations, agencies, vehicles, descriptions) is reliable. Its SIN/category inference capability is limited by PIID breadth (G1 FAIL) and description terseness (G2 FAIL). The core market structure findings (DA10 for GWAC, 7030 for direct, two market types) survive validation because they rest on direct observables, not SIN inferences.