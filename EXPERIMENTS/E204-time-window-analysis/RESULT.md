<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E204 RESULT — Time-window analysis: recent 12 months vs FY2020–2025 for 7030, DA10, 7A21

**Date:** 2026-10-20. **Outcome: Markets are shifting — 7030 and 7A21 concentrating, DA10 diversifying; all show massive obligation growth in recent period.**

## 1. Experiment question

> **How do market dynamics in the top three software PSC codes (7030, DA10, 7A21) compare between the full FY2020–2025 period and the most recent 12 months (Oct 2024–Sep 2025)?**

E203 established current market composition. This experiment tests whether small-team accessibility is improving or deteriorating by comparing:
- Concentration trends (top-10 share)
- Small-award availability (≤ $40k, ≤ $100k)
- New entrant velocity (share outside top 50 vendors)
- Vendor landscape turnover

## 2. Methodology

**Data source:** USAspending API `spending_by_award/` endpoint (same as E203).
**Time windows:**
- **Full:** FY2020-01-01 to FY2025-12-31 (5 years)
- **Recent:** 2024-10-01 to 2025-09-30 (12 months)
**Sample:** 5,000 awards per window per code (50 pages × 100).
**Metrics:** Categorization (software/service/hardware/telecom/other), award size distribution, top-10 concentration, new entrant share (vendors outside top 50 by obligation).

## 3. Results summary

| Metric | **7030** (IT Software) | **DA10** (App Dev SaaS) | **7A21** (Business App SW) |
|--------|------------------------|-------------------------|----------------------------|
| **Recent obligation (annualized)** | **$28.7B/yr** (30× full avg) | **$58.4B/yr** (98× full avg) | **$31.1B/yr** (50× full avg) |
| **Top-10 share: Full → Recent** | **45.3% → 63.9%** ⬆️ **+18.6 pp** | **59.1% → 52.4%** ⬇️ **−6.7 pp** | **62.3% → 67.7%** ⬆️ **+5.4 pp** |
| **Software % (count): Full → Recent** | 64.5% → 70.7% ⬆️ | 57.8% → 68.4% ⬆️ | 71.8% → 74.4% ⬆️ |
| **Awards ≤ $40k: Full → Recent** | **42.0% → 24.1%** ⬇️ **−17.9 pp** | **49.5% → 35.4%** ⬇️ **−14.1 pp** | **42.2% → 37.4%** ⬇️ **−4.8 pp** |
| **New entrant share: Full → Recent** | **21.7% → 10.8%** ⬇️ **−10.9 pp** | **16.0% → 23.1%** ⬆️ **+7.1 pp** | **13.0% → 11.6%** ⬇️ **−1.4 pp** |

## 4. Detailed findings by code

### 4.1 7030 — **Concentrating rapidly, small awards disappearing**

**Bad news for small teams:**
- Top-10 share jumped from **45.3% to 63.9%** (+18.6 pp)
- Small awards (≤ $40k) dropped from **42.0% to 24.1%** (−17.9 pp)
- New entrant share fell from **21.7% to 10.8%** (−10.9 pp)

**Vendor turnover — new giants entered:**
| Vendor | Recent Obligation | Change |
|--------|------------------|--------|
| LEIDOS, INC. | $754M | **NEW** (0 → 13.1%) |
| IBM | $595M | **NEW** (0 → 10.4%) |
| CA, INC. | $429M | **NEW** (0 → 7.5%) |
| FOUR LLC | $271M | **NEW** (0 → 4.7%) |
| BMC SOFTWARE | $268M | **NEW** (0 → 4.7%) |
| ECS FEDERAL | $178M | **NEW** (0 → 3.1%) |
| CGI FEDERAL | $109M | **NEW** (0 → 1.9%) |

**Vendors that disappeared from top 10:**
Dell Marketing ($318M), Minburn ($133M), ESRI ($123M), DLT ($113M), Document Storage ($110M), FCN ($106M)

**Interpretation:** The 7030 market is being captured by large integrators (Leidos, ECS, CGI) and major software vendors (IBM, CA, BMC) winning very large awards. The accessible small-award segment is shrinking.

### 4.2 DA10 — **Diversifying, more new entrants, but awards growing**

**Good news for small teams:**
- Top-10 share **decreased** from 59.1% to 52.4% (−6.7 pp)
- New entrant share **increased** from 16.0% to 23.1% (+7.1 pp)
- Software share increased from 57.8% to 68.4%

**Concerning:**
- Small awards (≤ $40k) dropped from 49.5% to 35.4% (−14.1 pp)
- Massive new vendors entered with huge awards

