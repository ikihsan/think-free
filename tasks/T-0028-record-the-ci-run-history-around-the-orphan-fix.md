<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0028
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: grep -q '37166490623' STATE.md && tools/origin doc lint
-->

# T-0028 — Record the CI run history around the orphan fix: six red runs with the

## Goal

Record the CI run history around the orphan fix: six red runs with their single verified cause, and the green runs after it

## Why this matters

Since T-0025 recorded one green run, this VM has pushed five more commits and CI has run eleven times: six red and five green. Every red run has the same verified cause - the orphan rule on a commit that carried a task file without the rebuilt indexes - and the last four runs are green. Without this, the next agent reads six red runs in the history and either rediagnoses a solved defect or assumes the gates are flaky.

## Preconditions

None: the runs are readable through the public Actions API and each has already been attributed to a step.

## Steps

1. List the runs for 9e865a4..fc9d9ed with their step conclusions, captured through tools/x. 2. Record in STATE.md's CI row: the green runs by id, the six red runs by id, and the one cause, with the commit at which the claim path started carrying the indexes. 3. State what is still not observed: nothing has exercised a rebase conflict, and the 2.56.0 git path has not run on CI at all.

## Acceptance criteria

- [x] Every CI run since the T-0024 land is listed with its conclusion and its step.
- [x] The six red runs share one named cause and the commit that ended it is named.
- [x] What CI has still not exercised is stated, not implied.
- [x] doc lint exits 0.

## Verification

```bash
grep -q '37166490623' STATE.md && tools/origin doc lint
```

## Rollback

Revert the STATE.md commit.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**Seven red runs, not six.** The task said six; the list is
`37163434868`, `37163438950`, `37165502352`, `37165507351`, `37165802926`,
`37165807196` and `37166490623`. The seventh is this VM's own T-0027 claim commit,
which was made *before* T-0027's fix landed - the same defect, one task earlier
than the record claimed. Every one of the seven failed the same step with the
same exit code, and each was checked against the tree at its commit rather than
inferred from the previous one.

**What the history does not show.** All green runs are one runner image and one
Python (3.12, pinned). The git 2.56.0 path that F011 broke has never run on CI,
and no run has contained a rebase conflict between two VMs, so the conflict and
land-conflict rules remain unexercised by the runner.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
