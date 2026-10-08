<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Decisions — screening candidates and judging experiments, part 13

Decisions **D079–D087**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

## D079 — A candidate's stated pain is measured on bytes against the incumbents that
## would also have to fix it, before it is ranked

`observed` 2026-10-07, session 2026-10-07-003, T-0084, E047, F084.

**The situation.** E045 closed the only candidate and left one live observation,
which `STATE.md` ranked as the mission's single most useful next action: two rows
of the 189-row demand corpus describe a formatter hook that re-stages a whole
file and sweeps a partially-staged file's unstaged hunks into the commit. The
record called it "a correctness failure with a byte-level oracle, named by two
independent repositories". Two rows is not evidence for a candidate, so the
action was to establish whether the hook behaviour is real **in the shipped
tools**.

**The choice.** Measure it, on bytes, with every runner in the population and
with the strongest accessible alternative for each. Not screen it further, not
count how many repositories have the pattern, and not build something.

**The evidence.** Nine arms, git 2.56.0 built from source, lefthook 2.1.17,
pre-commit 4.6.2, lint-staged 17.6.0, husky 9.1.7, prettier 3.9.9. The hazard is
real and byte-exact — the naive hook's commit contains a line that was never
staged — and **no shipped runner produces it**. lefthook 2.1.17 hides unstaged
changes with *and* without `stage_fixed`; lint-staged hides them with defaults
*and* with `--no-stash`; pre-commit hides them around the hook by default; and
`git stash push --keep-index` prevents the hazard with no framework at all. Two
arms running the **same hook body one layer apart** differ only in whether the
framework manages unstaged changes: husky sweeps, pre-commit does not.

**Why this is a rule and not a one-off.** The record's own framing contained the
error. It called the hazard a gap on the strength of two issue rows, and one of
those rows (`nextjs-app-template#95`) turns out to *exonerate* the tool it names,
while the other (`agent-orchestra#154`) records its own reviewer raising the
hazard and the defense being **sustained** as out of scope. The population for
the claim was "the shipped tools", and the shipped tools were exactly the thing
that had to be measured. D077 requires a candidate's *population* to be read out
of its evidence; this requires the same of a candidate's **stated pain**, and
goes one step further by naming where the bytes are.

**Rejected: build a tool that preserves partial staging across hooks.** The
hazard is real and its population is real, and the measurement is what shows
there is nothing to build: three of the four shipped runners prevent it by
default, the fourth supplies no staging of its own, and a two-line git idiom
prevents it. Building here would duplicate incumbents that already work, which
is F026's shape in a different domain.

**Rejected: treat "the two rows disagree" as enough to close it.** Rows are
evidence about a population, not about a tool's behaviour, and this record had
already been burned by trusting a classifier whose precision was never measured
(F064, F069). The disagreement was the reason to measure, not the measurement.

**Rejected: check the runners' source rather than run them.** Reading lefthook's
hiding code would have produced a claim about what the code intends; running it
produced a claim about what the commit contains. The arms differ on that
distinction in exactly the way reading could not have shown — A1b's formatted
worktree and unformatted commit is invisible in the source and obvious in the
blob.

**Ceiling, and what this rule costs.** One fixture, one formatter, one hook
event, one commit per arm. It does not speak to hooks in languages this
experiment did not run, to codegen or `git commit -a` rewriting the worktree, or
to a runner whose behaviour depends on repeated commits. The cost is an
afternoon and a git build, and it is required only when a candidate's claim is
about what an incumbent does to a user's bytes — which is the case where being
wrong is silent.

**Relation to D077 and D075.** D077 reads a population out of demand evidence
before ranking it; this measures a stated pain against incumbents before ranking
it. D075 turned a candidate's limitations section into a measurement plan; F084 is
what that plan finds when the limitation is *someone else's default behaviour*.

## D080 — Fresh exploration begins with a runnable falsification experiment, not a product design (2026-10-07)

`observed` 2026-10-07, session 2026-10-07-014, E051.

**The situation.** The stg candidate (E037) was withdrawn after seven measurements (E043–E048, F075–F085) showed no population for it. The mission's seat for a candidate is empty. The owner brief requires fresh exploration until a specific testable opportunity appears, not reopening closed readings.

**The choice.** Select literature review workflows as a new domain based on independent observation of researcher frustration with manual synthesis tasks. Design a falsification experiment (E051) before any implementation: a rule-based claim extractor for directional contradictions (increases/decreases/no effect) in paper abstracts, tested on synthetic fixtures with predeclared kill gates (recall ≥60%, precision ≥80%).

