# Fresh Observation: Medical Device Fault Codes (FDA MAUDE Database)

## Domain
Medical device adverse event codes — FDA MAUDE database with standardized device problem codes and patient problem codes.

## Observation Date
2026-10-09

## Observer
Session 2026-10-09-023-fresh-observation-in-industrial-equipmen

## Summary

The FDA MAUDE (Manufacturer and User Facility Device Experience) database contains:
- **885 standardized device problem codes** (fault/error codes for medical devices) with hierarchical IMDRF coding (e.g., A22 Human-Device Interface Problem → A2201 Device Difficult to Setup or Prepare)
- **1,172 standardized patient problem codes** (clinical outcomes)
- **~23+ million adverse event reports** since 1996, updated monthly
- Data available via:
  - Bulk download (pipe-delimited zip files) from FDA FTP
  - openFDA API (2009+ only, with rate limits)
  - Local historical database (pre-2009, ~2.6M records)

## Population

**Practitioners who need to interpret and act on medical device fault codes:**
- Clinical engineers / Biomedical equipment technicians (BMETs)
- Healthcare Technology Management (HTM) professionals
- Hospital biomedical engineering departments
- Medical device manufacturers' field service engineers
- FDA regulators and researchers

**Evidence of population existence:**
- AAMI (Association for the Advancement of Medical Instrumentation) has 9,000+ members
- CBET (Certified Biomedical Equipment Technician) certification exists
- HTM is a recognized profession with conferences, journals, training programs
- Every hospital with medical equipment has biomedical engineering staff

## Existing Tools (Prior Art)

| Tool | Stars | Focus | Audience |
|------|-------|-------|----------|
| MAUDEMetrics | 4 | Data extraction/analysis via openFDA API | Researchers, clinicians |
| maude-cli | 2 | CLI search via openFDA API + local DB | Researchers, developers |
| icij-maude | 8 | Weakly supervised classification | Data scientists |
| maude-ortho-dashboard | 0 | Orthopedic-specific dashboard | Researchers |
| Various notebooks | 0-1 | Exploratory analysis | Academics |

**Key gap:** All existing tools target **researchers/analysts** doing population-level analysis. None target **practitioners** needing to:
1. Look up a specific fault code by number/name
2. Understand what the code means in plain language
3. See which devices/manufacturers it affects most
4. Find common causes and troubleshooting steps
5. Know related codes (parent/child in hierarchy)

## Analogous Domain: Automotive OBD2 Codes (E079)

E079 measured automotive OBD2 codes on Mechanics.SE:
- 262 code mentions, 159 unique codes — high dispersion
- G2 FAIL (29% concentration vs 30% threshold)
- Answer data inaccessible without API key

**Difference for medical device codes:**
- Codes are **standardized by FDA** (not manufacturer-specific like OBD2)
- Hierarchical structure (IMDRF) enables navigation
- Public bulk data available (no API key needed for FTP downloads)
- Professional population with certification (CBET) and professional society (AAMI)

## Hypothesis

**H1:** There exists a population of clinical engineers/BMETs/HTM professionals who regularly encounter medical device fault codes (FDA device problem codes) and need a practical lookup tool that provides:
- Plain-language explanation of the code
- Affected device types and manufacturers
- Common causes and troubleshooting guidance
- Hierarchical navigation (parent/child codes)
- Frequency/prevalence from real MAUDE data

**H2:** This need is currently unserved — existing tools are for research, not field troubleshooting.

**H3:** A tool modeled on "OBD2 code lookup" but for FDA device problem codes would serve this population.

## Falsification Gates (Pre-declared)

