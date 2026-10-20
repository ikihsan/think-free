# Next actions, closed items

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

Split out of [`STATE-next-actions.md`](STATE-next-actions.md) on 2026-10-06 at its
300-line cap, by invariant rather than by size: **everything here is closed, done, or a
standing "do not" instruction**, and none of it is a candidate for the next session's
effort. Originally items 3–12; **items 0b, 1 and 2 moved here the same day**, so that a
reader looking for what to do next finds only things that are open. **Items 1-12 are numbered items in
[`STATE-next-actions-closed-2.md`](STATE-next-actions-closed-2.md)**, which this
file split into on 2026-10-06 at its own cap: that file holds the prose about why
closed work was moved plus the standing deferral 0b, and that one holds the items.
**The live items are now **0** and **0d**.

**Why the split is not housekeeping.** The list had reached 300 lines partly
because closed entries kept their full derivations, which made the open items
harder to find than the closed ones. Read this file when a future session wants
the reasoning behind a closed item — most often to check whether re-running it
would produce anything new.

**A second move on 2026-10-06, and it was the owner's brief rather than the line
count.** Items **0b, 1 and 2** moved here. All three are about *this
repository's own gates and CI*, none is candidate work, and leaving them in a
file headed **Ordered by information gained per unit of effort** made maintenance
look like the next experiment. F031 raised this in the first place, and five of the
last eight sessions have been about instruments. **The live items are now 0 and 0d,
and only one of those is research.** The gate discipline D025 and T-0036/T-0042
established is a *rule for writing gates* and stays in force from
[`docs/policy/gate-falsification.md`](docs/policy/gate-falsification.md); it does
not need a place in the ranked list to keep applying.

## Items moved on 2026-10-06

**The gaps in the gate pattern, both found by colliding with it, and one in the record
rather than in a red run**, are closed and were carried in full by items 1 and 2 of
[`STATE-next-actions.md`](STATE-next-actions.md), which moved to
[`STATE-next-actions-closed.md`](STATE-next-actions-closed.md) on 2026-10-06 because they
are maintenance and the list is ranked by what to do next: rule 7 read three of the four
places a number is written, so two VMs took **defect 7** in the same hour (T-0036) and two of
five decision records were false while every gate passed (T-0042). One entry point reads the
sources now, and its residual ceiling is written down: a repeated number is detectable, a
dropped one is not.

**F055 is the ninth instance of that shape and the sharpest, because no gate was involved
at all:** a selection rule declared for one reason — `sort=votes`, because "elaborated need
statements live there" — selects for *answered* questions, and the stratum it draws is
**4.5× poorer in the thing being measured**. Full statement and the rule it generalises
to, in [`STATE-constraints.md`](STATE-constraints.md).
**The pattern in the red runs of 2026-10-04 is not "gates are missing" but gates that exist
and are never run**: a task's `verify` omits the one gate its change can break, a fixture
omits the clock the code reads, a split leaves one reader unwired. T-0045's fix is the
general one — put the gate in the command the protocol already points at, so there is
nothing to forget. A gate must also read the property it claims to check and be falsified
against the defect's own bytes (D025, F013); ten gates work that way, the two newest being
a restated experiment number held to its artifact by the number's *shape* (T-0056, F024,
defect 22) and E034's arms, whose 11 mutations are each caught. **Line caps are the
standing friction**, and each repair moved material to the file whose invariant owns it —
this session four times for E034. `STATE-defects.md` cannot be split inside its own list,
so that split is a task.

 0b. **The CI flake: deferred on purpose, not overlooked.** Three tests failed on
     identical bytes and six full suite runs did not reproduce it. T-0057 makes the
     next occurrence name itself; the unmeasured half is that `make_fleet` builds a
     bare remote plus two clones **per test class**, so fixture cost scales with the
     test count and only a 2-CPU runner shows it. **Deferred because CI is green
     and nothing is blocked on it**, and not worth displacing a research question.

     **Ceiling:** one platform, one label, three sites at 3–5 tags each, and the
     canonical edge unreachable through nine named channels — so a moderator's judgement
     and a findability failure are not separated here. Reading in
     [`STATE-in-flight-2.md`](STATE-in-flight-2.md).

  0f. **CLOSED. The score-tail worklist is one unauthenticated URL, so the candidate is
      prior art and nothing is built** (F059, D066, D067, `EXPERIMENTS/036-search-backlog/`,
      T-0080). The declared next action — *does a person's own search box already return
      this?* — was answered **before** the second measurement request, by a reachability
      probe: `/search/advanced?site=stackoverflow&tagged=git&sort=votes&order=asc&pagesize=100`
      returns **100 questions ascending by score, 81 of them ids already in E034's committed
      harvest (first at rank 1), and 13 labelled `Duplicate`/`exact duplicate` in the
      payload's own `closed_reason`**. No key, no custom filter, no computation. E035's
      differentiator was *"the platform's own closure label over a population no surface
      orders that way"*, and **the platform orders it that way itself**. KILL-R met at 8
      requests after three experiments spent 1125 rows on the population. Gate R1 is
      `not_evaluated` (200 with 0 items on `travel/customs`, cause untested), KILL-Q is
      `not_evaluated` at n=4 against n=2, and the negative control was refused by the quota
      window — **the kill does not need them**, being an id-intersection against committed
      bytes, but the retrieval arms are thin and the two plumbing bugs are in the raw
      evidence. Reading in [`STATE-in-flight-3.md`](STATE-in-flight-3.md).
      **Three corrections to the record.** F058's *"no surface offers the ordering"* was
      measured on a tag page's seven rendered tabs and is now scoped to that (**D066**:
      a reachability claim must name the interface surface it enumerated). E035's *"the
      label needs an API key"* was a per-route fact about `/questions/unanswered` and
      `/questions/{ids}` generalised to the platform, and `/search/advanced`'s **default**
      filter carries the label unauthenticated. And `closed` is the one filter value that
      route does **not** validate — `closed=maybe` returns 200 with `closed=yes`'s items —
      so no closed-only control was ever establishable from that route's behaviour.
      **D067 now governs the next candidate.** A candidate whose value is a mechanism is
      tested against **that mechanism's existing source before any population is measured
      for it**. Two requests, not 1125 rows. **Ceiling:** the rendered site is Cloudflare-
      blocked from this host, so whether the *web UI* exposes this against the API is
      `not_measured` — a browser or user question, not another request.
   0d. **Invention item (D048), and its seat is empty by measurement — now by a kill
   as well, and the rule that orders the next search is D067.** This entry
