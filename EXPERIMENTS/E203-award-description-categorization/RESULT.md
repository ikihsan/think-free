<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E203 RESULT — Award description categorization for 7030 and four comparator PSC codes

**Date:** 2026-10-20. **Outcome: 7030 CONFIRMED as best software market; DA10 and 7A21 are strong software markets but with higher concentration; DA01 and D304 are not software markets.**

## 1. Experiment question

> **Do individual award descriptions in the five IT/software PSC codes confirm the E199/E202 screen prediction that 7030 is the best code for small-team software sales?**

E199 candidate screen and E202 CLI tool used recipient-level concentration metrics. This experiment validates at the **award level** by classifying 5,000 individual award descriptions per code (25,000 total) via the `spending_by_award/` endpoint.

## 2. Methodology

**Data source:** USAspending API `spending_by_award/` endpoint with `fields` parameter requesting: Award ID, Award Amount, Description, Recipient Name, PSC Code, NAICS Code, Agency Name, Funding Agency Name, Start Date, End Date, Award Type, Type of Contract Pricing.

**Time period:** FY2020–FY2025 (consistent with E196–E202).
**Award types:** A, B, C, D (all).
**Sample:** First 50 pages × 100 awards = 5,000 awards per PSC code.

**Categorization:** Keyword-based classification of award descriptions (case-insensitive):
- **Software:** license, saas, subscription, cloud, platform, application, development, programming, api, database, analytics, cybersecurity, devops, github, office 365, erp, crm, machine learning, ai, etl, bi, etc.
- **Service:** support, maintenance, consulting, implementation, integration, managed services, staffing, training, professional services, project management, testing, audit, compliance, etc.
- **Hardware:** server, laptop, desktop, router, switch, storage, monitor, printer, mobile, equipment, appliance, memory, cpu, gpu, hard drive, ssd, etc.
- **Telecom:** bandwidth, circuit, voip, wireless, 5g, fiber, carrier, connectivity, mpls, sd-wan, etc.
- **Other:** No keyword matches.

## 3. Results — all five PSC codes (5,000 awards each)

| Code | Name | Software % (count) | Software % ($ oblig) | Software ≤$40k | Software ≤$100k | Top-10 Share | Assessment |
|------|------|-------------------|---------------------|----------------|-----------------|--------------|------------|
| **7030** | IT Software | **64.5%** | **75.6%** | **41.4%** | **62.8%** | **45.3%** | **✅ STRONG** |
| **DA10** | App Dev SaaS | 57.8% | 64.7% | 49.9% | 69.7% | 59.1% | ✅ STRONG |
| **7A21** | Business App SW | 71.8% | 84.1% | 41.6% | 64.8% | 62.3% | ✅ STRONG* |
| **DA01** | App Dev Support | 12.8% | 57.9% | 15.6% | 29.5% | 52.3% | ❌ WEAK |
| **D304** | Telecom | 8.1% | 25.4% | 54.8% | 70.3% | 75.0% | ❌ WEAK |

\* 7A21 has strong software % but **extreme concentration**: Carahsoft alone holds 27.1% of $3.1B.

### 3.1 7030 — Best overall for small software teams

- **3,223 of 5,000 awards (64.5%)** are software, representing **$3.58B (75.6%)** of $4.74B total
- **1,333 software awards (41.4%) ≤ $40k** — very small, highly accessible entry points
- **2,024 software awards (62.8%) ≤ $100k** — within small program threshold
- **Top-10 concentration: 45.3%** — lowest of the three software codes; 54.7% of obligation accessible to newcomers
- **1,363 unique recipients** — large, diverse vendor base
- **Median software award: ~$55k** — well within small-team range

Top 10 includes IBM (11.4%), CA (7.2%), Dell (6.7%), CDW (4.0%), Carahsoft (3.7%) — no single dominant vendor.

### 3.2 DA10 — Strong software market, higher concentration

- 2,891 software awards (57.8%), $1.93B (64.7%)
- Best small-award rates: **49.9% ≤ $40k, 69.7% ≤ $100k**
- **But top-10 concentration: 59.1%** — Accenture (12.0%), Peraton (11.6%), DLT (10.0%), Palantir (8.0%)
- Higher concentration makes it harder for newcomers to break in

### 3.3 7A21 — Highest software %, extreme concentration

- 3,588 software awards (71.8%), $2.61B (84.1%) — most software-heavy code
- Good small-award rates: 41.6% ≤ $40k, 64.8% ≤ $100k
- **But top-10 concentration: 62.3%** — **Carahsoft alone 27.1%**, Dell 9.5%
- Market effectively controlled by large resellers; very difficult for independent software vendors

### 3.4 DA01 — Services market, not software

- Only 641 software awards (12.8%) — **78.4% are services**
- Software obligations are large (57.9% of $5.39B) but **only 15.6% ≤ $40k**
- Dominated by services primes: Advantaged Solutions (16.2%), Accenture (9.0%), Leidos (8.1%)
- This is **application development labor**, not software products

### 3.5 D304 — Telecom market, not software

- Only 407 software awards (8.1%) — **51.1% services, 11.1% telecom**
- **Extreme concentration: 75.0%** — V2X Systems alone **43.7%** of $7.32B
- Telecom/space communications market; not addressable for software teams

## 4. What this decides

**E199/E202 screen prediction CONFIRMED and refined:**

1. **7030 remains the best PSC code for small software teams** — optimal balance of software share (64.5%), small-award accessibility (41.4% ≤ $40k), and moderate concentration (45.3%).

2. **DA10 is a viable alternative** for SaaS/product companies — better small-award rates than 7030 but significantly higher concentration (59.1% vs 45.3%). Suitable if the team can navigate prime-dominated channels.

3. **7A21 is a trap** — highest software % (71.8%) but extreme concentration (62.3%) with Carahsoft at 27.1%. The market is reseller-dominated; independent vendors face steep barriers.

4. **DA01 and D304 are not software markets** — DA01 is labor/services (78.4%), D304 is telecom/services (62.2%). The E199 screen's concentration metric correctly deprioritized them but for the wrong reason: they're not software markets at all.

## 5. Key insight: PSC code labels ≠ market reality

| PSC Code | Label | Actual Market |
|----------|-------|---------------|
| 7030 | Information Technology Software | **Software products (64.5%)** |
| DA10 | IT & Telecom — App Dev, SaaS | **Software products (57.8%)** |
| 7A21 | IT & Telecom — Business App SW, Perpetual | **Software licenses via resellers (71.8%)** |
| DA01 | IT & Telecom — App Dev Support, Labor | **Services/labor (78.4%)** |
| D304 | IT & Telecom — Telecommunications | **Telecom/services (62.2%)** |

**The screen's concentration metric worked as a proxy for "not a software product market" but award-level categorization reveals the true mechanism.**

## 6. Limitations

- Keyword-based categorization has false positives/negatives (e.g., "support" in "software support" → service)
- 5,000 award sample per code (first 50 pages); full dataset would require more pages
- Does not distinguish COTS vs. custom development within software category
- Does not analyze agency distribution or contract vehicle (GSA, SEWP, etc.)

## 7. Next steps

1. **E204 — Time-window analysis:** Compare last 12 months vs. FY2020–FY2025 to detect market trends and new entrant velocity.
2. **E205 — Agency distribution analysis:** Which agencies buy in 7030/DA10, and do small vendors win direct or only subcontract?
3. **Refine categorization:** Add COTS vs. custom development distinction; validate against manual sample.
4. **Build MVP tool:** Package E202 + E203 as a distributable CLI for small teams evaluating federal marketplace entry.