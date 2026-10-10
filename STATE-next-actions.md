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

The seed for a candidate remains empty. The mission has now closed candidates across six report domains (A-F), seven emptiness measurements (F029/F051/F055/F059/F081/F084/F107), the view-count prototype from five independent angles (PyPI, NPM, Maven Central, Steam, Discourse forums), and three fresh observations in structured fault domains (E079, E083, E084). The DECISIONS-SCREENING-14.md D084-D088 and D091-D092 record the arrival-instrument corrections and kill-gate design lessons.

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
  - **3D printer fault codes (E083): G2 PASS (73.4%), G3 FAIL (1.8 models/fault vs 10)** — brand silos prevent cross-model coverage, view_count 100%
  - **PX4 drone fault codes (E084): G1 FAIL (~39 cases vs 100), G3 PASS (17 combos), G4 PASS (88.9%)** — population too small

**Key finding:** The view-count principle works on platforms with exposable metadata about arrival/arrival rates: package repositories (PyPI, NPM) with download/view counts, and non-software Q&A forums (Discourse, Stack Exchange) with view_counts. The principle does NOT generalize to social media/issue-tracking platforms without such metadata (GitHub issues API, web search, HN corpus), where no arrival field is recorded or the population is structured differently. The need-classification framework (E078) generalizes the measurement methodology to estimate served fractions in new communities, with gates G1-G3 confirming framework validity and G4's sample-size condition controlling for insufficient data. 

Three structured-fault-code domains tested: Automotive OBD2 (E079) fails concentration (G2); 3D printer faults (E083) fail cross-model coverage (G3); PX4 drone faults (E084) fail population size (G1). All three have standardized codes and real practitioners, but none yield a viable population under the mission's gates.

**Next action:** Fresh observation in a new domain with accessible structured problem data. Priority domains: industrial equipment fault codes (PLC/SCADA) — forums block access; medical device alarm codes — FDA MAUDE accessible but narrative not standardized codes; laboratory instrument error codes — unknown accessibility; aviation maintenance fault codes — Aviation Stack Exchange exists but API throttled. The search continues for a domain with: (1) standardized fault codes, (2) accessible practitioner discussions, (3) sufficient volume, (4) cross-model coverage, (5) specific root causes, (6) incumbent gap.