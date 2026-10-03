<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures — recorded findings, part 3 (F013 onwards)

Continues [`FAILURES-findings-2.md`](FAILURES-findings-2.md), which holds
F009–F012 and reached the 300-line cap at F013. **Identifiers are stable across
all three files**: a reference to `F012` means the same entry wherever it
appears. New findings are appended here.

**The invariant is unchanged by the split.** Findings are separated from
`FAILURES.md`'s live list because a reader must be able to tell a disproved
claim from a still-open question. The files split by line cap, not by subject:
part 1 holds F001–F008, part 2 F009–F012, part 3 the rest. F014 and F015 were
written on a second VM while this file was being written on the first, and were
renumbered into place when both branches landed; `STATE.md` records the collision
and what it cost.

## F013 — Three mission records were committed with conflict markers, and every gate passed

Source: T-0021, commit `fd7b4a1`, repaired in `FAILURES.md`, `FAILURES-findings-2.md`,
and `DECISIONS-GATING.md`. Rule: `tools/originlib/conflicts.py`, doc lint rule 6.

**What happened.** The third identifier collision of 2026-10-03 was renumbered by
hand while a rebase was in progress, and the commit went out with `<<<<<<< HEAD`
still in three mission records. `FAILURES.md` and `FAILURES-findings-2.md` each
held a complete block; `DECISIONS-GATING.md` held one block plus a terminator
left behind with nothing open. F011 and F012 were ambiguous exactly where the
markers sat: the renumber had deleted an F011 that had meanwhile become a
different VM's finding, so the "empty" side of the conflict was wrong and the
records were unreadable in the region that decides what is disproved.

**Why every gate passed.** `doc lint` checked line counts, metadata, links,
orphans, and generated-file drift — never whether the *text* was a resolved file.
`session verify` checks the event stream. `skills verify` checks vendored
hashes. Reconciliation compares trees, not content. A marker is a content defect
in files that every existing rule reads for a different reason.

**Fix and its falsification.** The repair keeps both sides of all three regions,
because both sides carried distinct claims (F011 and F012 are different
findings). The gate is `doc lint` rule 6: exactly seven `<`, `|` or `>` at
column 0 opens or closes a block, a seven-character `=` divider belongs to a
block only when one is open, and a block is reported once at its opening line. A
file may declare `origin-allow-conflict-markers`, reported as `info` so a waiver
is never silent.

**The rule was wrong before it was right.** The first implementation reported
only *malformed* blocks. Run against the three historical files it found one
defect out of four, because a well-formed `<<<<<<< / ======= / >>>>>>>` triple
is exactly what a committed unresolved conflict looks like. The kill gate — scan
the pre-fix bytes, require a finding per defect — is what caught it. Same clause
shape as D024: the gate clause was implemented as a weaker proxy.

**Classification.** Record-keeping defect, found by reading the base branch
rather than by a gate. Fourth collision of the evening, and the first one whose
damage outlived the session that caused it.

**Lesson kept.** A gate that checks structure cannot catch a structural mistake
in content, and a repair performed by hand during a rebase is the highest-risk
edit in the repository. What made this survivable was that the markers were
still text: nothing had been lost, only made ambiguous.

## F014 — The documented VM sequence was impossible, and refusals printed tracebacks

**What failed.** `docs/operations/vm-execution.md` §3 tells a VM to
`task claim` and then `worktree add`. Observed 2026-10-03: the second command
refused, because `worktree.add` rejected *any* claim, including the one the same
VM had just published. The isolation step of the whole fleet flow could not be
reached by following the document that specifies it.

**Second defect, same command.** `worktree.WorktreeError` and `sync.SyncError`
were not in `cli.main`'s handlers, so the refusal escaped as a Python traceback.
The exit status was `1` by accident of an uncaught exception rather than by the
documented contract, and a caller could not distinguish a refusal from a crash.

**Consequence.** Two agents following the documentation on one VM: one keeps
working in the shared tree (the isolation the docs call "the thing that removes
the collision at the filesystem level" never happens), the other is deterred.
Nothing detected either state; the refusal is an exit code and a stack trace,
which is exactly the output nobody pastes into a bug report.

**Fix.** `worktree.add` refuses only a claim held by a *different* VM. The VM is
the right unit of isolation: two agents on one machine already share a working
tree, a git index, and one `sessions/active.json`, which is the collision
`worktree` exists to remove. A claim with no recorded VM is still refused, since
an unattributable claim cannot be shown to be ours. `cli.main` now maps both
errors to exit `1` with one stderr line. Tests in `tests/test_fleet.py`: a claim
from another VM is still refused, a claim from this VM is accepted, and the CLI
returns `1` with no traceback.

**Classification.** Documentation and implementation disagreed, and the
implementation's error path was unhandled. Both found by following the
documented sequence rather than by reading it.

**Lesson kept.** A procedure nobody has executed end to end is a description,
not a contract. `worktree add` had been exercised in the fleet tests only
*before* a claim existed, so the two features had never met.

## F015 — The local and remote views of a task's holder disagreed after every takeover

**What failed.** `tasks.active_claims()` opened a claim only for the ledger
action `claim`, while `taskremote.remote_active()` opened it for `claim` **or**
`takeover`. A takeover is how this fleet legally takes a dead VM's work, and
after one the local view reported no holder while the remote view reported the
new holder.

**Consequence.** Two views of the same file disagreeing is worse than one wrong
view: `tasks/INDEX.md` and `task list` printed a holder that a fetched
`task list --remote` contradicted, so a reader could not tell which was true. It
also matters mechanically — the in-flight classification added by T-0020 reads the
ledger to decide whether an unfinished session is still being worked on, and an
ignored takeover would have made a legitimately re-claimed task look abandoned.

**Fix.** `active_claims()` honours `takeover`, matching the remote view, and the
behaviour is pinned by a test that appends `release` then `takeover` and asserts
the claim is still in force locally.

**Classification.** Implementation defect, duplicated logic in two places with
no shared definition. The two functions had drifted because nothing compared
them.

**Lesson kept.** When two modules answer the same question from the same file,
one of them must call the other.
