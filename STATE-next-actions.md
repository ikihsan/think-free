<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-19
-->

# Next actions

## E193/E194 + F142/D121/D122 completed (2026-10-19) — the money axis is opened, and the prototype-shaped gate is retired as a screen

**What was tested.** Two things, in this order. E193 probed ten candidate sources
for a *price* signal with four controls; E194 then scanned twelve pre-declared
recurring household jobs against the one that answered. F142 recovered why the
record had no money evidence at all: **twelve of seventeen sessions on 2026-10-18
captured zero commands and declared zero artifacts**, six of them planner-shaped
Stage-A gates of which four reported a pass, none touching a price or a user.

**The result.** Every price-bearing marketplace is **hard-blocked from this
host** — Etsy, eBay and Reddit `403`, DuckDuckGo `202`, Census key-gated — while
the iTunes Search API answers. E194's twelve jobs hold **286 on-topic apps and 6
paid (2.1%)**; nine jobs have no paid app at all; the single high-demand paid row
is **`TurboScan™ Pro`, a PDF scanner matching the word *receipt***. G2 fired in both
panels (the API returns ~4 junk free apps for a nonsense term), so this is
**descriptive, not a gate result**. F142's structural finding is the harder one:
a gate whose population, baseline and oracle share an author **cannot fire on
anything outside the model**.

**What this decides.** **D121** retires the Stage-A computational gate as a
candidate screen: no prototype-shaped candidate is written until its protocol
names one measurement taken from outside the session that invents it.
**D122** routes the money axis through **spend** — USAspending contract amounts
and Comtrade trade values, both `200` from this host, neither ever used here —
because price is not reachable.

**Do not run:** another consumer app-store scan as a prevalence estimate (fifteen
hand-declared terms bound nothing outside themselves); a re-run of any 2026-10-18
planner; a Stage A for the knitting candidate (closed by F009 on 2026-10-03).

**Named next action.** Measure what an organisation **already pays for** in a
domain where a program could displace a metered unit, and let that measurement
screen candidates. **E195 has already run this probe: USAspending answers from
this host with no key and returns award rows carrying amounts and descriptions,
so the axis is open.** G3 failed on two terms — `knitting` returned **$3.58M of
combat uniforms**, `laundry` $112,839 of base laundry service — which earns the
rule that a spend screen must **read the descriptions on the rows it sums**. Next:
a declared scan addressed by **product and service code (PSC/NAICS)** rather than
by keyword, because the keyword form is closed as declared, and re-running it with
the same words is exactly the repair this record keeps refusing. Every total must
be reported beside its industry distribution.

> **READ FIRST (2026-10-12).** The view-count domain sweep is **STOPPED**
> (E113, F116, D105). E113's matched-harvest control of E107 showed the
> effect is a harvest artifact (δ 0.826 → 0.075, stratified p=0.183) and the
> shared classifier labels only 28% of a representative pool. Every
> "ALL GATES PASS" below that came from this line is **`untested` on a matched
> harvest, not confirmed**. Do not run another registry sweep. See
> [`EXPERIMENTS/113-viewcount-matched-harvest/`](EXPERIMENTS/113-viewcount-matched-harvest/README.md).

## E183/E184 completed (2026-10-18) — the ground-truth-quality axis closes; the three signals are redundant

**What was tested.** Whether vote margin, corroboration count, and residualised
prescriptive divergence carry answer-quality information a known Stack Overflow
quality predictor does not already carry. E183's prior-art check found the area
established (6+ papers, 2015-2022, text + metadata features; vote-based features
standard). E184 tested whether the three signals add predictive power.

**The result.** 200 questions, 7,822 answer rows, logistic regression, 5-fold CV.
**Baseline AUC 0.9986, treatment AUC 0.9986, delta −0.0000.** The baseline
includes `answer_score` — the defining characteristic of the top-voted answer —
so the model trivially identifies it, and the three signals add **zero**
predictive power.

**What this decides.** The ground-truth-quality axis, as a product filtering
Stack Overflow answers for training/evaluation corpora, **does not clear the
screen**.

**Do not run:** another variant with the same label (is top-voted); the result
is definitive. **Named next action — taken 2026-10-19 as E193/E194:** return to
fresh exploration, on an axis with no money evidence in it at all.

[`RESULT.md`](EXPERIMENTS/183-prior-art-ground-truth-quality/RESULT.md).

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

