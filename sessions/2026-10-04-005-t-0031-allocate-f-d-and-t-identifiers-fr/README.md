# Session 2026-10-04-005-t-0031-allocate-f-d-and-t-identifiers-fr

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T01:31:01+00:00
- **Duration:** 1979.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `task/T-0031-instance-20260717-0944`

## Goal

T-0031: allocate F, D and T identifiers from the shared base, not from this working tree

## Summary

T-0031: F, D and T identifiers are now allocated from origin/<base> plus the working tree, and every command that hands out a number prints the record it read. Falsified against the defect's own bytes first: a clone behind the base returned T-0002 where the base already defined it, and a deleted task file recycled its number. The first run also caught two defects in the implementation under test. Two further defects surfaced from running the task's own verification: session start wrote its report before its first event, so doc lint could not pass while a session was open; and cli.py and tasks.py passed the 300-line cap, so the parser and the task template moved to their own modules. 329 tests green; doc lint, release check and preflight exit 0. Ceiling unchanged in kind: two VMs allocating between their own fetches still collide, and T-0030's detector is what catches that.

## Next

Land this branch on the shared base with 'tools/origin sync land', then pick up the remaining unclaimed item: the Python equivalent of tests/git-versions.json (defect 6), which docs/operations/vm-execution.md names as unclaimed. T-0030 remains open on instance-20260717-0947; do not start its detector half here.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/idalloc.py | 4ff22de52cb9 | 10543 |
| tests/test_idalloc.py | cfd333576e09 | 7794 |
| tools/originlib/cli_args.py | bacecbc698df | 11080 |
| tools/originlib/tasktemplate.py | c32c928c4875 | 918 |
| docs/reference/identifier-allocation.md | f8e8231bc76a | 4006 |
| STATE-next-actions.md | f895f9d06d1d | 5308 |
| tools/originlib/session.py | 1446a423395f | 8058 |
| tests/test_doclint.py | 9869d80dc717 | 10132 |
| tasks/T-0031-allocate-f-d-and-t-identifiers-from-the-shared-b.md | 9b90733eef91 | 5372 |
| ROADMAP.md | 8eb9126fbe83 | 12245 |
| tests/README.md | 246932991b9e | 6521 |
| RELEASE-MANIFEST.md | 6d56a6de5b61 | 4447 |

## Commands

