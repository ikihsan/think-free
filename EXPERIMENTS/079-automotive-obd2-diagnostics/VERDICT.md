# E079 Verdict: Automotive OBD2 Diagnostic Codes Fresh Observation

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

## Summary

**PARTIAL — Gates G2/G3 evaluated on title+tag data; G1/G4 blocked by API throttle; G5 pending manual review.**

The experiment tested whether automotive OBD2 diagnostic trouble codes on Mechanics Stack Exchange form a concentrated, structured problem population suitable for a computational tool.

## Gate Results

| Gate | Threshold | Result | Status |
|------|-----------|--------|--------|
| **G1 Population** | ≥ 200 structured cases | **BLOCKED** — 210 title candidates, 128 answered, but answer bodies not fetched | PENDING |
| **G2 Code concentration** | Top 10 codes ≥ 30% of mentions | 29.0% (262 mentions, 159 unique codes) | **FAIL** |
| **G3 Vehicle coverage** | ≥ 15 vehicle configs for top 10 codes | 30 make-model pairs | **PASS** |
| **G4 Root cause specificity** | ≥ 60% name specific part | **BLOCKED** — requires answer analysis | PENDING |
| **G5 Incumbent gap** | No free tool covers ≥ 50% of top 10 | Not evaluated | PENDING |

## Key Findings

### Population (from 10,251 Mechanics.SE questions)
- **210 questions** contain OBD2 codes in title (2.0%)
- **262 total code mentions** across **159 unique codes** — high dispersion
- **Top 10 codes**: P0420 (18), P0171 (15), P0300 (12), P0302 (5), P0430 (5), P0304 (5), P1135 (4), P0303 (4), P0172 (4), P0507 (4)
- **Classic high-frequency codes dominate**: Catalyst efficiency (P0420/P0430), fuel trim (P0171/P0172), misfire (P0300/P0302/P0303/P0304)
- **25 makes represented** in title candidates (Toyota, Honda, Ford, Chevrolet, etc.)
- **30 vehicle configs** (make+model) for top 10 codes — exceeds G3 threshold

### Critical Limitation: API Throttle
Stack Exchange API allows **300 requests/day per IP** without a key. The experiment exhausted this quota fetching 10,251 title-only questions. Fetching 210 candidate bodies + answers requires ~20 more requests, but the IP is throttled for ~10 hours.

**Without answer data, G1 and G4 cannot be evaluated.** The 128 answered questions (from metadata) suggest answer data exists, but root cause specificity (G4) and structured case count (G1) require reading answer bodies.

### G2 Near-Miss Analysis
G2 failed by **1 percentage point** (29.0% vs 30.0% threshold). With full body text, additional code mentions would likely increase total mentions and potentially change the ratio. However, the **159 unique codes for 262 mentions** indicates a fundamentally long-tailed distribution — many rare codes.

| Code | Mentions | Description |
|------|----------|-------------|
| P0420 | 18 | Catalyst System Efficiency Below Threshold (Bank 1) |
| P0171 | 15 | System Too Lean (Bank 1) |
| P0300 | 12 | Random/Multiple Cylinder Misfire Detected |
| P0302 | 5 | Cylinder 2 Misfire |
| P0430 | 5 | Catalyst System Efficiency Below Threshold (Bank 2) |
| P0304 | 5 | Cylinder 4 Misfire |

These are the "bread and butter" codes that appear across all makes.

## Incumbent Survey (G5) — Not Performed
Free OBD2 code databases (OBD-Codes.com, Engine-Codes.com, AutoCodes.com) provide generic definitions but limited vehicle-specific root causes. A manual survey of top 10 codes against these sites would be needed.

## Conclusion

**The candidate does not survive on current evidence.**

- G2 **failed** (29% vs 30% threshold) — code concentration insufficient
- G1/G4 **blocked** by API throttle — cannot confirm if structured cases ≥ 200 or if answers name specific parts
- G3 **passed** — vehicle diversity is adequate
- G5 **unknown** — incumbent gap not verified

### Why G2 matters
A computational tool needs a concentrated target. With 159 unique codes for 262 mentions, any tool would need to handle a very long tail. The top 10 codes cover only 29% — the remaining 71% is spread across 149 codes.

### Path forward (if pursuing)
1. **Obtain Stack Exchange API key** (10,000 req/day) to fetch answer data
2. **Use Stack Exchange data dump** (quarterly release on archive.org/Kaggle)
3. **Alternative source**: Reddit r/mechanicadvice (Pushshift/API), automotive forums
4. **Lower G2 threshold** to 25% and re-evaluate — but this weakens the concentration argument

### Recommendation
**Do not pursue this candidate further without answer data.** The API throttle is a solvable infrastructure problem (API key), but the near-miss on G2 and the fundamental long-tail distribution suggest the population may not support a focused tool. The domain shows real structure (standardized codes, vehicle tags) but the concentration is marginal.

**Record as F105 (tentative): Automotive OBD2 population on Mechanics.SE shows structure but insufficient code concentration (G2 FAIL at 29%), answer data inaccessible due to API throttle.**

---
*Experiment conducted 2026-10-09. API throttle hit at ~300 requests. Raw data: 10,251 questions, 210 title candidates, 262 code mentions, 159 unique codes.*