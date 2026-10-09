# E078 — Need-Classification Prototype

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

Prototype experiment testing whether the need-classification and served-fraction
measurement framework from E077 generalizes to a new online community dataset.

## Objective

Estimate the fraction of need statements in online technical forums that are
"unserved-open-like" (no tool recommendation in replies) and test whether the
three-clause rubric and classification rules generalize across datasets.

## Protocol

### Input dataset

A JSONL file where each line is a thread with at minimum:
- `title` (str): the thread title
- `answer_count` (int): number of replies
- `accepted_answer` (bool): whether an answer is accepted
- `answers` (list): list of answer dicts with at least `score` (int) and
  optionally `content` or `body` (str)

### Classification rules (pre-declared)

**Need patterns** (title suggests a concrete problem/question):
15 regex patterns covering how/what/why questions, help requests, recommendations,
which/where/any questions, stuck/confused/lost, trying to, wondering, should I.

**Non-need patterns** (title suggests sharing, showing off, meta):
10 regex patterns covering IC, show off, my new setup, look at this, just got, what
you getting, welcome, thank you, images, pictures, introductions.

**Unserved-open-like rubric** (three clauses, all must be true):
1. **No platform-recorded resolution**: No accepted answer AND (answer_count < 3 OR
   no answer with score >= 1)
2. **States a concrete need**: Title matches at least one need pattern AND no
   non-need pattern
3. **Not a request for content/service/price/access/human work**: Already filtered
   by non-need patterns

### Gates

| Gate | Criterion | Pass condition |
|---|---|---|
| G1 | Classification validity | Single-rater with well-defined rules (satisfied by design) |
| G2 | Need prevalence | ≥5% of threads classified as need topics |
| G3 | Served fraction measurable | Wilson CI95 upper bound < 70% |
| G4 | Cross-platform signal | ≥2 of 3 sampled threads have replies naming a tool/artifact |

### Falsification

The experiment fails if:
- G2: need prevalence < 5%
- G3: Wilson upper bound ≥ 70%
- G4: 0 of 3 threads have replies naming a tool/artifact

### Deliverables

- `raw/threads_<dataset>.jsonl` — raw thread data
- `results.json` — aggregated results with gates assessment
- `README.md` — experiment summary and served-fraction estimate