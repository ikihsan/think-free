<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-19
-->

# Decisions — records (part 6)

Decisions **D123, D127, D128**. Same invariant and shape as
[`DECISIONS-RECORDS-5.md`](DECISIONS-RECORDS-5.md): a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason. Split
2026-10-19 because part 5 was near its cap; D127 added 2026-10-20; D128 added
2026-10-21.

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

## D127 — the line-anchor rewrite route closes as dominated; the remedy is build configuration

**Date:** 2026-10-20. **Session:** 2026-10-20-001. **Evidence:**
[E202](EXPERIMENTS/202-line-anchor-rewrite/RESULT.md),
[F149](FAILURES-findings-48.md).

**The choice that was open.** E162 closed the deterministic *repairer* (0 of
125 eliminated) but left one class it could not touch: the machine-generated
empty self-link `<a id="__codelineno-N-M" name="…" href="#…"></a>` that
`pymdownx.highlight` emits with `anchor_linenums` on. Two routes existed —
rewrite the element after the fact, or change the build so it is never emitted.

**What E202 measured.** On the 3 pages where the class appears, the rewrite
eliminates **83/83** empty-self-link instances, adds **0** strings, introduces
no regression and keeps **260/260** targets resolvable. The upstream CSS
mitigation (`a[id^="__codelineno"]{visibility:hidden}`) removes **83/83** too,
changes nothing in the DOM, loses no target and needs no migration. The protocol
declared the outcome in advance: if arm 2 removes as much as arm 1, arm 1 is
dominated. **G4 fires on population** — 3 pages / 3 hosts against ≥ 12 / ≥ 6.

**What is decided.**

1. **The rewrite route closes.** No line-anchor rewriter is built. The remedy
   is build configuration — `anchor_linenums: false`, the CSS rule, or authored
   text inside the anchor — all of which prior art already ships.
2. **A dominated mechanism is not a candidate, whatever its gate rate.** G1 =
   1.0, G2 = 0, G5 = 1.0 and the route still closes, because the strongest
   accessible alternative does the same job with none of the migration.
3. **E162's "dominant class" is scoped to its corpus, not withdrawn.** A fresh
   mkdocs harvest puts the pattern on 3 of 65 pages (4.6%) against E162's 90 of
   125 instances (72.0%) on 27 fame-selected pages.

**Rejected.** (a) *Ship the rewrite as a post-processor for sites that cannot
change their build.* It is dominated wherever the stylesheet ships, which is the
normal case; the uncovered scope (a raw HTML export, a pasted fragment) is a
scope statement, not a market. (b) *Treat G1 = 1.0 as a result.* G4 fired, so
the population is too thin to validate anything, and a mechanism demonstration
on 3 pages is not a product.

## D128 — a number at the reload point is verified by re-deriving it from the population it names, and a committed prototype whose sampling cannot produce that number is a provenance defect even when the number is correct

**Date:** 2026-10-21. **Session:** 2026-10-21-001. **Evidence:**
[E207](EXPERIMENTS/E207-sbir-category101-census/RESULT.md).

**The choice that was open.** E204/E206 sat at `STATE.md`'s reload point
reporting NIH SBIR category 101 = 147 grants, 134 distinct orgs, top-5 share
11.6% — "the most fragmented market measured in this repository" — and a
committed prototype (`tools/nih_accessibility_prototype.py`, T-0095) encoded a
derived IC consensus (NIAID, NCI, NHLB, NIA) as recommendations. Three observed
facts made the number unverifiable *as recorded*: (1) E204/E206 directories
hold only a `RESULT.md`, no script and no raw data — the F142/D121 pattern; (2)
the prototype's `fetch_grants()` has **no `activity_codes` filter** — it pulls
from all 85,133 FY2023 projects, caps at 2,000 in default order, then filters
that slice — so it cannot produce a 368-row population; (3) the API does report
exactly 368 for FY2023 `R41`/`R42`, so a correct census is reachable. Either
re-run the census or leave the reload-point number unbacked.

