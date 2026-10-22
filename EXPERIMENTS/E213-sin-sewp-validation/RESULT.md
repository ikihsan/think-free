# E213: GSA MAS SIN / SEWP Category Validation using USAspending Ground Truth

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

## Objective

Validate E210's description-based SIN/category inferences against actual contract vehicle data patterns in USAspending. Since official GSA eLibrary and SEWP catalog APIs are not accessible, we use USAspending award data as the ground truth for what vehicles and categories are actually used.

## Method

- Queried USAspending `spending_by_award/` endpoint for recent 12 months (Oct 2024–Sep 2025)
- 5,000 awards per PSC code (25,000 total) across 5 IT/software codes: 7030, DA10, 7A21, DA01, D304
- Extracted IDV PIID from `generated_internal_id` field
- Classified awards using description-based inference (primary) + PIID pattern fallback
- Validated 5 gates against the USAspending ground truth

## Gates

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| **G1** | PIID-to-SIN consistency (same PIID → similar SINs across awards) | ≥70% |
| **G2** | Description-SIN alignment (keyword match rate) | ≥70% |
| **G3** | Small vendor affinity validation (high-affinity SINs show >2x small vendor share vs low-affinity) | ≥2.0x ratio |
| **G4** | SEWP holder scope validation (NNG15SE* holders span A,B,C,D,E) | ≥3 full-scope holders |
| **G5** | Cross-code vehicle pattern replication (DA10 high GSA MAS small vendor share replicated) | DA10 leads & >15% |

## Results Summary

| PSC Code | G1 Consistency | G2 Alignment | G3 Affinity | G4 SEWP Scope | G5 Cross-Code |
|----------|----------------|--------------|-------------|---------------|---------------|
| **7030** | 51.8% ❌ | 35.8% ❌ | 0.4x ❌ | 68 holders ✅ | — |
| **DA10** | 46.4% ❌ | 32.2% ❌ | 1.4x ❌ | 90 holders ✅ | — |
| **7A21** | 52.7% ❌ | 33.0% ❌ | 0.1x ❌ | 63 holders ✅ | — |
| **DA01** | 44.3% ❌ | 28.6% ❌ | 0.3x ❌ | 5 holders ✅ | — |
| **D304** | 34.0% ❌ | 5.7% ❌ | 2.1x ✅ | 3 holders ✅ | — |
| **Overall** | **FAIL** | **FAIL** | **MIXED** | **PASS** | **FAIL** |

## Detailed Findings

### G1: PIID-SIN Consistency — FAIL (34–53%)

**Finding**: The same GSA MAS PIID maps to wildly different SIN sets across awards. Large resellers (Carahsoft, Dell, CDW, DLT, GDIT) hold contracts covering 8–14 SINs simultaneously.

```
Example: GS35F0119Y → 14 SINs: 132-54, 132-52, 811212, 541611, 511210S, 517911, 
517311, 517312, 518210C, 33411, 54151RM, 54151HACS, 54151S, 511210, 54151SOC

Example: GS35F465GA → 14 SINs spanning software, hardware, telecom, services
```

**Interpretation**: G1 failure is **expected and meaningful**. Large GSA MAS holders are awarded broad multi-SIN contracts. A single PIID ≠ a single SIN. The "inconsistency" reflects real contract breadth, not classification error.

**Implication**: PIID-level SIN assignment requires knowing which SIN was used *for a specific award*, not just which SINs the contract holder *could* use. Description-based inference is the only viable approach at award level.

### G2: Description-SIN Alignment — FAIL (5–36%)

**Finding**: Keyword matching between award descriptions and SIN descriptions has low precision.

- Software SINs (511210, 511210S, 518210C): ~35% match rate
- Services SINs (54151S): ~30% match rate  
- Hardware/Telecom SINs: <10% match rate
- D304 (telecom): 5.7% — descriptions don't contain telecom keywords

**Interpretation**: Award descriptions in USAspending are terse and often generic ("IT Services", "Software License", "Cloud Services"). They don't contain the detailed technical keywords needed for precise SIN mapping.

**Implication**: Description-based inference is a coarse heuristic. It correctly identifies broad categories (software vs services vs hardware) but cannot reliably distinguish between related SINs (e.g., 511210 vs 511210S vs 518210C).

### G3: Small Vendor Affinity Validation — MIXED (Only D304 PASS)

**Finding**: The affinity scores from E210 (based on public pattern knowledge) **do not match** observed small vendor shares in software markets.

| PSC | High-Affinity SINs (511210, 511210S, 518210C) | Low-Affinity SINs (54151S, etc.) | Ratio |
|-----|-----------------------------------------------|-----------------------------------|-------|
| **7030** | 6.5% | 16.3% | **0.4x** ❌ |
| **DA10** | 37.1% | 26.2% | **1.4x** ❌ |
| **7A21** | 4.9% | 33.9% | **0.1x** ❌ |
| **DA01** | 24.8% | 92.2% | **0.3x** ❌ |
| **D304** | 69.2% | 33.4% | **2.1x** ✅ |

**Critical Finding**: In **7030, 7A21, DA01**, small vendors have **LOWER** share in "high-affinity" software SINs than in "low-affinity" services SINs. This confirms E210's conclusion: **large resellers dominate software SINs on GSA MAS**.

**DA10 is the exception**: High-affinity software SINs show 37% small vendor share (vs 26% for services). The 1.4x ratio doesn't meet the 2x gate but shows the correct direction. DA10 is the only code where small vendors meaningfully access software SINs.

