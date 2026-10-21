<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E201 PROTOCOL — MVP prototype for small-team software sales into 7030 federal marketplace

**Purpose:** Build a minimal viable prototype that demonstrates small-team accessibility into the PSC code 7030 ("Information technology software") federal marketplace, validating the E199 candidate screen's prediction that 7030 admits programs a small team could build and sell.

**Screen prediction to validate (from E199):**
- 7030 has 3,915 distinct recipients and 38.4% top-10 concentration
- Score = 3,915 × (1 − 0.384) = 2,412 (highest of 5 codes)
- This combination predicts good small-team accessibility: large market + moderate concentration

**Experiment methodology:**

1. **Data source:** USAspending API `spending_by_category/recipient/` endpoint
   - Filter: `psc_codes: ["7030"]`, `award_type_codes: ["A", "B", "C", "D"]`, `spending_level: "awards"`
   - Time period: FY2020–FY2025 (consistent with E196-E198)

2. **Collection:** Paginate through all results, capturing each page's body + sha256 for reproducibility
   - Expected: ~40 pages to reach 3,915 recipients (100 per page)

3. **Analysis metrics:**
   - Total distinct recipients (expected: ~3,915)
   - Top-10 recipients' share of total obligation (expected: ~38.4%)
   - Recipient award count distribution (expected: ~3,913 with exactly 1 award)
   - Awards by size category:
     - ≤ $40k (very small, highly accessible)
     - ≤ $100k (small program threshold)
     - > $100k (larger awards)
   - Sample award description categorization (software vs. service vs. other)
     - Note: The recipient endpoint provides recipient-level data; description categorization may require additional `spending_by_award/` queries

4. **Small-team entry metrics:**
   - Count of recipients with ≤ $40k total obligation (potential "very small" entry points)
   - Count of recipients with ≤ $100k total obligation (small program threshold)
   - Fraction of recipients with exactly 1 award (entry points for newcomers without established track records)
   - Concentration analysis: top-10 share leaving ~62% of obligation potentially accessible

5. **Kill gate:** N/A — this is a prototype validation, not a gate-validated experiment. The purpose is to support or refute the E199 screen's prediction.

6. **Data integrity:** Each response body is saved with its sha256 hash and request payload metadata, so a later reader can distinguish API changes from parse defects.

**Expected outcome if screen is correct:**
- Recipient count near 3,915
- Top-10 share near 38.4%
- Significant fraction of recipients with ≤ $40k obligation (≈29.9%)
- Significant fraction of recipients with ≤ $100k obligation (≈45.1%)
- ~3,913 recipients with exactly 1 award (entry points for new vendors)
- Non-trivial fraction of award descriptions categorizable as "software"

**Refuting outcome:**
- Recipient count orders of magnitude different
- Top-10 share dramatically different (e.g., > 50%)
- Overwhelming majority of recipients have obligations >> $100k
- Nearly all recipients have many awards (no single-award entry points)
- Award descriptions uniformly categorize as "service" or "other" with no "software" category

**Reference data (from pre-run exploration):**
- 3,915 unique recipients from 3,917 total awards
- Median recipient obligation: $132,858
- Recipients ≤ $40k: 1,134 (29.9%)
- Recipients ≤ $100k: 1,711 (45.1%)
- Recipients > $100k: 2,083 (54.9%)
- Top-10 recipients' total obligation: ~$9.93B of ~$25.83B cell total
- ~2 recipients have multiple awards; ~3,913 have exactly 1 award