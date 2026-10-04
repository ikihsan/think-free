# Session 2026-10-04-012-measure-the-test-suite-on-every-cpython

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T03:30:46+00:00
- **Duration:** 7674.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure the test suite on every CPython minor from 3.8 to 3.14 and make CI keep running them (T-0034)

## Summary

T-0034 closed the gap tests/python-versions.json named in five words ('CI pins a single version'). Measuring it found two machine-fact gates rather than a clean run: the interpreter assertion (F018), which failed on all five unrecorded interpreters, and the git assertion (F019), which had CI's seven rows red because the runner ships git 2.55.0 and the record named 2.25.1 and 2.56.0 - a failure no run could report, since the log needs admin rights and the public check-runs API returns no annotations. Both are now the module's contract rather than claims about the machine, tests/test_ci_matrix.py holds the matrix to the record in both directions, and the runner's own git was measured rather than assumed. 392 tests green on 3.8.10, five portable builds and git 2.55.0; run 37180041369 green on all seven jobs with the five file-reading gates on one row.

## Next

Two gaps this session ran into, both recorded in STATE-next-actions.md: doc lint rule 7 does not read STATE-defects.md's numbering, so two VMs took defect 7 in an hour; and a red CI run still names a step and a version rather than a test, for which one check per test file is the fix. Neither VM has a task claimed.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tests/python-versions.json | 672857403b64 | 6554 |
| tests/test_ci_matrix.py | d7d63f5fd4bb | 13150 |
| .github/workflows/ci.yml | 728d88317224 | 4571 |
| sessions/2026-10-04-012-measure-the-test-suite-on-every-cpython/commands.log | 6662505a4806 | 7103 |
| tests/git-versions.json | f8f35d917b23 | 2468 |
| FAILURES-findings-4.md | be58a81cc174 | 9049 |
| tests/python-versions.json | a33307899004 | 7102 |

## Commands

13 captured, 4 non-zero exit.

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
| 24 | ['tools/origin', 'task', 'verify', 'T-0034'] | 0 | 232727 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 23 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-GATING.md |
|   undeclared | DECISIONS-PRACTICE.md |
|   undeclared | DECISIONS.md |
|   undeclared | FAILURES.md |
|   undeclared | RELEASE-MANIFEST.md |
|   undeclared | ROADMAP.md |
|   undeclared | STATE-defects.md |
|   undeclared | STATE-history-2.md |
|   undeclared | STATE-history.md |
|   undeclared | STATE-next-actions.md |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

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
| 24 | 05:38:07 | command | $ tools/origin task verify T-0034 |
| 25 | 05:38:08 | artifact | wrote tests/python-versions.json |
| 26 | 05:38:41 | unlogged_change | changed but never declared as an artifact: DECISIONS-GATING.md |
| 27 | 05:38:41 | unlogged_change | changed but never declared as an artifact: DECISIONS-PRACTICE.md |
| 28 | 05:38:41 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 29 | 05:38:41 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 30 | 05:38:41 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 31 | 05:38:41 | unlogged_change | changed but never declared as an artifact: ROADMAP.md |
| 32 | 05:38:41 | unlogged_change | changed but never declared as an artifact: STATE-defects.md |
| 33 | 05:38:41 | unlogged_change | changed but never declared as an artifact: STATE-history-2.md |
| 34 | 05:38:41 | unlogged_change | changed but never declared as an artifact: STATE-history.md |
| 35 | 05:38:41 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 36 | 05:38:41 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 37 | 05:38:41 | unlogged_change | changed but never declared as an artifact: docs/operations/ci.md |
| 38 | 05:38:41 | unlogged_change | changed but never declared as an artifact: docs/operations/doctor.md |
| 39 | 05:38:41 | unlogged_change | changed but never declared as an artifact: docs/operations/vm-execution.md |
| 40 | 05:38:41 | unlogged_change | changed but never declared as an artifact: tasks/T-0034-run-the-test-suite-on-the-python-versions-tests.md |
| 47 | 05:38:41 | unlogged_change | changed but never declared as an artifact: tests/test_pythonversions.py |
| 48 | 05:38:41 | unlogged_change | changed but never declared as an artifact: tools/originlib/versions.py |
| 49 | 05:38:41 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 50 | 05:38:41 | doc_update | updated DECISIONS-GATING.md |
| 51 | 05:38:41 | doc_update | updated DECISIONS-PRACTICE.md |
| 52 | 05:38:41 | doc_update | updated DECISIONS.md |
| 53 | 05:38:41 | doc_update | updated FAILURES.md |
| 54 | 05:38:41 | doc_update | updated ROADMAP.md |
| 55 | 05:38:41 | doc_update | updated STATE.md |
| 56 | 05:38:41 | session_end | T-0034 closed the gap tests/python-versions.json named in five words ('CI pins a single version'). Measuring it found two machine-fact gates rather th |

_6 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-012-measure-the-test-suite-on-every-cpython/events.jsonl
```
