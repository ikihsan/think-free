# Session 2026-10-10-020-measure-pyprovides-adoption-and-evaluate

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T21:03:35+00:00
- **Duration:** 4721.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure pyprovides adoption and evaluate integrations

## Summary

Improved pyprovides resolver tool: expanded known aliases from 19 to 100+ entries (covering git, slack, protobuf, ML frameworks, web frameworks, DevOps tools, etc.), added --scan-stdout flag to fix-import for catching tracebacks printed to stdout, refactored CLI to delegate to shared fix_import module, rebuilt wheel with all changes. All 27 tests pass. Verified installed package works end-to-end for alias resolution (git -> GitPython instant via alias, cv2 -> opencv-python, etc.) and search fallback.

## Next

Test pyprovides in real developer workflows by installing in a clean environment and measuring time-to-resolution for common missing imports; consider adding automatic install flag (--install) and requirements.txt scanning

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| pyprovides/pyprovides/constants.py | 0342de5ed015 | 4611 |
| pyprovides/pyprovides/fix_import.py | 11ca93f19f1f | 6540 |
| pyprovides/pyprovides/pyprovides_cli.py | 441d17c54a79 | 6881 |
| pyprovides/setup.py | b152b0c98690 | 392 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 37 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-view-count-arrival-prototype/harvest.py |
|   undeclared | EXPERIMENTS/092-view-count-arrival-prototype/outcome.py |
|   undeclared | LICENSE |
|   undeclared | README.md |
|   undeclared | RELEASE-MANIFEST.md |
|   undeclared | STATE-next-actions.md |
|   undeclared | pyfix.zsh |
|   undeclared | pyprovides/.pyprovides-ranked.json |
|   undeclared | pyprovides/README.md |
|   undeclared | pyprovides/__init__.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:03:35 | session_start | Measure pyprovides adoption and evaluate integrations |
| 2 | 21:03:52 | milestone | Ready for adoption measurement phase |
| 3 | 22:05:04 | milestone | Fixed pyfix wrapper entry point; all 27 tests pass; verified fix-import works for alias cases |
| 4 | 22:18:22 | milestone | Rebuilt wheel with expanded alias table (100+ aliases), added --scan-stdout flag, verified installed package works |
| 5 | 22:18:29 | artifact | wrote pyprovides/pyprovides/constants.py |
| 6 | 22:18:29 | artifact | wrote pyprovides/pyprovides/fix_import.py |
| 7 | 22:18:30 | artifact | wrote pyprovides/pyprovides/pyprovides_cli.py |
| 8 | 22:18:31 | artifact | wrote pyprovides/setup.py |
| 9 | 22:22:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-view-count-arrival-prototype/harvest.py |
| 10 | 22:22:16 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-view-count-arrival-prototype/outcome.py |
| 11 | 22:22:16 | unlogged_change | changed but never declared as an artifact: LICENSE |
| 12 | 22:22:16 | unlogged_change | changed but never declared as an artifact: README.md |
| 13 | 22:22:16 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 14 | 22:22:16 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 15 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyfix.zsh |
| 16 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/.pyprovides-ranked.json |
| 17 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/README.md |
| 18 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/__init__.py |
| 19 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/_pyprovides |
| 20 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/constants.py |
| 21 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/core.py |
| 22 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/find.py |
| 23 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/fix_import.py |
| 24 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/known_aliases.py |
| 25 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyfix |
| 26 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyfix.fish |
| 27 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyproject.toml |
| 28 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides |
| 29 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides/__init__.py |
| 30 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides/core.py |
| 31 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides/find.py |
| 32 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides/known_aliases.py |
| 33 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides_cli.py |
| 34 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/test_multi_import.py |
| 35 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/test_pyprovides.py |
| 36 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/test_workflow.py |
| 37 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/test_workflow_v2.py |
| 38 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/test_workflow_v3.py |
| 39 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/tests/__init__.py |
| 40 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/tests/test_core.py |
| 41 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/tests/test_multi_import_1.py |
| 42 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/tests/test_workflow_1.py |
| 43 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/tests/test_workflow_2.py |
| 44 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/tests/test_workflow_3.py |
| 45 | 22:22:16 | unlogged_change | changed but never declared as an artifact: pyprovides/tests/workflow_results.json |
| 46 | 22:22:16 | session_end | Improved pyprovides resolver tool: expanded known aliases from 19 to 100+ entries (covering git, slack, protobuf, ML frameworks, web frameworks, DevOp |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-020-measure-pyprovides-adoption-and-evaluate/events.jsonl
```
