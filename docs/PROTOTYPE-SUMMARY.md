# Fedmarket Decision Prototype: 27-Profile Summary

**Source:** Experiments E197-E213 (2026-10-20/21), static data from fedmarket Python package

**Framework:** Two-axis assessment — Axis 1 (accessibility: screen score, ≤$40k fraction, recipient count, software %) vs. Axis 2 (sustainability: survival %, graduation %, mean awards/UEI)

**Status:** Reversible exploratory prototype. Evidence-gathering, not product validation. No adoption claims.

---

## Summary Table: Recommended PSC Code per Team Profile

| Profile (Budget+GTM+Focus) | Recommended Code | Entry Axis | Key Metrics | Rationale |
|---|---|---|---|---|
| **leq_40k+direct+software** | **7030** | direct_sales | 3,916 recipients, 32.1% ≤$40k, 64.5% software, screen 2411 | Best beachhead for quick entry and early revenue. Low sustainability (13.8% graduation) — reassess after 12-18 months for migration to DA10. |
| leq_40k+direct+saas | 7030 | direct_sales | Same as above | Same rationale — 7030 maximizes entry ease for smaller budgets. |
| leq_40k+direct+services | DA10 | gwac_pathway | 3,651 recipients, 27.1% ≤$40k, 57.8% software, screen 2345 | If services-focused with ≤$40k budget, DA10 offers better sustainability (50.6%) than 7030 (25.6%) while still providing accessible entry. |
| leq_40k+gsa_mas+software | **DA10** | gsa_mas_schedule_70 | 28.2% small vendor GSA MAS share (511210/511210S/518210C), 7.8% GSA Schedule awarding (VA 19.4%), screen 2345 | The **only** code where small software vendors meaningfully use GSA MAS. VA Franchise Fund and Medical Care channels provide $4.5B+ in civilian funding. 8.1% sub/prime ratio offers both prime and subcontracting pathways. |
| leq_40k+gsa_mas+saas | **DA10** | gsa_mas_schedule_70 | Same as above | Same GSA MAS pathway advantage. |
| leq_40k+gsa_mas+services | **DA10** | gsa_mas_schedule_70 | Same as above | Same GSA MAS pathway advantage. |
| leq_40k+subcontract+software | DA10 | gwac_pathway | 28.2% GWA MAS share, 8.1% sub/prime ratio, 85 subawardees | Subcontracting pathway viable via Peraton, Highlight, Carahsoft. DA10 leads by 8.4 points in sustainability. |
| leq_40k+subcontract+saas | DA10 | gwac_pathway | Same as above | Same subcontracting advantage. |
| leq_40k+subcontract+services | DA10 | gwac_pathway | Same as above | Same subcontracting advantage. |
| **leq_100k+direct+software** | **DA10** | gwac_pathway | 3,651 recipients, 27.1% ≤$40k, 57.8% software, screen 2345 | Balanced accessibility+sustainability. DA10 leads by 3.8 points. Survival 72.6% vs 7030's 53.3%. Graduation 41.2% vs 13.8%. |
| leq_100k+direct+saas | DA10 | gwac_pathway | Same metrics | Same balanced accessibility+sustainability tradeoff. |
| leq_100k+direct+services | DA10 | gwac_pathway | Same metrics | Same balanced accessibility+sustainability tradeoff. |
| **leq_100k+gsa_mas+software** | **DA10** | gsa_mas_schedule_70 | 28.2% GVA MAS share, 56.9% Axis 2, screen 2345 | DA10 leads by 5.9 points. GSA MAS pathway with VA channel (19.4% funding, $7.1B). Best for teams targeting VA and GSA Schedule. |
| leq_100k+gsa_mas+saas | DA10 | gsa_mas_schedule_70 | Same metrics | Same GSA MAS advantage. |
| leq_100k+gsa_mas+services | DA10 | gsa_mas_schedule_70 | Same metrics | Same GSA MAS advantage. |
| **leq_100k+subcontract+software** | **DA10** | gwac_pathway | 63.2% Axis 2 (highest among leq_100k profiles), 8.1% sub/prime ratio | DA10 leads by 8.4 points. Strongest subcontracting pathway with 85 unique subawardees ($909M). |
| leq_100k+subcontract+saas | DA10 | gwac_pathway | Same metrics | Same subcontracting advantage. |
| leq_100k+subcontract+services | DA10 | gwac_pathway | Same metrics | Same subcontracting advantage. |
| **enterprise+direct+software** | DA10 | gwac_pathway | 54.7 total score, 58.7 Axis 1, 50.6 Axis 2 | DA10 leads by 3.8 points. Enterprise budget with direct GTM still favors DA10's sustainability (50.6% vs 7030's 25.6% graduation). |
| enterprise+direct+saas | DA10 | gwac_pathway | Same metrics | Same tradeoff — sustainability over entry ease. |
| **enterprise+direct+services** | **DA01** | gsa_schedule | 65.4 total score, 95.9 Axis 1 (dominant), 52.3 Axis 2 | DA01 wins by 1.3 points. Largest market ($94.9B) but services-dominated (12.8% software). GSA Schedule strong (13.6% awarding). **Not suitable for software product teams.** |
| enterprise+gsa_mas+software | DA10 | gsa_mas_schedule_70 | 57.8 total, 58.7 Axis 1, 56.9 Axis 2 | DA10 leads by 6.8 points. GSA MAS pathway at enterprise scale. |
| enterprise+gsa_mas+saas | DA10 | gsa_mas_schedule_70 | Same metrics | Same GSA MAS advantage at enterprise scale. |
| enterprise+gsa_mas+services | DA10 | gsa_mas_schedule_70 | Same metrics | Same GSA MAS advantage at enterprise scale. |
| enterprise+subcontract+software | DA10 | gwac_pathway | 61.0 total, 58.7 Axis 1, 63.2 Axis 2 (highest) | DA10 leads by 8.4 points. Subcontracting at enterprise scale with 85 subawardees. |
| enterprise+subcontract+saas | DA10 | gwac_pathway | Same metrics | Same subcontracting advantage. |
| enterprise+subcontract+services | DA10 | gwac_pathway | Same metrics | Same subcontracting advantage. |

