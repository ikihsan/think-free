<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E101 — View-count principle on Hugging Face Hub (ML model registry)

Session `2026-10-11-009`, VM `instance-20260717-0944`, declared 2026-10-11.

## The question

Does the view-count principle — that "need-related" items on a platform with exposable arrival metadata show systematically higher activity than random items — generalize to **Hugging Face Hub**, an ML model/dataset/space registry with download counts?

This is a fresh observation in a **new platform type** (ML model registry) not previously tested by this mission. Prior tests cover: code package repositories (PyPI, NPM, Maven), Q&A forums (Stack Exchange, Discourse), and fault-code forums (multiple Discourse instances). Hugging Face Hub is a distinct platform type: a registry for ML models, datasets, and Spaces (demos), with public download counts and task categorization.

## The candidate decision this changes

This experiment is evidence-gathering per D083. It does not directly produce a candidate. If the view-count principle generalizes to a third platform type (ML model registry), it strengthens the instrument's validity and opens the door to future candidate generation in ML practitioner tooling. If it fails, it establishes a boundary for the principle.

**If the principle generalizes** (need-related models have significantly higher download activity), the instrument's platform invariance is extended to ML model registries, and a practitioner-facing tool for model discovery could be a candidate.

**If the principle does not generalize** (no significant difference, or reverse), the instrument is limited to code package repositories and Q&A forums, and ML model registries have different dynamics.

## Population and arms

| arm | source | classification | what it carries |
|---|---|---|---|
| **1 (need-related)** | Hugging Face Hub models for **common ML tasks**: `text-classification`, `token-classification`, `question-answering`, `text-generation`, `fill-mask`, `summarization`, `translation`, `feature-extraction`, `image-classification`, `object-detection`, `image-segmentation`, `automatic-speech-recognition`, `text-to-speech` | `pipeline_tag` matches one of the 13 common tasks above | modelId, downloads (lastMonth), likes, tags, pipeline_tag, createdAt |
| **2 (random)** | Hugging Face Hub models **without** a common-task pipeline_tag, or with pipeline_tag `null`/rare tasks | `pipeline_tag` not in the 13 common tasks, or absent | modelId, downloads (lastMonth), likes, tags, pipeline_tag, createdAt |

**Why these populations.** The 13 pipeline_tags cover the overwhelming majority of practitioner ML needs (classification, generation, extraction, detection, speech). Models for these tasks are what practitioners search for when they have a "need". Models without these tags are either experimental, research-only, or serve niche needs not representative of common practitioner demand.

## Gates, all declared before any row is fetched

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 models retrieved per arm (need-related and random) | the platform API does not yield sufficient sample at this cost. Stop; record the ceiling. |
| **G2 activity difference** | need-related arm has higher "active" rate than random arm, with Welch's t-test p < 0.05 on `downloads_lastMonth > 100` | the view-count principle does not generalize to this platform type. Stop; record the boundary. |
| **G3 need-related activity floor** | Wilson CI95 lower bound of need-related active rate > 0.60 (active = `downloads_lastMonth > 100`) | the signal is too weak for practical use even if G2 passes. Stop; record the measurement. |

**Denominators.** Every fraction is over models retrieved. Models not retrieved (API errors, pagination limits) are reported as not retrieved. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Activity definition

A model is **"active"** if `downloads_lastMonth > 100`. This threshold is chosen because:
- E071 (PyPI) used "significant activity metadata" as a binary; here we use a concrete download threshold
- 100 downloads/month indicates non-trivial practitioner adoption
- The threshold is declared before measurement and not tuned to results

## Ceiling, stated now

One API (Hugging Face Hub public REST), two arms defined by `pipeline_tag`, 13 common tasks vs rest. This measures the view-count principle's generalization to ML model registries. It does not measure demand for a specific tool, does not measure adoption, and does not close any candidate. The experiment is stdlib-only, uses synthetic fixtures for unit tests, and has predeclared kill gates per E065/D083.

## Reproduce

```bash
python3 harvest.py     # fetch both arms from Hugging Face Hub API
python3 outcome.py     # evaluate gates and report results
```

Needs internet access for Hugging Face Hub API, Python 3.8+ with stdlib only (`urllib`, `json`, `statistics`, `math`).

## Synthetic fixtures

`fixtures/` contains:
- `need-related-sample.json` — 5 mock model records with common pipeline_tags and high downloads
- `random-sample.json` — 5 mock model records without common pipeline_tags and low downloads
- Unit tests use these to verify gate logic without network access.