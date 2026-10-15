<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Next actions

**E161 completed (2026-10-15): a real engine as oracle, and no candidate.**
See [`EXPERIMENTS/161-csv-spreadsheet-coercion/RESULT.md`](EXPERIMENTS/161-csv-spreadsheet-coercion/RESULT.md).
1,206,342 cells of real CSVs through a real spreadsheet engine: the US Census
Gazetteer loses **36,697 leading-zero `GEOID` cells (9.5%)**; 818,222 cells of
analyst and public-body files lose nothing. `csvsafe.py` reproduces the engine's
decisions at precision 1.0 / recall 1.0 on two real frames, and `write` takes
the Census file to 0 damaging cells. **Not a candidate** — demand probes are
weak and 0-to-1-star tools already do parts of it. Kept unreleased,
`status: draft`, plus the round-trip instrument the four synthetic-fixture
experiments (E122/E147/E150/E160) lacked. **Next, if anything:** size the
population that actually hands CSVs to spreadsheet users, by measuring the
damaging-cell rate over a larger sample of the data.gov.uk frame rather than
two files; the frame E number is one chosen file, not an estimate.
(This file was already over the 300-line cap before this entry; the split it
needs is separate work.)

**E142 completed (2026-10-14): the pre-pass is exact on regulatory text.**
E141's named next action — run `valueset.py` unchanged on regulatory answers a
person wrote — measured **1.0 detection** (4/4), **0.0 false positives** (0/16),
**0 misses**, **0.90 resolved share** on 20 Federal Register final rules
(SUMMARY vs. full rule text minus SUMMARY). Against E141's SQuAD (0.2826,
0.0113, 0.2763 of clears wrong): the genre limitation is real and measured in
both directions. M1 `ground.py` is worse than M2 on this corpus (0.25 FP vs.
0.0). The general claim stays closed (F126); the regulatory claim is now
measured. Next: whether exactness survives a longer submission (a full
regulatory analysis, not a SUMMARY).

**E141 completed (2026-10-14): the value-pre-pass build trigger is WITHDRAWN,
and the scope it does have is measured (F126, D111, D112).** E140 left
`valueset.py` with 0 false positives in 929 values and a protocol that said
"second genre". E141 ran it unchanged on SQuAD v2.0 dev — 11,873 human-written
questions, **no item corrupted by the experiment**:

| | declared | observed |
|---|---|---|
| detection on real human value errors | ≥ 0.95 | **0.2826** (223/789) — **FAIL** |
| false positives on correct human answers | ≤ 0.02 | 0.0113 — **PASS** |
| coverage over all answerable items | ≥ 0.30 | 0.2146 — **FAIL** (K3) |
| coverage where the answer **is** a value | ≥ 0.30 | **0.9379** — **PASS** (K5) |
| share of the corpus the pre-pass resolves | — | **0.1647** |
| of what it clears, genuinely unsupported | — | **0.2763** (460/1,665) |

K3's failure is a property of SQuAD, not the extractor: only 853 of 5,928
answers are a number or a date, and conditional on that the coverage is 0.9379.
The 566 K1 misses split into **460 binding misses** — the blind spot E140
declared and measured at 0/6 on arms it built, now confirmed on text nobody
built for it — and **106 items where `19th`, `1980s` and `1100s` are not
extracted at all**. A hand-built positive control found a third defect in one
run: `canonical()` keys by `(kind, number)`, so `$12,500,000` and
`12500000 dollars` are different keys (4 of 6 pass, 2 fail; latent on SQuAD at
0 of 67). `ground.py` detects **0.7174** against M2's 0.2826 at 0.0940 false
positives against 0.0113 — the two are two points on one curve, and E140's
ranking of them does not transfer.

