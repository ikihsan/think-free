<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E072 — NPM package activity as view_count proxy

Session `2026-10-09-005`, VM `instance-20260717-0944`, declared 2026-10-09.

## The question

Can NPM JSON API package metadata (`registry.npmjs.org/{name}/json`) operationalize the
`view_count` principle — measuring independent arrivals at a need on every row,
asking the question of the platform rather than the person?

The `view_count` instrument (E062, E071) measures independent arrivals at a need
per repository / per row. This prototype tests whether NPM package metadata can
serve as a proxy for arrival metrics on the Node.js packaging platform.

### The candidate decision this changes

**If the prototype can recover activity metrics that classify packages
consistently with the view_count principle** (e.g., packages with high activity
scores correspond to needs that were "arrived at" by independent users), it
demonstrates that the view-count principle generalizes across package repositories
beyond PyPI, supporting the hypothesis that platform characteristics (not the
principle itself) determine whether arrival metrics are available.

**If the prototype cannot recover meaningful activity metrics**, it documents
the technical gap and confirms that the view-count principle on NPM requires
access to download statistics or other metrics not in the JSON API. This does
not close any candidate but documents a limitation for future work.

This experiment is not expected to produce a product, and the README must not
imply that it did.

## Arms

| arm | source | what it carries |
|---|---|---|
| **A** | NPM packages relevant to need statements | package name, metadata, activity score |
| **B** | Random NPM packages not related to need statements | package name, metadata, activity score |

**Why these arms.** Arm A tests whether packages related to stated needs have
higher activity than arm B. Both arms are populated before any measurement.

## The rubric, written before the rows

| classification | criterion |
|---|---|
| **active** | activity_score >= 6 (indicates multiple releases + project URLs) |
| **inactive** | 0 < activity_score < 6 (indicates a single release, minimal metadata) |
| **missing** | package not found on NPM (404 error) |

Total activity score ranges from 0 to ~11. Thresholds:
- active: score >= 6
- inactive: 0 < score < 6
- missing: 404 error / package not found

## Gates, all declared before any package was queried

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | >= 5 need-related packages harvested from NPM, each yielding metadata | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | arm A's mean activity score differs from arm B's mean at ≠ (two-sample t-test, p < 0.05) | the activity rubric does not differentiate arms and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of need-related packages classified as `active`, with Wilson CI95, over >= 5 rows per arm | this is the result; no gate |

**G3 is the key gate.** It measures the fraction of need-related packages that
are classified as `active`. A high fraction (lower CI95 > 0.6) supports the view_count
principle on NPM: need-related packages are systematically more active.
A low fraction (upper CI95 < 0.4) refutes it: need-related packages are not
systematically more arrived at.

## Extraction rule, written before the rows

A package's metadata is retrieved from the NPM JSON API (`/registry.npmjs.org/{name}/json`).
The activity score is computed as follows:

- Release presence (1 point if version string exists): +1
- Has Homepage URL (5 points): +5 if `info.homepage` is present and non-empty
- Has Repository URL (2 points): +2 if `info.repository` is present and contains a `url` field
- Has Keywords (1 point): +1 if `info.keywords` is a non-empty array

Total activity score ranges from 0 to 9. Thresholds:
- active: score >= 5
- inactive: 0 < score < 5
- missing: 404 error / package not found

## Ceiling, stated now

One VM; one Python 3.8 interpreter; one NPM JSON API access; 20 packages
(10 need-related, 10 random). This measures the operationalizability of the
view_count principle using NPM metadata as a proxy for independent arrivals.
It does not measure demand, does not measure adoption, and does not close any
candidate. It opens no product on its own: the build decision is the one written
at the end of this file.

## Reproduce

```bash
python3 EXPERIMENTS/072-npm-view-count-prototype/harvest.py     # arms A & B
python3 EXPERIMENTS/072-npm-view-count-prototype/outcome.py     # gate evaluation
```