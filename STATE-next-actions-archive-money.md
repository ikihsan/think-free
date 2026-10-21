<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# Next actions — archive: the federal money axis (E196–E198)

Split out of [STATE-next-actions.md](STATE-next-actions.md) on 2026-10-21
under the 250-line rule. Entries are verbatim; nothing was deleted. One markup
repair: an unclosed bold marker in E198's named-next-action paragraph.

## E198 completed (2026-10-19) — the vendor landscape is fragmented: 9,977 distinct companies, top 10 per code hold 34.5%–57.6%

**What was tested.** E197 established five IT/software cells carrying $203.32B
across 98,640 funded purchases ≤ $100k. E198 read the recipient endpoint
(`spending_by_category/recipient/` under the same `psc_codes` filter) for all
five codes to name who is paid.

**The result.** **15,210 recipient records across 9,977 distinct companies** for
the five codes. G1 PASS (all five codes return well-formed paginated lists).
G2 PASS (survives): total distinct recipients 9,977 ≥ 20; top-10 share per
code: DA01 34.5%, DA10 35.8%, 7A21 48.9%, 7030 38.4%, D304 57.6% — all ≤ 80%
kill threshold. Controls C1–C4 all PASS (recipient sums match cell totals within
0.02%, no unused filters, zero controls hold).

| code | cell total | purchases $1–$100k | recipients | distinct | top-10 share |
|---|---:|---:|---:|---:|---:|
| `DA01` | $94.91B | 14,719 | 3,610 | 3,112 | 34.5% |
| `DA10` | $33.01B | 16,477 | 3,651 | 3,089 | 35.8% |
| `7A21` | $29.21B | 32,747 | 3,977 | 3,384 | 48.9% |
| `7030` | $25.83B | 14,033 | 3,917 | 3,298 | 38.4% |
| `D304` | $20.37B | 20,664 | 1,155 | 1,004 | 57.6% |

**What this decides.** The vendor landscape is **fragmented**, not concentrated.
The money axis now has all four coordinates: **buyer** (federal agencies),
**unit** (98,640 funded purchases ≤ $100k), **budget** ($203.32B),
**vendor** (9,977 distinct companies, top 10 hold 41.4% aggregate). This is a
**genuine market at the scale a small program operates at** — concentration is
low enough that a small program could win direct awards without being a
subcontractor to a prime.

**Named next action:** candidate screen on the money axis — **COMPLETED** via E199 and E200 in this tree. E199 screened the five IT/software PSC codes (DA01, DA10, 7A21, 7030, D304) against criteria for small-program accessibility (vendor concentration, sub-$40k purchase count, recipient diversity), ranking them: 7030 > 7A21 > DA10 > DA01 > D304. E200 performed a sub-segment screen within 7030, identifying **small_technical** as the most accessible sub-segment: 1,126 sub-$40k purchase entry points, 1,126 recipients with amount data, top-3 concentration 0.6%. **E201 practical access test:** 1,130 sub-$40k contractors in 7030/small_technical; category breakdown: small_software_vendor 222 (19.6%), consulting_firm 95 (8.4%), specialized_tool 148 (13.1%), niche_provider 665 (58.8%); contract amounts: min $40, max ~$40K, median $16.8K, mean $18.1K. **Answer to the E198 question:** PSC code **7030 "Information technology software," sub-segment small_technical** admits a small program to build and sell, with 1,130 sub-$40k entry points and very low vendor concentration (0.6% top-3 share), though individual contract values are modest (median $16.8K).

**Do not run:** a re-run of the same candidate screen on unchanged data; the practical access test (E201) has characterized the market depth but cannot alone validate a product; fresh exploration without first documenting these findings.

## E197 completed (2026-10-19) — E196's "purchases" are purchases: 98.6% of federal award records carry money

**What was tested.** E196 §2 reported five IT/software cells carrying $203.32B
"bought in tens of thousands of separate sub-$40k purchases," and F143/D123
recorded that nine of the 25 cells clearing the addressability gate clear it only
because their 10,000th-smallest award carries no money. E197 counted the awards
that carry money (≥ $1) per code by bisecting the ascending award order, for all
100 PSC codes, with an independent descending arm on the 25 G4 codes.

**The result.** Median `funded_fraction` = **0.9862** over 100 codes. **12 of 25**
E196 G4 codes clear ≥10,000 funded awards ≤ $100k (G4 survives, ≥10). All five IT
codes clear: `DA01` 14,719, `DA10` 16,477, `7A21` 32,747, `7030` 14,033, `D304`
20,664. The descending arm agrees exactly on all 13 comparable codes (12 censored
at the 500-page ceiling — G5 fails on censoring, not disagreement). G6: no
vocabulary confound (all five IT codes below 2× ratio). **F143's concern is
resolved: an award count IS a purchase count here.**