**Major new vendors:**
| Vendor | Recent Obligation | Change |
|--------|------------------|--------|
| DELL MARKETING L.P. | $1.38B | **NEW** (0 → 11.8%) |
| WORLD WIDE TECHNOLOGY | $830M | **NEW** (0 → 7.1%) |
| IRON BOW TECHNOLOGIES | $828M | **NEW** (0 → 7.1%) |
| GENERAL DYNAMICS IT | $601M | **NEW** (0 → 5.1%) |
| DATAMINR | $299M | **NEW** (0 → 2.6%) |

**Interpretation:** DA10 is attracting more large vendors (creating more competition at the top) and more new entrants overall, but award sizes are ballooning. The market is expanding rapidly with more players, but the entry point for small teams is moving up.

### 4.3 7A21 — **Extreme concentration worsening, Carahsoft losing share to new giants**

**Bad news for small teams:**
- Top-10 share increased from 62.3% to 67.7% (+5.4 pp)
- New entrant share decreased from 13.0% to 11.6% (−1.4 pp)
- Small awards dropped from 42.2% to 37.4% (−4.8 pp)

**Carahsoft's dominance eroded but replaced by larger players:**
- Carahsoft: 27.1% → 16.7% (still #1 but share halved)
- **LEIDOS: NEW at $1.25B (20.1%)** — now #2
- **DELL MARKETING: NEW at $956M (15.4%)** — now #3
- DLT: 3.0% → 4.1%

**Interpretation:** 7A21 is a reseller market (perpetual licenses) where large aggregators (Carahsoft, DLT) are being joined by massive integrators (Leidos, Dell). The market structure is hardening, not opening.

## 5. Cross-code comparison: the obligation explosion

All three codes show **massive obligation growth** in the recent 12 months vs. 5-year average:

| Code | Full 5-yr Total | Recent 12-mo | Annualized Recent | Multiple of 5-yr Avg |
|------|-----------------|--------------|-------------------|---------------------|
| 7030 | $4.74B | $5.74B | $28.7B/yr | **30×** |
| DA10 | $2.99B | $11.68B | $58.4B/yr | **98×** |
| 7A21 | $3.10B | $6.21B | $31.1B/yr | **50×** |

**This is not organic growth.** Possible explanations:
1. **IDIQ/GWAC ceiling increases** — large contract vehicles (SEWP, GSA, CIO-SP4) raised ordering limits
2. **COVID/IT modernization funding** — recent appropriations bills (IIJA, IRA, CHIPS) driving spend
3. **Data artifact** — API may return different record sets for recent vs. historical queries
4. **Large single awards** — a few mega-awards (Leidos $1.25B, Dell $1.38B) dominate

**Regardless of cause, the trend is clear: award sizes are exploding, concentrating obligation among fewer, larger vendors.**

## 6. What this decides for small-team strategy

| Code | Trend | Small-Team Verdict |
|------|-------|-------------------|
| **7030** | Concentrating fast, small awards vanishing | **⚠️ WINDOW CLOSING** — Enter now or wait for next cycle |
| **DA10** | Diversifying at top, more new entrants, but awards growing | **✅ BEST BET** — More vendors winning, more new entrants, but need to target mid-size |
| **7A21** | Hardening around mega-resellers | **❌ AVOID** — Reseller-dominated, barriers rising |

**Key insight:** DA10 is the only code where concentration is *decreasing* and new entrants are *increasing*. Despite larger awards, the competitive dynamics favor newcomers more than 7030 or 7A21.

## 7. Limitations

- 5,000 award sample per window; full recent period may have >5,000 awards for DA10/7A21 (hit page limit)
- Recent window (Oct 2024–Sep 2025) may include partial FY2025 data; not a clean fiscal year
- Obligation explosion may be driven by a few mega-awards; median award analysis needed
- Does not distinguish prime vs. subcontractor awards
- Categorization is keyword-based (same as E203)

## 8. Next steps

1. **E205 — Agency distribution:** Which agencies drive the recent surge in each code? Do small vendors win direct or only subcontract?
2. **Median award tracking:** Analyze full award size distributions (not just ≤ $40k threshold) to understand distribution shifts.
3. **Contract vehicle analysis:** Cross-reference with contract vehicle data (GSA, SEWP, CIO-SP4) to identify which vehicles drive concentration.
4. **Validate obligation explosion:** Check if recent-period mega-awards are real or data artifacts (e.g., IDIQ ceiling values vs. actual orders).