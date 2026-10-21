<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E199 RESULT — candidate screen on the money axis: which PSC code admits a small program?

**Date:** 2026-10-20. **Outcome: SCREEN COMPLETED.**

## 1. The screen question

> **Which of the five IT/software PSC codes (DA01, DA10, 7A21, 7030, D304) admits a program that a small team could build and sell?**

The money axis now has four confirmed coordinates (E198):
1. **Buyer** — US federal agencies
2. **Unit** — 98,640 funded awards ≤ $100k in five codes
3. **Budget** — $203.32B across those cells
4. **Vendor** — 9,977 distinct companies, top 10 per code hold 34.5%–57.6%

The named next action from E198 was: *a candidate screen on the money axis. The screen asks: which of these five codes, or which sub-segment within them, admits a program that a small team could build and sell?*

## 2. Screen methodology

I scored each PSC code on two dimensions relevant to small-team entry:

| Code | Distinct Recipients | Top-10 Share | Score = recipients × (1 − top10_share) |
|---|---|---|---|
| **7030** | 3,917 | 38.4% | **2,412** |
| **DA01** | 3,610 | 34.5% | **2,363** |
| **DA10** | 3,651 | 35.8% | **2,345** |
| **7A21** | 3,977 | 48.9% | 2,034 |
| **D304** | 1,155 | 57.6% | 490 |

**Scoring logic:** `recipient_count × (1 − top10_share)` higher = better for small teams. This balances:
- More recipients → more entry points / larger addressable market
- Lower top-10 share → less concentration = easier for a newcomer to break in

## 3. Results and ranking

1. **7030** (Information technology software) — highest score. 3,917 distinct recipients, top 10 hold 38.4% of obligation. The code's moderate concentration and large recipient base make it the most accessible for a small team entering the federal software market.

2. **DA01** (IT & Telecom — app development support, labour) — very close second. 3,610 recipients, top 10 hold 34.5%. Also has the largest cell budget at $94.91B, offering the most total market volume among the concentrated codes.

3. **DA10** (IT & Telecom — app development, SaaS) — third place. 3,651 recipients, top 10 hold 35.8%. Cell budget $33.01B.

4. **7A21** (IT & Telecom — business application software, perpetual licence) — fourth. Highest recipient count (3,977) but significantly higher concentration (48.9% top 10) reduces small-team accessibility despite the large pool.

5. **D304** (IT & Telecom — telecommunications and transmission) — far behind. Only 1,155 recipients and the highest concentration (57.6% top 10). While the cell budget is $20.37B, the market is too concentrated for a small independent program to realistically enter.

## 4. What this decides

**7030 is the best PSC code for a small team to target** for building and selling software into the federal marketplace. It offers the best balance of:
- Large addressable recipient base (3,917 distinct companies)
- Moderate concentration (top 10 hold 38.4%, leaving 61.6% of $25.83B = ~$15.9B available to newcomers)
- Significant total market size ($25.83B cell obligation)

DA01 is a close alternative if the team wants the largest total market ($94.91B) and can tolerate slightly higher concentration challenges.

**D304 should be deprioritized** — its high concentration (57.6% top 10) means the market is effectively controlled by a small number of primes, making it very difficult for a small team to win direct awards.

**7A21** has the most recipients but the highest concentration, making it a trade-off: more potential entrants but each faces a more crowded top tier.

## 5. Limitations and next steps

- This screen uses **vendor concentration** (top-10 share from recipient data) as the primary accessibility metric. It does not account for:
  - The average award size per recipient (some codes may have many small awards others have fewer large ones)
  - The specific type of software needed (each code procures different kinds of IT services)
  - Geographic or agency distribution effects
- A full **program-level study** would require querying individual award descriptions to assess fit, which is the next experimental step if a candidate wants to validate this screen with real contract data.

**Named continuation:** build a prototype that queries `spending_by_category/recipient/` for the top-ranked code (7030) and analyzes award amounts and descriptions to verify that the screen's prediction of small-team accessibility holds at the individual award level.