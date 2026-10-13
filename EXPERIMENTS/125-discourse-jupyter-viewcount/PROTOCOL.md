# E125 — Fresh observation: discourse.jupyter.org (Jupyter Support Forum)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Summary

Fresh observation in a new domain per D083: **discourse.jupyter.org** — the Jupyter project's Discourse forum for help, notebook, JupyterHub, Binder, and community discussion.

**G1 PASS, G2 FAIL** — Classifier coverage 50.4% (< 60% floor). Domain CLOSED per kill gate.

## Results

| Metric | Value | Gate |
|---|---|---|
| Total topics | 500 | — |
| View_count > 0 | 100% | G1 PASS |
| Classifier coverage | 50.4% | **G2 FAIL** (< 60%) |
| Need-related (classified) | 167 (33.4%) | — |
| Random (classified) | 85 (17.0%) | — |
| Unclassified | 248 (49.6%) | — |
| Unserved fraction (classified only) | 43.1% (72/167) | — |
| Wilson CI95 | [35.8%, 50.7%] | — |

## Coverage Gap Analysis

The improved classifier (classifier_gnome from E124) achieves 50.4% coverage — better than GNOME (37.2%) but still below the 60% floor.

**Unclassified genuine questions** (sample):
- "Trouble reverse proxying to JupyterHub on a subpath"
- "GLIBCXX_3.4.26 not found from RStudio"
- "Local wheel file in requirements.txt"
- "Folder Permissions"
- "'LooseVersion' object has no attribute 'version'"
- "Binder from github & dockerfile not starting Rstudio?"
- "Jupyterhub Persistant Volume resets on every pod restart"
- "Something up with mybinder.org cache"
- "BinderHub HTTPS?"
- "Official Mastodon account(s)?"

**Missing pattern categories**:
1. Error messages as titles (CamelCase identifiers, "not found", "no attribute")
2. "Trouble [verbing]..." / "Problem with..." / "Issue with..."
3. "X not working" / "X failing" / "X broken" / "X isn't working"
4. "Something up with X"
5. Noun phrase questions ending with "?"

## Contamination Issue

The 43.1% unserved fraction among classified topics is inflated by:
- **Job postings** (community category): 10+ hiring posts misclassified as need-related
- **Announcements**: "IPython security update", "Mybinder.org reducing capacity", "[ANN] RISE 5.7.1"
- **Meta questions**: "How to use the community forum", "About the Meta category"

The classifier's excluded patterns don't catch all job/announcement content.

## Comparison with Prior Discourse Results

| Forum | Type | Coverage | Unserved (classified) | Notes |
|---|---|---|---|---|
| E077 (non-software) | Support | ~80% | 11.7% | Baseline |
| E082 (embedded) | Support | ~80% | 15.3% | Baseline |
| **E123 (meta.discourse)** | Support | **87.6%** | **27.3%** | Blog contamination → 25.1% genuine |
| **E124 (GNOME)** | Developer | **37.2%** | — | **G2 FAIL** |
| **E125 (Jupyter)** | Mixed | **50.4%** | **43.1%** | **G2 FAIL** |

**Pattern**: Q&A-style **support forums** achieve ≥60% coverage. **Developer/design/mixed forums** fail the coverage floor due to diverse question styles.

## Conclusion

The view-count principle measurement framework with keyword-based classification has a **domain-dependent coverage boundary**:
- Works on product support forums (users follow standard question formats)
- Fails on developer/design forums (diverse, abbreviated, error-message question styles)

The 60% coverage floor correctly identifies this boundary. Jupyter forum shows high unserved fraction (43.1%) among classified topics, suggesting a genuinely underserved population, but the measurement is unreliable due to low coverage and contamination.

Per D083, this domain is closed for candidate generation with the current classifier.

## Reproduction

```bash
cd EXPERIMENTS/125-discourse-jupyter-viewcount
python3 fetch_jupyter.py           # Fetch data (done)
python3 measure_jupyter.py data_jupyter.jsonl  # Measure gates
python3 analyze_coverage.py        # Analyze coverage gap
python3 analyze_unserved.py        # Unserved analysis (despite G2 fail)
```