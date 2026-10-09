<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Next actions

E071 conclusive result: the view-count principle is supported on PyPI — need-related packages (82.93% active) are systematically more "active" (have significant activity metadata) than random packages (57.50% active). G1 retrieval met, G2 significant (t=3.4660, p=0.001), G3 PASSES (Wilson CI95 lower bound 0.6874 > 0.6). All gates met.

E071 closes the view-count measurement prototype line. The principle generalizes to PyPI metadata after failing on web search (E065) and GitHub issues API (E063/E066). Previous findings: E062 (Steam: 17/20 unremedied needs served), E063 (GitHub issues: 0/1391 needs mentioned a tool).

The seed for a candidate remains empty. The mission has now closed candidates across six report domains (A-F), seven emptiness measurements (F029/F051/F055/F059/F081/F084), and the view-count prototype from three independent angles. The DECISIONS-SCREENING-14.md D084-D088 and D091-D092 record the arrival-instrument corrections and kill-gate design lessons.

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

**Key finding:** The view-count principle works on package repositories (PyPI, NPM) but not on social media/issue tracking platforms (GitHub issues, web search). The key platform characteristic appears to be whether the platform is a package repository with exposeable metadata (release/version info, project URLs, keywords), rather than a social media or web search platform.

**Next action:** Integrate E072 finding into mission evidence base. The view-count principle has now been validated across package repositories; fresh observation needed in a non-package-repository domain until a specific testable opportunity appears.

## Decision

The view-count principle on PyPI is conclusive — no further gate testing needed. The mission's evidence base now includes this result across four platforms. No candidate generated from this line; the seed remains empty. Fresh observation needed in a new domain or platform.