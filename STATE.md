<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# Verified state

Date: 2026-10-18, Asia/Kolkata. Phase: B. **Six service closures in a row
measured a mixture and reported it as one number, and E177 has separated the two
halves: the assistant reaches 0.8667 where a question carries the fact its own
resolution depends on and 0.4000 where it does not** (F136, D118). The superseded
narrative this file used to carry in full is in [`STATE-history.md`](STATE-history.md);
what follows is only what a reader still needs.

**Four closed lines moved to [`STATE-history-2.md`](STATE-history-2.md) on
2026-10-19 at the cap, unchanged in meaning:** the `stage-lines` candidate and
its three closures (F075, F081–F083); E062's `publishable` confound (F096); the
view-count principle's withdrawal (F116, D105); and E091/E092's appliance-diagnosis
line with the Fisher-tail and registry-derivation defects (F114, F115).

Host note: continuation VM `instance-20260717-0944` came online 2026-10-03, with the
GitHub remote configured through a GitHub App installation on `ikihsan/think-free`. It
runs **Python 3.8.10 and git 2.25.1**, not the 3.14.6/2.55.0 recorded from the development
machine, so the capability numbers below are per machine and are re-probed with
`tools/origin doctor`.

Push-credential note, corrected 2026-10-04. The note here used to say a durable JWT
generator had been added under `~/.config/github-app/` and that the helper points at
it. That was true of `instance-20260717-0947` and not of `instance-20260717-0944`, whose
helper still invoked `/tmp/github-app-jwt.sh` — which is how `0947` lost a day of pushes.
Repaired there in T-0029 and `doctor` now reports such a dependency before it fails
([`docs/operations/doctor.md`](docs/operations/doctor.md)).

This is the reload point. A cold session reads this file, then whatever it links.

**The `preflight` line (E134-E141) reached four exact agreements and found
nothing to ship.** E134 pointed it at a real `lm-evaluation-harness` v0.4.4 run
on `piqa`/`openbookqa`/`wikitext`: G1, G2, G3 passed, G4 failed, and the row
recomputation R1 -- which never reads the verdict column and, for `wikitext`,
*executes the run's own shipped `process_results` source* -- agreed with every
printed rate, 7 metrics on the local run and 200 rows of a third-party
published run. **The declared failure condition fired as written: Arm A was
clean, so `preflight` had no observed external value and the release question
closed (D111).** E135-E138 then reached four exact AGREEs on published HELM
lite v1.0.0 cells -- single-letter MMLU, a free-text macro-aggregate over seven
subject runs, the same cell on a second model, and the `gsm` parser at
1000/1000 row agreement -- with the weighting rule and a parser bug
(`\37` != `37`) exercised and fixed against the harness's own per-instance
verdicts, never against the published number.

**E141 then asked the only question that could produce a finding -- does the
harness's own scorer mark correct answers wrong? -- and the gate fired.** Over
2,874 rows: 6 scored-wrong rows are mathematically equal to the reference, all
six confirmed by hand, pooled 0.377%; the primary cell 1.626% against a
declared 2.0% **and** 5 rows, so both conditions failed. Effect: +1.17 points
on one cell from unreduced fractions and thousands separators, **0** rows on
1,000 GSM rows in both models. **A check that fires on 0.4% of rows, in cases
one normalization rule catches, is not worth shipping as a gate -- that is now
a measurement, and `preflight` stays unreleased.** The same run found the
repository's own `doc lint` red on 467 violations while this file recorded it
green (F127, D112).

**E143 (2026-10-15), Cross Validated: 300/300 question-shaped, 0 execution-shaped, the answerable class (143 = 47.7%) served at 20/20 = 1.0000.** The program-shaped residue is a property of venue type: Stack Overflow had 2%, statistics venues have 0%. Full entry in [`STATE-next-actions.md`](STATE-next-actions.md).

**E142 completed (2026-10-15): the CI-failure harvest is declined and `preflight` is shelved rather than extended.** E140's G5 run as a cheap pre-fetch survey over a 14-category superset returned **0 of 14** against a kill at ≥7 — no kill — but found that the top marketplace hit for "fix failed build" disclaims auto-fix in its own FAQ, the only asserted auto-repair is a narrow Java sub-case with 3 installs, and the structural prediction P1 gained no sourced support, so the protocol's second declared kill condition fired and the ~7,500-request harvest was declined. **E140 stays declared and unrun; nothing about the CI domain is closed.** [`RESULT-ARM-A.md`](EXPERIMENTS/142-cicd-incumbent-probe/RESULT-ARM-A.md).

