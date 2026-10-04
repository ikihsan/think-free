<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0036
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
-->

# T-0036 — Report a duplicate defect number in STATE-defects.md as a doc lint vio

## Goal

Report a duplicate defect number in STATE-defects.md as a doc lint violation, so rule 7 stops skipping the one identifier list it does not read

## Why this matters

T-0034 and T-0035 were written on two VMs in the same hour and both took defect 7; the unpushed side renumbered by hand and nothing reported the collision. Doc lint rule 7 reads findings definitions, findings index rows and decision spans, and this file is an ordered list of bold headings with no F/D identifier in it, so it is the one document in the repository whose identifiers are checked by reading them. Named as next-actions item 2(a) and recorded in STATE-defects.md.

## Preconditions

No task holds the identifier rule; preflight green on origin/research/origin@e576e26 with 400 tests green, observed 2026-10-04.

## Steps

1. Read STATE-defects.md at e53ca23 and e701ad8 and confirm both hold defect 7 twice (the defect's own bytes, not a paraphrase). 2. Add tools/originlib/defectlist.py: a numbered list item in STATE-defects.md defines that number, and a number defined twice is an issue naming both lines. 3. A file that exists and yields no entry is itself reported, so a restructure cannot leave the rule quietly dead (D025). 4. Route doc lint and sync land through one entry point, because doclint.py is at 299 of 300 lines and cannot grow. 5. Add tests/test_defectlist.py quoting e53ca23's two entries, with controls: the current tree is clean, a prose mention is not a definition, an indented list item is not a definition, and out-of-order numbering is not a violation. 6. Sweep every commit touching STATE-defects.md: exactly e53ca23 and e701ad8 flagged, the tip not. 7. Add the wiring tests to tests/test_identifier_enforcement.py: doc lint fails and sync land refuses. 8. Run the full suite and doc lint through tools/x.

## Acceptance criteria

- [ ] STATE-defects.md and STATE-next-actions.md record the gap as closed, with its ceiling

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
```

## Rollback

git revert the two new modules, the two call sites and the new tests; nothing else imports them.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
