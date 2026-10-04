# Decisions — what this repository's own records must be

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

Decisions **D029, D032, D035, D041, D043, D046, D047**. Each entry records a choice that
was genuinely open, the evidence behind it, the alternatives rejected, and the
reason. Decisions that constrain later work belong here; ordinary edits do not.

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

**Why this split and not the one T-0030 reversed.** The reversed attempt moved session-state
decisions out of this file while another VM appended to its destination in the same hour, and
both moves overflowed: a file at 289 lines with a real invariant is a smaller problem than
two files whose prose contradicts each other. The line between these two files is the one D032
and D035 already used in their own text — *the check must read the property*, which says
nothing about **which** property, against *a named record of this repository*. The earlier
attempt drew its line between two claims about session state, which is why the two VMs
claimed incompatible invariants.

## D029 — A generated file is a function of the tree, never of the clock (2026-10-04)

Observed: `doc lint` failed on 42 committed session reports and all three indexes on
2026-10-04, the day after they were generated. Nothing in them had changed except the
calendar: each stamped `last-verified` with `now`, and rule 5 compares a committed generated
file with what the generator produces *now*. CI would have failed on the same comparison for
any push after local midnight, on any VM, for content nobody had touched — found while
running T-0024's own verification, which could not pass.

Decision: every generator stamps `last-verified` from the content it renders — a session
report from its newest event, the sessions index from the newest session's, the tasks index
from the newest claim in the ledger, the docs index from the newest `last-verified` it lists.
An index with nothing to index says `unknown`, because a stamp nobody can support claims a
verification that never happened.

Rejected: making rule 5 ignore the stamp, which would hide a real staleness in
every other field; and pinning CI's date, which a hosted runner does not let a
repository control.

**Ceiling.** A generated file is now stable until its *content* changes, which
is the property rule 5 was written to check. The date no longer tells a reader
when the file was last regenerated — only when its newest input was verified,
which is the claim the field can actually support.

**Falsified against its own defect.** `tests/test_generated_stamps.py` moves
`events.now_iso` to 2031 in place: against the pre-change code, 2 failures and 1 error,
with `doc lint` reporting the four stale files. A first attempt failed to falsify anything
— it mutated a fallback the two callers never reach — and was redone by reverting the three
generators. Both runs are in session 015's `commands.log`; the method is in
[`gate-falsification.md`](docs/policy/gate-falsification.md).
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

**Ceiling, and it is the same ceiling defect 5 records.** This is a detector, not an
allocator: it can refuse a commit that reuses an identifier and cannot stop two VMs allocating
at once. It reads the tree, so a collision created and resolved between two pushes is never
seen. Hypothesis identifiers are out of scope, and an index row is matched on identity alone.
Bookkeeping hygiene with a measured cost; it says nothing about any candidate.

**Falsified against its own defect, in two directions.** Over all 174 commits on the shared
base the rule reports **one** — `e6eb992` — and the hand repair a minute later is clean. The
second direction mattered more: the first version of the decision-index check matched nothing
in any commit, its regex not allowing a Markdown link, so a check that had never fired looked
identical to one that had nothing to report. The control — this repository's two paraphrased
rows — is what found it.

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

## D041 — A link's verdict is a function of the repository, never of the checkout's neighbours (2026-10-04)

Observed: T-0047 shipped `../../docs/reference/identifier-allocation.md` from a task file
and recorded that `doc lint` passed on it in the worktree the branch was built in and failed
on the same bytes in the main checkout after landing — and could not reproduce which run
decided it. `check_links` asked `exists()` of each candidate, so a link leaving the root was
decided by whatever the checkout's *parent directory* held. Measured: one probe document,
identical bytes, two checkout locations — no finding where the parent held the target,
`broken link` where it did not. D035's form, one question further out: F018 and F019 read a
record of the environment inside the repository, and this read the filesystem *outside* it.

Decision: **containment is decided lexically** from the link and the root —
`os.path.relpath`, never `Path.resolve()`, so the rule asks the filesystem nothing beyond the
existence check it already made. An escaping link is its own violation rather than a broken
one, so the reason printed is the reason found and `origin annotate` files it.

Rejected: `Path.resolve()` plus a prefix test, which follows symlinks and reads the disk again
— the same defect one indirection away. Rejected: warning rather than reporting, which leaves
a tree publishable that CI cannot diagnose. Rejected: reporting an escape as `broken`, which
names the wrong reason and would still differ between two machines.

**Ceiling.** Inline links only, and `check_links` still trusts git for the file list, so an
untracked document is invisible to it as to every other rule. Method and the falsification
script: [`gate-falsification.md`](docs/policy/gate-falsification.md).

## D043 — A record says one thing once; a merge that makes it say it twice is reported (2026-10-04)

Observed: commit `eff1126` was a rebase of one VM's T-0047 branch onto a base the
other had already extended, and it carried `STATE.md` with a byte-identical second
copy of its `Implemented (2)` dashboard row — one row from each VM. Every gate
passed: line cap, metadata, links, orphans, generated freshness, identifier
agreement. The reload point a cold session reads first therefore showed two rows
that are one fact, and the next session found it by reading and removed one by
hand. Nothing scanned for it, because nothing reads a document for repetition.

