<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E092 — View-count principle on Maven Central Java packages

**Status:** Experiment in progress.

**Date:** 2026-10-11

**Question:** Can the view-count principle generalize to a third package repository ecosystem (Java/Maven Central), beyond PyPI and NPM? Specifically: are "need-related" Java packages systematically more "active" (have significant metadata indicating adoption/usage) than random packages?

**Expected outcome:** 
- If G1 passes: the view-count principle generalizes across package repository ecosystems, supporting its broader applicability.
- If G1 fails: the view-count principle does not generalize to Maven Central, suggesting ecosystem-specific factors affect the active/metadata relationship.

**Next steps:** Run `python3 -m unittest discover -s EXPERIMENTS/092-viewcount-maven` or `python3 run.py --gate` to execute the experiment and check gate results.