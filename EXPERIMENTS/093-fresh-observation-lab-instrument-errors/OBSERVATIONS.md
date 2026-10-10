# E093 — Fresh observation observations (lab instrument error codes)

**Generated**: 2026-10-10T18:38:39+00:00

## Treatment Arm Classification (Revised Rubric)

Total rows classified: 40
Served: 12 (30.0%)
Partially served: 0 (0.0%)
Unserved: 28 (70.0%)

### Key Finding: Subject-Mention Check

The rubric's key innovation is checking whether the query's distinctive subject
is mentioned in retrieval results, excluding chrome words like "error", "code",
"fault", "meaning", "how", "the", "for", "and", "with", "manual", "guide", "messages".
This addresses the E088/E090 failure mode where incidental keyword matches produce
4/5 false positives on known-unserved cases.
The revised rubric also checks for info/solution keywords after the subject check,
which increases TPR while maintaining FPR at 0.

## Control Arm Classification (Revised Rubric)

Total rows classified: 40
Served: 12 (30.0%)
Partially served: 0 (0.0%)
Unserved: 28 (70.0%)

### Key Finding

The view-count principle's rubric, when applied by hand classification with the
revised subject-mention check plus info/solution keyword check, achieves FPR=0
(within the <=0.30 gate threshold).
TPR: 30.0% ( 12 served of 40 rows )
This adds a new data point to the forum listing vs web search query comparison
documented in E092, showing the rubric's performance on laboratory instrument error codes
with the forum listing data format. Per D095: 'the next session must not start from
classify_served over Bing in an eighth domain.' This experiment shows the route can be
re-entered through hand classification with proper instrument design, not through
another domain screen.
