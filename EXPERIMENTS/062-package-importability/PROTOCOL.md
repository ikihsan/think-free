# E062 — Python package name import resolvability probe

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

## Question

Fresh observation (per D080): given Python package-like names following common naming conventions, what proportion are resolvable by the import mechanism (`importlib.util.find_spec`) without package installation?

## Method

- Sample: 100 synthetic package name strings following common Python naming patterns
  - Lowercase with underscores (e.g. `my_tool`, `data_utils`)
  - Lowercase with hyphens (e.g. `my-tool`, `data-tool`)
  - UpperCamelCase (e.g. `MyTool`, `DataTool`)
  - Digits suffixes (e.g. `tool_01`, `lib_v2`)
  - Common prefix patterns (e.g. `py_`, `lib_`, `tool_`, `mod_`)
- Instrument: `importlib.util.find_spec(name)` — returns a `ModuleSpec` if the module can be resolved through the import machinery, `None` otherwise
- Per name: record `find_spec_result` (True/False), and if False, categorize the failure mode
- Kill gate (declared): if the resolvability share < 0.30 AND the sample contains > 5 names that are valid Python identifiers but unresolved → population not observed → KILL → nothing to build

## Reproduction

```bash
python3 EXPERIMENTS/062-package-importability/run.py
```

Raw results saved to `results.json`. Classification logic in `classify.py`.

## Verdict

**KILL.** resolvability share = 0.13 (threshold 0.30), valid_identifier_unresolved = 70 (> 5).
The hypothesis that "Python package-like names are generally resolvable by the import mechanism" is falsified. Only 13% of tested names resolved: 6 were standard library names (json, os, sys, math, collections, random), and the remaining 7 resolved names included additional stdlib hits. 70 valid Python identifiers were unresolvable, and 17 names had invalid identifier patterns.

**Failure mode breakdown:**
- `valid_identifier_not_resolved`: 61 (61.0%) — names that are syntactically valid Python identifiers but not find-spec-resolvable
- `invalid_identifier`: 17 (17.0%) — names with hyphens, dots, or other non-identifier characters
- `camelcase_identifier_not_resolved`: 9 (9.0%) — UpperCamelCase names not resolvable
- `resolved`: 13 (13.0%) — standard library module names only

**Raw evidence:** `EXPERIMENTS/062-package-importability/results.json` contains the full results for all 100 names with per-name resolution status and failure category.

**Decision:** The import-resolvability hypothesis is closed. Synthetic Python-package-like names are generally not resolvable without package installation. This advances the practical difficulty measurement: when programmers encounter package names in Q&A, documentation, or tutorials, they cannot determine importability via `importlib.util.find_spec` alone, confirming the friction point identified in the mission's prior art (E059 measured name mismatches, E039 measured need-to-tool gaps).

**Next action:** Close this experiment and move to fresh observation. The seat for a new candidate remains empty; continue independent exploration for a specific testable opportunity.