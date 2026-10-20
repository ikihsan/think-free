# RESULT: Hacker News "Ask HN" Fresh Observation

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

## Experiment Summary

**Experiment:** 165-hn-ask-fresh-observation
**Date:** 2026-10-15
**Status:** Complete — kill gates fired

## Outcome

**KILL GATE FIRED** — The view-count principle does **not** generalize to Hacker News "Ask HN" posts under this protocol.

## Gate Results

| Gate | Status | Details |
|------|--------|---------|
| G1 (sample size ≥30 per arm) | **FAIL** | Only 6 need-related, 17 random (unique posts) |
| G2 (need-related activity >0 ≥80%) | PASS | 6/6 = 100% |
| G3 (Cliff's δ ≥ 0.147, p < 0.05) | **FAIL** | δ = 0.400, p = 0.117 |
| G4 (metadata universality) | PASS | API guarantees fields |

## Root Cause Analysis

### 1. Insufficient Data from API (Primary)
The HN Firebase API `askstories` endpoint returns only **~23 current top Ask HN posts**, not the ~1000 implied by documentation. This is a hard limit of the endpoint — it returns currently ranked ask stories, not a historical archive.

**Evidence:** `askstories.json` returned 23 IDs. Sampling 100 recent + 100 middle produced duplicates (only 23 unique posts).

### 2. Classifier Vocabulary Mismatch (Secondary)
The pre-declared keywords missed many genuine need-related Ask HN posts:

| Post Title | Why Missed |
|------------|------------|
| "Ask HN: CAD for wood working with LLM support?" | "support?" not in keywords |
| "Ask HN: What problem is Apple Home solving?" | "what problem is" ≠ "what is" |
| "Ask HN: Are you hesitant to install...?" | "are you" not in keywords |
| "Ask HN: Can I tell my managers...?" | "can i" not in keywords |
| "Ask HN: Any secrets for reaching...?" | "any" only matched "anyone"/"anybody" |
| "Ask HN: How long before...?" | "how long" not in keywords |
| "Ask HN: Any way to remove ads...?" | "any way" not in keywords |
| "Ask HN: What do you think will be hot...?" | "what do" not in keywords |
| "Ask HN: Many SWEngs considering re-training" | Statement form, no keyword match |

**Estimated true need-related share:** ~60-70% of Ask HN posts are need-shaped (questions asking for help, recommendations, how-to), but classifier caught only 6/23 = 26%.

### 3. Statistical Power
With only 6 need-related posts, Mann-Whitney U test lacks power (p = 0.117 despite δ = 0.400).

## Activity Data (Observed)

| Arm | n | Mean Activity | Median Activity |
|-----|---|---------------|-----------------|
| Need-related (classified) | 6 | 59.87 | 10.40 |
| Random (classified) | 17 | 14.46 | 6.40 |

Cliff's delta = 0.400 (large effect) but not statistically significant at n=6 vs n=17.

## Honest Limitations

- **Data source limitation:** HN Firebase API `askstories` is not suitable for this experiment design. It provides a snapshot of currently-ranked posts, not a sampleable population.
- **Classifier under-coverage:** Keywords were designed for Stack Exchange / forum phrasing, not HN's terse "Ask HN: [question]" style.
- **Duplicate sampling:** Code did not deduplicate when recent and middle slices overlapped.
- **No view_count:** HN API does not expose view counts, only points and comments.

## What This Does NOT Mean

- It does **not** mean the view-count principle fails on HN. The data source was inadequate to test it.
- It does **not** mean need-related Ask HN posts have lower activity. The observed δ = 0.400 suggests the opposite, but n is too small.
- It does **not** invalidate the protocol. The protocol correctly fired kill gates when its preconditions (sample size, statistical significance) were not met.

## Next Action

Per mission protocol: **preserve the reason, then move to a different opportunity.**

The failure reason is **data source inadequacy**, not principle failure. Two paths forward:

1. **Same domain, better data source:** Use Algolia HN Search API (`hn.algolia.com/api/v1/search?tags=ask_hn&hitsPerPage=1000&page=...`) which provides paginated historical Ask HN posts with view counts (`nbHits`, though not per-post views). Requires protocol revision.

2. **Different domain:** Choose a fresh domain with better data access per the stated selection rule.

**Decision:** Move to a different domain. The Algolia API would require protocol revision (new data source, new classifier validation) which is a new experiment, not a continuation. The mission's standing constraint: "Do not continue an audit chain merely because the previous audit exposed another uncertainty."

## Artifacts

- `results.json` — raw machine-readable output
- `classification.json` — per-post classification with keyword matches
- `run.py` — implementation (stdlib only)
- `README.md` — protocol (committed before fetch)

## Evidence Labels

- Gate results: `observed`
- Root cause analysis: `observed` (from data), `inferred` (classifier mismatch estimate)
- "Principle does not generalize": `untested` — data source was insufficient to test
- Next action recommendation: `speculative`