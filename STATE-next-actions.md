<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Next actions

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

**Named next action:** candidate screen on the money axis — COMPLETED across E199-E201.
E199 (name-pattern: prime_integrator moderately less concentrated), E200 (size-screen: small sub-segment extremely fragmented 1.5-5.8% top-10 share), E201 (combined size+name: 7A21/small/prime_integrator at 1.7% = absolute best entry point). Screen question resolved; no further screen needed on this axis.

**New next priority:** explore a fresh observation in a different domain, since the federal contracting money axis candidate screen series is complete and the screen question is answered with stable, conclusive findings across three experiments.

**Do not run:** the keyword form of this axis (closed by E195); an award-amount
filter on the recipient endpoint (E197 probe.py finding 2); a re-run of E197
panels on the same parameters.

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



## E185 completed (2026-10-18) — knitting repair planner Stage A: local planner beats full-row rollback

**What was tested.** 8 synthetic fixtures (4×4–7×7 grids, single errors). A0
full-row rollback, A1 local planner (prioritized BFS with boundary and
yarn-order constraints), A2 exhaustive oracle on F1–F2.

**The result.** G1 **8/8** repairs found; G2 A1 releases fewer loops than A0 on
**6/8 = 0.75** (kill threshold 0.625); G3 A1 matches A2 exactly on F1–F2. **Kill
gate NOT FIRED.** Per-fixture A0→A1 releases: dropped stitch 1→**0**, twisted
2→**1**, wrong cable cross 5→**1**, extra yarnover 3→**1**, wrong stitch type
3→**1**, two dropped 0→0, mis-crossed cable 5→**1**, edge dropped 0→0. The two
non-improving fixtures are dropped-stitch cases where both approaches simply
re-knit missing loops.

**What this decides — superseded 2026-10-19; read F142 first.** The mechanism
survives its own Stage A, and that is all it establishes. The candidate's
algorithmic-advantage claim was closed by **F009 on 2026-10-03**
(`RESEARCH/PRIOR-ART-KNITTING.md`): minimum-cost repair under constraints,
decomposed over independent regions and emitted as an ordered sequence, is
published work from 2007 to 2026. The fixture population, the A0 baseline and
the A2 oracle were all written by the same session, so the gate measures
self-consistency (D121). **Do not run its Stage B**, and do not read "kill gate
NOT FIRED" as a live candidate. Physical feasibility, user input burden,
adoption and product viability were never tested.

[`RESULT.md`](EXPERIMENTS/185-knitting-repair-planner-stage-a/RESULT.md).

## E182 completed (2026-10-18) — the fourth explanation of F136's gap is gone, and the ground truth has a measured ceiling

**What was tested.** E181 left one explanation standing: is the EVID gap a
disagreement with the community's chosen resolution? **The question had to be
corrected before it could be asked.** E177's draw is of questions that were
*unanswered*, so `accepted_answer_id` is non-null on **3 of 181** rows, **1 of
145** key rows, and **0 of the 60 scored rows** — the key answer is the
**top-voted** one, which E177 had already disclosed in its own RESULT and in a
pre-declared AMENDMENT-2. Three documents carried the superseded wording into the
next session, so *is the **accepted** answer the best answer, or merely the
**accepted** one?* named a field the population does not contain (F141).
Corrected to **top-voted**, with an instrument built for it.

**Two instruments, and the first had to be destroyed.** Vote margin looked like a
cheap non-judgemental proxy and was **4 of 10 against hand-read labels** — wrong
in both directions at similar rates, so not a noisy proxy but no proxy:
implementation competition reads as disagreement (`zip_transform` against a `zip`
loop), and flat contradictions sit under wide margins (`qid 79556333`: "you
can't, closed Shadow Root" against "you can add CSS, see the docs", runner-up at
44%). **Its earlier null was therefore withdrawn rather than reported.** Raw
prescriptive-token overlap was then **rejected at 0.6500 balanced accuracy
against a bar of 0.80 declared before either ran**, with specificity at
**0.5000 — chance**. The rejection is what identified the defect: shared
*problem* vocabulary counted as shared *prescription*. **Residualised against the
question's own tokens it reached 0.8000 balanced accuracy at specificity 1.0000**,
and the gate ran on it. Neither the bar nor τ moved after a result was seen.

| arm | rows | `divergent` |
|---|---|---|
| EVID missed / EVID hit / SELF hit | 9 / 6 / 12 | 4 / 3 / 4 |

**G2′ did not fire: Fisher exact p = 1.0, OR 0.80, diff −0.0556.** A post-hoc
exact permutation test on the continuous statistic, same instrument, same rows:
median residual overlap **0.054 against 0.083**, **U exactly at `n₁n₂/2`,
p = 1.0000** — not a near-null.

**Coverage is the real ceiling.** Of 60 rows, 16 are `single_answer`, 2 have a
runner-up scoring ≤ 0, and 5 are conceptual rows with no prescription to
compare: **37 of 60 rows are labelled, 21 of the 30 EVID rows**; the other 9 are
`untested`. The accepted detector has sensitivity 0.6000, and the bound it
implies straddles both arms.