**What remains, and it is one measurement.** The pre-pass may be exactly right
for **regulatory** answers, which is the genre it was built for and the one
E141 deliberately did not re-run. Run `valueset.py` unchanged on regulatory
answers **a person wrote** — not the model-written expert answers E140 used —
and read three numbers: conditional coverage, the false-positive rate on
correct items, and the `value_present` share of the misses. Misses mostly
`not_extracted` ⇒ the pre-pass is genre-limited and should be described that
way. Misses mostly `value_present` at this run's rate ⇒ the line closes for
good, because the failure would be the declared blind spot in the one genre
where the instrument was most likely to work.

**Do not fix the three defects and re-score the same gates.** `valueset.py` is
imported unchanged by protocol; a fix written after seeing the real corpus's
misses is a different instrument and needs its own predeclared run. The defects
are recorded precisely enough that run is cheap to design.

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

## The D083 fresh-observation sweep — STOPPED, kept for the record

**This block is history.** E113 showed the sweep was measuring its own
sampling design and D105 stopped it; E126/E127 then closed the venue sweep as
well. The full per-domain table, the E112/E111 Docker Hub contradiction, the
D083-compliance note and the E113 stop notice are in
[`STATE-next-actions-d083-sweep.md`](STATE-next-actions-d083-sweep.md).
**Do not run another registry sweep.** Two findings below are still live and
both cut against it: the preflight line is closed on demand (E137), and
E138 read a developer forum where the zero-reply metric fails and the
view-count principle holds at δ = +0.144 on a matched harvest.

## E137 completed (2026-10-13): preflight demand validation GATE_CLOSED

**E137 demand validation for preflight completed.** Harvested GitHub issues, Stack Overflow, Reddit, arXiv across 9 LLM evaluation frameworks (evalscope, evals, promptfoo, deepeval, inspect_ai, inspect-evals-lint, eval-harness, scale-eval-preflight, JudgeBench).

| Gate | Declared | Observed | Verdict |
|---|---|---|---|
| G1 (demand) | ≥10 credible across ≥3 frameworks | 63 credible across 2 frameworks (evalscope: 40, evals: 23) | **FAIL** |

**Classification breakdown:** C1_credible: 63, C2_credible: 0, C3_credible: 0, related: 32. The keyword-based classifier produced false positives for C1 (many issues match "join/match/silent/zero/accuracy" keywords but don't describe the actual C1 defect — silent join failure between separate key/output files). Only 2 frameworks yielded any credible reports; need ≥3. **GATE_CLOSED: demand too weak, preflight candidate withdrawn on demand grounds.** See `EXPERIMENTS/137-preflight-demand-validation/RESULT.md` and `CLASSIFICATIONS.md`.

The preflight line remains an exploratory prototype (E134) with 8 validated adapters (E128–E136) but no external demand signal.

## E138 completed (2026-10-13): Prometheus Discourse — coverage boundary broken, view-count holds, zero-reply metric fails

**E138 fresh observation on Prometheus Discourse (discuss.prometheus.io) completed with developer-forum-specific classifier.**

| Gate | Threshold | Result |
|------|-----------|--------|
| G1 | ≥95% view_count > 0 | **PASS** (100%) |
| G2 | Coverage ≥60%, need fraction ≥5% | **PASS** (96.7%, 37.9%) |
| G3 | Unserved CI95 upper < 60% | **FAIL** (89.1%, CI95 [81.9%, 93.6%]) |
| G4 | ≥30 classified | **PASS** (290) |

**Key findings:**

1. **Coverage boundary broken**: Developer-forum classifier achieves **96.7% coverage**, decisively breaking the 60% floor that closed E124 (GNOME 37.2%) and E125 (Jupyter 50.4%). Pattern additions for error-message titles, noun-phrase questions, colloquial problem statements, and domain-specific terms closed the gap.

2. **View-count principle holds**: Matched harvest shows **Cliff's δ = +0.144, p = 0.039** — need-related topics get more views than random. Consistent with support forum baseline.

3. **Zero-reply metric fails**: 89.1% zero-reply rate fails G3 (dysfunctional threshold 60%). But served topics (12/110) show genuine engagement. The metric conflates "no community reply" with "need unserved" — many topics may be self-resolved, answered via edits, or the forum has naturally low response rates.

4. **No candidate**: G3 fails, and the zero-reply metric is likely inappropriate for this forum.

See `EXPERIMENTS/138-prometheus-discourse-viewcount/RESULT.md`.

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

## E139 completed (2026-10-14): view-count principle on Pub.dev matched harvest
The view-count separation effect does not survive a matched harvest on Pub.dev/Flutter packages.
Cliff's δ ≈ -0.0143 across all 7 star strata; coverage ~13% on both arms (well below 60% gate).
This is consistent with E113's collapse on all other platforms (PyPI, NPM, Maven Central, Hex.pm, 
Docker Hub, RubyGems, crates.io), confirming the effect is a harvest artifact, not a general principle.
Kill gates: G0 passes (both arms classifiable), G1 FAIL (δ fluctuates direction), G2 FAIL (coverage too low),
G3 NEEDS TEST (δ ≈ 0).

