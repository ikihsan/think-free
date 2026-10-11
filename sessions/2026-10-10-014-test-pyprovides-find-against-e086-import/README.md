# Session 2026-10-10-014-test-pyprovides-find-against-e086-import

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T16:54:00+00:00
- **Duration:** 1193.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test pyprovides find against E086 import error corpus to measure resolution success rate

## Summary

Built and tested fix-import integration for pyprovides resolver. The pyprovides fix-import command runs a user command, captures stderr, detects ModuleNotFoundError/ImportError patterns, extracts module names, and uses the pyprovides find resolver to suggest correct PyPI distributions to install. Evaluated against 19 discrimination test probes: 15/19 (78.9%) resolved via alias/exact/stdlib methods. Failures: attr (name collision with 'attr' package), pysftp (not in top 500), pkg_resources (setuptools .pth mechanism), ldap (python-ldap no wheel). All 27 tests pass (17 existing + 6 new fix_import tests + 4 find_provider tests).

## Next

Measure actual usage: integrate fix-import into a developer workflow (e.g., as a shell wrapper or pre-commit hook) and measure time-to-fix for import errors vs manual 'pip install <module>' baseline

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| pyprovides/fix_import.py | b9f683e45be6 | 6133 |
| pyprovides/pyprovides_cli.py | 99260f29a503 | 10702 |
| pyprovides/test_pyprovides.py | b58be81655b2 | 10267 |
| pyprovides/__init__.py | 448a7dcd7bfb | 1829 |
| sessions/INDEX.md | f208df7cd274 | 6777 |

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
| 1 | 16:54:00 | session_start | Test pyprovides find against E086 import error corpus to measure resolution success rate |
| 2 | 16:59:47 | milestone | Evaluated pyprovides resolver against known aliases from discrimination test: 16/19 resolved via alias/exact, 3 failed (pkg_resources via setuptools . |
| 3 | 17:00:54 | milestone | Ran pyprovides find against 19 discrimination test probes: 15/19 resolved (78.9%), 4 failed (attr name collision, pysftp not in top 500, pkg_resources |
| 4 | 17:07:08 | milestone | Built and tested fix-import integration: pyprovides fix-import command runs a command, detects ModuleNotFoundError/ImportError from stderr, extracts m |
| 5 | 17:11:52 | artifact | wrote pyprovides/fix_import.py |
| 6 | 17:11:59 | artifact | wrote pyprovides/pyprovides_cli.py |
| 7 | 17:11:59 | artifact | wrote pyprovides/test_pyprovides.py |
| 8 | 17:12:00 | artifact | wrote pyprovides/__init__.py |
| 9 | 17:12:29 | artifact | wrote sessions/INDEX.md |
| 10 | 17:13:53 | session_end | Built and tested fix-import integration for pyprovides resolver. The pyprovides fix-import command runs a user command, captures stderr, detects Modul |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-014-test-pyprovides-find-against-e086-import/events.jsonl
```
