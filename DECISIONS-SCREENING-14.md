<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# Decisions — screening candidates and judging experiments, part 14

Split out of [`DECISIONS-SCREENING-13.md`](DECISIONS-SCREENING-13.md) on 2026-10-08 when that file reached the 300-line cap. The rule is unchanged: a decision is recorded when the choice was genuinely open, with evidence, alternatives, and reason.

Decisions **D084–D088, D095–D097**. Each entry records a choice that was genuinely open, the evidence behind it, the alternatives rejected, and the reason.

## D084 — Arrival at a need is a different quantity from a statement of need (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-006, E062, F096.

**The situation.** Every population this mission has measured counted *statements* of need and read them as service levels. F039 measured the closest available proxy — whether requesters came back — and read 1 reply of 794 as absence of demand. E062 read the whole no-remedy population of a second venue (110 rows) and attempted the top 20 **by arrival** against the strongest accessible alternative, a general-purpose assistant answering from its own knowledge, free and instant. **17 of 20 are answered in full today.** The residual 3 are a data absence: a 2001 BMX serial number nobody recorded, and per-model spec sheets nobody made queryable.

**The choice.** `view_count` is adopted as the mission's arrival measure, and any future population carrying an arrival measure reports **both** a statement count and an arrival count with its denominators stated separately. A missing reply is never read as an absence of service.

**Why this is a rule and not a one-off.** Someone whose boiler question is answered by an assistant in 2024 does not post on a forum either way, so reply rate cannot distinguish "served elsewhere" from "never served" — the two hypotheses F039's 1 of 794 could not separate. The gap between statement and service measured 17 in 20 here, which is large enough that a single reader's verdict on the strength of replies would have been wrong about nearly every row it touched.

**Measured alongside it, and against expectation:** unremedied need is **not** heavy-tailed on this venue — the top 10% of unremedied rows carry **3.2%** of all views. Ranking rows by arrival is therefore *not* a privileged sample of unmet need, and the mission's habit of reading a screened subset as representative is wrong on this venue too. This is the same correction D063 made for a tag-stratified rate, arriving from the other direction.

**Rejected: use `view_count` as a demand measure.** Views count arrivals at a question, not unmet need; the 15,635-view row is answered free today. Arrival ranks attention. **Rejected: keep F039's reply rate and discount it.** The number is not wrong; the inference from it was, and D084 names which.

**Ceiling.** `view_count` exists on Stack Exchange and not on most venues, which is why E062's harvest chose it, and arrival is not available for a private or single-tenant population at all. The rule governs reporting, not acquisition.

## D085 — A trigger-phrase harvest of need statements is not a candidate source (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-013, E063, F098.

**The decision.** The mission's standing route for finding candidates — harvest statements of need by trigger phrase from Hacker News and GitHub issues, screen them, kill the ones that do not survive — is retired. E063 ran the E062 answerability instrument on both corpora: arm A served share 0.676 (48/71), arm B 0.969 (31/32), `unserved-open` 0 of 103 rows, and 12 of 71 arm A rows state no requestable need under a trigger phrase. The route selects rows the strongest accessible alternative already serves, and what resists it is never a tool-shaped need.

**What still holds.** D083 stands — a rubric whose null branch would close a route permanently disarms that branch, so the find-a-new-venue route is deferred with its reason recorded, not closed. D084 stands — report arrivals and statements separately. D080 stands — fresh observation begins any future exploration. The difference is that the fresh observation must be of a need the harvest cannot show: a trigger phrase in a forum is now evidence of a statement, never of a service gap.

**Rejected: keep screening such corpora with more gates.** The gates were not wrong; their inputs were. **Rejected: treat the 0.814 over-stated-need share as a route worth mining for the unserved 19%.** That 19% is `unserved-remedy-is-human` (9 rows) plus `unserved-data-absent` (2): the remedy is the requester's own institution or a record nobody kept, neither of which is a buildable gap. **Ceiling:** one labeller, one incumbent, two corpora, today, not then — this retires the route as a candidate generator, not every conceivable way of listening for need.

## D086 — The need-harvest route is closed at the population level; fresh observation begins in a new domain (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-021, E066, F100.

