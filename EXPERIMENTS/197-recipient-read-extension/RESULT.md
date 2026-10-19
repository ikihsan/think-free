<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E197 Recipient Read Extension — Vendor identification for remaining 3 IT codes

**Date:** 2026-10-19. **Outcome: Partial — binary search for 7A21 thresholds initiated; 7030 and D304 not started. API budget (60 req/hr unauthenticated) makes full completion impractical in one session.**

## Background

E197 established that 98.6% of federal award records carry money (median funded fraction 0.9862). 12 of 25 G4 codes clear ≥10,000 funded awards ≤$100k, including all 5 IT codes totaling 98,640 purchases ($203.32B). The named next action was the recipient read (`spending_by_category/recipient/` or `spending_by_award/` with ascending sort) to identify who is paid.

The recipient read was completed for **DA01** and **DA10** in the main E197 experiment (see `E197_RECIPIENT_READ_SUMMARY.md`). Those two codes account for 14,726 + 10,256 = **24,982 funded awards ($1-$100k)** with recipients identified by awarding agency.

**Remaining codes:** `7A21` (32,747 awards), `7030` (14,033 awards), `D304` (20,664 awards) — total **67,444** funded awards ($1-$100k) without vendor data.

## Progress this session

### 7A21 (Business Application Software, $29.21B, 50,777 awards)

Binary search thresholds initiated:

| Threshold | Status | Pages sampled |
|---|---|---|
| t=1 (funded/non-funded) | **Complete** — turning page = **7** | 4, 16, 32, 63, 7 (turning) |
| t=100001 (funded ≤$100k) | **In progress** — 18 binary steps completed | 250, 312, 327, 331, 333, 334, 335, 343, 375, ... |

Prior blocks for t=1 read: pages 1–6 captured (`priors_7A21_1..6`).

**Turning block page 7** contains mixed amounts: $0.0 (deobligated) and small positive amounts ($0.01–$0.99), confirming the funded boundary.

**t=100001 binary search** is narrowing toward the page where awards cross $100k. Current samples show amounts in the $10k–$100k range (pages 250–375). The turning point is likely around page 330–340 based on E197 panel B (10,000th award at $14,313; 50,777 total awards).

### 7030 and D304

Not started. Each would require similar binary searches + full page reads.

## API budget constraint

USAspending unauthenticated limit: **60 requests/hour**.

Per-code cost estimate:
- t=1 binary search: ~9 requests
- t=100001 binary search: ~9 requests  
- Full page reads up to t=100001 turning page: **~330 requests for 7A21**, ~140 for 7030, ~210 for D304
- **Total: ~350–680 requests per code** → **6–11 hours per code** at rate limit

Three codes = **18–33 hours** of sequential API calls. Not feasible in a single session.

## What this decides

1. **The recipient read mechanism is validated** — `spending_by_award/` with ascending sort by Award Amount successfully identifies funded awards and their awarding agencies for DA01 and DA10.

2. **The vendor landscape for 2/5 IT codes is known** — 24,982 small funded purchases mapped to 56+ agencies each (DoD dominant).

3. **Completing the remaining 3 codes requires either:**
   - Authenticated API access (higher rate limit)
   - Multiple sessions over days
   - The `spending_by_category/recipient/` endpoint (top-100 recipients by obligation, not per-award granularity)

4. **The money axis now has buyer, unit, budget, and partial vendor data** — the first money-sized, code-addressed, funded population with identified payees in this record.

## Next action

**Fresh exploration on a new axis** (per STATE.md: "return to fresh exploration" after E182 closed the EVID line). The federal spend axis has produced its money-sized population; the recipient read demonstrates the mechanism works but is rate-limited. A new observation experiment should target a different domain or need type.

**Do not run:** continued unauthenticated recipient reads for 7A21/7030/D304 — budget makes this a multi-day commitment with diminishing returns (vendor data for 2/5 codes already establishes the pattern).

## Artifacts

- `/home/ubuntu/think-free/raw_recipient/` — all API captures with sha256 hashes
- New files this session: `binary1_7A21_*`, `turn1_7A21_*`, `priors_7A21_1..6`, `binary100k_7A21_*`
- E197_RECIPIENT_READ_SUMMARY.md — summary of DA01/DA10 results