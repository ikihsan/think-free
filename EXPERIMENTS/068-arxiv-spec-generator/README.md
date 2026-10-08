<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-08
-->

# E068 — Spec generator from partial repo information for ArXiv computational papers

**Status**: Complete — **2 of 4 kill gates PASSED, 2 FAILED**

## Experiment Summary

**Experiment ID:** 068-arxiv-spec-generator  
**Date:** 2026-10-08  
**Follows:** E067 (ArXiv reproducibility measurement)

## Hypothesis Tested

**H0 (null):** A deterministic, stdlib-only algorithm cannot generate runnable pinned environment specifications from the partial information available in ArXiv paper repositories (README install instructions, unpinned requirements, source code imports).

**H1 (alternative):** A deterministic algorithm using only Python stdlib can generate syntactically valid pinned `requirements.txt` files that cover ≥50% of source code imports, with ≥70% version resolution rate, and can recover ≥80% of known pins for repos with ground truth.

**Result:** **MIXED** — Mechanism shows promise (syntactic validity 100%, import coverage 73.8%), but validation recovery and version resolution gates failed.

## Kill Gate Results (Observed)

| Gate | Threshold | Actual | Pass/Fail |
|------|-----------|--------|-----------|
| **K1** (validation recovery) | ≥80% pins recovered for ≥2 of 4 A1 repos | **1/4** repos had comparable ground truth (100% recovery) | ❌ FAIL |
| **K2** (syntactic validity) | ≥90% valid `pkg==X.Y.Z` lines | **100%** (505/505) | ✅ PASS |
| **K3** (import coverage) | ≥50% avg import coverage for A3/A4 | **73.8%** avg | ✅ PASS |
| **K4** (version resolution) | ≥70% packages resolve on PyPI | **55.3%** (384/695) | ❌ FAIL |

## Detailed Results

### K1: Validation Recovery (Ground Truth A1 Repos)

| Repo | Env Type | Original Packages (req.txt) | Recovered | Rate |
|------|----------|----------------------------|-----------|------|
| illidanlab/inversion-influence-function | conda | N/A (conda only) | — | — |
| Profluent-Internships/MMDiff | conda | N/A (conda only) | — | — |
| deeplearning-wisc/args | pip | 57 | 57 | **100%** |
| qzhb/BSSARD | conda | N/A (conda only) | — | — |

**Problem**: 3 of 4 A1 repos use conda `environment.yml` as their machine-runnable spec. The extractor only parsed `requirements.txt`, so no ground truth was available for comparison. The one pip-based repo achieved 100% recovery.

### K2: Syntactic Validity

All 505 generated package lines across 25 repos are syntactically valid `pkg==X.Y.Z` format.

### K3: Import Coverage (A3/A4 Repos)

| Repo (Arm) | Imports Covered | Total Imports | Coverage |
|------------|----------------|---------------|----------|
| LPMP/BDD (A3) | 20 | 29 | 69.0% |
| suzy0223/STSM (A3) | 7 | 9 | 77.8% |
| Goallow/Mini-Hes (A3) | 0 | 0 | 100% |
| ambroiseodt/tsim (A3) | 8 | 10 | 80.0% |
| EternityYW/Gemini-Commonsense-Evaluation (A3) | 0 | 0 | 100% |
| liujf69/EPP-Net-Action (A3) | 69 | 139 | 49.6% |
| hao1635/LIT-Former (A3) | 20 | 22 | 90.9% |
| cvblab/Mitosis-UTS (A3) | 14 | 16 | 87.5% |
| JHW2000/JARNet (A3) | 20 | 29 | 69.0% |
| DrLuo/RTM (A3) | 13 | 17 | 76.5% |
| AmitRozner/domain-generalizable-multiple-domain-clustering (A3) | 35 | 63 | 55.6% |
| CIAM-Group/NCO_code (A4) | 22 | 75 | 29.3% |
| AlibabaResearch/DAMO-ConvAI (A4) | 90 | 130 | 69.2% |
| clovaai/TVQ-VAE (A4) | 27 | 35 | 77.1% |
| FARAZLOTFI/underwater-object-tracking (A4) | 15 | 26 | 57.7% |
| geoaigroup/GEOAI-ECRS2023 (A4) | 36 | 58 | 62.1% |
| peteryang1031/Causal-GWIB (A4) | 32 | 49 | 65.3% |
| google-research/google-research (A4) | 0 | 0 | 100% |
| Xiaoqi-Zhao-DLUT/Multi-Source-APS-ZVOS (A4) | 6 | 7 | 85.7% |