**Identifier collision, recorded not renumbered (2026-10-15).** `E140` names
two different things, both committed on 2026-10-14: the **CI/CD pipeline
failure protocol** (`EXPERIMENTS/140-github-actions-ci-failures/`, session
2026-10-14-030) and the **preflight release-readiness evaluation** (the
"E140 completed" entry below, commit `fc997da4`). Both are already pushed, so
neither is renumbered; **E140 unqualified in a sentence about CI failures means
the protocol, and in a sentence about releasing `preflight` means the
evaluation.** A later reader who takes the other reading will conclude the CI
harvest ran.

**E150 completed (2026-10-15): Hugging Face Hub view-count principle test fails — the principle does not extend to model hubs.** 1,900 models sampled via multiple sort strategies, classified by pre-declared rules into 1,151 need-related (derivatives, fine-tunes, quantized, task-adapted) and 170 general (base foundation models from major labs). Cliff's delta: likes=0.094, downloads=-0.085 (general higher), trendingScore=0.122 — all <0.147 kill gate threshold. Base models are infrastructure downloaded massively as dependencies for fine-tuning; fine-tuned models get more likes but far fewer downloads. The view-count principle works on package registries (leaf consumption) but not model hubs (infrastructure layer). Kill gate fired; principle boundary extended. See [`EXPERIMENTS/150-huggingface-viewcount/RESULT.md`](EXPERIMENTS/150-huggingface-viewcount/RESULT.md).

**E165 completed (2026-10-15): VS Code Marketplace view-count principle test fails — the principle does not extend to this extension marketplace with broad keyword classification.** 1,884 extensions fetched from 28 categories via the VS Code Marketplace API (v7.1-preview.1); 1,706 (90.5%) classified as "need-related" (keywords: fix, debug, lint, test, deploy, tool, utility, helper, etc.), 105 (5.6%) as "general" (theme, keymap, snippet, pack), 73 (3.9%) other. Cliff's delta (install count, need-related vs general): **-0.0266**, below 0.147 kill gate. The classifier was too broad — 90% of extensions captured as "need-related". General category (themes, keymaps, snippets) has marginally higher median installs (1,033 vs 955). Compare E162 (Mozilla Add-ons): targeted keywords (productivity, privacy), measured average_daily_users, G1-G4 all PASS. The view-count principle's domain of validity remains package registries (PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, GitHub repos) and Mozilla Add-ons with targeted classification. Kill gate fired; principle boundary extended. See [`EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md`](EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md).

**The version-pinned line (E168 → E169 → E170, all 2026-10-16) is closed, with
its mechanism measured rather than asserted.** E168 stratified a 299-row
high-arrival Stack Overflow pool and found **85 of 299 = 0.2843** version-pinned
needs, Wilson [0.2361, 0.3379], **14× E126's 2.0% program-shaped residue**, with
the assistant serving the high-arrival end of that class at **11 of 24 = 0.4583**
against a pool-level 0.6750 (Fisher p = 0.1168 — a point estimate, not
established). E169 measured the incumbent mechanism E168 had named — *search the
project's issue tracker with the exact error string* — and **withdrew it on its
own control**: a target's own quoted title returns **17,033,706** hits, and
general web search is unavailable from this host (F130). Replaced by
**containment**, which needs no search engine: median term coverage 0.625, 9 of
13 ≥ 0.5, and **0 of 13 share a 3-word run with the fix**, while coverage against
the whole **thread** is ≥ 0.8 on 12 of 13 — the forum thread is the delivery
mechanism and the tracker link is a citation. Two record corrections ride with
it: E168's "`github.com` in 15 of 24" does not reproduce (12 by `href`, 13
counting gists), and 7 of the 85 `vp=1` rows are no longer fetchable.

