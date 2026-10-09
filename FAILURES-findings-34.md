<!-- origin-meta
owner: FAILURES.md
status: active
last-verified: 2026-10-08
-->

# Findings 34 — independent confirmation of the need-harvest route retirement

`observed` 2026-10-08, session 2026-10-08-021, VM `instance-20260717-0944`.
Evidence: [`EXPERIMENTS/066-need-answerability/`](EXPERIMENTS/066-need-answerability/README.md).

Split out of [`FAILURES-findings-33.md`](FAILURES-findings-33.md) on 2026-10-08.
**Identifiers are stable across all findings files.**

## F100 — E066 confirms E063: the need-harvest route is closed at the population level

**What happened.** E066 ran an independent classification of the two corpora every
candidate screen in this repository consumed: E038's 189 GitHub issues (the
corpus behind the `stg` candidate) and E012's 1401 Hacker News "is there a tool
that" comments (the corpus behind the 0-of-50 harvest). This was a separate
session from E063, using a different classifier (this model's direct judgment
rather than E062's instrument with controls), to confirm the primary result.

**The measurement.**

| corpus | total | actually about target | served | not-software | notes |
|---|---|---|---|---|---|
| GitHub (E038) | 189 | 34 (18%) | 34 (100% of real) | — | 155 false positives on CI/CD/build/pipeline stages |
| HN (E012, sampled) | 100 | 45 | 39 (86.7%) | 55 | top 5 triggers by frequency, 20 each |

**GitHub corpus:** Only 34 of 189 issues are actually about git line/hunk
staging. The other 155 are false positives from the search queries matching
"stage" in CI/CD contexts (GitHub Actions stages, build pipeline stages,
deployment stages, Docker multi-stage builds, etc.). All 34 real issues request
capabilities that already exist in the ecosystem: `git add -p`, lazygit, magit,
VS Code's `git.stageSelectedRanges`, neogit, tig, git-hunk, gah, filterdiff.
Two shipped tools (`gah`, `git-hunk`) take the exact coordinate `stg` uses and
name the agent population in their READMEs. This replicates E045's finding that
the classifier had 0.372 precision / 0.552 recall and the "population" was
largely noise.

**HN corpus:** The top 5 trigger phrases by frequency capture predominantly
non-software content:
- "i wish there was" (749): personal wishes, political commentary, philosophy
- "is there a way to" (154): mixed technical and non-technical
- "any tool that" (97): often political/philosophical statements
- "looking for a way to" (70): mixed
- "is there anything that" (54): mostly political/philosophical

55% of sampled needs are not software needs at all. Of the 45 software-related
needs, 39 (86.7%) are resolved-from-knowledge — tools, libraries, frameworks,
or patterns already exist. 4 are unresolved-no-public-data (private contact,
undocumented firmware), 2 resolved-needs-external-data (proprietary
subscriptions).

**What it buys.** E063's finding (F098) is independently confirmed: seven
emptiness measurements in this repository (F029, F039, F051, F059, F081, F084,
F085) were not wrong about the domains they sampled; they were reading a route
that selects **served statements**. The trigger-phrase harvest over HN/GitHub
has no tail where a tool could start (`unserved-open` = 0). The route is
retired as a candidate source. Per D083, any successor session starts from
fresh observation in a new domain with a runnable falsification experiment
(stdlib-only, synthetic fixtures, predeclared kill gates).
## F101 — the software arm's `view_count` zero was a missing observation, and E069's confirmation was a platform artifact

**What happened.** Four experiments (E067, E067b, E069 ×2) and
`MISSION-OUTCOME.json` were sitting unlanded on the tree, all resting on E069's
headline: *100% of non-software need statements have `view_count` > 0 …
this **directly contradicts the E063/E066 finding** … `view_count` is 0% in
software need corpora … the instrument's domain scope is **not
software-narrow**.* That contrast is what "validated the instrument outside
software" rests on, and E070 lists it as `ground_truth_context`. E069 had read
the software cells as **measured zeros**; the question of whether they are
zeros at all had never been asked.

E071 asked it, with three arms and a predeclared kill condition
([`EXPERIMENTS/071-viewcount-denominator/`](EXPERIMENTS/071-viewcount-denominator/README.md)).
Probing eight spellings of an arrival field across 148 returned objects:
**Hacker News 0 of 60 items carry one, the GitHub issues API 0 of 8, and
Stack Exchange — the surface E062 actually measured — 80 of 80 items carry a
positive `view_count`.** All three gates fired. The instrument can say no: its
classifier returns `zero` / `positive` / `absent` / `not_an_object` correctly
on five fabricated cases, and arm C is what makes arms A and B interpretable,
because it shows the harness reads the field when a platform returns it.

**Why it happened.** The E063/E066 corpora were harvested from exactly those two
APIs, which publish no arrival count — so the software arm of E069's comparison
was reading a field that does not exist and recording its absence as `0`.
That is **D082 committed a second time**: an arm that produced no observation
is a missing observation, never a zero and never a denominator, and a session
that had just written D082 down read its own rule and then harvested a field
the platform does not serve. The same E063/E066 rows that produced eight
`unserved-open` zeros — the result the route retirement rests on — are
unaffected, because `unserved-open` was labelled from an outcome field both
platforms do return. **This finding does not reopen the need-harvest
retirement.**

**What it costs.** E069's `CONFIRMED` verdict is withdrawn, and
`MISSION-OUTCOME.json`'s `vc_always_100_percent` and
`instrument_validated_outside_software` cannot be recorded as observed. The
corrected statement is narrower and survives: **`view_count` is
Stack-Exchange-shaped.** It is a real arrival measure where a platform
publishes one, and every software-arm reading of it in this record
(E063, E066, E069, E070) is missing rather than zero. It also retires a route
rather than opening one — carrying `view_count` into software corpora to see
arrivals E063 could not see is now known to be **impossible from those APIs**,
not merely unmeasured, so a fresh observation has to come from a surface that
publishes arrivals.

**Ceiling:** scoped to the public documented API response objects, because
that is the only surface E063/E066 harvested and the only one a reproduction
can use. This does **not** claim HN and GitHub expose no view counters
anywhere; a web UI or an undocumented endpoint is untested, and GitHub's
per-issue `reactions.total_count` was probed for and is not an arrival count.
The claim is the narrow one that blocks the landing: the corpora carry no
arrival field, so the software-arm cell cannot be a measured zero.

**A second defect, found by using the allocator to write this entry.** F097's
own findings row quotes the bike serial `SNACEOSF18391`, and the allocator's
cell pattern had no word boundary — so the serial's `F183` counted as a defined
finding and `origin id next F` handed out **F184**, skipping 83 numbers. The
rule against counting a citation as an allocation was already written in the
same module, and the stricter pattern existed next door in `identifiers.py`.
Repaired, falsified against its own bytes, and recorded as **defect 26**.
