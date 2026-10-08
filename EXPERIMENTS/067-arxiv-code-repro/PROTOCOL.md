<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E067 — Do ArXiv computational papers with code links provide runnable environments?

## Question

Researchers routinely link code repositories from ArXiv papers, but the computational environment (dependencies, versions, OS, hardware) is often underspecified. A paper's results may not be reproducible because the environment cannot be reconstructed. This experiment measures how many papers with code links actually provide machine-readable, runnable environment specifications.

## Population

ArXiv papers from **2024-01-01 to 2024-12-31** in categories:
- `cs.LG` (Machine Learning)
- `cs.AI` (Artificial Intelligence)
- `stat.ML` (Machine Learning)
- `physics.comp-ph` (Computational Physics)
- `cs.CV` (Computer Vision)
- `cs.CL` (Computation and Language)

That declare a **code repository link** in their ArXiv metadata (the `journal-ref` or `comments` field often contains "Code: https://github.com/...").

Stride sample: every 50th paper from the API results, targeting ~200 papers total across categories.

## Method

For each sampled paper:

1. **Fetch metadata** via ArXiv API (OAI-PMH or search API).
2. **Extract code URL** from `comments`, `journal-ref`, or `doi` fields using regex for GitHub/GitLab/Bitbucket URLs.
3. **Fetch repository** metadata via GitHub API (public repos only, no auth needed for metadata).
4. **Check for environment specification files** in the default branch:
   - `Dockerfile*`, `docker-compose*.yml`, `.devcontainer/`
   - `environment.yml`, `environment.yaml`, `conda.yml`
   - `requirements*.txt`, `setup.py`, `pyproject.toml`, `Pipfile`, `poetry.lock`, `uv.lock`
   - `README*` with setup/install instructions (heuristic: contains "install", "setup", "requirements", "dependencies", "conda", "docker", "pip install")
5. **Assess runnability** of each found spec:
   - **Docker**: Has `FROM` with specific base image tag (not `latest`), and dependency installation commands with pinned versions.
   - **Conda**: `environment.yml` with `dependencies:` listing packages with versions (e.g., `python=3.10`, `pytorch=2.0`).
   - **Pip**: `requirements.txt` or `pyproject.toml` where **all** dependencies have pinned versions (`==`, not `>=` or bare).
   - **README only**: Counted as "documentation only" — not machine-readable.

## Arms

| Arm | Definition |
|-----|------------|
| **A1** | Paper has code link AND repo has **machine-runnable spec** (Dockerfile with pinned base + pinned deps, OR conda env with pinned versions, OR pip requirements all pinned) |
| **A2** | Paper has code link AND repo has **partial spec** (Dockerfile without pinned base, OR conda env with some unpinned, OR requirements.txt with some unpinned) |
| **A3** | Paper has code link AND repo has **documentation only** (README with install instructions, no machine-readable spec) |
| **A4** | Paper has code link AND repo has **no environment info** (no Dockerfile, no conda, no requirements, no README install section) |
| **A5** | Paper has **no code link** (control) — checked for any environment spec in linked supplementary materials |

## Kill Gates (predeclared)

| Gate | Condition | Verdict if met |
|------|-----------|----------------|
| **K1** (population) | < 20 papers with code links found in sample | **KILL** — population too small to measure |
| **K2** (severity) | **A1 / (A1+A2+A3+A4) ≥ 0.50** — ≥50% of code-linked papers provide machine-runnable specs | **KILL** — problem not severe; environment capture is already common practice |
| **K3** (differentiation) | **A4 / (A1+A2+A3+A4) ≤ 0.10** — ≤10% have no environment info at all | **KILL** — the "no info" tail is too small to build for |
| **K4** (baseline) | A5 (no-code-link papers) has **higher** runnable-spec rate than code-link papers | **KILL** — code links don't correlate with better environment capture |

## Instrument Falsifiability

The assessment of "pinned versions" is deterministic:
- `requirements.txt`: every line matching `^[a-zA-Z0-9_-]+==` counts as pinned; `>=`, `<=`, `~=`, bare name = unpinned.
- `environment.yml`: every dependency line with `=` followed by version (e.g., `python=3.10.12`) counts as pinned; bare name = unpinned.
- `Dockerfile`: `FROM` line with explicit tag (not `latest`, not bare) + `RUN pip install pkg==X.Y.Z` or `apt-get install pkg=X.Y.Z` patterns.

A test suite asserts the classifier returns known values for synthetic fixtures.

## Reproduction

```bash
python3 EXPERIMENTS/067-arxiv-code-repro/fetch.py      # fetch ArXiv metadata, extract code URLs
python3 EXPERIMENTS/067-arxiv-code-repro/assess.py     # assess repos for environment specs
python3 EXPERIMENTS/067-arxiv-code-repro/report.py     # compute arm counts, apply kill gates
python3 -m unittest discover -s EXPERIMENTS/067-arxiv-code-repro -t EXPERIMENTS/067-arxiv-code-repro -p 'test_*.py'
```