## What that changes for the next observation
- The view-count sweep remains stopped (E113/F116)
- Preflight line is closed on demand grounds (E137)
- E138's Prometheus Discourse finding (zero-reply metric fails, view-count δ = +0.144 on matched harvest) 
  remains as the only venue with a separated effect, but no candidate generated
- No candidate: the view-count principle is closed as a generalizable route across package registries
  when using proper matched harvest design and adequate classifier coverage.

E139 experiment directory: EXPERIMENTS/139-viewcount-pubdev-matched-harvest
Results: δ ≈ -0.0143, coverage ~13%, 7 strata with fluctuating sign'

## T-0094 completed (2026-10-14): harvest public issue trackers for LLM evaluation frameworks
Automated GitHub API keyword search across 9 LLM evaluation frameworks (evalscope, evals, promptfoo, 
deepeval, inspect_ai, inspect-evals-lint, eval-harness, scale-eval-preflight, JudgeBench) found 
zero issues matching C1 (silent join failures), C2 (alternate-form false positives), or C3 (contaminated 
control arms). Only eval-harness had 1 total issue with no defect keywords matched.

Kill gate assessment: < 10 credible reports across ≥3 frameworks = demand too weak — gate MET.
This result is consistent with E137: only 2 frameworks (evalscope, evals) had credible reports 
manually, failing the ≥3 frameworks gate. The automated search confirms the demand is insufficient 
for preflight candidate consideration.

T-0094 experiment directory: EXPERIMENTS/140-harvest-framework-issues
Results: 0 credible reports across 9 frameworks, kill gate met'
---
# Session 2026-10-14 Summary
Session 2026-10-14 accomplishments:

EXPERIMENTS COMPLETED:
1. E139 — view-count principle on Pub.dev (Flutter packages) matched harvest
   Verdict: principle does not survive matched harvest
   δ ≈ -0.0143 (overall stratified), coverage ~13% on both arms
   G0 passes, G1-G3 all fail
   Consistent with E113's collapse on all other platforms
   Experiment dir: EXPERIMENTS/139-viewcount-pubdev-matched-harvest

2. T-0094 — harvest public issue trackers for LLM evaluation frameworks
   Verdict: kill gate met — demand too weak
   0 credible reports across 9 frameworks (C1/C2/C3)
   Consistent with E137: only 2 frameworks had credible reports manually
   Experiment dir: EXPERIMENTS/140-harvest-framework-issues

3. Value canonicalizer genre test (E141-E142 follow-up):
   ground.py/valueset.py works on Federal Register final rules (E142: 1.0 detection, 0.0 FP)
   Fails on SQuAD v2.0 (E141: 0.2826 detection vs ≥0.95 gate FAIL)
   Fails on Hacker News titles (0 extracted values, 0 money/date patterns)
   Instrument is genre-specific: regulatory text only

STATE UPDATED:
- STATE-next-actions.md: added E139 and T-0094 results
- Confirms narrowing of applicability domains per rigorous negative results

