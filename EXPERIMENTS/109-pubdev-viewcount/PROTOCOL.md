# E109 — View-count principle on Pub.dev (Dart/Flutter package registry)

<!-- origin-meta
owner: docs/INDEX.md
status: superseded
last-verified: 2026-10-12
-->

> **SUPERSEDED BEFORE ANY FETCH (2026-10-12, E110 / F116 / D105). Never run.**
> This protocol was written under D083's domain sweep. E110 then measured that
> the sweep's shared design produces its own result: the need arm and the random
> arm are drawn by different queries and sorted by the outcome metric, and the
> classifier labels 28% of a representative population. Running E109 would have
> inherited both defects and added a sixteenth number that means nothing.
> Retained as the record of what the next action was before E110 answered it.
> See [`EXPERIMENTS/110-viewcount-matched-harvest/`](../110-viewcount-matched-harvest/).

## Origin
- Mission: Think Free
- Decision driver: D083 — "the next session must start from fresh observation in a new domain" (**withdrawn by D105**)
- Predecessors: E071 (PyPI), E090 (Maven Central), E095 (crates.io), E101 (Hugging Face Hub), E102 (NuGet), E103 (Hex.pm), E108 (Docker Hub), 0xx-cpan-viewcount (CPAN), 0xx-packagist-viewcount (Packagist)
- This experiment tests whether the view-count principle generalizes to Pub.dev, the package registry for Dart and Flutter

## Question
Does the view-count principle hold on Pub.dev? Specifically: are packages whose metadata indicates they address a developer need (need-related) systematically more active (higher download counts) than random packages?

## Hypothesis
H0: Need-related packages on Pub.dev have the same download activity distribution as random packages.
H1: Need-related packages on Pub.dev have significantly higher download activity than random packages.

## Population and Sampling

### Source
Pub.dev API v2:
- Search: `https://pub.dev/api/search?q={query}&page={n}`
- Package detail: `https://pub.dev/api/packages/{name}`
- Random: `https://pub.dev/api/packages?page={n}` (default listing)

### Need-related package definition
A package is "need-related" if its name, description, or tags contain keywords indicating it solves a common programming problem or fulfills a common developer need. Keywords include but are not limited to:

**Core Infrastructure:**
- HTTP: "http", "dio", "client", "rest", "api", "graphql", "grpc", "websocket"
- Database: "database", "db", "sql", "sqlite", "postgres", "mysql", "mongo", "redis", "firestore", "realm", "hive", "objectbox", "drift", "floor", "sqflite"
- State management: "bloc", "cubit", "provider", "riverpod", "getx", "mobx", "redux", "state", "state-management"
- Routing: "router", "routing", "go_router", "auto_route", "navigator", "navigation"
- Dependency injection: "inject", "get_it", "service_locator", "di", "dependency-injection"
- Serialization: "json", "serialization", "serializable", "freezed", "built_value", "protobuf", "msgpack"
- Network: "network", "connectivity", "socket", "tcp", "udp", "webrtc"

**Platform & Device:**
- Platform integration: "platform", "android", "ios", "macos", "windows", "linux", "web", "channel", "method_channel", "pigeon"
- Device: "camera", "location", "gps", "geolocation", "sensors", "accelerometer", "gyroscope", "biometric", "fingerprint", "face_id"
- Storage: "storage", "shared_preferences", "secure_storage", "keychain", "keystore", "file", "path_provider"
- Background: "background", "workmanager", "flutter_background", "isolate", "service"

**UI & UX:**
- UI components: "ui", "widget", "component", "material", "cupertino", "design-system", "theme", "animation", "transition"
- Forms: "form", "validation", "validator", "input", "field", "textfield", "dropdown", "picker", "date-picker"
- Media: "image", "video", "audio", "player", "cache", "cached_network_image", "photo", "gallery"
- Charts: "chart", "graph", "visualization", "fl_chart", "syncfusion", "charts"

**Testing & Quality:**
- Testing: "test", "mock", "mockito", "mocktail", "integration-test", "widget-test", "golden-test", "driver"
- Linting: "lint", "analyzer", "dart_code_metrics", "custom_lint"
- CI/CD: "ci", "cd", "github-actions", "codemagic", "bitrise", "fastlane"

**Developer Tools:**
- CLI: "cli", "command", "argument", "parser", "console", "terminal"
- Build: "build", "builder", "codegen", "generator", "build_runner", "source_gen"
- Logging: "logger", "logging", "log", "sentry", "crashlytics", "analytics"

### Random package definition
A package sampled without keyword filtering, using the default package listing (pagination through default API listing) that does not select for need-relatedness.

### Sample sizes
- Need-related: target n ≥ 50 (per G1 gate)
- Random: target n ≥ 50 (per G1 gate)

### Activity metric
Primary: `download_count` field from Pub.dev API (total downloads across all versions)
Secondary: `recent_download_count` or weekly/monthly downloads if available

## Gates (predeclared, must all pass for principle to be considered supported)

### G1 — Retrieval (sample size)
Both arms must return ≥50 classified packages each.
- If either arm <50: FAIL, principle not testable on this platform.

### G2 — Separation (statistical significance)
Mann-Whitney U test (two-sided) comparing download_count of need-related vs random packages.
- p < 0.05 required for PASS.
- Effect size (Cliff's delta) also reported, must exceed 0.147 (small effect threshold).

### G3 — Effect magnitude (practical significance)
Wilson lower bound of the proportion of need-related packages with download_count > median of random packages must exceed 0.60.
- Equivalent to: need-related packages are "more active" than random at a rate that is practically meaningful.

### G4 — Arrival field coverage
≥95% of sampled packages must have a non-zero, non-null `download_count` field.
- If field missing or zero for >5%: FAIL, activity metric not reliable on this platform.

## Procedure

1. Fetch need-related packages: query Pub.dev API with keyword-based searches, classify each result.
2. Fetch random packages: query Pub.dev API default listing (pagination), classify each result.
3. For each package, record: name, download_count, description, tags, classification.
4. Apply gates G1–G4.
5. Report all numbers, confidence intervals, and gate verdicts.

## Analysis script
`run.py` — implements the protocol, prints gate verdicts, writes `results.json`.

## Reproduction
```bash
cd EXPERIMENTS/109-pubdev-viewcount
python3 run.py --gate
```

## Outputs
- `results.json` — machine-readable gate results and raw data
- `README.md` — human-readable summary

## Kill condition
If any gate FAILs, the view-count principle does not generalize to Pub.dev under this protocol. The experiment closes the Pub.dev line for this principle.