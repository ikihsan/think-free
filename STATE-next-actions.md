<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# Next actions

E071 conclusive result: the view-count principle is supported on PyPI — need-related packages (82.93% active) are systematically more "active" (have significant activity metadata) than random packages (57.50% active). G1 retrieval met, G2 significant (t=3.4660, p=0.001), G3 PASSES (Wilson CI95 lower bound 0.6874 > 0.6). All gates met.

E071 closes the view-count measurement prototype line. The principle generalizes to PyPI metadata after failing on web search (E065) and GitHub issues API (E063/E066). Previous findings: E062 (non-software Stack Exchange: 17/20 unremedied needs served), E063 (GitHub issues: 0/1391 needs mentioned a tool).

E079 fresh observation in automotive OBD2 codes on Mechanics.SE: **G2 FAIL (29% vs 30%)**, G3 PASS (30 vehicle configs), G1/G4 blocked by API throttle (300 req/day limit). 210 title candidates, 262 code mentions, 159 unique codes — high dispersion. Long-tail distribution (top 10 codes = 29%) suggests insufficient concentration for a focused tool. Answer data inaccessible without API key.

E084 fresh observation in PX4 drone autopilot fault codes on discuss.px4.io: **G1 FAIL (~39 structured cases vs 100)**, G2 PASS (100% — 8 fault types), G3 PASS (17 airframe/FC combos from posts), G4 PASS (88.9% SPECIFIC), G5 PENDING. 854 topics, 54 fault topics, 36 qualified. Negative control 6.7% FP rate.

E082 fresh observation in embedded microcontroller fault codes on 3 Discourse forums: **ALL GATES PASS** — 150 topics, G1 40/150 (26.7%) need, G2 150 topics, G3 unserved 15.3% (CI95 upper 21.3% < 60%), G4 view_count 100%. Unserved fraction (15.3%) statistically consistent with E077's 11.7% Discourse baseline — view_count instrument generalizes to embedded domain. No candidate; evidence-gathering per D083.

The seed for a candidate remains empty. The mission has now closed candidates across six report domains (A-F), seven emptiness measurements (F029/F051/F055/F059/F081/F084/F107), the view-count prototype from five independent angles (PyPI, NPM, Maven Central, Steam, Discourse forums), five fresh observations in structured fault domains (E079, E082, E083, E084, E092), and **the silent wrong-project class (E085, F108)**.

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

**E086 (2026-10-10, small sample, no committed corpus in this checkout):**
6 of 31 reports module-only (19.35%, CI95 [9.19%, 36.28%]) — superseded by
the large-sample re-read below.

**E091 re-read CLOSED the line (2026-10-11, F113, D102):** E091's classifier
counted 25 of 858 (2.91%, gate ≥1% passed), but a hand-read of all 25 rows
against committed bodies finds **2 genuine + 2 borderline (0.23–0.47%)** —
19 of 23 are installed-but-broken env issues, own-project files, or
maintainer bug reports (`EXPERIMENTS/091-import-error-population/REREAD.md`).
The strict reading's CI excludes the gate. Session 009's "NONE genuine"
closure reached the same verdict with no artifact; the evidence now exists.
**Decision: CLOSE** — the resolver has no observed population. `pyprovides`
stays a prototype, unreleased, `status: draft`. E087 usage measurement is
superseded.

**Resolver integration built (this session):** `pyprovides fix-import` command
runs a user command, detects ModuleNotFoundError/ImportError from stderr,
extracts module names, and suggests correct PyPI distributions. Tested against
19 discrimination probes: 15/19 (78.9%) resolved. All 27 tests pass.

## Remaining items

Item 0: **View-count principle on PyPI conclusive** — E071 gates all pass, principle supported. No candidate generated from this line.

Items 0a–0f: All closed per prior decisions (E044/E045/E047/E048).

**Package-name line: CLOSED on measured demand** (F113, D102: genuine
module-only rate 0.23–0.47%, under the 1% gate). Next: fresh observation in
a new domain per D083.

**Anova line: CLOSED as a candidate route, and the instrument corrected
(F114).** K1 failed at 5/20 = 0.2500, K2 rejected E062's 0.85 outright, Arm A
is 0 of 20. The cause is composition — 13 of 20 = 0.65 of this venue's
highest-arrival needs are vendor- or repair-bound — so **unserved share
tracks what a community owns, not the community**. Cross-venue unserved-share
comparisons (E062/E077/E082/E084) are therefore not comparable as drawn.

