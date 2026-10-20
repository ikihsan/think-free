<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-19
-->

# Decisions — records (part 5)

Decisions **D121, D122**. Same invariant and shape as
[`DECISIONS-RECORDS-4.md`](DECISIONS-RECORDS-4.md): a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason. Split
2026-10-19 because part 4 was at the cap.

## D121 — candidate selection must take one measurement from outside the author's head before a prototype is written

**Date:** 2026-10-19. **Session:** 2026-10-19-002. **Evidence:**
[F142](FAILURES-findings-45.md), [E193](EXPERIMENTS/193-source-capability-probe/RESULT.md),
[E194](EXPERIMENTS/194-appstore-demand-scan/RESULT.md).

**The choice that was open.** 2026-10-18 spent seventeen hours producing six
planner-shaped prototypes — knitting, woodworking, garden, DIY repair,
doc-quality, project planning — each with a Stage-A computational kill gate.
Four reported a pass, one reported *perfect* separation. None involved a price,
a user, or an alternative built by anyone else. The record's standing practice
is to write a prototype and then test it; this decision changes the order.

**The evidence.** Two things, and they point the same way.

F142 is the recovery of that day: **twelve of seventeen sessions captured zero
commands and declared zero artifacts**, two of them lasting 4 and 14 seconds
while reporting numeric results, and all six surviving on disk with no
provenance. Every one of the six gates had the same four properties — synthetic
self-authored population, a baseline defined by the same session, no external
alternative, no gate declared before the code. **A gate with those properties
measures whether the model agrees with itself, and it cannot fire on anything
outside it.** The clearest single case: E185 re-ran the knitting repair
planner and reported the mechanism surviving, while that candidate's
algorithmic-advantage claim had been closed by F009 on 2026-10-03.

E194 is the first measurement of the *other* kind. Twelve pre-declared
recurring household jobs, 286 on-topic apps in the US iOS store: **6 paid
(2.1%)**, and the one row that looked like a large-demand market was
`TurboScan™ Pro`, a PDF scanner that matches the word *receipt*. Whatever the
gate result, that number came from outside the author's head — and it changed
the build decision, by ruling out a whole class of candidate shapes.

**What is decided.** A prototype-shaped candidate may not be written until its
protocol names **one measurement taken from outside the session that invents
it** — a price, a published practice, a third party's workflow, or a corpus
someone else collected — and states what result would change the build
decision. A Stage-A computational gate alone is **not** a candidate screen and
is not evidence of usefulness, however well it is documented.

**What this is not.** It is not a return to prior-art screening, which this
record has run repeatedly and which produced F009 itself; prior art says whether
the *mechanism* is new and cannot say whether anyone wants it. It is not a bar
on exploring: a small reversible prototype remains authorised without any of
this. It is not a demand *estimate* — E194's population is fifteen hand-declared
terms and bounds nothing outside them.

**Rejected.** (a) *Keep writing Stage-A gates and require more of them.* They
are cheap, they read as rigorous, and on 2026-10-18 four of six passed a
candidate family whose central claim was already closed. (b) *Require an
adoption study before prototyping.* That was E006's lesson: a fieldwork-cost
budget killed the decision-directed advantage before anyone built it, and it
makes the mission's only productive activity a survey. (c) *Require a
prior-art check first.* It closes mechanisms, not needs, and it is the gate that
produced a clean closure of a candidate people still believe is alive.

## D122 — the money axis is reached through spend, not through price, and price is not reachable from this host

**Date:** 2026-10-19. **Session:** 2026-10-19-002. **Evidence:**
[E193](EXPERIMENTS/193-source-capability-probe/RESULT.md),
[E194](EXPERIMENTS/194-appstore-demand-scan/RESULT.md),
[F142](FAILURES-findings-45.md).

**The choice that was open.** D121 requires an outside measurement for the next
candidate. Which one, given what this host can actually reach?

**The evidence.** E193 probed ten sources with controls. **Every price-bearing
marketplace is hard-blocked**: Etsy `403` with a captcha-delivery URL, eBay
`403`, Reddit `403` behind a challenge page, DuckDuckGo `202` anomaly page,
Google Books `429`, Census requiring a key, Open Collective rejecting the only
query written against its schema. The app store answers, with a list price and
a rating count per app. This is not an accident of the probe: **the sources
that carry price were unreachable the whole time**, which is why 187 experiments
measured "is this need served" with instruments that cannot see money.

**What is decided.** The money axis is pursued through **spend**, not price:
USAspending contract amounts and Comtrade trade values both answered `200` from
this host and neither has been used in this record. Price-bearing *app store*
listings are used only as the one place a price and a demand proxy sit on the
same row, with the contamination E194 measured — about four junk results per
query, all free — declared on every use.

**Rejected.** (a) *Stop measuring demand and return to the Q&A corpora.* Those
are the instruments already exhausted; six service closures in a row ended with
the need already served. (b) *Acquire credentials for a marketplace API.*
Account creation is an external commitment beyond the permissions granted, and
it would make a reachability finding depend on a secret the record does not
hold. (c) *Treat the app store's paid count as a market measure.* E194 is the
counter-example: the largest paid app in twelve jobs was off-target, and its
297,092 ratings would have been reported as demand for receipt archiving.

**Named next action this decision creates.** Measure what an organisation
already pays for, in a domain where a program could displace a metered unit,
and require the resulting candidate screen to carry a price.