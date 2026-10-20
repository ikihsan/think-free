<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E146 — View-Count Principle on crates.io

**Result: GATE_CLOSED — classifier vocabulary mismatch**

## Experiment ran 2026-10-15

The view-count principle was tested on crates.io, the Rust package registry, but
the experiment failed at G4 (arrival field) because 0 out of 100 crates fetched
from the default listing were classified as `need-related`. All 100 crates were
classified as `random`.

### What was tested

- 100 crates were fetched from crates.io API default listing (`/crates?per_page=100`)
- Each crate was classified as `need-related` or `random` based on its name and
  description containing need indicator or generic term keywords
- Active status was defined as `downloads > 0`
- Need-related crates were expected to have systematically higher download counts

### What happened

The default crates.io listing returned crates with very generic names and descriptions
(e.g., "A-Mazed: App to generate mazes in terminal", "A2VConverter: AudioVideoConverter
is a Rust library..."). The need indicator keywords (originally web/API/framework
focused) and even a broadly expanded set did not match any crate names or descriptions
in the default sampling. All 100 crates were classified as `random`.

This is a **classifier vocabulary mismatch**: the view-count principle's classification
scheme, developed for package registries where packages tend to have web/API/framework
terminology in their names/descriptions (PyPI, NPM, NuGet, Hex.pm), does not map
cleanly to crates.io's crate ecosystem, which is more system-level, driver-oriented,
and tool-focused with different naming conventions.

### Gate results

| Gate | Status | Notes |
|------|--------|-------|
| G1 | PASS | 100 crates fetched (≥50 required) |
| G2 | N/A | Cannot evaluate; 0 need-related crates classified |
| G3 | N/A | Cannot evaluate; 0 need-related crates classified |
| G4 | FAIL | Both categories not represented (0 need-related, 100 random) |

### Evidence recorded

- `EXPERIMENTS/146-viewcount-crates/collect.py` — Data collection script
- `EXPERIMENTS/146-viewcount-crates/results.json` — Experiment results (G4 fail)
- The classifier vocabulary mismatch is itself a valid finding: the view-count
  principle's need classification is domain-specific and may not transfer across
  package ecosystems with different naming conventions

### Decision

The view-count principle could not be assessed on crates.io because the default
crate sample's vocabulary does not align with the need indicator/generic term
classification scheme developed for other package registries. This documents an
important boundary condition: the principle's classification scheme is not
universally applicable across different package registries.

Future work on crates.io would need to adapt the need classification scheme to
Rust crate naming conventions, or use a different sampling strategy (e.g.,
keyword-search-based selection) to obtain a mixed need-related/random sample.