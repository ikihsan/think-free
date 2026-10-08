<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# Decisions — screening candidates and judging experiments, part 14

Split out of [`DECISIONS-SCREENING-13.md`](DECISIONS-SCREENING-13.md) on 2026-10-08 when that file reached the 300-line cap. The rule is unchanged: a decision is recorded when the choice was genuinely open, with evidence, alternatives, and reason.

Decisions **D085–D086**. Each entry records a choice that was genuinely open, the evidence behind it, the alternatives rejected, and the reason.

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

## D086 — the need-harvest route is closed at the population level; fresh observation begins in a new domain (2026-10-08)

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