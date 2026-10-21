<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# Next actions — archive: accessibility and the EVID line (E162, E181, E182, E185)

Split out of [STATE-next-actions.md](STATE-next-actions.md) on 2026-10-21
under the 250-line rule. Entries are verbatim; nothing was deleted. One markup
repair: E162's header had been broken across two lines and is rejoined here.

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

## E162 completed (2026-10-15) — the accessibility repairer is closed on mechanism; the dominant WCAG class is machine-generated plumbing (`162-a11y-deterministic-repair/`)

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
