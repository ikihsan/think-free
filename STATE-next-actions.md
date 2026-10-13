<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# Next actions

> **READ FIRST (2026-10-12).** The view-count domain sweep is **STOPPED**
> (E113, F116, D105). E113's matched-harvest control of E107 showed the
> effect is a harvest artifact (δ 0.826 → 0.075, stratified p=0.183) and the
> shared classifier labels only 28% of a representative pool. Every
> "ALL GATES PASS" below that came from this line is **`untested` on a matched
> harvest, not confirmed**. Do not run another registry sweep. See
> [`EXPERIMENTS/113-viewcount-matched-harvest/`](EXPERIMENTS/113-viewcount-matched-harvest/README.md).

E071 conclusive result: the view-count principle is supported on PyPI — need-related packages (82.93% active) are systematically more "active" (have significant activity metadata) than random packages (57.50% active). G1 retrieval met, G2 significant (t=3.4660, p=0.001), G3 PASSES (Wilson CI95 lower bound 0.6874 > 0.6). All gates met. **Superseded by E113/F116 as unconfirmed on a matched harvest.**

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

**E091 re-read CLOSED the line (2026-10-11, F113, D102):** genuine module-only
rate 0.23–0.47%, under the 1% gate. **Decision: CLOSE.**

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
| **E107 (2026-10-11)** | **GitHub code repositories** | **WITHDRAWN by E113 (F116).** The "ALL GATES PASS, δ=0.826, need median 8.6× random" result is a **harvest artifact**: 80/80 need rows carry `topic:web-framework` and 80/80 random rows carry `topic:utils`, both star-sorted, before any classifier runs. E113's matched harvest gives within-stratum δ=+0.075, stratified p=0.183. The classifier also labels only **28%** of a representative pool. |
| **E113 (2026-10-12)** | **Matched-harvest control of E107** | **The view-count effect does not survive a matched harvest.** E107's δ=0.826010 reproduced exactly from its own data, then collapses to +0.0746 within stratum (permutation p=0.183, 20k iters). Two defects: asymmetric harvest (need vs utils topic), and unanchored substring matching (`ai` in `email`, `base` in `database`). Coverage: 196/700 rows labelled; 458 match neither vocabulary. **F116, D106.** |
| **E112 (2026-10-11, this branch)** | **Docker Hub, independent second run** | **GATES FAIL** - 55 need-related, 55 random images; G2 Cliff's delta = **-0.810** (large, OPPOSITE sign), G3 Wilson LB = 0.000. Random arm caught base images (alpine 12.3B, ubuntu 10.1B, node 7.1B, mysql 5.2B pulls); need arm caught specialised infra tools (<10M pulls). **Contradicts the landed E111 on the same platform** (delta = +0.386, 3,313/537). Opposite signs on one platform: neither is independent evidence, and E113's matched harvest is the shape of explanation for both. |

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
- **GitHub code repositories (E107): WITHDRAWN by E113** — the δ=0.826 was a harvest artifact (need vs `utils` topic); not an independent confirmation (F116)
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

**The D083 domain sweep is STOPPED (E113, F116, D106).** It named "fresh
observation in a new domain" as the next action; that is withdrawn, because the
sweep was measuring its own sampling design. E113 found E107's arms were drawn
from two *different* topics, both sorted by the outcome metric, so "need 8.6×
random" compared the most-starred web frameworks against the most-starred
utility libraries. Under a matched harvest on E107's own platform the effect is
**δ=+0.075, stratified p=0.183**.

**Do not run another registry sweep.** Every remaining "ALL GATES PASS" on this
line (PyPI, NPM, NuGet, Hex.pm, Code Review SE) used the same shared classifier
and the same "sort the random arm by the outcome metric" pattern, so they are
`untested` on a matched harvest, not confirmed.

**The venue sweep is complete (E126/E127, 2026-10-13).** Every venue class
has been measured and all are served. The program-shaped residue — 6 rows
from E126 — is served by prior art (E127): all 6 are standard programming
tasks that existing tools (Python stdlib, BeautifulSoup, Postman) already
serve. No candidate population exists in any venue class. The mission needs
a new direction: a completely new domain, or a meta-question about the
mission's own method.

**What would justify reopening the line,** in order:

1. **A classifier that covers its population.** E113 measured 196 of 700 rows
   labelled (28%), with 458 matching *neither* vocabulary. This is the binding
   constraint and it is a buildable engineering problem, not a research one.
2. **A coverage gate declared before the run** — the fraction of the population
   the labeler assigns at all, with a floor. No experiment on this line had
   one, which is how a 28% screen came to be reported as a 100% measurement.
3. **A matched harvest as the default design**, not a control added after a
   positive.

None of this is a candidate and none is a product. It is the minimum needed
before the line's next result would mean anything.


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

