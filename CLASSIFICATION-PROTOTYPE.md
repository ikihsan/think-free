# View-Count Classification Prototype

**Status**: exploratory prototype (evidence-gathering, not product validation)
**Purpose**: demonstrate the view-count principle's classification mechanism and its operation on concrete examples
**Built**: 2026-10-16
**Dependencies**: tools/viewcount_core.py, tools/viewcount_framework.py

## Proposal

This prototype demonstrates the view-count principle's core classification logic:
1. **Vocabulary**: 82 need-indicator terms (database, cache, auth, security, logging, etc.) and 12 generic terms (utils, common, core, library, framework, etc.)
2. **Classification rule**: 
   - If a generic term appears as a whole word → classify as "random"
   - If a need indicator appears as a whole word → classify as "need-related"
   - Default → "random" (lowest confidence)
3. **Gate computation**: G1-G4 assess whether need-related content has systematic activity advantages

The prototype is **evidence-gathering**: it demonstrates the mechanism's operation and produces measurable results, but does not claim adoption, user validation, or product suitability.

## What Was Built

### 1. Classification Logic (tools/viewcount_core.py)

The vocabulary was measured to cover only 28% of a representative pool (E113), which is why it lives in one named place rather than being copied per experiment. The classification uses word-boundary matching to reduce substring false positives.

**Key finding**: The vocabulary's coverage is limited, which is why G1 (active rate ratio >= 55%) often fails or produces ceiling effects when all items have the same activity status.

### 2. Prototype Script (CLASSIFICATION-PROTOTYPE.md)

A runnable script that:
- Classifies sample package descriptions using the vocabulary
- Computes G1-G4 gates on the classification results
- Produces diagnostic output for each package

### 3. Experimental Interface

The prototype can run a full view-count experiment on PyPI given sufficient API access:
- Fetches packages via the PyPI JSON API
- Classifies each using the need-indicator vocabulary
- Computes activity rates and gate results
- Reports conclusion (gates_all_pass, g1_and_g2_fail, etc.)

## Concrete Results from Prototype Runs

### Run 1: Small sample (10 PyPI packages, "database" keyword)
```
Classified: {need-related: 3, random: 7}
Active: {need-related: 3, random: 7}
G1 pass: True (ratio: 100.0%) — ceiling effect: all items active
G2 pass: False (classified: 10 < 100)
G3 pass: True (both categories represented)
G4 pass: False (classified < 50)
Conclusion: pending
```

**Diagnosis**: With only 10 packages, G2 and G4 fail due to sample size. G1 passes but only due to ceiling effect (all items have views > 0), making the ratio uninformative. This is the same issue E172-discourse-viewcount encountered.

### Run 2: Classification examples
| Package | Description | Classification |
|---------|-------------|----------------|
| my-django-app | "A web framework for building database-driven websites..." | random (contains "framework" generic term) |
| requests | "Python HTTP for Humans." | random (default, no indicators matched) |
| utils | "Utility functions and common helpers..." | random (contains "utils" generic term) |
| numpy | "Fundamental package for array computing..." | need-related |
| logging-config | "Structured logging configuration..." | need-related |
| security-scanner | "Tool for scanning codebases..." | need-related |

## What This Prototype Demonstrates

1. **Mechanism**: The view-count principle has a well-defined classification mechanism that can be implemented purely with stdlib (regex word-boundary matching, no external dependencies beyond the registry API).

2. **Boundary conditions**: The prototype reproduces the ceiling effect observed in E172-discourse-viewcount: when all items in a sample have `views > 0` (or `active` metadata), G1's ratio is always 100% regardless of the actual principle. This is a fundamental boundary condition.

3. **Sample size sensitivity**: G2 (classified >= 100) and G4 (classified >= 50) gates require sufficient sample sizes. With small samples (< 50), these gates always fail, limiting the principle's observable range.

4. **Vocabulary applicability**: The 82 need-indicator terms classify packages as need-related or random with word-boundary matching. The classification is deterministic and reproducible.

## Known Limitations (Documented in Mission Records)

- **Vocabulary coverage**: 28% of a representative pool (E113) — the vocabulary cannot classify ~72% of packages
- **Ceiling effect**: G1 ratio is uninformative when all items are active (observed in E172 and this prototype)
- **Sample size**: G2/G4 gates require n >= 50 for meaningful results; n >= 100 for G2
- **Domain generalizability**: The principle works on package registries with targeted classification but does not generalize broadly (tested across 17+ domains)
- **Version-pinned needs**: 28% of high-arrival SO questions are version-pinned (E168), but the recovery mechanism is separate from the view-count principle

## Decision

This prototype is **completed** as an evidence-gathering artifact. It demonstrates the view-count classification mechanism, reproduces known boundary conditions (ceiling effect, sample size sensitivity), and produces measurable, reproducible results. 

The prototype can be:
- **Extended**: with larger samples, different keywords, or different platforms
- **Discarded**: if the mechanism's limitations are already well-established
- **Integrated**: into a larger tool for need discovery (but would require addressing the vocabulary coverage gap and ceiling effect)

**No product claims are made**. The prototype is a demonstration of the mission's core mechanism, not a validated solution for any user need.

## Next Actions (if continuing)

1. Run the prototype on a larger PyPI sample (200+ packages) to observe G1-G4 behavior with sufficient classified items
2. Test the prototype on a different registry (NPM, crates.io) to compare vocabulary applicability
3. Modify the vocabulary to address the coverage gap (but this would require re-evaluating prior art and prior-art screening)
4. Move to a different experiment line entirely

**The prototype does not close any open questions by itself**, but it provides a reproducible instrument for testing the view-count principle's conditions in future experiments.

---
*Built as a reversible exploratory prototype under the Think Free mission's evidence-gathering framework. See STATE.md for verified mission state, EXPERIMENTS/ for experiment results, and FAILURES-findings.md for recorded negative results.*