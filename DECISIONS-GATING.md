# Decisions — how this repository's own gates are written and run

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

Decisions **D013, D024–D029**. Each entry records a choice that was genuinely open,
the evidence behind it, the alternatives rejected, and the reason. Decisions that
constrain later work belong here; ordinary edits do not.

**Invariant:** every entry here governs *how this repository verifies itself* —
verification strictness, and the shape a gate or its control must have before it
is trusted. What *passes* — candidate screens, kill-gate conditions, verdict
metrics — belongs in [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md); how work
is recorded, moved, or published in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md).
The index is [`DECISIONS.md`](DECISIONS.md).

Split from `DECISIONS-PRACTICE.md` on 2026-10-03 (T-0018) when that file reached
297 of the 300 permitted lines. Entries moved verbatim; numbering is continuous
and unchanged, so any existing reference to a decision id still resolves.

Split attempted and reversed on 2026-10-04 (T-0030). D013, D027 and D028
were moved out to `DECISIONS-PRACTICE.md` because D030 had reached 289 of the 300
permitted lines — and `instance-20260717-0944`, working in the same hour, appended
D031 to that file. Both moves overflowed their destination: this one reached 323
lines, and the other put a fifth session-state decision where no other session-state
decision had ever been. The entries are therefore back where they were, and the
reason is recorded rather than the attempt: **a split is a claim about an
invariant, and the two VMs were claiming incompatible ones in the same hour.** A
file at 289 lines with a real invariant is a smaller problem than two files whose
prose contradicts each other.

D030 was missing from the index row above until this session, and the rule added in
T-0030 is what found it: a decision can be written without being listed, and no gate
compared the two. This session's own decision was renumbered D031 to D032 for the
same class of reason — the collision is resolved on the side that has not been
pushed, which is the rule both VMs settled on earlier today.

## D024 — A gate clause must be implemented as written, and a control must be able to fail (2026-10-03)

Observed: T-0017's predeclared G2 reads "a planted content change is detected
**and attributed to a non-timestamp cause**". The code implemented "the artifacts
differ". The planted file was `src/__planted__.txt`, which none of the five
`setup.py` files packages, so the planted artifact differed from its control only
by the wall-clock stamps on its `.dist-info` files — and *that* difference is
exactly what the experiment was measuring elsewhere. The control passed, the gate
was reported met, and nothing had been tested. The proxy clause was satisfied on
four sources while `residual_causes_after_patch` was empty on all of them.

Decision: two rules for every gate written from here on. **A control clause is
implemented by its own noun, not by a weaker proxy** — "attributed to a
non-timestamp cause" is checked by looking for that cause, never by looking for
any difference. **A control's expected failure is asserted, not assumed**: if the
planted defect cannot be observed, the run reports the control as unfired rather
than as passed. Planting is done by reading a real build's artifact and editing a
file the artifact demonstrably contains, because a control aimed at a path no build
writes is a control that measures the harness.

Rejected: reading the first run's verdict, because it was produced by a clause the
code did not implement; and re-running until the control fires, which would have
been indistinguishable from picking the result.

Consequence: the first run is kept as
`EXPERIMENTS/008-build-timestamp-attribution/first-failure.json`, the second run
is the one `results.json` holds, and both the experiment README and
`FAILURES.md` F012 name the defect. The strengthened check now reports
`content-differs` on 5 of 5 sources with 40,493–97,407 non-timestamp bytes, which
is what makes the headline "no residual cause" a result rather than a blind spot.

## D025 — A gate must read the property it claims to check (2026-10-03)

Observed: commit `fd7b4a1` committed three mission records to the shared base
with `<<<<<<< HEAD` still in them, and every gate passed (`FAILURES.md` F013).
`doc lint` read 300-odd files for line counts, metadata, links, orphans, and
generated drift; `session verify` read event streams; `skills verify` read
vendored hashes. Every gate read the file. None read the conflict markers.

