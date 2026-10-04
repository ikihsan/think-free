# Session 2026-10-04-034-separate-the-line-cap-exemption-from-rec

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T11:45:49+00:00
- **Duration:** 6565.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Separate the line-cap exemption from reconciliation so a data-file edit cannot pass undeclared (T-0050)

## Summary

Closed defect 12's stated false negative (T-0050, D042, F022): a data file's suffix no longer decides whether a session declared it, the claim ledger and vendor/hashes.json are declared by the bytes their writers wrote, and the change was priced before it was made at 72 (session, path) pairs over 17 paths.

## Next

The 50 closed sessions that appended to tasks/CLAIMS.jsonl now report a file they cannot declare, and nothing reads a closed stream. Either a gate reads a closed stream's task_rewrite events and reports the mismatch, or that debt is written into the defect list as permanent. Also open: T-0052 on the other VM, and the next unclaimed item in STATE-next-actions.md.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/declaredwrite.py | f25cef3b3010 | 4150 |
| tools/originlib/taskindex.py | 54ecf4954607 | 3503 |
| tools/originlib/doclint.py | a5a0f435b73f | 9318 |
| tools/originlib/reconcile.py | 9e774810881d | 7754 |
| tools/originlib/tasks.py | bad06a480f7e | 9035 |
| tools/originlib/taskops.py | 33cb8112dd83 | 6677 |
| tools/originlib/skillsync.py | 456065613fed | 10988 |
| tools/sweep_unlogged_data.py | c23c8c292f61 | 8295 |
| tests/test_unlogged_data.py | b0007f007aa2 | 11988 |
| tests/test_task_rewrite.py | 2f11610cb59a | 11410 |
| tests/test_task_rewrite_recorded.py | 28a4933b00ed | 5057 |
| tests/README.md | 0b66c811d41e | 26479 |
| docs/process/session-protocol.md | 310d51ceee4c | 12663 |
| STATE.md | c7fb303cba32 | 27177 |
| STATE-defects.md | b49ffec12dd8 | 21667 |
| STATE-next-actions.md | 7bffab0766c7 | 17089 |
| FAILURES.md | 5fc3b10dd6a8 | 5815 |
| FAILURES-findings-5.md | e183a1048bc2 | 5816 |
| DECISIONS.md | 8aa70120ad37 | 5593 |
| DECISIONS-SESSIONS.md | 9ae17380693e | 15660 |
| tasks/T-0050-separate-the-line-cap-exemption-from-reconciliat.md | f0a5c2b79b85 | 3386 |
| RELEASE-MANIFEST.md | 2dbca6aea2b4 | 4565 |
| ROADMAP.md | a67c716fcc3e | 19116 |
| ROADMAP.md | a67c716fcc3e | 19116 |

## Commands

