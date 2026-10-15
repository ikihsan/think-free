<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Next actions

> **READ FIRST (2026-10-12).** The view-count domain sweep is **STOPPED**
> (E113, F116, D105). E113's matched-harvest control of E107 showed the
> effect is a harvest artifact (δ 0.826 → 0.075, stratified p=0.183) and the
> shared classifier labels only 28% of a representative pool. Every
> "ALL GATES PASS" below that came from this line is **`untested` on a matched
> harvest, not confirmed**. Do not run another registry sweep. See
> [`EXPERIMENTS/113-viewcount-matched-harvest/`](EXPERIMENTS/113-viewcount-matched-harvest/README.md).

The D083 sweep table and the completed closing entries this file used to
carry were split into
[`STATE-next-actions-sweep-history.md`](STATE-next-actions-sweep-history.md)
at the 300-line cap.

## E137 completed (2026-10-14) — cross-model agreement: third exact AGREE

E136's named next action is done. The calibrated instrument (last-`\boxed`
extraction, normalized-string equality, macro-mean-of-subject-means weighting)
pointed at `01-ai/yi-6b` (first model in the HELM lite v1.0.0 inventory other
than `01-ai/yi-34b`, selection rule pre-declared in E137's protocol, no
substitution) achieved exact AGREE on the same `math_chain_of_thought` cell:
437/437 row verdicts agree with the harness's per-instance verdicts; the
recomputed macro mean (0.12585197340399298) equals the published group macro
to full printed precision, diff 0.0. One yi-6b-specific calibration fix:
backslash stripping now only before letters (LaTeX commands), not before
digits — corrected one case where `\37` ≠ `37` (harness scored 0, naive
strip-all-backslashes would have scored 1). Kill gate not fired; D111
stands (cross-model reach demonstrated further, external value still
unobserved). This is the third exact AGREE on this line (E135: MMLU
single-letter; E136: math_chain_of_thought yi-34b with parser+weighting
stress; E137: math_chain_of_thought yi-6b cross-model).
[`EXPERIMENTS/137-leaderboard-cross-model-agreement/`](EXPERIMENTS/137-leaderboard-cross-model-agreement/RESULT.md).

## E138 completed (2026-10-14) — GSM `####` parser: fourth exact AGREE

E136's pre-named cell F is done. The calibrated instrument pointed at
`01-ai/yi-34b` gsm run (1000 instances) achieved exact AGREE: recomputed
`final_number_exact_match` = 0.648000, published = 0.648, diff 0.0.
Row-level verdict agreement: **1000/1000** with the harness's per-instance
verdicts. The `####` marker was absent from this population (HELM's GSM8K
references end with "The answer is N"); the fallback rule (last number in
text) was exercised on 1000/1000 rows for both gold and predicted answers.
No parser bugs found; 352 mismatches are genuine model errors. Kill gate
not fired; D111 stands (reach demonstrated further across four stressors:
single-letter, free-text aggregate with weighting, cross-model, `####`
parser, external value still unobserved).
[`EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md`](EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md).

**Named next action:** superseded by E141 below. The R1 instrument was validated
on four cells in HELM lite v1.0.0 with exact agreement on all, and E141 then
measured whether that reach carries a finding. It does not.

## E141 completed (2026-10-15) — the scorer false-negative rate is small; kill gate FIRED

E141 is the experiment D111 was waiting on. `preflight` had demonstrated reach
(four exact AGREEEs) but never a finding, so its release question had nothing to
go on. E141 pointed the calibrated instrument at the one check that could have
produced one: **does the harness's own scorer mark correct answers wrong?**

On the four already-fetched, hash-verified HELM lite v1.0.0 cells — 2,874 rows,
two models, two scenarios — **6 scored-wrong rows are mathematically equal to the
reference**, all six confirmed correct by hand. Pooled 6 of 1,593 wrong rows
= 0.377%. Primary cell P1: **4 of 246 = 1.626%** against a declared gate of 2.0%
**and** 5 rows, so **both conditions failed and the gate fired**. Effect on the
published number: +1.17 accuracy points on P1, entirely from unreduced fractions,
thousands separators and decimals; **0** rows on 1,000 GSM rows in both models.

