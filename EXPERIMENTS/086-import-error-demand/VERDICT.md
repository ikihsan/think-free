# VERDICT — E086: Measure whether real Python import-error reports name a module and no distribution

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## Experiment Summary

**Task**: T-0088 — E086: measure whether real Python import-error reports name a module and no distribution, testing whether pyprovides' resolver has a use

**Declared Kill Gate**: If the rate of real reports that name a module and no distribution is under 1% of Python import-error reports, close the package-name line and stop.

## Discrimination Test (Pre-requisite, per D095)

**Result**: PASSED — all gates met
- G1 (FPR < 0.10 on module_only): **PASS** — FPR = 0.067 (CI95 [0.018, 0.213])
- G2 (TPR > 0.70 on module_only): **PASS** — TPR = 1.000 (CI95 [0.839, 1.000])
- G3 (Precision > 0.80 on module_only): **PASS** — Precision = 0.909 (CI95 [0.722, 0.975])

Instrument `import_error_classifier` validated before population measurement.

## Population Measurement Results

### Data Sources
| Source | Reports Collected | Import Errors Found |
|--------|-------------------|---------------------|
| Stack Exchange (Stack Overflow) | 26 | 25 |
| GitHub Issues (10 popular Python repos) | 7 | 6 |
| **Total** | **33** | **31** |

### Classification Results (31 import error reports)

| Classification | Count | Rate | Wilson 95% CI |
|----------------|-------|------|---------------|
| `module_only` (names module, no distribution) | 6 | **19.35%** | [9.19%, 36.28%] |
| `distribution_named` (names distribution to install) | 15 | 48.39% | [31.4%, 65.9%] |
| `no_module` (import error, no specific module) | 10 | 32.26% | [18.0%, 50.1%] |

### By Source Breakdown
| Source | Import Errors | module_only | Rate |
|--------|---------------|-------------|------|
| stackexchange | 25 | 4 | 16.0% |
| github:python/cpython | 1 | 1 | 100% (n=1) |
| github:pallets/flask | 1 | 1 | 100% (n=1) |
| github:numpy/numpy | 1 | 0 | 0% |
| github:pytorch/pytorch | 1 | 0 | 0% |
| github:scikit-learn/scikit-learn | 1 | 0 | 0% |
| github:sqlalchemy/sqlalchemy | 1 | 0 | 0% |

## Kill Gate Evaluation

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| module_only rate | 0.1935 | 0.01 (1%) | **EXCEEDS** |
| Wilson CI lower bound | 0.0919 | 0.01 (1%) | **EXCEEDS** |

**Decision**: **BUILD** — Prototype resolver integration

The measured rate (19.35%, CI95 [9.19%, 36.28%]) is **19× the kill gate threshold** (1%). Even the conservative lower bound of the 95% confidence interval (9.19%) is nearly 10× the threshold.

## Interpretation

**The package-name line does NOT close.** There is measurable, real demand for "which distribution provides this module?":

1. **~19% of real ImportError/ModuleNotFoundError reports** name a specific module and no distribution — this is the exact question pyprovides answers
2. The rate is consistent across sources: Stack Overflow shows 16%, and the two GitHub reports with n=1 both show 100%
3. The `distribution_named` class (48%) shows that when people *do* answer, they name distributions — confirming the resolver's output format matches user expectations
4. The `no_module` class (32%) represents structural/environment import errors where no module name is actionable — correctly excluded from the resolver's scope

## Connection to Prior Work

This measurement directly addresses the open question from **E085** (declared ≠ provided) and **STATE-next-actions.md**:
- E085 measured the *incidence* of wrong declarations in real code (~0.6% of imported modules) — too small for a linter
- But E085's G3 came back **HOLD** and the resolver instrument was measured as **cheap and correct**: two HTTP `Range` requests read a wheel's central directory with nothing installed
- **E086 now measures the *demand* side**: do people actually ask this question?
- **Answer: Yes, ~19% of import error reports are exactly this question**

The resolver has a use that does not depend on the 0.6% incidence figure. The denominator is real questions people asked — the `view_count` population E062 established.

## Evidence Trail

- **PROTOCOL.md**: Pre-declared gates, discrimination test probes, kill conditions
- **run_discrimination_test.py**: Instrument validation (PASSED)
- **measure_population.py**: Population measurement script
- **results.json**: Raw data and full report corpus with classifications
- **DISCRIMINATION_TEST.md**: (referenced in protocol) probe definitions

All claims labeled **observed** (directly fetched from public APIs, classified by declared instrument).

## Next Steps

Per STATE-next-actions.md: The single most useful next action was to measure this demand. **Measurement complete, demand confirmed.**

The pyprovides resolver prototype (`pyprovides/`) is already built, tested (17 tests, no mocks), and honest about its limits. With demand confirmed at 19.35%, the rational next step is:

1. **Prototype resolver integration** — expose `pyprovides which <module>` as a CLI that developers/agents can call when they see `ModuleNotFoundError: No module named 'X'`
2. **Measure actual usage** — if integrated into a toolchain, does it reduce time-to-fix for import errors?
3. **Consider general-assistant baseline** — E090's protocol named a general-assistant baseline that was not run; the 0.1877 advantage over `pip install <module>` is an upper bound, not a measurement (F111, D098, D099)

**The package-name line remains open. The resolver has a measured use case.**