<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# The D083 fresh-observation sweep, 2026-10-11 to 2026-10-12 — STOPPED

Split out of [`STATE-next-actions.md`](STATE-next-actions.md), which was at 375
of 300 lines. **This is the record of a route that was stopped, kept because its
two deaths are the reason the route is not reopened casually.**

E113 re-ran E107's own platform with a matched harvest and found the published
effect was a harvest artifact: E107's need arm was drawn from
`topic:web-framework` and its random arm from `topic:utils`, both sorted by
stars, so "need 8.6x random" compared the most-starred web frameworks against
the most-starred utility libraries. Within stratum the effect is
**δ = +0.0746, stratified permutation p = 0.183**. The shared classifier also
labelled only **196 of 700** rows (28%), and no experiment on the line had a
coverage gate, so a 28% screen was recorded as a 100% measurement (F116,
D105).

The table below is preserved as **what was believed and on what evidence**, not
as a current claim. Every "ALL GATES PASS" row on it is `untested` on a matched
harvest.

---

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

**E128 completed (2026-10-13): the preflight line reopens, conditionally.**
E125 §7's open question — does a harness's run output directory have the
shape preflight needs? — answered: **yes.** The run output has predictions
and reviews joined by `index`. The tax is a per-harness adapter (a few
lines), not a loader library. Next: measure the adapter on a second harness.

**E129 completed (2026-10-13): the openai/evals adapter is also a few lines.**
`openai/evals` has a fundamentally different output structure (single
append-only event stream), but the adapter is also a few lines: parse the
event stream, filter for "match" events, extract `sample_id` and `data`.
**Both harnesses have the shape preflight needs, and the adapter is a few
lines for both.** The preflight line reopens — the tool can be pointed at
any harness's run output with a small per-harness adapter. Next: prototype
the adapter and measure its size on a third harness, or release the tool
with a per-harness adapter interface.
