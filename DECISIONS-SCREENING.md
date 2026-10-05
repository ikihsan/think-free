# Decisions — screening candidates and judging experiments

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

Decisions **D019–D023, D055, D056**. Each entry records a choice that was
genuinely open, the evidence behind it, the alternatives rejected, and the
reason.

**Invariant:** every entry here governs *what passes*: which candidates and
experiments are screened in or out, what a kill-gate condition may mean, and
which metric a verdict is taken on. How this repository's own gates are written
and run belongs in [`DECISIONS-GATING.md`](DECISIONS-GATING.md); recording and
publishing in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md). The index is
[`DECISIONS.md`](DECISIONS.md). **D048 onward is in
[`DECISIONS-SCREENING-2.md`](DECISIONS-SCREENING-2.md)**, which carries this
same invariant continued rather than a new one.

Split out of `DECISIONS-GATING.md` on 2026-10-03 (T-0020), first when D027 pushed
that file past the 250-line split trigger and again when D024–D027 took it past
the 300-line cap. Entries moved verbatim; numbering is continuous and unchanged,
so any existing reference to a decision id still resolves.

Split again on 2026-10-05 (T-0063) when D051 pushed this file to 324 of the 300
permitted lines: D048–D050 moved verbatim to
[`DECISIONS-SCREENING-2.md`](DECISIONS-SCREENING-2.md).

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

## D055 — A hand-labelled rate is only a finding once a control arm shares the population it controls (2026-10-05)

Observed: E022 concluded that a need corpus is "a population of needs the world
absorbed conversationally" from two numbers — 58.0% of 1401 statements drew a
reply, and 15 of 39 hand-labelled replies named an artifact serving the clause
(0.385). The second number had **no control**: E022's C1 and C2 both measure
`answered`, and its own protocol says "`answered` is not `served`".

T-0067 (`EXPERIMENTS/023-served-baseline/`) drew the missing control: ordinary
comments in the same stories, matching none of the 23 trigger phrases, and
**restricted to answered** so both arms share the "a reply exists" condition. The
need arm reads 15/38 = 0.395 and the control arm 14/38 = 0.368, with the Wilson
intervals overlapping. The rubric is not the cause: two readers labelled the
identical 39 rows at κ = 0.9226.

Decision: **a rate measured against no population is a rate, not a finding, and
no state record may carry one into a conclusion that depends on the difference.**
The 0.385 is withdrawn as a demand-side measurement. It describes how Hacker News
conversations go, and the record read it as a description of needs.

The two design rules this commits to, both written into E023's `PROTOCOL.md`
before the run:

1. **A control arm shares the conditioning of the arm it controls.** `served` is
   defined only where a reply exists, so a control drawn from unanswered comments
   would re-measure `answered` — the cell E022 already controlled. This is the
   rule that made E023 a test rather than a second reading of the same
   population.
2. **Instrument reliability is established before instrument output is
   believed.** Gate B3 is computed and reported *before* gate B2, because a
   difference between populations means nothing while two readers disagree about
   what the labels mean. E022 recorded "one reader, no second coder" as a limit;
   this turns that caveat into a measured quantity by re-reading its own sample.

Rejected: (a) keeping the 0.385 with a caveat, because the number's function in
the record is comparative — it is what makes "absorbed conversationally" sound
like a demand-side discovery — and a caveat on a number doing comparative work
does not reduce that work; (b) re-running E022 with a second coder only, which
would measure the rubric's reliability and still leave the population question
open; (c) drawing the control from all non-trigger comments regardless of whether
they were answered, which is the cheaper draw and measures `answered` again.

Consequence: `STATE.md` item 0 rests on E022's `answered` rate and its build arm,
both of which survive; the sentence about `served` is withdrawn. Nothing reopens
a prior-art death, the 589 unanswered statements, or item 12. F043.


## D056 — A kill-reason count is a finding about the procedure, and a majority gate with a one-row margin is reported as a plurality (2026-10-05)

Observed: "twelve candidates, twelve prior-art deaths" was carried in four
summaries and was the stated premise of E015/F034, E016/F035, E017/F037,
E021/F041 and of item 0. T-0068 counted it from the primary records
(`EXPERIMENTS/024-kill-reason-causes/`) against a population rule, four
categories and a declared precedence written down first: **prior art is 10 of 18
eligible rows = 0.556, and the population is 20 rather than twelve.**

The gate survived. **The margin is the finding.** Every one of the 10 prior-art
rows, moved to any other declared category, puts the share at 9/18 = 0.500 and
kills it; six rows are contested by the declared precedence and moving all six
also kills it.

Decision: **a majority gate declared against a bare threshold is reported with
its sensitivity, and a result that one reclassification reverses is reported as
the plurality it is.** This experiment's own declaration omitted the sensitivity
band and had to have it added after the run — the defect was in the protocol, not
in the data, and the amendment is recorded rather than applied silently.

Two design rules this commits to:

1. **A cause claim about the mission's own record is counted from primary
   sources, with the deciding sentence quoted per row.** The four files that
   carried "twelve" reconcile with neither the inventory's sixteen nor any sealed
   report, which is only visible by re-deriving it. `rowcheck.py` enforces that
   each quote is present in the file it cites — a check that caught two restated
   sentences in this session's own hand work.
2. **A control that cannot fail is discarded, not reported as a pass.** The
   declared control failed as constructed on a category-vocabulary mismatch; its
   first repair scored 19/19 and was thrown away. The replacement uses an
   independently produced label set with known errors in it, so the rule is free
   to score worse than the baseline and a worse score is a real result.

Rejected: (a) reporting 0.556 as "prior art is the dominant kill reason", which
is what the declared floor licenses and what the margin does not support;
(b) re-running with a second reader to get κ, which is the right next experiment
and is not this one's scope — the honest reading is a plurality plus an open
reliability question; (c) opening the six contested rows to get a cleaner
majority, which would be choosing a threshold after seeing which side it favours.

Consequence: item 0 stays an owner decision, now over a plurality, and gains a
second option with a count behind it — promote fewer claims and price each one's
gate before promoting it, which is what F006's A1 shows was available at report
time. Nothing reopens a prior-art verdict or a candidate. F044.
