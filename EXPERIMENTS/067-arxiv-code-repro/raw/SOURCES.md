<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E067 Data Sources

## ArXiv OAI-PMH Harvest

- **Endpoint**: `http://export.arxiv.org/oai2`
- **Verb**: `ListRecords`
- **Metadata Prefix**: `arXiv`
- **Sets**: `arXiv:cs.LG`, `arXiv:cs.AI`, `arXiv:stat.ML`, `arXiv:physics.comp-ph`, `arXiv:cs.CV`, `arXiv:cs.CL`
- **Date Range**: `2024-01-01` to `2024-12-31`
- **Harvest Date**: 2026-10-08
- **Sampling**: Stride of 50 (every 50th record)

## Code URL Extraction

Regex patterns applied to `comments`, `journal-ref`, `doi`, and `abstract` fields:
1. `(?:code|github|gitlab|bitbucket)[:\s]*(https?://(?:github|gitlab|bitbucket)\.com/[\w\-]+/[\w\-\.]+)`
2. `(https?://(?:github|gitlab|bitbucket)\.com/[\w\-]+/[\w\-\.]+)`

## GitHub API Assessment

- **Endpoint**: `https://api.github.com`
- **Authentication**: Unauthenticated (public repos only)
- **Rate Limit**: 60 requests/hour (unauthenticated)
- **Data Retrieved**:
  - Repository tree (recursive) for file listing
  - File contents for: Dockerfile*, environment.yml, requirements*.txt, pyproject.toml, README*

## Classifier Definitions

### Dockerfile
- **Pinned base**: `FROM` with explicit tag (not `latest`, not bare)
- **Pinned deps**: `RUN pip install pkg==X.Y.Z` or `apt-get install pkg=X.Y.Z`

### Conda environment.yml
- **Pinned**: Dependency line contains `=` followed by version digit (e.g., `python=3.10.12`)

### Pip requirements.txt / pyproject.toml
- **Pinned**: Line contains `==` version specifier
- **Unpinned**: Bare name, `>=`, `<=`, `~=`, `^`, `>`, `<`

### README
- **Has install instructions**: Contains any of: `install`, `setup`, `requirements`, `dependenc`, `conda`, `docker`, `pip install`, `poetry install`, `uv sync`

## Arm Classification Rules

| Env Spec Type | Arm | Condition |
|---------------|-----|-----------|
| docker, conda, pip | A1 | pinned_score ≥ 0.8 |
| docker_partial, conda_partial, pip_partial, lockfile_only | A2 | pinned_score > 0 and < 0.8 |
| readme | A3 | README has install keywords |
| none | A4 | No environment files found |

## Known Limitations

1. **GitHub API rate limits** - Unauthenticated requests limited to 60/hour; large samples may need pacing or authentication
2. **Private repositories** - Cannot assess private repos; counted as "no tree" / A4
3. **Non-GitHub hosts** - GitLab, Bitbucket not fully supported in assessment (only GitHub API used)
4. **Default branch assumption** - Assumes `main` then `master`; other branch names missed
5. **Monorepo detection** - Does not detect environment specs in subdirectories
6. **Dynamic dependencies** - Cannot detect dependencies installed via scripts, Makefiles, or CI configs