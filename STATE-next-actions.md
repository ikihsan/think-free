<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Next actions

E071 conclusive result: the view-count principle is supported on PyPI — need-related packages (82.93% active) are systematically more "active" (have significant activity metadata) than random packages (57.50% active). G1 retrieval met, G2 significant (t=3.4660, p=0.001), G3 PASSES (Wilson CI95 lower bound 0.6874 > 0.6). All gates met.

E071 closes the view-count measurement prototype line. The principle generalizes to PyPI metadata after failing on web search (E065) and GitHub issues API (E063/E066). Previous findings: E062 (Steam: 17/20 unremedied needs served), E063 (GitHub issues: 0/1391 needs mentioned a tool).

E079 fresh observation in automotive OBD2 codes on Mechanics.SE: **G2 FAIL (29% vs 30%)**, G3 PASS (30 vehicle configs), G1/G4 blocked by API throttle (300 req/day limit). 210 title candidates, 262 code mentions, 159 unique codes — high dispersion. Long-tail distribution (top 10 codes = 29%) suggests insufficient concentration for a focused tool. Answer data inaccessible without API key.

E084 fresh observation in PX4 drone autopilot fault codes on discuss.px4.io: **G1 FAIL (~39 structured cases vs 100)**, G2 PASS (100% — 8 fault types), G3 PASS (17 airframe/FC combos from posts), G4 PASS (88.9% SPECIFIC), G5 PENDING. 854 topics, 54 fault topics, 36 qualified. Negative control 6.7% FP rate.

E082 fresh observation in embedded microcontroller fault codes on 3 Discourse forums: **ALL GATES PASS** — 150 topics, G1 40/150 (26.7%) need, G2 150 topics, G3 unserved 15.3% (CI95 upper 21.3% < 60%), G4 view_count 100%. Unserved fraction (15.3%) statistically consistent with E077's 11.7% Discourse baseline — view_count instrument generalizes to embedded domain. No candidate; evidence-gathering per D083.

The seed for a candidate remains empty. The mission has now closed candidates across six report domains (A-F), seven emptiness measurements (F029/F051/F055/F059/F081/F084/F107), the view-count prototype from five independent angles (PyPI, NPM, Maven Central, Steam, Discourse forums), four fresh observations in structured fault domains (E079, E082, E083, E084), and **the silent wrong-project class (E085, F108)**.

## The one continuation worth making (2026-10-10)

**E085 closed a linter and left a resolver.** The class it measured is real
(reproduced by hand: `pip install Crypto` → exit 0, wrong project plus 8 of its
dependencies, `import Crypto` then fails) and deptry 0.25.1 cannot detect it at
all. But it occurs in **~0.6% of imported modules** (3 of 500, after the
precision gate removed three instrument artifacts), which is not worth a CI
gate. **Do not rebuild the linter.**

What E085 did establish, and did not test, is that the *instrument* is cheap
and correct: two HTTP `Range` requests read a wheel's central directory and
return every module a distribution ships, with **nothing installed**. deptry
cannot do this before an install, and names a module without ever naming its
provider.

**The single most useful next action:** measure whether *"which distribution
provides this module"* is actually asked. The denominator is real
`ImportError` / `ModuleNotFoundError` text that names a module and no
distribution — Stack Overflow, GitHub issues, CPython and library issue
trackers. If that population is large, the resolver has a use that does not
depend on the 0.6% figure, and `pyprovides/` is already built, tested and
honest about its limits. If it is small, the whole package-name line closes and
this record's E064/E070/E085 arc is finished for good.

Declared kill gate, before the run: **if the rate of real reports that name a
module and no distribution is under 1% of Python import-error reports, close
the line and stop.** Do not run it on package registries; the denominator must
be *questions people asked*, which is the `view_count` population E062
established and no registry exposes.

## Remaining items

Item 0: **View-count principle on PyPI conclusive** — E071 gates all pass, principle supported. No candidate generated from this line.

Items 0a–0f: All closed per prior decisions (E044/E045/E047/E048).

## Fresh observation needed

The view-count principle has been tested on:
  - Steam (E062): works, 17/20 unremedied needs served
  - GitHub issues API (E063/E066): no arrival field, every software-arm cell missing observation
  - Web search (E065): 0 results with meaningful content
  - PyPI metadata (E071): supported (82.93% vs 57.50%, all gates met)
  - NPM metadata (E072): supported (82.93% vs 57.50% analog, all gates met; 100% need-related active vs 0% random)
  - **Discourse forums (E077): all 4 gates pass** — view_count principle works on non-software Q&A forums, 11.7% unserved-open-like fraction, CI95 [8.8%, 15.5%]
  - **Need-classification prototype (E078): framework validated** — G1-G3 pass demonstrates the three-clause unserved-open-like rubric and classification rules are operational; G4's sample-size requirement is by design (needs ≥2 unserved threads to detect served fraction < 100%)
  - **Automotive OBD2 codes (E079): G2 FAIL** — 29% code concentration vs 30% threshold, high dispersion (159 codes/262 mentions), G1/G4 blocked by API throttle
  - **Embedded/microcontroller fault codes (E082): ALL GATES PASS** — 150 topics across 3 Discourse forums, unserved 15.3% (CI95 [10.5%, 21.3%]), view_count 100% — consistent with Discourse baseline 11.7%, confirming platform invariance
  - **3D printer fault codes (E083): G2 PASS (73.4%), G3 FAIL (1.8 models/fault vs 10)** — brand silos prevent cross-model coverage, view_count 100%
  - **PX4 drone fault codes (E084): G1 FAIL (~39 cases vs 100), G3 PASS (17 combos), G4 PASS (88.9%)** — population too small

**Key finding:** The view-count principle works on platforms with exposable metadata about arrival/arrival rates: package repositories (PyPI, NPM) with download/view counts, and non-software Q&A forums (Discourse, Stack Exchange) with view_counts. The principle does NOT generalize to social media/issue-tracking platforms without such metadata (GitHub issues API, web search, HN corpus), where no arrival field is recorded or the population is structured differently. The need-classification framework (E078) generalizes the measurement methodology to estimate served fractions in new communities, with gates G1-G3 confirming framework validity and G4's sample-size condition controlling for insufficient data. 

Four structured-fault-code domains tested: Automotive OBD2 (E079) fails concentration (G2); Embedded/microcontroller (E082) passes all gates but unserved fraction 15.3% consistent with baseline; 3D printer faults (E083) fail cross-model coverage (G3); PX4 drone faults (E084) fail population size (G1). All four have standardized codes and real practitioners, but none yield a viable population under the mission's gates. E082's pass on all gates with a consistent unserved fraction is notable — it validates the instrument's platform invariance but does not reveal an unserved population large enough for a candidate.

**Next action:** Fresh observation in a new domain with accessible structured problem data. Priority domains: industrial equipment fault codes (PLC/SCADA) — forums block access; medical device alarm codes — FDA MAUDE accessible but narrative not standardized codes; laboratory instrument error codes — unknown accessibility; aviation maintenance fault codes — Aviation Stack Exchange exists but API throttled. The search continues for a domain with: (1) standardized fault codes, (2) accessible practitioner discussions, (3) sufficient volume, (4) cross-model coverage, (5) specific root causes, (6) incumbent gap.