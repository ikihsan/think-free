<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E150 Result — View-Count Principle on Stack Overflow Questions

Experiment: E150
Platform: Stack Overflow
Date: auto-generated

## 1. Hypothesis

**H1 (view-count principle extends to SO):** Stack Overflow questions classified as 
need-related based on title keywords will have systematically different view counts 
than random questions.

**H0:** View count distributions do not differ between need-related and random questions.

## 2. Method

- **Platform:** Stack Overflow (public API, no auth required)
- **Per-request metadata:**  per question
- **Need statements:** Question titles classified using need-related keywords
- **Classification:** A question is "need-related" if its title contains at least one 
  keyword from the predeclared list covering problem-solving patterns.
- **Random set:** Questions excluding anti-keyword (discussion/recommendation) patterns 
  and need-related keywords.
- **Corpus:** Fetched from Stack Exchange API, sorted by activity, 500 questions
- **Gates:** G1–G4 as declared above

## 3. Gates

| gate | result |
|------|--------|
| G1 retrieval | PASS |
| G2 separation | FAIL (Cliff's delta = 0.014) |
| G3 effect magnitude | PASS (delta > 0, direction nr>r) |
| G4 arrival field | PASS |

## 4. Decision

**G1–G4: FAIL**

The view-count principle not validated on Stack Overflow: need-related content 
does not show a statistically separable pattern of systematically higher view counts. 
Cliff's delta = 0.014 indicates negligible effect size between groups.

External value still unobserved. D111 stands. The principle's boundary conditions 
are reinforced: the direction and magnitude of the view-count effect varies significantly 
by venue type. This extends the principle's recorded scope to Q&A forums, where 
effect sizes are typically smaller than package repositories or code repositories.

**Classification keywords**: how do i, how to, why does, why is, how to fix, error, bug, troubleshoot, debug, need help, fix my, solve this, calculate, compute
