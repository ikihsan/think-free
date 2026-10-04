# Session 2026-10-04-012-measure-the-test-suite-on-every-cpython

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `opencode`
- **Started:** 2026-10-04T03:30:46+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure the test suite on every CPython minor from 3.8 to 3.14 and make CI keep running them (T-0034)

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tests/python-versions.json | 672857403b64 | 6554 |
| tests/test_ci_matrix.py | d7d63f5fd4bb | 13150 |
| .github/workflows/ci.yml | 728d88317224 | 4571 |
| sessions/2026-10-04-012-measure-the-test-suite-on-every-cpython/commands.log | 6662505a4806 | 7103 |
| tests/git-versions.json | f8f35d917b23 | 2468 |
| FAILURES-findings-4.md | be58a81cc174 | 9049 |

## Commands

12 captured, 4 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['/tmp/opencode/fetch-pythons.sh'] | 0 | 48401 |
| 4 | ['env', 'PYTHONPATH=tools:tests', '/tmp/opencode/pythons/cpython-3.14.2/bin/python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 177087 |
| 5 | ['env', 'PYTHONPATH=tools:tests', '/tmp/opencode/pythons/cpython-3.9.23/bin/python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 261317 |
| 6 | ['/tmp/opencode/falsify-ci-matrix.sh'] | 0 | 1144 |
| 7 | ['/tmp/opencode/falsify-ci-matrix.sh'] | 0 | 1471 |
| 8 | ['/tmp/opencode/measure-all.sh'] | 0 | 1075716 |
| 15 | ['tools/origin', 'task', 'verify', 'T-0034'] | 0 | 234486 |
| 16 | ['env', 'PYTHONPATH=tools:tests', '/tmp/opencode/pythons/cpython-3.12.11/bin/python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 193735 |
| 17 | ['env', 'PATH=/tmp/opencode/conda/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bi | 1 | 292203 |
| 18 | ['env', 'PATH=/tmp/opencode/conda/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bi | 0 | 334221 |
| 19 | ['env', 'PATH=/tmp/opencode/conda/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bi | 2 | 280287 |
| 23 | ['tools/origin', 'task', 'verify', 'T-0034'] | 0 | 238070 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 03:30:46 | session_start | Measure the test suite on every CPython minor from 3.8 to 3.14 and make CI keep running them (T-0034) |
| 2 | 03:31:31 | milestone | T-0034 claimed on instance-20260717-0947; the first claim named 0944 by mistake and was released and re-claimed with the reason recorded in the ledger |
| 3 | 03:32:28 | command | $ /tmp/opencode/fetch-pythons.sh |
| 4 | 03:55:41 | command | $ env PYTHONPATH=tools:tests /tmp/opencode/pythons/cpython-3.14.2/bin/python3 -m unittest discover -s tests -t tests |
| 5 | 04:00:32 | command | $ env PYTHONPATH=tools:tests /tmp/opencode/pythons/cpython-3.9.23/bin/python3 -m unittest discover -s tests -t tests |
| 6 | 04:16:03 | command | $ /tmp/opencode/falsify-ci-matrix.sh |
| 7 | 04:16:17 | command | $ /tmp/opencode/falsify-ci-matrix.sh |
| 8 | 04:34:33 | command | $ /tmp/opencode/measure-all.sh |
| 9 | 04:40:58 | artifact | wrote tests/python-versions.json |
| 10 | 04:40:58 | artifact | wrote tests/test_ci_matrix.py |
| 11 | 04:40:59 | artifact | wrote .github/workflows/ci.yml |
| 12 | 04:40:59 | artifact | wrote sessions/2026-10-04-012-measure-the-test-suite-on-every-cpython/commands.log |
| 13 | 04:41:06 | decision | CI runs one matrix row per CPython minor from 3.8 to 3.14, the five file-reading gates stay guarded to one row, and tests/test_ci_matrix.py holds the  |
| 14 | 04:41:06 | experiment_result | the suite failed on all five interpreters the exercised-version record had never named, on a T-0033 test that asserted this interpreter is in the reco |
| 15 | 04:45:05 | command | $ tools/origin task verify T-0034 |
| 16 | 04:53:31 | command | $ env PYTHONPATH=tools:tests /tmp/opencode/pythons/cpython-3.12.11/bin/python3 -m unittest discover -s tests -t tests |
| 17 | 05:07:33 | command | $ env PATH=/tmp/opencode/conda/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/sn |
| 18 | 05:17:10 | command | $ env PATH=/tmp/opencode/conda/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/sn |
| 19 | 05:22:30 | command | $ env PATH=/tmp/opencode/conda/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/sn |
| 20 | 05:23:00 | artifact | wrote tests/git-versions.json |
| 21 | 05:23:00 | artifact | wrote FAILURES-findings-4.md |
| 22 | 05:23:01 | decision | the portable form of a gate that reads a record is to assert about the artefacts and state the environment's gaps as not_exercised data, rather than a |
| 23 | 05:26:59 | command | $ tools/origin task verify T-0034 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-012-measure-the-test-suite-on-every-cpython/events.jsonl
```