Decision: **a hand-authored document may not contain the same table row twice.**
The exemption is keyed on the `generated-by: origin` marker rather than on a path or
an extension, because the property that distinguishes the two cases is *whether the
repetition is the point*: measured 2026-10-04, 47 tracked documents contain a
repeated row, every one of them a generated session report listing an artifact once
per event, and 0 hand-authored ones. A path-based rule would have had to enumerate
the exceptions and would have gone stale; a marker reads the document's own claim
about itself, which is the same property `check_meta` already reads.

Rejected: **deduplicate silently**, which would hide which of the two copies a VM
meant and make the next merge of the same kind invisible for a second reason.
Rejected: comparing only the first cell, which would call two rows that differ in a
later cell duplicates and report a fact that is not there. Rejected: treating two
identical rows in two *different* tables of one document as a duplicate, since they
are two tables. Rejected: leaving it to `idcheck`, whose subject is the identifier
record — a repeated row is not an identifier collision, and T-0036's lesson is that a
rule read by one gate is not thereby read by the others.

**Ceiling.** Rows are compared as their exact Markdown text, so a row differing in
one cell is a different row; only pipes-delimited tables in `.md` files are read, and
the rule reads the working tree rather than what a renderer would produce, so a stale
generated file remains `doclint_tree`'s subject.

## D047 — A restated number is held to the artifact it names, by the number's shape

Evidence: T-0056, session `2026-10-04-042`, 2026-10-04. Defect 22 in
[`STATE-defects.md`](STATE-defects.md); [`FAILURES-findings-5.md`](FAILURES-findings-5.md)
F024.

**The choice.** A mission record's restated number is checked against the
machine-readable result it names, and the check is decided by what the number
*is*: a fraction `N/M` is a claim about a countable population, so `M` must be a
count the artifact declares; a decimal is distinctive enough to match against any
value the artifact states. A bare integer, and a number in a line naming two
experiments, are not read.

Rejected: **"does this number occur anywhere in the artifact?"** — the obvious one, and it
is *green on the defect*, since `113` also sits at `patch_cost_sensitivity/*/cases`. A rule
that reads every value in a file concludes about a different property than the one a sentence
claimed: D025 with a new environment, not a field that means something else but a **value**
occurring where something else is meant. Rejected: **guessing which nested field is the
"headline"** by depth or by key — the borrowed-predicate mistake D042 records, one level up.
It needs a case per artifact, and on this tree admits either `113` or the true values of `006`,
never both. Rejected: **requiring every restated number to cite the field it came from.** Only
that design generalises; it changes the shape of a hand-maintained index rather than adding a
gate, and it is the right next step if this coverage is ever found wanting. Rejected: exempting
a **tool version** behind a keyword list — `2.30` and `0.30` are the same shape. Reported
instead, with the remedy in the message: environment facts belong outside the results table.

**Ceiling.** One row per experiment in one index. Prose is not read, and neither is
`STATE.md`'s dashboard row, which names all nine experiments at once — so the most
prominent restatement of these numbers in the repository is *not* covered, which is
stated here rather than left to be discovered. The loose rule's blindness is
asserted in `tests/test_result_numbers_falsified.py`, so the restriction cannot be
dropped quietly.

## D046 — A list split across files is read by a reader that reads all of them

Evidence: T-0056, session `2026-10-04-042`. Defect 22 in
[`STATE-defects.md`](STATE-defects.md).

**The choice.** `STATE-defects.md` was split at its 300-line cap, and
`defectlist.py` reads **every file of the list** rather than the first. The parent
file's own record had said the split could not be made without exactly this change
— "it cannot be done inside its own numbered list without `defectlist.py` reading
more than one file" — and it was done here rather than by trimming an entry to make
room, the cut falling at the `## Open` heading the document already states as a
boundary.

The alternative was to leave the reader pointed at the parent and note in prose that
the other half is unchecked. That is the defect the rule exists to catch: **the
reason `defectlist.py` reads this list at all is defect 10**, where two VMs took
defect 7 in the same hour, each tree internally consistent, and only a human reading
the file reported it. A duplicate spanning the two halves is invisible to a reader of
either half, so it is exactly the case the rule must catch and exactly the one a
single-file reader cannot.

Rejected: **trim entries instead of splitting** — what the cap has been met with five
times already, each time repaired by moving material to the file whose invariant owns
it. Rejected: **making the split generate both files**, which would make a numbered
list a derived artefact and lose the property that an entry is written once, by the
session that found it.

**Ceiling.** A **gap** in the numbering is still unreported, and after a split a gap
can straddle the two files as easily as sit inside one — so this fixes the reader, not
the coverage. Both halves are checked in `tests/test_defectlist.py`, including a
control asserting that reading only the parent would have missed the collision the
split makes possible.
