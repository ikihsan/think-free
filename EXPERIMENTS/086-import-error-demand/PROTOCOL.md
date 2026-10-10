# E086 — Measure whether real Python import-error reports name a module and no distribution

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## The question

**Of real Python `ImportError` / `ModuleNotFoundError` reports that name a module, what fraction name *only the module* and no distribution to install?**

This is the denominator the pyprovides resolver needs: if people ask "which distribution provides this module?", the instrument has a use. If they don't, the package-name line closes.

Per STATE-next-actions.md: **Declared kill gate — if the rate of real reports that name a module and no distribution is under 1% of Python import-error reports, close the line and stop.**

## Per D095: Discrimination test required before population measurement

The instrument is a classifier `import_error_classifier(report_text)` that returns:
- `module_only` — report names a specific module to import, no distribution named
- `distribution_named` — report names a distribution to install (e.g., "pip install X", "install X")
- `no_module` — report does not name a specific importable module
- `not_import_error` — report is not an ImportError/ModuleNotFoundError

**Discrimination test probes (labels known by construction):**

### Known-module-only (should classify as `module_only`) — 20 probes
Real ImportError patterns where module is named, no distribution:

| # | Probe Text | Rationale |
|---|------------|-----------|
| M1 | `ModuleNotFoundError: No module named 'sklearn'` | Classic sklearn vs scikit-learn |
| M2 | `ImportError: No module named 'PIL'` | PIL vs pillow |
| M3 | `ModuleNotFoundError: No module named 'cv2'` | cv2 vs opencv-python |
| M4 | `ImportError: No module named 'yaml'` | yaml vs PyYAML |
| M5 | `ModuleNotFoundError: No module named 'bs4'` | bs4 vs beautifulsoup4 |
| M6 | `ImportError: No module named 'dateutil'` | dateutil vs python-dateutil |
| M7 | `ModuleNotFoundError: No module named 'serial'` | serial vs pyserial |
| M8 | `ImportError: No module named 'attr'` | attr vs attrs |
| M9 | `ModuleNotFoundError: No module named 'Crypto'` | Crypto vs pycryptodome |
| M10 | `ImportError: cannot import name 'sklearn' from 'sklearn'` | Namespace confusion |
| M11 | `ModuleNotFoundError: No module named 'skimage'` | skimage vs scikit-image |
| M12 | `ImportError: No module named 'pysftp'` | Module name differs from package |
| M13 | `ModuleNotFoundError: No module named 'MySQLdb'` | MySQLdb vs mysqlclient |
| M14 | `ImportError: No module named 'pkg_resources'` | pkg_resources vs setuptools |
| M15 | `ModuleNotFoundError: No module named 'ldap'` | ldap vs python-ldap |
| M16 | `ImportError: No module named 'magic'` | magic vs python-magic |
| M17 | `ModuleNotFoundError: No module named 'psycopg2'` | psycopg2 vs psycopg2-binary |
| M18 | `ImportError: No module named 'redis'` | redis module name |
| M19 | `ModuleNotFoundError: No module named 'elasticsearch'` | elasticsearch vs elasticsearch-py |
| M20 | `ImportError: No module named 'kubernetes'` | kubernetes vs kubernetes-client |

### Known-distribution-named (should classify as `distribution_named`) — 10 probes
Reports that explicitly name a distribution to install:

| # | Probe Text | Rationale |
|---|------------|-----------|
| D1 | `pip install scikit-learn fixed the ModuleNotFoundError for sklearn` | Explicit distribution |
| D2 | `I installed pillow and now PIL works` | Distribution named |
| D3 | `Try: pip install opencv-python` | Distribution named |
| D4 | `Install PyYAML: pip install PyYAML` | Distribution named |
| D5 | `You need to install beautifulsoup4, not bs4` | Distribution named |
| D6 | `python-dateutil provides dateutil` | Distribution named |
| D7 | `pip install pyserial solves the serial import` | Distribution named |
| D8 | `attrs package provides attr module` | Distribution named |
| D9 | `pycryptodome is the drop-in replacement for Crypto` | Distribution named |
| D10 | `Install scikit-image for skimage` | Distribution named |

