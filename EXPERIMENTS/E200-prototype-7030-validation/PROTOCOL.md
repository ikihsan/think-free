<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E200 PROTOCOL — prototype validation of 7030 candidate screen

**Purpose:** Validate E199's candidate screen prediction that PSC code 7030 ("Information technology software") admits a program a small team could build and sell.

**Screen prediction to validate:**
- 7030 has 3,917 distinct recipients and 38.4% top-10 concentration
- Score = 3,917 × (1 − 0.384) = 2,412 (highest of 5 codes)
- This combination predicts good small-team accessibility: large market + moderate concentration

**Experiment methodology:**

1. **Data source:** USAspending API `spending_by_category/recipient/` endpoint
2. **Filter:** `psc_codes: ["7030"]`, `award_type_codes: ["A", "B", "C", "D"]`, `spending_level: "awards"`
3. **Collection:** Paginate through all results, capturing each page's body + sha256 for reproducibility
4. **Analysis metrics:**
   - Total distinct recipients
   - Total awards collected
   - Total obligation (sum of award amounts)
   - Average award size
   - Awards ≤ $40k (very small, more accessible)
   - Awards ≤ $100k (small program threshold)
   - Recipient award count distribution (how many have exactly 1 award?)
   - Top-10 recipients' share of total obligation
   - Sample award descriptions (categorize as software, service, hardware, etc.)

**Kill gate:** N/A — this is a prototype validation, not a gate-validated experiment. The purpose is to support or refute the E199 screen's prediction.

**Data integrity:** Each response body is saved with its sha256 hash and request payload metadata, so a later reader can distinguish API changes from parse defects.

**Expected outcome if screen is correct:**
- Recipient count near 3,917
- Top-10 share near 38.4%
- Significant fraction of recipients with exactly 1 award (entry points)
- Non-trivial fraction of awards ≤ $40k and ≤ $100k

**Refuting outcome:**
- Recipient count orders of magnitude different
- Top-10 share dramatically different (e.g., > 70%)
- Overwhelming majority of awards >> $100k
- Nearly all recipients have many awards (no entry points)