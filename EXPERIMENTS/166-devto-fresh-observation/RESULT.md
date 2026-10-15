# RESULT: Dev.to Community Articles Fresh Observation

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

## Experiment Summary

**Experiment:** 166-devto-fresh-observation
**Date:** 2026-10-15
**Status:** Complete — **INVALIDATED BY DATA QUALITY ISSUE**

## Outcome

**EXPERIMENT INVALID** — The view-count principle test cannot be evaluated because the key metadata (`page_views_count`) is **0 for all 196 articles**. The "ALL GATES PASS" result is an artifact of using reactions/comments as a proxy, not a genuine view-count test.

## Gate Results (As Computed)

| Gate | Status | Details |
|------|--------|---------|
| G1 (sample size ≥30 per arm) | PASS | 41 need-related, 100 random (after sampling) |
| G2 (need-related activity >0 ≥80%) | PASS | 100% (activity = reactions×10 + comments×50) |
| G3 (Cliff's δ ≥ 0.147, p < 0.05) | PASS | δ = 0.301, p = 0.0051 |
| G4 (metadata universality) | **FAIL (actual)** | `page_views_count` = 0 for 100% of articles |

## Root Cause

**The Dev.to public API does not expose real page view counts.**

- All 196 articles returned `page_views_count: 0`
- This includes articles published days ago with hundreds of reactions
- The field appears to be either:
  - Only available to article authors (private metric)
  - Requires authentication
  - Not implemented in the public API endpoint

**Evidence:** Article "How I Feel about the Grace Hopper Celebration Getting Cancelled" has 83 reactions, 9 comments, but `views: 0`. Article "Requests, Promises, Assertions..." has 19 reactions, 17 comments, `views: 0`.

## Classifier Analysis

| Need Tag | Count | Notes |
|----------|-------|-------|
| discuss | 15 | Overbroad — "discuss" ≠ need-seeking |
| tutorial | 5 | Legitimate need-indicator |
| beginners | 2 | Legitimate |
| learning | 1 | Legitimate |

| Need Keyword | Count |
|--------------|-------|
| why | 10 |
| vs | 4 |
| best | 3 |
| how to | 2 |
| guide | 1 |
| learn | 1 |
| alternative | 1 |

**Classifier issue:** "discuss" tag (15/41 need-classified) is not a need-indicator — it's a discussion format tag. This contaminates the need arm with non-need content.

## Activity Data (Reactions/Comments Only)

| Arm | n | Mean Activity | Median Activity |
|-----|---|---------------|-----------------|
| Need-related (classified) | 41 | 1,297 | 950 |
| Random | 100 | 1,016 | 310 |

Activity = `reactions × 10 + comments × 50` (views=0 for all)

Cliff's delta = 0.301 (p = 0.005) but **measures reaction/comment engagement, not view arrivals**.

## Honest Limitations

- **Fatal:** `page_views_count` is not a real view count in the public API. The view-count principle requires exposure/arrival metadata; reactions/comments are engagement, not arrival.
- **Classifier contamination:** "discuss" tag over-classifies. True need-indicators: tutorial, beginners, learning, howto, questions, askdev, help.
- **Survivorship bias:** Only 196/2000 articles were from last 30 days; older articles not fetched due to pagination limits.
- **No view_count alternative:** Dev.to does not expose any arrival/exposure metric publicly.

## What This Does NOT Mean

- It does **not** mean the view-count principle works on Dev.to. The test measured the wrong thing.
- It does **not** mean need-related content gets more views on Dev.to. Views are unobserved.
- It does **not** invalidate the protocol. The protocol's G4 gate (metadata universality) should have caught this — the metadata exists but is **not meaningful**.

## Protocol Fix Needed

G4 must verify that the activity metric **actually measures arrivals/exposure**, not just that the field exists. Add: "G4b: spot-check ≥5 articles against known external view counts or author-reported analytics."

## Next Action

Per mission protocol: **preserve the reason, then move to a different opportunity.**

The failure reason is **metadata unavailability** — the platform does not expose the required arrival/exposure signal publicly.

**Decision:** Move to a different domain with genuine view/exposure metadata.

Candidate domains with verifiable view/exposure metadata:
- **GitHub repository traffic** (views/clones) — but requires auth
- **npm download counts** — already tested (works)
- **PyPI download stats** — already tested (works)
- **Docker Hub pull counts** — already tested (works)
- **Reddit post views** — API blocked (E145)
- **YouTube video views** — requires API key
- **Wikipedia page views** — public API exists (`pageviews` endpoint)
- **arXiv paper downloads** — no public per-paper download counts
- **Thingiverse model views/downloads** — public API
- **GrabCAD model views/downloads** — may require auth

**Selected next domain:** **Wikipedia page views** — public API, genuine view counts, "need" = article creation requests / "Requested articles" / stubs needing expansion. Distinct platform type (encyclopedia), not tested.

Or: **Thingiverse** — 3D model platform, public API, views/downloads, needs = model requests / "make this" posts.

Let me choose **Wikipedia** as it has a robust public pageview API and a clear "need" category (Wikipedia:Requested articles, stub articles).