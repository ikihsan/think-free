# E117 — View-count classifier prototype v3 (coverage & matched harvest)

<!-- origin-meta
owner: docs/INDEX.md
status: planning
last-verified: 2026-10-14
-->

## Objective

Build and validate a classifier for the view-count principle that:
1. Achieves a **coverage floor** ≥80% of a representative pool (addressing the E113/E107 limitation where the shared classifier only labelled 196/700 rows = 28% due to unanchored substring matching).
2. Demonstrates a **statistically significant effect size** (Cliff's delta > 0.147, Mann-Whitney U p < 0.05), addressing the E116 v1 limitation where δ = 0.0265 on Hex.pm.
3. Tests on a **previously untried platform with exposable metadata** (CRAN R packages), extending the methodology across 12+ domains.

This prototype directly addresses the two binding constraints identified across the view-count line: (a) classifier coverage floor, and (b) effect size magnitude.

## Scope

- **Platform**: CRAN (The Comprehensive R Archive Network), R package registry
- **Pool size**: 200 packages (random sample + need-related query), matched harvest design
- **Metric**: Recent (30-day) download count from CRAN API
- **Comparison**: Need-related vs. random packages within the same pooled population

The classifier must satisfy all four gates before effect-size claims are valid.

## Hypothesis

**H1**: A classifier with whole-word token matching, R-specific expanded vocabulary, and contextual disambiguation can classify ≥80% of a representative CRAN package pool as need-related or random, AND need-related packages will have significantly higher recent download counts than random packages (Cliff's delta > 0.147, p < 0.05).

**H0**: The classifier covers <80% of the pool, OR need-related and random packages have indistinguishable download counts under a matched harvest design.

## Gates (per protocol, extended from E116)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 100 total (50 per group minimum) |
| G2 | Coverage floor | ≥80% of the representative pool classified (need-related + random) |
| G3 | Effect size | Mann-Whitney U test, p < 0.05, Cliff's delta > 0.147 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

If G2 fails, the experiment stops — effect size (G3) cannot be meaningfully measured without coverage of the population.

If G3 fails despite G2 passing, the classifier prototype is not validated under this measurement. The vocabulary or matching strategy is improved and re-run.

## Need Indicators (R-specific expansion)

```python
NEED_INDICATORS = {
    # Web infrastructure
    "web", "rest", "api", "http", "client", "server", "framework",
    "shiny", "rmarkdown", "knitr", "latex",
    # Database & storage
    "database", "orm", "sql", "postgres", "mysql", "mariadb", "redis",
    "mongo", "mongodb", "elasticsearch", "couchdb", "storage", "cache",
    "persistent", "session", "state",
    # Authentication & security
    "auth", "oauth", "oidc", "jwt", "session", "cookie", "security",
    "encrypt", "decrypt", "sign", "verify", "validator", "schema",
    "passport", "token",
    # Networking & communication
    "socket", "tcp", "udp", "http", "rest", "grpc", "websocket",
    "pubsub", "messaging", "queue", "topic", "broker", "channel",
    "plumber", "httpuv",
    # Testing & CI
    "test", "mock", "fixture", "benchmark", "profile", "fuzz",
    "continuous", "integration", "deployment",
    "reticulate", "cran", "github",
    # Package metadata disambiguation
    # Explicitly excluded from GENERIC_TERMS when they carry need-specific meaning
}
```

```python
GENERIC_TERMS = {
    # Truly generic, always disqualifying (when found alone without need-specific context)
    "base", "minimal", "alpine", "scratch", "distroless", "slim",
    "latest", "stable", "edge", "main", "master", "dev", "test",
    "example", "demo", "sample", "template", "boilerplate",
    "sandbox", "playground", "poc", "prototype", "experiment",
    # Core R computing (always generic)
    "r-base", "rstats", "cran", "github", "pkg", "package",
    "library", "func", "fun", "helper", "utils", "core",
    # Language-agnostic infrastructure (always generic)
    "ci", "build", "builder", "compile", "runtime", "debug",
    "example", "demo", "tutorial", "learning", "workshop",
    # Vague qualification
    "personal", "private", "internal", "custom", "fork", "mirror",
    "copy", "backup", "archive", "old", "deprecated", "legacy",
    "unmaintained", "abandoned",
    # R-specific generics
    "tidy", "verse", "purrr", "dplyr", "ggplot", "readr",
    "write", "read", "df", "dt", "dtypes",
}
```

**Disambiguation rule**: A term from NEED_INDICATORS that also appears in GENERIC_TERMS is only counted if it carries need-specific context (e.g., `cache` as in "cache layer" vs. `cache` as in "utils"). Context is determined by nearby tokens: if any other NEED_INDICATOR appears within the same token window (3 tokens left/right), the term is retained as need-specific.

## Matched Harvest Design

1. **Single pooled pool**: Draw all candidate packages from the CRAN API (`https://cran.r-project.org/packages`).
2. **Stratified splitting**: Split the pool into need-related and random arms using the classifier. The classifier's label determines the arm.
3. **Matched sorting**: Within each arm, sort by the same metric (recent 30-day download count). The matched design means we compare the distribution of need-related vs. random packages that exist in the same overall pool — eliminating the asymmetric harvest defect where need and random arms were drawn from different queries/topics.
4. **Coverage measurement**: Before effect-size measurement, compute the classification rate: `(need-related + random classified) / total pool`. This must meet the ≥80% floor (G2).

If G2 fails, the experiment is documented as a coverage limitation, not a principle failure. The classifier is improved and re-run.

## Activity Definition

A package is "active" if its `recent` (30-day) download count > 0. This follows E095/E102 precedent where the activity signal is the time-windowed download metric.

## API Endpoints (CRAN example)

- Package search/listing: `https://cran.r-project.org/packages`
- Package detail: `https://cran.r-project.org/packages/{name}` (includes downloads, description, title)
- Random packages: sorted by reverse-alphabetical or by download count from the search results page

## Success Criteria

All four gates (G1-G4) must pass for the classifier prototype to be validated as a drop-in replacement for the unanchored-substring matcher and as a meaningful advance on the E116 v1 result (δ = 0.0265).

If G2 (coverage floor) fails, the experiment is documented as a coverage limitation, not a principle failure. The classifier is improved and re-run.

If G3 (effect size) fails despite G2 passing, the classifier vocabulary or matching strategy is improved and re-run.

## Falsification

If G1 fails (insufficient sample), G2 fails (coverage <80%), or G3 fails (p ≥ 0.05 or Cliff's delta ≤ 0.147), the classifier prototype is not validated under this measurement. If G4 fails (one arm empty), the vocabulary or matching strategy is imbalanced.

If both G2 and G3 fail after three re-runs with improved vocabularies, the view-count principle is falsified for this platform, and the experiment documents the boundary conditions.

## Deliverables

- `collect.py` — CRAN data collection script (matched harvest from single pool, extracts package names, descriptions, recent download counts)
- `classify.py` — Classifier with whole-word token matching, R-specific expanded vocabulary, contextual disambiguation, and coverage reporting
- `analyze.py` — Gate evaluation: coverage floor, effect size, Cliff's delta, Wilson CI95
- `results.json` — Raw results with gate outcomes and coverage metrics
- `PROTOCOL.md` — Experiment summary (this file)
- `README.md` — Experiment summary

---