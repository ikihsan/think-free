<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E079 — ArXiv computational reproducibility: falsification experiment

## Predeclared protocol (before any implementation)

### Claim under test (H-01)

Given an ArXiv computational paper's GitHub repository with incomplete environment specification (A2: partial spec, or A3: docs-only per E067 classification), a deterministic tool can generate a machine-runnable environment specification (conda `environment.yml` or `requirements.txt` with all versions pinned) that successfully installs and executes the paper's main computational entry point on a clean virtual environment.

### Kill gate (must be met to continue)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** — Install success rate | Fraction of generated specs that `pip install`/`conda env create` without error | **≥ 80%** |
| **G2** — Smoke test pass rate | Fraction of installed envs where main module imports and `--help`/minimal run succeeds | **≥ 80% of installed** |
| **G3** — Combined success rate | Fraction of papers with both install success AND smoke test pass | **≥ 30% of A2+A3 papers** |
| **G4** — Baseline comparison | Tool combined success rate vs `repo2docker` baseline combined success rate | **Tool > Baseline + 10pp** |

**Abandon if:** Any gate fails. Gates evaluated on held-out sample of 20 A2+A3 papers (stride sample from E067 population, excluding the 34 already assessed).

### Strongest baseline

**`repo2docker` (v2024)** — builds Docker image from repo's existing config files (requirements.txt, environment.yml, Dockerfile, etc.), using latest compatible versions where unpinned. Run on each test repo, then smoke test in container.

Why this baseline: It is the strongest existing automated approach for "build runnable env from repo." It uses the same input (repo files) and same oracle (execution test). It does not invent pinned versions — it uses latest — so any improvement from version inference is measurable.

### Information-sufficiency witness (pre-implementation)

**Witness W-ARXIV-1:** Two synthetic repositories with identical permitted inputs but requiring different pinned versions.

- **Repo A:** `requirements.txt` = `numpy\npandas`, uses `numpy.lib.array_function` (added in 1.16, changed in 1.22). Requires `numpy==1.21.0`.
- **Repo B:** `requirements.txt` = `numpy\npandas`, uses only stable `numpy.array` API. Works with `numpy>=1.20`.

**Permitted inputs for tool:** Repository file tree, `requirements.txt` content, Python version, paper metadata (date).

**Required outputs:** Pinned `requirements.txt` with `numpy==X.Y.Z`.

**Test:** If tool produces identical pinned versions for both repos from identical permitted inputs, the witness **fails** — the tool cannot distinguish the two realities. If tool produces different versions (or abstains on one), the witness **passes** — the permitted inputs suffice to distinguish.

**Implementation:** `witness.py` creates two temp dirs, runs tool on both, compares outputs.

### Negative controls (must fail)

1. **Deleted repo:** Repo URL returns 404. Tool must abstain or fail gracefully.
2. **Proprietary dependency:** `requirements.txt` contains `matlab-engine` (no PyPI). Tool must detect unresolvable dep and abstain.
3. **Hardware-specific:** Code imports `cupy` with CUDA kernel. Tool must detect hardware dep and abstain or flag.
4. **Empty repo:** No Python files, no config. Tool must abstain.

### Adversarial control (should fail)

**Version-conflict repo:** `requirements.txt` = `numpy==1.19.0\npandas==1.5.0` but code uses `pandas.DataFrame.at` (needs pandas≥2.0). Tool must detect conflict or fail at install.

### Inputs, oracle, thresholds, resource limits

- **Input corpus:** 20 A2+A3 papers from E067's population (stride sample from 1,682 papers with code links, excluding the 34 assessed). Harvested via GitHub API (authenticated, 5000 req/hr).
- **Oracle:** Clean `venv` per paper → `pip install -r generated_requirements.txt` → `python -c "import main_module; main_module.main(['--help'])"` (or equivalent entry point). Timeout: 300s install, 60s smoke test.
- **Resource limits:** 20 papers × (300s + 60s) = 2 hours max wall time. Parallelizable to 4 workers = 30 min.
- **Versions:** Python 3.8.10 (match E067), pip 24.x, GitHub API authenticated.
- **Seeds:** Fixed stride (every 84th paper from sorted-by-date list) for reproducibility.

### Reproduction command

```bash
cd EXPERIMENTS/079-arxiv-reproducibility
python3 witness.py          # Information-sufficiency witness (must pass before run.py)
python3 run.py --sample 20 --gate
```

### Evidence labels

- `observed`: Harvested paper metadata, install/smoke test results, witness outcome
- `inferred`: Version constraints from import analysis
- `speculative`: Full computational reproducibility from smoke test
- `untested`: Adoption, usefulness, commercial viability