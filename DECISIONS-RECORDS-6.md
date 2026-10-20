<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-19
-->

# Decisions — records (part 6)

Decisions **D123**. Same invariant and shape as
[`DECISIONS-RECORDS-5.md`](DECISIONS-RECORDS-5.md): a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason. Split
2026-10-19 because part 5 was near its cap.

## D123 — a candidate screen may be addressed by money, and the unit it counts must be a unit a program can displace

**Date:** 2026-10-19. **Session:** 2026-10-19-003. **Evidence:**
[E196](EXPERIMENTS/196-federal-spend-metered/RESULT.md),
[F143](FAILURES-findings-45.md).

**The choice that was open.** D122 routed the money axis through spend because
price is unreachable from this host. E195 showed the endpoint answers and that a
keyword's money belongs to a different industry than the word, so the form was
closed. That left the named alternative: **address the same money by the buyer's
own taxonomy** — product and service code — and let the *shape* of the money
screen candidates, rather than its size.

**What E196 measured.** Across the top 100 PSC base codes of US federal
contracting (FY2020–FY2025, $5.65T, `spending_level: awards`), **25 codes hold
at least 10,000 separate awards of $100,000 or less inside a cell of at least
$1B**, and the densest cluster is IT and software: `DA01` app-development
support ($94.91B, 27,425 awards), `DA10` app development SaaS ($33.01B, 26,656),
`7A21` business application software ($29.21B, 50,777), `7030` information
technology software ($25.83B, 24,492) and `D304` telecommunications ($20.37B,
29,072) — **$203.32B bought in tens of thousands of separate sub-$40k
purchases.** G3 fired (families are distinguishable, H = 40.63, p = 0.00416), so
the metering is a property of the code and not an artifact of the head.

**And the measurement that constrains everything built on it.** Nine of those
25 clear only because their 10,000th-smallest award carries under $100, and at
the instrument's ceiling — `spending_by_award` refuses past page 500, so the
50,000th award is the deepest any code can reach — `R499` ("Support-Professional:
Other", $270.27B, 302,317 awards) has its 50,000th award at **$51.93–$52.04**.
**Half a million federal award records worth about fifty dollars each.**

**What is decided.**

1. **A spend screen may be addressed by the buyer's taxonomy rather than by
   keyword.** The keyword form stays closed (E195), and the code-addressed form
   is the one this mission uses.
2. **The unit a screen counts must be a unit a program can displace, and the
   screen must prove it counted that unit.** An award count is not a purchase
   count where a material share of award records carry no money, and no gate may
   report a count without stating whether the records behind it were funded.
3. **The next money measurement on this axis is exact or it is not reported.**
   Bisecting the ascending order for the rank at which award amounts turn
   positive returns the funded-award count for ~10 requests per code; a screen
   that needs a longer walk instead of that bisection is choosing the expensive
   wrong answer.

**Rejected.** (a) *Address spend by keyword with better keywords.* E195's
finding is that the word buys the industry, not the market: `knitting` returned
$3.58M of combat uniforms. (b) *Treat the 25 codes as a shortlist.* They are
cells, not opportunities; 9 of them are nominal, and nothing here says who is
paid or for what. (c) *Report G4's 25 and let the reader discount the 9.* The
discount is the finding — a screen that cannot tell a funded award from an
unfunded record cannot size anything, and the next instrument exists.

**Named next action this decision creates.** For all 100 codes, bisect the
ascending award order for the rank at which amounts turn positive, and report
the funded-award count beside the cell total; then, for the codes that survive,
read `spending_by_category/recipient/` under the same `psc_codes` filter to name
who is paid for the small purchases. That is a named, reachable, falsifiable
step, and it is the first in this record where a buyer, a unit and a budget are
all known at the same time.