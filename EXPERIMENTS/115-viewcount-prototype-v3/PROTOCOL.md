<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E115 — view-count prototype v3: matched harvest on PyPI

**Date:** 2026-10-12 · **Status:** prototype — evidence-gathering, not product validation.

## The question

Can the `view_count` principle be operationally realized on PyPI using a
matched-harvest design and a word-boundary-aware classifier, without the
harvest artifacts that confounded E107/E113? This prototype is not expected
to produce a candidate or a product. It is an evidence-gathering prototype
that tests whether the `view_count` principle can be operationalized with
proper controls on the PyPI platform.

If successful, it provides a reusable instrument for future corpus measurements
on package ecosystems. If unsuccessful, it documents the technical gap and
confirms that `view_count` measurement on package platforms requires proper
design (matched harvest, coverage floor, age-controlled comparison).

**This experiment is not expected to produce a product, and the README must not
imply that it did.**

## The practical difficulty

Python developers who need to find packages addressing specific unmet needs
cannot reliably differentiate need-relevant packages from popular-but-general
ones using download counts alone, because popular packages inflate the
apparent relevance of need-related queries. The view-count principle (need-related
artifacts receive more arrivals than random ones) has been validated on PyPI
(E071, E102-adjacent) but previous designs have been vulnerable to confounds
from asymmetric arm design and classifier coverage gaps.

**Who experiences this:** Python developers, data scientists, software teams
choosing dependencies who need to find relevant packages quickly and reliably.

**Available evidence:** View-count principle works on PyPI (82.9% active vs 57.5%
random, all gates met in E071/E102). But the classifier only labels ~28% of rows
in earlier designs (E113 coverage issue), and harvest artifacts from asymmetric
arm design confound the effect (E113/F116). Boundary conditions: principle works
on mature package ecosystems with exposable metadata (PyPI, NPM, NuGet, Hex.pm),
does not generalize to platforms without such metadata (GitHub repos, crates.io,
Maven Central, Hugging Face).

**What the next action could establish:** Whether a matched-harvest view-count
prototype with word-boundary-aware classification and API failure handling can
reliably differentiate need-related packages from random ones on PyPI, with
known false-positive/false-negative rates, and produce a prioritized package
list ranked by need-relatedness+active-rate product.

## Design — the matched harvest

| Element | Value |
|---|---|
| **Platform** | PyPI (Python Package Index), using the JSON API at https://pypi.org/pypi/{package}/json |
| **Pool size** | target 300 packages (150 need + 150 generic) |
| **Label assignment** | Random assignment after pool fixation (matched harvest: label cannot restate selection) |
| **Classifier** | Word-boundary regex patterns matching need indicators vs generic terms in package description + keywords. AMENDMENT-3 masking so `learning` does not cancel `machine learning`. |
| **Activity metric** | PyPI JSON API success/failure: a package is "active" if its metadata is fetchable from the PyPI JSON API. This is a binary, platform-agnostic metric. |
| **Stratification** | By package name initial letter, to ensure distribution across the alphabet. |
| **Unlabelled exclusion** | Packages classified as "unlabelled" (both need and generic terms fire, or neither fires) are excluded from the need/generic comparison and counted separately, per D082. |

Asymmetry is removed by construction: identical query (no need vocabulary), identical
pool, only the label differs. The label is assigned randomly after the pool is
fixed, so it cannot be a restatement of how the row was selected.

## Gates, declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need packages and ≥ 30 generic packages harvested, each with successful PyPI JSON API fetch | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 10 seeded control packages — 5 known served, 5 known unserved — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of active packages (API success) in the need arm, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4 answerability sub-test** | 17 of 20 top-arrival need packages classified as `need` or `generic` (i.e., labelled, not `unlabelled`) | the answerability gap generalizes; the `view_count` principle does not serve the top-arrival need population |

**Denominators.** Every fraction is over rows read, and rows not read are reported
as rows not read. Per D082, an arm that produced no observation is a missing
observation, never a zero and never a denominator.

**G0 kill gate (predeclared, must pass first):** The labeler must recover
independent real positives: seeded on 20 packages with descriptions explicitly
containing a technology noun (`database`, `cache`, `auth`, `orm`, etc.) it must
label `need` at ≥ 9/10 and on 20 packages matching only generic vocabulary at
`generic` ≥ 9/10. Kill: G0 below threshold stops the experiment — a labeler
that cannot find planted positives cannot be trusted to find natural ones.

## Ceiling, stated now

One platform (PyPI) JSON API; one rubric with word-boundary-aware classification
using both description and keywords; and one corpus of packages fetchable via
the PyPI JSON API. This measures the operationalizability of the `view_count`
principle using the PyPI JSON API, with matched harvest design confirming the
effect is not a harvest artifact. It does not measure demand, does not measure
adoption, and does not close any candidate.

## Reproduce

```bash
python3 EXPERIMENTS/115-viewcount-prototype-v3/harvest.py    # fetch pool, split arms
python3 EXPERIMENTS/115-viewcount-prototype-v3/outcome.py    # every gate above
```

Needs internet access for the PyPI JSON API, and Python 3.8+ with `requests`
or `urllib`.