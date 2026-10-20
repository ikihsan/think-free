# Fresh Observation: Dev.to Community Articles — View-Count Principle Test

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

## Hypothesis

**H0 (null):** On Dev.to, need-related articles (questions, help requests, "how-to" seeking) do not have systematically higher activity (page views + reactions + comments) than random articles.

**H1 (alternative):** On Dev.to, need-related articles have systematically higher activity than random articles, measured by Cliff's delta ≥ 0.147 on composite activity score.

This tests whether the view-count principle generalizes to a developer blogging platform with community Q&A features.

## Domain Selection Rule (Stated Before Fetch)

Select the largest platform by estimated monthly active users in the "developer community content" category that:
1. Has a public API requiring no authentication for basic access
2. Has a distinct "need statement" format (tags, title patterns, or series for questions/help)
3. Has measurable activity signals (page views, reactions, comments — all exposed per-article)
4. Has not been tested by this mission's view-count principle
5. Is not a package registry, Stack Exchange Q&A forum, fault code database, or news aggregator (HN)

Dev.to satisfies all five: public API (no auth for reading), tags like "help", "questions", "askdev", "beginner", "tutorial" + title patterns, `page_views_count` + `positive_reactions_count` + `comments_count` per article, not previously tested, distinct platform type (blogging + community).

## Prior Art Check

- Dev.to API: https://developers.forem.com/api/v1 (public, no auth for GET /articles)
- ~2M+ registered users, ~1M+ monthly active (public stats)
- Tags include "help", "questions", "askdev", "beginners", "tutorial", "howto", "discuss", "career", "learning"
- No prior work found testing "view-count principle" on Dev.to specifically
- Platform type distinct from tested: not package registry, not SE-style Q&A, not fault codes, not news aggregator

## Protocol

### Data Source
- Dev.to API: `https://dev.to/api/articles`
- Parameters: `per_page=1000`, `page=1..N` (max 1000 per page, paginated)
- No authentication required for public articles
- Rate limit: generous (unauthenticated)

### Sampling
1. Fetch 2000 recent articles (2 pages × 1000)
2. Filter to articles published in last 30 days (to avoid survival bias)
3. Stratified sample: 200 articles total
   - 100 from "need-indicator tags" (help, questions, askdev, beginners, tutorial, howto, learning)
   - 100 from other tags (general, career, discuss, productivity, etc.)

### Classification (Pre-declared, Before Any Fetch)

**Need-related (treatment):** Article has ANY of these tags:
- "help", "questions", "askdev", "beginners", "tutorial", "howto", "learning", "discuss"

**AND/OR** title contains (case-insensitive):
- "how to", "how do", "how can", "how should"
- "what is", "what are", "what's the"
- "help", "help me", "need help"
- "anyone", "anybody", "experience with"
- "best", "recommend", "recommendation", "suggest"
- "looking for", "searching for"
- "why", "why does", "why is"
- "advice", "guidance", "direction"
- "alternative", "alternatives", "vs", "versus"
- "compare", "comparison"
- "learn", "tutorial", "guide", "getting started"

**Random (control):** Articles not matching need-related tags OR title patterns

### Activity Metric
Composite score = `page_views_count + positive_reactions_count * 10 + comments_count * 50`
- Page views: typically 100-10000+
- Reactions: typically 0-500
- Comments: typically 0-100
- Scaling factors chosen so each component contributes meaningfully (views dominate but reactions/comments add signal)

All three fields always present in API (default 0).

### Gates (Pre-declared)

**G1 (sample size):** Both arms ≥ 30 articles each
**G2 (activity presence):** ≥ 80% of need-related articles have activity > 0
**G3 (differential activity):** Cliff's delta ≥ 0.147 on composite activity score (need-related vs random)
**G4 (metadata universality):** 100% of sampled articles have all three activity fields (API guarantee)

### Kill Conditions
- Any gate FAIL → principle does not generalize to this domain
- G3 FAIL with p ≥ 0.05 (Mann-Whitney U) → no evidence of differential activity
- Classifier vocabulary mismatch (need-related < 30 articles) → G1 FAIL, domain requires platform-adapted keywords

### Falsification
Strongest accessible alternative: "no systematic difference" — random variation in Dev.to article activity. Significant Cliff's delta in opposite direction (random > need-related) would also falsify.

### Resource Limits
- Max 2000 API requests (2 pages × 1000, but actually 2 requests for 2000 articles)
- Timeout 30 seconds per request
- Stdlib only (urllib, json, statistics, datetime)
- No external dependencies

### Output
- `results.json`: Raw data + gate results + Cliff's delta + p-value
- `classification.json`: Per-article classification with tag/keyword matches
- `RESULT.md`: Human-readable summary with evidence labels

## Expected Outcomes

If H1 supported: View-count principle extends to developer community blogging platforms with Q&A features.
If H0 supported: Principle boundary confirmed — works on package registries (leaf consumption) but not on community content platforms where need-related content may not systematically attract more activity.

Either result advances the mission by mapping the principle's boundary conditions.