<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0045
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-027-classify-decisions-records-md-in-the-rel
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_cli tests.test_release -q && tools/origin doc lint && tools/origin preflight
-->

# T-0045 — Run release check from preflight, and classify DECISIONS-RECORDS.md wh

## Goal

Run release check from preflight, and classify DECISIONS-RECORDS.md which T-0042 added unclassified

## Why this matters

Run 37191658964 at c9e89e1 is red on Documentation lint with one real violation: DECISIONS-RECORDS.md is tracked at the top level and classified by neither manifest table. This session added that file in T-0042 and never ran release check - T-0042's verify was the suite, doc lint and preflight, and preflight is lint + skills + sessions. So the gate that would have caught it is a gate the task never ran, which is the defect: every new root document hits this. Putting release check in preflight makes the command the protocol tells every agent to run include it.

## Preconditions

release check is a CI step already, so this adds a second cheap run rather than a new gate

## Steps

1. Classify DECISIONS-RECORDS.md in RELEASE-MANIFEST.md next to the other decision records and confirm release check exits 0.
2. Falsify first: with release check out of preflight, a repository carrying an unclassified root document must still pass preflight, which is the defect.
3. Add release check to preflight, keeping its exit code distinguishable in the failure line so a reader knows which gate failed.
4. Add a control that must stay silent: a repository that classifies every path preflights clean.
5. Update docs/operations and tests/README.md, then run the suite, doc lint and preflight.

## Acceptance criteria

- [ ] DECISIONS-RECORDS.md is classified and release check exits 0 on this repository.
- [ ] preflight fails on an unclassified root document, falsified against the pre-change code.
- [ ] preflight still passes on a repository that classifies every path.
- [ ] docs/process/session-protocol.md and tests/README.md say that a change's verify command must include every gate the change can break.
- [ ] The full suite is green.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_cli tests.test_release -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit; the manifest row and the preflight call are independent of the split they came with

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
