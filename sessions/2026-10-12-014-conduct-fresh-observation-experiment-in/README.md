# Session 2026-10-12-014-conduct-fresh-observation-experiment-in

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `failed`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T22:38:45+00:00
- **Duration:** 5780.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Conduct fresh observation experiment in a new domain per D083, following E113's matched-harvest requirement

## Summary

E117 Nix/Home Manager observation abandoned before any gate fired. What exists: 150 classified topics, a 19-probe G0 discrimination arm, and an interactive answer loop (run_assistant.py) that makes the treatment arm a manual per-topic typing session. The line itself was withdrawn at E113/F116/D105 -- the view-count domain sweep was measuring its own sampling design. Retaining classification.jsonl and g0_answers.jsonl as raw evidence, untracked; no rate, delta or verdict is claimed from either.

## Next

Do not resume E117. A hand-typed treatment arm is the structural cost of every 'can a general assistant serve this' line, and six such lines have closed on service (E062, E091, E092, E114, E115, E116). Next session works on a buildable artifact instead: a validator that refuses to emit an evaluation rate until the instrument producing it has been measured (E114 F118 verifier FP=1.00, E116 F121 key/answer mismatch, F122 invalid control arm), tested against those committed artifacts.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/117-nix-home-manager-fresh/classification.jsonl | 052e56b8e16e | 42154 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 31 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/AMENDMENT-1.md |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/PROTOCOL.md |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/README.md |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/classifier.py |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/evaluate.py |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/results.json |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/topic_classifier.py |
|   undeclared | EXPERIMENTS/115-classifier-coverage-prototype/vocab_expander.py |
|   undeclared | EXPERIMENTS/117-cicd-failure-fresh-observation/PROTOCOL.md |
|   undeclared | EXPERIMENTS/117-cicd-failure-fresh-observation/results.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 22:38:45 | session_start | Conduct fresh observation experiment in a new domain per D083, following E113's matched-harvest requirement |
| 2 | 22:47:31 | milestone | Starting E117 Nix/Home Manager fresh observation - fetching remaining topics from Discourse |
| 3 | 23:44:18 | milestone | Continuing active session: completing Nix/Home Manager E117 experiment by answering 129 answerable-class topics |
| 4 | 23:44:27 | artifact | wrote EXPERIMENTS/117-nix-home-manager-fresh/classification.jsonl |
| 5 | 00:15:04 | milestone | abandoned the E117 Nix/Home Manager run: its G0 discrimination arm was collected (19 probes) but the treatment arm requires a hand-typed answer per to |
| 6 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/AMENDMENT-1.md |
| 7 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/PROTOCOL.md |
| 8 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/README.md |
| 9 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/classifier.py |
| 10 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/evaluate.py |
| 11 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/results.json |
| 12 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/topic_classifier.py |
| 13 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/115-classifier-coverage-prototype/vocab_expander.py |
| 14 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-cicd-failure-fresh-observation/PROTOCOL.md |
| 15 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-cicd-failure-fresh-observation/results.json |
| 16 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-cicd-failure-fresh-observation/run.py |
| 17 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/PROTOCOL.md |
| 18 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/answer_batch.py |
| 19 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/answerable_topics.json |
| 20 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/classify.py |
| 21 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/classify_all.py |
| 22 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/fetch.py |
| 23 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/g0_answers.jsonl |
| 24 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/g0_probes.md |
| 25 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-nix-home-manager-fresh/run_assistant.py |
| 26 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/PROTOCOL.md |
| 27 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/broken_spec.txt |
| 28 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/results.json |
| 29 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/run.py |
| 30 | 00:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/123-cicd-log-diagnosis/PROTOCOL.md |
| 31 | 00:15:05 | unlogged_change | changed but never declared as an artifact: results.json |
| 32 | 00:15:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-009-run-install-test-falsification-for-e068/events.jsonl |
| 33 | 00:15:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-010-design-and-implement-a-fresh-observation/events.jsonl |
| 34 | 00:15:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-011-implement-and-run-e123-ci-cd-build-log-f/events.jsonl |
| 35 | 00:15:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-012-identify-and-design-a-fresh-observation/events.jsonl |
| 36 | 00:15:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-013-design-and-run-a-fresh-observation-exper/events.jsonl |
| 37 | 00:15:05 | session_end | E117 Nix/Home Manager observation abandoned before any gate fired. What exists: 150 classified topics, a 19-probe G0 discrimination arm, and an intera |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-014-conduct-fresh-observation-experiment-in/events.jsonl
```
