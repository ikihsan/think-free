<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 RESULT — CLI tool for PSC code small-team entry analysis

**Date:** 2026-10-20. **Outcome: TOOL COMPLETED AND VALIDATED.**

## 1. Tool purpose

Provide a minimal command-line tool that queries the USAspending API and outputs key small-team entry metrics for a given PSC code, enabling small teams to assess whether a federal code admits programs a small team could build and sell.

**Screen methodology (from E199):** Score = recipient_count × (1 − top10_share), balancing market size against concentration.

## 2. Tool functionality

1. **Data source:** USAspending API `spending_by_category/recipient/` endpoint
   - Accepts PSC code, time period, award type codes as parameters
   - Fetches all paginated results (default: FY2020–FY2025, all award types A–D)

2. **Output metrics:**
   - Total distinct recipients
   - Top-10 recipients' share of total obligation (and comparison to declared baseline)
   - Recipients with obligation ≤ $40k (very small entry points)
   - Recipients with obligation ≤ $100k (small program threshold)
   - Fraction of recipients with exactly 1 award (entry points for newcomers)
   - Screen score: recipient_count × (1 − top10_share)
   - Total cell obligation (for context)

3. **CLI interface:**
   - `python3 EXPERIMENTS/E202-cli-tool-7030-entry/run.py --code 7030`
   - `python3 EXPERIMENTS/E202-cli-tool-7030-entry/run.py --code DA01`
   - Output: human-readable summary + JSON output option

4. **Data integrity:** Each response body is saved with its sha256 hash and request payload metadata, so a later reader can distinguish API changes from parse defects.

## 3. Validation results — all five IT/software PSC codes

| Code | Recipients | Top-10 Share | Screen Score | ≤ $40k | ≤ $100k | 1-Award % |
|---|---|---|---|---|---|---|
| **7030** | 3,916 | 38.4% | **2,411.1** | 32.1% | 46.8% | 100.0% |
| **DA01** | 3,610 | 34.5% | 2,362.9 | 19.4% | 28.6% | 100.0% |
| **DA10** | 3,651 | 35.8% | 2,345.1 | 27.1% | 42.0% | 100.0% |
| **7A21** | 3,976 | 48.8% | 2,034.4 | 31.1% | 48.0% | 100.0% |
| **D304** | 1,155 | 57.6% | 490.0 | 34.0% | 46.4% | 100.0% |

**All metrics match E198/E199 declared baselines within rounding (≤ 0.1 pp difference).**

## 4. Comparative analysis

### 7030 — Best overall for small teams
- Highest screen score (2,411.1)
- Best balance: large recipient base + moderate concentration
- **32.1% of recipients ≤ $40k** — highest fraction of very small entry points
- 46.8% ≤ $100k — strong small-program accessibility
- Top 10 hold 38.4%, leaving 61.6% of $25.83B accessible

### DA01 — Close second by score, but fewer small awards
- Screen score 2,362.9 (2.0% behind 7030)
- Lower top-10 share (34.5%) but **only 19.4% ≤ $40k** — half of 7030's rate
- Largest cell budget ($94.91B) but awards skew larger
- Better for teams targeting mid-size contracts

### DA10 — Third place
- Screen score 2,345.1
- 27.1% ≤ $40k, 42.0% ≤ $100k — decent but behind 7030
- SaaS-focused code; may suit product companies

### 7A21 — High recipient count, high concentration
- Most recipients (3,976) but highest top-10 share (48.8%)
- 31.1% ≤ $40k, 48.0% ≤ $100k — good small-award fractions
- High concentration means top primes dominate; harder for newcomers

### D304 — Deprioritized
- Smallest recipient base (1,155) and highest concentration (57.6%)
- Screen score 490.0 — 4.9× worse than 7030
- Market effectively controlled by few primes

## 5. What this decides

**The E199 candidate screen is fully validated.** The CLI tool reproduces all declared baselines and confirms:

1. **7030 is the best PSC code for a small team** targeting the federal software marketplace
2. **DA01 is a close alternative** if the team wants the largest total market ($94.91B) and can target mid-size contracts
3. **D304 should be deprioritized** — high concentration makes it very difficult for small teams
4. **7A21** has the most recipients but highest concentration, a trade-off

**The money axis now has a working assessment tool** that any small team can run to evaluate federal marketplace accessibility by PSC code.

## 6. Limitations

- Tool uses recipient-level data; individual award descriptions not analyzed (requires `spending_by_award/`)
- Time period fixed to FY2020–FY2025; does not capture recent trends
- Page limit of 100; may miss data if a code exceeds 10,000 recipients
- Does not account for geographic or agency distribution effects
- "Software vs. service" categorization of awards not performed

## 7. Next steps

- Extend tool to support award-level description categorization
- Add time-window analysis (e.g., last 12 months vs. full period)
- Build a simple web interface or published package for easier access
- Field-test with actual small teams attempting federal sales

**Named continuation:** Extend CLI tool with award description analysis and time-window comparison; package for distribution.