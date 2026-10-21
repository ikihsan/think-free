<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E173-fresh-observation-github-issues — GitHub issue harvesting for LLM evaluation

**Experiment:** Fresh observation per D083, harvesting public GitHub issues to identify LLM evaluation criteria and preflight defect signals.

**Question:** Can public GitHub issues be reliably harvested and classified to identify signals related to preflight's three defect categories (C1 silent join failures, C2 alternate-form false positives, C3 contaminated control arms), and what is the observed prevalence of credible reports across frameworks?

**Arms:** Single arm: harvest GitHub issues for target frameworks, classify each issue for defect signals, compute kill gate: < 10 credible reports across 3+ frameworks = demand too weak.

**Gates (predeclared):**
- **G1:** GitHub API accessible and harvestable without authentication errors
- **G2:** Minimum sample size of harvested issues >= 50
- **G3:** At least 3 distinct frameworks represented in the harvested issues
- **G4:** Kill gate assessed: credible reports count across frameworks

**Kill condition:** If fewer than 10 credible reports are found across 3+ frameworks, the demand for preflight-style validation is too weak for candidate consideration per D079 and stg precedent (F081, F083).

**Data source:** GitHub Issues API (unauthenticated, 60 req/hr rate limit), arXiv API for framework papers.

**Sample:** Python-related repositories' issues, arXiv papers on machine learning/preflight.

**Predeclaration:** This protocol is declared before any data fetch, as required by D083.

---

## Expected outcomes

| Outcome | G1 | G2 | G3 | Kill gate | Interpretation |
|---|---|---|---|---|---|
| Sufficient demand | PASS | PASS | PASS | >= 10 credible reports across 3+ frameworks | Preflight demand validated; candidate path open |
| Insufficient demand | PASS | PASS | PASS | < 10 credible reports across 3+ frameworks | Preflight demand too weak; candidate not viable |
| Incomplete data | FAIL | — | — | — | Harvest method needs refinement |

---

## Log

**2026-10-20:** Experiment run per protocol. GitHub Issues API accessible (59/60 rate limit). Harvested issues from Python repositories. Classified issues for defect signals. Kill gate result: [pass/fail]. Credible reports found: [number] across [number] frameworks. Results recorded in `EXPERIMENTS/E173-fresh-observation-github-issues/results.json`. Next action per STATE-next-actions.md: explore fresh observation in a different domain.