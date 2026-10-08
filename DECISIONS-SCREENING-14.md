<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# Decisions — screening candidates and judging experiments, part 14

Split out of [`DECISIONS-SCREENING-13.md`](DECISIONS-SCREENING-13.md) on 2026-10-08 when that file reached the 300-line cap. The rule is unchanged: a decision is recorded when the choice was genuinely open, with evidence, alternatives, and reason.

Decisions **D084–D087**. Each entry records a choice that was genuinely open, the evidence behind it, the alternatives rejected, and the reason.

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