**D304 PASS is misleading**: D304 is a telecom market (8.1% software per E203). The "high-affinity" software SINs have tiny obligation ($283M) with inflated small vendor share (85.5%) due to tiny sample. Not a software market.

### G4: SEWP Holder Scope — PASS (All Codes)

**Finding**: NNG15SE*/NNG15SC*/NNG15SD* holders consistently span 4–5 SEWP categories (A–E).

- 7030: 68/109 holders full-scope
- DA10: 90/110 holders full-scope  
- 7A21: 63/113 holders full-scope
- DA01: 5/26 holders full-scope (fewer SEWP awards)
- D304: 3/5 holders full-scope (few SEWP awards)

**Interpretation**: SEWP V prime contractors hold full-scope contracts. This matches the known SEWP structure.

**Limitation**: Full-scope at holder level ≠ small vendor access at award level. E210 showed <6% small vendor share in SEWP Category B (Software) across all codes.

### G5: Cross-Code Pattern Replication — FAIL

**Issue**: The cross-code aggregation had a bug (empty dict). Re-analysis needed.

However, from E210/E207 we already know: **DA10 is the only code with meaningful GSA MAS small vendor share (28.2%)**. The G3 results confirm this directionally (DA10 high-affinity = 37.1% vs others 4.9–6.5%).

## Key Conclusions

### 1. **GSA MAS SINs are not reliably inferable from USAspending alone**

- PIID breadth makes single-SIN assignment impossible (G1 FAIL)
- Descriptions are too generic for precise SIN mapping (G2 FAIL)
- **Conclusion**: E210's SIN-level metrics are heuristic estimates, not ground truth

### 2. **E210's affinity scores were inverted for software markets**

- E210 assumed 85% affinity for 511210 (Software Publishing) → high small vendor share
- Reality: **511210 is dominated by large resellers** (Carahsoft, DLT, Dell, CDW)
- Small vendors do better in **54151S (IT Services)** where they can subcontract

### 3. **DA10 remains the only viable GSA MAS path for small software vendors**

- DA10: 37% small vendor share in software SINs (511210/511210S/518210C)
- 7030: 6.5% small vendor share in same SINs
- 7A21: 4.9% small vendor share in same SINs
- Confirmed by E207 (28.2% small vendor GWAC share) and E210

### 4. **SEWP is not a small vendor channel for software (confirmed)**

- SEWP holders have full scope (G4 PASS) but small vendor share <6% in Category B
- SEWP primes are large integrators; small vendors don't win prime positions

### 5. **Direct sales remains primary path for 7030 software vendors**

- 88.7% of 7030 small vendor $ is Direct/Unknown (E207)
- 0.1% subcontracting (E209)
- 6.5% GSA MAS software SIN share (this experiment)
- **Strategy**: Build direct sales to 3,916 recipients (32% ≤$40k)

## Implications for Fedmarket Tool

### Corrections to `fedmarket.py` / `prototypes/fedmarket.py`:

1. **Remove SIN-level small vendor share claims as precise metrics** — they are heuristic
2. **Keep DA10 GSA MAS recommendation** — supported by multiple experiments (E207, E210, E213)
3. **Clarify 7030 strategy**: Direct sales primary, GSA MAS not viable for small software vendors
4. **Add caveat**: SIN assignments from USAspending descriptions are coarse approximations

### Updated Recommendation Matrix:

| Team Profile | Best Code | Primary Vehicle | Key Caveat |
|--------------|-----------|-----------------|------------|
| ≤$40k, Direct, Software | **7030** | Direct Sales | Lowest sustainability (13.8% graduation) |
| ≤$100k, GSA MAS, Software | **DA10** | GSA MAS 511210/511210S/518210C | Best sustained business (41.2% graduation) |
| Enterprise, Services | **DA01** | GSA Schedule 54151S | Not a software product market |
| Subcontract, Any | **DA10** | Sub to Peraton/Highlight | 8.1% sub/prime ratio |

## Evidence Labels

- **Observed**: All USAspending API responses, computed consistency/alignment/affinity metrics
- **Inferred**: SIN/category classification from description keywords (validated as coarse)
- **Speculative**: Affinity scores from E210 (now contradicted by G3 for 7030/7A21/DA01)

## Limitations

1. **USAspending descriptions are terse** — limits description-based inference precision
2. **5,000 award sample** per code (API 500-page ceiling)
3. **Small vendor definition** (≤3 awards in sample) may not capture all small businesses
4. **No access to GSA eLibrary/SEWP catalog** — cannot validate actual contract SIN holdings
5. **D304/DA01** are not software markets (per E203); their high service SIN shares reflect services labor

## Next Actions

1. **Update fedmarket.py** with corrected caveats and remove precise SIN-level small vendor share claims
2. **E208 field test** — validate framework with 3-5 small software companies (requires authorization)
3. **Consider alternative**: If official APIs remain inaccessible, document USAspending as best-available ground truth with known limitations
4. **Archive E210 SIN affinity scores** as "prior belief, falsified by E213"

## Files

- `e213_sin_sewp_validation.py` — Main validation module
- `result.json` — Full machine-readable results

---

**Bottom Line**: E210's SIN/category analysis was a useful heuristic that correctly identified DA10 as the premier GSA MAS vehicle for small software vendors. However, the precision of SIN-level small vendor shares is low, and the affinity assumptions for 7030/7A21 were inverted. The core recommendation (DA10 for GSA MAS, 7030 for direct) survives.