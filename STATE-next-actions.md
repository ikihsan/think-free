<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Next actions

Split out of [`STATE.md`](STATE.md) on 2026-10-04 at its 300-line cap. The reload
point keeps a pointer and the top item; the reasoning behind each item lives here so
a rewrite of one does not force a rewrite of the other. Read an item's ceiling before
spending effort on it: a pass still leaves prior art, usefulness and adoption
untouched, and every item says which.
## Ordered by information gained per unit of effort
0a. **CLOSED by E045 — do not run it (F081, F082, D077).** The item was to test
    `stg` against the one agent population E043 named as still open: an agent that
    must *discover* which line changed, with no line number and no `git diff`. That
    population came from E043's harness, and E045 read the demand evidence the
    candidate rests on — all 189 unique issues in E038's cached corpus, one row at a
    time — and it is **not there: 0 of 189**. The reader's own count of issues about
    choosing which lines reach the index is 29 (0.153); **28 carry explicit diff
    access, the 29th GUI-implied, none carries none**, and all ten automated callers
    in the need rows name their diff access in their own text. Three of the four
    issues F064 cites are not evidence of what they were cited for, and the classifier
    behind the record's `0.033–0.067` was re-measured at **precision 0.372, recall
    0.552** before its output was read. The same reading killed the differentiator:
    those 29 rows name **26 distinct repositories**, two of them shipped command-line
    tools taking `stg`'s coordinate (`gah`, `git-hunk`), and `git-hunk` has already
    run the two-arm agent experiment this item was built around. Evidence in
    [`EXPERIMENTS/045-demand-evidence/README.md`](EXPERIMENTS/045-demand-evidence/README.md);
    reading in [`STATE-in-flight-7.md`](STATE-in-flight-7.md).
0f. **The one live action, and it is a fact to establish, not a screen: is the
    partial-stage-sweeping behaviour real in the shipped hook tools?** Two of
    E045's 29 need rows are about something none of `stg`, `gah` or `git-hunk`
    addresses — **a formatter or lint hook that re-stages a whole file and sweeps a
    partially-staged file's unstaged hunks into the commit.**
    `nextjs-app-template#95` states that the warning its own `lefthook.yml` carries
    is **false**; `agent-orchestra#154` is the same class of bug in a pre-commit
    hook that re-staged a reformatted file whole. That is a correctness failure
    with a byte-level oracle — `.git/index` before and after the hook — and it is
    **checkable by reading and running `lefthook` and `pre-commit`**, not by a
    screen. Declared now, before the run: it is established if, on a repository
    with one partially staged file and one hook that reformats a different
    unstaged file in the same run, the unstaged hunks of the first end up in the
    index; it is refuted if `lefthook`'s `stage_fixed` and `pre-commit`'s
    unstaged-restoration both provably preserve them. **Two rows is not evidence for
    a candidate and none is promoted here** — a promotion needs the mechanism
    confirmed and then D067's prior-art check against both tools' own sources,
    which the check below gets for free.
    **Ceiling:** two issues in two personal repositories, both closed, one of them
    asserting a false statement about its own config file. If the behaviour is
    confirmed, the next thing it needs is D075's limitations-section measurement and
    D067's existing-source check, in that order.
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
Split out of [`STATE.md`](STATE.md) on 2026-10-04, which was at 299 of the 300
permitted lines and had to grow. The reload point keeps a pointer and the top
item; the reasoning behind each item lives here so that a rewrite of one does
not force a rewrite of the other.
**Two siblings, by invariant rather than by size.** The standing constraints —
rules true whichever item is next — moved to
[`STATE-constraints.md`](STATE-constraints.md) on 2026-10-04. **Item 0, the owner
decision on what the mission selects candidates on, moved to
[`STATE-selection.md`](STATE-selection.md) on 2026-10-06** when it reached 168
lines: it is not work, no experiment here can settle it, and its presence in a
ranked work list invited it to be worked on.
Read the ceiling on an item before spending effort on it: a pass still leaves
prior art, usefulness and adoption untouched, and every item says which.
0. **Decide what the mission selects candidates on — an owner decision, and
   it is no longer a work item.** The full reasoning, the four measurements that
   bear on it, and the ceilings on each are in
   [`STATE-selection.md`](STATE-selection.md), where it was moved on 2026-10-06
   because it had reached 168 of this file's 300 permitted lines and is not work:
   no experiment in this repository can settle it. **Short version:** novelty cannot
   be the filter, because the screen's premise has now been measured on four axes
   and all four came out against it (F034 soundness, F035 coverage, F037
   composition, F060 demand side). Neither is prior art nor star-shaped adoption
   nor harvested recurrence able to carry the choice. **E039 closed the last
   proposal:** the axis "did they use the thing?" has no channel, because 1 of 794
   requesters replied again. What remains is the owner's.
   **Ceiling:** this entry points at the decision; it does not make it.
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

Items 3–12 — every closed, done, or standing "do not" entry, with the derivations
that made the ranked list too long to read — moved to
[`STATE-next-actions-closed.md`](STATE-next-actions-closed.md) on 2026-10-06 at
the 300-line cap. Read it when re-running a closed item looks tempting.

## Standing constraints

Moved to [`STATE-constraints.md`](STATE-constraints.md) at the 300-line cap:
they are true whichever item is next, and the rank has changed twice since they
were last true of anything.
