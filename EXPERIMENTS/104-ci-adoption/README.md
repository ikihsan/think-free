# E104 — CI/CD adoption on PyPI

**Status:** Experiment in progress.

**Date:** 2026-10-11

**Question:** Can the rate of Python packages with CI/CD configuration be measured on PyPI, and do "need-related" packages have a higher CI/CD adoption rate than "random" packages?

**Expected outcome:**
- If G1 passes: need-related Python packages adopt CI/CD at a rate at least 10pp above random, supporting the generalizability of CI/CD metrics to need-related packages.
- If G1 fails: need-related Python packages do not systematically adopt CI/CD at a higher rate than random, and this measurement does not generalize to CI/CD patterns.

**Next steps:** Run `python3 run.py --gate` to execute the experiment and check gate results.