# Fresh Observation: Hacker News "Ask HN" — View-Count Principle Test

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

## Hypothesis

**H0 (null):** On Hacker News "Ask HN" posts, need-related content (questions asking for help, recommendations, how-to) does not have systematically higher activity (comments + points) than random content.

**H1 (alternative):** On Hacker News "Ask HN" posts, need-related content has systematically higher activity than random content, measured by Cliff's delta ≥ 0.147 on the composite activity score (comments + normalized points).

This tests whether the view-count principle — that need-related content attracts systematically more activity — generalizes to a community news aggregator with explicit "ask" posts.

## Domain selection rule (stated before fetch)

Select the largest platform by estimated monthly active users in the "community question/need" category that:
1. Has a public API requiring no authentication
2. Has a distinct "need statement" format (explicit "Ask" prefix or category)
3. Has a measurable activity signal (comments, points/votes, views if available)
4. Has not been tested by this mission's view-count principle
5. Is not a package registry, Stack Exchange Q&A forum, or fault code database

Hacker News "Ask HN" satisfies all five: public Firebase API (no auth), "Ask HN:" title prefix, comments + points as activity signals, not previously tested, distinct from tested categories.

## Prior art check (per protocol §61–63)

- HN API is public and well-documented (https://github.com/HackerNews/API)
- "Ask HN" is a recognized category with ~200-300 posts/day
- No prior work found testing "view-count principle" on HN Ask posts specifically
- Prior work on HN focuses on story ranking, not need/activity correlation

## Protocol

### Data source
- Hacker News Firebase API: `https://hacker-news.firebaseio.com/v0/`
- Endpoints: `askstories` (IDs of Ask HN posts), `item/{id}.json` (post details)
- No authentication required, rate limits generous (~1000 req/sec)

### Sampling
1. Fetch `askstories` (returns ~1000 most recent Ask HN post IDs)
2. Sample 200 posts: 100 most recent (by ID order, which is roughly chronological) + 100 from middle of list (to avoid recency bias)
3. For each post, fetch full item data

### Classification (pre-declared, before any fetch)

**Need-related (treatment):** Title contains any of (case-insensitive):
- "how to", "how do", "how can", "how should"
- "what is", "what are", "what's the", "what are the"
- "best", "recommend", "recommendation", "suggest", "suggestion"
- "help", "advice", "guidance", "direction"
- "looking for", "searching for", "need", "want"
- "anyone", "anybody", "experience with", "used"
- "alternative", "alternatives", "replace", "replacement"
- "learn", "tutorial", "guide", "resource", "resources"
- "compare", "comparison", "vs", "versus"
- "why", "why does", "why is", "why are"

**Random (control):** All other Ask HN posts not matching need-related keywords

### Activity metric
Composite score = `comments_count + (points * 0.1)` 
- Points typically range 1-1000+, comments 0-500+
- Scaling factor 0.1 makes points contribute roughly equally to comments (median points ~10-20, median comments ~5-10)
- Both fields always present in API (default 0)

### Gates (pre-declared)

**G1 (sample size):** Both arms ≥ 30 posts each
**G2 (activity presence):** ≥ 80% of need-related posts have activity > 0
**G3 (differential activity):** Cliff's delta ≥ 0.147 on composite activity score (need-related vs random)
**G4 (metadata universality):** 100% of sampled posts have both comments and points fields (API guarantee)

### Kill conditions
- Any gate FAIL → principle does not generalize to this domain
- G3 FAIL with p ≥ 0.05 (Mann-Whitney U) → no evidence of differential activity
- Classifier vocabulary mismatch (need-related < 30 posts) → G1 FAIL, domain requires platform-adapted keywords

### Falsification
The strongest accessible alternative is "no systematic difference" — random variation in HN post activity. A significant Cliff's delta in the opposite direction (random > need-related) would also falsify.

### Resource limits
- Max 200 API requests (1 askstories + 200 item fetches)
- Timeout 30 seconds per request
- Stdlib only (urllib, json, statistics)
- No external dependencies

### Output
- `results.json`: Raw data + gate results + Cliff's delta + p-value
- `classification.json`: Per-post classification with keyword matches
- `RESULT.md`: Human-readable summary with evidence labels

## Expected outcomes

If H1 supported: View-count principle extends to community news aggregators with explicit ask categories.
If H0 supported: Principle boundary confirmed — works on package registries (leaf consumption) but not on community ask forums (where all asks are needs by definition, so no differential).

Either result advances the mission by mapping the principle's boundary conditions.