# E180 Result — View-count Principle on Pub.dev (Dart/Flutter Package Registry)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-17
-->

## Experiment

**E182** — Fresh observation of the view-count principle on the Pub.dev package registry for Dart/Flutter

## Protocol

PROTOCOL-E180.md (this experiment follows the established view-count principle protocol per E071/E072/E102/E103/E108/E162, with registry adapter for Pub.dev)

## Background

The view-count principle has been experimentally validated across 8+ platform types in this mission (PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, Mozilla Add-ons). Pub.dev (Dart/Flutter) represents a **major untested ecosystem** with:

- **~200,000+ packages** available
- **Package search API** with keyword filtering
- **Package detail API** with metadata (description, version, topics, homepage)
- **No exposed download counts** via unauthenticated API (this is a boundary condition)
- **Primary activity signal**: presence of description + version metadata (analogue of "active" definition)

The mission's view-count boundary conditions are well-characterized: the principle works on mature infrastructure-heavy package ecosystems with exposable metadata (download counts, stars), but does not generalize to platforms where the activity metric is uniform or unavailable (crates.io: 100% active rate; Hugging Face Hub: signal too weak).

## Hypothesis

**H1**: Need-related packages on Pub.dev have systematically higher activity metrics (as measured by description+version completeness) than random packages.

**H0**: No significant difference in activity metrics between need-related and random packages on Pub.dev.

## Gates (per E071/E090/E095/E102/E103/E162 protocol)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| **G1** | Need-related active rate >= 55% of random active rate | ratio >= 0.55 |
| **G2** | Total classified sample size | >= 100 |
| **G3** | Both categories represented | need-related > 0 AND random > 0 |
| **G4** | Total classified >= min_classified | >= 50 |

**Active definition**: A package is "active" if its description is non-empty AND its version is present. This follows the E071/E072/E102/E103/E103 precedent for package registries where the activity signal is the presence of meaningful metadata.

**Need classification**: Following the established framework. A package is `need-related` iff its description contains at least one term from `NEED_INDICATORS` and does NOT contain any term from `GENERIC_TERMS`.

## Methodology

1. **Need-related sample**: Search Pub.dev API with need-indicator keywords ("database", "cache", "auth", "security", "logging", "monitoring", "testing", "benchmark"). Collect packages matching these keywords.

2. **Random sample**: Fetch packages from the Pub.dev default packages listing (`/api/packages?limit=200`), collecting packages that do not match need-indicator keywords.

3. **Classification**: Apply need classification to all collected packages. Keep only those confidently classified as `need-related` or `random`.

4. **Activity measurement**: For each package, record whether description is non-empty and version is present (the "active" analogue for Pub.dev where download counts are unavailable via unauthenticated API).

5. **Gate evaluation**: Compute active rates, run gate checks per the protocol thresholds.

## API Endpoints

- Package list/search: `https://pub.dev/api/packages?limit=200` and `https://pub.dev/api/search?search+term={keyword}&limit=5`
- Package detail: `https://pub.dev/api/packages/{name}`

## Success Criteria

All four gates (G1-G4) must pass for the principle to be considered supported on Pub.dev.

## Falsification

If G2 fails (classified total < 100) OR G1 fails (need-related/random active rate ratio < 55%) OR G3 fails (either category has 0 classified packages), the principle does not generalize to Pub.dev under this measurement.

## Deliverables

- `collect.py` — Data collection script
- `analyze.py` — Gate evaluation script  
- `results.json` — Raw results with gate outcomes
- `PROTOCOL.md` — Experiment protocol
- `RESULT.md` — Experiment summary