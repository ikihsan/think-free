# E104 — CI/CD adoption on PyPI

<!-- origin-meta
owner: EXPERIMENTS/104-ci-adoption
status: active
last-verified: 2026-10-11
-->

## Question

Can the rate of Python packages with CI/CD configuration be measured on PyPI, and do "need-related" packages have a higher CI/CD adoption rate than "random" packages? This is a fresh observation in the PyPI domain, different from E071 (which classified packages as "active" vs "random" based on metadata activity level) and from the view-count principle experiments (which focused on Q&A tag domains).

## Population

**Denominator**: A sample of Python packages with known CI/CD status, using a hardcoded list of well-known Python packages.

**Numerator**: Python packages classified as `need-related` — those whose description or keywords indicate a specific problem/domain where a library would be sought.

## Instrument

### Data Fetch

A hardcoded list of well-known Python packages with their CI/CD configuration status:

### Classification Rule

A package is `need-related` iff its description or keywords contain at least one term from a predefined set of problem-domain indicators.

**Need-related indicators** (description or keywords contains at least one):
- `api`, `client`, `server`, `framework`, `engine`, `core`, `utility`, `helper`
- Domain-specific: `web`, `rest`, `mvc`, `orm`, `sql`, `json`, `xml`, `http`
- Functional: `parser`, `lexer`, `encoder`, `decoder`, `converter`, `transform`
- Application type: `gui`, `cli`, `webapp`, `framework`, `library`, `tool`

**Excluded terms** (too generic, always classified as `random`):
- `utils`, `common`, `api` (when alone), `core`, `library`, `framework` (when alone), `jar`, `dependencies`

A package is `random` if it does not meet the `need-related` criteria.

### Metric

**CI/CD adoption rate**: proportion of `need-related` packages that have a CI/CD configuration file (`.github/workflows/`, `.travis.yml`, `.circleci/config.yml`, `azure-pipelines.yml`, `appveyor.yml`).

**Baseline random rate**: proportion of `random` packages with CI/CD configuration.

G4 (sample-size): at least 30 packages classified for the rate to be meaningful.

## Kill Gates

**G1**: If the CI/CD adoption rate of `need-related` packages is under **10 percentage points** higher than the `random` baseline rate, **close the line**. Need-related Python packages do not systematically adopt CI/CD at a higher rate, and this measurement does not generalize to CI/CD patterns.

**G2**: Must sample at least **50** packages total for the rate to be meaningful.

**G3**: Each of at least **2** separate fetches must contribute classified packages to avoid fetch bias.

**G4**: At least **30** packages must be classified total.

## Reproduction

```bash
cd EXPERIMENTS/104-ci-adoption
python3 run.py --gate
```

## Hypothesis

Need-related Python packages on PyPI will show a higher CI/CD adoption rate than random packages, consistent with the expectation that packages addressing practical needs are more likely to have automated testing and CI pipelines. Expected outcome: need-related packages adopt CI/CD at a rate at least 10pp above random, supporting broader applicability of CI/CD metrics as a measure of project health.