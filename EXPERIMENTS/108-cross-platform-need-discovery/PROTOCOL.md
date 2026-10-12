<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E108 — Cross-Platform Need Discovery Prototype

## Objective

Build a reversible exploratory prototype that leverages the validated view-count principle across multiple platforms to help developers discover the right package/repository for their stated need. The view-count principle has been validated on PyPI, NPM, NuGet, Hex.pm, GitHub repositories, Discourse forums, Stack Exchange, and Code Review Stack Exchange.

## Background

The view-count principle states: **need-related items (packages, repositories, questions) have systematically higher engagement metrics (downloads, stars, views) than random items.** This has been experimentally validated across 8+ platform types:

| Platform | Metric | Result | Key Finding |
|----------|--------|--------|-------------|
| PyPI | Downloads | ALL GATES PASS | Need-related 82.93% active vs 57.50% random |
| NPM | Activity score | ALL GATES PASS | 100% need-related active vs 0% random |
| NuGet | Downloads | ALL GATES PASS | p=1.7e-14, Cliff's δ=0.996 |
| Hex.pm | Downloads | ALL GATES PASS | Need median 220× random median |
| GitHub Repos | Stars | ALL GATES PASS | Need median 8.6× random median |
| Discourse | Views | ALL GATES PASS | 11.7% unserved fraction |
| Stack Exchange (non-sw) | Views | ALL GATES PASS | 17/20 unremedied needs served |
| Code Review SE | Views | ALL GATES PASS | 73.3% unserved need rate |

The practical difficulty: **Every developer who has searched for a library and gotten noisy, irrelevant, or abandoned results understands this problem.** Current package search (PyPI, NPM, GitHub) does not leverage the view-count signal to prioritize genuinely useful, well-maintained packages.

## The Prototype: `needfind` command

A small Python command-line tool that:

1. **Takes a natural language need description as input** (e.g., "async HTTP client for Python", "React state management library")
2. **Classifies the need** into categories (web, database, auth, cache, etc.) using the Need Indicator / Generic Term framework (E078/E103)
3. **Searches relevant platforms** based on detected language/ecosystem keywords:
   - Python needs → PyPI + GitHub (Python repos)
   - JavaScript/TypeScript needs → NPM + GitHub (JS/TS repos)
   - .NET/C# needs → NuGet + GitHub (C# repos)
   - Elixir/Erlang needs → Hex.pm + GitHub (Elixir repos)
   - Generic needs → GitHub repos (all languages)
4. **Ranks results by view-count signal** (downloads, stars) within each platform
5. **Outputs a prioritized, cross-platform result set** with platform, name, description, activity metric, and need-relevance classification

## Need Classification Framework (from E078/E103)

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
}

LANGUAGE_KEYWORDS = {
    "python": ["python", "py", "django", "flask", "fastapi", "asyncio", "pypi", "pip"],
    "javascript": ["javascript", "js", "node", "npm", "react", "vue", "angular", "typescript", "ts"],
    "typescript": ["typescript", "ts", "node", "npm"],
    "csharp": ["csharp", "c#", ".net", "dotnet", "nuget", "aspnet"],
    "elixir": ["elixir", "ex", "phoenix", "ecto", "hex", "mix"],
    "rust": ["rust", "cargo", "crates"],
    "go": ["go", "golang"],
    "java": ["java", "maven", "gradle", "spring"],
}
```

## Platform APIs

| Platform | Search Endpoint | Activity Metric | Auth Required |
|----------|-----------------|-----------------|---------------|
| PyPI | `https://pypi.org/search/?q={query}` | Downloads (via stats API) | No |
| NPM | `https://registry.npmjs.org/-/v1/search?text={query}` | Downloads (via API) | No |
| GitHub | `https://api.github.com/search/repositories?q={query}` | Stars | No (60/hr) |
| NuGet | `https://azuresearch-usnc.nuget.org/query?q={query}` | Total downloads | No |
| Hex.pm | `https://hex.pm/api/packages?search={query}` | Recent downloads | No |

## Gates (Prototype Validation)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Tool runs without error on test queries | 5/5 test queries complete |
| G2 | Returns results for at least 2 platforms per query | ≥ 2 platforms with results |
| G3 | Need-related results rank higher than generic | Manual inspection: top-3 results are relevant |
| G4 | Cross-platform deduplication works | Same logical package not duplicated |

## Falsification

If G1 or G2 fail, the prototype cannot function as a cross-platform tool. If G3 fails on manual inspection of 5 test queries, the ranking signal is not useful for discovery.

## Deliverables

- `needfind.py` — Main CLI entry point
- `platforms/` — Platform-specific search modules
- `classifier.py` — Need and language classification
- `ranker.py` — Cross-platform ranking by view-count signal
- `PROTOCOL.md` — This document
- `README.md` — Prototype summary

## Commands

```bash
# Search for a need
python3 needfind.py "async HTTP client for Python"

# Search with explicit platform targeting
python3 needfind.py "React state management" --platforms npm,github

# Search with language hint
python3 needfind.py "web framework" --language python

# Output as JSON
python3 needfind.py "database ORM" --json
```