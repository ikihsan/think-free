<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E151 Result — View-Count Principle on Software Engineering Stack Exchange

Experiment: E151
Platform: softwareengineering.stackexchange.com
Date: auto-generated

## 1. Hypothesis

**H1 (view-count principle extends to SE):** Software Engineering Stack Exchange questions classified as 
need-related based on title keywords will have systematically different view counts 
than random questions.

**H0:** View count distributions do not differ between need-related and random questions.

## 2. Method

- **Platform:** Software Engineering Stack Exchange (public API, no auth required)
- **Per-request metadata:** `view_count` per question
- **Need statements:** Question titles classified using need-related keywords
- **Classification:** A question is "need-related" if its title contains at least one 
  keyword from the predeclared list covering problem-solving, design, and pattern topics.
- **Random set:** Questions excluding anti-keyword (discussion/recommendation) patterns 
  and need-related keywords.
- **Corpus:** Fetched from Stack Exchange API, sorted by activity, 500 questions
- **Gates:** G1–G4 as declared above

## 3. Gates

| gate | result |
|------|--------|
| G1 retrieval | PASS |
| G2 separation | FAIL (Cliff's delta = -0.094) |
| G3 effect magnitude | FAIL (direction nr>r) |
| G4 arrival field | PASS |

## 4. Decision

**G1–G4: FAIL**

The view-count principle not validated on Software Engineering Stack Exchange: need-related content does not show a statistically separable pattern of systematically higher view counts. Cliff's delta = -0.094 indicates negligible effect size between groups.

External value still unobserved. D111 stands. The principle's boundary conditions are reinforced: the direction and magnitude of the view-count effect varies significantly by venue type. This extends the principle's recorded scope to yet another Q&A forum, where effect sizes are typically smaller than package repositories or code repositories. The consistent pattern of negligible effect sizes across multiple SE sites (Stack Overflow: delta=0.014, Software Engineering SE: delta=-0.094) suggests that Q&A forums are a venue type where the view-count principle does not produce reliably separable groups.

**Classification keywords**: how do i, how to, why does, why is, how to fix, error, bug, troubleshoot, debug, need help, fix my, design, architecture, pattern, best practice, anti-pattern, refactor, performance, scalability, latency
