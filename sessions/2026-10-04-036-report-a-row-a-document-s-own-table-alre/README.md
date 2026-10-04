# Session 2026-10-04-036-report-a-row-a-document-s-own-table-alre

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T12:47:26+00:00
- **Duration:** 3283.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `task/T-0052-instance-20260717-0944`

## Goal

report a row a document's own table already contains, so a merge that concatenates two VMs' edits cannot pass every gate

## Summary

A hand-authored document may not contain the same table row twice. Commit eff1126 - a rebase of one VM's T-0047 branch onto a base the other had already extended - carried STATE.md with a byte-identical second copy of its Implemented (2) dashboard row, one per VM, and every gate passed; the next session removed it by hand after finding it by reading. Measured: 47 documents repeat a table row and all 47 are generated session reports, where an artifact listed once per event is the truth, so the exemption reads the generated-by marker in the document rather than a path or an extension. Falsified both ways - the rule removed reports nothing on eff1126, the exemption removed reports 47 findings on a clean tree - because too few and too many are the same mistake one clause apart. D043, defect 20, method in gate-falsification.md. 524 tests, doc lint and preflight green. doclint.py hit 308 and the rule moved to doclint_table.py rather than the file losing a fact.

## Next

STATE-defects.md is at exactly 300 again and its structural repair is still a task rather than an edit: the numbered list cannot be split without defectlist.py reading more than one file. ROADMAP.md is at 300. The next entry in either costs prose, and the third session in a row has paid that way.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/doclint.py | 554d329ec48d | 10743 |
| tools/originlib/doclint_table.py | 515c4dc382cb | 4084 |
| tests/test_table_rows.py | 078d974342cc | 11483 |
| tools/mutate_table_rule.py | d1bbf2c46fe0 | 3416 |
| STATE-defects.md | 55a541568738 | 21707 |
| DECISIONS-RECORDS.md | 792a88250f7a | 16114 |
| DECISIONS.md | e3d956546eb4 | 5599 |
| docs/policy/gate-falsification.md | d82742b4faf6 | 6538 |
| docs/policy/doc-standards.md | 06c649fb67ae | 6642 |
| tests/README.md | ace0bc4e3912 | 25613 |
| tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md | 049db7400d55 | 7026 |

## Commands

15 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'tools/mutate_table_rule.py', 'apply', 'no-rule'] | 1 | 113 |
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_table_rows'] | 0 | 6508 |
| 4 | ['python3', 'tools/mutate_table_rule.py', 'restore'] | 0 | 94 |
| 5 | ['python3', 'tools/mutate_table_rule.py', 'apply', 'no-rule'] | 0 | 95 |
| 6 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_table_rows'] | 1 | 6628 |
| 7 | ['python3', 'tools/mutate_table_rule.py', 'restore'] | 0 | 100 |
| 8 | ['python3', 'tools/mutate_table_rule.py', 'apply', 'no-generated-exempt'] | 0 | 111 |
| 9 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_table_rows'] | 1 | 6826 |
| 10 | ['python3', 'tools/mutate_table_rule.py', 'restore'] | 0 | 97 |
| 11 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_table_rows'] | 0 | 6747 |
| 13 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 265780 |
| 14 | ['tools/origin', 'doc', 'lint'] | 0 | 2615 |
| 27 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 266273 |
| 28 | ['tools/origin', 'preflight'] | 0 | 8091 |
| 29 | ['tools/origin', 'task', 'verify', 'T-0052'] | 0 | 17282 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 3 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | ROADMAP.md |
|   undeclared | STATE.md |
|   undeclared | tests/test_doclint.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:47:26 | session_start | report a row a document's own table already contains, so a merge that concatenates two VMs' edits cannot pass every gate |
| 2 | 13:00:23 | command | $ python3 tools/mutate_table_rule.py apply no-rule |
| 3 | 13:00:30 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_table_rows |
| 4 | 13:00:31 | command | $ python3 tools/mutate_table_rule.py restore |
| 5 | 13:00:58 | command | $ python3 tools/mutate_table_rule.py apply no-rule |
| 6 | 13:01:05 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_table_rows |
| 7 | 13:01:05 | command | $ python3 tools/mutate_table_rule.py restore |
| 8 | 13:01:26 | command | $ python3 tools/mutate_table_rule.py apply no-generated-exempt |
| 9 | 13:01:33 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_table_rows |
| 10 | 13:01:33 | command | $ python3 tools/mutate_table_rule.py restore |
| 11 | 13:01:40 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_table_rows |
| 12 | 13:01:56 | milestone | 11/11 new tests green; both mutations fail them - the rule removed reports nothing on eff1126, the generated-document exemption removed reports 47 fin |
| 13 | 13:06:22 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests |
| 14 | 13:06:35 | command | $ tools/origin doc lint |
| 15 | 13:35:06 | artifact | wrote tools/originlib/doclint.py |
| 16 | 13:35:07 | artifact | wrote tools/originlib/doclint_table.py |
| 17 | 13:35:07 | artifact | wrote tests/test_table_rows.py |
| 18 | 13:35:08 | artifact | wrote tools/mutate_table_rule.py |
| 19 | 13:35:08 | artifact | wrote STATE-defects.md |
| 20 | 13:35:09 | artifact | wrote DECISIONS-RECORDS.md |
| 21 | 13:35:09 | artifact | wrote DECISIONS.md |
| 22 | 13:35:10 | artifact | wrote docs/policy/gate-falsification.md |
| 23 | 13:35:11 | artifact | wrote docs/policy/doc-standards.md |
| 24 | 13:35:11 | artifact | wrote tests/README.md |
| 25 | 13:35:12 | artifact | wrote tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md |
| 26 | 13:35:12 | decision | a hand-authored record says each thing once, and the exemption reads the document's own generated-by marker rather than a path, because the distinguis |
| 27 | 13:39:39 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests |
| 28 | 13:39:54 | command | $ tools/origin preflight |
| 29 | 13:40:35 | command | $ tools/origin task verify T-0052 |
| 30 | 13:40:35 | task_rewrite | rewrote tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md (status: done) |
| 31 | 13:42:09 | unlogged_change | changed but never declared as an artifact: ROADMAP.md |
| 32 | 13:42:09 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 33 | 13:42:09 | unlogged_change | changed but never declared as an artifact: tests/test_doclint.py |
| 34 | 13:42:09 | doc_update | updated DECISIONS-RECORDS.md |
| 35 | 13:42:09 | doc_update | updated DECISIONS.md |
| 36 | 13:42:09 | doc_update | updated ROADMAP.md |
| 37 | 13:42:09 | doc_update | updated STATE.md |
| 38 | 13:42:09 | session_end | A hand-authored document may not contain the same table row twice. Commit eff1126 - a rebase of one VM's T-0047 branch onto a base the other had alrea |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-036-report-a-row-a-document-s-own-table-alre/events.jsonl
```
