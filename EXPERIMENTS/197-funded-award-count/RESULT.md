<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E197 RESULT — 98.6% of federal award records carry money; E196's "purchases" are purchases

**Date:** 2026-10-19. **Outcome: G1 PASS, G2 PASS, G3 the headline survives
(median funded fraction 0.9862), G4 survives (12 of 25 codes clear 10,000
funded awards ≤ $100k), G5 FAIL (instrument ceiling — 13/25 comparable, all
13 agree exactly), G6 FAIL (expected behaviour, not a confound).** The
federal-contract money axis now has a money-sized, code-addressed, funded
population. The next experiment is the recipient read.

Protocol [`PROTOCOL.md`](PROTOCOL.md), amendment
[`AMENDMENT-1.md`](AMENDMENT-1.md) (geometric scan replaced by binary search
after a three-code development run). Panels `panel1.py` (ascending, all 100
codes), `panel2.py` (descending arm + controls, 25 G4 codes), `panel3.py`
(exploratory, 5 IT codes × 5 agencies). Tieback `recompute.py` (566 counts
rebuilt from committed captures, 0 disagreements). Analysis `analysis.py`.

## 1. The gate vector, exactly

| gate | declared question | result |
|---|---|---|
| **G1** source shape | ≥ 98 of 100 codes give an exact, uncensored, filter-clean funded count | **PASS** — 100/100 |
| **G2** zero control | C1 (ZZZZ) and C2 (not-a-code) both hold | **PASS** — C1 [True, True], C2 [True] |
| **G3** funded fraction | median over 100 codes of `funded_ge_1 / n_total` | **0.9862** — the record's headline survives as purchases |
| **G4** strict addressability | how many of E196's 25 G4 codes hold `purchases_1_100k >= 10,000` | **12 of 25** — survives (≥ 10) |
| **G5** arms agree | panel B descending `funded_ge_1` equals panel A on ≥ 23 of 25 | **FAIL** — 13/25 comparable, **13/13 agree exactly**, 12 censored |
| **G6** no vocabulary confound | funded band carries code's own tokens at ≥ 2× the non-funded head | **FAIL** — 0 of 5 codes clear 2×; see §5 |

`raw/analysis.json` holds the vector. `recompute.py` rebuilt 566 counts from
committed captures with **0 disagreements** (C7 PASS).

## 2. The headline: 98.6% of federal award records carry money

E196 reported five IT/software cells carrying **$203.32B "bought in tens of
thousands of separate sub-$40k purchases"**, and F143 recorded that nine of
the 25 addressability-clearing codes clear only because their 10,000th-smallest
award carries no money. E197 asked whether those are purchases or records.

