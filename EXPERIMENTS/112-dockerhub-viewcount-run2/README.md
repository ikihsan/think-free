<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E112 — View-count principle on Docker Hub (container registry)

## Summary
**Result: FAIL — View-count principle does NOT generalize to Docker Hub.**

The experiment tested whether need-related Docker images (specialized infrastructure/operations tools) have higher pull counts than random images. The opposite was observed: random images (which captured official/base images) have systematically higher pull counts.

## Key Findings

| Metric | Need-related | Random |
|--------|-------------|--------|
| Sample size | 55 | 55 |
| Median pull count | ~4,500 | ~55M |
| Mann-Whitney U | 288.0 | - |
| p-value | 2.48e-13 | - |
| Cliff's delta | **-0.810** (large effect, opposite direction) | - |
| Wilson LB (above random median) | 0.000 | - |

## Gate Results

| Gate | Status | Details |
|------|--------|---------|
| G1: Retrieval (≥50 each) | **PASS** | 55 need-related, 55 random |
| G2: Separation (p<0.05, δ>0.147) | **FAIL** | p=2.48e-13, δ=-0.810 (wrong direction) |
| G3: Effect magnitude (Wilson LB>0.60) | **FAIL** | 0/55 need-related above random median (LB=0.000) |
| G4: Arrival field coverage (≥95%) | **PASS** | All 110 images have pull_count > 0 |

## Why It Fails

The "random" sampling strategy (single-letter queries) captured Docker Hub's most popular images:
- **alpine**: 12.3B pulls
- **ubuntu**: 10.1B pulls  
- **node**: 7.1B pulls
- **mysql**: 5.2B pulls
- **mariadb**: 3.2B pulls
- **golang**: 2.7B pulls
- **debian**: 1.8B pulls
- **portainer/portainer-ce**: 1.6B pulls
- **vault**: 555M pulls

These are **general-purpose base images** (OS distributions, language runtimes, major databases) - not "need-related" specialized tools. They're foundational infrastructure that everything else builds on.

The "need-related" sample captured specialized infrastructure images:
- Build caches (plugins/cache: 6.8M, islandora/cache: 226K)
- Specialized caches (mcaptcha/cache: 362K, harness/cache: 345K)
- Various small project-specific cache images (mostly <100K pulls)

## Interpretation

The view-count principle works on **package registries** (PyPI, NPM, NuGet, Hex.pm, CPAN, Packagist) because:
- Users actively search for and download libraries that solve specific problems
- "Need-related" packages = problem-solving libraries = high downloads

The principle **fails on Docker Hub** because:
- The dominant usage pattern is pulling base images as `FROM` in Dockerfiles
- Base images (OS, runtimes) are not "need-related" in our classification - they're prerequisites
- Specialized infrastructure tools (caches, proxies, monitoring) have orders of magnitude fewer pulls

This is a **platform architecture difference**, not a measurement failure. Container registries are dependency-heavy by design (layered filesystems), so foundational images accumulate massive pull counts regardless of "need-relatedness."

## Conclusion

Docker Hub is **not a viable domain** for the view-count principle under the current definition of "need-related." The principle's assumption - that things addressing specific needs get more traffic - breaks down when the platform's primary traffic driver is foundational dependency pulling rather than need-driven discovery.

**Recommendation**: Close the Docker Hub line for the view-count principle. The failure is structural and informative - it reveals a boundary condition for the principle's generalizability.