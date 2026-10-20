<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E165: Go Module Ecosystem (pkg.go.dev) View-Count Principle Test

## Objective
Test whether the view-count principle generalizes to the Go module ecosystem (pkg.go.dev), using "Imported by" count as the activity metric.

## Background
The view-count principle has been tested across 17+ domains:
- **Supported** (principle holds): PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, GitHub repos, Mozilla Add-ons
- **Not supported**: CRAN, Maven Central, GitHub Issues API, web search, automotive OBD2, PX4 drone faults, 3D printer fault codes, medical device fault codes, embedded/MCU fault codes, industrial SCADA, CFPB consumer complaints, Physics SE, crates.io (classifier mismatch), GitLab (classifier mismatch)
- **Boundary**: Works on package registries (leaf consumption), fails on model hubs (Hugging Face - infrastructure layer), fails on Q&A forums

Go modules (pkg.go.dev) is a **major package registry not yet tested**. It exposes "Imported by" counts (number of known importers) universally on search results and package pages. This is analogous to "dependent count" on other registries.

## Hypothesis
Need-related Go packages (derivatives, wrappers, adapters, framework extensions, middleware, plugins, clients, drivers, bindings) have systematically higher "Imported by" counts than random packages.

## Method

### G1 Gate (Classification Rate)
- Sample 200 packages via multiple search strategies
- Classify each as **need-related** or **general** using pre-declared keyword rules on package path + synopsis
- **Pass**: ≥30 packages per class (need-related and general)

### G2 Gate (Statistical Significance)
- Compare "Imported by" distributions using Cliff's delta
- **Pass**: Cliff's delta ≥ 0.147 (same threshold as previous experiments)

### G3 Gate (Activity Advantage)
- Need-related class must have ≥80% packages with positive "Imported by" arrivals
- Random class must have <80% (differential activity)

### G4 Gate (Metadata Coverage)
- "Imported by" count must be present for ≥95% of sampled packages
- **Pass**: Universal presence confirmed

### Sampling Strategy
Use multiple search queries to get diverse coverage:
1. `framework` - web frameworks, framework extensions
2. `client` - API clients, service clients
3. `wrapper` - library wrappers, bindings
4. `middleware` - HTTP middleware, framework middleware
5. `plugin` - plugins, extensions
6. `driver` - database drivers, hardware drivers
7. `adapter` - adapters, converters
8. `library` - general libraries (baseline)
9. `tool` - CLI tools, utilities
10. `util` - utilities, helpers
11. `sdk` - SDKs
12. `api` - API packages
13. Random search (empty query) - baseline
14. `standard library` - stdlib packages (baseline)

Each query returns up to 20 results (max per page), targeting ~200 total unique packages.

### Classification Rules (Pre-declared)

**Need-related keywords** (in package path OR synopsis):
- `wrapper`, `wrap`, `binding`, `bind`, `adapter`, `adaptor`, `bridge`
- `client`, `sdk`, `api` (as suffix/prefix in path)
- `middleware`, `plugin`, `extension`, `ext`
- `driver`, `dialect`
- `framework`, `fw`
- `implementation`, `impl` (when not the primary/original)
- `fork`, `port`, `mirror`
- `v2`, `v3` (major version paths suggesting forks/derivatives)

**General keywords** (in package path OR synopsis):
- Base/original framework names: `gin`, `echo`, `fiber`, `beego`, `iris`, `revel`, `chi`, `gorilla`, `httprouter`
- Core language: `stdlib`, `standard`, `builtin`, `core`
- Primary/original libraries (not derivatives)

**Decision rule**: If any need-related keyword matches → need-related. Else if any general keyword matches → general. Else → unclassified (excluded from primary analysis).

### Kill Gate
If G1 FAILS (insufficient classification rate) → **stop, principle not testable on this platform with current vocabulary**.
If G2 FAILS (Cliff's delta < 0.147) → **principle does not generalize to Go modules**.
If G3 FAILS (no differential activity) → **principle does not generalize**.
If G4 FAILS (metadata not universal) → **principle not applicable**.

## Falsification
The experiment could be falsified by:
1. Finding that "Imported by" counts don't correlate with need-indicators (Cliff's delta < 0.147)
2. Finding that classifier vocabulary mismatch prevents G1 passage (like crates.io, GitLab)
3. Finding that metadata coverage is incomplete (G4 fail)

## Pre-registered Analysis
- Primary: Cliff's delta between need-related and general "Imported by" counts
- Secondary: Mann-Whitney U test, median comparison
- Exploratory: Distribution shapes, outlier analysis, query-stratum effects

## Deliverables
- `harvest.py` - fetches packages from pkg.go.dev search
- `classify.py` - applies pre-declared classification rules
- `measure.py` - computes Cliff's delta, gates, statistics
- `run.py` - orchestrates the experiment
- `results.json` - raw results
- `RESULT.md` - written report with gate verdicts