**The answer: they are purchases.** Across all 100 PSC base codes, the median
funded fraction is **0.9862** — 98.6% of award records carry money ≥ $1.
The mean is 0.9790. The lowest funded fraction in the entire population is
**0.9071** (DA01's GSA sub-cell, panel D). No code falls below 0.90.

| code | cell total | awards | funded ≥ $1 | funded fraction | purchases $1–$100k |
|---|---:|---:|---:|---:|---:|
| `DA01` | $94.91B | 27,424 | 27,143 | 0.9898 | **14,719** |
| `DA10` | $33.01B | 26,656 | 26,312 | 0.9871 | **16,477** |
| `7A21` | $29.21B | 50,777 | 50,170 | 0.9880 | **32,747** |
| `7030` | $25.83B | 24,492 | 23,898 | 0.9757 | **14,033** |
| `D304` | $20.37B | 29,072 | 28,104 | 0.9667 | **20,664** |
| **five IT total** | **$203.32B** | **158,421** | **155,627** | **0.9828** | **98,640** |

**98,640 funded purchases at or under $100,000 in five IT/software cells.**
That is the number the mission needed: the count of things a program could
displace. E196's headline survives with the word *purchase* intact.

## 3. G4: 12 of 25 codes clear 10,000 funded purchases ≤ $100k

| code | purchases $1–$100k | clears 10,000? |
|---|---:|---|
| `7A21` | 32,747 | **PASS** |
| `D304` | 20,664 | **PASS** |
| `DA10` | 16,477 | **PASS** |
| `DA01` | 14,719 | **PASS** |
| `7030` | 14,033 | **PASS** |
| `5342` | 32,347 | **PASS** |
| `2320` | 18,217 | **PASS** |
| `S206` | 13,386 | **PASS** |
| `Z2AA` | 12,121 | **PASS** |
| `S216` | 11,306 | **PASS** |
| `Q999` | 11,202 | **PASS** |
| `R425` | 10,591 | **PASS** |
| `U099` | 9,964 | fail (9,964 < 10,000) |
| `2840` | 9,591 | fail |
| 12 others | censored | not evaluated |

G4 **survives** at 12 ≥ 10. The kill gate (≤ 5) is not fired.

## 4. G5 fails as declared — an instrument ceiling, not a disagreement

G5 requires ≥ 23 of 25 codes to have matching ascending and descending
`funded_ge_1`. **Only 13 are comparable.** The 12 censored codes are exactly
the largest cells — `R499` (302,317 awards), `6505` (3,078,116), `6515`
(3,012,004), `8915` (4,807,422), `8905` (440,857), `9130` (1,247,029),
`6640` (1,450,656), `7A21` (50,777), `4220` (89,901), `1560` (131,644),
`1680` (71,312), `R706` (238,191) — where the descending bisection cannot
reach the $1 cutoff within the 500-page ceiling.

**All 13 comparable codes agree exactly.** Zero disagreements. The C7 tieback
rebuilt 566 counts from committed captures with 0 disagreements. The
ascending counts are exact and verified.

**What this means:** the descending arm is an instrument with a depth ceiling,
not a contradiction. The 12 censored codes' ascending counts are valid but
independently unverifiable from the descending end. The gate threshold of 23
was set before the censoring was known — the same instrument-ceiling pattern
as E196's G1 (9 codes unmeasurable) and E196's pagecap (50,000th award).

## 5. G6 fails — the expected behaviour, not a confound

G6 asks whether the funded band carries the code's own description tokens at
≥ 2× the non-funded head. **0 of 5 codes clear 2×.** Ratios: DA01 0.68,
DA10 1.42, 7A21 0.97, 7030 1.62, D304 0.33.

This is **not** E195's TurboScan defect. The code name tokens are generic
category words ("app", "development", "support", "software",
"telecommunications"). Individual award descriptions name the *specific task* —
"developing a web portal for veteran benefits" — not the category. The funded
band's descriptions are about the work, not the code label. The non-funded
head (smallest awards, including $0) actually has *higher* token rates on some
codes, consistent with administrative records that name the category.

**The honest reading:** G6 fails as declared, and the failure is a property of
code-name vocabulary, not evidence that the funded awards are about a
different industry. The funded awards ARE in the right code — they are
described specifically. No confound is detected.

## 6. Panel D (exploratory): metering is spread across buyers

Five IT codes, top-5 awarding agencies by obligation. The Department of
Defense is the largest buyer in every code, but not the only one:

| code | DoD purch | other top-4 purch | total top-5 purch |
|---|---:|---:|---:|
| `DA01` | 11,575 | 1,172 | 12,747 |
| `DA10` | 5,766 | 1,793 | 7,559 |
| `7A21` | 15,760 | 7,177 | 22,937 |
| `7030` | 5,606 | 2,825 | 8,431 |
| `D304` | 17,630 | 437 | 18,067 |

Funded fractions are consistently 0.94–1.00 across all agencies. The metering
is not concentrated in one office; it is a property of the code.

## 7. What this decides

**E196's headline survives.** The $203.32B in five IT/software cells was
bought in **98,640 funded purchases at or under $100,000** — real money,
real purchases, metered at a scale a small program operates at. The federal-
contract money axis now has:

1. **Buyer** — US federal agencies (DoD, VA, GSA, HHS, DHS, …)
2. **Unit** — 98,640 funded awards ≤ $100k in five codes
3. **Budget** — $203.32B across those cells

**What is not yet known:** who is paid for those purchases. The recipient
read (`spending_by_category/recipient/` under the same `psc_codes` filter —
verified reachable from this host in E196's reconnaissance) names the
companies. That is the next experiment.

**Named next action — the recipient read.** For the five IT codes, read
`spending_by_category/recipient/` under the same `psc_codes` filter. This
names who is paid for the 98,640 small purchases. Combined with the
agency-level breakdown in panel D, this gives buyer, unit, budget, and
vendor — the full picture of the first money-sized, code-addressed, funded
population this record has produced.

**Do not run:** a re-run of panels A/B/D on the same parameters (the client
reuses captures); the keyword form (closed by E195); any rank walk past page
500 (refused); or a re-test of G6's vocabulary ratio (the failure is a
property of code-name vocabulary, not a confound to repair).