**The decision.** The mission's standing route for finding candidates — harvest statements of need by trigger phrase from Hacker News and GitHub issues, screen them, kill the ones that do not survive — is **closed** (not deferred) at the population level. E066 independently confirmed E063's finding with a separate classifier: GitHub corpus has 82% false positive rate (155 of 189 issues are about CI/CD/build stages, not git line staging); HN corpus has 55% non-software content in its top triggers; `unserved-open` is 0 of sampled rows. The seven emptiness measurements (F029, F039, F051, F059, F081, F084, F085) were not wrong about the domains they sampled — they were reading a route that selects served statements.

**The choice.** The route is retired. Any successor session starts from fresh observation in a new domain, per D083: runnable falsification experiment first (stdlib-only, synthetic fixtures, predeclared kill gates), not a product design. The difference from D085 is that D085 deferred the route (the instrument needed work); E066 confirms the population itself has no unserved tail. The route is closed, not deferred.

**Rejected: one more screen or one more corpus.** The population is the problem, not the screen. **Rejected: treat the HN corpus as a separate route.** The top triggers are dominated by non-software content; the software subset is 86.7% served. **Ceiling:** two independent classifiers, two corpora, one incumbent (the labeller), today not then. This closes the route; it does not close the mission.

## D087 — No deterministic existence checker is worth building: the existence bit is materially insufficient and its cheap repair does not work (2026-10-08)

`observed` 2026-10-08, session 2026-10-08-014, E064-A1, F099.

**The decision.** E064-A1's two gates close the route the original E064 protocol opened. **G5 fired:** 93 of 576 plausible near-miss mutations of real package names resolve to real, different artifacts — 0.1615, Wilson CI95 [0.134, 0.194] (npm 0.278, PyPI 0.167, crates 0.156, RubyGems 0.063, Packagist 0.000), ground truth definitional, zero missing observations. So the one bit every existence check returns is materially insufficient: an installer, an IDE squiggle, or a pre-install checker that says "exists" is wrong 16% of the time on this population, silently — the install succeeds. **G6 failed its recall arm:** the rule this protocol fixed before any mutation was generated (downloads < 1 000; badge/empty description; newest release older than 3 years; no repository URL) flags 69 of 93 false accepts (0.742 against a 0.90 gate) while correctly leaving 29 of 30 real registry-listing names alone (0.967). The 24 it misses are healthy, popular, maintained projects — `jinja2-cli` (11.2 M downloads/year), `sqlalchemy-utils`, `django-click` (1.7 M), the gem `async-redis` (863 K) — indistinguishable from the real class on every declared signal, several of them the seeds' de-facto companion libraries.

**What still holds.** D080 stands — fresh observation begins any future exploration, and this one began from the prior art's own limitation section (arXiv:2501.19012 names the squatted-name failure with n = 2 anecdotes and no rate). D082 stands — a registry that cannot answer is a missing observation: the metadata run transiently lost all NuGet and all Homebrew rows, they were re-fetched and are recorded as recovered, and PyPI/Packagist/Homebrew download fields that do not exist are dropped per row, never zeroed. D077 stands — the population was read out of the evidence before anything was built: the negative control was arm C's own 30 hand-invented names, 2 of which resolved, which is why the ground truth was rebuilt definitionally instead of labelled. D081 stands — the checker's verdict had to be non-derivable from the incumbent's output, and the registry's own response is the whole verdict here.

**Rejected: build the pre-install existence checker anyway.** The original E064 candidate would have *confirmed* 16% of the wrong names it was asked about; its success case is the failure case, and the rate it would have trusted is published (F099). **Rejected: tune the rule until it separates.** The gate was fixed before the data and its failure is informative — the residual is a *semantic* population (packages that do something adjacent), so a better metadata heuristic is looking for a signal the classes do not carry; chasing recall past 0.90 on 93 rows against a specificity arm that already flags real packages (`zero-fill`, newest release 2020) would be fitting the sample. **Rejected: extend to more ecosystems and re-declare.** The five measured span the namespace shapes (flat, `vendor/pkg`, scoped) and the rate tracks them; more ecosystems would narrow the interval, not change the decision.

