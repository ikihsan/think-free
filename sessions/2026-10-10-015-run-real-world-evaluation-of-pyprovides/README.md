# Session 2026-10-10-015-run-real-world-evaluation-of-pyprovides

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T18:49:59+00:00
- **Duration:** 1296.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Run real-world evaluation of pyprovides against E086 import error corpus to measure resolution success rate vs pip install baseline

## Summary

Evaluated pyprovides fix-import in developer workflow. Built pyfix wrapper script and tested against 3 alias cases (cv2->opencv-python, psycopg2->psycopg2-binary, MySQLdb->mysqlclient). Key findings: pyfix correctly suggests correct distribution for all alias cases (100% suggestion accuracy). For psycopg2 (only case that installs without system dependencies), pyfix achieves 2.44x speedup vs manual baseline (7.8s vs 19.0s) by eliminating package-name search time (15s -> 2s). cv2 and MySQLdb fail to install due to missing system dependencies (pkg-config, OpenGL, MySQL client libs) - not a pyfix limitation. Multi-import test shows pyfix detects first ModuleNotFoundError and suggests fix; Python stops at first import error so only one suggestion per run.

## Next

Consider packaging pyprovides for distribution (PyPI, pipx, Homebrew). Next: evaluate whether to build shell integration (e.g., fish/zsh function that wraps python) for seamless workflow integration, or focus on editor/IDE integration where import errors are surfaced.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| pyprovides/test_workflow.py | 1b8f95054b7f | 7334 |
| pyprovides/test_workflow_v3.py | cf8e90c5c662 | 7578 |
| pyprovides/workflow_results_v2.json | ade57d4123e6 | 714 |
| pyprovides/pyfix | a358e1d20e5d | 315 |
| pyprovides/test_workflow_v2.py | 21cdfcfb657a | 9714 |
| pyprovides/workflow_results.json | a1eac7d3c9b3 | 5753 |
| pyprovides/test_multi_import.py | 6f02eebd3b4b | 1737 |
| pyprovides/workflow_results_v3.json | 69b65843e272 | 10610 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:49:59 | session_start | Run real-world evaluation of pyprovides against E086 import error corpus to measure resolution success rate vs pip install baseline |
| 2 | 18:56:23 | milestone | Created pyfix wrapper script for pyprovides fix-import integration |
| 3 | 19:08:20 | artifact | wrote pyprovides/test_workflow.py |
| 4 | 19:08:21 | artifact | wrote pyprovides/test_workflow_v3.py |
| 5 | 19:08:21 | artifact | wrote pyprovides/workflow_results_v2.json |
| 6 | 19:08:22 | artifact | wrote pyprovides/pyfix |
| 7 | 19:08:22 | artifact | wrote pyprovides/test_workflow_v2.py |
| 8 | 19:08:22 | artifact | wrote pyprovides/workflow_results.json |
| 9 | 19:08:22 | artifact | wrote pyprovides/test_multi_import.py |
| 10 | 19:08:23 | artifact | wrote pyprovides/workflow_results_v3.json |
| 11 | 19:11:36 | session_end | Evaluated pyprovides fix-import in developer workflow. Built pyfix wrapper script and tested against 3 alias cases (cv2->opencv-python, psycopg2->psyc |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-015-run-real-world-evaluation-of-pyprovides/events.jsonl
```
