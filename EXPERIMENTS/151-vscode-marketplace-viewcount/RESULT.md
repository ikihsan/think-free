<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# Experiment 151: VS Code Marketplace (Open VSX) View-Count Principle Test

**Decision: FAIL (population kill gate: insufficient samples)**

Need-related extensions: 4519
General extensions: 24
Excluded: 40

## downloadCount

- Need-related: n=4519, median=2,603, mean=265,705
- General: n=24, median=2,830, mean=23,523
- Cliff's delta: **-0.0551** (95% CI: [-0.2439, 0.1699])
- Mann-Whitney U: 51234.0, p=0.640362
- Shuffle test p: 0.6930

## Interpretation

The population kill gate fired: only 24 general extensions (themes, icons, keymaps, snippets) could be sampled vs. 4,519 need-related extensions, against a pre-declared threshold of 30 per group. This is a limitation of the Open VSX search API, which returns only the top 100 results per query sorted by download count, with significant overlap across queries. Theme/icon/keymap/snippet extensions have systematically lower download counts than language/tool extensions and do not appear in sufficient numbers.

With the available sample, Cliff's delta = -0.0551 (95% CI: [-0.24, 0.17]), indicating no meaningful difference in download counts between need-related and general extensions. The view-count principle test is inconclusive on this platform due to API sampling limitations, not due to a measured effect.

## API Limitation Note

The Open VSX search API (`/-/search`) returns only the top 100 results per query sorted by `downloadCount`. Pagination returns identical results for all pages. This prevents stratified or random sampling. General extensions (themes, icons, keymaps, snippets) have median download counts ~2,800 vs. ~2,600 for need-related, but the top 100 theme query results are exhausted after ~80 unique general extensions, many of which are deduplicated across queries or misclassified due to language/framework keywords in their names.

## Kill Gate Status

- Primary (Cliff's delta < 0.147): FIRED
- Direction (Cliff's delta < -0.147): NOT FIRED
- Population (n < 30): FIRED
