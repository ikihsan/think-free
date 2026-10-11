# E097 — View-count principle on GitHub pyproject.toml presence

<!-- origin-meta
owner: EXPERIMENTS/097-pyproject-toml
status: active
last-verified: 2026-10-11
-->

## Question

Can the view-count principle generalize to a measurement of Python package metadata format adoption? Specifically: what fraction of Python packages on GitHub have a `pyproject.toml` file (indicating use of PEP 517/518 modern build system), and does the presence of `pyproject.toml` correlate with "need-related" package characteristics?

## Population

**Denominator**: A sample of Python packages fetched from GitHub via the GitHub API, searching for repositories containing Python code.

**Numerator**: Python packages classified as `need-related` — those whose description or topic indicates a specific problem/domain where a library would be sought, AND that have a `pyproject.toml` file.

## Instrument

### Data Fetch

Query GitHub Search API for Python repositories:

```
https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=100
```

Fetch at minimum 100 repositories (G2 gate). Each repository includes:
- `full_name`, `description`, `language`
- `topics` (list)
- `html_url`, `stargazers_count`, `forks_count`
- `open_issues_count`, `default_branch`
- Optionally: file contents via `github API /contents` endpoint

### Classification Rule

A repository is `need-related` iff its description or topics contain at least one term from a predefined set of problem-domain indicators.

**Need-related indicators** (examples):
- `api`, `client`, `server`, `framework`, `engine`, `core`, `utility`, `helper`
- Domain-specific: `web`, `rest`, `mvc`, `orm`, `sql`, `json`, `xml`, `http`
- Functional: `parser`, `lexer`, `encoder`, `decoder`, `converter`, `transform`
- Application type: `gui`, `cli`, `webapp`, `framework`, `library`, `tool`

**Excluded terms** (too generic):
- `utils`, `common`, `api` (when alone), `core`, `library`, `framework` (when alone), `jar`, `dependencies`

A repository is `random` if it does not meet the `need-related` criteria.

### Metric

**pyproject.toml adoption rate**: proportion of `need-related` Python packages that have a `pyproject.toml` file at the repository root.

**Baseline random rate**: proportion of `random` Python packages that have a `pyproject.toml` file.

G4 (sample-size): at least 30 repositories classified for the rate to be meaningful.

## Kill Gates

**G1**: If the `pyproject.toml` adoption rate of `need-related` packages is under **10 percentage points** higher than the `random` baseline rate, **close the line**. Need-related Python packages do not systematically adopt modern build system metadata, and the measurement principle does not generalize to this correlation.

**G2**: Must sample at least **50** repositories total for the rate to be meaningful.

**G3**: Each of at least **2** separate API fetches must contribute classified repositories to avoid fetch bias.

**G4**: At least **30** repositories must be classified total.

## Reproduction

```bash
cd EXPERIMENTS/097-pyproject-toml
python3 run.py --gate
```

## Hypothesis

Need-related Python packages on GitHub will show a higher `pyproject.toml` adoption rate than random packages, consistent with the view-count principle's generalizability to code repository metadata. Expected outcome: need-related packages adopt `pyproject.toml` at a rate at least 10pp above random, supporting the principle's broader applicability.