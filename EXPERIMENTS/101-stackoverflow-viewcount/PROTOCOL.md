# Experiment 101: Stack Overflow View-Count Principle Test

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

## Claim

The view-count principle generalizes to Stack Overflow (software Q&A on Stack Exchange): high-view-count unanswered questions on Stack Overflow correlate with genuine unserved software needs, with an unserved-open-like fraction statistically consistent with the Discourse baseline (11.7%, E077) or the embedded Discourse baseline (15.3%, E082).

## Scope

- Platform: Stack Overflow (Stack Exchange API)
- Domain: Software Q&A (programming questions)
- Population: Unanswered questions (no accepted answer) with high view counts
- Metric: Unserved-open-like fraction per E078 three-clause rubric

## Background

The mission has validated the view-count principle on:
- Package registries (PyPI E071, NPM E072): download counts → 82.93% active vs 57.50% random
- Non-software Q&A forums (Stack Exchange E062, Discourse E077/E082): view_counts → 11.7-15.3% unserved

The principle FAILED on:
- GitHub Issues API (E063/E066): no arrival field
- Web search (E065): no reliable view counts
- Fault-code domains on Discourse (E079/E083/E084): vendor-bound needs dominate, population too small

Stack Overflow is a **software Q&A forum on Stack Exchange** with view_counts — a new category (software) on a tested platform (Stack Exchange). E062 tested non-software Stack Exchange (DIY, etc.). This experiment tests whether the principle holds for software needs on the same platform.

## Methodology

### Data Collection (G1: Population Size)

1. Fetch unanswered questions from Stack Overflow via `/questions/unanswered` endpoint
2. Sort by votes (proxy for views; API doesn't support sort=views)
3. Filter for `is_answered: false` (no accepted answer)
4. Target: ≥100 questions with view_count > 1000 (G1 threshold from E078)
5. Tags: python, javascript, java, c#, c++, go, rust, typescript (top languages)

### Need Classification (G2: Concentration)

Per E078 three-clause rubric, classify each question as:
- **NEED**: Question asks "how do I...", "why does...", "what is...", "error when...", "fix for..." — expresses a concrete technical need
- **NOT-NEED**: Homework, opinion, recommendation, meta, duplicate-closure-bait

Require: ≥30% NEED concentration (G2 threshold from E078)

### Served/Unserved Classification (G3: Unserved Fraction)

For NEED-classified questions only, apply E078 three-clause rubric:
- **SERVED**: Has answer with score ≥1 that provides actionable solution (code, config, command)
- **PARTIALLY_SERVED**: Has answer with score ≥1 that provides partial guidance (link, concept, workaround)
- **UNSERVED**: No answer with score ≥1, or answers are irrelevant/incorrect

Measure: Unserved fraction with Wilson CI95. G3 passes if CI95 upper bound < 60%.

### View Count Coverage (G4)

All sampled questions must have view_count field populated. G4 passes if 100%.

## Kill Gate

**The line closes if ANY gate fails:**
- G1 FAIL: <100 questions with view_count > 1000
- G2 FAIL: NEED concentration < 30%
- G3 FAIL: Unserved fraction CI95 upper bound ≥ 60%
- G4 FAIL: view_count coverage < 100%

**Additional closure condition (per E092 composition finding):**
If the NEED population is dominated by vendor-bound or repair-bound questions (analogous to E092's 65% vendor/repair-bound), the unserved share is not comparable to non-software venues. Record composition mix.

## Baseline Comparison

- Discourse baseline (E077): 11.7% unserved, CI95 [8.8%, 15.5%]
- Embedded Discourse (E082): 15.3% unserved, CI95 [10.5%, 21.3%]
- Non-software Stack Exchange (E062): 17/20 = 85% served by free assistant (inverse measure)

If Stack Overflow unserved fraction is statistically consistent with Discourse baseline (overlapping CIs), the principle generalizes to software Stack Exchange.

## Negative Control

Fetch 50 random low-view-count questions (view_count < 100) from same tags. Expect:
- Lower NEED concentration
- Higher SERVED fraction (easy questions get answered fast)
- This validates the instrument distinguishes high-view unserved needs from low-view noise

## Resource Limits

- Stack Exchange API: 300 requests/day unauthenticated
- 100 questions per request → 30,000 questions max
- Target: 500 questions across 5 tags × 10 pages = 50 requests
- No LLM API required (classification by keyword/rules per E078)

## Deliverables

- `harvest.py` — fetch questions from Stack Exchange API
- `classify.py` — NEED/NOT-NEED classification per E078 rubric
- `measure.py` — served/unserved classification per E078 rubric
- `results.json` — gate results with CIs
- `README.md` — experiment summary