<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- task-meta
id: T-0082
status: claimed
created: 2026-10-07
claim-agent: opencode
claim-session: 2026-10-06-016-dogfood-stg-on-real-changes-in-this-repo
claim-vm: instance-20260717-0947
verify: python3 EXPERIMENTS/043-real-changes/run.py
-->

# T-0082 — E043: measure stg on real repository changes (renames, mode changes, m

## Goal

E043: measure stg on real repository changes (renames, mode changes, multi-hunk real diffs) using git's own diff as the referee, and decide whether the artifact is release-ready

## Why this matters

Every stg experiment E037-E042 declares the same untested ceiling: renames, mode changes, binary files, untracked files, conflicted merges, multi-file cases, on real rather than synthetic diffs. The candidate's surviving differentiator is packaging ('a tested tool you can trust on your real changes'), and that claim is unmeasured. E038's stronger oracle found two real bugs the synthetic corpus missed, so the same move is expected to pay again.

## Preconditions

git 2.25.1 and Python 3.8.10 on instance-20260717-0947; patchutils 0.3.4 present; session 2026-10-06-016 is open on this working tree and carries this work.

## Steps

1. Harvest real (pre-image, post-image) file pairs from real commits in this repository and at least one independent public repository; record repo, commit sha, path, blob shas, mode and rename flags in a manifest. 2. Declare the question, the referee (git diff on blobs, not stg's parser), the positive control (E038's 30 rows through the same oracle) and the kill condition in PROTOCOL.md before running. 3. Run stg over every harvested change: enumerate addresses, stage each address alone in a fresh repo, compare the staged blob against the working-tree version with git's own line diff. 4. Completeness: staging every address of a file must reproduce the post-image byte-for-byte. 5. Honesty: an address that stages nothing must exit non-zero. 6. Record results, findings and the build decision.

## Acceptance criteria

A results table over real changes with, per row, the address, the declared change size, the size git's own diff reports, and the verdict; plus a positive-control row showing the oracle returns the known-correct answer on E038's matrix; plus either zero soundness failures (release-ready, with the untested ceiling narrowed to what remains) or a named list of reproducible failures.

## Verification

```bash
python3 EXPERIMENTS/043-real-changes/run.py
```

## Rollback

All output is under EXPERIMENTS/043-real-changes/; the harvest is read-only over git history and the run works in temporary directories. No change to stg until a failure is reproduced and named.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
