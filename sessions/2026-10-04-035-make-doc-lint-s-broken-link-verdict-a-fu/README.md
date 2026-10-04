# Session 2026-10-04-035-make-doc-lint-s-broken-link-verdict-a-fu

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T11:48:26+00:00
- **Duration:** 3035.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `task/T-0051-instance-20260717-0944`

## Goal

make doc lint's broken-link verdict a function of the repository, not of the directory the checkout sits in

## Summary

A link's verdict is now a function of the repository. doc lint rule 3 asked exists() of each candidate, so a link leaving the root was decided by what the checkout's parent directory held - measured on one probe document at two checkout locations: no finding in one, broken link in the other. That is T-0047's recorded symptom, whose note could not identify the deciding run; the run was never the variable. Containment is decided lexically with os.path.relpath, the existence check is the only filesystem read, an absolute path is caught by the same clause, and an escaping link is its own violation so annotate files it. One mutation falsifies both directions because removing the filter is the previous rule. D041 in DECISIONS-RECORDS.md (its invariant names that file, not the GATING file the task's step named), defect 19, method in gate-falsification.md. 513 tests, doc lint and preflight green. Also corrected: defect 12 pointed at D039 where the decision is D040, and STATE.md carried a byte-identical duplicate dashboard row.

## Next

State-defects.md is at 299 and ROADMAP.md at 300, so the next entry in either needs the split STATE-next-actions.md names as a task rather than an edit. The duplicated-dashboard-row class has no reader: a merge of two VMs' STATE.md edits can duplicate a row and every gate passes.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/doclint.py | 1d4e8d932273 | 9982 |
| tests/test_link_escape.py | cad25e067476 | 10983 |
| tools/mutate_link_rule.py | 3958ee0dd294 | 2715 |
| STATE-defects.md | 5d8519dfbb08 | 21662 |
| DECISIONS-RECORDS.md | 6603a2775b02 | 13852 |
| DECISIONS.md | 079e9b53b507 | 5593 |
| docs/policy/gate-falsification.md | bc95ac3daab5 | 4937 |
| docs/policy/doc-standards.md | db4bde6f9052 | 6150 |
| tests/README.md | 38eeb24e388d | 25012 |
| STATE.md | 0b4f712d1a57 | 25439 |
| ROADMAP.md | 5bae1fcc84fd | 18678 |
| tasks/T-0051-make-doc-lint-s-broken-link-verdict-a-function-o.md | e13750014d9e | 6651 |

## Commands

12 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_link_escape'] | 1 | 4597 |
| 4 | ['python3', 'tools/mutate_link_rule.py', 'apply'] | 0 | 81 |
| 5 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_link_escape'] | 1 | 4203 |
| 6 | ['python3', 'tools/mutate_link_rule.py', 'restore'] | 0 | 202 |
| 7 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_link_escape'] | 0 | 5233 |
| 8 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 253696 |
| 9 | ['tools/origin', 'doc', 'lint'] | 0 | 2303 |
| 23 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 252316 |
| 24 | ['tools/origin', 'preflight'] | 0 | 7402 |
| 25 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_link_escape', 'tests.test_doclint', 'tests.test_annotate', 'tests.test_ci_a | 0 | 14888 |
| 26 | ['tools/origin', 'doc', 'lint'] | 0 | 2245 |
| 29 | ['tools/origin', 'task', 'verify', 'T-0051'] | 0 | 16013 |

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
| 1 | 11:48:26 | session_start | make doc lint's broken-link verdict a function of the repository, not of the directory the checkout sits in |
| 2 | 11:52:24 | milestone | 5 of 10 tests fail on the unrepaired rule; the previous-rule witness passes, so the 4 in-repository controls are not vacuous |
| 3 | 11:52:30 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape |
| 4 | 11:56:45 | command | $ python3 tools/mutate_link_rule.py apply |
| 5 | 11:56:49 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape |
| 6 | 11:56:50 | command | $ python3 tools/mutate_link_rule.py restore |
| 7 | 11:56:56 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape |
| 8 | 12:03:58 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests |
| 9 | 12:04:09 | command | $ tools/origin doc lint |
| 10 | 12:04:19 | milestone | rule in place: 10/10 new tests, 513 in the suite, doc lint OK; falsified both ways by removing the containment filter (5 failures, parent-dependence r |
| 11 | 12:28:16 | artifact | wrote tools/originlib/doclint.py |
| 12 | 12:28:16 | artifact | wrote tests/test_link_escape.py |
| 13 | 12:28:17 | artifact | wrote tools/mutate_link_rule.py |
| 14 | 12:28:17 | artifact | wrote STATE-defects.md |
| 15 | 12:29:12 | artifact | wrote DECISIONS-RECORDS.md |
| 16 | 12:29:13 | artifact | wrote DECISIONS.md |
| 17 | 12:29:13 | artifact | wrote docs/policy/gate-falsification.md |
| 18 | 12:29:14 | artifact | wrote docs/policy/doc-standards.md |
| 19 | 12:29:14 | artifact | wrote tests/README.md |
| 20 | 12:29:15 | artifact | wrote STATE.md |
| 21 | 12:29:15 | artifact | wrote ROADMAP.md |
| 22 | 12:29:16 | decision | a link's verdict is a function of the repository, not of the checkout's neighbours: containment is decided lexically, the existence check is the only  |
| 23 | 12:33:39 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests |
| 24 | 12:33:55 | command | $ tools/origin preflight |
| 25 | 12:35:17 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape tests.test_doclint tests.test_annotate tests.test_ci_annotations |
| 26 | 12:35:20 | command | $ tools/origin doc lint |
| 27 | 12:37:31 | artifact | wrote tasks/T-0051-make-doc-lint-s-broken-link-verdict-a-function-o.md |
| 28 | 12:37:32 | milestone | records written: D041 in DECISIONS-RECORDS.md (the file whose invariant owns it), defect 19, the method in docs/policy/gate-falsification.md, doc-stan |
| 29 | 12:37:48 | command | $ tools/origin task verify T-0051 |
| 30 | 12:37:58 | task_rewrite | rewrote tasks/T-0051-make-doc-lint-s-broken-link-verdict-a-function-o.md (status: done) |
| 31 | 12:39:01 | doc_update | updated DECISIONS-RECORDS.md |
| 32 | 12:39:01 | doc_update | updated DECISIONS.md |
| 33 | 12:39:01 | doc_update | updated ROADMAP.md |
| 34 | 12:39:01 | doc_update | updated STATE.md |
| 35 | 12:39:01 | session_end | A link's verdict is now a function of the repository. doc lint rule 3 asked exists() of each candidate, so a link leaving the root was decided by what |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-035-make-doc-lint-s-broken-link-verdict-a-fu/events.jsonl
```
