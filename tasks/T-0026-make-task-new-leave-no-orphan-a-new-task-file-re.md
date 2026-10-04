<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0026
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0026 — Make task new leave no orphan: a new task file regenerates tasks/INDEX

## Goal

Make task new leave no orphan: a new task file regenerates tasks/INDEX.md so the Documentation lint step cannot fail on a task that was only created

## Why this matters

Two real CI runs failed on 2026-10-03 for exactly this (37163434868, 37163438950): this VM ran the cheapest sequence the tooling offers - task new, commit, push - and the orphan rule then rejected the tree because tasks/INDEX.md still predated the new file. The defect is not that lint is strict; it is that the command that creates the document does not update the index that makes it reachable. Every other state change in the fleet flow that touches a generated file regenerates it, so this one is an omission, not a policy.

## Preconditions

The generated-file check already compares committed bytes with what the generator produces, so the fix is testable without a new gate. Nothing here invents a rule; it removes a sequence that breaks an existing one.

## Steps

1. Falsification first (D025). Kill gate: on a fresh fixture repository, 'origin task new' followed by 'origin doc lint' must exit 0 with no manual 'doc index' in between. Against the current code it exits 2 with 'orphan document'. Second assertion: the bytes of tasks/INDEX.md on disk equal render_tasks_index() the moment the task exists. 2. Add tasks.write_index(), which renders and writes only when the content changes, and call it from create, claim and transition - the three paths that change a row in that index. 3. Test the three paths, plus the negative control: a file created outside the tooling is still an orphan. 4. Docs: task-lifecycle.md, cli-reference, STATE-defects.md, ROADMAP.md.

## Acceptance criteria

- [ ] After 'origin task new' in a clean repository, 'tools/origin doc lint' exits 0 with no intervening 'doc index'.
- [ ] tasks/INDEX.md on disk equals render_tasks_index() immediately after create, claim and complete, without a manual regeneration.
- [ ] A file that no command created is still reported as an orphan: the rule stays, only the omission is fixed.
- [ ] The kill gate fails against the pre-change code, captured not asserted.
- [ ] Full suite, doc lint, release check, skills check and session verify all exit 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Revert tools/originlib/{tasks,taskops}.py and the new tests. tasks/INDEX.md content is unchanged by the revert - the generator is the same, only who calls it changes - so no committed file needs regenerating.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
