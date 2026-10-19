# E180 Result — View-count Principle on Pub.dev (Dart/Flutter Package Registry)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-17
-->

## Experiment

**E180** — Fresh observation of the view-count principle on the Pub.dev package registry for Dart/Flutter

## Results

### Classification counts

- **Need-related**: 50 topics (45.5%)
- **Random**: 60 topics (54.5%)
- **Total classified**: 110

### Activity metrics (presence of description + version)

- **Need-related active rate**: 50/50 = 100.0% (all need-related packages have non-empty description and version present)
- **Random active rate**: 60/60 = 100.0% (all random packages have non-empty description and version present)
- **G1 ratio**: 100.0% (need/random active rate ratio)
- **G1 pass**: YES (ratio >= 55% threshold)

### Gate results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** | need-related active rate >= 55% of random active rate | **PASS** (ratio = 100.0% >= 55%) |
| **G2** | total classified >= 100 | **PASS** (classified total = 110) |
| **G3** | both categories represented | **PASS** (need-related > 0 and random > 0) |
| **G4** | total classified >= 50 | **PASS** (classified total = 110) |

### Cliff's delta on activity

- **Delta**: N/A — no activity variation observed (100% active rate in both categories)
- The view-count instrument's activity metric (description + version completeness) is uniformly present across all packages on Pub.dev, creating a ceiling effect that precludes discrimination between need-related and random packages.

### Conclusion

**gates_all_pass** — All four gates pass. However, this result is **not indicative of a successful validation** of the view-count principle. The G1 pass is a ceiling effect: on Pub.dev, the activity metric (non-empty description AND version present) is effectively universal, holding for 100% of both need-related and random packages. This makes the active-rate ratio trivially 100% regardless of the underlying principle.

This is the **fifth platform** (after crates.io, Hugging Face Hub) where the activity metric's universality prevents the view-count principle from producing a meaningful discrimination. The principle's boundary condition requires **variation in the activity metric** — where some packages/items have the metric and others do not — in order for need-related classification to systematically correlate with higher activity.

### Key observation

The Pub.dev API's `/api/packages` endpoint returns packages with descriptions and versions as a default feature of the registry format. Unlike PyPI, NPM, NuGet, and other registries where inactive/abandoned packages may lack complete metadata, Pub.dev packages consistently have both description and version fields. This means the "active" signal — the core differentiator the view-count principle relies on — is not domain-differentiated on Pub.dev.

**G1 passes trivially** because the ratio is 100/100 regardless of classification. **This does not constitute evidence that need-related packages have systematically higher activity**, because there is no activity variation to measure.

### Notes

- The experiment used keyword "database" to fetch need-related packages via the Pub.dev search API, and random packages from the default `/api/packages?limit=200` listing.
- 110 packages were classified (50 need-related, 60 random), exceeding the G2 threshold of 100.
- The need-indicator vocabulary classified 50/110 packages (45.5%) as need-related, with triggering terms including `database`, `auth`, `network`, `api`, `http`, `client`, `server`, `framework`, `cache`, `security`, `logging`, `monitoring`, `testing`, `benchmark`.
- The random category also contained packages with need-indicator words in their descriptions, indicating vocabulary overlap with the forum's topic domain.
- A larger sample from multiple pages or categories would confirm whether the ceiling effect is universal across Pub.dev or specific to the `/latest.json` equivalent endpoint.

### Raw data

See `EXPERIMENTS/E180-pubdev-viewcount/results.json` for complete classified packages and activity metrics.

### Correction — 2026-10-17

The declared outcome `gates_all_pass` is **not licensed as a positive finding** for the view-count principle. The G1 gate fires only due to a ceiling effect where the activity metric is universal. Per D083 and the mission's evidence-labels policy, this outcome closes the Pub.dev route for the view-count principle until such time as an activity metric with measurable variation becomes accessible from the platform. The finding is: **view-count principle does not generalize to Pub.dev due to activity metric universality**. This venue is **not** added to the mission's tally in either direction.

Status: `closed` (activity metric boundary condition).