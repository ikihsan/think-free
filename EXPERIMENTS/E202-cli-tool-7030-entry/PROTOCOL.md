<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 PROTOCOL — CLI tool for PSC code small-team entry analysis

**Purpose:** Provide a minimal command-line tool that queries the USAspending API and outputs key small-team entry metrics for a given PSC code, enabling small teams to assess whether a federal code admits programs a small team could build and sell.

**Screen methodology (from E199):** Score = recipient_count × (1 − top10_share), balancing market size against concentration.

**Tool functionality:**

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

4. **Kill gate:** N/A — this is a prototype tool, not a gate-validated experiment.

5. **Data integrity:** Each response body is saved with its sha256 hash and request payload metadata, so a later reader can distinguish API changes from parse defects.

**Expected output format:**
```
=== 7030 Information technology software ===
PSC Code: 7030
Time period: FY2020–FY2025

=== Screen Metrics ===
Distinct recipients: 3,916
Top-10 share: 38.4% (declared baseline: 38.4%)
Screen score: 2,411.1 (declared baseline: 2,412)

=== Small-Team Entry ===
Recipients with obligation ≤ $40k: 1,257 (32.1%)
Recipients with obligation ≤ $100k: 1,834 (46.8%)
Recipients with exactly 1 award: 3,916 (100.0%)

=== Accessibility ===
~62% of total obligation potentially accessible to newcomers
(top 10 hold 38.3%, leaving 61.7% available)

Score = 3,916 × (1 − 0.384) = 2,411.1
```

**Prototype data (from E201 exploration of 7030):**
- 3,916 unique recipients from 3,917 total award rows
- Top-10 share: 38.4% (exactly matches E198 declaration)
- Recipients ≤ $40k: 1,257 (32.1%)
- Recipients ≤ $100k: 1,834 (46.8%)
- 100.0% recipients with exactly 1 award
- Total obligation: $25,830,343,900 (matches E196 cell total $25.83B)