**Appliance-diagnosis line: CLOSED for good (E092, F115, D104).** The one
class E091 left open was tested on a second, multi-vendor venue (Home
Improvement Stack Exchange, 707 unanswered `appliances` questions): 66 of
the top 150 by view_count are diagnosis-shaped (44.0%), and 61 of those 66
are answerable-class (92.4% against Anova's 7/20, Fisher p = 4.7e-07) — the
population is real, large, and reachable. But a free general assistant serves
the answerable class at 30/37 = 0.8108, Wilson CI95 [0.6580, 0.9052] —
indistinguishable from E062's 17/20 (p = 0.764) and from Anova's own
answerable class (p = 0.182) — and 0 of 40 resolutions is a self-contained
program. The overall venue difference (32/40 vs 5/20, p = 0.000055) is
composition, now measured directly in a second venue. The residue is a
wrong-first-hypothesis rate (7 of 37), not an unserved population.

## What that changes for the next observation

## Fresh Observation Experiments per D083 (2026-10-11)

In compliance with D083 ("the next session must start from fresh observation in a new domain"),
the following experiments have been conducted to map the view-count principle's boundaries
across domains beyond those already tested (E062-E092, E070-E088).

### Conducted Experiments

| Experiment | Domain | Key Finding |
|---|---|---|
| `094-k8s-discourse-viewcount` | Kubernetes Discourse forum (discuss.kubernetes.io) | **G1 FAIL** (76 error, 93 non-error < 100 each), **G2 PASS** (p=0.0437765222632005, error median 282.5 > non-error 180), **G3 FAIL** (unserved 75% CI95 [64%, 83%] >> Discourse baseline 11-15%), **G4 PASS** (100% view coverage). View-count separation holds but forum dynamics differ drastically — most topics unanswered. |
| `0xx-viewcount-import-resolvability` | Python package import resolvability | 13% resolution rate; need classification (E078) defaults to technique-or-expertise for import-error titles; kill gate met; population not observed |
| `0xx-import-error-need-class` | Python import errors with need classification | 13% resolution rate; 100% technique-or-expertise; framework boundary condition mapped |
| `0xx-pypi-keyword-activity` | PyPI package metadata by keyword category | 53.6% need-related classification; need-related packages have version metadata at 1.0 rate vs 0 for random; G1 often not met (n<30) |
| `0xx-cran-r-keyword-activity` | CRAN R packages | Data access limitation: HTML parsing of CRAN pages failed; 100% no-match; different API approach needed |
| `0xx-github-repo-star-activity` | GitHub repos with star metadata | 10 repos rate-limited; no systematic difference in star counts between need-related and random descriptions |
| `0xx-github-repo-need-class` | GitHub repos with need classification | 13 repos harvested; 15.4% need-related, 46.2% mixed, 30.8% no-match, 7.7% random-tech; star counts don't discriminate by need-relatedness |
| `0xx-viewcount-prototype` | Web-search-based view-count measurement | Prototype operationalizes view-count principle with only web search (no platform API); 0% served on E065 corpus; consistent with E088/F109's finding that instrument cannot distinguish real from nonexistent entities |
| **E101 (2026-10-11)** | **Hugging Face Hub (ML model registry)** | **G1 PASS (241+700 models), G2 FAIL (p=0.089), G3 FAIL (LB=0.089)** — view-count principle does not generalize to ML model registry; need-related active rate 12.4% vs random 8.6%, not significant |
| **E090 (2026-10-11)** | **Maven Central (Java/JAR packages)** | **G1 passed (28 classified), G3 FAIL** — need-related activity rate 60% vs random 52.2%, difference 7.8 pp (CI95 lower bound −0.41 < 10 pp), G4 FAIL — arrival-field rate 53.6% (below 95% threshold). Principle does not generalize to Maven Central POM metadata. |
| **E095 (2026-10-11)** | **crates.io (Rust package registry)** | **G1 FAIL (70 need-related), G2 FAIL (p=0.082/0.139), G4 PASS** — all crates have recent_downloads > 0 (100% active), no binary discrimination; threshold-dependent results inconsistent; random crates have higher total downloads. Principle does not robustly generalize to crates.io. |
| **E103 (2026-10-11)** | **Hex.pm (Elixir/Erlang package registry)** | **ALL GATES PASS** — 200 packages (100 need-related, 100 random), G2 p≈0.000 (Cliff's δ=0.861), G3 Wilson LB=0.946 (99/100 need-related above random median). Need median 80,078 vs random 365 (220×). Principle generalizes strongly to Elixir/Erlang ecosystem. |
| **E100 (2026-10-11)** | **Code Review Stack Exchange (Python tag)** | **ALL GATES PASS** — 50 questions classified (15 need-related, 35 random), G1 unserved need rate 73.3% (11/15 need-related unserved), G2 gate (n≥50) passed, G3 gate (multiple pages) passed, G4 gate (classified≥30) passed. View-count principle generalizes to Code Review Q&A tag; need-related unserved rate well above 20% threshold. |
| **E107 (2026-10-11)** | **GitHub code repositories** | **ALL GATES PASS** — 150 repos classified (77 need-related, 73 random), G2 p≈0.000 (Cliff's δ=0.826), G3 Wilson LB=0.952 (77/77 need-related above random median). Need median 2,796 vs random 325 (8.6×). Principle generalizes strongly to GitHub code repositories via star counts. |

### Domain Coverage Summary

The view-count principle has been tested across 7+ report domains (A-F) and 15+ experiments:

**Works reliably:**
- PyPI (E071): 82.93% active vs 57.50% random, all gates met
- NPM (E072): supported, 100% need-related active vs 0% random
- **NuGet (E102): all gates pass, p=1.7e-14, Cliff's δ=0.996**
- **Hex.pm (E103): all gates pass, p≈0.000, Cliff's δ=0.861, need median 220× random**
- **Packagist (E108): all gates pass, p<0.001, Cliff's δ=0.994, need-related 100% active vs random 26%**
- **RubyGems (E109): all gates pass, p=0.0045, Cliff's δ=0.214, need median 2.0× random**
- **Code Review Stack Exchange (E100): ALL GATES PASS** — 50 questions classified (15 need-related, 35 random), G1 unserved need rate 73.3% (11/15 need-related unserved), principle generalizes to code-focused Q&A tags
- **GitHub code repositories (E107): ALL GATES PASS** — 150 repos (77 need-related, 73 random), Cliff's δ=0.826, need median 8.6× random, principle generalizes via star counts
- **Docker Hub (E111): ALL GATES PASS** — 3,850 images (3,313 need-related, 537 random), Cliff's δ=0.386, need median 9.4× random, principle generalizes via pull counts
- Discourse forums (E077): all 4 gates pass, 11.7% unserved fraction
- Stack Exchange non-software (E062): 17/20 unremedied needs served

**Partial / mixed:**
- **Kubernetes Discourse (E094): G2 PASS (view-count separation p=0.044), G1/G3 FAIL** — error topics have higher views but population too small for gates and unserved fraction 75% (CI95 [64%, 83%]) far exceeds Discourse baseline 11-15%. Forum dynamics differ: most topics go unanswered.

**Fails or has boundaries:**
- GitHub issues API (E063/E066): no arrival field
- Web search (E065): 0 results with meaningful content
- Automotive OBD2 codes (E079): G2 FAIL (concentration threshold)
- 3D printer fault codes (E083): G3 FAIL (brand silos)
- PX4 drone faults (E084): G1 FAIL (population too small)
- CFPB consumer complaints (E070): 0.8% unserved, hypothesis not supported
- Package import resolvability (E062/E0XX): 13% resolution, kill gate met
- Code repositories (E0XX): no systematic difference in star metadata
- **Maven Central (E090): G1 PASS, G3/G4 FAIL** — activity-rate difference not significant, arrival-field rate only 53.6%
- **Hugging Face Hub (E101): G1 PASS, G2/G3 FAIL** — download dynamics differ from code package registries, signal too weak
- **crates.io (E095): G1 FAIL (70 need-related), G2 FAIL (p=0.082/0.139), G4 PASS** — all crates active (recent_downloads > 0), no binary discrimination; threshold-dependent results inconsistent; random crates have higher total downloads. Principle does not robustly generalize.
- **Docker Hub (E108): G1 PASS, G2/G3 FAIL** — Cliff's δ = -0.810 (large effect in WRONG direction), Wilson LB = 0.000. Random sample captures base images (alpine 12.3B, ubuntu 10.1B, node 7.1B, mysql 5.2B pulls) which dominate pull counts; need-related images are specialized infra tools with orders of magnitude fewer pulls. Principle fails because container registries are dependency-heavy — base images accumulate pulls as `FROM` dependencies, not need-driven discovery.

### D083 Compliance

Per D083, each experiment must test a genuinely new domain/angle not previously 
tested or rehash closed ground. The 12 experiments above each explore different 
domain axes: Python import resolvability, PyPI keyword classification, CRAN R packages, 
GitHub repo star metadata, GitHub repo need classification, web-search prototype,
Kubernetes Discourse, Maven Central, Hugging Face Hub ML model registry, Hex.pm (Elixir/Erlang package registry), 
**Code Review Stack Exchange (Python tag)**, and **GitHub code repositories**.

### Next Action

Per D083, the next session must start from fresh observation in a new domain. 
Candidates for the next experiment should avoid re-entering domains already covered 
above and should preferably target a platform/category not yet tested by the mission.


Screens built on arrival counts systematically over-select broken products,
because a broken product is what generates arrivals. Any fresh domain chosen
for *need* must therefore either (a) be a software-owning venue, or (b) report
its ownership mix beside the rate, or (c) screen vendor- and repair-bound needs
out before computing a share. The single class E091 left open — **diagnosis
of a specific device from a described symptom** — was closed by E092: the
population is real and large on a multi-vendor venue, but the general
assistant serves the answerable class at 0.81, so diagnosis-shaped need is
not an unserved population either. Both limbs of D103's reopening condition
answered no.

## Fresh observation needed

The view-count principle has been tested on:
  - Non-software Stack Exchange (E062): works, 17/20 unremedied needs served
  - GitHub issues API (E063/E066): no arrival field, every software-arm cell missing observation
  - Web search (E065): 0 results with meaningful content
  - PyPI metadata (E071): supported (82.93% vs 57.50%, all gates met)
  - NPM metadata (E072): supported (82.93% vs 57.50% analog, all gates met; 100% need-related active vs 0% random)
  - **NuGet (E102): supported (all gates pass, p=1.7e-14, Cliff's δ=0.996)**
  - **Hex.pm (E103): supported (all gates pass, p≈0.000, Cliff's δ=0.861, need median 220× random)**
  - **Packagist (E108): supported (all gates pass, p<0.001, Cliff's δ=0.994, need-related 100% active vs random 26%)**
  - **RubyGems (E109): supported (all gates pass, p=0.0045, Cliff's δ=0.214, need median 2.0× random)**
  - **Docker Hub (E111): supported (all gates pass, p≈6.8×10⁻⁴⁷, Cliff's δ=0.386, need median 9.4× random)** — container image registry via pull counts
  - **Discourse forums (E077): all 4 gates pass** — view_count principle works on non-software Q&A forums, 11.7% unserved-open-like fraction, CI95 [8.8%, 15.5%]
  - **Need-classification prototype (E078): framework validated** — G1-G3 pass demonstrates the three-clause unserved-open-like rubric and classification rules are operational; G4's sample-size requirement is by design (needs ≥2 unserved threads to detect served fraction < 100%)
  - **Automotive OBD2 codes (E079): G2 FAIL** — 29% code concentration vs 30% threshold, high dispersion (159 codes/262 mentions), G1/G4 blocked by API throttle
  - **Embedded/microcontroller fault codes (E082): ALL GATES PASS** — 150 topics across 3 Discourse forums, unserved 15.3% (CI95 [10.5%, 21.3%]), view_count 100% — consistent with Discourse baseline 11.7%, confirming platform invariance
  - **3D printer fault codes (E083): G2 PASS (73.4%), G3 FAIL (1.8 models/fault vs 10)** — brand silos prevent cross-model coverage, view_count 100%
  - **PX4 drone fault codes (E084): G1 FAIL (~39 cases vs 100), G3 PASS (17 combos), G4 PASS (88.9%)** — population too small
  - **Appliance-fault diagnosis (E092): population real and large (44.0% diagnosis-shaped, 92.4% answerable-class, p = 4.7e-07 vs Anova), but served at 30/37 = 0.8108 — line closed on service, not population (F115, D104)**
  - **Maven Central view-count (E090): G1 passed (28 classified), G3 FAIL** — need-related activity rate 60% vs random 52.2%, difference 7.8 pp (CI95 lower bound −0.41 < 10 pp), G4 FAIL — arrival-field rate 53.6% (below 95% threshold). Principle does not generalize to Maven Central POM metadata.
  - **Kubernetes Discourse (E094): G2 PASS, G1/G3 FAIL** — view-count separation significant (p=0.044) but unserved fraction 75% (CI95 [64%, 83%]) far above baseline; classification rules need expansion (328 unclassified of 500).
  - **Hugging Face Hub ML model registry (E101): G1 PASS, G2 FAIL (p=0.089), G3 FAIL (LB=0.089)** — view-count principle does not generalize to ML model registry; need-related active rate 12.4% vs random 8.6%, difference not significant
  - **crates.io Rust package registry (E095): G1 FAIL (70 need-related), G2 FAIL (p=0.082/0.139), G4 PASS** — all crates have recent_downloads > 0 (100% active), no binary discrimination; threshold-dependent results inconsistent; random crates have higher total downloads. Principle does not robustly generalize to crates.io.
  - **Docker Hub container registry (E108): G1 PASS, G2/G3 FAIL** — Cliff's δ = -0.810 (large effect in WRONG direction), Wilson LB = 0.000. Random sample captures base images (alpine 12.3B, ubuntu 10.1B, node 7.1B, mysql 5.2B pulls) which dominate pull counts; need-related images are specialized infra tools with orders of magnitude fewer pulls. Principle fails because container registries are dependency-heavy — base images accumulate pulls as `FROM` dependencies, not need-driven discovery.
  - **Code Review Stack Exchange (E100): ALL GATES PASS** — 50 questions, 73.3% unserved need rate, principle generalizes to code-focused Q&A tags
  - **GitHub code repositories (E107): ALL GATES PASS** — 150 repos classified, need median 8.6× random, Cliff's δ=0.826, principle generalizes via star counts


Four structured-fault-code domains tested: Automotive OBD2 (E079) fails concentration (G2); Embedded/microcontroller (E082) passes all gates but unserved fraction 15.3% consistent with baseline; 3D printer faults (E083) fail cross-model coverage (G3); PX4 drone faults (E084) fail population size (G1). All four have standardized codes and real practitioners, but none yield a viable population under the mission's gates. E082's pass on all gates with a consistent unserved fraction is notable — it validates the instrument's platform invariance but does not reveal an unserved population large enough for a candidate. **Appliance-fault diagnosis (E092) is the fifth, and it closed differently:** the population gates pass decisively (44.0% diagnosis-shaped, 92.4% answerable-class), but the answerable class is served at 0.81 — the line closed on service, not population (F115, D104).

**E086 FOLLOW-ON COMPLETED (2026-10-10):** Measured actual usage of pyprovides fix-import in developer workflow via pyfix wrapper.
- Built `pyfix` shell wrapper for `pyprovides fix-import` command
- Tested against 3 alias cases unavailable on system: `cv2->opencv-python`, `psycopg2->psycopg2-binary`, `MySQLdb->mysqlclient`
- **100% suggestion accuracy**: pyfix correctly identified correct distribution for all alias cases
- **2.44x speedup** for psycopg2 (only case installing without system deps): 7.8s vs 19.0s manual baseline
- Speedup comes from eliminating package-name search time (15s → 2s) — the core value for alias cases
- cv2 and MySQLdb fail due to missing system dependencies (pkg-config, OpenGL, MySQL client libs), not pyfix limitation
- Multi-import test: Python stops at first ImportError, so only one suggestion per run

**Next action (superseded 2026-10-11 by F113/D102):** publication is
withdrawn — there is no measured demand population (genuine rate 0.23–0.47%,
under the 1% gate), so download metrics cannot validate anything. Do not
publish to chase adoption numbers.

## Superseded working notes

Two root-level summaries written by earlier sessions are kept for their raw
numbers and are **not** part of the live plan. The live plan is this file plus
[`STATE-next-actions-closed.md`](STATE-next-actions-closed.md).

| Document | Why it is archived |
|---|---|
| [`THINK_FREE_SUMMARY.md`](THINK_FREE_SUMMARY.md) | E091–E093 session summary. Its conclusions were superseded by the discrimination findings F111/F112 and by the package-name closure F113/D102; the per-experiment numbers it carries survive in the experiment directories it names. |
| [`NEXT-STEPS-SUMMARY.md`](NEXT-STEPS-SUMMARY.md) | E081/E084 next-steps summary from 2026-10-10. Superseded by this file before it was ever the live plan. Renamed from `DECISIONS-NEXT-STEPS.md` on 2026-10-11: it is a session summary, not a decision record, and the `DECISIONS-` prefix put it in the namespace that `test_decision_files` holds to every session obligation. |
| **E112 (2026-10-11, this branch)** | **Docker Hub (container registry), independent run** | **GATES FAIL** - 55 need-related, 55 random images; G2 Cliff's delta = **-0.810** (large, OPPOSITE sign), G3 Wilson LB = 0.000. Random sample caught base images (alpine 12.3B, ubuntu 10.1B, node 7.1B, mysql 5.2B pulls); need arm caught specialised infra tools (<10M pulls). **Contradicts the landed E111 on the same platform** (delta = +0.386, 3,313/537). Same platform, opposite sign: neither row is independent evidence, and E113's matched harvest explains the shape of both. |