**What this decides.** E196's headline — "$203.32B bought in tens of thousands of
separate sub-$40k purchases" — survives. The money axis now has a confirmed,
funded-purchase population. **Named next action:** the recipient read
(`spending_by_category/recipient/` under the same `psc_codes` filter) names
**who is paid** for the 14,000–32,000 small purchases in each IT cell — buyer,
unit and budget all known at once, for the first time.

**Do not run:** a re-run of panels A/B on the same parameters; the keyword form
of this axis (closed by E195); any `rank_p × 100` checkpoint (refused past page
500).

## E196 completed (2026-10-19) — five IT/software PSC codes hold $203.32B bought in tens of thousands of separate sub-$100k awards

**What was tested.** D122 routed the money axis through spend because price is
unreachable; E195 proved the endpoint answers and that a keyword's money belongs
to a different industry than the word. E196 addressed the same money by
**product and service code** — the buyer's own taxonomy — and asked the question
that makes it a screen rather than a ranking: **is the money bought in many
small separate purchases, at a scale a program could sit in front of?**

**The result.** Top 100 PSC base codes, FY2020–FY2025, `spending_level: awards`,
**$5.65T across 100 codes.** **G2 PASS** (7 of 7 zero-control checks), **G3 fires**
(H = 40.63, **p = 0.00416**, 21 families, 91 codes — the families are
distinguishable, so the metering is a property of the code), **G4 fires on 25 of
100**, **G1 FAIL** and **G5 not evaluated**, both for reasons below.

**25 codes hold at least 10,000 separate awards of $100,000 or less inside a
cell of at least $1B**, and the densest cluster is IT and software:
`DA01` app-development support ($94.91B, 27,425 awards, 10,000th award
**$27,519**), `DA10` app development SaaS ($33.01B, 26,656, **$30,903**), `7A21`
business application software ($29.21B, 50,777, **$14,313**), `7030` IT software
($25.83B, 24,492, **$40,320**), `D304` telecommunications ($20.37B, 29,072,
**$11,544**). **$203.32B bought in tens of thousands of separate sub-$40k
purchases** — the first money-sized addressable population this record has
produced, and still not a candidate.

**The finding that decides the next experiment (F143, D123).** Nine of the 25
clear only because their 10,000th award carries no money, and at the measured
instrument ceiling — `spending_by_award` answers 200 for page 500 and 422 for
page 501, so **the 50,000th award is the deepest any code can be read to** —
`R499` ("Support-Professional: Other", $270.27B, 302,317 awards) has its
50,000th award at **$51.93-$52.04**. **Half a million federal award records
worth about fifty dollars each.** An award count is not a purchase count here,
and the error runs in the direction that manufactures markets.

**G1's failure is an instrument ceiling, not a source defect.** The nine codes
with more than 100,000 awards — exactly `R499`, `6505`, `R706`, `9130`, `6515`,
`1560`, `8915`, `8905`, `6640` — have no median stratum because the endpoint
refuses past page 500. All their counts and rank checkpoints to 10,000 returned
`200`, and no request carried an ignored-filter message.

**G5 is not evaluated, and the reason is structural.** `Y1` construction passes
(`construct` ratio **11.1**, `remodel` **20.0**) and `S2` housekeeping passes
(`cleaning` 5.88, `custodial` 50.0, `guard` 2.38), so **the code-addressed read
is not procurement vocabulary** — E195's `TurboScan` defect does not recur. The
`3` arm **had no members**: no `3`-prefixed code reached the head-100, so no
keyword can clear a 2× base rate over an empty set. `PROTOCOL.md` declared
thresholds and a `not evaluable` rule for G3 and G4 and **none for G5**.

**Named next action — bisect the funded-award count, for all 100 codes.**
Bisect the ascending award order for the rank at which amounts turn positive.
About ten requests per code, exactly, and it returns the number the mission
actually needs: how many records carry money, i.e. how many things a program
could displace. It settles whether the $203.32B in the table above is tens of
thousands of real purchases or tens of thousands of records. Once that is
exact, `spending_by_category/recipient/` under the same `psc_codes` filter —
**verified reachable from this host** — names who is paid for the small
purchases. **Buyer, unit and budget, all known at once, for the first time.**

**Do not run:** the keyword form of this axis (E195, G3 fired against it); a
longer tail walk (superseded by AMENDMENT-3's order statistics); any
`rank_p x 100` checkpoint (refused past page 500); or a re-run of panel 2 on the
same parameters — `client.call` reuses any capture whose stored request key
matches, so it is free and would return the same bytes.