16 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_idalloc.py', '-v'] | 1 | 11946 |
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_idalloc.py', '-v'] | 0 | 14390 |
| 4 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 181726 |
| 5 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 179011 |
| 6 | ['sh', '-c', 'tools/origin id next T; tools/origin id next F; tools/origin id next D; tools/origin id next Q; echo "exit=$?"'] | 0 | 3023 |
| 13 | ['sh', '-c', 'tools/origin doc lint; echo "lint exit=$?"; tools/origin session verify; git log --oneline -1'] | 0 | 2310 |
| 14 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_doclint.py', '-v'] | 1 | 6296 |
| 15 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_doclint.py', '-k', 'OpenSession', | 1 | 1113 |
| 16 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_doclint.py', '-v'] | 0 | 6411 |
| 17 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-p', 'test_doclint.py', '-k', 'OpenSession'] | 1 | 1149 |
| 24 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 179588 |
| 25 | ['sh', '-c', 'tools/origin doc index; tools/origin doc lint --quiet; echo "lint exit=$?"; tools/origin release check; echo "release exit=$?"; tools/or | 0 | 8716 |
| 26 | ['sh', '-c', 'tools/origin doc index; tools/origin doc lint --quiet; echo "lint exit=$?"; tools/origin release check; echo "release exit=$?"'] | 0 | 7426 |
| 27 | ['sh', '-c', 'tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check >/dev/null; echo "release=$?"; tools/o | 0 | 8875 |
| 28 | ['sh', '-c', 'tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check >/dev/null; echo "release=$?"; wc -l S | 0 | 6196 |
| 29 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 178927 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 12 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-PRACTICE.md |
|   undeclared | DECISIONS.md |
|   undeclared | STATE-defects.md |
|   undeclared | STATE.md |
|   undeclared | docs/process/multi-vm-coordination.md |
|   undeclared | docs/process/task-lifecycle.md |
|   undeclared | docs/reference/cli-reference.md |
|   undeclared | tools/originlib/cli.py |
|   undeclared | tools/originlib/cli_repo.py |
|   undeclared | tools/originlib/cli_task.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 01:31:01 | session_start | T-0031: allocate F, D and T identifiers from the shared base, not from this working tree |
| 2 | 01:33:12 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_idalloc.py -v |
| 3 | 01:34:54 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_idalloc.py -v |
| 4 | 01:40:05 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 5 | 01:44:21 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 6 | 01:44:30 | command | $ sh -c tools/origin id next T; tools/origin id next F; tools/origin id next D; tools/origin id next Q; echo "exit=$?" |
| 7 | 01:44:53 | milestone | falsified: the stale-clone test returns T-0002 against the unfixed allocator and T-0003 after the repair; 327 tests green |
| 8 | 01:44:53 | milestone | cli.py split into cli_args.py and the task template into tasktemplate.py to stay under the 300-line cap |
| 9 | 01:44:53 | artifact | wrote tools/originlib/idalloc.py |
| 10 | 01:44:53 | artifact | wrote tests/test_idalloc.py |
| 11 | 01:44:53 | artifact | wrote tools/originlib/cli_args.py |
| 12 | 01:44:53 | artifact | wrote tools/originlib/tasktemplate.py |
| 13 | 01:47:00 | command | $ sh -c tools/origin doc lint; echo "lint exit=$?"; tools/origin session verify; git log --oneline -1 |
| 14 | 01:48:34 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_doclint.py -v |
| 15 | 01:49:11 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_doclint.py -k OpenSession -v |
| 16 | 01:49:49 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_doclint.py -v |
| 17 | 01:49:54 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -p test_doclint.py -k OpenSession |
| 18 | 01:50:23 | note | stash@{0} on this worktree is session 040's leftover (a stale mid-stream state of a session whose session_end is already committed at seq 117). Not ap |
| 19 | 01:50:23 | decision | allocate F, D and T identifiers from origin/<base> rather than from the working tree, and print the record every number was read from |
| 20 | 01:50:35 | artifact | wrote docs/reference/identifier-allocation.md |
| 21 | 01:50:35 | artifact | wrote STATE-next-actions.md |
| 22 | 01:50:35 | artifact | wrote tools/originlib/session.py |
| 23 | 01:50:35 | artifact | wrote tests/test_doclint.py |
| 24 | 01:54:11 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 25 | 01:57:29 | command | $ sh -c tools/origin doc index; tools/origin doc lint --quiet; echo "lint exit=$?"; tools/origin release check; echo "release exit=$?"; tools/ |
| 26 | 01:58:06 | command | $ sh -c tools/origin doc index; tools/origin doc lint --quiet; echo "lint exit=$?"; tools/origin release check; echo "release exit=$?" |
| 27 | 01:58:48 | command | $ sh -c tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check >/dev/null; echo "release=$?"; tools |
| 28 | 02:00:10 | command | $ sh -c tools/origin doc index; tools/origin doc lint --quiet; echo "lint=$?"; tools/origin release check >/dev/null; echo "release=$?"; wc -l |
| 29 | 02:03:42 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 30 | 02:03:49 | artifact | wrote tasks/T-0031-allocate-f-d-and-t-identifiers-from-the-shared-b.md |
| 31 | 02:03:49 | artifact | wrote ROADMAP.md |
| 32 | 02:03:49 | artifact | wrote tests/README.md |
| 33 | 02:03:49 | artifact | wrote RELEASE-MANIFEST.md |
| 34 | 02:04:00 | unlogged_change | changed but never declared as an artifact: DECISIONS-PRACTICE.md |
| 35 | 02:04:00 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 36 | 02:04:00 | unlogged_change | changed but never declared as an artifact: STATE-defects.md |
| 37 | 02:04:00 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 38 | 02:04:00 | unlogged_change | changed but never declared as an artifact: docs/process/multi-vm-coordination.md |
| 39 | 02:04:00 | unlogged_change | changed but never declared as an artifact: docs/process/task-lifecycle.md |
| 40 | 02:04:00 | unlogged_change | changed but never declared as an artifact: docs/reference/cli-reference.md |
| 41 | 02:04:00 | unlogged_change | changed but never declared as an artifact: tools/originlib/cli.py |
| 42 | 02:04:00 | unlogged_change | changed but never declared as an artifact: tools/originlib/cli_repo.py |
| 43 | 02:04:00 | unlogged_change | changed but never declared as an artifact: tools/originlib/cli_task.py |
| 44 | 02:04:00 | unlogged_change | changed but never declared as an artifact: tools/originlib/taskops.py |
| 45 | 02:04:00 | unlogged_change | changed but never declared as an artifact: tools/originlib/tasks.py |
| 46 | 02:04:00 | doc_update | updated DECISIONS-PRACTICE.md |
| 47 | 02:04:00 | doc_update | updated DECISIONS.md |
| 48 | 02:04:00 | doc_update | updated ROADMAP.md |
| 49 | 02:04:00 | doc_update | updated STATE.md |
| 50 | 02:04:00 | session_end | T-0031: F, D and T identifiers are now allocated from origin/<base> plus the working tree, and every command that hands out a number prints the record |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-005-t-0031-allocate-f-d-and-t-identifiers-fr/events.jsonl
```
