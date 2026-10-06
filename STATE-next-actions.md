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

0. **Decide what the mission selects candidates on, now that novelty cannot be
   the filter — and the premise behind the old filter has now been counted.**
   **F044 measured it: prior art is the plurality of kill reasons, not the
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
   where this mission's candidates live. Still an **owner decision**: which axis
   replaces it (usefulness without users, distribution, domain knowledge, or
   something not yet named), and whether publishing the tooling as-is is ever on
   the table. **Ceiling:** F034's own gate is `inconclusive` — 43% of incumbents
   were undecided against a declared 20% ceiling — and its young arm rests on
   four decided rows; F027's sample is small and self-selected, and 0 stars is a
   weak proxy with known false negatives (`ripgrep`, `jq`); **F044's has one
   reader and no second coder at a one-row margin, which is the same defect E023
   fixed with κ = 0.923.** **Nothing here is
   blocked on tooling,** which is the standing reason this item stays the top
   one.
   **The four measurements that bear on this each closed a reading rather than
   opening one (F035, F037, F039, F041).** F035 measured **coverage** (3 of 12
   adjudicable kills have no prior art on any of three corpora; 4 were reachable
   only on the open web); F037 measured **composition** (the young-vocabulary
   population is **14 of 18 executable code**, so it is not documents); F039
   measured the **need corpus the survivors came from** and found **1250 distinct
   individuals**, median one comment each, with no need-level recurrence inside
   it (D051). The instrument questions are answered too: **four of six positive
   controls with demonstrated adoption returned 0 or 1 distinct author**, so the
   recurrence gate is *not evaluable*, and **the copy-count instrument read 17 of
   18 young-arm repositories and 0 of 13 placebo ones.** A lexical count cannot
   carry a claim about demand and a code index cannot carry one about unpopular
   work. **F044 then counted the kill reasons this item assumed:** a plurality
   with a one-row margin, over 20 rows rather than twelve, with 7 of the 18 dying
   of something else. Full reading in
   [`STATE-in-flight-2.md`](STATE-in-flight-2.md).

   **The third reading has been taken, and it is answered in the negative**
   (F041, D053), full account in [`STATE-in-flight.md`](STATE-in-flight.md):
   **the serving channel the prior-art screen was alleged to be blind to
   measured 0.118× the install channel**, so the screen was reading the dominant
   one and **the twelve prior-art deaths stand.** The instrument premise here was
   also wrong — a public unauthenticated API does serve the copy count — and its
   blind spot is recorded beside it: **17 of 18 young-arm repositories and 0 of
   13 placebo ones.**

   **What was left for the owner was one question, and E022 has now measured
   it.** Everything measured about supply says supply is uninformative about
   demand (F028, F032, F037). The demand-side corpus is 1250 named people who
   each wrote down, in public and unprompted, what was missing, and it had never
   been followed forward — and the question was measurable, so it was measured.

   **E022 has now measured that asset, and the answer narrows it** (F042, F043;
   numbers and reading in [`STATE-in-flight.md`](STATE-in-flight.md)). **Two** of
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

   **What E022 names and deliberately does not run:** the **589 statements that
   drew no reply at all** are the only sub-population the outcome data marks
   unserved, and their requesters did not self-serve either. That inverse filter
   needs the same two public APIs and no new instrument. **Ceiling:** it is a
   second read of a population already read twice, so it needs its own
   falsifiable claim before it is worth the API budget.

  0b. **The CI flake: deferred on purpose, not overlooked.** Three tests failed on
     identical bytes and six full suite runs did not reproduce it. T-0057 makes the
     next occurrence name itself; the unmeasured half is that `make_fleet` builds a
     bare remote plus two clones **per test class**, so fixture cost scales with the
     test count and only a 2-CPU runner shows it. **Deferred because CI is green
     and nothing is blocked on it**, and not worth displacing a research question.

   0d. **Invention item (D048), and its seat is empty by measurement.** This entry
   holds the seat for candidate work; every other item here had been gates, CI
   diagnosis, identifier allocation or line caps (F031's complaint). E016's arm 2
   put **three needs no artifact on three corpora serves** (F035, D050) — the
   first leads this mission had that did not come from its own sealed reports —
   and **all three are now closed.** Lead 7 got its mechanism answer (E018,
   F038): a per-call mode variable is the interposition point, the stock OTel
   Python SDK ships none, and the missing piece is a feature gap rather than a
   candidate. Leads 12 and 16 were closed by F039 rather than by their mechanism
   answers — the premise underneath them, that someone else wants the same thing,
   was never measured and cannot be measured from the corpus they came from.
   **D051 supersedes D050's narrowing here: the harvest is refuted as a generator
   on a population measurement, not on a screen.**

   **A third generator closed in session 021, and it settles the reading rather
   than adding a candidate** (F051, D062, T-0075). Accounts seeking an
   alternative state a missing capability at 0.347 against ordinary comments'
   0.181 — and **the seek and move strata are identical at 0.347 each**, so the
   population has no "unfilled" property and this seat's premise is retired by
   measurement. **0 of 100** clause pairs recur, with κ = 0.7189 and a pair
   positive control at 20/20, so the zero comes from an instrument that works.
   Three populations, three instruments, **no cross-author recurring requirement
   in public text**. **Ceiling:** 63 clauses; four channels unread by declaration.
   Reading in [`STATE-in-flight-2.md`](STATE-in-flight-2.md).

   **All three generators under this seat are closed, for measured reasons rather
   than a prior-art one** — the live corpus 0 of 50 (F029), which F039
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
1. **A gate must read the property it claims to check, and must be falsified
   against the defect's own bytes before it is trusted** (D025, from F013). Nine
   gates now work that way, the newest being the rule that holds a restated
   experiment number to its artifact (T-0056, D047, defect 22). Its case is the
   sharpest yet, because the **obvious rule is green on the defect**: "does this
   number occur anywhere in the artifact?" answers *yes* for `113`, which also
   sits at `patch_cost_sensitivity/*/cases`. What settles it is reading the
   number's *shape* rather than the file's contents, and the blindness of the
   rejected rule is now asserted so the restriction cannot be dropped quietly.
   Method: `docs/policy/gate-falsification.md`.
   **Ceiling:** each rule detects only the shape it was written against, and
   `resultnumbers.py`'s is one table row per experiment.
2. **The gaps in that pattern, both found by hitting them — closed, and the
   second found by reading the record rather than by a red run.** (a) **T-0036.**
   Doc-lint rule 7 read findings definitions, index rows and decision spans, and
   not the numbered list in [`STATE-defects.md`](STATE-defects.md), so two VMs
   took **defect 7** in the same hour and nothing reported it; both copies reached
   the shared base, each tree internally consistent, and the unpushed side
   renumbered by hand. `idcheck.py` is now the one entry point both publishing
   gates call, because a module wired into one gate is not thereby read by the
   other, and it reports a list it cannot read.
   **Ceiling:** a repeated number and nothing else — a dropped entry and a
   withdrawn defect are the same bytes — and there is no allocator here, so this
   is the detection half of a race it cannot prevent.
   (b) Settled by item 3, which falsified its premise.
   (c) **T-0042.** A decision number is written in three places that must agree —
   the `## Dnnn` heading, the row in [`DECISIONS.md`](DECISIONS.md), and the
   `Decisions **…**` header under each record's title — and only the first two had
   a reader. Two of five records were false while every gate passed, with both
   index rows correct throughout. `decisionheader.py` reads the third through the
   same entry point.
   **Ceiling:** identifier sets rather than wording, one line per record.
   A cheaper observation belongs here: a commit published while a **taskless**
   session is open is red on the session step — five runs in one day, every one
   green on the next commit. D027's predicate can only prove a session alive from
   a claim. `docs/operations/ci.md` now says how to recognise the case from the
   run alone; whether a taskless session should publish code commits at all is
   open.
   (d) **Closed in T-0050 (D042, F022).** `reconcile._is_vendored` reused the
   **line cap's** exemption predicate, which answers yes for every `.json`,
   `.jsonl` and `.log`, so `tests/python-versions.json` — the record that decides
   whether a VM can run the work — changed with nothing declared and nothing
   reported. Priced first by a committed script: **72 (session, path) pairs over 17
   paths**, 50 of them the ledger, so 50 closed sessions now report a file they
   cannot declare; a closed stream is not edited, so the residual is written down
   rather than discovered.
   **Ceiling:** forward-only, and `EXPERIMENTS/**/results.json` now needs an
   artifact event — 16 raw captures do.

3. **Read a red run from the annotations it already publishes** — the successor to
   2(b), and it starts by falsifying 2(b)'s premise. **Done in T-0038: the premise
   is false, and the finding is `FAILURES.md` F020.** The public check-runs API
   *does* publish annotations for a `Tests` failure — run `37178057818` at
   `687961f` carries 11 on `verify (3.12)`, nine of them failures, one naming
   `test_doctor_versions.RealRecordTest.test_this_vms_versions_are_exercised_against_the_real_records`
   at line 69 — `observed`, no rights, no token. The runs that carry none are the
   *Documentation lint* failures, whose step emits no `::error::` lines, so their
   one failure annotation says only "Process completed with exit code 2". **That
   answers most of VM 0944's claimed T-0037:** runs `37178057818` and `37179073002`
   are the already-recorded F019 on all seven rows rather than unexplained runs.
   Method: [`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md).
   **The `::error::` half is closed in T-0040, and item 4 carries what it cost.**
   **Ceiling:** the annotations are the workflow's own emission, capped at 60 lines,
   and the endpoint gives four answers of which three look like "none" — the wrong
   endpoint, the wrong sub-resource, and a 403 from the 60-requests-an-hour
   unauthenticated limit. What survives of 2(b) is the half that is real: a red
   `Documentation lint` used to name a step and nothing more, and a **red `Tests` step
   used to skip every gate step**, so which of the four answers a red run is depends on
   which step failed first. Defect 18, `FAILURES.md` F021.
4. **Closed in T-0040, and its ceiling measured rather than guessed.** All five
   file-reading steps run `tools/origin annotate`, so a violation becomes a
   check-run annotation naming the file; falsified against `e53ca23`'s real bytes
   in both directions. GitHub files an annotation on the emitted `file=`:
   `observed` on run `37191658964`, whose `Documentation lint` annotation carries
   `path: DECISIONS-RECORDS.md`, `start_line: 0`, message verbatim. What this file
   called `unmeasured` had been measured once and read wrongly (F021): the run
   quoted for it had a red `Tests` step, so every later `if:`-guarded step was
   skipped and the annotator emitted nothing. Defect 18 is the repair and
   `tools/origin probe` re-measures the rest on every run. **Ceiling:** the probe
   measures the shapes it lists, and nothing observes a `file=` value containing
   `:` or `,`, because this repository has no file whose name contains either.
5. **Identifier allocation: the allocation half is done (T-0031), the detector
   half is T-0030** (defect 5 in [`STATE-defects.md`](STATE-defects.md)).
   `tools/originlib/idalloc.py` allocates F, D and T numbers from
   `origin/<base>` plus this working tree, and every command that hands out a
   number prints the record it read. Twelve collisions between two VMs in two
   days; a stale tree no longer collides with the base, and a withdrawn task's
   number is not recycled.
   **Ceiling:** two VMs allocating between their own fetches still collide, and
   an unpushed number reserves nothing. Rule and states:
   [`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md).
6. **Fleet bookkeeping is now end to end** (T-0018, T-0032, T-0033). The records
   exist — `tests/git-versions.json` (`origin.git-versions/1`) and
   `tests/python-versions.json` (`origin.python-versions/1`) — each entry saying
   how much of the suite that version actually ran, each record naming the
   versions nobody has run, and `doctor` now reads both and reports
   `exercised` / `NOT exercised` / `record unreadable` / `no record` with the
   entry's own scope attached. A VM outside the exercised set says so at the point
   where an agent decides whether it can do the work.
   **Ceiling:** bookkeeping hygiene, not a claim about a candidate. `exercised`
   means a run happened, and nothing between 3.8 and 3.12 has ever run this
   suite.
7. **Done in T-0025** (run `37165413909`, commit `9e865a4`, six steps green,
   `observed`); superseded by item 0b's newer runs. A run says nothing about a
   second runner image or a rebase conflict.
8. **E3's line is closed** (F010 census, F012 attribution, T-0017). Timestamps
   are the only byte-level cause for the one builder available here, and
   `SOURCE_DATE_EPOCH` removes all of it. **Do not re-run either half.** Still
   open is the census's per-package heterogeneity, which this run does not
   explain. **Ceiling:** one builder, pure-Python sources, Linux.
9. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
   the prior-art condition is settled (T-0015): the algorithmic advantage is
   prior art (F009) and no tool supplies an intervention sequence for an
   existing hand-knit structure. Stage B needs an experienced knitter and
   authorization. **Ceiling:** nothing software-side remains; only usefulness
   is live, and this repository cannot measure it.
10. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
11. **E2 stays scheduled, side A snapshotted (T-0019, VM 0947), one fast-drift
   null measured.** The informative comparison is two snapshots weeks apart, so
   side A (`EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json`, 8
   artifacts: requests/six/packaging/pyparsing plus 4 pulled deps, pip 20.0.2) is
   banked with no verdict, and a same-week rerun found **zero drift at ~21h**.
   Take side B no earlier than days later and diff the closures; fast drift
   shows as a version or hash change.
12. **Do not build a product.** Nothing is selected, and the base rate for
   agent-generated ideas with prior art is high. Three candidate lines have
   returned negative results, and one (knitting) died of prior art rather than of
   measurement — which is the cheapest way to die and the one worth copying.

## Standing constraints

Moved to [`STATE-constraints.md`](STATE-constraints.md) at the 300-line cap:
they are true whichever item is next, and the rank has changed twice since they
were last true of anything.
