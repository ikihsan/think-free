<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E173 Protocol — View-count Principle on GitHub Discussions

## Arms

- **Arm A**: Discussions classified as "need-related" (title or labels contain a need indicator from the mission's vocabulary)
- **Arm B**: Discussions classified as "random" (no need indicator found in title or labels)

## Classification Rule

Each discussion from the GitHub Discussions API/search is classified as follows:

1. Extract the discussion `title` and `labels` (list of label texts).
2. Lowercase both.
3. If any word in the title or any label text matches a whole-word entry from `NEED_INDICATORS` (viewcount_core.py), classify as `"need-related"`.
4. Otherwise, classify as `"random"`.

This mirrors the word-boundary matching used for package descriptions, applied to discussion title and label text.

## Gates (G1–G4)

Using the standard `compute_gates` function from `tools/viewcount_framework.py`:

- **G1**: need-related active rate / random active rate >= 0.55
  - Active = discussion has non-zero arrival metric (primary) or activity (secondary)
  - need-related active rate = (need-related discussions with activity > 0) / (total need-related classified)
  - random active rate = (random discussions with activity > 0) / (total random classified)
- **G2**: total classified >= 100
- **G3**: both categories represented (need-related > 0 and random > 0)
- **G4**: total classified >= 50

**Kill condition**: G1 fails AND G2 fails (both the activity advantage and the sample size are insufficient). If G1 passes, the principle is supported for this domain.

## Activity Metric — Primary Question

**Does GitHub Discussions publish a per-discussion arrival metric?**

The experiment will determine this by attempting to fetch an arrival/metric field from the Discussions API or web page. Possible metric names include:
- `view_count` / `views` / `viewCount`
- `popularity` / `score` / `hotness`
- `last_viewed` / `visited`
- Any numeric metric that represents per-discussion arrival/interest

If no such metric exists in the available data source, the experiment will record this as the finding and conclude the venue is not measurable for the principle (per D088).

## Data Fetch

- **Primary**: GitHub Discussions search/API endpoint
  - If unauthenticated API is available: use it with appropriate headers
  - If only web page scraping is possible: use the discussions page
- **Fields per discussion**: `title`, `body`, `labels`, `created_at`, `updated_at`, and any arrival/metric field
- **Sample size**: All available discussions (minimum 50 desired for G4)

## Procedure

1. **Write PROTOCOL-E173.md** (this file) and commit.
2. **Fetch data** from the GitHub Discussions source.
3. **Determine if a per-discussion arrival metric exists** — this is the primary question.
4. **If a metric exists**: classify each discussion and compute gates G1–G4.
5. **If no metric exists**: record the finding that the venue is not measurable for the principle (D088), note the lack of metric, and conclude.
6. **Compute Cliff's delta** on the metric between need-related and random groups (if metric exists).
7. **Record RESULT.md** with full results.
8. **Update STATE.md** and `FAILURES-findings.md` with outcomes.

## Notes

- This is the first view-count principle test on GitHub Discussions.
- The need-indicator vocabulary was designed for package descriptions; its applicability to discussion titles/labels is part of the experiment.
- If classification yields very few need-related discussions (e.g., < 10), the experiment should note this as a vocabulary-inapplicability finding.
- The declared bar for a "supported" result is G1 pass (ratio >= 0.55) with at least G2 passing (classified total >= 100).
- If no per-discussion arrival metric is found, the experiment stops after determining this fact and recording the result — no classification or gate computation is needed beyond confirming the absence of a metric.

## Failure Condition (D088)

If GitHub Discussions does not publish a per-discussion arrival metric (view_count analogue), the venue is not measurable for the principle. The experiment will record this as the outcome and close the venue for future view-count principle testing, similar to how Q&A forums were closed when program-shaped residue was found to be zero.