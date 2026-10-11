# Session 2026-10-11-042-run-fresh-observation-experiment-in-a-ne

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T18:23:56+00:00
- **Duration:** 2492.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run fresh observation experiment in a new domain per D083 - test view-count principle on a platform not yet tested

## Summary

E108: Fresh observation on Docker Hub (container registry) - view-count principle FAILS. Tested 55 need-related vs 55 random images. G1 PASS (sample size), G2 FAIL (Cliff's δ = -0.810, large effect in WRONG direction), G3 FAIL (Wilson LB = 0.000), G4 PASS. Random sample captured massive base images (alpine 12.3B, ubuntu 10.1B, node 7.1B, mysql 5.2B pulls) while need-related captured specialized infra tools (<10M pulls). Principle fails because container registries are dependency-heavy - base images accumulate pulls as FROM dependencies, not need-driven discovery. Per D083, next session must start fresh observation in new domain.

## Next

Fresh observation in a new domain per D083 - view-count principle has been tested on package registries (PyPI, NPM, NuGet, Hex.pm, CPAN, Packagist), code hosting (GitHub repos), Q&A forums (Discourse, Stack Exchange), ML model registry (Hugging Face), crate registry (crates.io), Maven Central, and now Docker Hub. Next domain should be untested: e.g., Go pkg.go.dev, JSR (JavaScript Registry), conda-forge, or another package registry not yet tested.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 9 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/108-dockerhub-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/108-dockerhub-viewcount/README.md |
|   undeclared | EXPERIMENTS/108-dockerhub-viewcount/classify.py |
|   undeclared | EXPERIMENTS/108-dockerhub-viewcount/dockerhub_lib.py |
|   undeclared | EXPERIMENTS/108-dockerhub-viewcount/results.json |
|   undeclared | EXPERIMENTS/108-dockerhub-viewcount/run.py |
|   undeclared | EXPERIMENTS/108-dockerhub-viewcount/stats.py |
|   undeclared | STATE-next-actions.md |
|   undeclared | STATE.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:23:56 | session_start | Run fresh observation experiment in a new domain per D083 - test view-count principle on a platform not yet tested |
| 2 | 19:05:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-dockerhub-viewcount/PROTOCOL.md |
| 3 | 19:05:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-dockerhub-viewcount/README.md |
| 4 | 19:05:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-dockerhub-viewcount/classify.py |
| 5 | 19:05:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-dockerhub-viewcount/dockerhub_lib.py |
| 6 | 19:05:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-dockerhub-viewcount/results.json |
| 7 | 19:05:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-dockerhub-viewcount/run.py |
| 8 | 19:05:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/108-dockerhub-viewcount/stats.py |
| 9 | 19:05:28 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 10 | 19:05:28 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 11 | 19:05:28 | doc_update | updated STATE.md |
| 12 | 19:05:28 | session_end | E108: Fresh observation on Docker Hub (container registry) - view-count principle FAILS. Tested 55 need-related vs 55 random images. G1 PASS (sample s |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-042-run-fresh-observation-experiment-in-a-ne/events.jsonl
```
