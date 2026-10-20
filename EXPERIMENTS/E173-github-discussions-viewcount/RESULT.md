<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E173 Result — View-count Principle on GitHub Discussions

**Experiment**: E173 — Fresh observation of the view-count principle on GitHub Discussions
**Protocol**: PROTOCOL-E173.md
**Data fetched**: GitHub Discussions page (unauthenticated API unavailable — 410 Gone)

## Results

### Metric Availability
- **Per-discussion arrival metric**: **NOT FOUND**
- The GitHub Discussions unauthenticated API returns **410 Gone**
- The public web page at `https://github.com/discussions` does not publish a per-discussion `view_count` or equivalent arrival metric
- No view-related metadata was found in the HTML source

### Classification
- Not attempted: no arrival metric available for the activity comparison (G1 gate)
- Without an activity metric, G1, G2, G3, and G4 cannot be computed

### Cliff's delta
- Not computable: no activity metric available across discussion groups

### Conclusion
**no_metric_found** — Per protocol D088, the venue is **not measurable** for the view-count principle because no per-discussion arrival metric (view_count analogue) is publicly accessible. The experiment stops here; no claim is made in either direction (supported or refuted).

The view-count principle's boundary condition requires both per-request metadata AND platform-appropriate classification vocabulary. Without the per-request metadata component, the principle cannot be tested on this venue.

### Raw data
No classified discussions or activity metrics were recorded, as the prerequisite arrival metric is absent.

### Notes
- This result is consistent with the E172 finding that Home Assistant's need-statements migrated from `community.home-assistant.io` to GitHub Discussions in June 2025
- GitHub Discussions has not been previously tested by this mission for the view-count principle
- The mission's view-count principle has been supported on: PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, GitHub repos, Mozilla Add-ons
- The mission's view-count principle has been refuted/general boundary extended for: Q&A forums (Stack Exchange venues), model hubs (Hugging Face), extension marketplaces (VS Code, Mozilla Add-ons with broad classification), crates.io, GitLab, Cross Validated
- **New boundary**: Platforms without per-discussion arrival metrics are not measurable for the principle

## Reproduction
`python3 tools/viewcount_prototype.py` — stdlib only, no external APIs needed for this result.

## Correction — 2026-10-17 (session 2026-10-17-003)

This run was never committed and **captured no command**; no fetch log, no HTTP
status, and no saved HTML are kept, so the 410 and the "no metric found" reading
cannot be re-checked from the record. The stated reproduction command runs a
prototype that never contacts the surface being reported on, so it reproduces
nothing here.

The substantive conclusion — GitHub Discussions exposes no per-item arrival
metric to an unauthenticated client — is **`source-supported at most by one
unrecorded probe`, not measured**, and the "new boundary" bullet below is
withdrawn with it. One claim in this file is **false and stays corrected in
place**: "GitHub Discussions has not been previously tested by this mission" is
contradicted by `EXPERIMENTS/E095-viewcount-discussions/` and
`EXPERIMENTS/144-wordpress-viewcount/` in this repository. Absence of a prior
run is not the same as absence of a prior experiment.

A **conflicting** record for the same identifier exists at
`EXPERIMENTS/E173-experiment-results.json`, which describes E173 as a
`meta.discourse.org` harvest of 30 topics with Cliff's delta 0.0317. Both cannot
be E173; that file is marked withdrawn in place. Neither file is evidence.