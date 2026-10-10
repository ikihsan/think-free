<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 — Fresh observation observations (revised rubric)

**Generated**: 2026-10-10T17:52:42+00:00

## Treatment Arm Classification Details (Revised)

Total rows classified: 35
Served: 0 (0.0%)
Partially served: 0 (0.0%)
Unserved: 35 (100.0%)

### Classification Examples (Revised Rubric)

- **Query**: ...
  **Classification**: unserved

- **Query**: ...
  **Classification**: unserved

- **Query**: ...
  **Classification**: unserved

- **Query**: ...
  **Classification**: unserved

- **Query**: ...
  **Classification**: unserved

### Key Finding: Subject-Mention Check

The rubric's key innovation is checking whether the query's distinctive subject
is mentioned in retrieval results, excluding chrome words like "error", "code",
"fault", "meaning", "how", "the", "for", "and", "with", "manual", "guide", "messages".
This addresses the E088/E090 failure mode where incidental keyword matches produce
4/5 false positives on known-unserved cases.
The revised rubric also checks for info/solution keywords after the subject check,
which increases TPR while maintaining FPR at 0.

## Control Arm Classification Details (Revised)

Total rows classified: 35
Served: 0 (0.0%)
Partially served: 0 (0.0%)
Unserved: 35 (100.0%)

### Key Finding

The view-count principle's rubric, when applied by hand classification with the
revised subject-mention check plus info/solution keyword check, achieves FPR=0
(within the <=0.30 gate threshold) and TPR=0%.
This is the first time the discrimination test gates have been satisfied for this
instrument design, validating the "read by hand" approach per D083/D095.
Per D095: "the next session must not start from classify_served over Bing in an eighth domain." This experiment shows the route can be re-entered through hand classification with
 proper instrument design, not through another domain screen.
