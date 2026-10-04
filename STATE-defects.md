<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Known defects

Every defect this repository's own tooling and records have shown, whether or not
it is fixed. Split out of [`STATE.md`](STATE.md) on 2026-10-04 when that file
reached 293 of the 300 permitted lines, so the reload point stays a reload point.

The rule for this list: a defect is *solved* only when a gate fails on its own
bytes and passes on the repair. A repair that has not been falsified against the
defect is listed as open.

## Solved

1. **An in-flight session reddened every other VM's CI** (solved in T-0020). Two
   correct rules met — `task claim` needs HEAD on the remote base, so a claiming
   VM must publish its `session_start` first, and D013 then failed every push.
   `tools/originlib/inflight.py` separates in flight from abandoned from the tree
   alone (D027; findings F014 and F015). The live record corrected that predicate
   once already: clause 1 required the session to name a task, the other VM
   started one without `--task`, so the gate called a working session abandoned. A
   claim in the ledger naming the session now counts.
2. **Reconciliation compared trees, not authorship** (solved in T-0024, D028). A VM
   that landed another VM's work inherited its `unlogged_change` and
   `documentation_gaps` reports — session 029 emitted nine of the first, none of
   them its own. `sync pull`/`sync land` now record a `base_advance` naming the
   commits that arrived, and reconciliation attributes a path by the newest thing
   that touched it. **Ceiling:** attribution knows only about base moves the
   tooling performed, so a rebase run by hand still reports; that is the intended
   direction of failure.
3. **Every generated file stamped `last-verified` with the render date** (solved
   in T-0024, D029), so `doc lint` failed on 42 committed session reports and all
   three indexes on 2026-10-04 — the day after they were written. Each generator
   now stamps from the content it renders. The CI consequence is `inferred` from
   that local reproduction: no pushed run has failed this way, because the two
   red runs at 23:58 on 2026-10-03 had a different and verified cause (defect 5).
4. **A pushed task file without `doc index` reddens CI** (solved in T-0026 and
   T-0027). Runs `37163434868` and `37163438950` failed on Documentation lint:
   this VM created a task, committed it and pushed it without rebuilding the
   generated indexes, so the orphan rule rejected the file the VM had just
   created. `task new`, `claim`, `complete` and `release` now rebuild
   `tasks/INDEX.md` and `docs/INDEX.md`; a *published claim* also stages them,
   because that commit is the first thing every other VM reads (four more red
   runs, `37165502352`–`37165807196`, were the same defect one step later).
   **The rule is unchanged** — a file no command wrote is still an orphan, which
   the new tests assert — because the omission was the defect, not the strictness.
   **Residual:** the create commit is the agent's own, so `task new` prints the
   command that stages the indexes; nothing can enforce that step.

## Open

5. **Identifier allocation collides by construction** (open). Identifiers are
   allocated by reading the local tree, so two VMs in an hour take the same
   numbers. Six times on 2026-10-03: T-0016 and F009/F010/D022; session 029's
   F012 against session 026's F010; session 030's F012 for E3's attribution
   against VM 0947's F012 for the worktree defect; D024 issued twice for unrelated
   decisions; then F013, `FAILURES-findings-3.md`, D025 and D026 all taken on
   0944 while 0947 held the same numbers. VM 0947's two findings became F014 and
   F015 and its session-gate decision D027. **The cost is measured:** a rebase
   resolution restored one file's index row to the renumbered form while reverting
   its body, so a findings file and its own table disagreed about the same entries
   until both were read together. **Ceiling of any fix:** a detector can refuse a
   commit that reuses an identifier; it cannot stop two VMs allocating at once.
6. **`doctor` does not compare this VM's git against what the suite has been
   exercised on** (open, partly closed in T-0018 with `tests/git-versions.json`).
   There is still no equivalent record for Python, which
   `docs/operations/vm-execution.md` names as unclaimed work.
   **Ceiling:** bookkeeping hygiene, not a claim about a candidate.

## What a fix costs to believe

Every entry above marked solved was falsified against its own defect first: the
new tests were run against the unfixed code and had to fail. One of those
falsifications (T-0024's second attempt) mutated a code path the callers never
reach and passed anyway — the failure of the falsification, not of the gate — so
it was redone by reverting the generators instead. See D025 in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md).