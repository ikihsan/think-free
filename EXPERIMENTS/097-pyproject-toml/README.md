# E097 — View-count principle on GitHub pyproject.toml presence

**Status:** Experiment in progress.

**Date:** 2026-10-11

**Question:** Can the view-count principle generalize to a measurement of Python package metadata format adoption? Specifically: what fraction of Python packages on GitHub have a `pyproject.toml` file (indicating use of PEP 517/518 modern build system), and does the presence of `pyproject.toml` correlate with "need-related" package characteristics?

**Expected outcome:**
- If G1 passes: need-related Python packages adopt `pyproject.toml` at a rate at least 10pp above random, supporting the view-count principle's generalizability to code repository metadata.
- If G1 fails: need-related Python packages do not systematically adopt `pyproject.toml` at a higher rate than random, and the principle does not generalize to this correlation.

**Next steps:** Run `python3 run.py --gate` to execute the experiment and check gate results.