## Money SE fresh observation (2026-10-17) — the round trip is stronger when the missing fact is personal

Declared prediction: on money SE, missing facts are more personal and harder to
elicit, so the round trip should fail *more*. **Result: the opposite** — 9/30 =
0.3000 of the highest-arrival answered questions lack a specific personal fact
and **27/30 = 0.9000 carry a round-trip ask**, against Stack Overflow's 31/46 =
0.6739. The venue asks *more* readily when the fact is sensitive. **The
"unserved need" hypothesis is dead for money SE too** (F138). **Next action —
taken 2026-10-19:** fresh exploration (E193/E194/E195).

## E178 completed (2026-10-17) — the missing evidence is not in anything the project publishes; the venue's own round trip already supplies it

**The gap E177's own measurement opened.** E177 found a class of **46 of the 100
highest-arrival rows that carry a key answer** whose resolution depends on a fact
or artefact the question does not contain, and on that class a free general
assistant reaches **12/30 = 0.4000** against **26/30 = 0.8667** on the
self-contained half (gap +0.4667, Fisher p = 0.000368; F136, D118). **None of
that says the population is buildable**, which is what this experiment asks.

**The result.** Blind re-key of all 46: **publishable 0/46 = 0.0000, asker_only
0.4565, third_party 0.4348, none 0.1087**. **G1 FIRED** (publishable < 0.50): the
FETCH route closes. **G4 FIRED** (has_ask 0.6739 >= 0.50, ask_then_asker 0.6739 >=
0.25): the venue's own workflow already runs the round trip on these very rows, and
the person supplies the fact. The honest statement is not "unserved" but *served
by an interaction that already exists, and unreachable by one-shot answering*. **G5
NOT fired** (none = 5, not > 9): EVID precision is above 0.80. M1: has_comment
0.8043, has_ask 0.6739, answer_asks 0.4348, evidence_in_comments 0.8478,
discriminating_and_asked 0.6087. M3: already_present 0.1522 (a ceiling on E177's
labels), used 0.8043. The exploratory comparison does not reproduce the addendum's
reframing: gap -0.0741, p = 0.52. **E177's population closes with no candidate.**

**What this decides.** The missing evidence is a version, a config value, or a data
value the asker holds; the venue's own round trip already supplies it. **Do not
run:** E176 as written, E170's global arm, another view-count domain (D105, F133),
or a fresh draw of E177's comparison.

## E186 completed (2026-10-18) — NHTSA complaint-recall prediction kill gate fired

**What was tested.** Automotive safety; a new need type (predictive monitoring).
Does public NHTSA complaint data predict recalls for a component?

**The result.** 20 model/years, 12 with a recall (46 recalls), 42,015 complaints.
**G1 PASS, G2 PASS, G3 FAIL** (median recalled ratio 1.78x < 2.0), **G4 PASS**
(non-recalled 1.25x < 1.5), **G5 FAIL** (Mann-Whitney p = 0.187 > 0.05).

**What this decides.** Complaints rise 1.78x before recalls but weakly and
non-specifically; 39% of recalls had zero pre-recall complaints in their category,
and manufacturer channels are clearly primary. **Do not pursue** prediction from
public complaint trends. **Named next action — taken 2026-10-19:** fresh
exploration on an axis carrying no money evidence at all (D121, D122).

## E187 completed (2026-10-18) — Clinical trial eligibility matching kill gate fired

**What was tested.** A new domain (clinical trials) and a new need type
(matching): can ClinicalTrials.gov structured eligibility fields match patient
profiles to recruiting trials with useful yield?

**The result.** 100 synthetic patients, 385 recruiting trials. Funnel:
condition (median 16.5) -> age (16.0) -> sex (16.0) -> **location (1.0)** ->
exclusion (0.0). **G1 PASS**, **G2 FAIL** (35/100 <80), **G3 FAIL** (median 0.0),
**G4 FAIL** (mean 0.5 <3), **G5 FAIL** (0% retention).

**What this decides.** Location is the dominant bottleneck (94% reduction); free-text
exclusions eliminate the rest; only 4 of 20 conditions yield any match, and a
structured-field-only tool returns empty for 65% of patients. **Do not pursue**
patient-trial matching on structured API fields alone. **Named next action — taken
2026-10-19 as E193/E194/E195:** fresh exploration on an axis carrying no money
evidence at all, which is what D121 and D122 now require of every candidate.

