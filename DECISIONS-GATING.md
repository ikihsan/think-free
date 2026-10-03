# Decisions — verifying, screening, and judging work

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

Decisions **D013, D019–D026**. Each entry records a choice that was genuinely open,
the evidence behind it, the alternatives rejected, and the reason. Decisions that
constrain later work belong here; ordinary edits do not.

**Invariant:** every entry in this file governs *how work is verified, screened,
or judged* — verification strictness, kill gates, screens, and verdict rules.
If a decision can be restated as "how work is recorded, moved, or published",
it belongs in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md) instead. The index is
[`DECISIONS.md`](DECISIONS.md).

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
## D019 — A candidate may not be implemented until its witness is run (2026-10-03)

Observed: `HYPOTHESES.md` carried "information-sufficiency witness" prose for
three candidates but none had been executed, while the A1 masking experiment was
already being deepened.

Decision: run the witness for every held candidate before any implementation.
A passive candidate that cannot separate two realities with identical inputs and
different outputs is information-insufficient and must narrow its input or permit
refusal; an active candidate fails only when *no* permitted observation
separates the pair. Results are recorded per candidate in `HYPOTHESES.md`, and a
disproved input set is recorded in `FAILURES.md`.

Rejected: treating the witness as a formality after the fact, because a gate
written after seeing results is a rationalisation; and applying it only to the
candidate then in focus, because the two others were cheap to screen in the same
session and one (knitting) failed.

Consequence: the knitting candidate's input set must add loop orientation or
refuse (F007); the sidewalk and ventilation candidates may proceed to their
behavioural experiments under their stated scope conditions.

## D020 — Screen candidates by whether a surviving result changes a build decision (2026-10-03)

Observed: `STATE.md` asked for the six sealed investigations to be compared with
E's and F's criteria as a screen. Applying them literally produced nothing — F's
C1–C6 describe a built repository (a runnable README, one-command install, CI
coverage) and score **not applicable** against six unimplemented candidates, so
they discriminate nothing. Applying E's entry criterion alone also failed to
separate the software candidates: E1 and E3 both have killing experiments much
smaller than the argument for them.

Decision: screen on three questions in order, and require all three before an
experiment is scheduled. (1) Is the experiment that could kill the candidate
smaller than the argument for keeping it (E)? (2) What does a user receive, in
how many steps, and at what comprehension cost (F's time-to-first-value, not its
checklist)? (3) **If the gate passes, what gets built** — a nameable mechanism
with a nameable owner, or nothing? Question 3 is the discriminator E and F left
out, and it is the one that killed E1: jitter is in every modern client library,
so a passing simulator would confirm a 2015 blog post and change no build
decision.

Consequence: F's C1–C6 stay a **gate at stage D**, applied to a repository that
exists, and are not cited as a candidate screen. E1 is not run despite being the
cheapest experiment in the repository. The screen itself, with the full
per-candidate tables and the ranked next actions, is
[`RESEARCH/SYNTHESIS.md`](RESEARCH/SYNTHESIS.md).

Rejected: applying C1–C6 as written and reporting six "not applicable" rows as
the result, because that is a screen that cannot fail and therefore teaches
nothing; and ranking by cheapness alone, because the cheapest experiment here
(E1) is also the one whose outcome changes nothing.

## D021 — An experiment is judged by the setting that can fail, not the best one (2026-10-03)

Observed: the interrupted T-0011 draft defined its "bounded" planner by taking the
product of every per-neighbourhood candidate. Measured, that product equals the
oracle's `2**|errors|` on every T-0010 case, so its `all_optimal = true` was a
tautology of the decomposition rather than a result. The replacement planner
produces two settings that are also optimal — and two of them (`cap=1, beam=2`,
`cap=2, beam=4`) turn out to evaluate exactly the oracle's `2**|errors|`
combinations, because keeping a second candidate per chunk is exhaustive search
wearing the planner's clothes.