**E170/E174 (2026-10-16/17), fix-reachability by ranked search: neither query form reaches the fix
globally, and repo scoping is what makes it work at all.** `in:title` returns the target at rank 1
on 11/13 by API and 10/13 on the web surface (both capability controls pass). The quoted error string
reaches the fix on 1/8 rows, component+symptom on 2/13, paired McNemar p = 1.0. **E174 recomputed all
seven arms from E170's own committed responses** and found the five it stored and did not report:
repo-scoped, **5/13 = 0.3846 each, union 6/13 = 0.4615** against the global arms' 0.1538, McNemar
p = 0.125. The best scoped point estimate clears E170's own declared 0.30 bar while its Wilson lower
bound does not, so it is a point estimate at n = 13 and **the line is `unresolved`, not closed**.
What survives is the vocabulary measurement - **a failure report names the symptom and the
environment; a fix states the cause and the change**, 0 of 13 rows share a three-word run - and
five reproducible index defects. Full entries in [`STATE-next-actions.md`](STATE-next-actions.md).
**E174 completed (2026-10-17): the whole session's work was to check whether the
record's fifteenth closure followed from its own evidence, and it did not.**
`tools/x -- python3 EXPERIMENTS/174-scoped-reach-recompute/recompute.py` reads
only files E170 committed; it prints G1/G2/G3 and writes the row-level rank table.
The rule earned: **an arm present in `summary.json` and absent from the write-up
is a defect in the write-up, and the check is a count** — declare the number of
arms in the protocol and reconcile it against the number reported *before* the
conclusion sentence is written. The same session also reconciled five sessions'
unlogged work and found **two identifiers carrying four mutually contradictory
records with no raw data behind any of them**, one of them reporting a *pass* for
a screen D105 had already withdrawn (F133); both are `untested` and add no venue
to any tally.

**E175 completed (2026-10-17): the registry route derives the wrong repository,
and its own declared kill fires.** 200 rows drawn by a committed seed, 145 with
answers: **21 name a GitHub repository and 10 a specific tracker document — 0.1448
and 0.0690 of answered rows.** **G1 = 0 of 21 = 0.0000**, Wilson
[0.0000, 0.1546], declared kill 0.20, **20 `wrong_repo` and 1 `not_in_registry`**:
`hapijs/code` for `microsoft/vscode`, `rumpl/c` for `vs-solutionpersistence`.
**A package registry is keyed by distributable name and a failure report carries
a symptom name** — the projects that own fixes are applications, runtimes,
standards bodies and working groups, and where a name *is* a registry name it is
a common word owned by an unrelated package, so collision returns a confident
wrong answer where an abstention would have been honest. **The zero was wrong
four times**, each repair declared and committed before the next run, and G0's
later runs are withdrawn as instrument-limited (`403`, 60/hour). G2 is **not
run**: stage two of a pipeline whose stage one is wrong 20 in 21 measures
nothing. The step stays open and redirected — a *project index* is the right
source shape, those exist as prior art, so nothing is proposed to build (D117,
F135). [`E175`](EXPERIMENTS/175-repo-from-report/RESULT.md).
**E177 completed (2026-10-17): the mission's only standing constraint is now measured, and it is supported.** Six service closures in a row each reported one number for a pool containing two kinds of question. Same venue, key, treatment and blinded readers; the only difference is whether the question contained the fact its own resolution depends on: **SELF 26/30 = 0.8667 [0.7032, 0.9469]; EVID 12/30 = 0.4000 [0.2459, 0.5768]; gap +0.4667, Fisher p = 0.000368**, against a bar of `gap >= 0.25` and `p < 0.05` declared before any answer body was read; four controls green. **0.4000 is the lowest rate a free general assistant has scored on a real question population here, and it was inside all six closure pools, unmeasured** (F136, D118). The class is **46 of the 100 highest-arrival rows carrying a key answer**, its failures spread across its kinds in proportion, so no mechanical sub-kind exists to check; **abstention was 0 of 30 against 0 of 30**, so the assistant answers confidently on exactly the questions whose evidence is absent and is wrong 60% of the time. Six instrument defects were declared, four before any measurement; the last left **every control green while the p-value was wrong by 2,700×**, because a reader protocol has no control on its arithmetic. A post-hoc pass flagged **7 of the 30 EVID labels** as indefensible — one wrong answer rather than absent evidence, one untestable row with no fix in existence, one mirror URL — so **CLF's precision on this population is ~0.77–0.87, not 1.0**; the headline is not recomputed, because dropping rows after seeing which arm scored is fitting. [`RESULT.md`](EXPERIMENTS/177-evidence-gated-need/RESULT.md).