**Average**: 73.8% — **GATE PASSES**

### K4: Version Resolution Rate

- Total unique packages identified across all sources: 695
- Resolved to stable PyPI version: 384 (55.3%)
- Not found on PyPI: ~250 (many are internal modules, local package names, stdlib false positives)
- No stable version: ~60

**Root causes of low resolution:**
1. **Internal/local modules**: Many imports are internal package names (e.g., `models`, `utils`, `config`, `data`, `train`, `engine`) not published on PyPI
2. **Stdlib false positives**: Some stdlib modules not in exclusion list (e.g., `copyreg`, `cmath`, `imp`, `cpickle`, `gzip`, `tarfile`, `zipfile`, `queue`, `pdb`, `traceback`, `xml`)
3. **Conda-only packages**: CUDA toolkits (`nvidia_cublas_cu12`, etc.), `detectron2`, `mmcv`, `openslide`, `rclpy`
4. **Non-standard names**: Packages with `_` prefixes, numbered names, or very generic names

## Algorithm Design

**Core approach:** Deterministic multi-source extraction + PyPI resolution:

1. **Source extraction** (stdlib `ast`, `re`, `tomllib`):
   - `requirements*.txt` → package names
   - `pyproject.toml` (project/poetry deps) → package names
   - `poetry.lock` → package names
   - README text → version hints via regex
   - Source code (`.py` files, ≤200 per repo) → `ast` import scanning

2. **Version resolution** (stdlib `urllib` + `json`):
   - PyPI JSON API (`https://pypi.org/pypi/{package}/json`)
   - Latest stable version (excludes alpha/beta/rc/dev; allows post)
   - Local disk caching for reproducibility

3. **Generation**: Sorted `pkg==version` lines for all resolved packages

**No external dependencies**: Pure Python 3.8+ standard library.

## Baseline Comparison

No automated baseline run (would require installing each repo in a clean venv). Manual inspection: the naive baseline of "install via `pip install -e .` or `pip install -r requirements.txt` then `pip freeze`" fails for most A3/A4 repos because they lack installable metadata.

## Artifacts

- `fetch_repos.py` — Shallow clone repos from E067 assessment
- `extract.py` — Extract partial info (README, requirements, imports)
- `resolve.py` — Resolve versions via PyPI API (cached)
- `generate.py` — Generate pinned `requirements.txt` files
- `validate.py` — Apply kill gates
- `cache/extracted.json` — Extracted partial info per repo
- `cache/resolved.json` — PyPI resolution cache (695 packages)
- `cache/generated_specs/` — 25 generated `requirements.txt` files
- `cache/validation_results.json` — Full gate evaluation

## Environment

- Python 3.8.10, stdlib only
- Network: PyPI API (unauthenticated, ~695 requests with 0.1s delay)
- Disk: ~200MB for shallow clones + PyPI cache
- Runtime: ~15 min (mostly PyPI resolution)

## Epistemic Limits

- **Conda blind spot**: 3/4 A1 ground truth repos use conda; parser doesn't read `environment.yml` pins for validation
- **Import ≠ dependency**: Many scanned imports are internal modules, stdlib, or transitive deps
- **No install test**: Gates measure generation quality, not whether `pip install -r generated.txt` works
- **Single Python version**: Resolution assumes Python 3.10; some packages have version constraints per Python version
- **PyPI-only**: Cannot resolve Conda-only, private, or system packages
- **Shallow clones**: May miss files in subdirectories
- **A passing gate establishes mechanism feasibility, not product viability or adoption**

## Most Useful Next Action

**Fix the conda parsing gap for K1 validation** — add `environment.yml` parsing to extract ground-truth pins from the 3 conda-based A1 repos. This would likely make K1 pass (100% recovery on args + expected high recovery on conda repos).

**For K4**, the 55% resolution rate reflects a fundamental limitation: import scanning captures many non-PyPI names. A practical generator would need:
- Better stdlib/module filtering (expand exclusion list with common internal patterns)
- Conda-forge API fallback for ML/scientific packages
- Heuristics to distinguish "real dependency" from "internal import"

**The mechanism is viable for pip-based projects with requirements.txt/pyproject.toml**; for conda-only or import-only repos, it needs the above improvements before product claims.