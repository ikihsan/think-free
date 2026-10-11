<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E104 — View-count principle on RubyGems — Gate Evaluation

## Data import

Load the raw harvest results from `results.json` (output of `harvest.py`). Expected fields per gem:
`name`, `description`, `needs_classification`, `recent_downloads`, `total_downloads`, `api_url`, `classification_reason`.

## Active definition

A gem is **"active"** if `recent_downloads > 0`. Follows E095/E102 precedent.

## Classification summary

From the harvested sample, count:
- `n_need_related`: gems classified as need-related
- `n_random`: gems classified as random
- `n_active_need`: need-related gems with recent_downloads > 0
- `n_active_random`: random gems with recent_downloads > 0
- `p_need_active`: `n_active_need / n_need_related`
- `p_random_active`: `n_active_random / n_random`

## Gate evaluation

| Gate | Criterion | Threshold | Pass/Fail |
|------|-----------|-----------|-----------|
| **G1** | Classified sample size | ≥ 100 total (50 per group minimum) | |
| **G2** | Need-related active rate > random active rate | Mann-Whitney U test, p < 0.05, Cliff's delta > 0.147 | |
| **G3** | Effect size — Wilson LB | Wilson CI95 lower bound for proportion of need-related above random median > 0.60 | |
| **G4** | Both categories represented | need-related > 0 AND random > 0 | |

## Mann-Whitney U test

- Test whether the distribution of `recent_downloads` differs between need-related and random groups
- `p < 0.05` indicates statistically significant difference
- Cliff's delta > 0.147 indicates a small but meaningful effect size

## Wilson CI95 computation

For the proportion of need-related active gems:
- `p_need_active` = n_active_need / n_need_related
- Wilson score interval at 95% confidence
- Lower bound (LB) must be > 0.60

## Decision table

| G1 | G2 | G3 | G4 | Verdict |
|----|----|----|----|---------|
| Pass | Pass | Pass | Pass | Principle supported on RubyGems |
| Pass | Fail | — | — | Principle does not generalize |
| Pass | Pass | Fail | — | Effect size too small |
| Pass | Pass | Pass | Fail | Only one category has data |
| G1 not met | — | — | — | Route not measurable at this cost |

## Run

```bash
python3 EXPERIMENTS/104-rubygems-viewcount/analyze.py
```