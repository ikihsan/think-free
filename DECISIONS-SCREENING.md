# Decisions — screening candidates and judging experiments

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

Decisions **D019–D023, D048, D049**. Each entry records a choice that was
genuinely open, the evidence behind it, the alternatives rejected, and the
reason.

**Invariant:** every entry here governs *what passes*: which candidates and
experiments are screened in or out, what a kill-gate condition may mean, and
which metric a verdict is taken on. How this repository's own gates are written
and run belongs in [`DECISIONS-GATING.md`](DECISIONS-GATING.md); recording and
publishing in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split out of `DECISIONS-GATING.md` on 2026-10-03 (T-0020), first when D027 pushed
that file past the 250-line split trigger and again when D024–D027 took it past
the 300-line cap. Entries moved verbatim; numbering is continuous and unchanged,
so any existing reference to a decision id still resolves.

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

## D048 — The next-action list carries at least one invention item (2026-10-04)

Observed: F031 measured where effort went over two days — 1.3% of day-two
commits touched `EXPERIMENTS/`, 4.8:1 lines of record-keeping to
world-measurement, and `STATE-next-actions.md` held no action that could
produce or advance a candidate. No candidate moved as a result, and no
artefact had reported the trend; the drift had become executable.

Decision: `STATE-next-actions.md` must always include at least one action
whose success is a candidate produced, tested, revived, or explicitly
rejected, and that item is reviewed whenever the list is rewritten. Record-
keeping repairs remain legitimate, but they may not crowd out the only zone
whose contents measure something outside this repository.

Rejected: (a) fixing this with a hard quota in the linter, which prices
sessions instead of informing the human choice; (b) declaring the ratio
invalid because lines are a weak proxy, which is true of the metric, not of
the trend it caught; (c) letting the item be optional because invention
cannot be scheduled, which is how the list filled with gates.

Consequence: the allocation measurement stays runnable
(`tools/measure_allocation.py`, held by `tests/test_allocation_measurement.py`),
and the next-action list is expected to show an invention item beside any
infrastructure item.

## D049 — A need corpus supplies problem statements; recurrence comes from a repository-denominated issue corpus (2026-10-04)

Observed: F028. A harvest of 1401 unmet-need statements from Hacker News
comments created after 2024-01-01, screened by a stated rule that drew 50 of
them, yielded **zero survivors** — 38% already served by a tool, 30% stating
no mechanism, 24% not software needs, 8% needing hardware. The prior generator's
own record is 3 live candidates from 16 (18.75%), none validated. The corpus has
no internal recurrence signal either: term recurrence over 1273 clauses returns
only function words. But the same cluster, measured in a different unit, gives
5805 open issues across 28 repositories for `"not asked for"` and 14510 across
29 for `"unrelated changes"`, with `claude-code` and `copilot-cli` in the sets.
F029: one search query decides a prior-art verdict wrongly in both directions —
502 hits from `in:readme` that were `awesome-go`, and 0 hits that became 29-83
on a second phrasing.

Decision: the candidate pipeline has two distinct inputs and they may not be
substituted for each other. A **problem statement** comes from a dated,
countable need corpus; a **recurrence signal** comes from issues counted by
repository, because a thousand issues in one project is one project's problem
and a hundred issues in a hundred projects is a cross-project one. A need
statement alone may not be promoted to a candidate on the strength of its own
existence. And a prior-art verdict requires more than one phrasing, on more than
one corpus, with the phrasings written down.

Rejected: (a) keeping the harvest as the candidate generator, refuted by the
0-against-50 measurement; (b) taking GitHub's issue count as a measure of
prevalence, which is full-text self-selection and needs a repository-signal
filter before it means anything; (c) treating F029's four revised verdicts as
candidate gaps, which is the error the decision exists to prevent; (d) declaring
candidate generation solved and moving on, since 0 of 50 says this generator is
spent, not that the pipeline is.

Consequence: `EXPERIMENTS/011-candidate-harvest/` is retained with its raw
capture and four runnable probes. The next candidate action is to build the
repository-signal filter and re-harvest through it, testing first the cluster
with the strongest measured recurrence — changes a coding agent makes that
nobody asked for — against a stated falsification of its own.
