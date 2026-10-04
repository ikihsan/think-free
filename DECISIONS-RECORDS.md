# Decisions — what this repository's own records must be

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

Decisions **D029, D032, D035**. Each entry records a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason.
Decisions that constrain later work belong here; ordinary edits do not.

**Invariant:** every entry here governs *a particular record or artefact this
repository keeps* — what it must be a function of, what may not collide, and
which two artefacts must agree with each other. How a gate, a diagnostic or a
control must be **written** belongs in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md); how work is recorded, moved and
published in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md); what *passes* in
[`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md); what the mission is in
[`DECISIONS-FOUNDATION.md`](DECISIONS-FOUNDATION.md); the state of a session's
own record in [`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split from `DECISIONS-GATING.md` on 2026-10-04 (T-0042) when that file reached
297 of the 300 permitted lines and its own header recorded that the next gating
decision had nowhere to go. Entries moved verbatim; numbering is continuous and
unchanged, so any existing reference to a decision id still resolves.

**Why this split and not the one T-0030 reversed.** The reversed attempt moved
session-state decisions out of this file while another VM appended to its
destination in the same hour, and both moves overflowed: a file at 289 lines
with a real invariant is a smaller problem than two files whose prose
contradicts each other. The line that separates these two files is the one D032
and D035 both already used in their own text — *the check must read the
property*, which says nothing about **which** property, against *a named record
of this repository*. D024, D025, D026 and D030 are about the reader; D029, D032
and D035 are each about one artefact this repository keeps. The earlier attempt
drew its line between two claims about session state, which is why the two VMs
claimed incompatible invariants.

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
## D035 — CI runs every minor version the floor claim covers, and the matrix and the record are held to each other (2026-10-04)

Observed: `tests/python-versions.json` named 3.9 to 3.11 as versions nobody had
run, and its own `why` clause gave the reason in five words — *"CI pins a single
version"*. The 3.8-or-newer floor was therefore a claim resting on two points
with a gap between them, and the gap was named rather than measured. Running the
suite on the missing interpreters (T-0034) then failed on **all five** of them,
on an assertion with nothing to do with the code (F018).

Decision: **CI runs one matrix row per CPython minor from 3.8 to 3.14**, and the
two artefacts that must agree — the workflow's row list and the record — are held
to each other by a gate that reads both (`tests/test_ci_matrix.py`). The five
gates that read files rather than run the interpreter stay on one row, 3.12,
guarded explicitly. `fail-fast: false`, because a cancelled row is not a version
anything has run on.

Rejected: a second job for the file-reading gates. Same work, two job names
instead of five `if:` lines, and it renames the checks every "CI is green" claim
refers to. Rejected: leaving those gates unguarded so they run on every row,
which multiplies the slowest steps by seven for a check whose result cannot depend
on the interpreter. Rejected: a matrix of two or three sampled minors — cheaper,
and it would leave the record describing versions it never ran, which is the
exact defect T-0032 was written to stop. Rejected: recording the local
measurements *instead of* the CI rows, because `doctor` would then warn a VM
whose interpreter demonstrably ran here.

The gate's parsers are deliberately dumb and deliberately loud: an unrecognised
matrix, a step at the wrong indent, and a `not_exercised` range that names a
version it cannot resolve are **failures**, not passes. That is the shape of
T-0030's control failure, where the regex matched no row in any of 174 commits
and the sweep was green while half the rule did nothing.

**Ceiling, stated rather than discovered later.** The matrix is a property of the
workflow, so nothing here notices a change to the *floor claim* — that needs
reading, not a gate. And a `not_exercised` range phrased in a form this parser
does not read has to be taught to it first, a small tax paid to keep an
unreadable gap a failure rather than a silent pass. Falsified in four directions:
a row with no recorded scope, a guard naming a version that is not a row,
`fail-fast` returned to its default, and the unmodified workflow — with the
restored file green as the control. One non-detection is recorded rather than
hidden: moving every guard to a *different real row* passes, because which row
carries the file-reading gates is a decision in `docs/operations/ci.md` and not a
property this gate can read without duplicating that decision.

**The same principle, one function away, and the form that generalises.** Two
gates in `test_doctor_versions.py` asserted that the environment running them
matched a hand-maintained list: one about the interpreter (F018) and one about
git (F019). Each was green on the machine that wrote it, and each was red
somewhere else for an opposite reason — the interpreter assertion failed on every
version the record lacked, the git assertion failed on the runner, which ships a
git nobody recorded. **A gate that reads its own environment is only as portable
as the record of that environment**, and adding the missing entry fixes the run
without fixing the assumption.

The portable form separates the two questions. What the *artefacts* must agree on
is checked on the artefacts: every CI matrix row has a recorded scope, and
nothing a row runs is still called unexercised. What the *environment* does not
cover is stated as data — `not_exercised` in both records, with a test that the
list is non-empty, because an empty list reads as "the fleet is complete". And
what a version comparison must do is a property of the comparison: four reachable
states, an `exercised` verdict carrying its entry's scope and the machine it ran
on, and a negative control that emptying the record moves every version off
`exercised` so the weaker assertion cannot pass for the wrong reason. `doctor`
prints "this machine is not in the record"; the suite must not assert it.
