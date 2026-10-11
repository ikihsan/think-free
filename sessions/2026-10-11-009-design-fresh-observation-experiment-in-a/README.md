# Session 2026-10-11-009-design-fresh-observation-experiment-in-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T09:36:18+00:00
- **Duration:** 1361.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Design fresh observation experiment in a new domain per D083, avoiding re-tested ground

## Summary

E101 completed: Fresh observation in new domain (Hugging Face Hub ML model registry) per D083. View-count principle tested on ML model registry — G1 PASS (241 need-related, 700 random models retrieved), G2 FAIL (p=0.089, need-related active 12.4% vs random 8.6%), G3 FAIL (Wilson LB=0.089). Principle does not generalize to ML model registries. STATE-next-actions.md updated with E101 results.

## Next

Per D083, next session must start fresh observation in another new domain not yet tested. Consider: container registries (Docker Hub), IDE extension marketplaces (VS Code), scientific paper repositories, or other platforms with exposable arrival metadata.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 44 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/fixtures/need-related-sample.json |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/fixtures/random-sample.json |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/generate_fixtures.py |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/harvest.py |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/outcome.py |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/results/results.json |
|   undeclared | EXPERIMENTS/101-huggingface-viewcount/test_gates.py |
|   undeclared | STATE-next-actions.md |
|   undeclared | sessions/2026-10-09-012-explore-fresh-observations-on-non-softwa/commands.log |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:36:18 | session_start | Design fresh observation experiment in a new domain per D083, avoiding re-tested ground |
| 2 | 09:53:46 | milestone | E101 completed: view-count principle does not generalize to Hugging Face Hub (G1 PASS, G2 FAIL p=0.089, G3 FAIL LB=0.089) |
| 3 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/PROTOCOL.md |
| 4 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/fixtures/need-related-sample.json |
| 5 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/fixtures/random-sample.json |
| 6 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/generate_fixtures.py |
| 7 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/harvest.py |
| 8 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/outcome.py |
| 9 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/results/results.json |
| 10 | 09:59:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/101-huggingface-viewcount/test_gates.py |
| 11 | 09:59:00 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 12 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-012-explore-fresh-observations-on-non-softwa/commands.log |
| 13 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-012-explore-fresh-observations-on-non-softwa/events.jsonl |
| 14 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-013-continue-view-count-measurement-investig/events.jsonl |
| 15 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-014-fresh-observation-in-a-new-non-software/commands.log |
| 16 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-014-fresh-observation-in-a-new-non-software/events.jsonl |
| 17 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-017-document-e065-e067-findings-and-decide-o/events.jsonl |
| 18 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-018-fresh-observation-in-a-new-domain-per-d0/commands.log |
| 19 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-018-fresh-observation-in-a-new-domain-per-d0/events.jsonl |
| 20 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-020-fresh-observation-in-a-new-non-software/events.jsonl |
| 21 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-021-fresh-observation-in-new-domain-laborato/events.jsonl |
| 22 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-022-fresh-observation-in-new-domain-medical/events.jsonl |
| 23 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-001-fresh-observation-in-new-domain-aviation/events.jsonl |
| 24 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-002-fresh-observation-in-new-domain-industri/events.jsonl |
| 25 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-003-fresh-observation-in-new-domain-building/events.jsonl |
| 26 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-004-falsify-the-e081-e087-view-count-general/commands.log |
| 27 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-004-falsify-the-e081-e087-view-count-general/events.jsonl |
| 28 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-005-measure-whether-e064-s-package-name-fals/events.jsonl |
| 29 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-008-measure-import-error-population-asking-w/events.jsonl |
| 30 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-010-record-e090-hand-classification-results/events.jsonl |
| 31 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-011-measure-real-python-import-error-reports/events.jsonl |
| 32 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-013-prototype-query-time-reverse-lookup-give/commands.log |
| 33 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-014-fresh-observation-in-aviation-maintenanc/events.jsonl |
| 34 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-016-package-pyprovides-for-distribution-and/events.jsonl |
| 35 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-017-package-pyprovides-for-distribution-and/events.jsonl |
| 36 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-018-finalize-pyprovides-packaging-for-distri/events.jsonl |
| 37 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-019-publish-pyprovides-to-pypi-and-measure-a/events.jsonl |
| 38 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-020-measure-pyprovides-adoption-and-evaluate/events.jsonl |
| 39 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-021-package-pyprovides-resolver-for-pypi-dis/events.jsonl |
| 40 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-022-prepare-pyprovides-for-pypi-publication/events.jsonl |
| 41 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-001-measure-pyprovides-resolver-correctness/commands.log |
| 42 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-001-measure-pyprovides-resolver-correctness/events.jsonl |
| 43 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-002-land-e100-evidence-repair-the-gitignore/commands.log |
| 44 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-002-land-e100-evidence-repair-the-gitignore/events.jsonl |
| 45 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-003-fresh-observation-in-medical-device-alar/commands.log |
| 46 | 09:59:00 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-003-fresh-observation-in-medical-device-alar/events.jsonl |
| 47 | 09:59:00 | session_end | E101 completed: Fresh observation in new domain (Hugging Face Hub ML model registry) per D083. View-count principle tested on ML model registry — G1 P |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-009-design-fresh-observation-experiment-in-a/events.jsonl
```