**E126 completed (2026-10-13): the venue sweep is complete, and every venue
class is served.** Stack Overflow — the flagship software-owning venue —
was screened (299 rows: 292 question-shaped, 6 execution-shaped, 1 other)
and the answerable class was attempted by a free general assistant at
**27/40 = 0.6750, Wilson CI95 [0.5202, 0.7992]** — the lower bound clears
the declared 0.50 gate. G0 discrimination passed (10/10, 10/10). The
composition finding extends to the last untested venue class: the
execution-shaped share is 6/299 = 0.0201, and the two draw strata differ
by 10x (Arm A votes 0.0050 vs Arm B creation 0.0500). The one residue is
**6 program-shaped rows** — the class where a self-contained program (not
an answer) could serve. Whether a tool could serve them is `untested`;
they were not attempted (the protocol's sample was the answerable class).
No candidate. The venue sweep is **closed**.

**E127 completed (2026-10-13): the program-shaped residue is served by prior
art.** All 6 program-shaped rows from E126 are well-defined programming
tasks that a self-contained program can solve, and all 6 are already served
by existing tools (Python stdlib, BeautifulSoup, Postman test scripts). The
asker needs to learn existing tools, not a new tool. **The venue sweep
closes completely — every venue class is served, and the program-shaped
residue is served by prior art.** No candidate.

## E114 closed the value-grounding line (2026-10-12)

The prototype-first route the brief asks for was taken once, in full: build the
thing, validate it against adversarial controls, then point it at real answers.
The build succeeded and the population turned out to be served.

- **0 of 374 values fabricated** (Wilson 95% upper bound 0.0098; kill gate 0.02).
  Five real Federal Register final rules, read in full, asked for every dollar
  amount, date and citation. **The widely repeated claim that models invent
  numbers when reading a document is withdrawn for this population.**
- **The verifier is dead, not the subject.** Recall 1.0000 on corrupted answers,
  0.0069 false alarms on verbatim spans, then 0.3717 of real values flagged with
  a false-positive rate of 1.00. Both controls were too easy; faithful paraphrase
  with nothing invented is the arm that was never built (F118, D106).
- **Kept, unreleased, `status: draft`:** `EXPERIMENTS/114-value-grounding/` —
  `ground.py` is a working, deterministic, stdlib-only checker and is worth
  reusing as a *ranker* (a flagged value is worth a human glance) even though it
  is worthless as a *gate*.

**What would reopen this, and it is not cheap:** a verifier whose paraphrase
step uses a language model. Its false-positive rate on faithful paraphrase is the
one number E114 never measured, because building it means paying the cost the
tool was meant to avoid.


## Domain record (superseded by E126/E127 — venue sweep complete)

The view-count principle has been tested on 15+ domains. All "works
reliably" rows are **`untested` on a matched harvest** (E113/F116).
The full per-domain record is in the experiment directories.

**Key finding (SUPERSEDED BY E113/F116 — read this first):** the results
below were produced with two defects now measured — an **asymmetric harvest**
(need arm and random arm drawn from different queries, sorted by the outcome
metric) and an **unanchored substring classifier** that labels only ~28% of a
representative population. E113 re-ran E107's platform with a matched harvest
and the effect collapsed to δ=+0.075, p=0.183. **None of the "works reliably"
rows below is an independent confirmation** until re-run on a matched harvest
with a classifier that covers its population. What follows is preserved as the
record of what was believed and on what evidence, not as a current claim.

Originally claimed: the view-count principle works on platforms with exposable metadata about arrival/arrival rates: package repositories (PyPI, NPM, **NuGet, Hex.pm**) with download/view counts, non-software Q&A forums (Discourse, Stack Exchange) with view_counts, code-focused Q&A tags (**Code Review Stack Exchange**), and **code hosting platforms (GitHub repositories) with star counts**. The principle does NOT generalize to social media/issue-tracking platforms without such metadata (GitHub issues API, web search, HN corpus), nor to Maven Central (Java/JAR packages), where the activity-rate difference between need-related and random packages is not observed (need-related 60% vs random 52.2%, difference 7.8 pp, Wilson CI95 lower bound −0.41 < 10 pp) and the arrival-field rate is only 53.6% (below the 95% threshold). **It also does not generalize to ML model registries (Hugging Face Hub)**, where download dynamics differ from code package repositories — both need-related and random models have low active rates, and the signal is too weak. **It also does not robustly generalize to crates.io (Rust package registry)**, where all crates have recent_downloads > 0 (100% active), eliminating binary discrimination, and threshold-based analyses yield inconsistent results. **It also does not generalize to Docker Hub (container registry)**, where base image dependency pulling (alpine 12.3B, ubuntu 10.1B, node 7.1B pulls) dominates over need-driven discovery — the platform's layered filesystem architecture makes foundational images accumulate massive pull counts regardless of "need-relatedness," reversing the expected effect (Cliff's δ = -0.810). The need-classification framework (E078) generalizes the measurement methodology to estimate served fractions in new communities, with gates G1-G3 confirming framework validity and G4's sample-size condition controlling for insufficient data. **Kubernetes Discourse shows the view-count separation effect (G2) holds on a software-focused Discourse forum, but the unserved fraction is drastically higher than other Discourse forums — suggesting forum culture/community dynamics dominate the unserved metric.** **Hex.pm shows the strongest separation yet observed (need median 220× random median), reinforcing that mature, infrastructure-heavy package ecosystems exhibit the principle.** **GitHub code repositories show strong separation (need median 8.6× random) — WITHDRAWN by E113: that number came from comparing the most-starred `web-framework` repositories against the most-starred `utils` repositories.**

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