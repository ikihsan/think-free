<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# E065 — view-count measurement prototype

Session `2026-10-08-014`, VM `instance-20260717-0944`, declared 2026-10-08.

## The question

Every population this mission has measured for candidate need comes from one route,
and that route is a software venue: GitHub issue trackers, PyPI, Hacker News, and
Stack Overflow. The `view_count` instrument (E062, E063) measures independent
arrivals at a need on every row, asking the question of the platform rather than
the person. This prototype asks: can a simple web-search-based approach recover
`view_count`-like arrival metrics for need statements, and use them to classify
needs as served, partially served, or unserved?

### The candidate decision this changes

This prototype is not expected to produce a candidate or a product. It is an
evidence-gathering prototype that tests whether the `view_count` principle can be
operationalized with minimal resources. If successful, it provides a reusable
instrument for future corpus measurements. If unsuccessful, it documents the
limitation and the gap for future work.

**If the prototype can recover arrival metrics that classify needs consistently
with E062/E063 findings** (e.g., 17/20 unremedied needs classified as served by
platform arrivals), it demonstrates that `view_count` is operationally useful
and opens the door to future corpus measurements with wider platform coverage.

**If the prototype cannot recover meaningful arrival metrics**, it documents the
technical gap and confirms that `view_count` measurement requires platform-specific
API access (as E062 used Stack Exchange API, E039 used Hacker News API).

This experiment is not expected to produce a product, and the README must not
imply that it did.

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Need statements from E062's non-remedy corpus (110 rows, raw/ noremedry-classified.tsv) | need text, web search results |
| **2 (control)** | Need statements from E063's GH issue corpus (59 rows stating a need, from E038's 189 issues) | need text, web search results |

**Why these populations.** E062 already measured `view_count` on a non-software
population (Steam per-game feature requests). E063 measured answerability on GH
issues. This prototype tests whether web search can recover arrival metrics on
these same corpora, providing a cross-validation of the `view_count` principle
without needing platform-specific API keys.

## The rubric, written before the rows

A need statement is classified based on web search results:

| classification | criterion |
|---|---|
| **served** | Web search returns an accepted answer, a working solution, or a direct link to a tool that addresses the need |
| **partially_served** | Web search returns relevant information but no complete solution (e.g., a partial answer, a workaround, a request for spec sheets) |
| **unserved** | Web search returns no relevant results, or only irrelevant results |

**Two readers** on an overlapping subsample, with κ reported, because reader
separation defects (E023/F043, E029/F049) have shown that single-reader
classification is unreliable without inter-reader agreement.

## Gates, all declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need statements harvested, each yielding web search results | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 10 seeded control statements — 5 known served, 5 known unserved — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of need statements classified as `served`, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4 answerability sub-test** | 17 of 20 top-arrival need statements classified as `served` or `partially_served` | the answerability gap generalizes; the `view_count` principle does not serve the top-arrival need population |

**Denominators.** Every fraction is over rows read, and rows not read are reported
as rows not read. Per D082, an arm that produced no observation is a missing
observation, never a zero and never a denominator.

## Ceiling, stated now

One retrieval route (web search); one rubric with two readers over a subsample;
and two corpora that have already been extensively measured. This measures the
operationalizability of the `view_count` principle using only web search, without
platform-specific API access. It does not measure demand, does not measure
adoption, and does not close any candidate.

## Reproduce

```bash
python3 EXPERIMENTS/065-view-count-prototype/harvest.py     # arms 1 & 2
python3 EXPERIMENTS/065-view-count-prototype/outcome.py     # every gate above
```

Needs internet access for web search, and Python 3.8+ with `requests` or
`urllib`.