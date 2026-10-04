# Session 2026-10-04-007-t-0032-record-the-python-versions-the-su

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T02:06:19+00:00
- **Duration:** 1191.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `task/T-0032-instance-20260717-0944`

## Goal

T-0032: record the Python versions the suite has actually run on

## Summary

T-0032: tests/python-versions.json records every interpreter the suite has actually run, each entry carrying its scope, and names the versions nobody has run (3.9-3.11, 3.13+, non-CPython, non-Linux). CI is credited with the minor version only because the run log needs admin rights. The test checks honesty clauses rather than schema and was falsified four ways first; its floor clause had a defect caught on its first run. Defect 6 is twice-partly closed: the claim exists and is checked, and nothing reads it at run time. 335 tests green; doc lint, release check and preflight exit 0.

## Next

Land this branch on the shared base with 'tools/origin sync land'. Then the reading half of defect 6 is the obvious next unclaimed item: make doctor compare this VM's git and interpreter against tests/git-versions.json and tests/python-versions.json, so an unexercised VM is warned rather than undocumented. T-0030 remains open on instance-20260717-0947.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tests/python-versions.json | ec9f3dcde6c4 | 2973 |
| tests/test_pythonversions.py | 82eac14d7734 | 4728 |
| tasks/T-0032-record-the-python-versions-the-suite-has-actuall.md | 1b7720d35ffe | 4700 |
| STATE-defects.md | ef2e05dc219a | 6477 |
| STATE-next-actions.md | 8f96b2f16710 | 5710 |
| ROADMAP.md | ea76eeb62a80 | 12754 |
| docs/operations/doctor.md | 97e74620f63b | 6899 |

## Commands

9 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_pythonversions.py', '-v'] | 1 | 377 |
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_pythonversions.py', '-v'] | 1 | 225 |
| 4 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_pythonversions.py', '-v'] | 0 | 283 |
| 5 | ['sh', '-c', '\necho "=== FALSIFICATION 1: floor claims a minor version nothing ran (3.10) ==="\npython3 -c "\nimport json\nd=json.load(open(\\"tests/ | 0 | 1600 |
| 6 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 175234 |
| 11 | ['sh', '-c', 'tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check >/dev/null; echo "release=$?"; tools/o | 0 | 8400 |
| 12 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 175801 |
| 16 | ['sh', '-c', 'tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check>/dev/null; echo "release=$?"; tools/or | 0 | 8495 |
| 17 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 173194 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 6 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-PRACTICE.md |
|   undeclared | DECISIONS.md |
|   undeclared | STATE.md |
|   undeclared | docs/operations/ci.md |
|   undeclared | docs/operations/vm-execution.md |
|   undeclared | tests/README.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:06:19 | session_start | T-0032: record the Python versions the suite has actually run on |
| 2 | 02:10:02 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_pythonversions.py -v |
| 3 | 02:10:46 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_pythonversions.py -v |
| 4 | 02:11:02 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_pythonversions.py -v |
| 5 | 02:11:10 | command | $ sh -c  echo "=== FALSIFICATION 1: floor claims a minor version nothing ran (3.10) ===" python3 -c " import json d=json.load(open(\"tests/pyt |
| 6 | 02:14:31 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 7 | 02:14:37 | milestone | python-versions.json written and falsified four ways: floor claiming 3.10, an entry with no scope, CI credited with an unreadable patch version, and a |
| 8 | 02:14:37 | artifact | wrote tests/python-versions.json |
| 9 | 02:14:37 | artifact | wrote tests/test_pythonversions.py |
| 10 | 02:14:37 | decision | record the exercised Python versions in a machine-readable file whose test checks honesty clauses, not just schema |
| 11 | 02:15:06 | command | $ sh -c tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check >/dev/null; echo "release=$?"; tools |
| 12 | 02:18:32 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 13 | 02:21:48 | artifact | wrote tasks/T-0032-record-the-python-versions-the-suite-has-actuall.md |
| 14 | 02:21:48 | artifact | wrote STATE-defects.md |
| 15 | 02:21:48 | artifact | wrote STATE-next-actions.md |
| 16 | 02:22:51 | command | $ sh -c tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check>/dev/null; echo "release=$?"; tools/ |
| 17 | 02:25:49 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 18 | 02:25:59 | artifact | wrote ROADMAP.md |
| 19 | 02:25:59 | artifact | wrote docs/operations/doctor.md |
| 20 | 02:26:10 | unlogged_change | changed but never declared as an artifact: DECISIONS-PRACTICE.md |
| 21 | 02:26:10 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 22 | 02:26:10 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 23 | 02:26:10 | unlogged_change | changed but never declared as an artifact: docs/operations/ci.md |
| 24 | 02:26:10 | unlogged_change | changed but never declared as an artifact: docs/operations/vm-execution.md |
| 25 | 02:26:10 | unlogged_change | changed but never declared as an artifact: tests/README.md |
| 26 | 02:26:10 | doc_update | updated DECISIONS-PRACTICE.md |
| 27 | 02:26:10 | doc_update | updated DECISIONS.md |
| 28 | 02:26:10 | doc_update | updated ROADMAP.md |
| 29 | 02:26:10 | doc_update | updated STATE.md |
| 30 | 02:26:10 | session_end | T-0032: tests/python-versions.json records every interpreter the suite has actually run, each entry carrying its scope, and names the versions nobody  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-007-t-0032-record-the-python-versions-the-su/events.jsonl
```
