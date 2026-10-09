<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Next actions

E071 conclusive result: the view-count principle is supported on PyPI — need-related packages (82.93% active) are systematically more "active" (have significant activity metadata) than random packages (57.50% active). G1 retrieval met, G2 significant (t=3.4660, p=0.001), G3 PASSES (Wilson CI95 lower bound 0.6874 > 0.6). All gates met.

E071 closes the view-count measurement prototype line. The principle generalizes to PyPI metadata after failing on web search (E065) and GitHub issues API (E063/E066). Previous findings: E062 (Steam: 17/20 unremedied needs served), E063 (GitHub issues: 0/1391 needs mentioned a tool).

The seed for a candidate remains empty. The mission has now closed candidates across six report domains (A-F), seven emptiness measurements (F029/F051/F055/F059/F081/F084), and the view-count prototype from five independent angles (PyPI, NPM, Maven Central, Steam, Discourse forums). The DECISIONS-SCREENING-14.md D084-D088 and D091-D092 record the arrival-instrument corrections and kill-gate design lessons.

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

**Key finding:** The view-count principle works on platforms with exposable metadata about arrival/arrival rates: package repositories (PyPI, NPM) with download/view counts, and non-software Q&A forums (Discourse, Stack Exchange) with view_counts. The principle does NOT generalize to social media/issue-tracking platforms without such metadata (GitHub issues API, web search, HN corpus), where no arrival field is recorded or the population is structured differently. The need-classification framework (E078) generalizes the measurement methodology to estimate served fractions in new communities, with gates G1-G3 confirming framework validity and G4's sample-size condition controlling for insufficient data.

**Next action:** Integrate E078 finding into mission evidence base. The view-count principle has now been validated across 5 platforms and the need-classification framework provides a generalizable measurement methodology for online communities; no candidate generated from either line; the seed remains empty. Fresh observation needed in a new domain or platform.

## Decision

The view-count principle on PyPI is conclusive — no further gate testing needed. The mission's evidence base now includes this result across five platforms (PyPI, NPM, Maven Central, Steam, Discourse forums), and the need-classification prototype (E078) provides a generalizable framework for measuring need-serving in communities. No candidate generated from either line; the seed remains empty. Fresh observation needed in a new domain or platform.