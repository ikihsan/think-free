<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E205 RESULT — Agency distribution analysis for 7030, DA10, 7A21

**Date:** 2026-10-20. **Outcome: All three codes are DOD-dominated; DA10 has unique VA/GSA channels; 7030 has broadest agency base; small-business-like recipients exist but are mostly large resellers.**

## 1. Experiment question

> **Which agencies buy in the top software PSC codes, and do small vendors win direct awards or only subcontract?**

E203–E204 established market composition and trends. This experiment maps the buyer landscape (funding/awarding agencies) and analyzes whether recipients with small-award portfolios (proxy for small businesses) win direct agency awards.

## 2. Methodology

**Data sources:**
- `spending_by_category/funding_agency/` — agencies providing funds
- `spending_by_category/awarding_agency/` — agencies issuing contracts
- `spending_by_category/federal_account/` — specific budget lines
- `spending_by_award/` — 5,000 awards per code for recipient analysis

**Time period:** FY2020–FY2025 (consistent with E196–E204).
**Small-business proxy:** Recipients with ≥3 awards and >50% of awards ≤ $100k.
**Limitation:** Award-level endpoint does not return agency names; agency analysis uses category endpoints only.

## 3. Agency landscape comparison

| Metric | **7030** (IT Software) | **DA10** (App Dev SaaS) | **7A21** (Business App SW) |
|--------|------------------------|-------------------------|----------------------------|
| **Total obligation (funding)** | $76.2B | $36.6B | $33.1B |
| **Top funding agency** | DOD (51.9%) | DOD (41.7%) | DOD (51.6%) |
| **2nd agency** | DHS (9.0%) | **VA (19.4%)** | DHS (10.0%) |
| **3rd agency** | Treasury (5.8%) | DHS (7.7%) | HHS (6.0%) |
| **GSA share (funding)** | 0.8% | 1.2% | 0.3% |
| **Funding agency concentration (top 5)** | 75.7% | 79.1% | 75.5% |
| **Awarding agency concentration (top 5)** | 73.2% | 76.0% | 75.2% |

### 3.1 Key agency differentiators

**7030 — Broadest civilian agency base**
- DOD dominant (51.9%) but 14+ agencies > $500M
- Strong Treasury (IRS), SSA, DOJ, HHS, USDA, State presence
- GSA is minor (0.8%) — not a GSA Schedule market

**DA10 — Unique VA and GSA channels**
- **VA is 2nd largest at 19.4%** ($7.1B) — distinct from other codes
- GSA is 3rd awarding agency (8.0%, $2.9B) — **GSA Schedule/FAS market**
- NASA 2.4% — only code with significant NASA spend
- More civilian-heavy than 7030/7A21

**7A21 — DOD/State-heavy, minimal GSA**
- DOD 51.6%, DHS 10.0%
- State Dept 4.5% (diplomatic/consular programs)
- GSA negligible (0.3% funding, 1.2% awarding)
- Traditional defense/intel software license market

### 3.2 Federal account concentration (budget line visibility)

| Code | Top 5 Accounts | Top Account |
|------|---------------|-------------|
| **7030** | 21.2% | SSA Salaries (6.3%) |
| **DA10** | 33.8% | VA IT Systems (9.2%) |
| **7A21** | 20.6% | Army O&M (4.9%) |

- **DA10 has highest federal account concentration** (33.8% top 5) — driven by VA and GSA centralized funds
- **7030 and 7A21 more distributed** across DOD service accounts
- Federal account data reveals *specific budget lines* — useful for targeting

## 4. Recipient analysis: direct vs. subcontractor proxy

**Method:** Recipients with awards from multiple agencies (via category data) would indicate prime contractors. Since award-level data lacks agency, we use **award count + small-award fraction** as small-business proxy.

### 4.1 Small-business-like recipients (≥3 awards, >50% ≤ $100k)

| Code | Total Recipients | Small-Biz-Like | % of Recipients | Top Small-Biz Recipient |
|------|-----------------|----------------|-----------------|------------------------|
| **7030** | 1,363 | **195** | **14.3%** | Dell Marketing ($318M, 71% small) |
| **DA10** | 882 | **207** | **23.5%** | DLT Solutions ($298M, 82% small) |
| **7A21** | 845 | **200** | **23.7%** | Carahsoft ($839M, 57% small) |

**Critical finding:** The "small-business-like" recipients are **not small businesses** — they are large resellers (Carahsoft, DLT, Dell, CDW, Four LLC, Insight, World Wide Tech) with high volumes of small individual awards.

### 4.2 Genuine small business assessment

Looking at recipients with **lower total obligation** (< $50M) and high small-award fraction:

