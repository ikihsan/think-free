# E116 — View-count classifier prototype (coverage & matched harvest)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Objective

Build and validate a classifier for the view-count principle that declares and achieves a **coverage floor** before measuring effect size. This directly addresses the binding constraint identified by E113/F116: the shared classifier only labelled 196 of 700 rows (28%), with 458 matching neither vocabulary.

The prototype must satisfy three conditions before effect-size claims are valid:

1. **A classifier that covers its population** — ≥80% of a representative pool must be classifiable as need-related or random (declared floor before the run).
2. **A coverage gate declared before the run** — the fraction of the population the labeler assigns at all, with a floor; no experiment on this line had one, which is how a 28% screen came to be reported as a 100% measurement.
3. **A matched harvest as the default design** — need and random arms drawn from the same pool, sorted by the same metric, with only the label differing.

## Hypothesis

**H1**: A classifier with whole-word matching, expanded vocabulary, and contextual heuristics can classify ≥80% of a representative package pool, and need-related packages will have significantly higher recent download counts than random packages.

**H0**: The classifier covers <80% of the pool, OR need-related and random packages have indistinguishable download counts under a matched harvest design.

## Gates (per E071/E078/E102 protocol, extended)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 100 total (50 per group minimum) |
| G2 | Coverage floor | ≥80% of the representative pool classified (need-related + random) |
| G3 | Effect size | Mann-Whitney U test, p < 0.05, Cliff's delta > 0.147 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

## Need Indicators (expanded & disambiguated)

```python
NEED_INDICATORS = {
    # Web infrastructure
    "web", "rest", "api", "http", "client", "server", "framework",
    # Database & storage
    "database", "orm", "sql", "postgres", "mysql", "mariadb", "redis",
    "mongo", "mongodb", "elasticsearch", "couchdb", "storage", "cache",
    "persistent", "session", "state",
    # Authentication & security
    "auth", "oauth", "oidc", "jwt", "session", "cookie", "security",
    "encrypt", "decrypt", "sign", "verify", "validator", "schema",
    # Networking & communication
    "socket", "tcp", "udp", "http", "rest", "grpc", "websocket",
    "pubsub", "messaging", "queue", "topic", "broker", "channel",
    # Testing & CI
    "test", "mock", "fixture", "benchmark", "profile", "fuzz",
    "continuous", "integration", "deployment",
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
    # Core computing (always generic)
    "utils", "common", "core", "library", "package", "tool", "util",
    "helper", "helper", "helper",
    # Language-agnostic infrastructure (always generic)
    "ci", "build", "builder", "compile", "runtime", "debug",
    "example", "demo", "tutorial", "learning", "workshop",
    # Vague qualification
    "personal", "private", "internal", "custom", "fork", "mirror",
    "copy", "backup", "archive", "old", "deprecated", "legacy",
    "unmaintained", "abandoned",
}
```

**Disambiguation rule**: A term from NEED_INDICATORS that also appears in GENERIC_TERMS is only counted if it carries need-specific context (e.g., `cache` as in "cache layer" vs. `cache` as in "utils"). Context is determined by nearby tokens: if any other NEED_INDICATOR appears within the same token window (3 tokens left/right), the term is retained as need-specific.

## Matched Harvest Design

1. **Single pooled pool**: Draw all candidate packages from a single source (e.g., Hex.pm API, or PyPI JSON API).
2. **Stratified splitting**: Split the pool into need-related and random arms using the classifier. The classifier's label determines the arm.
3. **Matched sorting**: Within each arm, sort by the same metric (recent download count). The matched design means we compare the distribution of need-related vs. random packages that exist in the same overall pool — eliminating the asymmetric harvest defect where need and random arms were drawn from different queries/topics.
4. **Coverage measurement**: Before effect-size measurement, compute the classification rate: `(need-related + random classified) / total pool`. This must meet the ≥80% floor (G2).

If G2 fails, the experiment stops — effect size (G3) cannot be meaningfully measured without coverage of the population.

## Activity Definition

A package is "active" if its `recent` (30-day) download count > 0. This follows E095/E102 precedent where the activity signal is the time-windowed download metric.

## API Endpoints (Hex.pm example)

- Search: `https://hex.pm/api/packages?search={query}&sort=downloads&page={n}`
- Random: `https://hex.pm/api/packages?page={n}` (default sort, no search query)
- Package detail: `https://hex.pm/api/packages/{name}` (includes downloads, metadata)

## Success Criteria

All four gates (G1-G4) must pass for the classifier prototype to be validated as a drop-in replacement for the unanchored-substring matcher.

If G2 (coverage floor) fails, the experiment is documented as a coverage limitation, not a principle failure. The classifier is improved and re-run.

## Falsification

If G1 fails (insufficient sample), G2 fails (coverage <80%), or G3 fails (p ≥ 0.05 or Cliff's delta ≤ 0.147), the classifier prototype is not validated under this measurement. If G4 fails (one arm empty), the vocabulary or matching strategy is imbalanced.

## Deliverables

- `collect.py` — Data collection script (matched harvest from single pool)
- `classify.py` — Classifier with whole-word matching, expanded vocabulary, contextual disambiguation, and coverage reporting
- `analyze.py` — Gate evaluation: coverage floor, effect size, Cliff's delta, Wilson CI95
- `results.json` — Raw results with gate outcomes and coverage metrics
- `README.md` — Experiment summary