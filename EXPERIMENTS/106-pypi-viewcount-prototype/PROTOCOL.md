<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E106 — View-count principle PyPI prototype

## Objective

Build a reversible exploratory prototype that leverages the view-count principle on PyPI to help developers identify need-related packages. The prototype demonstrates that the view-count principle (need-related packages have systematically higher activity metrics than random packages) can be operationalized as a practical tool for package discovery.

## Background

The view-count principle has been extensively tested and confirmed on PyPI (E071): need-related packages have 82.93% active rate vs 57.50% random, with all gates passing. This prototype builds on that validated foundation to create a usable tool.

The practical difficulty: every Python developer who has named a dependency from memory (`sklearn`, `telegram`, `beautifulsoup`) and pip-installed a *different real project* that happens to occupy that name understands the problem. E070 measured that the silent wrong-project class is real across PyPI and conda (F103, D089). E071 established that a deterministic checker can flag near-misses with a low false-positive rate. This prototype extends the checker concept by using view-count metadata to prioritize results.

## The Prototype: `pyviewcount` command

A small Python command-line tool that:

1. **Takes a module/import name as input**
2. **Queries PyPI's JSON API** for the package metadata
3. **Classifies the package as need-related or random** based on its description using the Need Indicator / Generic Term framework (E078/E103)
4. **Records the package's download counts** (total and recent) as the "view_count" metric
5. **Outputs a prioritized assessment** indicating whether the package is likely to address the stated need, based on its metadata and activity metrics

## How it works

### Need classification (from E078/E103)

A package is `need-related` iff its description contains at least one term from `NEED_INDICATORS` and does NOT contain any term from `GENERIC_TERMS`:

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
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "rubygem", "ruby", "rails", "rack"
}
```

### Active definition

A package is "active" if its total download count > 0 (following E095/E102 precedent).

### API endpoints

- Package search: `https://pypi.org/pypi/{name}/json`
- Package detail (including downloads): `https://pypi.org/pypi/{name}/json`

### Gates (for prototype validation)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Package found and classified | Package exists and has a description |
| G2 | Need-related active rate > random | Among sampled packages, need-related have higher active rate |
| G3 | Effect size | Wilson CI95 lower bound for proportion of need-related above random median > 0.60 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

## Deliverables

- `harvest.py` — Package fetching and classification script
- `outcome.py` — Gate evaluation script
- `pyviewcount.py` — Main CLI entry point
- `results.json` — Raw results with gate outcomes
- `README.md` — Prototype summary