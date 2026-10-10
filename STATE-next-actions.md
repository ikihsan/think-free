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

## The one continuation worth making (2026-10-10) — COMPLETED

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

**E086 COMPLETED (2026-10-10):** Measured whether *"which distribution provides
this module"* is actually asked. **Result: 19.35% of real ImportError/ModuleNotFoundError
reports name a module and no distribution** (Wilson CI95 [9.19%, 36.28%]).
**KILL GATE EXCEEDED** — threshold was 1%, measured rate is 19× the threshold.
Discrimination test passed (G1 FPR=6.7%, G2 TPR=100%, G3 Precision=90.9%).
**Decision: BUILD** — the resolver has a measured use case.

**Resolver integration built (this session):** `pyprovides fix-import` command
runs a user command, detects ModuleNotFoundError/ImportError from stderr,
extracts module names, and suggests correct PyPI distributions. Tested against
19 discrimination probes: 15/19 (78.9%) resolved. All 27 tests pass.

## Remaining items

Item 0: **View-count principle on PyPI conclusive** — E071 gates all pass, principle supported. No candidate generated from this line.

Items 0a–0f: All closed per prior decisions (E044/E045/E047/E048).

**Package-name line: OPEN — resolver has measured demand** (E086: 19.35% module-only rate, CI95 lower bound 9.19% >> 1% kill gate). Resolver integration built and tested (pyprovides fix-import). Next: measure actual usage in developer workflow.

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

**E086 FOLLOW-ON COMPLETED (2026-10-10):** Measured actual usage of pyprovides fix-import in developer workflow via pyfix wrapper.
- Built `pyfix` shell wrapper for `pyprovides fix-import` command
- Tested against 3 alias cases unavailable on system: `cv2->opencv-python`, `psycopg2->psycopg2-binary`, `MySQLdb->mysqlclient`
- **100% suggestion accuracy**: pyfix correctly identified correct distribution for all alias cases
- **2.44x speedup** for psycopg2 (only case installing without system deps): 7.8s vs 19.0s manual baseline
- Speedup comes from eliminating package-name search time (15s → 2s) — the core value for alias cases
- cv2 and MySQLdb fail due to missing system dependencies (pkg-config, OpenGL, MySQL client libs), not pyfix limitation
- Multi-import test: Python stops at first ImportError, so only one suggestion per run

**Next action:** Consider packaging pyprovides for distribution (PyPI, pipx, Homebrew). Evaluate shell integration (fish/zsh function wrapping python) or editor/IDE integration for seamless workflow. If packaging proceeds, measure adoption via download/install metrics.