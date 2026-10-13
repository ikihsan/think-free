<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E117 — view-count principle on Hackage (Haskell package registry)

**Date:** 2026-11-01 · **Status:** prototype — evidence-gathering, not product validation.

## The question

Can the `view_count` principle be operationalized on a non-software domain using a package registry archive, where "arrivals" are measured by download counts? This prototype is not expected to produce a candidate or a product. It is an evidence-gathering prototype that tests whether the `view_count` principle can be operationalized on a Haskell package archive with a matched-harvest design and a word-boundary-aware classifier.

If successful, it extends the principle's boundary conditions beyond the 5 package ecosystems already validated (PyPI, NPM, NuGet, Hex.pm, CPAN) into a sixth ecosystem with different linguistic conventions. If unsuccessful, it documents the domain limits of the principle for another package ecosystem.

**Who experiences this:** Haskell developers and package maintainers who need to identify high-impact or popular packages in the Hackage repository.

**Available evidence:** View-count principle works on 5 package ecosystems (PyPI, NPM, NuGet, Hex.pm, CPAN) and on Stack Exchange non-software Q&A. The principle does not generalize to platforms without exposable arrival metrics (GitHub issues API, web search, Automotive OBD2 codes, CFPB consumer complaints). Hackage provides exposable download count metadata, making it a candidate for extending the principle's boundary conditions.

**What the next action could establish:** Whether the view-count principle generalizes to a sixth package ecosystem (Haskell/Hackage) with download-based arrival metrics, and what classifier design works best when the arrival metric is download counts rather than view counts or citations.

## Design — the matched harvest

| Element | Value |
|---|---|
| **Domain** | Haskell package registry (Hackage) |
| **Pool query** | One query via Hackage API, no need vocabulary in the query |
| **Pool size** | target 300 rows (150 need + 150 generic) |
| **Label assignment** | Random assignment after pool fixation (matched harvest: label cannot restate selection) |
| **Classifier** | Word-boundary regex patterns matching need indicators vs generic terms in package description, with AMENDMENT-3 masking |
| **Arrival metric** | Per-paper download count from the archive's API |
| **Stratification** | By package category, to hold fame/age constant |
| **Unlabelled exclusion** | Papers classified as "unlabelled" (both need and generic terms fire, or neither fires) are excluded from the need/generic comparison and counted separately, per D082. |

Asymmetry is removed by construction: identical query, identical sort, identical age band, only the label differs.

## Gates, declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need papers and ≥ 30 generic papers harvested, each with download data fetchable | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 10 seeded control papers — 5 known high-download, 5 known low-download — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of high-download papers (download > 0) in the need arm, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4 answerability sub-test** | 17 of 20 top-arrival need papers classified as high-download or low-download (i.e., labelled, not unlabelled) | the answerability gap generalizes; the `view_count` principle does not serve the top-arrival need population |

**Denominators.** Every fraction is over rows read, and rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Ceiling, stated now

One Haskell package registry (Hackage); one rubric with word-boundary-aware classification using both description and keywords; and one corpus of packages fetchable via the archive's API. This measures the operationalizability of the `view_count` principle using a package registry archive with matched harvest design. It does not measure demand, does not measure adoption, and does not close any candidate.

## Reproduce

```bash
python3 EXPERIMENTS/117-hackage-viewcount/harvest.py    # fetch pool, split arms
python3 EXPERIMENTS/117-hackage-viewcount/outcome.py    # every gate above
```

Needs internet access for the archive API, and Python 3.8+ with `requests` or `urllib`.