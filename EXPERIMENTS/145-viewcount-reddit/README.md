<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E145 — View-Count Principle on Reddit

**Result: GATE_CLOSED — data accessibility boundary**

## Experiment ran 2026-10-15

The view-count principle was tested on Reddit communities, but the experiment was
blocked at the data accessibility gate. The Reddit API returned a network security
block (HTTP 410 Gone / blocked by network security policy) when accessed from the
experiment environment using unauthenticated curl requests with a custom User-Agent.

### What was tested

- 5 subreddits were selected: programming, learnpython, webdev, django, python
- 50 hot posts per subreddit were attempted (total target: 250 posts)
- Posts were to be classified as `need-related` or `random` based on title keywords
- Engagement metrics (post scores) were to be compared between the two groups

### What happened

The Reddit API endpoint `https://www.reddit.com/r/programming/hot.json?limit=50`
returned the HTML block page: "You've been blocked by network security. To continue,
log in to your Reddit account or use your developer token."

This is a **data accessibility boundary**: the Reddit public API is not reliably
accessible from this environment without authentication. This is consistent with
previous mission findings where API throttling, authentication requirements, and
network restrictions have blocked experiments (e.g., E079 automotive OBD2 on
Mechanics.SE with 300 req/day limit, E082 Discourse forums required specific API
configuration).

### Gate results

| Gate | Status | Notes |
|------|--------|-------|
| G1 | FAIL | 0 posts fetched; retrieval impossible |
| G2 | N/A | Cannot evaluate without fetched posts |
| G3 | N/A | Cannot evaluate without fetched posts |
| G4 | N/A | Cannot evaluate without fetched posts |

### Evidence recorded

- `EXPERIMENTS/145-viewcount-reddit/collect.py` — Data collection script
- `EXPERIMENTS/145-viewcount-reddit/results.json` — Experiment results (G1 fail)
- The Reddit API blocking is itself a valid data point about platform accessibility
  boundaries for the view-count principle

### Decision

The view-count principle's generalization to Reddit could not be assessed because
the platform's data is not accessible from this environment without authentication.
This documents an important boundary condition: not all platforms with potential
engagement metrics are experimentally accessible without authentication.

Per the protocol, negative results close the claim and population actually tested
— they do not automatically close an application domain or discovery route.
Future work on Reddit would need to address data accessibility (authentication,
rate limits, or alternative data sources).