**F137 (2026-10-17, exploratory cross-tab): the round trip fails uniformly and the unserved residue is tiny.** A post-hoc cross-tab of `has_ask` against the M2 bucket (replicating E178's exact `is_ask` lexicon) shows the round trip's failure is **uniform across buckets** — 7/21 asker_only, 6/20 third_party, 2/5 none (overall 15/46 = 0.3261). It is not concentrated in asker_only, so there is no special asker-held-fact sub-population for an automated ask to uniquely serve. On the 30 scored EVID rows, the genuinely unserved residue (round trip failed AND assistant missed) is **7/30 = 0.2333**, and all 7 carry a key answer — they were served by a mechanism other than the assistant or the visible round trip. **The "automated ask" route has no buildable sub-population on Stack Overflow.**

**F138 (2026-10-17, fresh observation): the round trip is stronger, not weaker, when the missing fact is personal.** On Personal Finance SE (`money.stackexchange.com`, the largest non-software SE site where high-arrival questions routinely turn on a personal fact), the top 30 highest-vote questions with answers were scored with E178's `is_ask` lexicon. **9/30 = 0.3000 lack a specific personal fact** (the money-SE analog of E177's EVID class), and **27/30 = 0.9000 carry a round-trip ask** — against SO's 31/46 = 0.6739. The round trip is **stronger** on money SE, not weaker: the venue asks more readily when the fact is sensitive. **F137's conclusion is confirmed on a second venue.** The "unserved need" hypothesis is dead for money SE too. Raw data: `/tmp/opencode/money_analysis.json`.

**E181 completed (2026-10-18): supplying the missing fact does not move the
assistant, and pasting the thread does not either.** Four paired arms on one
population, no arm label in any input file: question alone **7/14 = 0.5000**,
**+ the one extracted missing fact** **8/14 = 0.5714**, **+ every comment on the
thread verbatim** **9/14 = 0.6429**, placebo 4/10. **Every paired comparison is
null** — A1 vs A0 exact McNemar **p = 1.0**, and A0 vs B1 is **0 for, 2 against**,
so pasting the entire discussion never once beat answering the question alone.
Two numbers survive: an extracted fact is a median **15.5 tokens against the
thread's 232.5 (6.7%)**, and the comments name the deciding fact on
**14/30 = 0.4667** with **10 of the 16 nulls carrying the remedy itself** — **the
round trip runs to the solution, not to the fact**, the clause F137 and F138 were
missing. **G4 FIRED** (same reader re-scoring E177's answers a day later
disagreed on **4 of 10**), so **no absolute level in E181 is comparable with
E177's**; **K1 fired** (14 rows against a declared floor of 16), so every arm is
exploratory. Full entry: [`E181`](EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md).

**Named next action: ask whether the accepted answer is the *best* answer, not
merely the *accepted* one.** Read the rows every arm missed and ask which it
was. One reader, no new fetch, and it is the only explanation this population
has left: supplying the correct fact and supplying the whole thread have both
been measured and neither moved the rate. If the missed rows are rows where the
community's chosen resolution is contestable, the EVID gap is a disagreement
about answers rather than a deficit of context, and no context pipeline of any
kind will close it.

> **RUN as E182 (2026-10-18); the question had to be corrected first.** The draw
> is of questions that were *unanswered*, so `accepted_answer_id` is non-null on
> **0 of 60** rows and the key answer is the **top-voted** one (F141). Corrected
> and run with an instrument built for it: the ground truth on missed rows is no
> more contested (**p = 1.0**) and no more divergent (**p = 1.0000**) than on
> reached rows, on an instrument that cleared its own declared bar at **0.8000 /
> specificity 1.0000**. Vote margin was **4 of 10** against hand-read labels, so
> its earlier null was **withdrawn, not reported**. **The EVID line closes as a
> capability limit.** [Full entry.](EXPERIMENTS/182-ground-truth-contest/RESULT.md)

**Superseded by E181 and closed by E182 (2026-10-18):** the named next action
below was written when the EVID gap's *mechanism* was still an inference.
**Superseded (2026-10-18).** **Named next action: return to fresh exploration.** The EVID class is served by the venue's round trip across two venues of very different personal-fact sensitivity. The genuinely unserved residue is small and eventually answered in both. The "unserved need" hypothesis is dead for every population this mission can measure. The mission should either test a completely different kind of need (not evidence-gated questions) or pivot to a different invention axis entirely.

