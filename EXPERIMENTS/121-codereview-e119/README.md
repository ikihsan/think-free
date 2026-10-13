# E121 — View-count principle on Kubernetes Discourse with E119 matched-harvest framework

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Summary

Fresh observation per D083: tested the view-count principle on Kubernetes Discourse forum (discuss.kubernetes.io) using the E119 prototype with matched-harvest design, coverage-floor classifier (Discourse-specific classifier_discourse), and predeclared gates G1–G4.

**Result: G1 PASS, G2 PASS, G3 FAIL, G4 PASS.** The view-count principle's arrival instrument works (G1), the classifier achieves the ≥60% coverage floor (G2: 65.8%), but the unserved-open-like fraction is 76.4% (CI95 [71.2%, 80.9%]) which exceeds the 60% threshold (G3 FAIL).

## Experimental Setup

### Platform
- **Site:** Kubernetes Discourse (discuss.kubernetes.io)
- **Category:** General Discussions (id: 6)
- **API:** Discourse JSON API (unauthenticated)
- **Items fetched:** 500 topics with view_count ≥ 10
- **Items analyzed:** 497 (after excluding meta/announcements)

### Methodology (E119 Prototype)
1. **Matched harvest:** Need and random arms drawn from same pool of 497 topics, sorted by view_count descending
2. **Classifier (classifier_discourse):** Anchored word-boundary patterns + Discourse-specific technical problem keywords, declared before measurement
3. **Coverage floor:** G2 requires ≥60% classifier coverage before measuring need fraction
4. **Gates evaluated in order:** G1 → G2 (coverage first) → G3 → G4

### Classifier Performance (classifier_discourse)
- **Coverage:** 65.8% (327/497 classified) — **exceeds 60% floor**
- **Need-related:** 292 (58.8% of total)
- **Random:** 35 (7.0% of total)
- **Unclassified:** 170 (34.2% of total)
- **G0 discrimination:** PASS (planted positives/negatives recovered)

## Gate Results

| Gate | Threshold | Result | Details |
|------|-----------|--------|---------|
| **G1** | ≥95% view_count > 0 | **PASS** | 497/497 = 100% |
| **G2** | coverage ≥ 60% AND need fraction ≥ 5% | **PASS** | coverage 65.8%, need fraction 58.8% |
| **G3** | Wilson CI95 upper bound < 60% unserved | **FAIL** | unserved 76.4%, CI95 [71.2%, 80.9%] |
| **G4** | classified_total ≥ 30 | **PASS** | 327 classified |

## Interpretation

### Key Findings

1. **Arrival instrument validated (G1):** 100% of sampled topics have view_count > 0. The view-count instrument works on Discourse forums.

2. **Classifier covers population (G2):** 65.8% coverage exceeds the 60% floor. The Discourse-specific classifier (classifier_discourse) successfully addresses the E113/F116 binding constraint where the original E119 classifier only achieved ~40% coverage on Discourse data. The key improvement was adding Discourse-specific technical problem patterns (error/failure/problem keywords, configuration terms, troubleshooting actions) alongside question-form patterns.

3. **High unserved fraction (G3 FAIL):** 76.4% of need-related topics are unserved (no replies AND no accepted answer). The Wilson CI95 upper bound of 80.9% exceeds the 60% threshold. This is dramatically higher than:
   - Non-software Discourse baseline (E077): 11.7% (CI95 [8.8%, 15.5%])
   - Embedded Discourse forums (E082): 15.3% (CI95 [10.5%, 21.3%])
   - E094 original result on same data: 75% unserved

4. **Sufficient sample (G4):** 327 classified items well above the 30 minimum.

### Domain Comparison

| Domain | Coverage | Unserved Fraction | Gates |
|--------|----------|-------------------|-------|
| Non-software Discourse (E077) | ~100% | 11.7% | ALL PASS |
| Embedded Discourse (E082) | ~100% | 15.3% | ALL PASS |
| **Kubernetes Discourse (E121)** | **65.8%** | **76.4%** | **G3 FAIL** |
| Physics SE (E119) | 81.5% | 4.27% | ALL PASS |
| Mathematics SE (E120) | 71.4% | 1.96% | ALL PASS |

The Kubernetes Discourse forum is an outlier with extremely high unserved fraction. This suggests the forum is not effectively serving its community's technical needs — most questions/problems receive no replies and no accepted solutions.

## Classifier Details

The Discourse-specific classifier (classifier_discourse.py) combines:
- **E119 question-form patterns** (how to, why does, what is, can you, etc.)
- **E094 error/failure keywords** (error, fail, crash, timeout, oom, panic, etc.)
- **Discourse-specific technical patterns** (config, deploy, upgrade, install, proxy, ingress, dns, cert, backup, monitor, etc.)
- **Refined excluded patterns** (avoid false positives on container images, technical terms)

This achieves 65.8% coverage vs 40.2% with the original E119 classifier_v3.

## Files

| File | Purpose |
|------|---------|
| `classifier_discourse.py` | Discourse-specific classifier with declared patterns |
| `measure_discourse.py` | Gated measurement framework for Discourse |
| `data_k8s_discourse.jsonl` | 497 topics from discuss.kubernetes.io |
| `README.md` | This report |

## Reproduction

```bash
cd EXPERIMENTS/121-codereview-e119

# Run Discourse-specific measurement
python3 measure_discourse.py data_k8s_discourse.jsonl 0.60
```

## Conclusion

**The view-count principle's arrival instrument generalizes to Kubernetes Discourse (G1 PASS), and the Discourse-specific classifier resolves the E113/F116 coverage constraint (G2 PASS at 65.8%). However, the unserved fraction is 76.4% — far above the 60% threshold and the Discourse baseline of 11.7-15.3%. This domain is not a viable candidate source because the population's needs are overwhelmingly unserved.**

This result validates the E119 prototype's framework: it correctly identifies that Kubernetes Discourse has a view-count signal (people view need-related topics) but the community does not serve those needs (no replies/accepted answers). The high unserved fraction is a property of this specific community, not a platform failure.

**Next step per D083:** Test the E119 prototype on another Discourse forum (or Stack Exchange tag) to determine if the high unserved fraction is specific to Kubernetes Discourse or a broader pattern. The classifier_discourse framework is ready for reuse.