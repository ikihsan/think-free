# Decisions — how this repository's own gates are written and run

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

Decisions **D024–D026, D030, D036–D039**. Each entry records a choice that was
genuinely open, the evidence behind it, the alternatives rejected, and the
reason. Decisions that constrain later work belong here; ordinary edits do not.

**Invariant:** every entry here governs *how this repository verifies itself* —
the shape a gate, a diagnostic, or its control must have before it is trusted,
whichever record it reads. What a named record of this repository **is** —
a function of the tree rather than of the clock, free of a number that means two
things, held to the artefact it claims to describe — belongs in
[`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md). How work is recorded, moved, or
published in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md); what *passes* in
[`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split from `DECISIONS-PRACTICE.md` on 2026-10-03 (T-0018) when that file reached
297 of the 300 permitted lines. Entries moved verbatim; numbering is continuous
and unchanged, so any existing reference to a decision id still resolves.

Split again on 2026-10-04 (T-0042), when D029, D032 and D035 moved out to
[`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md) so that D036 had somewhere to
live: this file was at 297 of 300 permitted lines and its own header said the
next gating decision could not be recorded. The line between the two files is
the one D032 and D035 already used in their own text — *the check must read the
property* says nothing about **which** property, while each of D029, D032 and
D035 is about one artefact this repository keeps. Entries moved verbatim;
numbering is continuous and unchanged.

**This file's header was false until 2026-10-04 and no gate said so.** It read
`Decisions **D013, D024–D029**` while defining D024, D025, D026, D029, D030,
D032 and D035 — naming D013, which lives in `DECISIONS-SESSIONS.md`, and
omitting three of its own entries. T-0030 read the index row in `DECISIONS.md`
in both directions and T-0036 read the numbered defect list, and neither read
the line under the title, which is the first thing a reader sees. The rule that
now does is `tools/originlib/decisionheader.py`, and it reads this line as the
third source of decision identifiers rather than as prose.

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

## D036 — Every source of an identifier is read through one entry point, and a rule that cannot read its input says so (2026-10-04)

Observed: `doc lint` rule 7 read findings definitions, findings index rows and
decision spans, and not the numbered list in [`STATE-defects.md`](STATE-defects.md).
T-0034 and T-0035 were written on two VMs in the same hour and both took **defect
7** — this one on the interpreter assertion, that one on the credential fixture.
Both copies reached the shared base (`e53ca23`, `e701ad8`), each VM's own tree
internally consistent, and nothing reported it, because the collision exists only
in the merged result and every gate was reading a document rather than the merge.
The unpushed side renumbered 7 and 8 to 8 and 9 in `157e463`, which is the
standing rule and the cheapest available repair.

Decision: **a source of identifiers is read by one function that both publishing
gates call.** `tools/originlib/idcheck.py` is that function, so adding a source
is a change to that one file and nothing else — and a module wired into one gate
is provably not read by the other. Two obligations follow, and the second came
out of the first control failing. First, the entry point has to be the only
wiring, because T-0036's own first implementation added `defectlist` to `doc
lint`, and `land` — the operation that *creates* an identifier collision — went on
not reading it. Second, **a check that cannot read its input reports that it could
not**: a `STATE-defects.md` from which no entry can be read is itself a violation,
because a parser that quietly stops matching is indistinguishable from a clean
tree.

Rejected: adding the check to `doc lint` alone, which is what the defect list
was, and which defect 10 records as the cost. Rejected: preventing the collision
rather than detecting it — `idalloc` allocates from the shared base (T-0031) and
still cannot stop two VMs allocating between their own fetches, so detection is
needed anyway and T-0030 is where it lives. Rejected: renumbering the defect list
into a table of `F`/`D`/`T` identifiers, which would be easier to read and would
destroy the one document here whose numbering is chronological and continuous by
construction.

**The obligation earned a third source, and it was found by reading the record
rather than by a red run.** A decision number is written in three places that must
agree: the `## Dnnn — …` heading that defines it, the index row in
[`DECISIONS.md`](DECISIONS.md) that says which file holds it, and the
`Decisions **…**` header each record opens with. T-0030 read the second and
T-0036 the defect list; neither read the third, so two of the five decision
records were false while every gate passed — `DECISIONS-GATING.md` naming D013,
which lives in another file, and omitting three of its own entries, and
`DECISIONS-PRACTICE.md` naming a `D011–D018` range that covers three entries which
moved to `DECISIONS-SESSIONS.md` when T-0030's split was reversed.
`tools/originlib/decisionheader.py` reads it, reached through the same entry
point, so this file's own header is now held by the rule that describes it.

**Ceiling, stated rather than discovered later.** The header is compared as a
set of identifiers and not as wording, so a range that expands to the right
numbers passes however it is spelled, and a header is a claim about a file's
contents that a reader may reasonably distrust anyway. It does not read
`docs/INDEX.md`, `STATE*.md` or `tasks/INDEX.md`, which carry dates and paths
rather than decision identifiers. It reads one line per decision record; a
document that defined decisions outside a `DECISIONS*.md` file would not be asked
for a header, and nothing checks that such a document exists.

## D037 — A violation carries the location its own rule knows, and the workflow publishes it (2026-10-04)

Observed: a red `Documentation lint` named a step and nothing else, because the step
ran the gate, printed its report, and exited — and the run log that says which rule
failed needs repository admin rights. F019 cost an hour of elimination finding that
out, and recorded the reason as a property of the API that was false (`FAILURES.md`
F020). T-0040's prose lived in [`docs/operations/ci.md`](docs/operations/ci.md) for
a session because this file was at 297 of 300 and could not take the entry; the split
that freed the room was T-0042's, and this is the decision it was holding.

Decision: **the location travels with the violation, and the workflow publishes it
in a form a reader without rights can see.** So a gate's report stays a report, and
`origin annotate` re-emits each violation as one workflow command naming the file the
rule that found it already knows — read from the **structured** field, never parsed
out of the message, because `doc lint` also reports `identifier collision: …`, which
begins with a word and would be read as a path by a parser.

Rejected: making the run log readable, which needs rights this repository does not
have and which nobody should acquire to read one line of a diagnostic. Rejected:
teaching the workflow to parse each gate's own report, which is the D025 shape — a
reader sees the field it happened to look at and concludes about the property. And
rejected, on the evidence, the reading that `file=` reaches the reader but is not
filed on: F021 measured run `37191658964` and GitHub files it, so the document that
said otherwise was wrong.

**Ceiling:** this decides what a violation publishes, not whether the publication
happens — which is D038, and which F021 shows is a separate failure with its own
evidence.

## D038 — A step whose only job is to emit a diagnostic runs whenever the job runs, and the mechanism is measured by a probe on the same run (2026-10-04)

Observed: every gate step carried `if: matrix.python-version == '3.12'` and no status
function, so GitHub's implicit `success()` skipped all five whenever `Tests` failed.
Runs `37189825232` and `37190842104` carry no annotation the annotator emitted, and
four gates did not run at all with nothing in the annotations to say so. That produced
F021: a run's annotations were read as the mechanism's behaviour when the mechanism had
not run, and a test's assertion diff was read as an emitted command.

Decision: **two obligations, both falsifiable against the workflow's own bytes.** A
step whose purpose is to emit a diagnostic says `always() &&`, and the workflow is held
to it by a test that names the step and its expression when it is absent — because a
skipped gate is indistinguishable from a passing gate in the annotations, which is
D030's confusion one level down. And **a diagnostic mechanism is measured by a probe
that runs on every push**, not inferred from whichever run happened to be red:
`origin probe` emits one annotation per rendering shape, so the reference and the
failure come from the same place.

Rejected: reordering the job so the gates precede `Tests`, which hides the skip rather
than removing it and makes the tests the step whose own annotations are lost. Rejected
a probe that emits `::error`: whether an `::error` annotation can itself change a
green job's conclusion has never been observed here, and publishing that assumption on
every push is the record asserting something it has not measured — so the probe emits
only levels a green run already publishes.

**Ceiling:** the gate reads the workflow's text, so it cannot tell a step that ran and
passed from one GitHub chose to skip; only a run says that, which is what the probe is
for. And the probe measures the shapes it lists, so a shape not listed is not measured —
`tests/test_probe.py` holds the list literally for that reason.

## D039 — A refusal the tool's own next command cannot carry out is not yet a refusal (2026-10-04)

Observed: `sync land` stopped on a real content conflict in `tasks/CLAIMS.jsonl` and
said *resolve it and land again*. The second `land` could not: it refuses on a dirty
tree, and resolving the conflict is what makes the tree dirty. The only way out was
`git rebase --continue` by hand, which records no `base_advance`, so every path the
base brought was attributed to the session that resolved the conflict — defect 2's
ceiling, reached through a refusal message rather than by anybody's mistake.

Decision: **a refusal is part of a diagnostic, and a diagnostic whose instruction the
same tool cannot follow is not finished.** `land` completes a rebase it stopped on
once no path is still conflicted, and the three answers git's state has to give are
read in one place: both rebase backends (2.25 writes `rebase-apply`, 2.26
`rebase-merge`, and reading one is a check that passes on half the fleet), the
unresolved paths, and the pre-rebase tip from git's own `orig-head` rather than
`HEAD`, which mid-rebase is already the base carrying this branch's commits.

Rejected: making the reader commit the resolution, which asks for a judgement about
a conflict the tooling detected. Rejected: auto-resolving a ledger conflict the way
the generated indexes are auto-resolved — right for a file that is a function of the
tree, wrong for a record, since dropping a claim line loses the fact that two VMs
believed they held a task. Rejected: reading the tip from `HEAD` and accepting the
attribution, which is the defect.

**Ceiling.** A rebase an operator started by hand is resumed just the same, because
git's recorded state does not say who began it; and a path dirty and *not* staged is
refused rather than absorbed, since the continuation commits the whole index.