### Known-no-module (should classify as `no_module`) — 10 probes
Error reports without a specific module name:

| # | Probe Text | Rationale |
|---|------------|-----------|
| N1 | `ImportError: cannot import name 'X' from 'Y'` | Names submodule, not top-level |
| N2 | `ImportError: attempted relative import with no known parent package` | Structural, no module name |
| N3 | `ImportError: dynamic module does not define module export function` | C extension issue |
| N4 | `ModuleNotFoundError` | No module named at all |
| N5 | `ImportError: DLL load failed while importing _ssl` | Binary load failure |
| N6 | `ImportError: libssl.so.1.1: cannot open shared object file` | System library missing |
| N7 | `ImportError: /usr/lib/python3.8/lib-dynload/_ctypes.cpython-38-darwin.so: invalid ELF header` | Binary corruption |
| N8 | `SyntaxError: invalid syntax` then `ImportError` | Not an import error primarily |
| N9 | `ImportError: cannot import name 'foo' from partially initialized module 'bar'` | Circular import |
| N10 | `ImportError: Module 'x' has no attribute 'y'` | Attribute error, not module |

### Known-not-import-error (should classify as `not_import_error`) — 10 probes
Non-import errors:

| # | Probe Text | Rationale |
|---|------------|-----------|
| E1 | `SyntaxError: invalid syntax` | Syntax error |
| E2 | `NameError: name 'x' is not defined` | Name error |
| E3 | `AttributeError: 'NoneType' object has no attribute 'foo'` | Attribute error |
| E4 | `TypeError: 'int' object is not callable` | Type error |
| E5 | `ValueError: invalid literal for int()` | Value error |
| E6 | `KeyError: 'missing_key'` | Key error |
| E7 | `IndexError: list index out of range` | Index error |
| E8 | `FileNotFoundError: [Errno 2] No such file` | File error |
| E9 | `ConnectionError: [Errno 111] Connection refused` | Network error |
| E10 | `RuntimeError: CUDA out of memory` | Runtime error |

## Discrimination Test Gate Criteria

| Gate | Criterion | Threshold | Kill Condition |
|------|-----------|-----------|----------------|
| G1 | False Positive Rate on `module_only` (non-module-only classified as `module_only`) | < 0.10 (10%) | **FAIL → instrument invalid, redesign** |
| G2 | True Positive Rate on `module_only` (known-module-only correctly classified) | > 0.70 (70%) | FAIL → instrument lacks sensitivity |
| G3 | Precision on `module_only` (of predicted `module_only`, fraction that are truly `module_only`) | > 0.80 (80%) | FAIL → too many false positives |

**Pass Condition**: G1 PASS AND (G2 PASS OR G3 PASS)

## Population Measurement

After discrimination test passes, measure on real reports from:

1. **Stack Overflow** — Questions tagged `python` with `importerror` or `modulenotfounderror` in title/body
2. **GitHub Issues** — Issues in popular Python repositories with import error titles
3. **CPython Issue Tracker** — bugs.python.org / GitHub CPython issues
4. **Popular Library Issue Trackers** — numpy, pandas, requests, django, flask, etc.

For each source, collect up to 200 reports, classify each, compute rate with Wilson 95% CI.

## Kill Gate for Population Measurement

| Measured Rate (module_only / all import errors) | Decision |
|-------------------------------------------------|----------|
| < 0.01 (1%) | **KILL** — Close package-name line |
| 0.01 ≤ rate < 0.05 | **HOLD** — Report CI, consider larger corpus |
| ≥ 0.05 | **BUILD** — Prototype resolver integration |

## Denominators and Units

- Unit: one import-error report (question, issue, or thread)
- Fractions over reports classified as import errors (module_only + distribution_named + no_module)
- Each source reported separately + combined

## Reachable Success Region (per D088)

- Minimum 10 known-module-only probes must be reachable (have matching real reports)
- Maximum 3 known-distribution-named probes may be misclassified as module_only
- Classifier must not rely on a single keyword that correlates with noise

---

## Next Action

1. Implement discrimination test harness
2. Run discrimination test on probe set
3. If G1 PASS, proceed to population measurement on real reports
4. Report VERDICT.md with measured rate and decision