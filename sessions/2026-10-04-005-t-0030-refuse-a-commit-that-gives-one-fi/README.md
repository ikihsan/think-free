# Session 2026-10-04-005-t-0030-refuse-a-commit-that-gives-one-fi

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T01:16:09+00:00
- **Duration:** 3316.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `task/T-0030-instance-20260717-0947`

## Goal

T-0030: refuse a commit that gives one finding, decision or task identifier two definitions

## Summary

T-0030: an identifier collision is now refused before publication. tools/originlib/identifiers.py reports an identifier defined twice, a findings index row with no body, and a decision its own index row does not list; sync land refuses to push a tree the rule would refuse, because a collision is created by the merge and each VM's own lint sees nothing. Falsified in both directions: over all 174 commits on the base the rule reports one, e6eb992, and its hand repair is clean; removing each of three mechanisms makes the covering test fail with controls green. The control caught a draft that flagged 83 of 174 commits on wording and a decision-index regex that matched no row at all. The rule found a live desync on its first run: D030 missing from DECISIONS.md. 333 tests green.

## Next

Close the allocator half of defect 5: task new should take the next identifier from the remote claim ledger taskremote already fetches. Record the exercised Python versions, named as unclaimed work in docs/operations/vm-execution.md.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/identifiers.py | be3ca6dce2f6 | 10420 |
| tools/originlib/syncland.py | 0c7069e85874 | 6773 |
| tests/test_identifiers.py | 9a051b6e6e0b | 9938 |
| tests/test_identifier_enforcement.py | 326cae654cf8 | 6891 |
| DECISIONS-GATING.md | 39023ff6b4ba | 13954 |

## Commands

