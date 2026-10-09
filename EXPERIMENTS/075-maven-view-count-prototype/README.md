# E075 — Maven View-Count Prototype

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

Prototype CLI tool implementing the view-count principle across package repositories.
See `view_count_prototype.py` for the implementation and `EXPERIMENTS/075-maven-view-count-prototype/maven_exp.py` for the experimental results.

## Principle

The view-count principle: packages with higher activity metadata (download/view counts, recent releases) are systematically more "active" (actively maintained) than random packages.

Validated on: PyPI (E071, all gates met), NPM (E072, all gates met).
Marginal/negative on: Maven Central (E075b, gates mixed — recent-activity metric shows signal but does not reach significance threshold).

## Prototype

```
python3 view_count_prototype.py pypi <package>
python3 view_count_prototype.py npm <package>
python3 view_count_prototype.py maven <groupId:artifactId>
```

## Gates Summary

| Platform | G1 | G2 | G3 | Outcome |
|---|---|---|---|---|
| PyPI | PASS | PASS | PASS | Principle validated |
| NPM | PASS | PASS | PASS | Principle validated |
| Maven Central (recent) | PASS | FAIL (p=0.084) | FAIL (WC<0.6) | Mixed signal |
| Maven Central (VC≥20) | FAIL | FAIL | FAIL | Below baseline |

## Quick test

```bash
python3 view_count_prototype.py pypi requests
python3 view_count_prototype.py npm lodash
python3 view_count_prototype.py maven com.fasterxml.jackson.core:jackson-core
```