# Session 2026-10-10-013-prototype-query-time-reverse-lookup-give

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-10T14:21:15+00:00
- **Duration:** 3706.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Prototype query-time reverse lookup: given a module name, find which PyPI distribution provides it by checking candidate distributions' wheels

## Summary

Built a query-time reverse lookup prototype (pyprovides find command) that resolves 'which distribution provides this module' by checking: 1) stdlib (instant), 2) known aliases table (instant, covers sklearn->scikit-learn, cv2->opencv-python, etc.), 3) exact-name match, 4) top-N PyPI search via wheel central directory reads. Split pyprovides.py into 4 modules (constants, core, find, __init__) to stay under 300-line cap. All 17 tests pass. CLI works: 'pyprovides find sklearn' returns scikit-learn in 0.00s via alias, 'pyprovides find os' returns stdlib instantly, 'pyprovides find numpy' returns numpy via exact match.

## Next

Run a real-world evaluation: test pyprovides find against the E086 import error corpus (31 reports, 19.35% module-only) to measure actual resolution success rate and compare against 'pip install <module>' baseline

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| pyprovides/__init__.py | f5a652cdb71a | 1756 |
| pyprovides/constants.py | 71dd838310d1 | 2967 |
| pyprovides/core.py | 1b694ae41f1f | 6380 |
| pyprovides/find.py | c1e5395984c1 | 5261 |
| pyprovides/pyprovides_cli.py | 29ad9ee28f4f | 8093 |
| pyprovides/test_pyprovides.py | bf48a80850eb | 6575 |
| pyprovides/README.md | abd3efebada7 | 5387 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 2 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .pyprovides-ranked.json |
|   undeclared | pyprovides/known_aliases.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 14:21:15 | session_start | Prototype query-time reverse lookup: given a module name, find which PyPI distribution provides it by checking candidate distributions' wheels |
| 2 | 14:21:37 | milestone | Understanding current pyprovides implementation and planning query-time reverse lookup |
| 3 | 14:22:42 | milestone | Designing query-time reverse lookup: check top-N PyPI distributions for a given module name |
| 4 | 15:21:40 | artifact | wrote pyprovides/__init__.py |
| 5 | 15:21:40 | artifact | wrote pyprovides/constants.py |
| 6 | 15:21:41 | artifact | wrote pyprovides/core.py |
| 7 | 15:21:42 | artifact | wrote pyprovides/find.py |
| 8 | 15:21:42 | artifact | wrote pyprovides/pyprovides_cli.py |
| 9 | 15:21:43 | artifact | wrote pyprovides/test_pyprovides.py |
| 10 | 15:21:44 | artifact | wrote pyprovides/README.md |
| 11 | 15:23:02 | unlogged_change | changed but never declared as an artifact: .pyprovides-ranked.json |
| 12 | 15:23:02 | unlogged_change | changed but never declared as an artifact: pyprovides/known_aliases.py |
| 13 | 15:23:02 | session_end | Built a query-time reverse lookup prototype (pyprovides find command) that resolves 'which distribution provides this module' by checking: 1) stdlib ( |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-013-prototype-query-time-reverse-lookup-give/events.jsonl
```