Decision: report the whole sweep, name the setting that fails and the settings
that only look good, and count work as patch subsets enumerated **plus**
combinations evaluated, because the combination phase is where the cost hides.
A kill gate must name the setting it applies to. Settings that turn out to
enumerate the baseline's own search space are labelled as such in the results and
never counted as evidence for the planner under test.

Rejected: reporting only the headline setting, because a reader would then take
the best number as the planner's quality and never learn that the cheap settings
fail; and "the planner is optimal, so it works", because optimality that follows
from the model's structure is a check on the implementation, not a discovery.

Consequence: `EXPERIMENTS/005-knitting-bounded-search/README.md` states the cap
and beam sweep, the family-by-family work ratios (1.28x *worse* than the oracle
on T-0010's own cases), and the explicit verdict that "bounded neighbourhood" is
not an efficiency claim at this scale. The chunk cap is recorded as the failure
boundary: whole neighbourhoods are exact, per-error chunks are not.

## D022 — A kill-gate condition naming "prior art" must name which claim it gates (2026-10-03)

Observed: the knitting candidate's kill gate read "abandon the
algorithmic-advantage claim if existing graph tooling already supplies equivalent
intervention sequences". One sentence, two different claims: whether a *knitting*
tool already does this, and whether the *algorithm* is new. T-0015 answered both,
in opposite directions — no tool was found, and the mechanism has been published
since 2007 — so a single verdict would have been wrong whichever way it went, and
a later session reading only the verdict could not tell which claim died.

Decision: when a kill gate's condition contains the words prior art, no novelty,
or differentiated, the report must answer **one row per claim inside the
condition**, each with its own result and its own confidence label. A condition
whose reading is ambiguous is split in the record, not resolved silently by the
agent running it.

Rejected: picking the reading that made the candidate look best, because that is
the failure the gate exists to prevent; and rewriting the kill gate after seeing
the result, which turns a predeclared gate into a rationalisation (the D020
reasoning in a new place).

Consequence: `RESEARCH/PRIOR-ART-KNITTING.md` carries the two-row verdict table,
the algorithmic-advantage claim is recorded as `FAILURES.md` F009, and the
surviving physical question (Stage B) is stated as the only thing left for the
candidate. Any future kill gate that gates on prior art should be written with
its claims separated in the first place.

## D023 — Honour the declared gate metric; record that it cannot fail separately (2026-10-03)

Observed: E3's predeclared kill gate is "below 5% non-normalized wheel
timestamps, E3 is a weak lead". `EXPERIMENTS/007-build-timestamps/` measured
0.965 on that metric (T-0013), and the same run computed two stricter fractions
— 0.670 of wheels with disagreeing entry dates, 0.145 spanning an hour or more —
which the earlier interrupted run had printed first. 1980-01-01 appears in a wheel
only when the builder pins the DOS epoch, which almost nothing does, so the
declared metric is met by any ecosystem that does not pin, whether or not it is
reproducible. Zero of 200 wheels carried a unix-epoch string in `METADATA` or
`RECORD`, so the mechanism's stated assumption is half false as well.

Decision: the verdict is taken on the metric the report declared, not on the
stricter one the code happened to compute first, and the stricter fractions are
reported beside it as lower bounds that cannot overrule it. A gate whose metric
cannot fail is recorded as its own finding (`FAILURES.md` F010) with the
follow-up measurement that could decide the claim (T-0017), rather than fixed by
silently swapping in a metric chosen after seeing the data.

Rejected: (a) ruling on the stricter metric, because a gate is a commitment made
before the data and choosing the metric once the numbers exist makes the gate a
rationalisation; (b) ruling the gate invalid and declaring the experiment
uninformative, which discards a real prevalence measurement because the stated
metric is weak; (c) reporting only the favourable 0.965, which is the failure this
decision exists to prevent — the same shape of near-vacuous gate as F008.

Consequence: the census reports `lead-survives` and F010 explains why that
verdict licenses nothing yet. The attribution measurement is T-0017
(`EXPERIMENTS/008-build-timestamp-attribution/`).

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
