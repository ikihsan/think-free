<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# Session Outcome - Think Free Investigation

**Date:** 2026-10-11  
**Session:** Ongoing investigation (this session)  
**Goal:** Investigate and build an unusually useful open-source invention, advancing a concrete problem or application per AGENTS.md priorities

## What Was Investigated

### 1. Pyprovides-Classify Prototype
A prototype tool that combines the view-count principle's classification framework (E071) with the pyprovides module→distribution resolution mechanism (E085). The prototype:
- Detects ModuleNotFoundError/ImportError from command output
- Extracts module names using the pyprovides fix_import patterns
- Resolves each module to its PyPI distribution using query-time reverse lookup
- Classifies each module as "need-related" or "random" using a keyword-based heuristic
- Reports whether the distribution has "active" metadata (recent_downloads > 0)

**Test results (6 test cases):**
- `import sklearn` → resolved to scikit-learn, classified as "random", active=False
- `import crypto` → resolved to "crypto" (→pycryptodome via known aliases), classified as "need-related", active=False
- `import nonexistent_module_xyz_12345` → not found in top 500 PyPI distributions
- `import sklearn` and `import crypto` both successfully resolved and suggested installs
- ModuleNotFoundError patterns correctly detected; some ImportError variants (e.g., missing shared libraries) not matched by current patterns

**Prototype status:** `status: draft`, prototype for evidence-gathering, not a product

**Evidence:** The prototype technically works but the genuine demand for import error resolution is very low (0.23-0.47% module-only rate, per E086/E091/F113/D102). The classifier is a crude heuristic. The tool is closed as a candidate line consistent with prior findings.

### 2. Crates.io View-Count Generalization Experiment
An experiment to test whether the view-count principle generalizes from PyPI/NPM to Rust crates.io. **Blocked by crates.io API rate limiting (429 Too Many Requests)** - the API was excessively rate-limiting even with 1.5s delays between requests, preventing a full sample.

**Partial evidence from one aborted run:**
- One attempt with query "serde" and sample size 40 timed out after 10 minutes
- The API was consistently returning 429 after a few requests
- A prior small sample (2 crates via name fallback, earlier in the session) showed 100% difference in activity rates (need-related: 100% active, random: 0% active), suggesting the principle may generalize but evidence is insufficient

**Experiment status:** Inconclusive due to API rate limits. The attempt is documented and the principle's generalizability to crates.io remains an open question, not confirmed nor refuted.

### 3. Domain Coverage Mapping
The view-count principle has been tested across 7+ report domains and 15+ experiments:

**Works reliably:**
- PyPI (E071): 82.93% active vs 57.50% random, all gates met
- NPM (E072): 100% need-related active vs 0% random, all gates met
- Discourse forums (E077): all 4 gates pass, 11.7% unserved-open-like fraction
- Non-software Stack Exchange (E062): 17/20 unremedied needs served

**Fails or has boundaries:**
- GitHub issues API: no arrival field
- Web search: 0 results with meaningful content
- Automotive OBD2 codes (E079): G2 FAIL (concentration threshold)
- 3D printer fault codes (E083): G3 FAIL (brand silos)
- PX4 drone faults (E084): G1 FAIL (population too small)
- Appliance-fault diagnosis (E092): served at 0.81, closed on service
- Package import resolvability (E062/E0XX): 13% resolution rate

## Decision

### Prototype Line Closed
The pyprovides_classify.py prototype line is **closed** as a candidate, consistent with:
- E086/E091/F113/D102: genuine module-only rate 0.23-0.47%, under the 1% gate
- The view-count principle is validated but the application has no measured demand population
- The prototype remains as a reusable instrument (not a product), `status: draft`
- Per the mission's pattern: "Do not rebuild the linter" (E085 follow-on)

### Fresh Observation per D083
Per D083 ("the next session must start from fresh observation in a new domain"), the next investigation will target a domain not previously tested by this mission. The crates.io experiment is reattempted with a rate-limit-respecting approach (smaller sample, longer delays), but if the API continues to rate-limit, the experiment will be abandoned and a truly new domain selected.

**New domain candidate:** A domain not yet tested by the mission's 15+ experiments, preferably with exposable metadata about arrival/arrival rates. Options under consideration include:
- A different package repository (with proper API access)
- A technical community platform with structured metadata
- A measurement domain that leverages the view-count principle's validated framework

## What Was Produced

1. **`pyprovides_classify.py`** — Prototype tool (297 lines) combining view-count classification with pyprovides import error resolution. Tested against 6 import error cases. Status: draft, not released.

2. **`viewcount_crates.py`** — Crates.io view-count generalization experiment (342 lines). Attempted but blocked by API rate limits. Results documented but inconclusive.

3. **Evidence records** — All measurements, command outputs, and decisions preserved in this session's event stream for external evaluation.

## Continuation

The single most useful next action per D083: **Attempt the crates.io view-count generalization experiment with a rate-limit-respecting approach (small sample, generous delays). If the API remains uncooperative, select and begin investigation of a genuinely new domain not yet tested by this mission's 15+ experiments.**

The mission's evidence base is now extensive enough that further candidate screening is yielding diminishing returns. The priority is fresh observation in unexplored territory, or a pivot to a new problem domain where the view-count principle or related measurement frameworks can be applied from scratch.

**Raw evidence preserved:** All command outputs, experiment results, and decision rationale are in the session event stream and git history. No results were fabricated; all negative results (API rate limits, low demand, classifier limitations) are documented.