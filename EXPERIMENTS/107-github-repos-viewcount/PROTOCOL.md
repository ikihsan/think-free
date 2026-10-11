<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E107 — View-count principle on GitHub code repositories

## Objective

Test whether the view-count principle generalizes to GitHub code repositories. The principle states that **need-related repositories** (repositories addressing common programming needs like web frameworks, databases, auth, caching, etc.) have systematically higher activity metrics (stars, forks, recent activity) than **random repositories**.

## Background

The view-count principle has been tested on:
- **PyPI (E071)**: WORKS — need-related 82.93% active vs random 57.50%, all gates pass
- **NPM (E072)**: WORKS — 100% need-related active vs 0% random
- **NuGet (E102)**: WORKS — strong significance (p=1.7e-14, Cliff's δ=0.996)
- **Hex.pm (E103)**: WORKS — all gates pass, p≈0.000, Cliff's δ=0.861, need median 220× random
- **Maven Central (E090)**: FAILS — activity-rate difference not significant (60% vs 52.2%)
- **crates.io (E095)**: FAILS — all crates active (100%), no binary discrimination
- **Hugging Face Hub (E101)**: FAILS — download dynamics differ, signal too weak
- **CPAN (E0xx)**: WORKS — all gates pass, need-related 94.5% vs random 86.5%
- **Code Review Stack Exchange (E100)**: WORKS — all gates pass, 73.3% unserved need rate

Previous small GitHub repository experiments (0xx-github-repo-*) failed G1 due to insufficient sample size (10-13 repos, only 1-2 need-related). This experiment uses a proper sample (≥50 repos per group) to test whether the principle generalizes to code repositories.

GitHub repositories have:
- Star counts (primary arrival metric)
- Fork counts (secondary)
- Issue counts (tertiary)
- Recent commit activity (within 30 days)
- Topics/tags for classification
- Descriptions for classification

## Hypothesis

**H1**: Need-related repositories on GitHub have significantly higher star counts than random repositories.

**H0**: No significant difference in star counts between need-related and random repositories.

## Gates (per E071/E090/E095/E102/E103 protocol)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 100 total (50 per group minimum) |
| G2 | Need-related stars > random stars | Mann-Whitney U test, p < 0.05, Cliff's delta > 0.147 |
| G3 | Effect size | Wilson CI95 lower bound for proportion of need-related above random median > 0.60 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

**Active definition**: A repository is "active" if its star count > 0 AND it has had commits in the last 365 days. This follows the precedent of time-windowed activity metrics.

**Need classification**: Following E071/E078 framework. A repository is `need-related` iff its description/topics contain at least one term from `NEED_INDICATORS` and does NOT contain any term from `GENERIC_TERMS` as a primary classifier.

```python
NEED_INDICATORS = {
    "web-framework", "web-framework", "http-server", "http-client", "api-client",
    "database", "orm", "sql", "postgresql", "mysql", "redis", "mongodb",
    "cache", "caching", "memcached", "queue", "messaging", "rabbitmq", "kafka",
    "authentication", "authorization", "oauth", "jwt", "session", "security",
    "logging", "monitoring", "observability", "tracing", "metrics", "prometheus",
    "testing", "test-framework", "mocking", "benchmarking", "profiling",
    "deployment", "ci-cd", "continuous-integration", "continuous-deployment",
    "kubernetes", "docker", "container", "microservices", "service-mesh",
    "graphql", "grpc", "websocket", "real-time", "pub-sub", "message-broker",
    "serialization", "json", "xml", "yaml", "protobuf", "avro",
    "validation", "schema", "configuration", "config", "secrets-management",
    "email", "notification", "push", "file-storage", "object-storage", "s3",
    "search", "elasticsearch", "fulltext", "machine-learning", "ml", "ai",
    "data-processing", "etl", "streaming", "data-pipeline",
    "load-balancing", "rate-limiting", "circuit-breaker", "retry", "timeout",
    "router", "routing", "middleware", "dependency-injection", "cli",
    "command-line", "argument-parsing", "template-engine", "rendering",
    "migration", "seeding", "factory", "orm", "active-record",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package", "tool", "util", "helper",
    "base", "standard", "stdlib", "internal", "private", "experimental",
    "template", "boilerplate", "scaffold", "starter", "example", "demo",
    "tutorial", "learning", "practice", "playground", "sandbox", "toy",
    "sample", "proof-of-concept", "poc", "prototype", "experiment",
}
```

## Methodology

1. **Need-related sample**: Search GitHub API with need-indicator topics (using `topic:` qualifier). Collect up to 100 repositories.
2. **Random sample**: Search GitHub API with generic topics. Collect up to 100 repositories.
3. **Classification**: Apply need classification to all collected repositories. Keep only those confidently classified as `need-related` or `random`.
4. **Activity measurement**: For each repo, record star count, fork count, issue count, last push date.
5. **Gate evaluation**: Compute active rates (stars > 0 and recent commits), run Mann-Whitney U test on star counts, compute Cliff's delta, Wilson CI95.

## API Endpoints

- Search repos: `https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=100`
- Repo details: `https://api.github.com/repos/{owner}/{repo}`

Rate limit: 60 requests/hour unauthenticated, 5000/hour authenticated.

## Success Criteria

All four gates (G1-G4) must pass for the principle to be considered supported on GitHub repositories.

## Falsification

If G2 fails (p ≥ 0.05 or Cliff's delta ≤ 0.147) OR G3 fails (Wilson LB ≤ 0.60), the principle does not generalize to GitHub repositories under this measurement.

## Deliverables

- `harvest.py` — Data collection script
- `analyze.py` — Gate evaluation script
- `results.json` — Raw results with gate outcomes
- `README.md` — Experiment summary