# Decisions — how this repository's own gates are written and run

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

Decisions **D013, D024–D027**. Each entry records a choice that was genuinely open,
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

## D013 — Local verification tolerates an in-flight session; CI does not (2026-10-03)

Observed: `origin preflight` failed whenever it was run during a session, because
the current session has no `session_end` yet. A gate that cannot be run while
working is a gate that gets skipped.

Decision: `session verify` and `preflight` report the session in flight as
"in progress" and exit `0`. Both accept `--strict`, which fails for it; CI uses
`session verify --strict`, since on a pushed commit nothing is in flight and an
unfinished session genuinely is a failure.

Rejected: dropping the check for unfinished sessions entirely, because then a
crashed run would be indistinguishable from a completed one. Making strictness the
only mode, because it would make local use useless.
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
## D027 — An unfinished session fails CI only when it is provably abandoned (2026-10-03)

Observed: D013's premise does not hold for this fleet. `task claim` requires
HEAD to equal the remote base before it publishes a claim, so a VM that claims a
task must push its `session_start` first — measured on 2026-10-03 as `dfa6eb9`
(session 030's start) immediately followed by `4791ed3` (its claim). The
unfinished session is therefore *structurally required* to be on the shared base
branch, and `session verify --strict` failed on every push of every VM for as
long as any session was open. Run `37157528596`: four gates green, one red, and
the red one was reporting correct behaviour against an impossible premise.

Decision: strict verification asks whether an unfinished session is still **in
flight**, derived from the tree alone by `tools/originlib/inflight.py` — its
`session_start` names a task; that task is `claimed`; the claim identifies this
session by `claim-session`, or failing that by `claim-agent` plus `claim-vm`;
the last ledger entry for that task still opens a claim; and the claim is
younger than `--lease-hours` (default 12). An unfinished session failing any
clause is **abandoned** and fails the gate with the clause named. An in-flight
one is a note printing task, holder, and claim age, which CI re-emits as a
`::warning::` annotation. D013 is unchanged for the session running in the
working tree being checked.

Rejected: (a) dropping `--strict` entirely, which loses every unfinished-session
signal including the ones this keeps; (b) making the whole check a warning,
which leaves a crashed session indistinguishable from a live one forever; (c) a
bare staleness window on the last event with no claim check, which cannot tell
one long honest session from a dead VM's while the record already carries the
thing that can; (d) keeping in-flight sessions off the base branch by publishing
claims on a separate ref, which would hide the claim from `sync land` and from a
reader browsing the base branch — trading a cosmetic problem for the real one.

**Cost, stated plainly.** A crash *inside* the lease window is not detected by
this gate: the claim stays in force for up to `--lease-hours`, so a dead VM's
session keeps CI green for that long. Bounded detection comes from `task list
--remote`, which names the holder and the claim time, and the lease is a flag so
an operator can shorten it. No lease at all was rejected because "in flight"
with no upper bound is precisely the hiding place this replaces.

**Ceiling.** One gate made truthful. It says nothing about whether the claims it
trusts are true, and a session that crashes after `task complete` still looks
finished. Those are different problems, not solved ones.

**Clause 1 relaxed by observation, not by design.** The first implementation
required the `session_start` to name a task. Run against the live record it
immediately produced a false red: `instance-20260717-0944` started session
`2026-10-03-037-repair-the-three-mission-records-corrupt` without `--task` and
then claimed T-0021, so the predicate read a demonstrably live session as
abandoned. A claim in the ledger that *names the session* is now accepted in
place of the `task` field, under the same opening-action and lease clauses.
`--task` should still be passed; the fallback exists because the predicate met
reality, not because omitting it was right.

Consequence: `tools/origin session verify --strict` exits `0` in this repository
while a session on either VM is in flight; `tests/test_inflight_session.py`
fails if any clause is removed (verified by mutating each clause and re-running);
`docs/operations/ci.md` states what the gate now catches and what it does not.

Split on 2026-10-03 (T-0020): D019–D023 moved verbatim to
[`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md), because adding D024–D027 took
the gating file past the 300-line cap. D025 and D026 were written on
`instance-20260717-0944` while this branch was unpublished, so the session-gate
decision drafted as D025 is D027. Numbering is unchanged.
