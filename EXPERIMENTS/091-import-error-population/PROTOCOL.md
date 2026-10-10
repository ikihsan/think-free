# E091 — Import-error population asking "which distribution provides this module"

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-10
-->

## Question

What fraction of real Python import-error reports (Stack Overflow, GitHub issues, CPython/library trackers) explicitly name a module but no distribution — i.e., the user asks "I'm getting `ImportError: No module named 'X'`, what package do I install?"

This is the demand population for the `pyprovides` resolver. The tool is built and its mechanism is measured (E085: 0.931 forward coverage on declared distributions, 0.6% silent class on real imports). But its usefulness depends on whether people actually ask this question.

## Population

**Denominator**: Real Python import-error reports across three venues:
- Stack Overflow questions tagged `python` containing `ImportError` or `ModuleNotFoundError`
- GitHub issues in Python repositories containing `ImportError` or `ModuleNotFoundError`
- CPython and major library issue trackers (numpy, pandas, requests, django, etc.)

**Numerator**: Reports that name a module but no distribution — the user has an import error for `X` and wants to know what to `pip install`.

## Instrument

Search each venue with predefined queries, fetch results, classify each result by hand (or with a reproducible rule) into:
- `names_module_no_dist`: Names a module (e.g., `sklearn`, `cv2`, `Crypto`) but does not name the distribution to install (`scikit-learn`, `opencv-python`, `pycryptodome`)
- `names_both`: Names both the module and the distribution
- `names_dist_only`: Names the distribution but not the module (irrelevant to this question)
- `not_import_error`: Not actually an import error report
- `other`: Other

## Kill Gate

**G1**: If the rate of `names_module_no_dist` reports is under **1%** of all Python import-error reports sampled, **close the line and stop**. The resolver has no measurable demand.

**G2**: Must sample at least **200** import-error reports total across venues for the rate to be meaningful.

**G3**: Each venue must contribute at least **50** reports (or all available if fewer exist) to avoid venue bias.

## Queries (fixed before first fetch)

### Stack Overflow (via `api.stackexchange.com/2.3/search/advanced`)

All queries on `site=stackoverflow`, tagged `python`:

1. `"ImportError" "No module named"` — core import error pattern
2. `"ModuleNotFoundError" "No module named"` — Python 3.6+ pattern
3. `"ImportError" "what package"` — explicit package question
4. `"ModuleNotFoundError" "what to install"` — explicit install question
5. `"pip install" "ImportError"` — install then import failure
6. `"import" "failed" "what package"` — generic pattern
7. `"cannot import" "pip install"` — inverse pattern
8. `"No module named" "pip"` — module name + pip mention

### GitHub Issues (via `api.github.com/search/issues`)

Queries across all repositories (unauthenticated, 10/min):

1. `"ImportError" "No module named" language:python type:issue`
2. `"ModuleNotFoundError" "No module named" language:python type:issue`
3. `"import error" "what package" language:python type:issue`
4. `"pip install" "import failed" language:python type:issue`
5. `"cannot import" "pip install" language:python type:issue`

### CPython/Library Trackers (GitHub issues on specific repos)

Target repos: `python/cpython`, `numpy/numpy`, `pandas-dev/pandas`, `psf/requests`, `django/django`, `pallets/flask`, `sqlalchemy/sqlalchemy`, `pytest-dev/pytest`

Query per repo: `"ImportError" OR "ModuleNotFoundError" type:issue`

## Classification Rule

A report is `names_module_no_dist` iff:
- The text contains a Python module name pattern (import statement, error message `No module named 'X'`, or explicit mention of a module name)
- The text does NOT contain the corresponding distribution name (the PyPI package name that provides it)
- The user is asking for help resolving the import (question format, not just reporting a bug in their own code)

Common module→distribution mappings the classifier must know:
- `sklearn` → `scikit-learn`
- `cv2` → `opencv-python`
- `Crypto` → `pycryptodome` (or `pycrypto`, deprecated)
- `PIL` → `pillow`
- `yaml` → `pyyaml`
- `dateutil` → `python-dateutil`
- `MySQLdb` → `mysqlclient`
- `psycopg2` → `psycopg2-binary` (or `psycopg2`)
- `redis` → `redis` (same)
- `requests` → `requests` (same)
- `numpy` → `numpy` (same)
- `pandas` → `pandas` (same)

If the module name equals the distribution name (e.g., `requests`, `numpy`), it is NOT `names_module_no_dist` — the user already has the answer.

## Reproduction

```bash
cd EXPERIMENTS/091-import-error-population
python3 run.py --gate
```

## Outputs

- `raw/api/se-*.json` — Stack Overflow raw responses
- `raw/api/gh-*.json` — GitHub raw responses
- `raw/api/repo-*.json` — Library tracker raw responses
- `raw/manifest.json` — All fetches with counts
- `classified.jsonl` — Per-item classification with rationale
- `results.json` — Summary statistics and gate verdict
- `README.md` — Human-readable report