<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E095: crates.io view-count principle test

## Summary
**Result: View-count principle does NOT robustly generalize to crates.io (Rust package registry).**

## Method
Tested whether need-related crates (those with keywords indicating debugging, error handling, profiling, logging, monitoring, tracing, diagnostics, observability, benchmarking, testing) have systematically higher download activity than random crates.

- **Need-related sample**: 70 crates (substring keyword matching across 16 need-related keywords)
- **Random sample**: 476 crates (no need-related keywords)
- **Metrics**: `downloads` (total), `recent_downloads` (last 90 days)

## Key Findings

### Binary "active" (recent_downloads > 0)
- **Need-related**: 70/70 = 100%
- **Random**: 476/476 = 100%
- **Difference**: 0 pp
- **p-value**: 1.000
- All crates have at least some recent downloads — no discrimination.

### Threshold-based analysis (recent_downloads)
| Threshold | Need-related | Random | Difference |
|-----------|-------------|--------|------------|
| > 10 | 85.7% | 78.4% | +7.3 pp |
| > 50 | 68.6% | 56.5% | +12.1 pp |
| > 100 | 54.3% | 44.7% | +9.6 pp |
| > 500 | 28.6% | 22.1% | +6.5 pp |
| > 1000 | 24.3% | 11.1% | +13.2 pp |

### Threshold-based analysis (total_downloads)
| Threshold | Need-related | Random | Difference |
|-----------|-------------|--------|------------|
| > 100 | 80.0% | 78.6% | +1.4 pp |
| > 500 | 48.6% | 59.0% | -10.4 pp |
| > 1000 | 45.7% | 50.8% | -5.1 pp |
| > 5000 | 31.4% | 19.7% | +11.7 pp |
| > 10000 | 21.4% | 13.0% | +8.4 pp |

### Continuous analysis (Mann-Whitney U test, log scale)
- **Total downloads**: p = 0.082, rank-biserial r = 0.16 (need log mean 6.30 < random 6.89)
- **Recent downloads**: p = 0.139, rank-biserial r = 0.14 (need log mean 5.24 > random 4.70)
- Neither reaches significance at p < 0.05

### Median comparison
| Metric | Need-related | Random |
|--------|-------------|--------|
| Total downloads | 495 | 1,053 |
| Recent downloads | 109 | 83 |

Random crates have higher total downloads; need-related have slightly higher recent downloads.

## Gate Evaluation (per E071/E072/E090 protocol)

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** Sample size ≥ 100 each | Need: 70, Random: 476 | **FAIL** |
| **G2** Significance p < 0.05 | Proportion p=1.0, MW p=0.082/0.139 | **FAIL** |
| **G3** Effect size | Wilson LB=0.92 (but all active), r=0.16 | **MIXED** (binary PASS but trivial) |
| **G4** Arrival field rate ≥ 95% | 100% both groups | **PASS** |

## Conclusion
The view-count principle **does not generalize** to crates.io. Unlike PyPI and NPM where need-related packages showed systematically higher activity, on crates.io:

1. **All crates are "active"** (recent_downloads > 0), eliminating binary discrimination
2. **Threshold-dependent results** — differences appear at some thresholds but reverse at others
3. **No statistical significance** in continuous download metrics
4. **Small need-related population** — only 70 crates found with need-related keywords
5. **Random crates have higher total downloads** — popular general-purpose crates dominate

This is consistent with failures on Maven Central (E090) and Hugging Face Hub (E101), suggesting the view-count principle works on:
- ✅ Package registries with **semantic versioning and release cycles** (PyPI, NPM)
- ✅ **Q&A forums** with view_count metadata (Discourse, Stack Exchange)

But NOT on:
- ❌ **Artifact registries without clear release semantics** (Maven Central, crates.io, Hugging Face Hub)

## Files
- `PROTOCOL.md` — Experiment protocol
- `collect_v3.py` — Data collection script
- `analyze.py` — Analysis script (stdlib only)
- `raw/crates_data_v3.json` — Raw collected data
- `results.json` — Gate evaluation results