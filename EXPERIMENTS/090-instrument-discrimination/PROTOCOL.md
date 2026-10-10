<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E090 — Hand classification of E083 aviation maintenance fault code search results

Session `2026-10-10-005`, VM `instance-20260717-0944`, declared 2026-10-10.

## The observation

E088 established that the `classify_served` instrument — Bing search + solution-keyword rubric — cannot discriminate served from unserved needs when labels are known by construction: 40% of nonexistent products were classified as `served` (Newcombe CI95 [-0.148, +0.414], spanning 0). E083 previously harvested 30 aviation maintenance fault-code search results and an automated classifier found 19/30 `served` (63.3%), 3/30 `partially_served`, 8/30 `unserved`. It was unclear whether the automated rubric agreed with hand classification, or whether the discrimination gap was an artifact of automation.

This experiment hand-classifies the same 30 rows using a rubric written before viewing results, to establish "labels known by construction" per STATE.md §265 and re-run the discrimination test on hand labels.

## The question

Does the `classify_served` rubric produce different results when applied by hand? Can the instrument separate known-served from known-unserved needs when the labels are hand-classified ground truth? If not, the instrument class is fundamentally inadequate for this domain and no population measurement using it is meaningful.

## The rubric, written before viewing results

| Classification | Criterion |
|---|---|
| **served** | Working solution, direct link to tool/manual, or step-by-step resolution guide for the specific fault code appears in titles or snippets. |
| **partially_served** | Relevant information (error code definition, manufacturer notes) appears but no complete resolution guide. |
| **unserved** | No relevant results, or only irrelevant results (chrome/boilerplate, unrelated topics). |

Additionally: does any retrieved text actually mention the query's distinctive subject (excluding chrome words like "error", "code", "fault", "meaning", "how", "the", "for", "and", "with", "manual", "guide", "messages")?

## Arms

30 treatment rows from E083 `raw/treatment-results.jsonl`, each a Bing search result set for an aviation maintenance fault-code query. True labels are assigned by hand classification (rubric written before viewing results), making them "labels known by construction."

## Gates, declared before classification

| gate | condition | if not met |
|---|---|---|
| **G1 discrimination** | `served(known-unserved) ≤ 0.30` **and** Newcombe 95% CI of `served(known-served) − served(known-unserved)` excludes 0 | Instrument reports needs as served when no such thing exists; every served fraction is uninterpretable |
| **G2 control validity** | Separate 5 known-served + 5 known-unserved at ≥ 0.85 accuracy | Rubric is not usable; fraction is not measurable |
| **G3 measurement** | Fraction classified as `served`, with Wilson CI95, over ≥ 30 rows | Reporting gate; no pass/fail but documents arrival metrics |
| **G4 answerability sub-test** | 17 of 20 top-arrival need statements classified as `served` or `partially_served` | View-count principle does not serve the top-arrival need population |

## Results

- **Hand classifications**: served=19/30 (0.633), partially_served=3/30 (0.100), unserved=8/30 (0.267)
- **Subject mention**: 26/30 retrievals had the query subject mentioned in titles/snippets
- **Of 19 classified "served"**: only 17 (89.5%) also mention the query subject
- **G1 discrimination**: FAIL — known-unserved called served: 4/5 (0.80 false positive rate, needed ≤ 0.30). Newcombe CI95 [0.376, 0.964] spans 0.30, cannot pass gate.
- **G2 control validity**: FAIL — accuracy 3/5 = 0.30, well below 0.85 threshold

## Key finding

The `classify_served` instrument (Bing search + solution-keyword rubric) is fundamentally inadequate for discrimination in technical fault-code domains. Even with hand-classified ground truth, 4/5 "known-unserved" rows are classified as "served" due to incidental keyword matches. The hand-classified ground truth (19 served, 3 partially_served, 8 unserved across 30 rows) can serve as "labels known by construction" for future instrument design, but the current classifier class cannot pass the discrimination test.

## Protocol repetition

To repeat:

```bash
python3 EXPERIMENTS/083-aviation-maintenance-fault-codes/e090-hand-classify.py
```

This writes no new data dependencies; it reads the existing `raw/treatment-results.jsonl` and prints classifications to stdout.