| Code | Candidate | Obligation | Awards | Small % | Software % |
|------|-----------|------------|--------|---------|------------|
| **7030** | GOVSMART, INC. | $48M | 30 | 73% | 98% |
| **7030** | METGREEN SOLUTIONS | $34M | 7 | 71% | 100% |
| **7030** | EC AMERICA, INC | $28M | 33 | 73% | 98% |
| **7030** | SHI INTERNATIONAL | $21M | 24 | 58% | 99% |
| **DA10** | REDHAWK IT SOLUTIONS | $11M | 44 | 84% | 95% |
| **DA10** | STERLING COMPUTERS | $10M | 45 | 89% | 89% |
| **DA10** | ANSYS INC | $10M | 54 | 63% | 79% |
| **7A21** | RED RIVER TECHNOLOGY | $19M | 50 | 58% | 98% |
| **7A21** | VERTOSOFT, LLC | $12M | 39 | 54% | 69% |
| **7A21** | BLAZAR TECHNOLOGY | $8M | 38 | 66% | 87% |

**These are still mid-size resellers ($8–$48M), not small software vendors.**

### 4.3 Award size distribution

| Threshold | **7030** | **DA10** | **7A21** |
|-----------|----------|----------|----------|
| ≤ $10k | 10.9% | **16.3%** | 7.0% |
| ≤ $25k | 29.9% | **37.3%** | 30.2% |
| ≤ $40k | 42.0% | **49.5%** | 42.2% |
| ≤ $100k | 63.4% | **70.2%** | 66.4% |
| **Software median** | $58,010 | **$40,867** | $53,821 |

**DA10 has the most accessible award sizes** — highest fraction of small awards, lowest software median.

## 5. What this decides for small-team strategy

### 5.1 Agency targeting

| Code | Primary Target | Secondary Targets | Access Mechanism |
|------|---------------|-------------------|------------------|
| **7030** | DOD (Army, Air Force, Navy, Defense-Wide) | DHS, Treasury/IRS, SSA, DOJ, HHS | Multiple contract vehicles (SEWP, CIO-SP4, GSA) |
| **DA10** | **VA (VHA/VBA)** | DOD, GSA/FAS, DHS, USDA, NASA | **GSA Schedule**, VA T4NG, DOD vehicles |
| **7A21** | DOD (Army, Defense-Wide) | DHS, State, HHS, DOJ | Traditional DOD vehicles, limited GSA |

### 5.2 Small vendor reality check

**No genuine small software vendors (< $10M) found in top 5,000 awards.** The "small-business-like" recipients are mid-to-large resellers. This means:

1. **Direct awards to small software vendors are rare** in the 5,000-award sample
2. **Subcontracting through primes/resellers** is the likely entry path
3. **GSA Schedule / SEWP / CIO-SP4** are the vehicles where small vendors can get contract access
4. **DA10's GSA channel (8% awarding)** is a concrete access point for Schedule holders

### 5.3 Vehicle implications

- **7030:** SEWP VI, CIO-SP4, GSA MAS, NASA SEWP — broad vehicle access
- **DA10:** **GSA MAS (Multiple Award Schedule) is primary**, plus VA T4NG, DOD vehicles
- **7A21:** DOD-focused vehicles (SEWP, CIO-SP4), minimal GSA

## 6. Cross-experiment synthesis (E203–E205)

| Dimension | **7030** | **DA10** | **7A21** |
|-----------|----------|----------|----------|
| **Software market fit (E203)** | ✅ Strong (64.5%) | ✅ Strong (57.8%) | ✅ Strong (71.8%) |
| **Trend (E204)** | ⚠️ Concentrating fast | ✅ Diversifying | ❌ Hardening |
| **Agency access (E205)** | Broad DOD + civilian | **VA + GSA + DOD** | DOD + State |
| **Award accessibility** | Good (42% ≤ $40k) | **Best (49.5% ≤ $40k)** | Good (42.2% ≤ $40k) |
| **Reseller dominance** | Moderate | High (DLT, Carahsoft) | **Extreme (Carahsoft 27%)** |
| **Overall for small team** | **Good, but window closing** | **Best overall** | Avoid |

**DA10 emerges as the best code for small teams** despite lower total obligation than 7030:
- Diversifying vendor landscape (E204)
- GSA Schedule access channel (E205)
- Most small awards (E205)
- VA as dedicated major buyer (E205)
- Lower software median award ($40,867)

## 7. Limitations

- Award-level API lacks agency names; cannot directly link recipients to agencies
- Small-business proxy (award count + size) identifies resellers, not genuine small vendors
- 5,000 award sample per code; full dataset larger
- Does not analyze contract vehicles directly (SEWP, GSA, CIO-SP4)
- Federal account data shows budget lines but not award-level vehicle

## 8. Next steps

1. **Contract vehicle analysis:** Map awards to SEWP, GSA MAS, CIO-SP4, VA T4NG to identify which vehicles small vendors actually use.
2. **Subcontractor analysis:** Use USAspending subawards endpoint to trace prime→sub relationships.
3. **GSA Schedule holder validation:** Cross-reference GSA Schedule holders with DA10/7030 recipients.
4. **Build MVP tool:** Package E202–E205 as distributable CLI for small teams evaluating federal entry.
5. **Field test:** Recruit 3–5 small software companies to validate the assessment framework.