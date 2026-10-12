# E108 — View-count principle on Packagist (PHP/Composer package registry)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

## Objective

Test whether the view-count principle generalizes to Packagist, the package registry for PHP/Composer. The principle states that **need-related packages** (packages addressing common programming needs like web frameworks, HTTP clients, database drivers, etc.) have systematically higher activity metrics (downloads) than **random packages**.

## Background

The view-count principle has been tested on:
- **PyPI (E071)**: WORKS — need-related 82.93% active vs random 57.50%, all gates pass
- **NPM (E072)**: WORKS — 100% need-related active vs 0% random
- **Maven Central (E090)**: FAILS — activity-rate difference not significant (60% vs 52.2%)
- **crates.io (E095)**: FAILS — all crates active (100%), no binary discrimination
- **NuGet (E102)**: WORKS — strong significance (p=1.7e-14, Cliff's delta=0.996)
- **Hugging Face Hub (E101)**: FAILS — download dynamics differ, signal too weak
- **Hex.pm (E103)**: WORKS — all gates pass, p≈0.000, Cliff's δ=0.861, need median 220× random
- **GitHub repos (E107)**: WORKS — all gates pass, need median 8.6× random, Cliff's δ=0.826

Packagist is a **major untested ecosystem** (PHP/Composer) with:
- Download counts: `total`, `monthly`, `daily`
- Search API with keyword filtering
- Default listing for random packages
- Large ecosystem with ~467,000+ packages
- Mature, widely-used in production (Laravel, Symfony, etc.)

## Hypothesis

**H1**: Need-related packages on Packagist have significantly higher monthly download counts than random packages.

**H0**: No significant difference in monthly download counts between need-related and random packages.

## Gates (per E071/E090/E095/E102/E103 protocol)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 100 total (50 per group minimum) |
| G2 | Need-related active rate > random active rate | Mann-Whitney U test, p < 0.05, Cliff's delta > 0.147 |
| G3 | Effect size | Wilson CI95 lower bound for proportion of need-related above random median > 0.60 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

**Active definition**: A package is "active" if its `monthly` download count > 0. This follows E095/E102/E103 precedent where the activity signal is the time-windowed download metric. Monthly is chosen as the primary metric (more stable than daily, more current than total).

**Need classification**: Following E071/E078/E103 framework. A package is `need-related` iff its description/metadata contains at least one term from `NEED_INDICATORS` and does NOT contain any term from `GENERIC_TERMS`.

```python
NEED_INDICATORS = {
    "web", "rest", "api", "http", "client", "server", "framework",
    "database", "orm", "sql", "postgres", "mysql", "redis", "mongo",
    "json", "xml", "yaml", "parser", "serializer", "encoder", "decoder",
    "auth", "oauth", "jwt", "session", "cookie", "security",
    "cache", "queue", "worker", "job", "background", "async",
    "test", "mock", "fixture", "benchmark", "profile",
    "config", "settings", "env", "environment", "secret",
    "logger", "logging", "telemetry", "metrics", "tracing",
    "email", "mail", "smtp", "notification", "push",
    "file", "storage", "upload", "download", "archive",
    "image", "video", "audio", "media", "thumbnail",
    "search", "index", "elasticsearch", "fulltext",
    "graphql", "grpc", "websocket", "realtime", "pubsub",
    "crypto", "hash", "encrypt", "decrypt", "sign", "verify",
    "validate", "validator", "schema", "contract",
    "template", "render", "view", "html", "css", "asset",
    "router", "routing", "dispatch", "handler", "middleware",
    "dependency", "injection", "container", "provider",
    "cli", "command", "argument", "flag", "option",
    "migration", "schema", "seed", "factory",
    "pubsub", "broadcast", "channel", "presence",
    # PHP-specific terms
    "laravel", "symfony", "laminas", "zend", "slim", "lumen",
    "doctrine", "eloquent", "propel", "atlas",
    "guzzle", "httplug", "php-http", "buzz",
    "monolog", "psr/log", "psr/cache", "psr/container",
    "phpunit", "mockery", "phpspec", "behat",
    "twig", "blade", "latte", "smarty",
    "composer", "packagist", "satis",
    "flysystem", "league", "spatie",
    "carbon", "nesbot", "brick",
    "ramsey", "uuid", "ulid",
    "vlucas", "phpdotenv", "dotenv",
    "swiftmailer", "mailer", "sendmail",
    "fzaninotto", "faker", "factory",
    "sebastian", "code-coverage", "php-code-coverage",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "demo", "example", "sample", "test", "testing",
    "skeleton", "boilerplate", "starter", "template",
}
```

## Methodology

1. **Need-related sample**: Search Packagist API with need-indicator keywords (e.g., "web framework", "http client", "database", "auth", "cache", "queue", "json", "logger", "config", "test"). Collect up to 100 packages.

2. **Random sample**: Fetch packages from default package list (alphabetical/default sort) across multiple pages. Collect up to 100 packages.

3. **Classification**: Apply need classification to all collected packages. Keep only those confidently classified as `need-related` or `random`.

4. **Activity measurement**: For each package, record `monthly` download count from the package detail API.

5. **Gate evaluation**: Compute active rates (monthly > 0), run Mann-Whitney U test, compute Cliff's delta, Wilson CI95.

## API Endpoints

- Package list: `https://packagist.org/packages/list.json` (all package names)
- Search: `https://packagist.org/search.json?q={query}` (returns top ~15 results)
- Package detail: `https://packagist.org/packages/{name}.json` (includes downloads, favers, dependents, github_stars)

Note: The search API returns limited results (~15). For need-related collection, we'll use multiple search queries. For random collection, we'll sample from the full package list.

## Success Criteria

All four gates (G1-G4) must pass for the principle to be considered supported on Packagist.

## Falsification

If G2 fails (p ≥ 0.05 or Cliff's delta ≤ 0.147) OR G3 fails (Wilson LB ≤ 0.60), the principle does not generalize to Packagist under this measurement.

## Deliverables

- `collect.py` — Data collection script
- `analyze.py` — Gate evaluation script
- `results.json` — Raw results with gate outcomes
- `README.md` — Experiment summary