33 captured, 17 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '/tmp/opencode/falsify_ids.py'] | 0 | 586 |
| 3 | ['python3', '/tmp/opencode/sweep_ids.py'] | 1 | 41813 |
| 4 | ['python3', '/tmp/opencode/falsify_ids.py'] | 0 | 618 |
| 5 | ['python3', '/tmp/opencode/sweep_ids.py'] | 0 | 15677 |
| 6 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier', '-v'] | 1 | 4391 |
| 7 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier', '-v'] | 1 | 4031 |
| 8 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier'] | 1 | 6118 |
| 9 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier'] | 1 | 4203 |
| 10 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier'] | 1 | 5921 |
| 11 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier'] | 1 | 4124 |
| 12 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier'] | 0 | 4212 |
| 13 | ['python3', '/tmp/opencode/falsify_mutation.py'] | 1 | 1108 |
| 14 | ['python3', '/tmp/opencode/falsify_mutation.py'] | 0 | 5914 |
| 15 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 162031 |
| 16 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier or sync or landed or task_i | 0 | 1314 |
| 17 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 162610 |
| 18 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 163582 |
| 19 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 172334 |
| 20 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 166803 |
| 21 | ['python3', '/tmp/opencode/falsify_mutation.py'] | 0 | 6075 |
| 22 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'identifier'] | 0 | 4778 |
| 23 | ['python3', '/tmp/opencode/falsify_mutation.py'] | 1 | 4994 |
| 24 | ['python3', '/tmp/opencode/falsify_mutation.py'] | 0 | 5504 |
| 25 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 169705 |
| 26 | ['tools/origin', 'doc', 'lint'] | 0 | 1612 |
| 27 | ['tools/origin', 'release', 'check'] | 0 | 4031 |
| 28 | ['tools/origin', 'release', 'check'] | 2 | 5082 |
| 29 | ['tools/origin', 'release', 'check'] | 0 | 4188 |
| 30 | ['tools/origin', 'preflight'] | 2 | 2014 |
| 31 | ['tools/origin', 'session', 'verify'] | 4 | 1699 |
| 38 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 167902 |
| 39 | ['tools/origin', 'preflight'] | 2 | 2911 |
| 40 | ['tools/origin', 'task', 'verify', 'T-0030'] | 0 | 172021 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 14 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-PRACTICE.md |
|   undeclared | DECISIONS.md |
|   undeclared | RELEASE-MANIFEST.md |
|   undeclared | STATE-defects.md |
|   undeclared | STATE-history-2.md |
|   undeclared | STATE-history.md |
|   undeclared | STATE.md |
|   undeclared | docs/operations/ci.md |
|   undeclared | docs/process/multi-vm-coordination.md |
|   undeclared | tests/README.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 01:16:09 | session_start | T-0030: refuse a commit that gives one finding, decision or task identifier two definitions |
| 2 | 01:17:30 | command | $ python3 /tmp/opencode/falsify_ids.py |
| 3 | 01:18:26 | command | $ python3 /tmp/opencode/sweep_ids.py |
| 4 | 01:18:58 | command | $ python3 /tmp/opencode/falsify_ids.py |
| 5 | 01:19:14 | command | $ python3 /tmp/opencode/sweep_ids.py |
| 6 | 01:20:44 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier -v |
| 7 | 01:20:55 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier -v |
| 8 | 01:23:31 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier |
| 9 | 01:23:39 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier |
| 10 | 01:25:40 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier |
| 11 | 01:25:54 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier |
| 12 | 01:26:06 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier |
| 13 | 01:26:41 | command | $ python3 /tmp/opencode/falsify_mutation.py |
| 14 | 01:26:50 | command | $ python3 /tmp/opencode/falsify_mutation.py |
| 15 | 01:29:38 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 16 | 01:31:30 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier or sync or landed or task_index |
| 17 | 01:34:17 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 18 | 01:39:40 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 19 | 01:42:44 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 20 | 01:45:51 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 21 | 01:46:09 | command | $ python3 /tmp/opencode/falsify_mutation.py |
| 22 | 01:53:13 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k identifier |
| 23 | 01:53:36 | command | $ python3 /tmp/opencode/falsify_mutation.py |
| 24 | 01:53:46 | command | $ python3 /tmp/opencode/falsify_mutation.py |
| 25 | 01:56:46 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 26 | 01:56:53 | command | $ tools/origin doc lint |
| 27 | 01:56:57 | command | $ tools/origin release check |
| 28 | 02:01:31 | command | $ tools/origin release check |
| 29 | 02:01:50 | command | $ tools/origin release check |
| 30 | 02:01:52 | command | $ tools/origin preflight |
| 31 | 02:02:33 | command | $ tools/origin session verify |
| 32 | 02:05:17 | milestone | T-0030 gate written, falsified in both directions, docs and state updated |
| 33 | 02:05:18 | artifact | wrote tools/originlib/identifiers.py |
| 34 | 02:05:18 | artifact | wrote tools/originlib/syncland.py |
| 35 | 02:05:18 | artifact | wrote tests/test_identifiers.py |
| 36 | 02:05:18 | artifact | wrote tests/test_identifier_enforcement.py |
| 37 | 02:05:18 | artifact | wrote DECISIONS-GATING.md |
| 38 | 02:08:13 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 39 | 02:08:16 | command | $ tools/origin preflight |
| 40 | 02:11:16 | command | $ tools/origin task verify T-0030 |
| 50 | 02:11:25 | unlogged_change | changed but never declared as an artifact: tests/README.md |
| 51 | 02:11:25 | unlogged_change | changed but never declared as an artifact: tests/test_landed_work.py |
| 52 | 02:11:25 | unlogged_change | changed but never declared as an artifact: tests/test_sync.py |
| 53 | 02:11:25 | unlogged_change | changed but never declared as an artifact: tools/originlib/cli_sync.py |
| 54 | 02:11:25 | unlogged_change | changed but never declared as an artifact: tools/originlib/sync.py |
| 55 | 02:11:25 | doc_update | updated DECISIONS-GATING.md |
| 56 | 02:11:25 | doc_update | updated DECISIONS-PRACTICE.md |
| 57 | 02:11:25 | doc_update | updated DECISIONS.md |
| 58 | 02:11:25 | doc_update | updated STATE.md |
| 59 | 02:11:25 | session_end | T-0030: an identifier collision is now refused before publication. tools/originlib/identifiers.py reports an identifier defined twice, a findings inde |

_9 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-005-t-0030-refuse-a-commit-that-gives-one-fi/events.jsonl
```
