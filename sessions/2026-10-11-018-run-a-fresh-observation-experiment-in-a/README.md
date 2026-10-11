# Session 2026-10-11-018-run-a-fresh-observation-experiment-in-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T12:10:42+00:00
- **Duration:** 544.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run a fresh observation experiment in a new domain per D083, testing view-count principle boundaries

## Summary

Ran fresh observation experiment E102 testing view-count principle on NuGet (.NET package registry). All four predeclared gates PASS: G1 retrieval (40/40), G2 separation (p=1.7e-14, Cliff's delta=0.996), G3 effect magnitude (Wilson LB=0.912 > 0.60), G4 arrival field coverage (100%). Need-related packages median 7.8M downloads vs random 195K (~40x). The view-count principle generalizes to NuGet, joining PyPI and NPM as supported registries. Caveat: sampling bias toward official Microsoft packages in need-related arm inflates effect size.

## Next

Per D083, next session must start fresh observation in a new domain not yet tested. Candidate domains: Packagist (PHP), Go module proxy, Docker Hub, VS Code Marketplace, RubyGems, Pub.dev (Dart/Flutter), CocoaPods, or a non-registry domain like Reddit technical communities, Arduino Library Manager, or a new structured fault code domain.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/102-nuget-viewcount/PROTOCOL.md | 2864625f9c22 | 5557 |
| EXPERIMENTS/102-nuget-viewcount/run.py | 90bb94876904 | 13120 |
| EXPERIMENTS/102-nuget-viewcount/results.json | afcbde8d7b24 | 35605 |
| EXPERIMENTS/102-nuget-viewcount/README.md | 964a51e8fc3c | 3408 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/102-nuget-viewcount/run.py', '--gate', '--need', '40', '--random', '40'] | 0 | 5717 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 2 |
| redactions applied to command output | 0 |
|   undeclared | results.json |
|   error | FAILURES.md was not updated although the session recorded experiment_result |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:10:42 | session_start | Run a fresh observation experiment in a new domain per D083, testing view-count principle boundaries |
| 2 | 12:14:59 | command | $ python3 EXPERIMENTS/102-nuget-viewcount/run.py --gate --need 40 --random 40 |
| 3 | 12:18:59 | artifact | wrote EXPERIMENTS/102-nuget-viewcount/PROTOCOL.md |
| 4 | 12:19:06 | artifact | wrote EXPERIMENTS/102-nuget-viewcount/run.py |
| 5 | 12:19:17 | artifact | wrote EXPERIMENTS/102-nuget-viewcount/results.json |
| 6 | 12:19:24 | artifact | wrote EXPERIMENTS/102-nuget-viewcount/README.md |
| 7 | 12:19:31 | experiment_result | View-count principle generalizes to NuGet: all four gates PASS. Need-related packages (configuration, auth, logging, database, caching, etc.) have ~40 |
| 8 | 12:19:46 | unlogged_change | changed but never declared as an artifact: results.json |
| 9 | 12:19:46 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 10 | 12:19:46 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 11 | 12:19:46 | session_end | Ran fresh observation experiment E102 testing view-count principle on NuGet (.NET package registry). All four predeclared gates PASS: G1 retrieval (40 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-018-run-a-fresh-observation-experiment-in-a/events.jsonl
```