0c. **The cheapest question F034 opened, partly answered by F037 and now mostly
   closed.** F034 could read serving evidence for 57% of the incumbents its own
   population contained and 22% of the young arm, so *a screen whose premise is
   unmeasurable four times in five is not a screen* — a statement about the
   world's distribution rather than about this repository's tooling. **F037
   measured the fraction and it is high where the candidates live: 14 of 18 young
   rows undecided, 13 of them tools, and 43% of the mature arm.** What it also
   shows is that undecidability does **not** track artifact class — 10 of the 14
   unreadable young rows are executable — so "this is just a document" never
   explains an unreadable row. **What remains open is whether the fraction
   predicts anything about the need**, and its falsifier is a population where
   the unmeasurable fraction is near zero. **Ceiling:** 015's `placebo.py` shows
   the instrument *can* read unpopular projects when it looks for readable ones,
   so "unmeasurable" is partly an artefact of which channels were consulted; a
   follow-up must state the channel set or it measures the instrument.
   **E039 supplies the falsifier this item asked for, and it fails.** The
   falsifier was "a population where the unmeasurable fraction is near zero".
   E039's population is exactly that for the need corpus's own threads, and in it
   the *reading* fraction is high (99.3% of needs recovered) while the *serving*
   fraction is 0 of 1391. **So a channel can read the artifact perfectly well and
   still tell you nothing about whether it serves the clause** — which is the
   sharper form of this item's worry, and it is now measured rather than argued.
   What remains open is narrower: whether an unreadable row predicts anything,
   which needs a stated channel set or it measures the instrument.