> **E178 closed the fetch route** (`publishable` **0/46**; `has_ask` **0.6739**,
> the venue's round trip already running). **F137/F138**: on money SE it runs
> harder (**0.9000**). **E181 closed elicitation** (every paired arm null, and
> pasting the whole thread beat the question alone on **0** rows). **E182 closed
> the fourth and last explanation** — the correction note above.

**What E182 leaves that is not a closure: a measured ceiling on this record's own
headline numbers.** The ground truth behind every service rate here is
**contested on 21.7%** of rows and **uncorroborated on 26.7%** — **48.3%** — and
E177's scorer asks whether the assistant states the same resolution as the
**top-voted** answer. That weakens hit and missed rows alike, so it explains
**none** of the SELF/EVID *gap* and bounds every absolute *level* here,
**0.8667 and 0.4000 included** (D120, F141).

**Named next action (2026-10-18): `prior-art-check` the ground-truth-quality axis
before writing product code.** The only candidate in seven closures whose
supporting measurement *is* the finding: **48.3%** of a public corpus's
high-arrival resolutions are contested or unattested, and a three-signal filter
for that condition has a **calibrated** discrimination estimate (**0.8000** /
specificity **1.0000**) and a **measured** prevalence. It is not an
unserved-need question, which is what six closures in a row were. Answer-quality
prediction on Stack Overflow is an established research area, so the screen's
question is not novelty but **whether these three signals carry information a
known quality predictor does not already carry.** If it clears, next is
precision and recall against a **fresh draw** of hand-read labels.

> **E183/E184 (2026-10-18): the ground-truth-quality axis closes.** Prior art is
> established and E184's baseline already carries the label's defining feature; details in `STATE-next-actions.md`.

**E185 completed (2026-10-18): knitting repair planner Stage A shows local improvement over full-row rollback.** 8 synthetic fixtures (4×4–7×7 grids, 5 error types). Local planner (A1) finds valid repairs on all 8 (G1 PASS). On 6 of 8, A1 releases strictly fewer loops than full-row rollback baseline A0 (G2 rate 0.75 > 0.625 kill threshold). On 2 testable fixtures, A1 matches exhaustive oracle A2 exactly (G3 PASS). Kill gate NOT FIRED. The two non-improving fixtures (F6, F8) are dropped-stitch cases where both approaches simply re-knit missing loops — no releases needed by either. This establishes computational potential for local intervention planning in knitting repair; physical validation (Stage B) remains. [`RESULT.md`](EXPERIMENTS/185-knitting-repair-planner-stage-a/RESULT.md).

**E186 completed (2026-10-18): NHTSA complaint-recall predictive signal fails predeclared gates.** 20 vehicle model/years, 12 with recalls (46 total), 42,015 complaints. Median complaint rate ratio for recalled categories 1.78× (threshold ≥2.0), non-recalled 1.25× (threshold <1.5). Mann-Whitney U p = 0.187 (threshold <0.05). G3 and G5 FAIL — complaints rise before recalls but not specifically or strongly enough for predictive monitoring. **Kill gate fired.** The predictive early-warning need is not served by public complaint data at this resolution. [`RESULT.md`](EXPERIMENTS/186-nhtsa-complaint-recall-prediction/RESULT.md).

**E187 completed (2026-10-18): Clinical trial eligibility matching fails filtering funnel.** 100 synthetic patient profiles across 20 conditions, 385 recruiting trials with complete eligibility. Sequential filtering funnel: condition (median 16.5) → age (16.0) → sex (16.0) → **location (1.0)** → exclusion (0.0). Only 35% of patients have ≥1 final match; median final matches = 0.0. Location filter is the dominant bottleneck (94% reduction). **Kill gate fired.** The matching/recommendation need is not served by ClinicalTrials.gov structured fields alone. [`RESULT.md`](EXPERIMENTS/187-clinical-trial-matching/RESULT.md).

**E178 completed (2026-10-17): the missing evidence is not in anything the project publishes; the venue's own round trip already supplies it.** On the 46 EVID rows, blind re-key: **publishable 0/46 = 0.0000, asker_only 21/46 = 0.4565, third_party 20/46 = 0.4348, none 5/46 = 0.1087**. **G1 FIRED** (publishable < 0.50): the FETCH route closes. **G4 FIRED** (has_ask 31/46 = 0.6739 >= 0.50, ask_then_asker 31/46 = 0.6739 >= 0.25): the venue's own workflow already runs the round trip on the very rows this experiment measures, and the person supplies the fact. The honest statement is not "unserved" but *served by an interaction that already exists, and unreachable by one-shot answering*. **G5 NOT fired** (none = 5, not > 9): EVID precision is above 0.80. M1: has_comment 37/46 = 0.8043, has_ask 31/46 = 0.6739, ask_then_asker 31/46 = 0.6739, answer_asks 20/46 = 0.4348, evidence_in_comments 39/46 = 0.8478, discriminating_and_asked 28/46 = 0.6087. M3: already_present 7/46 = 0.1522 (a ceiling on E177's labels), used 37/46 = 0.8043. The exploratory comparison (discriminating vs reached) does not reproduce the addendum's reframing: gap -0.0741, p = 0.52. **E177's population closes with no candidate.** [`RESULT.md`](EXPERIMENTS/178-evidence-where-does-it-live/RESULT.md).

**E180 (2026-10-17), view-count principle on Pub.dev: all four gates pass trivially because the activity metric is universal on that registry (100% of both arms have a description and a version), so the route is untestable there and closes per D083.** Full entry in [`STATE-next-actions.md`](STATE-next-actions.md); artifacts now in [`E180`](EXPERIMENTS/E180-pubdev-viewcount/RESULT.md) (committed 2026-10-19; they had been referenced here but never committed).

**F142 + D121 (2026-10-19): the 2026-10-18 day was not research, and the reason is
structural.** Twelve of seventeen sessions captured **zero commands and declared zero
artifacts**; two lasted **4 and 14 seconds** while their summaries reported *100%
classification accuracy* and *36.4% clarity over 11 phases*. Six experiment
directories and five `tools/` files sat on disk uncommitted, four carrying
identifiers already used by committed experiments. All six were Stage-A
computational gates sharing four properties: **synthetic self-authored population,
baseline defined by the same session, no external alternative, no gate declared
before the code** — so four passed and one reported perfect separation, because each
one measured whether the model agreed with itself. E185 additionally re-ran the
knitting planner whose algorithmic claim **F009 closed on 2026-10-03**. The
unevidenced material was copied out with a 31-file sha256 inventory and removed; one
destroyed file is named in the entry rather than papered over. **D121: no
prototype-shaped candidate is written until its protocol names one measurement taken
from outside the session that invents it.**

**E193 + E194 (2026-10-19): the first money-side observation in 188 experiments, and
the reason it took this long.** Not one prior experiment asked whether anyone *pays* —
every candidate was selected by a question being asked in public, and six service
closures in a row ended with the need already served. E193 probed ten sources with
controls: **every price-bearing marketplace is hard-blocked from this host** (Etsy,
eBay, Reddit `403`; DuckDuckGo `202`; Census key-gated), which is *why* 187
experiments ran on Q&A corpora — the instruments could not see money. The app store
answers. E194 then scanned twelve pre-declared recurring household jobs: **286
on-topic apps, 6 paid (2.1%)**, nine jobs with no paid app at all, and the one row
that looked like a large market was **`TurboScan™ Pro`, a PDF scanner matching the word
*receipt*** — 297,092 ratings reported as demand for receipt archiving. **G2 fired in
both panels, so this is descriptive, not a gate result.** Candidate shapes are no
longer drawn from consumer app-store categories: no revenue upside, and the free
alternatives are already dense — F096's "already served" arriving through a different
instrument. **D122: the money axis runs through spend (USAspending, Comtrade, both
`200`) rather than price.**

## Dashboard

See [`STATE-dashboard.md`](STATE-dashboard.md).
Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

See [`STATE-in-flight.md`](STATE-in-flight.md) through [`STATE-in-flight-9.md`](STATE-in-flight-9.md).

## What changed recently

See [`STATE-history.md`](STATE-history.md).

## Next actions

Full list, with the ceiling on each item and the reasoning behind it, is in
[`STATE-next-actions.md`](STATE-next-actions.md); the standing constraints that hold
whichever item is next are in
[`STATE-constraints.md`](STATE-constraints.md).

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development machine:
12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy present, SciPy/pytest/Z3
absent; `gh` absent. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and pushes via
the GitHub App as `Ihsan Ai Server Bot`. **Unverified:** fleet access, unattended supervision, GPU.