Decision: **a gate that reports a property it never inspected is not a gate for
that property.** Two obligations follow. First, every declared gate is backed by
a check that names the property it checks, so the gap is visible in the code
rather than in a failure six sessions later. Second, a gate added for a defect
is falsified against the defect's own bytes before it is trusted: T-0021 scanned
`git show fd7b4a1:<file>` for all three files and required one finding per
committed defect, which is how the first implementation of the rule was caught
reporting only malformed blocks (1 finding of 4).

Rejected: scanning every tracked file's prose for *any* `<`/`>`/`=` run, because
a gate that flags ordinary documentation is a gate that gets waived wholesale.
Adding the check to `session verify`, whose subject is the event stream and not
file content. Fixing only the three records, which leaves the mechanism that
produced them intact — the same shape as F010's near-vacuous metric.

Consequence: `doc lint` rule 6 (`tools/originlib/conflicts.py`) is the
mechanism, and the honest claim about it is narrow — it detects git's marker
shape at column 0, which is what git writes and what was committed here. A
hand-typed marker, or one indented inside a code fence, is not detected; the
limitation is in the module docstring rather than discovered later.

## D026 — A task's verification must be runnable while its own session is open (2026-10-03)

Observed: T-0021 was declared with `verify: … && tools/origin session verify
--strict && …`. That command cannot pass, ever, in the session that must run it:
a task's verification runs on the claiming VM inside that VM's open session, and
`--strict` fails for every session still in flight — which at that moment is the
one claiming the task. `session verify` (no flag) reports the same session as in
progress and exits 0. T-0020, claimed on the other VM the same hour, declares the
same unpassable command.

Decision: **a task's `verify` command must be satisfiable at the moment it is
run.** A gate that fails because of the act of verifying is a gate that pushes
the claimant toward editing the command to make it pass, which
`docs/process/task-lifecycle.md` forbids and which would destroy the property
the gate exists for. Local verification therefore uses the tolerant flag; CI
keeps `--strict`, which is exactly the split D013 already draws, and a task that
wants the strict reading states it as a CI concern rather than a verify field.

Rejected: running `task verify` after `session finish` to dodge the problem,
which loses the check inside the session that did the work — the thing
task-lifecycle says must never happen. Running it with `--strict` and completing
the task anyway, which is a recorded false pass. Weakening the *other* gates to
match.

## D029 — A generated file is a function of the tree, never of the clock (2026-10-04)

Observed: `doc lint` failed on 42 committed session reports and all three
indexes on 2026-10-04, the day after they were generated. Nothing in them had
changed except the calendar: each stamped `last-verified` with `now`, and rule 5
compares a committed generated file with what the generator produces *now*. CI
would have failed on the same comparison for any push after local midnight, on
any VM, for content nobody had touched. Found while running T-0024's own
verification, which could not pass.

Decision: every generator stamps `last-verified` from the content it renders — a
session report from its newest event, the sessions index from the newest
session's, the tasks index from the newest claim in the ledger, the docs index
from the newest `last-verified` among the documents it lists. An index with
nothing to index says `unknown`, because a stamp nobody can support claims a
verification that never happened.

Rejected: making rule 5 ignore the stamp, which would hide a real staleness in
every other field; and pinning CI's date, which a hosted runner does not let a
repository control.

**Ceiling.** A generated file is now stable until its *content* changes, which
is the property rule 5 was written to check. The date no longer tells a reader
when the file was last regenerated — only when its newest input was verified,
which is the claim the field can actually support.

**Falsified against its own defect.** `tests/test_generated_stamps.py` moves
`events.now_iso` to 2031 in place. Against the pre-change code: 2 failures and 1
error, with `doc lint` reporting the four stale files. A first attempt at this
falsification failed to falsify anything — it mutated the fallback inside
`_meta`, which the two callers never reach — and was redone by reverting the
three generators. Both runs are in this session's `commands.log`.

## D030 — A diagnostic must distinguish "never configured" from "stopped working" (2026-10-04)

