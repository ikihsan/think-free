# Fresh Observation: Wikipedia Articles — View-Count Principle Test

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

## Hypothesis

**H0 (null):** On Wikipedia, stub articles (short articles marked as needing expansion, representing unmet information needs) do not have systematically higher page views per byte than developed articles.

**H1 (alternative):** On Wikipedia, stub articles have systematically higher page views per byte than developed articles, measured by Cliff's delta ≥ 0.147 on views-per-byte.

This tests whether the view-count principle — that need-related content attracts systematically more activity — generalizes to an encyclopedia where "need-related" = articles explicitly marked as incomplete (stubs), representing unmet information demand.

## Domain Selection Rule (Stated Before Fetch)

Select the largest platform by estimated monthly active users in the "reference knowledge" category that:
1. Has a public API requiring no authentication for view metadata
2. Has a distinct "need statement" format (explicit quality/need markers like stub templates)
3. Has measurable activity signals (page views per article, per day)
4. Has not been tested by this mission's view-count principle
5. Is not a package registry, Stack Exchange Q&A forum, fault code database, news aggregator, developer blogging platform, or model hub

Wikipedia satisfies all five: public REST API for pageviews (no auth), `{{stub}}` templates explicitly mark articles needing expansion, pageviews per article per day via `pageviews` endpoint, not previously tested, distinct platform type (encyclopedia).

## Prior Art Check

- Wikipedia Pageviews API: https://wikimedia.org/api/rest_v1/ (public, no auth)
- ~20B+ pageviews/month across all languages
- Stub articles: ~2M+ on English Wikipedia (Category:All stub articles)
- No prior work found testing "view-count principle" on Wikipedia stubs vs developed articles
- Platform type distinct: not artifact registry, not discussion forum, not marketplace

## Protocol

### Data Source
- Wikipedia REST API:
  - Pageviews: `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{title}/daily/{start}/{end}`
  - Article info: `https://en.wikipedia.org/w/api.php?action=query&prop=info|categories|templates&format=json`
  - Category members: `https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:All_stub_articles&format=json`
  - Random articles: `https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&format=json`

### Sampling
1. Fetch 200 stub article titles from `Category:All_stub_articles` (using categorymembers, limited to main namespace)
2. Fetch 200 random article titles from `list=random&rnnamespace=0` (main namespace, non-stub)
3. For each article, fetch pageviews for last 30 days (daily, summed)
4. For each article, fetch content length (bytes) via `prop=info`

### Classification (Pre-declared)

**Need-related (treatment):** Articles in `Category:All_stub_articles` (explicitly marked with `{{stub}}` or sub-stub templates, indicating unmet information need)

**Developed (control):** Random main-namespace articles NOT in any stub category

### Activity Metric
**Views per byte** = `total_pageviews_last_30_days / article_length_bytes`
- Normalizes for article length (stubs are short by definition)
- Measures view density: how much demand per unit of content
- Alternative: raw views (but stubs are short, so raw views may be lower)

Both metrics computed; primary = views per byte.

### Gates (Pre-declared)

**G1 (sample size):** Both arms ≥ 30 articles with valid data
**G2 (activity presence):** ≥ 80% of stub articles have views > 0
**G3 (differential activity):** Cliff's delta ≥ 0.147 on views-per-byte (stubs vs developed)
**G4 (metadata universality):** 100% of sampled articles have pageviews data and length > 0

### Kill Conditions
- Any gate FAIL → principle does not generalize to this domain
- G3 FAIL with p ≥ 0.05 (Mann-Whitney U) → no evidence of differential activity
- Metadata unavailable for >20% of sample → G4 FAIL

### Falsification
Strongest accessible alternative: "no systematic difference" — stubs and developed articles have similar view density. Significant Cliff's delta in opposite direction (developed > stubs) would also falsify.

### Resource Limits
- Max ~400 API requests for pageviews (200 + 200) + category/random fetches
- Timeout 30 seconds per request
- Stdlib only (urllib, json, statistics, datetime)
- Rate limit: be respectful (0.5s between requests)

### Output
- `results.json`: Raw data + gate results + Cliff's delta + p-value
- `classification.json`: Per-article data with views, bytes, views-per-byte
- `RESULT.md`: Human-readable summary with evidence labels

## Expected Outcomes

If H1 supported: View-count principle extends to encyclopedias — unmet information needs (stubs) attract disproportionate views per unit content.
If H0 supported: Principle boundary confirmed — works on artifact registries (packages, repos, extensions) but not on reference knowledge platforms where stubs indicate incompleteness, not specialized need-serving.

Either result advances the mission by mapping the principle's boundary conditions.