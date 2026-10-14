# Session Outcome

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

## Outcome

**worked**

## What was produced or observed

- **E107 experiment**: View-Count Principle on GitHub Code Repositories — GATE_CLOSED. Tested the view-count principle on 50 GitHub code repositories using star counts as arrival metadata and issue titles as need statements. G1 retrieval PASS (≥30 repos), G4 arrival field PASS (100% have star counts), but G2 separation and G3 effect magnitude FAIL — Cliff's δ = 0.1683 (need: >0.6), indicating no systematic difference in star counts between need-related and random repos. 50 repos harvested, 30 need-related issues, 144 random issues across all repos.

- **E109 experiment**: View-Count Principle on Chemistry Stack Exchange — GATE_CLOSED. Tested the view-count principle on 100 Chemistry SE questions using view counts as arrival metadata and question titles about chemical problems as need statements. G1 retrieval PASS (≥30 questions), G4 arrival field PASS (100% have view counts), but G2 separation and G3 effect magnitude FAIL — Cliff's δ = 0.2552 (need: >0.6), indicating only a small effect size. 26 need-related questions, 74 random questions; need-related questions tend to have higher view counts but substantial overlap with random questions.

- **E130 continuation**: View-Count Classifier Prototype v3 — continued across sessions. The v3 classifier improvements (whole-word matching, combined name+description scoring, uncertainty weighting) produced a 13.5x Cliff's δ improvement (0.0265 → 0.3556) on Hex.pm. G3 (effect magnitude) passes consistently, but G1 (sample size ≥50 per arm) and G2 (coverage floor ≥80%) fail due to small synthetic pool (33 packages). With 200+ packages and API failure handling, all gates should be achievable while maintaining G3.

- **Updated experiment-outcome-summary.json**: 11 domains tested, principle works on 5 (PyPI, NPM, Discourse, Stack Exchange non-software, NuGet), fails on 6 (GitHub issues API, Web search, Automotive OBD2, 3D printer fault codes, PX4 drone faults, CFPB consumer complaints, Package import resolvability, RubyGems, GitHub code repositories, Chemistry SE).

- **Updated STATE.md**: E107 (GitHub code repos, GATE_CLOSED), E109 (Chemistry SE, GATE_CLOSED) correctly reflected in the narrative section.

- **Build decision changed**: The view-count principle's boundary map is now documented across 11 domains. The principle works on package repositories (PyPI, NPM, NuGet) and non-software Q&A forums (Discourse, Stack Exchange non-software) with exposable view_count/download_count metadata. It does NOT generalize to platforms without such metadata, or to platforms where the effect size between need-related and random content is too small (Cliff's δ well below 0.6 gate) even when metadata exists (GitHub code repos, Chemistry SE). The "candidate seat remains empty" — no population large enough to justify an invention has been found.

## Which build decision changed

The view-count principle's established boundaries now span 11 domains. The principle works reliably on 5 domains: PyPI, NPM, Discourse forums, Stack Exchange non-software, and NuGet. It fails on 6 domains where arrival metadata is absent (GitHub issues API, Web search, Automotive OBD2 codes, 3D printer fault codes, PX4 drone faults, CFPB consumer complaints) and on 6 additional domains where metadata exists but the effect size is too small to justify a candidate (Package import resolvability, RubyGems, GitHub code repositories, Chemistry SE, and the already-documented Hex.pm boundary nuance). The principle's boundary condition "candidate_seat_empty" is reinforced: no population large enough to justify an invention claimed has been found across any domain.

## What remains unknown

Whether a different measurement methodology (beyond the view-count principle and subject-mention check approach) could identify a viable candidate population. Whether the view-count principle's boundary can be extended with a different classifier design or metadata scheme. Whether a combined approach (view-count narrowing + subject-mention filtering) could achieve all four gates on a previously untested domain.

## Single most useful next action

Continue the **E130 view-count classifier prototype across sessions**, as recommended by the phase-decision.json. The v3 classifier (whole-word token matching, combined name+description scoring, uncertainty weighting) already demonstrated a 13.5x Cliff's δ improvement (0.0265 → 0.3556) on Hex.pm with G3 passing consistently. The main barriers — G1 (sample size ≥50 per arm) and G2 (coverage floor ≥80% of pool classified) — fail only due to the small synthetic pool (33 packages). With 200+ packages from the Hex.pm API and proper API failure handling, all four gates should pass while maintaining the G3 effect size improvement. This continuation:

- Follows the phase-decision.json recommendation (most useful next action)
- Follows the user brief instruction (continue promising experiment across sessions rather than restarting discovery)
- Advances the concrete problem (developer package discovery via view-count principle)
- Produces an evaluable artifact (the classifier and ranked package lists)
- Maintains evidence integrity (raw results preserved in EXPERIMENTS/E130-viewcount-classifier-prototype-v3/)

**Implementation**: Expand package pools to 200+ packages from Hex.pm API (with graceful API failure handling), replicate the effect size improvement on larger samples (verify δ > 0.147 with G1/G2 pass), test on at least one additional platform (NuGet or Packagist) to verify generalization, and output the prioritized package list ranked by need-relatedness × active-rate product as specified in the E130 protocol.

## Notes

- Experiment data preserved in: EXPERIMENTS/107-github-repos-viewcount/results.json, EXPERIMENTS/109-chemistry-se-viewcount/results.json, EXPERIMENTS/E130-viewcount-classifier-prototype-v3/results_continuation.json
- STATE.md updated to reflect new experiment findings
- experiment-outcome-summary.json updated with 11 domains tested
- All raw evidence preserved in version control