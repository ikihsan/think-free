<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0048
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-030-make-sync-land-s-own-conflict-instructio
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_land -q && tools/origin preflight
-->

# T-0048 — Teach sync land to finish a paused rebase whose conflicts are already 

## Goal

Teach sync land to finish a paused rebase whose conflicts are already resolved, so its own instruction is executable

## Why this matters

sync land stopped on a real content conflict in tasks/CLAIMS.jsonl and said 'resolve it and land again'. The second land refuses on the dirty tree the resolution leaves, so the instruction cannot be followed: the only way out is a hand-run git rebase --continue, which records no base_advance, so every path that arrived from the base is attributed to the session that resolved the conflict. That is defect 2's stated ceiling, reached through the tool's own refusal message rather than by a mistake. Land already knows how to continue a rebase non-interactively for the generated files it auto-resolves; this is the same call for the case a human had to resolve.

## Preconditions

Two VMs publishing into tasks/CLAIMS.jsonl in the same hour, which is the normal case and has stopped a rebase more than once

## Steps

1. Read how land auto-resolves a generated conflict and reuses GIT_EDITOR=true; the resume path is the same call reached from a different state.
2. Detect a rebase already in progress with no unresolved path, continue it with the same non-interactive environment, and report what it completed.
3. Record the base_advance for the commits that arrived, so their paths are not attributed to this session - the half of defect 2 that a tooling-performed continuation can still close.
4. Falsify first: with the resume call removed, a two-clone fixture that resolves a CLAIMS.jsonl conflict cannot land at all.
5. Say what is still refused: an unresolved conflict, and a rebase land did not start.
6. Update docs/process/multi-vm-coordination.md, which documents the resolution but not the completion, and tests/README.md.

## Acceptance criteria

- [x] land completes a paused rebase with every conflict already resolved, and refuses one
      that still has an unresolved path. The refusal is the conflict one, in the same words —
      `test_a_conflict_still_unresolved_is_still_refused_with_the_same_words`, which is the
      case a reader hits by running `land` twice.
- [x] The completion is non-interactive, using the environment the generated-file path already
      used — now one constant, `landrebase.NON_INTERACTIVE` — and a sentinel editor proves it.
- [x] The arriving commits are recorded as a base advance, so the paths they brought are not
      attributed to the session that resolved the conflict. Read from git's own `orig-head`.
- [x] Falsified against the unmodified code, in a two-clone fixture that resolves a real
      `tasks/CLAIMS.jsonl` conflict. **With the resume removed: three errors and one failure** —
      nothing lands at all, and the unresolved case degrades to the dirty-tree message.
      **With `orig-head` read replaced by `HEAD`: one failure**, `no arrival recorded for a
      resumed rebase`.
- [x] What is still refused is documented: an unresolved conflict, a dirty-and-unstaged path,
      and a continuation that fails.
- [x] `docs/process/multi-vm-coordination.md` documents the whole procedure, and the CLI
      reference says what `resumed` is.
- [x] The suite and all four preflight gates are green.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_land -q && tools/origin preflight
```

## Rollback

Revert the resume branch in tools/originlib/syncland.py; the generated-file path it shares is unchanged and a real conflict still stops.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

## Notes

**The defect was in the refusal message, not in the code.** `land` stopped on a real
content conflict and said *resolve it (or `git rebase --abort`) and land again*. The
second `land` refuses on a dirty tree — and resolving the conflict is what makes the
tree dirty. So the instruction could not be followed by the tool that gave it. The only
way out was `git rebase --continue` by hand, which records no `base_advance`, so the
paths the base brought were attributed to this session: defect 2's ceiling, reached
through a refusal message rather than by a mistake. D039.

**Two facts about git's state had to be read, and both have a wrong answer that looks
like a working one.**

- *Is a rebase in progress?* Both backends. This VM's git 2.25 writes `regit
  rebase-apply` where 2.26 writes `rebase-merge`, so reading one directory is a check
  that passes on half the fleet and looks deliberate. Found by the first implementation
  of `_orig_head` returning `""` on this VM and the tests failing for no visible reason.
- *What was this branch's tip before the rebase began?* Not `HEAD`: mid-rebase, `HEAD`
  is the base with this branch's earlier commits already on it, so `before..base`
  computed from it names nothing and every arriving path looks like this session's own
  change. Git recorded the real tip in `orig-head` **when the rebase started**, and
  deletes it when the rebase finishes — so it is read before the continuation, not
  after. My first version read it after, and the arrival assertion caught it.

**`git rev-parse --git-path` prints a path relative to the repository, not to the
process.** Resolving it against the cwd reads a different VM's rebase state in a fleet
test — `gitutil.rebase_in_progress` already resolved it against the clone, and the new
code now does the same through `landrebase._repo_path`. It cost one debugging pass and
is the kind of thing that is green on the machine that wrote it and wrong on the fleet.

**The unstaged-path refusal is a real hazard, not a tidiness rule.** `git rebase
--continue` commits the whole index, so anything staged alongside the rebase's own
resolution is swept into the rebase's commit rather than the one that names it — the
`git add -A` mistake from the session protocol, arriving by a different route. A path
dirty and *not* staged is therefore refused. It also made the sentinel-editor test fail
for the right reason: the sentinel script was in the working tree, which is exactly the
condition the refusal exists for. It now lives outside the clone.

**Line caps again, and a relocation rather than a rewrite.** `syncland.py` reached 310
of 300, so the rebase-state readers went into `tools/originlib/landrebase.py` — the
same division `doclint_tree.py` used, reading git's state separated from acting on it.
`DECISIONS-GATING.md` reached 308 with D039, and the note recording T-0030's split that
was attempted and reversed moved to [`DECISIONS.md`](../DECISIONS.md), where the other
four splits are already recorded. It is at 296, so the next gating decision has room
and the one after it does not.

**Unrun and stated as such:** this path has been exercised against a real rebase on this
VM's git 2.25.1, whose backend is `rebase-apply`. The `rebase-merge` branch of
`orig_head` is not exercised here, and the CI runner's 2.55.0 will be the first
execution of it on that backend.
