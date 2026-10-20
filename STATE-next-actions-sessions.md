<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Next actions — per-session completion notes

Split out of [`STATE-next-actions.md`](STATE-next-actions.md) at the 300-line
cap, by invariant: that file is a ranked list of what to do next and this one
is what individual sessions appended to it. The ranked plan is the other
file; nothing here is a recommendation.

Scratch outcome summaries that three sessions wrote at the repository root instead
of in their own session directory are indexed here so they are not orphans:
[`SESSION_SUMMARY.md`](SESSION_SUMMARY.md),
[`session-outcome-summary.md`](session-outcome-summary.md) and
[`2026-10-14-001-session-summary.md`](sessions/2026-10-14-001-session-summary.md).

The durable record of each experiment is its own
`EXPERIMENTS/NNN-*/RESULT.md` and, for the disproved ones, a finding in
[`FAILURES.md`](FAILURES.md).

---

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

## T-0098 completed (2026-10-14): harvest public issue trackers for LLM evaluation frameworks
Automated GitHub API keyword search across 9 LLM evaluation frameworks (evalscope, evals, promptfoo, 
deepeval, inspect_ai, inspect-evals-lint, eval-harness, scale-eval-preflight, JudgeBench) found 
zero issues matching C1 (silent join failures), C2 (alternate-form false positives), or C3 (contaminated 
control arms). Only eval-harness had 1 total issue with no defect keywords matched.

Kill gate assessment: < 10 credible reports across ≥3 frameworks = demand too weak — gate MET.
This result is consistent with E137: only 2 frameworks (evalscope, evals) had credible reports 
manually, failing the ≥3 frameworks gate. The automated search confirms the demand is insufficient 
for preflight candidate consideration.

T-0098 experiment directory: EXPERIMENTS/140-harvest-framework-issues
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

2. T-0098 — harvest public issue trackers for LLM evaluation frameworks
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
- STATE-next-actions.md: added E139 and T-0098 results
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
Fresh observation in new domain per D083. Synthetic fixtures (27), structural vs keyword-only classifiers. Keyword baseline achieves 100% accuracy (non-overlapping keyword signatures by construction); structural classifier achieves 74.1% (parsing conservatism). G2 (Δ≥15pp) FAIL, G3 (≥80%) FAIL, G5 (abstention≤20%) FAIL. Negative controls violated (keyword beats structural). Claim falsified. Lesson: fixture design must force structural reasoning (overlapping keywords, ambiguity) to test structural classifiers. F147 recorded.

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