**What E207 measured.** A complete `R41`/`R42` FY2023 census (368 rows, stopped
by the API's own `meta.total`, no cap, no sampling) returns **147 grants, 134
orgs, top-5 share 0.1159, total $63,254,235** — matching E204 to the dollar,
with the top-5 orgs also matching to the dollar. All five predeclared gates
PASS (G1 population, G2 count, G3 orgs, G4 concentration, G5 category set).

**What is decided.**

1. **E204's category-101 finding is real and now source-supported** (it was
   previously *untested* from the repo). The accessibility pattern on this
   population survives its own replication.
2. **The record was defective independently of the science.** E204/E206 carried
   no runnable instrument and no raw data; the smallest repair is to commit the
   census script and the full 368-row `raw/census.json` so the number is
   reproducible from the repo. E207 is that repair.
3. **A committed prototype whose sampling cannot produce the population its
   RESULT.md names is a provenance defect even when the number it quotes is
   correct.** The prototype's IC consensus rests on an unfiltered 2,000-row
   slice of 85,133, not the 368-grant census — so the recommendations' stated
   basis does not match their actual basis. This is **un-repaired** and does not
   change E204's correctness.

**Rejected.** (a) *Leave the reload-point number as-is because it is probably
right.* It was, but "probably" is not the standard; the mission's non-negotiable
is that a claim carries something a reader can re-run, and the F142 day is the
cost of skipping that. (b) *Fix the prototype's sampling in the same pass.* It
is a separate instrument defect; folding it into a replication muddies what the
census established. It is recorded, not silently repaired.

**Rule.** A number presented at the reload point is verified by re-deriving it
from the population it names, and the re-derivation is committed as a script plus
raw data — not a `RESULT.md` alone. A prototype whose fetch cannot produce the
population it claims to analyze carries a provenance defect recorded beside the
number, whether or not the number is independently correct.

## D129 — a screen's axis is a candidate explanation only after its correlation with the obvious confound is measured, and an entry claim needs an entrant measurement

**Date:** 2026-10-21. **Session:** 2026-10-21-002. **Evidence:**
[E208](EXPERIMENTS/E208-sbir-entrant-share/RESULT.md), F152.

**The choice that was open.** Five experiments (E196–E207) reported a
"small-program accessibility" pattern — a fragmented vendor landscape means a
small team can build and sell there — and `STATE.md` carried the reading at its
reload point. Nobody had measured the step the reading depends on: *do the
winners include newcomers?* E208 measured it on the population where the
pattern was last claimed (NIH SBIR R41/R42, FY2014–FY2023, 3,407 rows, identity
`external_org_id`), with gates declared before the fetch.

**What the measurement returned.** The declared kill gate fired:
**fragmentation is not associated with newcomer entry** (Spearman ρ = −0.2456,
one-sided p = 0.9754 over the 64 categories with ≥ 10 awardees; the nine-year
sensitivity window agrees at −0.2748). The cause is visible and cheap to find:
**ρ(fragmentation, category size) = 0.9711** — "fragmented" is, in this
population, "many awardees" — and larger categories have *fewer* newcomers
proportionally. Entry itself is common (0.527 segment, 0.407 domain), which is
a measurement the record did not have before, and category 101's 0.5075 is
unremarkable.

**Rules adopted.**
1. **An entry claim requires an entrant measurement.** "Many vendors, low
   concentration" is a statement about incumbents; it says nothing about who
   wins next. A screen that reports concentration as an *entry* signal is
   reporting an inference.
2. **Before an axis explains anything, measure its correlation with the
   obvious confound.** Fragmentation correlated 0.97 with category size here,
   and that costs one fetch to find out. A screen whose axis is a proxy must
   say so on the screen.
3. **A negative closes the claim and the population tested, not the
   application.** The federal IT codes (E196–E198) remain untested on entry;
   this decision does not touch them.

**Rejected.** (a) *Keep the accessibility reading on the reload point anyway,
since E204/E207's concentration numbers are correct.* The numbers are correct
and the reading is a different claim; carrying the inference unmarked is the
F142 shape one level up. (b) *Follow the negative ρ into a size-adjusted
entry model now.* That is a new analysis on the same data, and the bound in
E208's protocol says one analysis per population; the IT codes are the cheaper
place to learn the next thing.