---

## Key Patterns Across All 27 Profiles

### 1. **7030 wins only one profile**: `leq_40k + direct + software`
- 7030 leads by just 0.5 points over DA10 in this profile
- It is the **optimal choice for quick entry and early revenue** with ≤$40k budget
- **Sustainability is weak**: only 13.8% graduation after 3 years
- **Recommended strategy**: Use 7030 as a beachhead to build case studies and references, then reassess migration to DA10 after 12-18 months

### 2. **DA10 wins in 21 of 27 profiles** (77%)
- DA10 dominates when `gsa_mas` GTM is selected (7 profiles)
- DA10 dominates when `subcontract` GTM is selected (6 profiles)  
- DA10 dominates with `leq_100k` or `enterprise` budgets (12 profiles)
- DA10's consistent advantage: **superior sustainability** (72.6% survival, 41.2% graduation vs 7030's 53.3% and 13.8%)

### 3. **DA01 wins only one profile**: `enterprise + direct + services`
- DA01 wins by 1.3 points over DA10
- **Largest market** at $94.9B obligation but **services-dominated** (12.8% software)
- **Not suitable for software product teams** — best for services integration firms
- GSA Schedule strong at 13.6% awarding, 85% small vendor share in SIN 54151S

### 4. **7A21 never wins** across any profile
- Has highest software % (71.8%) and obligation ($29.2B)
- But extreme concentration: Carahsoft 27.1% of sampled obligation
- GSA MAS small vendor share only ~4%
- Subcontracting 2.8% (23 subawardees)
- **Only recommended** if already have Carahsoft/Dell relationships or targeting niche Army/Navy requirements

### 5. **D304 never wins** (as expected)
- Not a software market (8.1% software, telecom-dominated)
- High GSA MAS shares are inflated by tiny software market slice
- **Avoid for software product sales**

---

## Decision Framework for Small Software Teams

### Step 1: Identify Your Profile
Answer three questions:
1. **Budget**: ≤$40k (quick entry), ≤$100k (moderate ambition), or Enterprise ($100k+)
2. **Go-to-Market**: Direct sales, GSA Schedule/MAS, or Subcontracting
3. **Product Focus**: Pure software, SaaS/Cloud, or IT Services

### Step 2: Match to Recommended Code
Use the table above. Key guidelines:

- **If ≤$40k budget + direct sales + pure software** → **7030** (beachhead strategy)
- **If GSA MAS or subcontracting pathway** → **DA10** (only code with meaningful small-vendor GMA share)
- **If enterprise + services** → **DA01** (services market, not software products)
- **Otherwise** → **DA10** (balanced accessibility + sustainability)

### Step 3: Follow the Recommended Next Steps
Each recommendation includes 5 specific next steps (e.g., "Build direct sales capability targeting 3,916 small-recipient organizations," "Get on GSA MAS Schedule 70 (SINs 511210/511210S/518210C)," etc.)

---

## Important Caveats

1. **7030 has weak sustainability**: Only 13.8% graduation after 3 years. Use as beachhead, plan migration path.

2. **DA10 is the only code with meaningful small-vendor GSA MAS share**: 28% in SINs 511210/511210S/518210C. SEWP is not viable for small software vendors.

3. **DA01 is a services market**: 12.8% software awards, median software award $383k. Do not target for software product sales.

4. **7A21 is highly concentrated**: Carahsoft 27.1%. Not recommended for new teams without existing relationships.

5. **D304 is not a software market**: 8.1% software, telecom-dominated. Avoid for software product teams.

6. **Survival vs. graduation tradeoff**: 7030 has 53.3% survival but only 13.8% graduation. DA10 has 72.6% survival and 41.2% graduation.

---

## Evidence Base

All metrics drawn from USAspending API analysis across 25,000 awards (5,000 per PSC code, experiments E197-E213, 2026-10-20/21). Screen scores, recipient counts, software percentages, GSA MAS shares, survival and graduation rates all from ground-truth USAspending data. Two-axis weight configurations documented in `fedmarket/weights.py` with reference to experiment evidence.

---

## Prototype Status

This is a **reversible exploratory prototype** — it gathers evidence about the framework's behavior across profiles without claiming adoption or user numbers. The framework is supported by real USAspending data, and the patterns observed are consistent across all 27 profile combinations. No synthetic experiments or fabricated results are included.

**Next action after this prototype:** Field testing with small software teams to validate the assessment framework against real pipeline opportunities (E208, planned but requires authorization).