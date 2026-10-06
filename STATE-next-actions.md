<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Next actions and standing constraints

Split out of [`STATE.md`](STATE.md) on 2026-10-04 at its 300-line cap. The reload
point keeps a pointer and the top item; the reasoning behind each item lives here so
a rewrite of one does not force a rewrite of the other. Read an item's ceiling before
spending effort on it: a pass still leaves prior art, usefulness and adoption
untouched, and every item says which.

## Ordered by information gained per unit of effort

0. **Decide what the mission selects candidates on, now that neither novelty nor
   harvested recurrence can be the filter.**
   **F044 measured the premise behind the old one: prior art is the plurality of
   kill reasons, not the
   majority — 10 of 18 = 0.556, a one-row margin, and every prior-art row moved
   to another category kills the majority reading. The population is 20 rows, not
   the twelve this item previously carried, and 7 of the 18 died of something
   else** (a falsified mechanism, a claim no observation could establish, one
   promoted then parked). So the diagnosis this item was built on is *narrower and
   less certain than stated*: novelty is the largest single kill reason, not the
   whole story, and a second option now has a count behind it — **promote fewer
   claims, and price each one's gate before promoting it**, which is what F006's
   A1 shows is available at report time. `tools/origin` remains the prior-art
   death the record treats as the twelfth (`RESEARCH/PRIOR-ART-ORIGIN.md`, F026,
   F027). F034 measures the prior-art verdict's premise on the population that
   screen consulted: **4 of 4 on-topic incumbents in mature vocabularies are
   served, 1 of 4 in a young one** — sound where it is least load-bearing, unsound
   where this mission's candidates live. **F055 removes the other filter this item
   carried**: the pooled recurrence bound of 0.0223 is refuted (0.0540 measured, CI95
   [0.0416, 0.0698]) and the five zeros were a stratum effect. Still an **owner
   decision**: which axis replaces them — usefulness without users, distribution,
   domain knowledge, **or the convergent-and-unanswered population F055 measured (a repeat
   is F055's withdrawn claim that repeats go unanswered)** — and whether publishing
   the tooling as-is is ever on the table. **Ceiling:** F034's own gate is
   `inconclusive` — 43% of incumbents were undecided against a declared 20% ceiling — on
   four decided young rows; F027's sample is small and self-selected, and 0 stars is a weak
   proxy with known false negatives (`ripgrep`, `jq`); **F044's has one reader and no
   second coder at a one-row margin, which is the same defect E023 fixed with κ = 0.923;
   F055's population is two sites on one platform and recovers no cluster.**
   **Nothing here is blocked on tooling,** which is the standing reason this item stays
   the top one.
   **Six measurements bear on this; five closed a reading and the sixth (F055) refuted
   the filter this item rested on.** **Coverage:** 3 of 12
   adjudicable kills have no prior art on any of three corpora, and 4 were
   reachable only on the open web. **Composition:** the young-vocabulary
   population is **14 of 18 executable code**, not documents. **The need corpus
   the survivors came from:** **1250 distinct individuals**, median one comment
   each, with no need-level recurrence inside it (D051), from **four of six**
   positive controls with demonstrated adoption returning 0 or 1 distinct author,
   so the recurrence gate was *not evaluable*. **Distribution:** the serving
   channel the screen was alleged to be blind to measured **0.118× the install
   channel**, so **the twelve prior-art deaths stand** (F041, D053); its
   instrument premise was also wrong, since a public unauthenticated API does
   serve the copy count, and it read **17 of 18** young-arm repositories against
   **0 of 13** placebos. **And this item's premise:** F044 counted a
   plurality with a one-row margin over 20 rows, with 7 of the 18 dying of
   something else, and F055 refuted the 0.0223 recurrence bound beside it. A lexical
   count cannot carry a claim about demand and a code
   index cannot carry one about unpopular work. Full reading in
   [`STATE-in-flight-2.md`](STATE-in-flight-2.md) and
   [`STATE-in-flight.md`](STATE-in-flight.md).

   **What was left for the owner was one question, and E022 has now measured it.**
   Everything measured about supply says supply is uninformative about demand (F028,
   F032, F037). The demand-side corpus is 1250 named people who each wrote down, in public
   and unprompted, what was missing, and it had never been followed forward.

   **E022 measured that asset and the answer narrows it** (F042, F043; numbers and reading
   in [`STATE-in-flight.md`](STATE-in-flight.md)). **Two** of
   its three numbers decide this item: **58.0% of 1401 stated needs drew a reply;
   and of the 24 whose need went unserved, 0 built it themselves.** The third —
   "38.5% named something serving the need" — **is withdrawn** (F043, D055): it had
   **no control**, and the control now run reads **0.368** against the need arm's
   0.395, so it is the base rate of a Hacker News conversation. The asset is **not**
   a population of unmet needs awaiting a builder. *"Need-staters are not builders"*
   is **false as an absolute** (F045, D057): **22.2%** of the 1250 have publicly
   shipped something against **27.8%** for ordinary commenters in the same stories,
   ratio **0.80×**. So they are a fifth builders who build **less** than their
   neighbours, and the rate at which they build **what they asked for** is
   unchanged at a 0-of-24 floor. **Item 0d's closure of this corpus is now measured
   rather than assumed.**

   **A second result is about the instrument that drew the corpus** (gate A2
   fired as declared before the first fetch): **carrying a trigger phrase does
   not mark a comment a thread answers**, lift 0.703 against a floor of 1.0. Its
   interval spans 1.0, so "answered less" is not established. F039 showed the
   corpus is 1250 people each asking once; **E022 shows the phrase that found
   them does not mark the comments that get answered.**

   **Those two cells bound every outcome read from a trigger-harvested corpus,
   E022's included** (F043, D055): a trigger vocabulary finds people who state
   needs and is **invisible to what happens to those needs afterwards**. Two
   readers on the same 39 rows agree at **κ = 0.923**.

   **E022 named the 589 never-answered statements as the only sub-population the
   outcome data marks unserved, and both have since been read** (T-0069, T-0070):
   58.0% answered, 0 of 24 unserved requesters built it, and 167 of the 241 who
   shipped anything shipped **before** they complained (F042, F049).

 0e. **The seat is no longer empty: E034 put a candidate in it and could not read two
     thirds of it** (`EXPERIMENTS/034-reask-tail`, F057, D063/D064, T-0078). Three
     matched arms of eight pre-named tags on one route, labelled by Stack Exchange's own
     `closed_reason`, with the **`Active` tab as the control** — the ordering a person
     browsing the tag actually sees. Pooled duplicate-closure rate **0.1352 in the score
     tail against 0.0303 in the Active tab**, 4.5×, on equal denominators too, which
     **replicates F055's whole-site gradient on an independent tag-stratified population**.
     **The rate is a per-tag property nothing in this record had measured**: ten tags span
     **0.0000 to 0.4300**, seven clear n ≥ 50, **12 pairs have disjoint intervals**, and
     both extremes reproduce on the next four pages (`customs` 0.430→0.495,
     `excel-formula` 0.000→0.000) from 43 distinct askers over 28 months. **The Active
     tab shows none of it**: it reads 0.02 where the tail reads 0.43 for `customs`, and
     0.03 where the tail reads 0.00 for `excel-formula`.

     **Two of the three claims that would make it a diagnostic failed, and that is what
     the next action is.** **D6:** duplicate closure is a **moderator act**, the declared
     population had one `travel` tag against five `stackoverflow` ones, and after
     AMENDMENT-1 added `travel`/`baggage` (0.1979) and `math`/`calculus` (0.1020),
     **within-site tag pairs separate 4/10 against 14/26 cross-site** — site and tag both
     carry real variance and 3–5 tags per site cannot apportion them, so the **per-tag
     reading is `not_established`** even though its kill gate fired. **B1:** among
     duplicates, the share with no accepted answer is 0.8163 in the tail against 0.7273 in
     the Active tab, difference **CI95 [−0.0774, +0.3075]**, so *"the answer existed and
     was not found"* cannot be separated from *"a moderator closed it"*. The a-priori
     stratum hypothesis is **backwards** — the situational exemplar has the lowest rate of
     all ten tags. **What is established is where the repeats sit, not what happened to
     them**, and that is still the first demand-side instrument in this record to return
     positives at all. **D064** governs the decision rule that failed to be exclusive,
     **D063** the ten-literal label that makes E033's 0.0540 a floor.

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


Items 3–12 — every closed, done, or standing "do not" entry, with the derivations
that made the ranked list too long to read — moved to
[`STATE-next-actions-closed.md`](STATE-next-actions-closed.md) on 2026-10-06 at
the 300-line cap. Read it when re-running a closed item looks tempting.

## Standing constraints

Moved to [`STATE-constraints.md`](STATE-constraints.md) at the 300-line cap:
they are true whichever item is next, and the rank has changed twice since they
were last true of anything.
