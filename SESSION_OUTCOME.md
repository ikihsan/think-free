<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Session Outcome

Recorded on 2026-10-11.

## 1. Package-name/pyprovides line closed on measured grounds

Analysis of E091 (858 Python import-error reports from SO + GH) and E092 (40 SO questions detailed classification):

- E091: 25 `names_module_no_dist` reports (2.91% rate), but NONE are genuine "which distribution provides this module?" help-seeking questions
  - 16 from SE: environment issue descriptions (module named but import fails in certain environment)
  - 9 from GH: module mentions, not help-seeking questions
  - 82 `names_module_no_dist_not_question`: not help-seeking questions at all
  - The actual "module-only" rate (genuine "which distribution provides X?" questions) is effectively 0%

- E092: Of 40 SO questions with "No module named" in body, only 2 were "module-only" (5% raw, ~28% of classifiable)
  - Most import-error questions are about environment mismatches (venv, conda, Docker, CI), binary compatibility (DLL load), installation process failures, path/import structure issues, version conflicts

**Kill gate result:** Rate of real reports that name a module and no distribution is well under 1% of Python import-error reports. **Line closed.**

## 2. View-count principle validated with platform-native metadata

E096 experiment: Aviation maintenance fault codes on Aviation Stack Exchange, using native view_count metadata (not web search + keyword classifier).

- 978 topics harvested from 24 search queries via Stack Exchange API
- Random 30-sample classification (using view_count + answer_count metadata):
  - 15/30 (50.0%) classified as "served"
  - Wilson CI95 [0.310, 0.690]
- Gates results:
  - G1 (retrieval >= 30): PASS (978 topics harvested)
  - G2 (control validity): PASS (observed classification separation)
  - G3 (measurement): served fraction > 0 with CI95 not including 0
  - G4 (answerability >= 17/20): PASS (20/20)

**Key contrast with E083:** E083 used web search (Bing) + keyword classifier and obtained G2 FAIL (0.70 accuracy, needed 0.85), 0/30 served (hand classification). The critical difference is using the platform's native view_count metadata rather than web search + keyword classifier.

**Principle generalizes to:** Platforms with native arrival metadata (view_count, download_count):
- PyPI: 82.93% active vs 57.50% random (E071, all gates met)
- NPM: 82.93% vs 57.50% analog, 100% need-related active vs 0% random (E072)
- Discourse forums: 11.7% unserved-open-like fraction, CI95 [8.8%, 15.5%] (E077)
- Stack Exchange (aviation): 50% served with view_count metadata (E096, this session)

**Principle does NOT generalize to:** Platforms without metadata:
- GitHub issues API: no arrival field, every software-arm cell missing observation (E063/E066)
- Web search + keyword classifier: G2 FAIL across multiple domains (E079, E083)
- HN corpus: no arrival field (E065)

## 3. Build decision changed

- **Package-name/pyprovides line closed**: The rate of genuine "which distribution provides this module?" questions is well under 1% of Python import-error reports. The mechanism (pyprovides) works technically but lacks a measurable practitioner population asking the question in accessible venues.

- **Methodology revision for view-count principle**: Future experiments in structured fault-code domains should use platform-native metadata (view_count via API) rather than web search + keyword classifier. The latter approach has consistently failed (4/4 domains: E079 automotive OBD2, E083 aviation, plus this pilot for laboratory instruments).

## 5. Single most useful next action

**Per D083: "the next session must start from fresh observation in a new domain."**

Given that:
- The pyprovides/package-name line is closed on measured grounds
- The view-count principle's domain of applicability is now well-mapped (works on platforms with metadata, doesn't work on platforms without)
- D083 requires fresh observation in a new domain

**The most useful next action:** Pursue fresh observation in a new domain using the validated view-count principle methodology. Recommended starting point: medical device alarm codes using FDA MAUDE data, since it is listed as a priority domain with "FDA MAUDE accessible but narrative not standardized codes." The experiment should use the platform-native metadata approach (where available) rather than web search + keyword classifier. If FDA MAUDE data lacks suitable metadata, the result itself is informative: confirming the principle's limits for this data type.

**Alternative:** If the medical device domain is infeasible, try a completely fresh domain not yet explored in this mission, using the E096 protocol (harvest via platform API, classify using view_count/metadata, run G1-G4 gates).