The result survives its own falsification because the recall audit bounds what
the instrument could have missed: 25 of 25 hand-read wrong rows are genuinely
wrong, and a weaker extractor over the 95 no-answer rows recovered 0. Controls
G0a/G0b/G0c/G0d all green, and two defects in this session's own work (a verdict
dict keyed on instance id alone, which crosses subject runs because the seven
HELM MATH runs carry only 267 distinct ids across 437 rows; and an incomplete
copy of the calibrated normalizer) were caught by them.
[`EXPERIMENTS/141-scorer-false-negatives/RESULT.md`](EXPERIMENTS/141-scorer-false-negatives/RESULT.md).

**What this decides.** Stop adding adapters, cells and harnesses to `preflight`.
A check that fires on 0.4% of rows, in cases a single normalization rule catches,
and on zero rows of half the populations tested, is not worth shipping as a gate;
that is now a measurement. D111's remaining sub-question is E134's population
question restated, and E134's answer was that the one published run available was
clean.

**Named next action: E140**, the only live fresh-observation protocol
(CI/CD pipeline failures, declared 2026-10-14, never run). Its G2 — top-10 error
patterns covering ≥30% of cases — is the gate most likely to decide it and is
cheap to run. Do not re-probe C1 Open LLM Leaderboard v2 or C3 Chatbot Arena:
both failed G2 at probe time and nothing new has happened to either.

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

### E117 completed (2026-10-14): view-count classifier prototype v3 on CRAN

E117 designed and executed a view-count classifier prototype with improved
labeling coverage and testing on previously untried platform (CRAN R packages).
The classifier uses whole-word token matching, R-specific expanded vocabulary,
and contextual disambiguation to classify packages as need-related or random.

Results:
- Pool: 25 popular R packages with download counts
- Classifier: 4 need-related, 21 random
- G1 (sample size >= 100): FAIL -- only 25 packages classified
- G2 (coverage floor >= 80%): PASS -- 100% coverage (25/25)
- G3 (effect size, Cliff's delta > 0.147, p < 0.05): FAIL -- delta = -0.7619,
  p = 1.6e-6; random packages have higher downloads
- G4 (both categories represented): PASS -- both arms have packages
- all_pass: False
- Decision: view-count principle does not produce a candidate in CRAN domain;
  experiment addresses E113/E107 coverage limitation but effect size threshold
  not met; documents fundamental limits across 12+ domains. No candidate.

### E139 completed (2026-10-14): preflight evalscope adapter demonstrated

E139 extended preflight population coverage by demonstrating the adapter for modelscope/evalscope's two-file run output format (predictions + reviews, joined by `index` within task directories). The adapter is ~10 lines of stdlib Python. All three preflight checks (C1, C2, C3) function correctly on this format.

Results:
- Clean run: C1 OK (best_rate 1.0), C2 OK (fp_rate 0.0), C3 OK (0/3 positives) → exit 0
- F121-style defect (composite key vs simple index): C1 NO_DISCRIMINATING_PAIRING → exit 3
- Repaired key (composite on both sides): C1 OK (best_rate 1.0) → exit 0
- F122-style control contamination: C3 CONTROL_NOT_EMPTY (2/3 positives, Wilson LB 0.2077) → exit 3
- C2 alternate-form FP (strict flagger): ALTERNATE_FORM_FP (Wilson LB 0.2307 > 0.02) → exit 3

Total harness structures with working adapters: 6 (lm-eval real run, evalscope synthetic, openai/evals inferred, JSONL, CSV, YAML, XML).

**Named next action**: The preflight adapter pattern is validated across 6 harness output structures. The remaining question is whether anyone outside this repository would use it. Options:
- A: Measure adoption interest among LLM evaluation practitioners (survey, issue search, outreach)
- B: Extend population coverage further by testing against additional real harness run outputs
- C: Document the tool with its limitations and release as stdlib-only instrumentation for harness authors
- D: Close the preflight line if no adoption path is visible

Recommendation: Option C (document and release with limitations) is the most honest continuation. The tool catches real defects (F118, F121, F122) that harnesses' own gates miss, and the adapter tax is small. Prior art is partially-covered. The population limitation (E125: only 5/22 harnesses have qualified committed pairs) is a documented boundary, not a blocker for a tool aimed at harness authors who control their run outputs.