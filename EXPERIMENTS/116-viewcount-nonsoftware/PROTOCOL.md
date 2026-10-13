<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E116 — view-count principle on non-software conference proceedings

**Date:** 2026-11-01 · **Status:** prototype — evidence-gathering, not product validation.

## The question

Can the `view_count` principle be operationalized on a non-software domain using
conference proceeding archives, where "arrivals" are measured by citation counts
or acceptance follow-up? This prototype is not expected to produce a candidate or
a product. It is an evidence-gathering prototype that tests whether the
`view_count` principle can be operationalized on a conference proceeding archive
with a matched-harvest design and a word-boundary-aware classifier.

If successful, it extends the principle's boundary conditions beyond software
package ecosystems into academic research evaluation. If unsuccessful, it documents
the domain limits of the principle for non-software contexts.

**This experiment is not expected to produce a product, and the README must not
imply that it did.**

## The practical difficulty

Academic researchers and librarians who need to identify foundational or
high-impact papers in their field cannot reliably differentiate high-impact
papers from merely popular ones using citation counts alone, because citation
counts inflate the apparent relevance of well-known topics. The view-count
principle (need-related papers receive more arrivals than random ones) has been
validated on software package ecosystems (PyPI, NPM, NuGet, Hex.pm, CPAN) but
has not been tested on non-software archives.

**Who experiences this:** Academic researchers, librarians, funding agencies,
and research administrators who need to identify high-impact or foundational
papers in their field.

**Available evidence:** View-count principle works on 5 package ecosystems
(PyPI, NPM, NuGet, Hex.pm, CPAN) and on Stack Exchange non-software Q&A
(where it measures view-like arrivals). The principle does not generalize to
platforms without exposable arrival metrics (GitHub issues API, web search,
Automotive OBD2 codes, CFPB consumer complaints). Non-software domains may
have different arrival metrics and metadata structures.

**What the next action could establish:** Whether the view-count principle
generalizes to non-software domains with exposable metadata (conference
proceedings, technical archives), and what classifier design works best when
the arrival metric is citations rather than downloads.

## Design — the matched harvest

| Element | Value |
|---|---|
| **Domain** | Conference proceeding archive (open-access papers with citation data) |
| **Pool query** | One query via open-access repository API (e.g., arXiv, CPC), no need vocabulary in the query |
| **Pool size** | target 300 rows (150 need + 150 generic) |
| **Label assignment** | Random assignment after pool fixation (matched harvest: label cannot restate selection) |
| **Classifier** | Word-boundary regex patterns matching need indicators vs generic terms in paper abstract + title, with AMENDMENT-3 masking |
| **Arrival metric** | Per-paper citation count from the archive's API (e.g., arXiv's citation data) |
| **Stratification** | By paper age (year of publication), to hold fame/age constant |
| **Unlabelled exclusion** | Papers classified as "unlabelled" (both need and generic terms fire, or neither fires) are excluded from the need/generic comparison and counted separately, per D082. |

Asymmetry is removed by construction: identical query, identical sort, identical
age band, only the label differs.

## Gates, declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need papers and ≥ 30 generic papers harvested, each with citation data fetchable | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 10 seeded control papers — 5 known high-impact, 5 known low-impact — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of high-citation papers (citation > 0) in the need arm, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4 answerability sub-test** | 17 of 20 top-arrival need papers classified as high-impact or low-impact (i.e., labelled, not unlabelled) | the answerability gap generalizes; the `view_count` principle does not serve the top-arrival need population |

**Denominators.** Every fraction is over rows read, and rows not read are reported
as rows not read. Per D082, an arm that produced no observation is a missing
observation, never a zero and never a denominator.

## Ceiling, stated now

One non-software archive (conference proceedings); one rubric with word-boundary-aware classification using both abstract and keywords; and one corpus of papers fetchable via the archive's API. This measures the operationalizability of the `view_count` principle using a conference proceeding archive with matched harvest design. It does not measure demand, does not measure adoption, and does not close any candidate.

## Reproduce

```bash
python3 EXPERIMENTS/116-viewcount-nonsoftware/harvest.py    # fetch pool, split arms
python3 EXPERIMENTS/116-viewcount-nonsoftware/outcome.py    # every gate above
```

Needs internet access for the archive API, and Python 3.8+ with `requests`
or `urllib`.