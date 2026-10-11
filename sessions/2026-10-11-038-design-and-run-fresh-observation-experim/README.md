# Session 2026-10-11-038-design-and-run-fresh-observation-experim

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T17:51:21+00:00
- **Duration:** 2471.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Design and run fresh observation experiment testing view-count principle on GitHub code repositories using star counts and issue activity as arrival metrics

## Summary

Designed and ran E107 fresh observation experiment testing view-count principle on GitHub code repositories (top 50 by stars). G1 FAIL (68.2% arrival metric), G2 PASS (15.4% need prevalence), G3 FAIL (54% unserved, Wilson upper 65.7%), G4 PASS (16 repos). Population skewed to awesome-lists/educational resources, arrival metric too sparse, unserved classification flawed without comment analysis. Principle does NOT generalize to this population. Results recorded in EXPERIMENTS/107-github-repos-viewcount/ with protocol, classifier, runner, results.json, and README.md. Updated STATE.md and STATE-next-actions.md with E107 findings. Resolved merge conflicts with parallel VM's different E107 experiment (star-count based).

## Next

Per D083, start fresh observation in a new untested domain. Candidate domains: Reddit personal finance forums, 3D printing communities, or GitHub Discussions (different from code repos). Must avoid rehashing closed ground.

## Artifacts

_none_

## Commands

1 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/107-github-repos-viewcount/run.py'] | 3 | 81357 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 25 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/0xx-cpan-viewcount/experiment.py |
|   undeclared | EXPERIMENTS/0xx-cpan-viewcount/results.json |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/results.json |
|   undeclared | EXPERIMENTS/100-viewcount-cre/results.json |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/README.md |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/analyze.py |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/classify.py |
|   undeclared | EXPERIMENTS/107-github-repos-viewcount/harvest.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:51:21 | session_start | Design and run fresh observation experiment testing view-count principle on GitHub code repositories using star counts and issue activity as arrival m |
| 2 | 17:55:56 | command | $ python3 EXPERIMENTS/107-github-repos-viewcount/run.py |
| 3 | 18:00:14 | milestone | E107 experiment completed: G1 FAIL (68.2% arrival), G2 PASS (15.4% need prevalence), G3 FAIL (54% unserved, Wilson upper 65.7%), G4 PASS (16 repos wit |
| 4 | 18:32:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-cpan-viewcount/experiment.py |
| 5 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-cpan-viewcount/results.json |
| 6 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
| 7 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 8 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-viewcount-cre/results.json |
| 9 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/PROTOCOL.md |
| 10 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/README.md |
| 11 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/analyze.py |
| 12 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/classify.py |
| 13 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/harvest.py |
| 14 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/raw_data.json |
| 15 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/results.json |
| 16 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/107-github-repos-viewcount/run.py |
| 17 | 18:32:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/phase-decision.json |
| 18 | 18:32:32 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-results.md |
| 19 | 18:32:32 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 20 | 18:32:32 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 21 | 18:32:32 | unlogged_change | changed but never declared as an artifact: THINK_FREE_SUMMARY.md |
| 22 | 18:32:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-037-synthesize-view-count-principle-across-e/events.jsonl |
| 23 | 18:32:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-038-finalize-view-count-principle-research-a/events.jsonl |
| 24 | 18:32:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-040-execute-t-0091-fresh-observation-experim/commands.log |
| 25 | 18:32:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-040-execute-t-0091-fresh-observation-experim/events.jsonl |
| 26 | 18:32:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-041-declare-artifacts-from-e107-experiment-a/events.jsonl |
| 27 | 18:32:32 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 28 | 18:32:32 | unlogged_change | changed but never declared as an artifact: tasks/T-0091-run-a-fresh-observation-experiment-testing-the-v.md |
| 29 | 18:32:32 | doc_update | updated STATE.md |
| 30 | 18:32:32 | session_end | Designed and ran E107 fresh observation experiment testing view-count principle on GitHub code repositories (top 50 by stars). G1 FAIL (68.2% arrival  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-038-design-and-run-fresh-observation-experim/events.jsonl
```
