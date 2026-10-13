<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E122 — Fresh observation: CI/CD pipeline failure classification

## Summary

Fresh observation in a new domain per D083: **CI/CD pipeline failures on GitHub Actions**.
This domain has not been previously tested in the mission's experiments. The practical problem:
developers spend significant time debugging failed CI/CD builds. A tool that classifies failure
types and suggests remediation could be unusually useful.

## The practical difficulty

When a CI/CD pipeline fails, developers must:
1. Read through verbose logs (often 100s-1000s of lines)
2. Identify the root cause (test failure, dependency issue, flaky test, environment problem, etc.)
3. Search for solutions or apply known fixes
4. Re-run and iterate

This is a recurrent, time-consuming task with observable failure patterns that could be
systematically classified and addressed.

## Population

**Unit**: One failed GitHub Actions workflow run from a public repository.
**Source**: GitHub Actions API (public repos, failed runs).
**Sampling**: Random sample of failed runs across diverse repositories (by language, size, activity).

## Instrument

A classifier that takes a failed workflow run's logs and classifies the failure into categories:

| Category | Description | Example patterns |
|---|---|---|
| `test_failure` | Unit/integration test failed | `FAILED`, `AssertionError`, `pytest` failures |
| `dependency_error` | Missing/broken dependency | `ModuleNotFoundError`, `npm ERR!`, `cargo build failed` |
| `flaky_test` | Intermittent test failure | Same test passes on re-run, timing-related |
| `environment_error` | Runner/environment issue | `docker: not found`, `permission denied`, `out of memory` |
| `compile_error` | Code compilation failed | `SyntaxError`, `type error`, `compilation failed` |
| `timeout` | Step exceeded time limit | `The operation was canceled`, `timeout` |
| `permission_error` | Auth/permission issue | `403 Forbidden`, `Permission denied (publickey)` |
| `unknown` | Cannot classify from logs | Insufficient log content |

## Kill gates (declared before any fetch)

| Gate | Threshold | Rationale |
|---|---|---|
| **KG1** | Classifier achieves ≥80% accuracy on synthetic fixtures | Must demonstrate the classification task is tractable |
| **KG2** | ≥5 distinct failure categories observed in real sample | Must show population diversity, not a single dominant mode |
| **KG3** | ≤30% classified as `unknown` on real sample | Classifier must cover the population |
| **KG4** | At least one category has ≥20% prevalence AND known remediation pattern | Must have actionable signal for at least one common failure type |

If any kill gate fails, the experiment returns `not_evaluated` and the domain is closed
for candidate generation (but the instrument and data are preserved).

## Falsification criterion

The experiment is falsified if **KG1 fails** — i.e., even on synthetic fixtures with
clear failure patterns, the classifier cannot achieve 80% accuracy. This would mean
the classification task is not tractable with the proposed approach.

## Synthetic fixtures (declared before real data)

20 synthetic log snippets per category (160 total), each containing clear markers
for its category. These are hand-crafted to represent the canonical pattern for
each failure type. The classifier is tested on these first — if it fails here,
the real-data run is not attempted.

## Baseline

**Strongest accessible alternative**: Manual log reading by a developer.
Measured as: time to classify + time to find remediation.
The prototype must demonstrate measurable advantage over this baseline on a
representative sample.

## Reproduction command

```bash
cd EXPERIMENTS/122-cicd-failure-fresh-observation
python3 run_experiment.py
```

This will:
1. Generate synthetic fixtures
2. Run classifier on fixtures (KG1)
3. If KG1 passes, fetch real failed runs from GitHub Actions API
4. Classify real runs (KG2, KG3, KG4)
5. Report results with all gates

## What this cannot establish

- Whether a tool built on this classifier would be adopted
- Whether the remediation suggestions are actually correct in practice
- Generalization to GitLab CI, Jenkins, CircleCI, etc. (GitHub Actions only)
- Whether the `unknown` category represents a fundamental limit or just needs more patterns

## Decision rule

If all kill gates pass: the domain supports further investigation toward a candidate.
If any kill gate fails: the domain is closed for candidate generation, recorded in FAILURES.