<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0030
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0030 — Refuse a commit that gives one finding, decision, or task identifier t

## Goal

Refuse a commit that gives one finding, decision, or task identifier two definitions, so an identifier collision between VMs cannot reach the shared base

## Why this matters

Defect 5 in STATE-defects.md is the one fleet defect still unfixed: F, D and T identifiers are allocated by reading the local tree, so two VMs in an hour take the same number. VM 0944 recorded a seventh collision on 2026-10-04 while this one was being created. Commit e6eb992 on the shared base carries two different findings both numbered F010 and no gate said so. T-0030 is the other half of the fix 0944 identified: allocating from the remote ledger stops the race at the source, a detector refuses the commit when the race happens anyway.

## Preconditions

The falsification bytes exist in history: e6eb992 is on origin/research/origin and holds two '## F010' headings in FAILURES-findings-2.md plus two '| F010 |' rows in FAILURES.md. It was renumbered by hand one commit later in 8a4ab8cef.

## Steps

1. Read the whole history and count, per commit, how many definitions each F, D and T identifier has; confirm the collision set is exactly one commit and the current tree is clean. 2. Write tools/originlib/identifiers.py to report a duplicate definition, a findings index row with no definition, a definition with no index row, and a decision entry its own index does not list. 3. Wire it as doc lint rule 7 and make sync land refuse to push a tree it would refuse. 4. Falsify: the rule must fire on e6eb992's own bytes and on no other commit in the history, and the repair commit 8a4ab8cef must be clean.

## Acceptance criteria

- [ ] The rule reports the duplicate F010 in commit e6eb992's bytes and is silent on all other commits in the history, including the current tree - [ ] A control exists that can fail: the current tree deliberately paraphrases two findings index rows, so a rule reading wording instead of duplication would flag the whole history - [ ] doc lint fails with exit 2 on a tree carrying the collision, and sync land refuses to push one - [ ] The full suite and doc lint are green - [ ] STATE-defects.md records the defect as refused before publication, with the ceiling that a detector cannot stop two VMs allocating at once

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Delete tools/originlib/identifiers.py, the rule 7 hook in doclint.py, the refusal in sync.py and tests/test_identifiers.py; the other gates are untouched by this change.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