**The evidence.** The experiment was built and run in the same session: 20 synthetic abstracts, 8 ground-truth contradictions. Extractor achieved 100% precision and 100% recall. Negative controls verified: non-directional abstracts (correlation-only language) produce no claims and no contradictions. Hedged language (may increase/may decrease) correctly detected as contradictions.

**Why this is a rule and not a one-off.** The mission has repeatedly built artifacts before falsifying them (E037 built stg before E043 ran real agents; E049/E050 built lockfile tools before E049's census gate was met). D080 makes the order explicit: **kill gate first, implementation only if it passes**. The experiment must be runnable on this machine (stdlib Python, no external deps), with synthetic fixtures labeled as such, and negative controls that must fail.

**Rejected: build a literature review tool first.** The mission has no validated user, no adoption evidence, and six failed candidates. Building without a passing kill gate is the failure mode this repository exists to avoid.

**Rejected: use an LLM for extraction.** The falsification must be cheap and deterministic. LLM calls add cost, variance, and API dependency. A rule-based extractor on synthetic fixtures is the minimum viable test of the mechanism.

**Ceiling.** Synthetic fixtures only. Real abstracts use varied language, hedging, and indirect phrasing that verb matching will miss. A 100% result on synthetic data does not establish real-world precision/recall. The next step is testing on real PubMed Central abstracts; if precision/recall drops below kill gates, the claim is abandoned. Human evaluation of triage usefulness is required before any product claim.

## D081 — A verifier earns a tool only when its verdict is not already derivable from the incumbent's own primary output; "wrong at exit 0" is not sufficient

`observed` 2026-10-08, session 2026-10-08-003, T-0087, E055, F088.

**The situation.** F082 closed the line-staging application by naming two shipped
incumbents, read from **README prose, never measured**. The prose implied a
*postcondition* gap: neither tool reads `.git/index` back, and a caller scripting
one gets exit 0 without learning what landed. E055 built the tool-neutral checker
that gap implies and ran 210 arm-rows against E038's hand-written oracle — and the
gap did not survive contact with bytes.

**The choice.** Require, as the build gate, not only that the incumbent *can* be
wrong at exit 0 but that its own **primary output** gives the caller no way to
derive the same verdict. Only then does a verifier add a fact rather than restate
one. Measure the incumbent's primary artifact — not its optional diagnostic
report — because a report that spans a neighbourhood cannot distinguish a carried
change from context the caller never asked about.

**The evidence.** K2 fired: `filterdiff` exits 0 on a wrong index on 6 rows, which
is **one** distinct index state reproduced across three contexts. K3 failed:
`filterdiff` emits a unified diff in which a carried line is exactly a `+`/`-`
body line, so the selected patch the caller already piped through the tool names
line 1 while the caller named line 2. `ceiling.py` established this is not an
artefact of `-U0`: at `-U1`, `-U3` and the default, 12 of 12 rows over-stage and
the primary output names a line beyond the want in 12 of 12, with C11 holding the
reader to `git diff --cached -U0` on all 16 staged rows and C12 holding it to an
exact selection read exactly. Verdict `do_not_build`.

**Why this is a rule and not a one-off.** D077 requires a candidate's *population*
to be read out of its demand evidence; D079 requires its *stated pain* to be
measured against the incumbents. This requires the **pain's mechanism** to be
checked for redundancy in the incumbent's own output — the last place a redundant
candidate can hide. F063 measured "wrong but exit 0" across three alternatives
and correctly declined to build, but had no artefact for the shape and no stated
criterion; the criterion is what turned 78 rows of wrongness into a build
decision, and the oracle that scored them turned out to be the reusable part.

**Rejected: build the checker because the incumbent exits 0 on a wrong index.**
That is the shape F063 measured and it is real; it is also, on this population,
information the caller already holds. Building here would ship a second reading of
a patch the first tool printed.

**Rejected: accept a probe that saw nothing as a negative.** Run 2's K3 did, and
it returned `do_not_build` from an instrument with no observations — the F010 shape,
where an arm that never ran reads as a clean result. An empty probe is now
`undecided` and the whole verdict follows it.

**Ceiling.** One fixture family (10 single-file LF cases × 3 contexts), one host,
`gah` never measured, one change requested per file. The rule does not need a
wider fixture to hold: it fired on the arm that over-stages, at every context
measured. The cost is a checker and its controls — the instrument, not the
experiment, was the expensive half.

**Relation to D079 and D077.** D079 asks whether an incumbent *has* the defect;
this asks whether anyone would *learn* something new from a tool that checks it.
A candidate must survive both, and the second is the one that closes the larger
share of them.
## D082 — An arm that produced no observation is a missing observation, never a zero and never a denominator (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-005, E061.

**The situation.** E061's population gate declared its kill condition before reading a row, then ran ten search arms. Two returned **HTTP 422** — a misspelled repository owner in a `repo:` qualifier — and returned zero items. Zero items from a 422 and zero items from a real negative are the same value in the same field, and the two failed arms were `coveragepy` and `vulture`, the two carrying the most weight. Two days earlier E056 (F087) closed a candidate with a three-row results table under a heading describing a five-package sample, its text saying `pre-commit and mypy runs timed out; partial evidence only`.

**The choice.** Every measurement in this repository states, per arm, whether an observation was produced, and a rate or count is only ever written over the arms that produced one. A missing arm is printed as missing, with the reason it is missing, and it is excluded from the denominator. A verdict reached over a subset names the subset in the verdict sentence itself.

**Why this is a rule and not a one-off.** It is F013, F021 and F025 one layer up. F013 is a gate that exists and is never run, so a green run proves nothing; F021 is an annotator's rendering declared `unmeasured` on a run whose annotating steps never ran; F025 is a red-run cause made readable but never explained. All three are a step that did not happen, read as a step that came back empty. The mission's own instruments produce the shape whenever a summary is a count over independently-failing arms, and two of the three instances found so far are verdicts that closed candidates.

**Rejected: fail the whole experiment on one missing arm.** The cost is the other arms, and the owner brief's bounded-audit rule applies — the missing arm is reported and the experiment continues over the arms that ran. **Rejected: retry until every arm succeeds.** Ten retries is how a bounded probe becomes an unbounded one, and the two 422s here were a misspelling, not a rate limit. **Rejected: treat a discarded arm as a zero.** A tenth arm returned `total_count = 202343` because its query contained an `OR`; counting that as a zero would have manufactured a population. It is discarded and named.

**Ceiling.** D082 is a records rule and cannot make a partial measurement sufficient. E056's verdict is **not withdrawn** — nothing here shows it is wrong — but it now reads *over three observed arms of five attempted*, and a reader can see which three.

## D083 — A rubric clause that cannot recover a positive on its own domain disarms its own null branch, permanently (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-006, E062, F095.

**The situation.** E062 was declared to answer whether the mission's empty
candidate seat is a property of *human unmet need* or of its *software sample
route*. Arm 1 was a non-software population, and the rubric's clause 1
disqualified any need consuming an input only the requester holds. That clause is
right for a software venue, where the requester's own data means an account, a
token, a private repository. In a physical domain it means their plant, their
stain, their nameplate, their symptom. **All 110 no-remedy rows were read**, and
the shape is 86 technique-or-material answers against 15 diagnoses of the
requester's own physical thing: the disqualifying clause rejects the treatment
arm's ontology, so it cannot recover a positive on it.

**The choice.** G3 — the declared measurement — was not run, and its null branch
is **permanently disarmed** rather than recorded as unfavourable. The
find-a-new-venue route is **deferred with its reason recorded**, which is a
different standing from closed. The clause was not rewritten to fit the data.

**Why this is a rule and not a one-off.** A gate whose null branch was declared
permanent must not be computed by an instrument that cannot produce a positive on
its own domain, because a permanent closure executed by a broken instrument is
unrecoverable in a way an unfavourable result is not. It was caught by reading the
population before labelling any of it — D077's rule applied to the instrument
rather than to a candidate — and D077's rule did not exist for instruments. This
generalises D075 (a candidate's limitations section is a measurement plan) and
D077 (read the population before building to measure it) to the measuring
apparatus itself.

**Rejected: loosen the clause until the gate computes.** The declared decision was
"comparable-or-lower closes the route permanently"; a rubric tuned until it
returns that answer measures the tuning. **Rejected: record the null as
unfavourable and leave the route closed.** Nothing observed a comparison; the
route's standing would rest on a number the instrument never produced.

**Ceiling.** The finding is about this clause on this population. A rubric that
disqualifies requester-held inputs is not wrong for a software venue, where such
an input usually means an account — the rule is that a disqualifying clause must
be shown to fire on positives in its own domain, not that it may never fire.

## D084 — Arrival at a need is a different quantity from a statement of need, and a non-reply is not an absence of service (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-006, E062, F096, F097.

**The situation.** Every population this mission has measured counted
*statements* of need and read them as service levels. F039 measured the closest
available proxy — whether requesters came back — and read 1 reply of 794 as
absence of demand. E062 read the whole no-remedy population of a second venue
(110 rows) and attempted the top 20 **by arrival** against the strongest
accessible alternative, a general-purpose assistant answering from its own
knowledge, free and instant. **17 of 20 are answered in full today.** The
residual 3 are a data absence: a 2001 BMX serial number nobody recorded, and
per-model spec sheets nobody made queryable.

**The choice.** `view_count` is adopted as the mission's arrival measure, and any
future population carrying an arrival measure reports **both** a statement count
and an arrival count with its denominators stated separately. A missing reply is
never read as an absence of service.

**Why this is a rule and not a one-off.** Someone whose boiler question is answered
by an assistant in 2024 does not post on a forum either way, so reply rate cannot
distinguish "served elsewhere" from "never served" — the two hypotheses F039's 1
of 794 could not separate. The gap between statement and service measured 17 in
20 here, which is large enough that a single reader's verdict on the strength of
replies would have been wrong about nearly every row it touched.

**Measured alongside it, and against expectation:** unremedied need is **not**
heavy-tailed on this venue — the top 10% of unremedied rows carry **3.2%** of all
views. Ranking rows by arrival is therefore *not* a privileged sample of unmet
need, and the mission's habit of reading a screened subset as representative is
wrong on this venue too. This is the same correction D063 made for a
tag-stratified rate, arriving from the other direction.

**Rejected: use `view_count` as a demand measure.** Views count arrivals at a
question, not unmet need; the 15,635-view row is answered free today. Arrival
ranks attention. **Rejected: keep F039's reply rate and discount it.** The number
is not wrong; the inference from it was, and D084 names which.

**Ceiling.** `view_count` exists on Stack Exchange and not on most venues, which is
why E062's harvest chose it, and arrival is not available for a private or
single-tenant population at all. The rule governs reporting, not acquisition.

## D085 — a trigger-phrase harvest of need statements is not a candidate source (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-013, E063, F098.

**The decision.** The mission's standing route for finding candidates — harvest
statements of need by trigger phrase from Hacker News and GitHub issues, screen
them, kill the ones that do not survive — is retired. E063 ran the E062
answerability instrument on both corpora: arm A served share 0.676 (48/71),
arm B 0.969 (31/32), `unserved-open` 0 of 103 rows, and 12 of 71 arm A rows
state no requestable need under a trigger phrase. The route selects rows the
strongest accessible alternative already serves, and what resists it is never a
tool-shaped need.

**What still holds.** D083 stands — a rubric whose null branch would close a
route permanently disarms that branch, so the find-a-new-venue route is
deferred with its reason recorded, not closed. D084 stands — report arrivals and
statements separately. D080 stands — fresh observation begins any future
exploration. The difference is that the fresh observation must be of a need the
harvest cannot show: a trigger phrase in a forum is now evidence of a statement,
never of a service gap.

**Rejected: keep screening such corpora with more gates.** The gates were not
wrong; their inputs were. **Rejected: treat the 0.814 over-stated-need share as
a route worth mining for the unserved 19%.** That 19% is `unserved-remedy-is-human`
(9 rows) plus `unserved-data-absent` (2): the remedy is the requester's own
institution or a record nobody kept, neither of which is a buildable gap.
**Ceiling:** one labeller, one incumbent, two corpora, today, not then — this
retires the route as a candidate generator, not every conceivable way of
listening for need.

## D087 — the need-harvest route is closed at the population level; fresh observation begins in a new domain (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-021, E066, F100.

**The decision.** The mission's standing route for finding candidates — harvest
statements of need by trigger phrase from Hacker News and GitHub issues, screen
them, kill the ones that do not survive — is **closed** (not deferred) at the
population level. E066 independently confirmed E063's finding with a separate
classifier: GitHub corpus has 82% false positive rate (155 of 189 issues are
about CI/CD/build stages, not git line staging); HN corpus has 55% non-software
content in its top triggers; `unserved-open` is 0 of sampled rows. The seven
emptiness measurements (F029, F039, F051, F059, F081, F084, F085) were not
wrong about the domains they sampled — they were reading a route that selects
served statements.

**The choice.** The route is retired. Any successor session starts from fresh
observation in a new domain, per D083: runnable falsification experiment first
(stdlib-only, synthetic fixtures, predeclared kill gates), not a product design.
The difference from D085 is that D085 deferred the route (the instrument
needed work); E066 confirms the population itself has no unserved tail. The
route is closed, not deferred.

**Rejected: one more screen or one more corpus.** The population is the
problem, not the screen. **Rejected: treat the HN corpus as a separate route.**
The top triggers are dominated by non-software content; the software subset
is 86.7% served. **Ceiling:** two independent classifiers, two corpora, one
incumbent (the labeller), today not then. This closes the route; it does not
close the mission.
