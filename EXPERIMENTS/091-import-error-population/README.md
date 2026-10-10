<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 — Import-error population measurement

## Summary

**ALL GATES PASS.** The population of Python import-error reports that name a module but no distribution is **2.91%** (25 of 858 reports), well above the 1% kill gate threshold.

## Gate Results

| Gate | Criterion | Result | Value |
|------|-----------|--------|-------|
| G1 | Rate ≥ 1% | **PASS** | 2.91% |
| G2 | Sample ≥ 200 | **PASS** | 858 |
| G3 | Each venue ≥ 50 | **PASS** | Stack Overflow: 259, GitHub: 599 |

## Method

### Population
- **Denominator**: Real Python import-error reports from Stack Overflow and GitHub issues (including library trackers)
- **Numerator**: Reports that name a module in the error message but do not mention the distribution to install, and are help-seeking questions

### Venues & Queries
**Stack Overflow** (8 queries, 259 total):
- `"ImportError" "No module named"` — 50
- `"ModuleNotFoundError" "No module named"` — 50
- `"ImportError" "what package"` — 5
- `"ModuleNotFoundError" "what to install"` — 1
- `"pip install" "ImportError"` — 50
- `"import" "failed" "what package"` — 3
- `"cannot import" "pip install"` — 50
- `"No module named" "pip"` — 50

**GitHub Issues** (5 general queries + 8 library trackers, 599 total):
- General search queries — 249
- python/cpython — 50
- numpy/numpy — 50
- pandas-dev/pandas — 50
- psf/requests — 50
- django/django — 0
- pallets/flask — 50
- sqlalchemy/sqlalchemy — 50
- pytest-dev/pytest — 50

### Classification Logic
1. Extract module name from error message: `ImportError: No module named 'X'` or `ModuleNotFoundError: No module named 'X'`
2. Skip standard library modules (os, sys, json, etc.)
3. Extract distribution names from `pip install X`, `conda install X`, etc.
4. Check if the expected distribution (from known mappings like `sklearn→scikit-learn`, `cv2→opencv-python`) is mentioned
5. Classify as `names_module_no_dist` only if:
   - The error module's distribution is NOT mentioned
   - The post is a help-seeking question (not a bug report)

## Results Breakdown

| Category | Count | Percentage |
|----------|-------|------------|
| names_module_no_dist (help-seeking) | 25 | 2.91% |
| names_module_no_dist_not_question | 82 | 9.56% |
| names_both (module + correct dist) | 142 | 16.55% |
| names_wrong_dist (module + other dist) | 173 | 20.16% |
| not_import_error | 158 | 18.41% |
| other | 268 | 31.24% |
| stdlib_module | 10 | 1.17% |
| **Total** | **858** | **100%** |

## Key Findings

1. **Population exists**: 2.91% of import-error reports are help-seeking questions that name a module but not its distribution. This translates to a real, measurable demand.

2. **Most common module→distribution gaps** (from the 25 `names_module_no_dist`):
   - `cv2` → `opencv-python`
   - `sklearn` → `scikit-learn`
   - `yaml` → `pyyaml`
   - `bs4` → `beautifulsoup4`
   - `crypto` → `pycryptodome`
   - `jwt` → `pyjwt`
   - `dateutil` → `python-dateutil`
   - `dotenv` → `python-dotenv`

3. **Venue difference**: Stack Overflow has higher rate (16/259 = 6.2%) than GitHub (9/599 = 1.5%), likely because Stack Overflow is more question-oriented while GitHub issues include many bug reports.

4. **Large `names_wrong_dist` category (20.16%)**: Many users mention a distribution but not the correct one for their error module, or mention the module name as the distribution (e.g., `pip install sklearn` when they need `scikit-learn`). This is a related but distinct problem.

## Implications for `pyprovides`

The `pyprovides` resolver (built in E085) addresses exactly this population:
- Mechanism: Reads wheel central directory via HTTP Range requests (no install needed)
- Forward coverage: 0.931 on 578 declared distributions from 24 real repositories
- Silent class rate: ~0.6% on real imports (E085, F108)

This experiment confirms the **demand side** exists at a measurable rate (2.91% of import-error reports). The resolver has a real population to serve.

## Artifacts

- `raw/api/` — Raw API responses (gitignored but tracked per manifest)
- `raw/api/manifest.json` — Fetch manifest with counts
- `classified.jsonl` — Per-item classification with rationale
- `results.json` — Summary statistics and gate verdict
- `PROTOCOL.md` — Pre-declared protocol
- `harvest.py`, `classify.py`, `evaluate_gates.py` — Reproducible pipeline

## Reproduction

```bash
cd EXPERIMENTS/091-import-error-population
python3 run.py --all
```

## Limitations

1. **Unauthenticated API limits**: Stack Overflow 300/day, GitHub 10/min. Sample sizes capped accordingly.
2. **Classifier precision**: Automated classification may misclassify some edge cases. The 2.91% is a lower-bound estimate.
3. **Venue coverage**: Only Stack Overflow and GitHub measured. Other venues (Reddit, Discord, mailing lists) not included.
4. **Time window**: Single harvest snapshot. Rates may vary over time.
5. **Module→dist mapping completeness**: The MODULE_TO_DIST dictionary covers ~120 common cases but is not exhaustive.

## Decision

**Population validated.** The import-error population asking "which distribution provides this module" exists at 2.91% rate, exceeding the 1% threshold. The `pyprovides` resolver has a measurable demand population. Next steps could include:
- Building a query-time reverse index (module → distribution) as a service
- Integrating with IDE/error-reporting tools
- Measuring adoption willingness (beyond scope of this experiment)