0d. **Invention item (D048), and its seat is now empty by measurement.** This entry
   holds the seat for candidate work; every other item here had been gates, CI
   diagnosis, identifier allocation or line caps (F031's complaint). E016's arm 2
   put **three needs no artifact on three corpora serves** (F035, D050) and
   **all three are now closed.** Lead 7 got its mechanism answer (E018, F038): a
   per-call mode variable is the interposition point, the stock OTel Python SDK
   ships none, and the missing piece is a feature gap rather than a candidate.
   Leads 12 and 16 were closed by F039 rather than by their mechanism answers —
   the premise underneath them, that someone else wants the same thing,
   was never measured and cannot be measured from the corpus they came from.
   **D051 supersedes D050's narrowing here: the harvest is refuted as a generator
   on a population measurement, not on a screen.**

   **A fourth closure, and the first that is not about a generator. E036 put a
   candidate in this seat and killed it against the incumbent itself** (F059,
   `EXPERIMENTS/036-search-backlog/`). The population E034 found is real,
   reproducible, per-tag, and **unreachable by no surface**: one
   `/search/advanced?tagged=…&sort=votes&order=asc` request returns it ascending,
   81 of 100 sampled ids among them, with Stack Overflow's own duplicate label in
   the same payload. **So the fourth generator question — "where does the next
   candidate come from" — is not the blocker; the ordering of the work is.**
   Three experiments harvested 1125 rows to describe a population whose *mechanism*
   was a documented query all along. **D067: test a mechanism-bearing candidate
   against its mechanism's existing source first, in about two requests, before
   measuring anything on its behalf.** F055, F058 and F059 are the same shape three
   times over — a fact about the instrument's own selection, read after the
   measurement. Applying D067 forward is the highest-information move available and
   it costs less than the cheapest experiment in this file.

   **A third generator closed in session 021, and it settles the reading rather
   than adding a candidate** (F051, D062, T-0075). Accounts seeking an
   alternative state a missing capability at 0.347 against ordinary comments'
   0.181 — and **the seek and move strata are identical at 0.347 each**, so the
   population has no "unfilled" property and this seat's premise is retired by
   measurement. **0 of 100** clause pairs recur, with κ = 0.7189 and a pair
   positive control at 20/20, so the zero comes from an instrument that works.
   **Ceiling:** 63 clauses; four channels unread by declaration. Reading in
   [`STATE-in-flight-2.md`](STATE-in-flight-2.md).

   **The third generator's closure is withdrawn as an artefact of sample size and
   stratum** (F055, `EXPERIMENTS/033-question-recurrence/`). The other two closures
   stand. Cross-author recurrence, read off Stack Exchange's own duplicate-closure
   judgement over 1000 questions, is **0.0540 CI95 [0.0416, 0.0698]** against the pooled
   0.0223 bound this item cited; **the top 60 by score contains 0 duplicate closures** and
   the rate is **4.5× higher in the bottom score tertile**. The demand-side generators are
   not closed on a fact about public conversation. **What survives is the instruction:**
   recurrence is real in public questions, and the mission's samples were drawn where it
   is rarest. **The run's one surviving result is a method result, and it produced no
   candidate**: no clause or cluster was recovered, and the closure's canonical is **not
   readable from the public API** ([`API.md`](EXPERIMENTS/033-question-recurrence/API.md)).
   Its mission-facing second claim, that repeats go unanswered, was **withdrawn as
   mechanical** — zero of the 54 duplicates has an accepted answer. **So the live question
   is *what to measure recurrence on*, and it has no measured handle yet.**
   **Ceiling:** two sites of 2024, one platform, a label that counts closures only, and no
   recovered cluster. **F053 and F054 are how the older closure got there** — one venue
   sampled five times, then a venue change that held the pooled bound at 0.0223 — and
   both runs are read in [`STATE-in-flight-2.md`](STATE-in-flight-2.md), which is also
   where F055 supersedes them. The seat's other two closures stand: the live corpus 0 of 50
   (F029), which F039
   shows was 1250 individuals each asking once rather than a sample of shared
   needs, and the recurrence hypothesis, which collapsed every cluster it was
   promised by >100× (F033) and whose person-level instrument failed its own
   controls (F039), and the departure population (F051, above). **F049 removed
   the last reason to read the need corpus as a demand-side discovery, and
   replaced it with a better description of what it is.**
   Of the 241 need-staters with a public `Show HN` item, **167 shipped it *before*
   they stated the need and only 74 after** (`EXPERIMENTS/029`, T-0073), so 69% of
   the population was never askable, and the need-to-build link bounds at CI95
   **[−0.0156, +0.1125]** (Fisher p = 0.245), consistent with zero. **F042's 0-of-24
   is confirmed on an instrument 10× larger, not refuted.** The corpus records
   needs asked *by builders*, not need waiting for one. **Ceiling:** 74 rows per arm,
   reader κ = 0.5004 against a 0.6 floor, so that arm is `not_evaluated` and is not
   raised by asking the same instrument for more. E2's lockfile claim:
   `EXPERIMENTS/009` **zero drift at ~21h**, a fast-drift null only. **Ceiling:**
   this item names
   where invention work goes; with every generator closed it names an empty seat.
   controls (F039). **Do not promote anything from this corpus.** E2's lockfile
   claim is the only live mechanism here:
   `EXPERIMENTS/009` side B, **zero drift at ~21h**, a fast-drift null only.
   **F037 adds a third negative here rather than a lead**, and F039 adds a
   fourth: this seat's question was what distinguishes a need someone has from a
   need nobody has, and what has now been measured is that the mission holds no
   instrument that answers it — the prior-art premise is unmeasurable in young
   vocabularies, and the demand corpus is one-off requests. **Ceiling:** this item
   names where invention work goes; it does not make invention happen, and with
   both generators closed it names an empty seat rather than a queue.

## Moved here 2026-10-19 — the two money-axis screens that preceded E196

Both are closed and both are kept in full because a later session reading
E196 needs to know what the keyword form was replaced by and why the
ground-truth-quality line stopped.

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
