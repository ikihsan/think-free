# Session 2026-10-12-012-identify-and-design-a-fresh-observation

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T18:27:21+00:00
- **Duration:** 7391.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Identify and design a fresh observation experiment in a new domain after view-count sweep stop (E113/F116)

## Summary

Built classifier coverage prototype (E115) achieving 78.6% coverage (2.8x improvement over E113's 28%), G0/G2 pass. G3 fails on matched harvest by design (stratified pool removes signal). Amendment-1 documents the design issue.

## Next

Test classifier on unmatched harvest to validate view-count effect preservation, or apply to fresh domain observation

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/115-classifier-coverage-prototype/README.md | 9d0b1107437e | 2563 |
| EXPERIMENTS/115-classifier-coverage-prototype/PROTOCOL.md | 4d305923467a | 3181 |
| EXPERIMENTS/115-classifier-coverage-prototype/AMENDMENT-1.md | bfd41442af98 | 2615 |
| EXPERIMENTS/115-classifier-coverage-prototype/topic_classifier.py | e31dfc65e926 | 19517 |
| EXPERIMENTS/115-classifier-coverage-prototype/vocab_expander.py | 5a553e9493c2 | 7198 |
| EXPERIMENTS/115-classifier-coverage-prototype/classifier.py | 44d59c78fcfc | 6621 |
| EXPERIMENTS/115-classifier-coverage-prototype/evaluate.py | 20c4fdba5d9e | 9888 |
| EXPERIMENTS/115-classifier-coverage-prototype/results.json | e0b4f9d62ccd | 1218 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 15 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/117-nix-home-manager-fresh/PROTOCOL.md |
|   undeclared | EXPERIMENTS/117-nix-home-manager-fresh/classification.jsonl |
|   undeclared | EXPERIMENTS/117-nix-home-manager-fresh/classify.py |
|   undeclared | EXPERIMENTS/117-nix-home-manager-fresh/fetch.py |
|   undeclared | EXPERIMENTS/117-nix-home-manager-fresh/g0_answers.jsonl |
|   undeclared | EXPERIMENTS/117-nix-home-manager-fresh/g0_probes.md |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/PROTOCOL.md |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/broken_spec.txt |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/results.json |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/run.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:27:21 | session_start | Identify and design a fresh observation experiment in a new domain after view-count sweep stop (E113/F116) |
| 2 | 19:27:27 | milestone | Designing classifier prototype with coverage guarantees to address E113's 28% coverage binding constraint |
| 3 | 20:18:15 | milestone | Classifier prototype achieves 78.6% coverage (2.8x improvement over 28%), G0/G2 pass, G3 fails on matched harvest due to design |
| 4 | 20:18:49 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/README.md |
| 5 | 20:18:50 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/PROTOCOL.md |
| 6 | 20:18:51 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/AMENDMENT-1.md |
| 7 | 20:18:51 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/topic_classifier.py |
| 8 | 20:18:52 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/vocab_expander.py |
| 9 | 20:18:53 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/classifier.py |
| 10 | 20:18:54 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/evaluate.py |
| 11 | 20:22:29 | artifact | wrote EXPERIMENTS/115-classifier-coverage-prototype/results.json |
| 12 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/PROTOCOL.md |
| 13 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/classification.jsonl |
| 14 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/classify.py |
| 15 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/fetch.py |
| 16 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/g0_answers.jsonl |
| 17 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/g0_probes.md |
| 18 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/PROTOCOL.md |
| 19 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/broken_spec.txt |
| 20 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/results.json |
| 21 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/run.py |
| 22 | 20:30:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/123-cicd-log-diagnosis/PROTOCOL.md |
| 23 | 20:30:32 | unlogged_change | changed but never declared as an artifact: results.json |
| 24 | 20:30:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-009-run-install-test-falsification-for-e068/events.jsonl |
| 25 | 20:30:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-010-design-and-implement-a-fresh-observation/events.jsonl |
| 26 | 20:30:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-011-implement-and-run-e123-ci-cd-build-log-f/events.jsonl |
| 27 | 20:30:32 | session_end | Built classifier coverage prototype (E115) achieving 78.6% coverage (2.8x improvement over E113's 28%), G0/G2 pass. G3 fails on matched harvest by des |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-012-identify-and-design-a-fresh-observation/events.jsonl
```
