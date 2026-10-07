<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- task-meta
id: T-0084
status: open
created: 2026-10-07
claim-agent:
claim-session:
claim-vm:
verify: python3 EXPERIMENTS/047-hook-partial-stage/harness.py; test $? -eq 0
-->

# T-0084 — Test with a byte-level oracle whether any shipped git hook runner fold

## Goal

Test with a byte-level oracle whether any shipped git hook runner folds a partially-staged file's unstaged hunk into the commit, and decide whether the hook hazard STATE.md names as the next action is a candidate

## Why this matters

STATE.md's ranked next action after E045: two rows of the 189-row demand corpus describe a formatter/lint hook that re-stages a whole file and sweeps a partially-staged file's unstaged hunks into the commit. nextjs-app-template#95 says the warning in its own lefthook.yml is false; agent-orchestra#154 is the same class of bug in a hand-written .githooks/pre-commit. STATE.md records this as 'a correctness failure with a byte-level oracle' and says two rows is not evidence for a candidate. Reading both rows verbatim first inverts half the record: #95 is a report that lefthook 2.x does NOT sweep (it hides the unstaged half the way lint-staged does, and the repository's own warning is the stale part), and #154's own review record shows a reviewer raising exactly the sweep hazard and the defense being SUSTAINED as out of scope. So the question must be settled against the real tools rather than against two issue bodies.

## Preconditions

network access for the fetches; gcc, make and perl for the git build; ~34G free

## Steps

1. Fetch lefthook, pre-commit, lint-staged, husky and prettier at current versions; record each version and the sha256 of the bytes used. Build a current git from source, because this VM's 2.25.1 is below lefthook's 2.31 and lint-staged's 2.32 minimums.
2. Build the fixture: one file, region A staged and badly spaced, region B an unstaged marker line six unchanged lines away so the two are separate hunks at git's default context. Staging is arranged without any interactive command.
3. Oracle: bytes of git show :app.js and git cat-file blob HEAD:app.js. No grading, no model. An arm where the formatter did not run is INCONCLUSIVE, not clean.
4. Positive control C0: the naive hand-written hook must SWEEP or the run is void (F010). Fixture control B0: with no hook the marker must stay out and the formatter must not run.
5. Arms: C0, B0, lefthook with stage_fixed, lefthook without it, pre-commit, lint-staged default, lint-staged --no-stash, husky, and git stash push --keep-index as the no-framework remedy.
6. Each arm is committed through its own installed hook, because the hiding is the mechanism and invoking a runner by hand would skip it.

## Acceptance criteria

Every arm that could run produced a verdict on bytes; both controls behaved as required; lefthook and lint-staged were measured on a git new enough for them to start. A reader can tell from raw/results.json whether a shipped runner sweeps, and the experiment names the population its result covers.

## Verification

```bash
python3 EXPERIMENTS/047-hook-partial-stage/harness.py; test $? -eq 0
```

## Rollback

everything lands under /tmp/opencode/e047 and is deleted with rm -rf; nothing is installed system-wide

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