**Ceiling.** One author's idea of "plausible mutation" (three families), 37 fame-selected seeds, five ecosystems, one day, 2026-10-08, public registries only. It measures existence and coarse metadata. It does not measure whether a resolved package is semantically right, whether any impostor is malicious, whether model output's real near-miss distribution matches these families (that was the withdrawn G2), or whether any person or agent would run such a check — `pip install` is free and already answers the existence bit, so the proposed difference was always only the false-accept bit, and that bit is now measured in both directions. The separator that remains is "does this package do what was asked" — the named alternative's job, a model call — so the cost and determinism advantage that justified a checker is gone with it.
## D088 — A kill gate whose only reachable successes are empty files measures nothing; read the gate's reachable set before the run (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-003, E069, F101.

**The decision.** E069's direction is closed, and it is closed on **K3**, not on K1. E069's `GEN` arm installs cleanly in 3 of the 16 repositories measured, so the predeclared K1 ("installs cleanly for >= 3 of 20") **passes** and the analysis tool labels the run "mechanism holds". That label is not taken as the result. All three installable specs name **no package at all** (two empty files) or one unrelated package (`temperature==2.7`); **verified imports are 0 of 16**. K3 is the gate that does not depend on the artifact: on 4 of 16 repositories the repository's own declared file installs while the generated one does not, 2 of them reaching a fully working environment. So the direction closes because a generator is *worse than the incumbent* where anything was tested, not because it failed to install three times.

**The generalisable rule.** `PROTOCOL.md` Amendment 1 predicted this outcome in advance — "K1 can therefore be met only by a specification that installs nothing" — and the prediction held, which means the protocol *knew* the gate could not fail and still ran it as the headline gate. **Before a gate is declared, enumerate what its passing value can actually be made of.** A gate is informative only if its passing region contains a case a working mechanism would produce and a broken one would not. K1's passing region contained only empty files: an artifact that installs nothing is indistinguishable from an artifact that installs everything correctly, so the gate had no discriminating power and its threshold of 3 was reachable by a generator that emits nothing. This is F010's shape again — a declared gate shown not to be able to fail — on an install test rather than on a timestamp field.

**The cost of finding out this way.** One additional repository was measured precisely because the static arm showed it carried no blocking pin. It was `google-research/google-research`, whose generated spec is an empty file, and measuring it moved the tool's label from `KILL` to `mechanism holds`. A single empty file moved a headline verdict. That is the concrete demonstration of the rule above, and it is why the verdict is now read from K3 and from verified counts.

