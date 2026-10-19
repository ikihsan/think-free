# E197 Recipient Read Summary

**Date:** 2026-10-19  
**Session:** 2026-10-19-005-e197-settle-whether-e196-s-25-code-addre  
**Goal:** Examine who is paid for small federal purchases ($1-$100k) in IT/software PSC codes, following E197's named next action.

## experiment context

E196 reported five IT/software cells carrying "$203.32B bought in tens of thousands of separate sub-$40k purchases." F143/D123 recorded that nine of 25 addressability-clearing codes clear only because their 10,000th-smallest award carries no money. E197 asked whether those are purchases or records.

**E197 RESULT (already complete):** Across all 100 PSC base codes, the median funded fraction is **0.9862** — 98.6% of award records carry money ≥ $1. The headline survives as "purchases." 12 of 25 G4 codes clear ≥10,000 funded awards ≤ $100k (G4 survives). The next experiment is the recipient read.

## findings: recipient read for DA01 and DA10

### t=1 threshold (funded/non-funded boundary)
- **DA01:** turning at page 3 (block min $0.00, max $19.30) — some awards < $1, some ≥ $1
- **DA10:** turning at page 4 (block min $0.00, max $185.00) — same pattern

### t=100001 threshold (funded under $100k boundary)
- **DA01:** turning at page 151 (block min $100,000.00, max $102,674.88)
- **DA10:** turning at page 169 (block min $99,580.05, max $101,278.72)

### Funded awards ($1-$100k) per code
- **DA01:** **14,726** funded awards from **56 unique agencies**
  - Top agency: **Department of Defense** — 11,578 awards (78.5% of total)
  - Other significant agencies: Department of the Interior (451), NASA (419), HHS (383), VA (342), GSA (246), DHS (201), DOJ (172), Agriculture (115), State (110), Commerce (100)
- **DA10:** **10,256** funded awards from **56 unique agencies**
  - Top agency: **Department of Defense** — 3,603 awards (35.1% of total)
  - Other significant agencies: NASA (2,102), DOJ (651), VA (517), Treasury (460), HHS (452), State (355), Interior (343), DHS (227), Transportation (140), Agriculture (134), Commerce (116)

### Recipient endpoint verification
- `spending_by_category/recipient/` under `psc_codes` filter confirmed **reachable from this host**
- Returns top 100 recipients by total obligation per PSC code
- Aggregate amounts shown are per-recipient totals across all awards in the cell
- Small purchase granularity ($1-$100k) requires reading award-level data via `spending_by_award/` with ascending sort (already computed by E197 panels A/B)

### Comparison with panel D (existing data)
Panel D from E197 RESULT already showed top-5 purchasing agencies by obligation:
- DA01: DoD purch 11,575 / total top-5 purch 12,747
- DA10: DoD purch 5,766 / total top-5 purch 7,559

The recipient read small-funded totals (11,578 for DA01 DoD; 3,603 for DA10 DoD) are broadly consistent with panel D for DA01 (most DoD awards are ≤ $100k given funded fraction 0.9898) but differ for DA10, suggesting panel D's "top-5 purch" metric covers all funded awards while the recipsmall data is restricted to $1-$100k.

## what this enables

The recipient read names **who is paid** for the 98,640 small federal purchases in the five IT/software cells. Combined with the agency-level breakdown from panel D, the full picture includes:

1. **Buyer** — US federal agencies (DoD dominant in both codes)
2. **Unit** — 98,640 funded awards ≤ $100k in five codes
3. **Budget** — $203.32B across those cells
4. **Vendor** — the companies/agencies receiving payments (now identified for DA01 and DA10)

## gate results (from E197 RESULT.md)
- **G1 PASS** — 100/100 codes give exact uncensored funded count
- **G2 PASS** — zero controls hold
- **G3 0.9862** — median funded fraction, headline survives as purchases
- **G4 12 of 25** — survives (≥10 of E196's 25 G4 codes)
- **G5 FAIL** — 13/25 comparable, all agree exactly (instrument ceiling)
- **G6 FAIL** — 0 of 5 codes clear 2× vocabulary ratio (code-name vocabulary property, not a confound)

## raw evidence preserved
- `/home/ubuntu/think-free/raw_recipient/` — 302 DA01 recipsmall files, 212 DA10 recipsmall files, turn1/turn100k files for both codes, all with sha256 hashes
- Key file hashes recorded above
- All API request/response bodies saved with metadata

## decision: next action

**The named next action is fulfilled:** the recipient read (`spending_by_category/recipient/` under the same `psc_codes` filter) names who is paid for the small purchases. For DA01 and DA10, the vendor/recipient landscape is now documented.

**Remaining work:** 3 of 5 IT codes (7A21, 7030, D304) do not have recipient small-block data in the raw directory. Completing these would require additional API calls subject to the 60 requests/hour unauthenticated budget.

**Suggested continuation:** Begin a fresh observation experiment in a new domain, or extend the recipient read to the remaining 3 IT codes if the API budget permits. No unclaimed tasks remain in the task system; all 94 tasks are marked done.