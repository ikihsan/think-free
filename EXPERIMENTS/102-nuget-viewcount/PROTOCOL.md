<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# Experiment Protocol: NuGet View-Count Principle Test

## Origin
- Mission: Think Free
- Decision driver: D083 — "the next session must start from fresh observation in a new domain"
- Predecessors: E071 (PyPI), E090 (Maven Central), E095 (crates.io), E101 (Hugging Face Hub)
- This experiment tests whether the view-count principle generalizes to NuGet (.NET package registry)

## Question
Does the view-count principle hold on NuGet? Specifically: are packages whose metadata indicates they address a developer need (need-related) systematically more active (higher download counts) than random packages?

## Hypothesis
H0: Need-related packages on NuGet have the same download activity distribution as random packages.
H1: Need-related packages on NuGet have significantly higher download activity than random packages.

## Population and Sampling

### Source
NuGet.org via the Azure Search API: `https://azuresearch-usnc.nuget.org/query?q=<query>&take=100`

### Need-related package definition
A package is "need-related" if its tags, description, or title contain keywords indicating it solves a specific developer problem or fulfills a common need. Keywords include but are not limited to:
- Problem-solving: "parser", "validator", "serializer", "mapper", "converter", "transformer", "resolver", "provider", "factory", "builder", "helper", "utility", "extension", "wrapper", "client", "adapter", "bridge", "proxy", "facade", "mediator", "handler", "processor", "manager", "service", "repository", "store", "cache", "queue", "bus", "event", "message", "notification", "email", "sms", "push", "auth", "authentication", "authorization", "identity", "security", "encryption", "hashing", "jwt", "oauth", "openid", "saml", "ldap", "logging", "tracing", "metrics", "monitoring", "health", "diagnostics", "profiling", "benchmarking", "testing", "mocking", "fixture", "assertion", "configuration", "settings", "options", "localization", "internationalization", "translation", "date", "time", "timezone", "calendar", "cron", "scheduler", "job", "task", "worker", "background", "queue", "hangfire", "quartz", "database", "orm", "entity", "migration", "sql", "nosql", "redis", "mongodb", "postgresql", "mysql", "sqlite", "entityframework", "dapper", "npgsql", "web", "http", "rest", "api", "graphql", "grpc", "signalr", "websocket", "mvc", "razor", "blazor", "aspnet", "core", "middleware", "filter", "attribute", "model", "view", "controller", "routing", "endpoint", "minimal", "api", "swagger", "openapi", "documentation", "ui", "component", "chart", "grid", "table", "form", "validation", "input", "file", "upload", "download", "excel", "csv", "pdf", "report", "chart", "graph", "diagram", "visualization", "map", "geolocation", "gis", "image", "video", "audio", "media", "streaming", "compression", "archive", "zip", "tar", "gzip", "brotli", "encryption", "decryption", "signing", "verification", "certificate", "ssl", "tls", "https", "proxy", "load", "balance", "circuit", "breaker", "retry", "timeout", "bulkhead", "fallback", "cache", "memory", "distributed", "redis", "memcached", "session", "cookie", "token", "claim", "policy", "permission", "role", "user", "account", "profile", "identity", "claim", "principal", "authentication", "authorization"

### Random package definition
A package sampled without keyword filtering, using a random or alphabetical query that does not select for need-relatedness.

### Sample sizes
- Need-related: target n ≥ 30 (per G1 gate)
- Random: target n ≥ 30 (per G1 gate)

### Activity metric
Primary: `totalDownloads` field from NuGet API (cumulative downloads across all versions)
Secondary: recent version download velocity (downloads of latest version)

## Gates (predeclared, must all pass for principle to be considered supported)

### G1 — Retrieval (sample size)
Both arms must return ≥30 classified packages each.
- If either arm <30: FAIL, principle not testable on this platform.

### G2 — Separation (statistical significance)
Mann-Whitney U test (two-sided) comparing totalDownloads of need-related vs random packages.
- p < 0.05 required for PASS.
- Effect size (Cliff's delta) also reported.

### G3 — Effect magnitude (practical significance)
Wilson lower bound of the proportion of need-related packages with totalDownloads > median of random packages must exceed 0.60.
- Equivalent to: need-related packages are "more active" than random at a rate that is practically meaningful.

### G4 — Arrival field coverage
≥95% of sampled packages must have a non-zero, non-null `totalDownloads` field.
- If field missing or zero for >5%: FAIL, activity metric not reliable on this platform.

## Procedure

1. Fetch need-related packages: query NuGet API with keyword-based queries, classify each result.
2. Fetch random packages: query NuGet API with non-selective queries (e.g., random letters, pagination), classify each result.
3. For each package, record: id, version, totalDownloads, description, tags, title, classification.
4. Apply gates G1–G4.
5. Report all numbers, confidence intervals, and gate verdicts.

## Analysis script
`run.py` — implements the protocol, prints gate verdicts, writes `results.json`.

## Reproduction
```bash
cd EXPERIMENTS/102-nuget-viewcount
python3 run.py --gate
```

## Outputs
- `results.json` — machine-readable gate results and raw data
- `README.md` — human-readable summary

## Kill condition
If any gate FAILs, the view-count principle does not generalize to NuGet under this protocol. The experiment closes the NuGet line for this principle.