**Rejected: report "mechanism holds" as the result.** It is what the predeclared arithmetic says, and reporting it would have been defensible to a reader who did not open `raw/`. It is not what was measured. **Rejected: re-declare K1 after seeing the data.** The threshold is kept exactly as written, and the strict reading is added *alongside* it rather than replacing it — `analyze.py` reports `pass` and `pass_strict` for every gate, so the declared arithmetic stays auditable and the honest reading is visible in the same object. **Rejected: complete all 20 repositories.** `results.json` reports `gates_determined: true` with the reason: all 4 unmeasured repositories carry at least one pin the static arm shows pip refuses, so `GEN` cannot install on any of them and no further measurement can move K1 or K2; K3 can only gain rows. The shortfall is a missing observation on `DECL` coverage (so K3's 4 rows are a floor), not an open gate.

**Standing consequence: the analysis must read durable bytes, not a file the run writes at the end.** `analyze.py` originally read `raw_results.json`, which `harness.py` writes once when a whole run finishes — so mid-run it described the pilot's single repository — and read a `controls.json` that no run produces, so `oracle_valid` was `None` and the arms would have been interpreted without the controls that license interpreting them. It now reads the per-repository files and the two control files the control run actually writes, and a missing control counts as `not all_pass`. A verdict that cannot be regenerated from committed bytes is not a verdict.

**Ceiling.** 16 of 20 repositories, one arXiv year, all deep-learning GitHub code, Python 3.10 only, no GPU. The oracle as amended cannot catch a spec that *omits* a needed dependency — it probes what the spec claimed, not what the code wants — so a generator that silently dropped half a dependency could pass every arm here. `DECL` is the strongest alternative available without inventing a mechanism; a colleague who fixes the install by hand is not measured and remains the honest ceiling. This closes E068's direction as implemented; it does not disprove that an environment can be inferred from a repository, and it says nothing about adoption.

## D096 — A mechanism that passes synthetic kill gates but requires identifier linkage that does not exist in practice is not a candidate (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-018, E080.

**The situation.** E080 tested food recall purchase matching: match consumer purchases (receipts, loyalty exports, manual entry) against FDA/USDA recall data using UPC, lot codes, best-by dates. Predeclared kill gates: G1 precision ≥80%, G2 recall ≥60%, G3 ≥2 of 3 formats pass both, G4 specificity = 1.0. The mechanism passed all gates on 5/5 random seeds with synthetic fixtures.

**The evidence.** Synthetic fixtures were constructed so that each recall and its corresponding purchases share the same store (→ same UPC), lot code, and best-by date by design. The matching algorithm correctly exploits this guaranteed linkage. Receipts: UPC suffix match (1.00/1.00). Loyalty: exact UPC match (1.00/1.00). Manual entry: fuzzy name match (1.00/0.93).

**The choice.** Record as technical feasibility only — the mechanism works when identifiers align. Do not advance as a candidate. The practical bottleneck is obtaining matchable purchase identifiers without store cooperation: real receipts rarely have UPCs (10-30%), almost never have lot codes; store brands use different UPCs than national brands; FDA recall data has UPC in ~40% of records. Loyalty programs (Kroger, Costco, Safeway) already notify members — they have the purchase UPC + store mapping.

**Why this is a rule and not a one-off.** D088 requires enumerating a gate's reachable set before declaring it; this requires enumerating a mechanism's *real-world preconditions* before calling it validated. A mechanism that only works when its inputs are guaranteed by fixture construction has not been tested — it has been assumed. The kill gates passed, but the preconditions are the claim.

**Rejected: advance to product engineering.** The identifier linkage problem is the hard part, not the matching logic. **Rejected: test on real receipts now.** Requires authorized data collection; not a reversible experiment. **Rejected: partner with a loyalty program.** Beyond current authorization.

**Ceiling.** 5 seeds, 30 products, 3 formats, stdlib Python. Measures matching logic correctness given identifiers; does not measure identifier availability, OCR noise, store-brand UPC divergence, recall data sparsity, or user adoption.

## D095 — An instrument must be shown to discriminate a known-positive from a known-negative before its numbers are read (2026-10-10)

`observed` 2026-10-10, session `2026-10-10-004`, E088, F109.

**The situation.** Seven consecutive sessions ran E081–E087, each a "fresh
observation in a new domain", and a committed synthesis
(`EXPERIMENTS/synthesis-view-count-principle.md`) reported a dose-response
gradient across domains, a regulatory-domain boundary, and intermediate
behaviour — describing all of it as the view-count principle generalising.
E088 froze 40 probes whose labels are known by construction and ran E087's own
`bing_search()` and `classify_served()` unchanged over them. **8 of 20
nonexistent products were classified `served`**; 11 of 20 genuinely-served
questions were classified `served`; the difference's CI95 spans zero. Every one
of the eight false positives is a page set that never mentions the subject.

**The choice.** A measurement instrument must pass a discrimination test —
labels known by construction, both arms, before any population is read — before
any number it produces is interpreted. Where that test is absent, the numbers
are not weak evidence; they are uninterpretable, and the line is closed rather
than carried forward. Applied here it closes E081–E087 and the synthesis.

**Why this is a rule and not a one-off.** E081–E087 each declared a G2 "control
validity" gate. E081's implementation hardcodes
`true_labels = ['unserved'] * 5 + ['served'] * 5` — the gate asserts the
labels it then checks the classifier against, so it cannot fail. That is F101's
failure mode, and it survived seven experiments because each protocol wrote its
own version of the gate rather than inheriting a validated one. A gate that
agrees with its own assumption is not a control. The instrument has to be shown
to separate cases whose answer is not in question.

**Why the working practice follows from it.** `view_count` was adopted as an
arrival measure in D084 and is not in question. What was in question was
whether an instrument *claiming* to measure it did. F109 does not touch
D084's rule, the E062 finding, or the arrival measure itself.

**Rejected: keep the seven experiments and discount their confidence.** The
gradient ordering does survive relevance restriction, which makes the results
look robust. It is not evidence: `partially_served` is produced by the
classifier, so restricting rows to relevant ones cannot move it. **Rejected:
re-run the domains with a better classifier.** That is a different experiment
and it needs a different question; the population question is still unasked.
**Rejected: report only the G1 failure and leave the synthesis standing.** The
synthesis is the artifact that would be read next, and it is false as written.

**Standing consequence: an experiment's protocol names the instrument and the
run must call that instrument, not a local copy.** E088 imports E087's
`classify_served` rather than reimplementing it, so a change to the instrument
cannot leave the older experiment's numbers describing a different thing.
Seven directories carrying seven near-identical `outcome.py` copies is how the
drift went unnoticed.

**Rejected, and recorded against this decision: trust a declared control
gate.** E088's own G2 — "does any non-chrome content token appear anywhere in
five HTML blocks" — passes at 0.763 while a third to two-thirds of those
blocks are ad slots and spam. It is written after F101 and reproduces F101's
shape. The rule above is not satisfied by *declaring* a gate; only by observing
that the gate can fail.

**Ceiling.** One search engine, one classifier, 40 probes, n=20 per arm, and
probes written by the agent that interprets them. F109 shows this instrument
fails to discriminate. It does not show that no classifier over Bing can, and
it says nothing about whether structured fault/error-code domains hold unserved
needs — that population was never measured here, and remains open.

## D097 — A rate whose ground truth is definitional is a count of the generator's assumption, and it is read as a rate about the world only after someone reads the artifacts (2026-10-10)

`observed` 2026-10-10, session `2026-10-10-005`, E089, F110.

**The situation.** F099 is the reason the package-name line is closed *against*
building: "0.1615 of plausible near-miss package names resolve to a real,
different artifact — the existence bit every installer, IDE and checker returns
is materially insufficient." The sentence is in `STATE.md`'s dashboard and is
the mission's strongest modern evidence about installer failure. E064's protocol
grounds it definitionally: the intended artifact of every mutated name "is the
original", so any resolving mutation "is a false accept **by construction**".

That is a claim about people — that they type `requests-utils` meaning
`requests` — made by the mutation operator and never measured. E089 read the 93
descriptions E064 had already fetched, committed, and never opened.

**The evidence.** 11 of 93 present themselves as providing the seed's capability
under their own name (0.118, CI95 [0.067, 0.199]); 44 are derivatives with a
stated purpose; 38 are other, **13 of them parked names** whose install succeeds
and imports nothing. The same rule labels **0 of 30** intended artifacts
`equivalent`, so the trigger is specific. Seven of the eleven say it in their own
words. **11 of 576 = 0.0191, against the 0.1615 that was quoted** — and E085's
independent hand-read of real declared dependencies put the silent rate at 0.6%,
so two measurements on different populations agree.

**The choice.** Annotate F099 and the dashboard sentence rather than delete the
experiment, and keep the line closed — now on a number that can be defended. The
existence bit is still insufficient; it is not insufficient at the strength
0.1615 implies.

**Why this is a rule and not a one-off.** The record has three instances of the
same shape, and they are its most expensive errors: E081's G2 asserts the labels
it checks against (F109), E029's control was a relabelled replicate of its
treatment arm (F049), and E064's ground truth is definitional (F110). In each
case **the instrument produced the label and the label was then read as a fact
about the world**. The rule: *a label produced by a generator's own assumption is
not evidence about the world until the artifacts it names have been read.* The
check is cheap — E089 needed no fetch, no classifier, and no budget, only the
descriptions already sitting in the repository unopened.

**Rejected: delete F099.** The 93 resolutions are `observed` and real; the
defect is in the label applied to them, not in the measurement. **Rejected: keep
0.1615 and add a footnote.** The sentence's force comes from its number, and a
footnote under a number that is 8.5x too high leaves the wrong figure in every
reader's memory — F109's failure was exactly that. **Rejected: treat 11 as a new
build target.** 11 real packages still present themselves as drop-in
replacements for other real packages and nothing says so, but at ~1.9% of
plausible near-miss names and ~0.6% of real declared dependencies that is a
warning, not a product, and E085 already measured the incumbent's gap.

**Ceiling.** 93 rows, four ecosystems, Packagist `not_exercised`. The population
is generated affix mutations, which is not what a person types; E089 does not
correct that bias, and says so.
