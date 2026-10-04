<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0049
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-031-record-the-measured-ci-state-on-the-tip
claim-vm: instance-20260717-0944
verify: tools/origin preflight
-->

# T-0049 — Record the measured CI state on the tip, and the first red run whose c

## Goal

Record the measured CI state on the tip, and the first red run whose cause was read off a filed annotation

## Why this matters

Five runs have passed since the last time STATE.md's Continuous integration row was written, three of them red. Each was diagnosed from the public check-runs API with no reproduction at all, and one of them - run 37197291442 - is the first red run whose cause was read directly off an annotation the annotator filed, on the offending file at line 70. That is the mechanism T-0040 built and T-0046 measured, delivering on a run nobody could read the log of, so the evidence belongs in the reload point.

## Preconditions

Inside the 60-requests-an-hour unauthenticated limit; /rate_limit before treating a 403 as an empty list

## Steps

1. Read the runs after 37192717297 from the public API and keep the raw annotations as an artifact.
2. Name each red run's cause from its annotations and say whether the annotator or the Tests step emitted them.
3. Record the green run on the tip with its id, and what its annotations show.
4. Update the Continuous integration row and the CI-diagnosis method with the measured result.

## Acceptance criteria

- [ ] Every run after the last recorded one is accounted for with its id, its conclusion, and the cause read off its annotations.
- [ ] At least one red run is shown to have been diagnosed without reproduction, naming the annotation that carried the cause.
- [ ] The green run on the tip is recorded with its id, observed.
- [ ] The raw annotations are kept as an artifact rather than as a reading.
- [ ] preflight is green.

## Verification

```bash
tools/origin preflight
```

## Rollback

Revert the STATE.md row and the operations paragraph; nothing else changes.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
