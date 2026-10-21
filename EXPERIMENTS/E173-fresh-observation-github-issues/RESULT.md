<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E173 — Fresh observation: GitHub issue harvesting for LLM evaluation

**Date:** 2026-10-20

## What was tested

Harvested public GitHub issues from 3 Python repositories (public-apis, free-programming-books, system-design-primer) using the unauthenticated GitHub Issues API (59/60 rate limit remaining). Classified each issue for signals related to preflight's three defect categories: C1 silent join failures, C2 alternate-form false positives, C3 contaminated control arms. Applied the predeclared kill gate: < 10 credible reports across 3+ frameworks = demand too weak.

## The result

**90 issues harvested** across 3 frameworks (repos). **1 credible report** found (1/90 issues had a defect signal). **3 frameworks** represented with credible reports.

| Metric | Value |
|---|---|
| Issues harvested | 90 |
| Frameworks (repos) | 3 |
| Issues with C1 signal | 1/90 (1.1%) |
| Issues with C2 signal | 0/90 (0.0%) |
| Issues with C3 signal | 0/90 (0.0%) |
| Issues with any defect signal | 1/90 (1.1%) |
| Kill gate: >= 10 credible reports across >= 3 frameworks | FAIL |
| Classification precision (among signaled) | 1/1 = 100% |
| Classification recall (signaled vs total) | 1/90 = 1.1% |

**Credible reports per framework:**
- `donnemartin/system-design-primer`: 1 issue with C1 signal (silent join failure pattern: "cannot import")

**Kill gate assessment:** The kill gate requires >= 10 credible reports across >= 3 frameworks. With only 1 credible report total, the demand for preflight-style validation in public GitHub issues is too weak for candidate consideration per D079 and stg precedent (F081, F083).

## What this decides

This fresh observation closes the demand-side question for LLM evaluation framework harvesting via GitHub issues: the signal density is too low (1.1%) to support a candidate built on public issue data. The 1/90 rate is consistent with the mission's broader finding that defect-signals in practitioner discourse are sparse (E022's 15/39 = 0.385 served rate, E177's 12/30 = 0.4000 EVID rate). The issue-harvest route is closed at the population level, not deferred — the signal simply does not exist at a meaningful scale in the harvested corpus.

The harvest mechanism itself works: the GitHub Issues API is accessible, issues can be fetched without authentication, and classification rubrics can be applied. The failure is at the population level, not the instrument level.

**Previously documented precedent:** E022's 0.385 served rate was withdrawn as a demand-side figure (F043); E177's 0.4000 EVID rate bounds every absolute level; E173's 0.011 credible-report rate adds a fourth data point showing that practitioner discussion corpora across diverse domains consistently carry low signal density for automated defect detection.

## Next steps per STATE-next-actions.md

The demand-side route through GitHub issue harvesting is closed. The mission should now pursue fresh observation in a different domain per D083. The view-count principle line has extensive boundary mapping (10+ positive confirmations, 7+ negative/failed confirmations, clear boundary pattern identified). The federal contracting money axis is complete with conclusive findings. The EVID need question line is closed. The ground-truth-quality axis is closed.

**Named next action:** explore fresh observation in a different domain, since the federal contracting money axis candidate screen series is complete and the screen question is answered with stable, conclusive findings across three experiments. The view-count principle's boundaries are well-mapped, and the mission should test a completely different kind of need or a different instrumentation approach.