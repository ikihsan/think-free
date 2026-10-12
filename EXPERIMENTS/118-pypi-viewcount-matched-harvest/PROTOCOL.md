# E118 — PyPI view-count matched-harvest experiment

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Objective

Test the view-count principle on PyPI using a **matched harvest design** that eliminates the asymmetric harvest defect identified by E113/F116. The principle is: need-related packages have significantly higher recent download counts than random packages. The matched harvest design ensures need-related and random arms are drawn from the same pool, sorted by the same metric, with only the label differing.

This directly addresses the binding constraint from E113/F116: previous "ALL GATES PASS" results used an asymmetric harvest (need arm and random arm drawn from different queries/topics, sorted by the outcome metric), which produces artifactual effects. Under a matched harvest, the effect should either replicate or collapse — providing a clean answer.

## Hypothesis

**H1**: On PyPI, need-related packages (as classified by the E116 whole-word matcher) have significantly higher recent download counts than random packages from the same pool, under a matched harvest design (H0: no significant difference, δ ≤ 0.147).

**H0**: After matching the harvest, need-related and random packages have indistinguishable download counts (Cliff's delta ≤ 0.147, p ≥ 0.05).

## Gates (per E071/E078/E102/E116 protocol, extended for matched harvest)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 50 need-related AND ≥ 50 random packages |
| G2 | Coverage floor | ≥80% of the representative pool classified (weight ≥ 0.5) |
| G3 | Effect size (matched harvest) | Mann-Whitney U p < 0.05 AND Cliff's delta > 0.147 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

## Matched Harvest Design

1. **Single pooled pool**: Collect all packages from a single PyPI search/query source.
2. **Classify and split**: Classify each package as "need-related" or "random" using the E116 classifier. The classifier's label determines the arm.
3. **Matched sorting**: Within each arm, sort by recent (30-day) download count. The matched design means we compare the distribution of need-related vs. random packages that exist in the same overall pool — eliminating the asymmetric harvest defect.
4. **Coverage measurement**: Before effect-size measurement, compute the classification rate: `(need-related + random classified) / total pool`. This must meet the ≥80% floor (G2).
5. If G2 fails, stop — effect size (G3) cannot be meaningfully measured without population coverage.

## Need Indicators (from E116, with PyPI-specific terms)

```python
NEED_INDICATORS = {
    # Web infrastructure
    "web", "rest", "api", "http", "client", "server", "framework",
    # Database & storage
    "database", "orm", "sql", "postgres", "mysql", "mariadb", "redis",
    "mongo", "mongodb", "elasticsearch", "couchdb", "storage", "cache",
    "persistent", "state",
    # Authentication & security
    "auth", "oauth", "oidc", "jwt", "session", "cookie", "security",
    "encrypt", "decrypt", "sign", "verify", "validator", "schema",
    # Networking & communication
    "socket", "tcp", "udp", "http", "rest", "grpc", "websocket",
    "pubsub", "messaging", "queue", "topic", "broker", "channel",
    # Testing & CI
    "test", "mock", "fixture", "benchmark", "profile", "fuzz",
    "continuous", "integration", "deployment",
    # General programming need terms
    "cli", "command", "argument", "flag", "option",
    "migration", "schema", "seed", "factory",
    "pubsub", "broadcast", "channel", "presence",
    "exq", "oban", "quantum", "cron", "scheduler",
    "broadway", "genstage", "flow", "stream",
    "nimble", "csv", "excel", "pdf", "docx",
    "timex", "calendar", "tzdata", "chrono",
    "decimal", "money", "currency", "exchange",
    "uuid", "ulid", "nanoid", "slug", "parameterize",
    "token",
    "crypto"
}
```

## Generic Terms (always disqualifying when present alone)

```python
GENERIC_TERMS = {
    "base", "minimal", "alpine", "scratch", "distroless", "slim",
    "latest", "stable", "edge", "main", "master", "dev", "test",
    "example", "demo", "sample", "template", "boilerplate",
    "sandbox", "playground", "poc", "prototype", "experiment",
    "tutorial", "learning", "workshop",
    "personal", "private", "internal", "custom",
    "fork", "mirror", "copy", "backup", "archive", "old",
    "deprecated", "legacy", "unmaintained", "abandoned",
    "utils", "common", "core", "library", "package", "tool", "util",
    "helper",
    "ci", "build", "builder", "compile", "runtime", "debug",
    "example", "demo", "tutorial",
}
```

## Activity Definition

A package is "active" if its `recent` (30-day) download count > 0.

## API Endpoints

- Search: `https://pypi.org/search?q={query}&sort=downloads`
- Package JSON: `https://pypi.org/pypi/{name}/json`

## Success Criteria

All four gates (G1-G4) must pass for the experiment to validate the view-count principle on PyPI under a matched harvest design.

If G2 (coverage floor) fails, the experiment is documented as a coverage limitation, not a principle failure. The classifier is improved and re-run.

If G3 fails (effect size too small), this indicates the view-count principle does not generalize to PyPI under a proper design — the previous "ALL GATES PASS" results were harvest artifacts.

## Falsification

If G1 fails (insufficient sample), G2 fails (coverage <80%), or G3 fails (p ≥ 0.05 or Cliff's delta ≤ 0.147), the view-count principle is not validated on PyPI under a matched harvest design. If G4 fails (one arm empty), the vocabulary or matching strategy is imbalanced.

## Deliverables

- `collect.py` — Data collection script (matched harvest from single PyPI pool)
- `classify.py` — Classifier with whole-word matching, expanded vocabulary, contextual disambiguation, and coverage reporting
- `analyze.py` — Gate evaluation: coverage floor, effect size, Cliff's delta, Wilson CI95
- `results.json` — Raw results with gate outcomes and coverage metrics
- `README.md` — Experiment summary