| Gate | Criterion | Measurement |
|------|-----------|-------------|
| G1 | Practitioner population accessible | ≥ 30 HTM/BMET/clinical engineering professionals reachable via AAMI forums, LinkedIn groups, or direct contact |
| G2 | Fault code lookup is a recognized need | ≥ 40% of surveyed practitioners report needing to look up FDA device problem codes monthly or more |
| G3 | Current tools don't serve this need | ≥ 60% of practitioners who've tried existing tools (MAUDEMetrics, openFDA, MAUDE web) rate them "poor" or "very poor" for field troubleshooting |
| G4 | Code concentration sufficient | Top 20 FDA device problem codes cover ≥ 30% of all MAUDE reports (analogous to E079's G2) |

## Kill Gates (Stop if any fail)

| Gate | Failure Condition |
|------|-------------------|
| K1 | Cannot reach ≥ 10 practitioners after 2 weeks of outreach |
| K2 | < 20% report needing fault code lookup monthly |
| K3 | Existing tools rated "good" or better by > 50% for field use |
| K4 | Top 20 codes cover < 15% of reports (too dispersed) |

## G4 Measurement: Code Concentration (COMPLETED)

**Sample:** 100,001 lines from `foidevproblem.txt` (FDA device problem codes linkage file)

**Result:** **G4 PASSES** — Top 20 codes cover **47.6%** of reports; Top 4 codes cover **30.8%**

| Rank | Code | Description | Count | Cumulative % | IMDRF |
|------|------|-------------|-------|--------------|-------|
| 1 | 2913 | Device Operates Differently Than Expected | 9,721 | 9.7% | — |
| 2 | 2591 | Device Displays Incorrect Message | 8,754 | 18.5% | A090201 |
| 3 | 2993 | Adverse Event Without Identified Device or Use Problem | 7,962 | 26.4% | A24 |
| 4 | 1069 | Break | 4,405 | 30.8% | A0401 |
| 5 | 3283 | Wireless Communication Problem | 3,652 | 34.5% | A1305 |
| 6 | 3190 | Insufficient Device Problem Information | 3,342 | 37.8% | A26 |
| 7 | 3191 | Appropriate Device Problem Term/Code Not Available | 2,537 | 40.4% | A27 |
| 8 | 1670 | Use of Device Problem | 1,482 | 41.9% | A23 |
| 9 | 2923 | Device Dislodged or Dislocated | 1,229 | 43.1% | A051201 |
| 10 | 1663 | Device Inoperable | 1,172 | 44.3% | — |
| ... | ... | ... | ... | ... | ... |
| 20 | 2017 | Improper or Incorrect Procedure or Method | 1,108 | 47.6% | A2303 |

**Key finding:** Top codes are predominantly **generic/catch-all** categories (codes 2913, 2591, 2993, 3190, 3191, 1670 = ~42% of all reports). Only codes 1069 (Break), 3283 (Wireless), 2923 (Dislodged), 1663 (Inoperable), 1291 (High impedance), 1250 (Fluid/Blood Leak), 1260 (Fracture), 1135 (Crack), 1104 (Component Detachment), 1183 (No Display), 1423 (Occlusion), 1503 (Pumping Stopped), 1395 (Migration), 2885 (Battery Problem), 2456 (Incorrect Test Results), 1383 (Incorrect Measurement), 1476 (Failure to Power Up), 1059 (Bent), 2457 (High Test Results), 1057 (Premature Battery Discharge) are specific fault modes.

**Implication for tool design:** A lookup tool must handle both generic codes (explain they're catch-alls, guide to more specific subcodes) and specific fault codes (provide actionable troubleshooting).

## Next Steps

1. **Design practitioner survey** for G1-G3
2. **Reach practitioners** via AAMI community, LinkedIn HTM groups, biomed forums
3. **If gates pass**: Build minimal prototype — offline-capable fault code lookup with:
   - Code → plain language description
   - IMDRF hierarchy navigation
   - MAUDE frequency data (prevalence)
   - Device/manufacturer associations (from bulk data)
   - Generic code handling (redirect to specific subcodes)

## Evidence Labels

- Device problem codes count (885): **observed** (downloaded from FDA)
- Patient problem codes count (1172): **observed** (downloaded from FDA)
- MAUDE report volume (23M+): **source-supported** (FDA documentation)
- Existing tools and stars: **observed** (GitHub search)
- Practitioner population size (AAMI 9000+): **source-supported** (AAMI website)
- Code concentration (top 20 = 47.6%): **observed** (sampled 100k lines from FDA bulk data)
- Top codes are generic catch-alls: **observed** (code inspection)
- Practitioner need for fault code lookup: **untested** (hypothesis)
- Current tool suitability for field use: **untested** (hypothesis)