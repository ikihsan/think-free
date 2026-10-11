# Session 2026-10-11-023-design-and-run-fresh-observation-experim

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T14:59:19+00:00
- **Duration:** 744.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Design and run fresh observation experiment on GitHub code repositories (Option A from synthesis) to test view-count principle generalization to code repositories with star/issue metadata

## Summary

E104 completed: Fresh observation experiment on GitHub code repositories (Option A from synthesis). View-count principle does NOT generalize to code repositories using star counts as arrival metric. G1 PASS (84 need-related, 32 random), G2 FAIL (both arms 100% active at stars>100, p=1.0; continuous stars Mann-Whitney p=0.79, random median 60,771 > need-related 57,219), G3 PASS trivial, G4 PASS. Stars measure popularity/foundationality, not practitioner need arrivals. Foundational infrastructure (generic names) dominates stars over specific tools. Principle now bounded across three platform types: package repos (works), Q&A forums (works), code repos (fails). Updated STATE-next-actions.md with results.

## Next

Per D083, next session must start fresh observation in a new domain not yet tested. Remaining untested package registries: Packagist (PHP), Go module proxy, Hex.pm (Elixir), CocoaPods, JSR, Deno registry, Docker Hub. Untested Q&A forums: other Discourse instances, specialized technical forums. Or explore entirely new domain axis.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 24 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/096-rubygems-viewcount/results.json |
|   undeclared | EXPERIMENTS/096-rubygems-viewcount/run.py |
|   undeclared | EXPERIMENTS/097-stackoverflow-viewcount/run.py |
|   undeclared | EXPERIMENTS/103-rubygems-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/103-rubygems-viewcount/README.md |
|   undeclared | EXPERIMENTS/103-rubygems-viewcount/results.json |
|   undeclared | EXPERIMENTS/103-rubygems-viewcount/rubygems_classify.py |
|   undeclared | EXPERIMENTS/103-rubygems-viewcount/rubygems_stats.py |
|   undeclared | EXPERIMENTS/103-rubygems-viewcount/run.py |
|   undeclared | EXPERIMENTS/104-github-repo-viewcount/PROTOCOL.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 14:59:19 | session_start | Design and run fresh observation experiment on GitHub code repositories (Option A from synthesis) to test view-count principle generalization to code  |
| 2 | 15:07:37 | milestone | E104 completed: view-count principle fails on GitHub code repositories (star counts). G2 FAIL - both arms 100% active, random median stars higher than |
| 3 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/096-rubygems-viewcount/results.json |
| 4 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/096-rubygems-viewcount/run.py |
| 5 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/097-stackoverflow-viewcount/run.py |
| 6 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/103-rubygems-viewcount/PROTOCOL.md |
| 7 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/103-rubygems-viewcount/README.md |
| 8 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/103-rubygems-viewcount/results.json |
| 9 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/103-rubygems-viewcount/rubygems_classify.py |
| 10 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/103-rubygems-viewcount/rubygems_stats.py |
| 11 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/103-rubygems-viewcount/run.py |
| 12 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/104-github-repo-viewcount/PROTOCOL.md |
| 13 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/104-github-repo-viewcount/README.md |
| 14 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/104-github-repo-viewcount/VERDICT.md |
| 15 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/104-github-repo-viewcount/fixtures/need-related-sample.json |
| 16 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/104-github-repo-viewcount/fixtures/random-sample.json |
| 17 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/104-github-repo-viewcount/harvest.py |
| 18 | 15:11:43 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/104-github-repo-viewcount/outcome.py |
| 19 | 15:11:43 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 20 | 15:11:43 | unlogged_change | changed but never declared as an artifact: pyprovides/pyfix |
| 21 | 15:11:43 | unlogged_change | changed but never declared as an artifact: pyprovides/pyfix.fish |
| 22 | 15:11:43 | unlogged_change | changed but never declared as an artifact: pyprovides/pyfix.zsh |
| 23 | 15:11:43 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides/__main__.py |
| 24 | 15:11:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-020-continue-view-count-principle-fresh-obse/events.jsonl |
| 25 | 15:11:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-021-design-and-run-rubygems-view-count-princ/events.jsonl |
| 26 | 15:11:43 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-022-recover-context-improve-pyprovides-proto/events.jsonl |
| 27 | 15:11:43 | session_end | E104 completed: Fresh observation experiment on GitHub code repositories (Option A from synthesis). View-count principle does NOT generalize to code r |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-023-design-and-run-fresh-observation-experim/events.jsonl
```
