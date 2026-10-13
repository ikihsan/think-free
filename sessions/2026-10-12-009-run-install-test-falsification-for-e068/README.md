# Session 2026-10-12-009-run-install-test-falsification-for-e068

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T16:19:22+00:00
- **Duration:** 3233.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run install-test falsification for E068 ArXiv spec generator: test whether generated pinned requirements.txt files produce working environments in clean venvs against A1 ground truth repos

## Summary

E122 install-test falsification for E068 ArXiv spec generator completed. Experiment ran and all gates FAILED (K1, K3, K4) except K2 (trivial pass with 0% gap). Both generated and ground truth specs fail to install on Python 3.8 due to version incompatibility (numpy, torch require Python 3.9+). No A3/A4 pure-Python repos were successfully tested. The generator's version resolution does not check Python version compatibility. Verdict: FAIL - the spec generator does not produce working environments on available Python version.

## Next

Start fresh observation experiment in a new domain per D083

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 4 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/PROTOCOL.md |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/broken_spec.txt |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/results.json |
|   undeclared | EXPERIMENTS/122-e068-install-test-falsification/run.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:19:22 | session_start | Run install-test falsification for E068 ArXiv spec generator: test whether generated pinned requirements.txt files produce working environments in cle |
| 2 | 17:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/PROTOCOL.md |
| 3 | 17:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/broken_spec.txt |
| 4 | 17:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/results.json |
| 5 | 17:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/122-e068-install-test-falsification/run.py |
| 6 | 17:13:16 | session_end | E122 install-test falsification for E068 ArXiv spec generator completed. Experiment ran and all gates FAILED (K1, K3, K4) except K2 (trivial pass with |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-009-run-install-test-falsification-for-e068/events.jsonl
```
