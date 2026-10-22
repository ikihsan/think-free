# Session 2026-10-21-021-package-fedmarket-as-a-proper-open-sourc

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T15:31:08+00:00
- **Duration:** 2143.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Package fedmarket as a proper open-source prototype with documentation, tests, and packaging for release evaluation

## Summary

Packaged fedmarket as a proper open-source prototype with:
- Python package structure (fedmarket/ with __init__, __main__, core, data, dynamic, dynamic_api, dynamic_rec modules)
- CLI entry point with --refresh, --decision, --subaward, --format, --output flags
- Two-axis recommendation engine (entry accessibility vs business sustainability)
- Static pre-computed data from E197-E211 experiments
- Dynamic USAspending API client with SQLite caching
- E211 survival/graduation metrics integration from raw results
- Profile-matched decision mode (budget + GTM + focus -> PSC code recommendation)
- 19 tests passing (static fallback, two-axis logic, format functions, dynamic API)
- README with usage examples and data provenance
- MIT license and pyproject.toml for packaging

## Next

Field test with 3-5 small software companies (E208) to validate decision guides against real pipeline opportunities; GSA eLibrary cross-reference for SIN validation; SEWP catalog deep dive

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| fedmarket/README.md | aa7b1db29aa4 | 5238 |
| fedmarket/__main__.py | 8a4af954978f | 23938 |
| fedmarket/dynamic_rec.py | abbf50f9d3e9 | 18744 |
| tests/test_fedmarket_dynamic.py | ccf900fced89 | 7797 |
| fedmarket/LICENSE | 07a91875c743 | 1074 |
| tests/test_fedmarket.py | 9e27501c37d0 | 8420 |
| fedmarket/dynamic_api.py | c065b953b440 | 15345 |
| fedmarket/dynamic.py | 0ccb03f1e693 | 1402 |
| pyproject.toml | 886753cb5d21 | 1069 |
| fedmarket/core.py | a4b3f131f213 | 3663 |
| fedmarket/__init__.py | f2e35ec23f90 | 788 |
| fedmarket/data.py | 5b327f3154bd | 5036 |
| fedmarket/__init__.py | f2e35ec23f90 | 788 |
| fedmarket/__main__.py | 8a4af954978f | 23938 |
| fedmarket/data.py | 5b327f3154bd | 5036 |
| fedmarket/core.py | a4b3f131f213 | 3663 |
| fedmarket/dynamic.py | 0ccb03f1e693 | 1402 |
| fedmarket/dynamic_api.py | c065b953b440 | 15345 |
| fedmarket/dynamic_rec.py | abbf50f9d3e9 | 18744 |
| fedmarket/README.md | aa7b1db29aa4 | 5238 |
| fedmarket/LICENSE | 07a91875c743 | 1074 |
| pyproject.toml | 886753cb5d21 | 1069 |
| tests/test_fedmarket.py | 9e27501c37d0 | 8420 |
| tests/test_fedmarket_dynamic.py | ccf900fced89 | 7797 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 930 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .fedmarket_cache.db |
|   undeclared | ENHANCEMENT-PLAN.md |
|   undeclared | EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_7A21.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_D304.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 15:31:08 | session_start | Package fedmarket as a proper open-source prototype with documentation, tests, and packaging for release evaluation |
| 2 | 16:02:42 | artifact | wrote fedmarket/README.md |
| 3 | 16:02:42 | artifact | wrote fedmarket/__main__.py |
| 4 | 16:02:42 | artifact | wrote fedmarket/dynamic_rec.py |
| 5 | 16:02:43 | artifact | wrote tests/test_fedmarket_dynamic.py |
| 6 | 16:02:43 | artifact | wrote fedmarket/LICENSE |
| 7 | 16:02:44 | artifact | wrote tests/test_fedmarket.py |
| 8 | 16:02:44 | artifact | wrote fedmarket/dynamic_api.py |
| 9 | 16:02:44 | artifact | wrote fedmarket/dynamic.py |
| 10 | 16:02:45 | artifact | wrote pyproject.toml |
| 11 | 16:02:47 | artifact | wrote fedmarket/core.py |
| 12 | 16:02:48 | artifact | wrote fedmarket/__init__.py |
| 13 | 16:02:49 | artifact | wrote fedmarket/data.py |
| 14 | 16:05:17 | artifact | wrote fedmarket/__init__.py |
| 15 | 16:05:22 | artifact | wrote fedmarket/__main__.py |
| 16 | 16:05:25 | artifact | wrote fedmarket/data.py |
| 17 | 16:05:28 | artifact | wrote fedmarket/core.py |
| 18 | 16:05:31 | artifact | wrote fedmarket/dynamic.py |
| 19 | 16:05:35 | artifact | wrote fedmarket/dynamic_api.py |
| 20 | 16:05:40 | artifact | wrote fedmarket/dynamic_rec.py |
| 21 | 16:05:43 | artifact | wrote fedmarket/README.md |
| 22 | 16:05:46 | artifact | wrote fedmarket/LICENSE |
| 23 | 16:05:49 | artifact | wrote pyproject.toml |
| 24 | 16:05:52 | artifact | wrote tests/test_fedmarket.py |
| 25 | 16:05:56 | artifact | wrote tests/test_fedmarket_dynamic.py |
| 26 | 16:06:19 | unlogged_change | changed but never declared as an artifact: .fedmarket_cache.db |
| 27 | 16:06:19 | unlogged_change | changed but never declared as an artifact: ENHANCEMENT-PLAN.md |
| 28 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
| 29 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
| 30 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
| 31 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
| 32 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_7A21.json |
| 33 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_D304.json |
| 34 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
| 35 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
| 36 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
| 37 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
| 38 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
| 39 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
| 40 | 16:06:19 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |
| 948 | 16:06:50 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-020-gsa-elibrary-cross-ref-validation-and-se/commands.log |
| 949 | 16:06:50 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-020-gsa-elibrary-cross-ref-validation-and-se/events.jsonl |
| 950 | 16:06:51 | unlogged_change | changed but never declared as an artifact: tests/test_docfiles_index.py |
| 951 | 16:06:51 | unlogged_change | changed but never declared as an artifact: tests/test_predirty_attribution.py |
| 952 | 16:06:51 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 953 | 16:06:51 | unlogged_change | changed but never declared as an artifact: usaspending_assess/__init__.py |
| 954 | 16:06:51 | unlogged_change | changed but never declared as an artifact: usaspending_assess/assess.py |
| 955 | 16:06:51 | unlogged_change | changed but never declared as an artifact: usaspending_assess/cli.py |
| 956 | 16:06:51 | doc_update | updated STATE.md |
| 957 | 16:06:51 | session_end | Packaged fedmarket as a proper open-source prototype with: - Python package structure (fedmarket/ with __init__, __main__, core, data, dynamic, dynami |

_907 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-021-package-fedmarket-as-a-proper-open-sourc/events.jsonl
```