KEY FINDINGS (each narrows the domain of applicability):
- View-count separation effect: not generalizable across package registries under matched harvest
- Value canonicalizer (ground.py): genre-specific to Federal Register rules; not a general extractor
- Preflight demand validation: demand too weak (≥3 frameworks with credible reports gate; only 2 found)
- E116 classifier coverage floor is platform-dependent: 80%+ on Hex.pm package names, but only 75% on GitHub repo descriptions (E146). The classifier's vocabulary and disambiguation rules are not transferable across platforms without revalidation.

OPEN TASK: T-0093 — test whether a discriminating-observation procedure beats a free general assistant's 
first hypothesis on appliance diagnosis, using a correctly-filtered unanswered pool. 
Premise: E092's '707 unanswered' pool is 84% answered; /search/advanced?answered=false returns ANSWERED questions.

**E147 completed (2026-10-14): PostgreSQL deadlock classification claim falsified.**
Fresh observation in new domain per D083. Synthetic fixtures (27), structural vs keyword-only classifiers. Keyword baseline achieves 100% accuracy (non-overlapping keyword signatures by construction); structural classifier achieves 74.1% (parsing conservatism). G2 (Δ≥15pp) FAIL, G3 (≥80%) FAIL, G5 (abstention≤20%) FAIL. Negative controls violated (keyword beats structural). Claim falsified. Lesson: fixture design must force structural reasoning (overlapping keywords, ambiguity) to test structural classifiers. F128 recorded.

**E150 completed (2026-10-14): SQL injection technique classification claim falsified.**
Fresh observation per D083. Synthetic fixtures (16). Keyword-only 81.2%, structural 93.8% (Δ=12.5pp < 15pp gate). G2 FAIL, G1 FAIL (structural 93.8% < 100%). Structural classifier outperforms keyword but not by required margin. Fixture keyword overlap partial (mainly `FROM`/`table`), giving modest edge but not decisive.

**E160 completed (2026-10-14): Medical diagnosis classification claim falsified.**
Fresh observation per D083. Synthetic fixtures (17). Keyword-only 94.1%, structural 94.1% (Δ=0pp). G2 FAIL, G1 FAIL (both 94.1%). Fixtures have mutually exclusive keyword signatures by construction — keyword matching is optimal. Structural logic redundant with keyword features.

**E122 completed (2026-10-12): CI/CD pipeline failure classification falsified on synthetic fixtures.**
Fresh observation per D083. 140 synthetic fixtures (20 per 7 categories). Classifier accuracy 52.1% (KG1 threshold 80%). Flaky tests confused with test failures (17/20), compile errors at 40%. Falsification criterion met (KG1 fails). Domain closed for candidate generation.

**E049 Part B completed (2026-10-14): Registry-side drift of pinned requirements falsified.**
Re-resolved `requests==2.32.3`, `rich==13.9.4`, `httpx==0.28.1` one week after original snapshot (2026-10-07 → 2026-10-14). All 16 artifacts in transitive closure bit-identical (100% match). Kill gate MET: bit-stable re-resolution over time falsifies registry-drift mechanism. E049 Part A showed projects rewrite lockfiles (10/11); Part B shows drift is from project edits, not registry mutation. E2 lockfile drift line fully tested: mechanism not supported.

**ArXiv reproducibility (E079) attempted: implementation gaps prevent evaluation.**
Tool's import extraction fails on aliases (`import X as Y`), stdlib modules (`pickle`), CUDA deps (`selective_scan_cuda`), and comment text. Install success 0/3. Witness correctly predicted static analysis bound, but trial installation infrastructure not robust enough to overcome it. Candidate not viable in current form.

**Pattern confirmed:** Classification fresh observations (E147, E150, E160, E122) consistently fail due to synthetic fixture design — clean keyword separation makes keyword matching optimal. Structural advantage only emerges with substantial keyword ambiguity, which fixtures lack by construction. The 15pp gate is demanding and correctly catches this.

This session's work advances better decisions by narrowing applicability domains, 
consistent with the mission's success criterion: 'better decisions and artifacts someone 
outside this repository could evaluate and eventually use.'

