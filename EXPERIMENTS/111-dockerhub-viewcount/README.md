# E111 — View-count principle on Docker Hub container images

## Summary

**ALL GATES PASS** — The view-count principle generalizes to Docker Hub container images.

Need-related Docker images (infrastructure/deployment tools like nginx, postgres, redis, prometheus, kubernetes, etc.) have systematically higher pull counts than random images.

## Key Results

| Metric | Need-related | Random |
|--------|-------------|--------|
| Count | 3,313 | 537 |
| Pull count median | 50,070 | 5,319 |
| Pull count mean | 29.2M | 2.16M |
| Active (pulls > 0) | 100% | 100% |

## Gate Evaluation

| Gate | Criterion | Result |
|------|-----------|--------|
| G1 | ≥ 200 total, ≥ 100 per group | **PASS** (3,850 total, 3,313 need, 537 random) |
| G2 | Mann-Whitney U p < 0.05, Cliff's δ > 0.147 | **PASS** (p ≈ 6.8×10⁻⁴⁷, δ = 0.386) |
| G3 | Wilson CI95 LB for proportion above random median > 0.60 | **PASS** (LB = 0.785) |
| G4 | Both categories represented | **PASS** |

## Methodology

1. **Harvested** 5,980 unique repositories from Docker Hub search API:
   - 28 need-related queries (nginx, postgres, mysql, redis, mongo, rabbitmq, kafka, prometheus, grafana, jenkins, gitlab, kubernetes, docker, terraform, ansible, vault, consul, traefik, kong, elasticsearch, influxdb, minio, cert-manager, keycloak, etcd, zookeeper, haproxy, caddy, envoy, istio)
   - 31 random queries (ubuntu, debian, alpine, busybox, centos, fedora, archlinux, opensuse, amazonlinux, rockylinux, almalinux, hello-world, scratch, distroless, myapp, test-app, sample-app, demo-app, example-app, myimage, testimage, custom-image, personal-image, internal-app, private-app, company-app, team-app, project-a, project-b, service-a, service-b)
   - 1 broad query (empty)

2. **Classified** using token-based matching on repo name + description:
   - `NEED_INDICATORS`: 80+ terms covering web servers, databases, message queues, monitoring, CI/CD, orchestration, service mesh, language runtimes, infrastructure tools, security, storage, logging, load balancing, API gateways, search, time-series
   - `GENERIC_TERMS`: 40+ terms for base images, templates, personal/test images
   - Excluded official images (34)

3. **Measured** pull_count as the primary arrival metric

## Interpretation

The view-count principle holds strongly on Docker Hub:
- Need-related images have ~9.4× higher median pull counts
- 79.9% of need-related images exceed the random median (Wilson LB 0.785)
- The effect size (Cliff's δ = 0.386) is medium and statistically decisive

This adds Docker Hub as the **8th platform** where the view-count principle is validated, joining:
- PyPI (E071)
- NPM (E072)
- NuGet (E102)
- Hex.pm (E103)
- Packagist (E108)
- RubyGems (E109)
- GitHub code repositories (E107)

And contrasts with platforms where it fails:
- Maven Central (E090)
- crates.io (E095)
- Hugging Face Hub (E101)

## Files

- `PROTOCOL.md` — Pre-declared experiment protocol with gates
- `harvest.py` — Data collection from Docker Hub API
- `classify.py` — Need/random classification
- `analyze.py` — Gate evaluation
- `raw_data.json` — Raw harvested repository data (5,980 repos)
- `classified_data.json` — Classification results
- `results.json` — Gate evaluation results