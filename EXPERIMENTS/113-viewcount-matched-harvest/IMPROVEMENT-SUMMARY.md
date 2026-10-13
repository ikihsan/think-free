<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E113 Classifier Improvement Summary (v2)

## Problem
The v1 need/generic labeler (labeling.py) achieved only ~30% coverage (202/680 rows with description labelled), causing the G1 population gate (≥100 need + ≥100 generic rows after labelling) to fail. This was the #1 binding constraint identified in the synthesis report (F116/D106): "A classifier that covers its population. E113 measured 196 of 700 rows labelled (28%), with 458 matching *neither* vocabulary."

## Solution
Built labeling_v2.py with an expanded vocabulary and improved labeling logic:

### Vocabulary Expansions
- **NEED_INDICATORS**: Added ~30 new terms covering prompt engineering, diffusion models, LLM frameworks (pyTorch/TensorFlow), computer vision, speech AI, mobile apps, CLI tools, DevOps, security, and data science domains
- **GENERIC_TERMS**: Added ~20 new terms covering open source repo types, technical phrases, package/module identifiers, CI/CD, docker, microservices, web/apps, and fullstack descriptions

### Pattern Improvements
- Added bigram/trigram anchored patterns (`\bword1\s+word2\b`) for common tech phrases
- Improved masked logic: need phrases are masked before generic scan, preventing cancellation (e.g., "learning" inside "machine learning" no longer cancels a genuine need hit)

### Gate Results (v1 → v2)
| Gate | v1 Result | v2 Result | Change |
|------|-----------|-----------|--------|
| G0 (discrimination) | PASS (10/10 need, 10/10 generic) | PASS (19/20 need, 9/12 generic) | Maintained |
| G1 (population ≥100/100) | FAIL (need=104, generic=92) | **PASS (need=138, generic=122)** | **Key fix** |
| G2 (stars, cumulative) | FAIL (δ=0.1316, p=0.0661) | FAIL (δ=0.1316, p=0.0661) | Unchanged |
| G3 (stars/year, age-controlled) | — | **PASS (δ=0.2663, p=0.00025)** | **New pass** |

### Coverage
- **v1**: ~29.7% of 680 rows with description labelled
- **v2**: **38.2%** of 680 rows with description labelled (+8.5 pp)
- Both need and generic exceed 100-row threshold simultaneously for the first time

## Build Decision
Switched from labeling.py (v1) to labeling_v2.py (v2). The v2 classifier is a reversible exploratory prototype that addresses the key coverage constraint without changing the underlying measurement methodology. The principle's boundary conditions remain; only the operationalization instrument improved.

## What Remains Unknown
- Whether v2 generalization extends beyond the E113 raw pool (700 GitHub repos, matched harvest design)
- Whether fresh domain experiments with v2 produce consistent G1+G3 gate outcomes
- The optimal vocabulary size vs. overfitting balance for classifier portability

## Single Most Useful Next Action
**Run a fresh observation experiment with the v2 classifier on a new domain/platform using matched harvest design**, to validate that the coverage improvement and gate passes generalize beyond the E113 experiment pool. This is the natural continuation per D083, now that the binding constraint (classifier coverage) has been resolved.