59 captured, 25 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['python3', '/tmp/opencode/sweep_unlogged.py'] | 0 | 524 |
| 5 | ['python3', '/tmp/opencode/sweep_unlogged.py'] | 0 | 1510 |
| 6 | ['python3', '/tmp/opencode/sweep_unlogged.py'] | 0 | 4997 |
| 7 | ['python3', '/tmp/opencode/sweep_unlogged.py'] | 0 | 6037 |
| 8 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py', '-v'] | 1 | 7700 |
| 9 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py', '-v'] | 1 | 8800 |
| 10 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py', '-v'] | 1 | 8097 |
| 11 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py', '-v'] | 1 | 7310 |
| 12 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py'] | 1 | 8033 |
| 13 | ['python3', '-'] | 0 | 808 |
| 14 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py'] | 0 | 9532 |
| 15 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 1 | 311698 |
| 16 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 1 | 318335 |
| 17 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_task_rewrite.py'] | 1 | 8680 |
| 18 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_task_rewrite.py'] | 1 | 8389 |
| 19 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_task_rewrite.py'] | 0 | 8911 |
| 20 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py'] | 1 | 8234 |
| 21 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_unlogged_data.py'] | 0 | 10218 |
| 22 | ['python3', 'tools/sweep_unlogged_data.py'] | 0 | 5616 |
| 23 | ['python3', 'tools/sweep_unlogged_data.py', '--all'] | 0 | 6515 |
| 24 | ['tools/origin', 'doc', 'lint'] | 2 | 2696 |
| 25 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_task_rewrite*.py'] | 0 | 8911 |
| 26 | ['tools/origin', 'doc', 'lint'] | 0 | 2607 |
| 27 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 305432 |
| 28 | ['tools/origin', 'preflight'] | 0 | 8030 |
| 30 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_decision*.py'] | 0 | 4087 |
| 31 | ['tools/origin', 'doc', 'lint'] | 0 | 2592 |
| 32 | ['tools/origin', 'doc', 'index'] | 0 | 923 |
| 33 | ['tools/origin', 'doc', 'lint'] | 0 | 2527 |
| 55 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 302604 |
| 56 | ['tools/origin', 'preflight'] | 2 | 8085 |
| 58 | ['tools/origin', 'preflight'] | 0 | 8019 |
| 59 | ['python3', 'tools/sweep_unlogged_data.py'] | 0 | 5817 |
| 60 | ['tools/origin', 'sync', 'land'] | 1 | 2582 |
| 61 | ['tools/origin', 'doc', 'lint'] | 2 | 4305 |
| 62 | ['tools/origin', 'doc', 'lint'] | 2 | 3211 |
| 63 | ['tools/origin', 'doc', 'lint'] | 2 | 2715 |
| 64 | ['tools/origin', 'doc', 'lint'] | 2 | 3314 |
| 65 | ['tools/origin', 'doc', 'lint'] | 2 | 2693 |
| 66 | ['tools/origin', 'doc', 'lint'] | 0 | 2998 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 9 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-RECORDS.md |
|   undeclared | docs/policy/doc-standards.md |
|   undeclared | docs/policy/gate-falsification.md |
|   undeclared | sessions/2026-10-04-035-make-doc-lint-s-broken-link-verdict-a-fu/commands.log |
|   undeclared | sessions/2026-10-04-035-make-doc-lint-s-broken-link-verdict-a-fu/events.jsonl |
|   undeclared | tasks/T-0051-make-doc-lint-s-broken-link-verdict-a-function-o.md |
|   undeclared | tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md |
|   undeclared | tests/test_link_escape.py |
|   undeclared | tools/mutate_link_rule.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:45:49 | session_start | Separate the line-cap exemption from reconciliation so a data-file edit cannot pass undeclared (T-0050) |
| 2 | 11:46:04 | task_rewrite | rewrote tasks/T-0050-separate-the-line-cap-exemption-from-reconciliat.md (status: claimed) |
| 3 | 11:46:31 | task_rewrite | rewrote tasks/T-0050-separate-the-line-cap-exemption-from-reconciliat.md (status: claimed) |
| 4 | 11:47:13 | command | $ python3 /tmp/opencode/sweep_unlogged.py |
| 5 | 11:47:25 | command | $ python3 /tmp/opencode/sweep_unlogged.py |
| 6 | 11:47:49 | command | $ python3 /tmp/opencode/sweep_unlogged.py |
| 7 | 11:48:24 | command | $ python3 /tmp/opencode/sweep_unlogged.py |
| 8 | 11:51:48 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py -v |
| 9 | 11:52:01 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py -v |
| 10 | 12:05:45 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py -v |
| 11 | 12:05:58 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py -v |
| 12 | 12:10:36 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py |
| 13 | 12:11:26 | command | $ python3 - |
| 14 | 12:12:31 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py |
| 15 | 12:17:55 | command | $ python3 -m unittest discover -s tests |
| 16 | 12:23:23 | command | $ python3 -m unittest discover -s tests |
| 17 | 12:24:13 | command | $ python3 -m unittest discover -s tests -p test_task_rewrite.py |
| 18 | 12:26:40 | command | $ python3 -m unittest discover -s tests -p test_task_rewrite.py |
| 19 | 12:27:11 | command | $ python3 -m unittest discover -s tests -p test_task_rewrite.py |
| 20 | 12:27:29 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py |
| 21 | 12:28:06 | command | $ python3 -m unittest discover -s tests -p test_unlogged_data.py |
| 22 | 12:30:28 | command | $ python3 tools/sweep_unlogged_data.py |
| 23 | 12:30:57 | command | $ python3 tools/sweep_unlogged_data.py --all |
| 24 | 12:31:12 | command | $ tools/origin doc lint |
| 25 | 12:33:35 | command | $ python3 -m unittest discover -s tests -p test_task_rewrite*.py |
| 26 | 12:33:57 | command | $ tools/origin doc lint |
| 27 | 12:39:09 | command | $ python3 -m unittest discover -s tests |
| 28 | 12:40:00 | command | $ tools/origin preflight |
| 29 | 12:40:59 | milestone | T-0050 repair in: suffix exemption split from reconciliation, ledger and vendor hashes declared by bytes, sweep committed; 521 tests green, preflight  |
| 30 | 12:47:53 | command | $ python3 -m unittest discover -s tests -p test_decision*.py |
| 31 | 12:50:37 | command | $ tools/origin doc lint |
| 32 | 12:53:59 | command | $ tools/origin doc index |
| 33 | 12:54:02 | command | $ tools/origin doc lint |
| 34 | 12:54:18 | artifact | wrote tools/originlib/declaredwrite.py |
| 35 | 12:54:19 | artifact | wrote tools/originlib/taskindex.py |
| 36 | 12:54:20 | artifact | wrote tools/originlib/doclint.py |
| 37 | 12:54:20 | artifact | wrote tools/originlib/reconcile.py |
| 38 | 12:54:21 | artifact | wrote tools/originlib/tasks.py |
| 39 | 12:54:21 | artifact | wrote tools/originlib/taskops.py |
| 40 | 12:54:22 | artifact | wrote tools/originlib/skillsync.py |
| 98 | 13:35:15 | unlogged_change | changed but never declared as an artifact: tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md |
| 99 | 13:35:15 | unlogged_change | changed but never declared as an artifact: tests/test_link_escape.py |
| 100 | 13:35:15 | unlogged_change | changed but never declared as an artifact: tools/mutate_link_rule.py |
| 101 | 13:35:15 | doc_update | updated DECISIONS-RECORDS.md |
| 102 | 13:35:15 | doc_update | updated DECISIONS-SESSIONS.md |
| 103 | 13:35:15 | doc_update | updated DECISIONS.md |
| 104 | 13:35:15 | doc_update | updated FAILURES.md |
| 105 | 13:35:15 | doc_update | updated ROADMAP.md |
| 106 | 13:35:15 | doc_update | updated STATE.md |
| 107 | 13:35:15 | session_end | Closed defect 12's stated false negative (T-0050, D042, F022): a data file's suffix no longer decides whether a session declared it, the claim ledger  |

_57 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-034-separate-the-line-cap-exemption-from-rec/events.jsonl
```
