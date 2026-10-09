<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E071 — PyPI package activity as view_count proxy

Session `2026-10-09-004`, VM `instance-20260717-0944`, declared 2026-10-09.

## The question

Can PyPI JSON API package metadata (release count, project URLs, classifiers)
operationalize the `view_count` principle — measuring independent arrivals at a
need on every row, asking the question of the platform rather than the person?

The `view_count` instrument (E062, E063) measures independent arrivals at a need
per repository / per row. This prototype tests whether PyPI package metadata can
serve as a proxy for arrival metrics on the Python packaging platform.

### The candidate decision this changes

**If the prototype can recover activity metrics that classify packages
consistently with the view_count principle** (e.g., packages with high activity
scores correspond to needs that were "arrived at" by independent users), it
demonstrates that PyPI metadata is a reusable instrument for future corpus
measurements without needing platform-specific API keys beyond what PyPI
already provides.

**If the prototype cannot recover meaningful activity metrics**, it documents
the technical gap and confirms that `view_count` measurement on PyPI requires
access to download statistics (available via BigQuery or similar, not the JSON
API). This does not close any candidate but documents a limitation for future
work.

This experiment is not expected to produce a product, and the README must not
imply that it did.

## Arms

| arm | source | what it carries |
|---|---|---|
| **A** | PyPI packages relevant to need statements from E062/E063 corpora (10 rows) | package name, metadata, activity score |
| **B** | Randomly selected PyPI packages not related to need statements (10 rows) | package name, metadata, activity score |

**Why these arms.** Arm A tests whether packages related to stated needs have
higher activity than arm B. Both arms are populated before any measurement.

## The rubric, written before the rows

| classification | criterion |
|---|---|
| **active** | activity_score >= 10 (indicates multiple releases + project URLs) |
| **inactive** | 0 < activity_score < 10 (indicates a single release, minimal metadata) |
| **missing** | package not found on PyPI (404 error) |

## Gates, all declared before any package was queried

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | >= 5 need-related packages harvested from PyPI, each yielding metadata | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | arm A's mean activity score differs from arm B's mean at ≠ (two-sample t-test, p < 0.05) | the activity rubric does not differentiate arms and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of need-related packages classified as `active`, with Wilson CI95, over >= 5 rows per arm | this is the result; no gate |

**G3 is the key gate.** It measures the fraction of need-related packages that
are classified as `active`. A high fraction (lower CI95 > 0.6) supports the view_count
principle on PyPI: need-related packages are systematically more active.
A low fraction (upper CI95 < 0.4) refutes it: need-related packages are not
systematically more arrived at.

## Extraction rule, written before the rows

A package's metadata is retrieved from the PyPI JSON API (`/pypi/{name}/json`).
The activity score is computed as follows:

- Release count: `min(release_count // 10, 10)` points
- Has Homepage URL: +5 points
- Has Documentation URL: +3 points
- Has Source URL: +2 points
- Development Status classifier 5 (Production/Stable): +5 points
- Development Status classifier 4 (Beta): +3 points

Total activity score ranges from 0 to ~40. Thresholds:
- active: score >= 10
- inactive: 0 < score < 10
- missing: 404 error / package not found

## Ceiling, stated now

One VM; one Python 3.8 interpreter; one PyPI JSON API access; 20 packages
(10 need-related, 10 random). This measures the operationalizability of the
view_count principle using PyPI metadata as a proxy for independent arrivals.
It does not measure demand, does not measure adoption, and does not close any
candidate. It opens no product on its own: the build decision is the one written
at the end of this file.

## Reproduce

```bash
python3 EXPERIMENTS/071-pip-name-guard-prototype/harvest.py     # arms A & B
python3 EXPERIMENTS/071-pip-name-guard-prototype/outcome.py     # gate evaluation
```

## Ethics and limitations

- PyPI JSON API access is rate-limited politely (0.5s delay between requests)
- Activity score is a proxy, not a direct measure of download counts or user arrivals
- Does not account for transitive dependencies or ecosystem-specific factors
- Does not measure whether a need was actually solved, only whether the package
  shows signs of independent arrival (activity)