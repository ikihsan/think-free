<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0043
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
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

- [ ] doc lint exits 0 with identifiers.py under 250 lines.
- [ ] identifiers.report() returns the same lines as the pre-split output on this repository, in the same order, byte for byte.
- [ ] The three modules import without a cycle and the identifier suites are green.
- [ ] The full suite is green.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_identifiers tests.test_identifier_enforcement tests.test_decision_header tests.test_defectlist -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commits; the move is a relocation and the rebase that made the file over the cap is already on the base

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