**What this decides.** With E178 (`publishable` 0/46, `has_ask` 0.6739), F137 /
F138 (0.9000 on money SE) and E181 (every paired arm null), **all four
explanations of F136's gap are closed and the EVID line closes as a capability
limit** — the assistant reasons worse on questions whose resolution needs a fact
the question omits, which no context pipeline closes (D120). This is the first
closure in the line with its last explanation measured rather than unexamined.

**And a ceiling on this record's own headline numbers.** The ground truth behind
every service rate here is **contested on 21.7%** of rows (a runner-up within a
factor of two of the top-voted answer) and **uncorroborated on 26.7%** (one
answer, nothing to disagree with) — **48.3%**. E177's scorer asks whether the
assistant states the same resolution as the **top-voted** answer, so on those
rows it measures agreement with a resolution that is disputed or uncorroborated.
That weakens hit and missed rows alike, so it explains **none** of the SELF/EVID
*gap* and bounds every absolute *level* here, **0.8667 and 0.4000 included**.

**Do not run:** any re-test of resolution divergence on this population; vote
margin as a disagreement proxy; a third overlap instrument.

**Named next action — closed 2026-10-18, do not run:** `prior-art-check` the
ground-truth-quality axis before writing product code. Done as E183/E184; the
three signals proved redundant with a known quality predictor (baseline AUC
0.9986, treatment 0.9986, delta −0.0000), so that axis is closed.
[`RESULT.md`](EXPERIMENTS/182-ground-truth-contest/RESULT.md).

## E181 completed (2026-10-18) — supplying the missing fact moves nothing, and neither does pasting the thread

**What was tested.** The obvious product for E177's class: identify the missing
fact, ask for it, close the gap. Four paired arms, one population, no arm label
in any input file. **question only 7/14 = 0.5000; + the one extracted missing
fact 8/14 = 0.5714; + every comment on the thread verbatim 9/14 = 0.6429;
placebo 4/10 = 0.4000.** Wilson 95% on the three treatment arms: [0.2680,
0.7320], [0.3259, 0.7862], [0.3876, 0.8362], [0.1682, 0.6873].

**Every paired comparison is null.** Treatment vs floor: exact McNemar
**p = 1.0**. Treatment vs whole thread: **p = 1.0**. Floor vs whole thread:
**0 rows for, 2 against, p = 0.5** — *pasting the entire discussion never once
beat answering the question alone.*

**Two numbers survive.** An extracted fact is **6.7%** of the thread's tokens, so
targeted elicitation would have been fifteen times cheaper than pasting; it
simply is not the mechanism. And on all 30 EVID rows the comments name the
deciding fact on **14/30 = 0.4667**, with **10 of the 16 nulls carrying the remedy
itself** — so **the round trip runs to the solution, not to the fact.**

**Two findings about this record rather than about the world. G4 FIRED**: the
same reader re-scoring E177's answers a day later disagreed on **4 of 10** against
a declared tolerance of 3, so **no absolute level in E181 may be compared with
E177's 0.4000 or 0.8667** — only within-session paired comparisons survive.
**K1 fired** (14 rows against a declared floor of 16), so every arm is
exploratory rather than a gate result.

**What this decides.** The elicitation route for the EVID class closes. F136's
population gap stands and is now *unexplained* rather than *under-supplied*.
**Do not re-run:** a larger elicitation study, a paste-the-thread arm, or a
placebo arm on this population — all three were measured.

**Named next action — RUN as E182:** read the rows every arm missed and ask
whether the top-voted answer is the **best** answer or merely the top-voted one.

## E162 completed (2026-10-15) — the accessibility repairer is closed on mechanism; the
### dominant WCAG class is machine-generated plumbing (`162-a11y-deterministic-repair/`)

**E162 completed (2026-10-15): the deterministic accessibility repairer is
closed on mechanism (F148).** 27 real pages, axe-core 4.14.0 in jsdom as an
independent oracle, corpus hashed before any repairer existed. Arm B, which may
only repair what the document itself states, eliminated **0 of 125** AA-tagged
instances against a declared 30% gate; arm A, which may invent, eliminated 99
(79.2%) and **104 of its 104 repairs were fabrications**. The mechanism is
available in no form the table implements: **120 of the 121 missing-name nodes
carry no author-written string at all**, and the table's ten cross-element
text paths abstained too. **No candidate.** See
[`EXPERIMENTS/162-a11y-deterministic-repair/RESULT.md`](EXPERIMENTS/162-a11y-deterministic-repair/RESULT.md).

**The one continuation worth making, and it is the same population read
differently.** §4 of that result is the reproducible part: **92 of 125 (73.6%)
of the WCAG-tagged violations on these pages are aimed at machine-generated
anchors no user navigates to**, 90 of them a single syntax highlighter's line
anchors, and one page carries 98 of 216 instances. Filter the plumbing and the
same 27 pages yield **33 content-bearing WCAG-tagged defects instead of 125**,
with no single rule holding 77% of the denominator. **Next, if anything:**
measure the composition of *content-bearing* defects on a population chosen for
defect density rather than fame, with the filtering rule declared before the
count. That answers a question every accessibility budget depends on and no
published number answers — and it is cheap, because the oracle and the corpus
already exist.

**Do not rebuild the repair table.** E162's protocol bounded the repair side to
one declared fix and one re-run, and that bound was kept; a wider table is a
different instrument whose remaining class is only knowable at runtime.
