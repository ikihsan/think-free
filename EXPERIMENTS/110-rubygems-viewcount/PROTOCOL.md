# E110 — View-count principle on RubyGems (Ruby package registry)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

## Objective

Test whether the view-count principle generalizes to RubyGems, the package registry for Ruby. The principle states that **need-related packages** (packages addressing common programming needs like web frameworks, HTTP clients, database drivers, etc.) have systematically higher activity metrics (downloads) than **random packages**.

## Background

The view-count principle has been tested on:
- **PyPI (E071)**: WORKS — need-related 82.93% active vs random 57.50%, all gates pass
- **NPM (E072)**: WORKS — 100% need-related active vs 0% random
- **Maven Central (E090)**: FAILS — activity-rate difference not significant (60% vs 52.2%)
- **crates.io (E095)**: FAILS — all crates active (100%), no binary discrimination
- **NuGet (E102)**: WORKS — strong significance (p=1.7e-14, Cliff's delta=0.996)
- **Hugging Face Hub (E101)**: FAILS — download dynamics differ, signal too weak
- **Hex.pm (E103)**: WORKS — all gates pass, p≈0.000, Cliff's δ=0.861, need median 220× random
- **Packagist (E108)**: WORKS — all gates pass, p<0.001, Cliff's δ=0.994, need-related 100% active vs random 26%
- **GitHub repos (E107)**: WORKS — all gates pass, need median 8.6× random, Cliff's δ=0.826

RubyGems is a **major untested ecosystem** (Ruby) with:
- Download counts: `downloads` (total), `version_downloads` (latest version)
- Search API with keyword filtering
- Large ecosystem with ~180,000+ gems
- Mature, widely-used in production (Rails, Sinatra, etc.)

## Hypothesis

**H1**: Need-related packages on RubyGems have significantly higher total download counts than random packages.

**H0**: No significant difference in total download counts between need-related and random packages.

## Gates (per E071/E090/E095/E102/E103/E108 protocol)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 100 total (50 per group minimum) |
| G2 | Need-related active rate > random active rate | Mann-Whitney U test, p < 0.05, Cliff's delta > 0.147 |
| G3 | Effect size | Wilson CI95 lower bound for proportion of need-related above random median > 0.60 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

**Active definition**: A package is "active" if its `version_downloads` (downloads of latest version) > 0. This follows E108 precedent where the activity signal is the time-windowed download metric. Since RubyGems doesn't have a direct "monthly" or "recent" field, we use `version_downloads` as the closest proxy for recent activity.

**Need classification**: Following E071/E078/E103/E108 framework. A package is `need-related` iff its description/metadata contains at least one term from `NEED_INDICATORS` and does NOT contain any term from `GENERIC_TERMS`.

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
    # Ruby-specific terms
    "rails", "sinatra", "hanami", "padrino", "roda", "cuba",
    "activerecord", "sequel", "rom", "datamapper",
    "sidekiq", "resque", "delayed_job", "que", "good_job",
    "devise", "warden", "omniauth", "clearance", "authlogic",
    "pundit", "cancancan", "rolify",
    "rspec", "minitest", "cucumber", "capybara", "factory_bot",
    "pry", "byebug", "debug",
    "rubocop", "reek", "flog", "flay",
    "capistrano", "mina", "vlad",
    "whenever", "rufus-scheduler", "clockwork",
    "paperclip", "carrierwave", "shrine", "activestorage",
    "kaminari", "will_paginate", "pagy",
    "redis", "redis-namespace", "connection_pool",
    "pg", "mysql2", "sqlite3", "trilogy",
    "httparty", "faraday", "excon", "typhoeus",
    "oj", "yajl", "multi_json",
    "nokogiri", "oga", "sax-machine",
    "sidekiq", "celluloid", "concurrent-ruby",
    "dry-", "rom-", "hanami-", "trailblazer",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "demo", "example", "sample", "test", "testing",
    "skeleton", "boilerplate", "starter", "template",
    "fork", "mirror", "copy", "clone",
}
```

## Methodology

1. **Need-related sample**: Search RubyGems API with need-indicator keywords (e.g., "web framework", "http client", "database", "auth", "cache", "queue", "json", "logger", "config", "test"). Collect up to 100 packages.

2. **Random sample**: Fetch packages from search with empty/popular query across multiple pages, or use the versions API to get recent gems and sample randomly. Collect up to 100 packages.

3. **Classification**: Apply need classification to all collected packages. Keep only those confidently classified as `need-related` or `random`.

4. **Activity measurement**: For each package, record `version_downloads` (downloads of latest version) from the package detail API.

5. **Gate evaluation**: Compute active rates (version_downloads > 0), run Mann-Whitney U test, compute Cliff's delta, Wilson CI95.

## API Endpoints

- Search: `https://rubygems.org/api/v1/search.json?query={query}` (returns ~30 results per page)
- Package detail: `https://rubygems.org/api/v1/gems/{name}.json` (includes downloads, version_downloads, version, etc.)
- Latest versions: `https://rubygems.org/api/v1/versions.json` (for random sampling)

Note: The search API returns limited results (~30). For need-related collection, we'll use multiple search queries. For random collection, we'll sample from the latest versions API or use empty search across pages.

## Success Criteria

All four gates (G1-G4) must pass for the principle to be considered supported on RubyGems.

## Falsification

If G2 fails (p ≥ 0.05 or Cliff's delta ≤ 0.147) OR G3 fails (Wilson LB ≤ 0.60), the principle does not generalize to RubyGems under this measurement.

## Deliverables

- `collect.py` — Data collection script
- `analyze.py` — Gate evaluation script
- `results.json` — Raw results with gate outcomes
- `README.md` — Experiment summary