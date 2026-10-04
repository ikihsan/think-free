<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0043
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-025-split-tools-originlib-identifiers-py-at
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_identifiers tests.test_identifier_enforcement tests.test_decision_header tests.test_defectlist -q && tools/origin doc lint && tools/origin preflight
-->

# T-0043 — Split tools/originlib/identifiers.py so doc lint passes again, one mod

## Goal

Split tools/originlib/identifiers.py so doc lint passes again, one module per record whose index must agree with its bodies

## Why this matters

doc lint on the shared base fails today: tools/originlib/identifiers.py is 307 of 300 permitted lines. This VM added 15 lines to it in T-0042 and instance-20260717-0944 added 26 in T-0040; each was under the cap alone and the merge concatenated them. STATE-next-actions.md already records that the next check added to this file has to split it, and the merge is what made it next. Red CI on every push until it is fixed.

## Preconditions

The identifier rule is read through tools/originlib/idcheck.py, so a move inside the package changes no gate's behaviour

## Steps

1. Move the findings-index agreement check into tools/originlib/findingindex.py and the decisions-index agreement check into tools/originlib/decisionindex.py, each carrying its own patterns and the module docstring that describes it.
2. Leave definitions, task definitions, duplicate detection and report() in identifiers.py, which is what the module is named for.
3. Update the three call sites that reached into identifiers internals: decisionheader's import of declarations, and the two references in tests/test_identifier_enforcement.py.
4. Record the pre-split output on this repository so the move can be shown to change nothing, then run the identifier suites, the full suite and doc lint through tools/x.

## Acceptance criteria

- [x] doc lint exits 0 with identifiers.py under 250 lines. 173, with `findingindex` at 94 and `decisionindex` at 108.
- [x] identifiers.report() returns the same lines as the pre-split output on this repository, in the same order, byte for byte. The comparison is on a fixture tree built from `d451169`, where the report is 28 lines long rather than empty — an empty report on the tip would have been a vacuous control, which is the failure F010 is about. `diff` of before against after is empty, captured in this session's `commands.log`.
- [x] The three modules import without a cycle and the identifier suites are green. 56 tests in the four identifier suites.
- [x] The full suite is green. 469 tests in 258s on Python 3.8.10, git 2.25.1, `observed` 2026-10-04.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_identifiers tests.test_identifier_enforcement tests.test_decision_header tests.test_defectlist -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commits; the move is a relocation and the rebase that made the file over the cap is already on the base

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The line cap was crossed by a merge, not by an edit.** This VM added 15 lines
to `identifiers.py` in T-0042 and `instance-20260717-0944` added 26 in T-0040.
Each file was under 300 alone; `sync land` concatenated the two diffs and
produced 307. `STATE-next-actions.md` had already recorded that the next check
added to this file has to split it, and the merge is what made it next. The
general form is the one the stale-generated-file defect recorded four times: two
VMs each working correctly against a rule the other cannot see.

**The merge was the only red thing about it, which the public annotations say.**
Run `37189825232` at `ea3bfb5` is red on all seven rows and its check-runs
annotations carry 11 each, naming
`test_annotate.GateTest.test_a_clean_gate_emits_nothing_at_all` and, in the
message, `tools/originlib/identifiers.py: 307 lines exceeds the 300-line cap`.
That is T-0040's own work making the failure readable without admin rights for
the first time, on the very run it was written to prevent. The annotation's
structured `path` is `.github` rather than the file to open, so the location
travels in the text; recorded in `STATE-next-actions.md` item 3 as `observed`,
with the cause not determined.

**The split is by record, not by size.** `identifiers` keeps what a definition is
and whether one number means two things; `findingindex` holds `FAILURES.md`'s
table to the findings; `decisionindex` holds `DECISIONS.md`'s rows to the
decisions. The two checks have the same shape and different tables, which is the
argument for not sharing a file: one file holding both grows by half each time a
check is added to either, and it is what happened here.

**A relocation cannot be falsified by mutation, so it was falsified by
equivalence.** The honest claim about a move is that the output did not change,
which is checkable and was checked: 28 lines before, 28 lines after, `diff`
empty. Running the comparison on this repository's tip instead would have been
vacuous, because a correct tree reports nothing at all.

**One record defect, this session's own.** The work commit used `git add -A`,
which swept the session report `session finish` had just rewritten into itself,
so the `session: … finished (worked)` commit landed empty while its message
claims it carries the session. Recorded where the next session reads it, in
`docs/process/session-protocol.md`, rather than only here — the same reason
DECISIONS.md records a constraint in the log and not just in the state file.