Observed: T-0025's first verdict logic tested the functional probe before it
tested whether any mechanism existed, so a fresh VM with no credential was
reported `broken` — the same verdict as the machine that lost every push to a
`/tmp` clear. That is the incident `STATE.md` records for
`instance-20260717-0947`, and the repair for it would have been to go looking for
a helper that was never configured. The harness caught it: three environments
that must be distinguishable produced two distinct reports instead of three.

Decision: **a diagnostic reports absence and breakage as different states, and
says which one it means.** `doctor` uses `configured`, `broken`, and
`unavailable`, ordered so the question "is anything configured at all?" is
answered before "does it work?". This extends D025 to diagnostics rather than
gates: D025 requires the check to read the property it claims, and a check that
cannot tell two states apart has not read either.

Rejected: a single `ok: false`, which is what the original line was; a warning
list without a verdict, which leaves the reader to re-derive the state; calling
absence `broken`, which is the defect. Also rejected: `git ls-remote <remote>`
as the functional probe, because this remote is public and `ls-remote` exits 0
with no credential at all — a check that cannot fail, F010 with extra steps —
and a report built from listing the helper's files, because
`instance-20260717-0947`'s helper survived and the script it invoked did not.

Consequence: `docs/operations/doctor.md` states the whole contract, including
that `configured` does **not** mean the credential can push. The verdict is
deliberately coarser than "works", and the ceiling is written down rather than
left to be discovered by someone who reads `configured` as permission.

## D032 — An identifier collision is refused before publication, and only the merge can see it (2026-10-04)

Observed: identifiers are allocated by reading the local tree, so two VMs in one
hour take the same number — seven times on 2026-10-03 and 2026-10-04, resolved by
hand every time. Commit `e6eb992` is the one that reached the shared base: two
different findings both headed `## F010` in `FAILURES-findings-2.md`, and two
`| F010 |` rows in `FAILURES.md`, one minute apart by commit time. No gate said
so. `doc lint` read 378 files for line counts, metadata, links, orphans, generated
drift and conflict markers; none of those is the question "does this number mean
one thing". The measured cost is in defect 5: a rebase once restored one file's
index row to the renumbered form while reverting its body, so a document and its
own table disagreed about the same two entries.

Decision: **the property is checked where it first exists, which is the merge.**
`doc lint` rule 7 (`tools/originlib/identifiers.py`) reports any identifier
defined twice, a findings index row with no definition, a defined finding with no
row, and a decision its own index row does not list. `sync land` refuses to push
a tree the rule would refuse, because a collision is created by the merge: each
branch is internally consistent and each VM's own lint sees nothing wrong.

Rejected: gating `sync push` and `task claim` as well. Refusing them blocks a VM
from publishing the very session record it needs in order to renumber its way out
of the collision — the gate would hold the defect in place. Rejected: comparing
an index row to its heading by string equality, which is what the first draft did
and which flags 83 of 174 commits including this one, because two rows in
`FAILURES.md` are shortened paraphrases on purpose. Rejected: allocating the next
number from the remote claim ledger, which is the fix at the source (VM
`instance-20260717-0944` named it on 2026-10-04) but catches neither a hand
renumbering nor a bad rebase, so it does not replace this.

**Ceiling, and it is the same ceiling defect 5 records.** This is a detector, not
an allocator: it can refuse a commit that reuses an identifier, and it cannot stop
two VMs allocating at once. It reads the tree, so a collision created and resolved
entirely between two pushes is never seen. Hypothesis identifiers are out of
scope, and an index row is matched on identity alone, so a body quoting another
entry's subject is not detected. This is bookkeeping hygiene with a measured cost;
it says nothing about any candidate.

**Falsified against its own defect, in two directions.** Run over all 174 commits
on the shared base the rule reports **one** — `e6eb992` — and the hand repair one
minute later (`8a4ab8cef`) is clean. The second direction mattered more: the
first version of the decision-index check matched nothing in any commit, because
the regex did not allow a Markdown link, so a check that had never fired looked
identical to a check that had nothing to report. The control test is the two
paraphrased rows in this repository, and it was the control that found it.
