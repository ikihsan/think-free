<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0025
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: grep -q '37165413909' STATE.md && tools/origin doc lint
-->

# T-0025 — Record the measured result of the pushed CI run for T-0024 in STATE.md

## Goal

Record the measured result of the pushed CI run for T-0024 in STATE.md and close the standing CI claim

## Why this matters

STATE.md's next action 1 has said since T-0020 that local green is not the same claim as a green run, and that no pushed run had been observed since. Two CI runs at 23:58 on 2026-10-03 failed (37163434868, 37163438950) and the two for 9e865a4 at 00:35 on 2026-10-04 succeeded (37165405776, 37165413909), all six steps green. The failures are the D029 defect biting a real run: the clock passed midnight UTC between the commit and the runner, so every committed generated file became stale. Both facts belong in the record, because the next agent otherwise has to rediscover that the gate is date-sensitive by pushing and watching it fail.

## Preconditions

The pushed commit must be reachable from origin/research/origin and its run readable through the public Actions API, as session 029 established.

## Steps

1. Read the run list and the job steps for 9e865a4 from the Actions API, captured through tools/x. 2. Record in STATE.md: the run id, all six steps green, the two failures and their cause, and which standing claims this closes or leaves open. 3. State the ceiling: one commit, one runner image, one day.

## Acceptance criteria

- [x] STATE.md names the run id, the commit, and all six step conclusions as observed, not inferred.
- [x] The two 23:58 failures are recorded with the cause rather than left unexplained.
- [x] The standing CI row says what is now observed and what is still not (no second runner, no re-run of the 2.56.0 git path).
- [x] doc lint exits 0.

## Verification

```bash
grep -q '37165413909' STATE.md && tools/origin doc lint
```

## Rollback

Revert the STATE.md commit; nothing else changes and no record is rewritten.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The assumption this task existed to check was wrong.** T-0024's D029 predicted
that a push after local midnight would fail Documentation lint. Two runs ten
minutes earlier *had* failed — and their failing step was Documentation lint, so
the prediction looked confirmed. Reading the step conclusions and then
`git show 8898f0a:tasks/INDEX.md` falsified it: that commit carries the new task
file and an index that does not list it, so the **orphan** rule fired. The clock
was still 23:58 UTC. The date defect was real (reproduced locally on 2026-10-04)
and is fixed; its CI consequence stays `inferred`, and defect 5 in
[`STATE-defects.md`](../STATE-defects.md) records the cause that actually reddened
two runs.

**Split while here.** `STATE.md` reached 293 lines, so the defect list moved to
[`STATE-defects.md`](../STATE-defects.md) with the solve/open status each entry
carries, and `RELEASE-MANIFEST.md` classifies the new file. That is the split the
doc standards ask for at 250 lines, done where the pressure actually was.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
