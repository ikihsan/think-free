<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E119 — View-Count Prototype Framework

## Summary

Experimental prototype implementing the E116 view-count measurement methodology with matched harvest design, coverage floor classifier, and gated measurement (G1–G4). This prototype is designed as a reusable framework for testing the view-count principle on new domains per D083.

The three conditions for reopening (D083/F116) are addressed:

| Condition | Status |
|---|---|
| **Classifier with coverage floor** | Declared anchored word-boundary patterns; coverage ≥60% floor enforced before G2 |
| **Coverage gate** | Declared before run; G2 halts if coverage < floor, even if need fraction ≥ 5% |
| **Matched harvest as default design** | Need and random arms drawn from same pool, sorted by view_count descending |

## Gates (evaluated in order: G1 → G2 → G3 → G4)

| Gate | Threshold | Purpose |
|---|---|---|
| **G1** | ≥95% view_count > 0 | Validate the arrival instrument |
| **G2** | coverage ≥ 60% floor **AND** need fraction ≥ 5% | Ensure classifier covers enough population; halt if coverage insufficient |
| **G3** | Wilson CI95 upper bound < 60% unserved fraction | Measure unserved need among classified need-related items |
| **G4** | classified_total ≥ 30 | Ensure sufficient sample size |

## Declared Classifier Patterns (fixed before measurement, not tuned post-hoc)

### Need-related indicators (anchored word-boundary patterns):

```
\bhow\s+do\b, \bhow\s+can\b, \bhow\s+to\b, \bwhy\s+does\b, \bwhat\s+is\b,
\bfix\b, \bdebug\b, \brefactor\b, \boptimize\b, \bresolve\b,
\bhelp\b, \berror\b, \bnot working\b, \bcannot\b, \bissue\b
```

### Excluded (non-need) patterns (hard exclusion, case-insensitive):

```
\bIC\b, \bshow\s+off\b, \bmy\s+new\b, \bwelcome\s+to\b,
\bthank(s)?\b, \bimage(s)?\b, \bpicture(s)?\b, \bintroduction(s)?\b
```

**Coverage tracking:** After classification, `coverage = classified_total / total_rows`. The coverage gate requires `coverage ≥ 0.60` (60% floor). If coverage < 60%, the experiment halts and the classifier is revised before re-run.

## Matched Harvest Design

The core innovation: need and random arms are drawn from the **same pool** of N items, then split and sorted by `view_count` descending. This ensures any observed effect is not a sampling artifact.

**Algorithm:**
1. Fetch N items with view_count > 0 from the corpus
2. Classify each item as need-related or random using declared anchored patterns
3. Split into need arm and random arm from the same pool
4. Sort both arms by view_count descending
5. Compute unserved fractions and compare (matched design, primary)
6. Also compute asymmetric comparison (reported for transparency, not relied upon)

**Addresses E113 finding:** Asymmetric harvest (need arm and random arm drawn from different topics, both sorted by the outcome metric) produced artifact effect δ=0.826 that collapsed to δ=0.075 (p=0.183) under matched harvest.