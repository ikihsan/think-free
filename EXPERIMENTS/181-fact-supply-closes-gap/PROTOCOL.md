<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E181 PROTOCOL — does supplying the missing fact close the evidence gap?

**Date opened:** 2026-10-18. **Status:** pre-declared before any comment on any
row of this population was fetched, before any fact was extracted, and before
any answer body was written. Nothing below may be edited after the first
`facts.jsonl` exists, except by an amendment file that names what it changed
and why.

## Why this axis, and why it is not another population screen

Thirteen experiments in a row measured *whether some population is unserved* and
thirteen answered "no" (E062, E091, E092, E115, E126, E143, E168, E169, E170,
E174, E177, E178, E179). The screen is sound and it has stopped producing
information: it compares a candidate against **one-shot answering**, and one-shot
answering now scores 0.40–1.00 on every population this mission can reach. A
screening instrument whose baseline scores that high cannot separate candidates.

**E177 is the one positive result in the run**, and it has never been used for
anything except more screening. It measured, on one population, under four green
controls, that a free general assistant reaches the accepted resolution on
**26/30 = 0.8667** questions whose resolution follows from the question's own
text and on **12/30 = 0.4000** questions whose resolution depends on a fact the
question does not contain — gap +0.4667, Fisher p = 0.000368 (F136, D118). It
also measured that **abstention was 0 of 30 against 0 of 30**: the assistant
answers confidently on exactly the questions whose deciding evidence is absent,
and is wrong 60% of the time.

So the practical difficulty is already named and quantified, and it is not a
missing population. **It is a missing input, and nobody supplies it.** The
question this experiment asks is therefore not *what need is unserved* but
**what happens to the 0.4000 when the missing fact is put back.**

That is a mechanism question with a product attached, and it is answerable on
data this repository already holds.

## The claim under test, in one sentence with its scope

**Among high-arrival answered Stack Overflow questions whose accepted answer
depends on a fact the question does not state, supplying that one fact raises a
free general assistant's rate of reaching the accepted resolution from the
measured 0.4000 toward the 0.8667 it already reaches on self-contained questions
of the same pool.**

Scope: one venue, one platform, 20 rows, one agent family, no retrieval. It is a
statement about this population and instrument, nothing wider.

## The strongest accessible alternative, named

Not one-shot answering. The alternatives a real user actually has:

| # | alternative | why it is the serious one |
|---|---|---|
| **B1** | **paste the whole discussion** — question plus every comment on the accepted answer, verbatim | costs nothing, needs no new tool, and is what people do. If targeted elicitation only matches this, there is no product. |
| **C1** | **ask the assistant to ask** — two turns, user supplies whatever is asked for | free in every major assistant today. This is the incumbent the treatment must beat on cost. |
| **A0** | one-shot | measured at 0.4000; the floor. |

**A1 is C1 executed by the pipeline:** the assistant identifies the fact it is
missing, the user supplies it, the assistant answers. **The experiment's real
target is B1, not A0.** A tool that says nothing more than "paste the thread" is
not an invention; a tool that delivers the thread's decision-relevant content in
one sentence is. So **G2 compares A1 against B1, and it is declared the
gate that matters most.**

## Population, draw, and why it is not a fresh one

**E177's 30 scored EVID rows, taking the first 20 in E177's `score/index.json`
order.** That order is CLF's emission order, which is the draw order, which is
descending `view_count`. So the 20 are the 20 highest-arrival EVID rows of that
pool, selected by arrival and by nothing anyone saw.

**Why reuse, and the cost declared in advance.** Reuse is the only way every
number here is comparable to E177's 0.4000 and 0.8667, and the reuse is the
same one E177 declared and E177's own `population_sha256` already fixes. The
cost: **these rows are not fresh.** E177's CLF read question+answer on all of
them, E177's ANS answered 30 of them, E177's SCORE graded them, and E178 blind-
re-keyed the same 46 rows against the same key answer. **So this experiment
cannot claim a prevalence, and it cannot use a fresh reader's surprise.** It can
claim a causal comparison between arms, because every arm is generated here.

**Why n = 20 and not 30.** Scoring is the bottleneck and it is a single
unblinded-in-time reader. 20 per arm detects the declared gap comfortably
(`0.40 → 0.85` on 20 rows is ~9-11 discordant pairs, one-directional, exact
McNemar p ≈ 5e-4) and does not support a precise level for any arm. **n is
chosen for the gap, not for the levels** — E177 declared the same rule and this
experiment inherits it.

## Arms, all on the same 20 rows, all answered in this session

| arm | input to `ANS` | role in the design |
|---|---|---|
| **A0** | question text only | floor, re-answered here so that model drift cannot masquerade as treatment effect |
| **A1** | question text + one extracted fact line, under the header `The reporter adds this:` | **the treatment** |
| **B1** | question text + every comment on the accepted answer, verbatim, under `Discussion under the accepted answer:` | **the strongest accessible alternative** |
| **C1** | question text + one extracted fact line **belonging to a different row** | negative control: rules out "any added sentence helps" |
| **P** | E177's committed A0 answer for the same row | drift control against the 0.4000 this experiment rests on |

**C1's fact** is taken by a fixed rule — the `A1` fact of the **next row in index
order**, wrapping at the end — so it is a real extracted fact of the same shape
and roughly the same length, and it is wrong for this row.

**B1's contamination, declared:** comments on a high-arrival accepted answer
frequently contain the resolution, not only the fact (E178 measured
`answer_asks` on 20/46 rows). **B1 is therefore an upper reference that is
deliberately contaminated, and A1 is not.** That asymmetry is the point: the
comparison asks how much of the whole thread is actually needed, and B1 is the
ceiling a user can reach by doing nothing clever.

## Three roles, kept apart, and the order they are committed in

F049 (a judgement re-keyed against the wrong reference) and D061 (a label tied to
no bytes) are this repository's own two failures in exactly this shape.

| role | sees | never sees | writes |
|---|---|---|---|
| **EXT** | question body, the comments on its accepted answer, in order | **the accepted answer body**, any arm label, any assistant answer | `facts.jsonl` — one row per qid: the single missing fact as one sentence with identifiers verbatim, or `no_fact` |
| **ANS** | the arm's own input and nothing else | accepted answer, comments, `facts.jsonl`, any other arm's answer | `answers.jsonl`, one row per (qid, arm) |
| **SCORE** | assistant answer + accepted answer | every arm label, both arms of a pair, `facts.jsonl` | `verdicts.jsonl` — `reached` / `not_reached`, one line |

`facts.jsonl` is committed **before** `answers.jsonl` exists. `answers.jsonl` is
committed **before** `verdicts.jsonl` exists. A reader checks the ordering from
git, not from this file.

**`EXT` sees the comments but not the answer, and that is what makes A1
legitimate rather than a leak.** In a live session the person who asked the
question is present and holds the fact; on these threads the same person wrote it
into a comment. Supplying the comment's content is a faithful simulation of the
user typing the value, and the arm that never sees the answer is the one whose
result can mean anything.

**Exclusion, declared:** a row where `EXT` writes `no_fact` runs **A0 only** and
is excluded from A1 and C1. It still runs B1 if it has at least one comment.
Every exclusion is counted and named.

## Gates, declared before measurement

All three use **McNemar exact, two-sided, on discordant pairs**, because every
comparison is within-row. All three declare both a size and a p-value, because
E170's record shows what a point estimate clearing a bar while its interval does
not looks like on the page (F134).

- **G1 — the fact is load-bearing.** `reached(A1) − reached(A0) >= 0.25` **and**
  McNemar `p < 0.05`. The full available lift is 0.8667 − 0.4000 = 0.4667, so
  0.25 is **more than half of the measured gap**; G1 is a low bar and passing it
  means "the missing input was a real part of the failure", not "solved".
- **G2 — targeted elicitation is not beaten by pasting the thread. This is the
  gate that decides the build.** `reached(A1) >= reached(B1) − 0.10` **and** the
  median token count of the A1 fact block is at most **25%** of the median B1
  comment block. A treatment that matches the thread in accuracy while using a
  quarter of its context is a candidate; one that does neither is not.
- **G3 — the placebo does not work.** `reached(C1)` must be at or below
  `reached(A0)` within noise, declared as `reached(C1) <= reached(A0) + 0.15`.
  At n = 10 this is a weak check and is reported as a weak check; it exists to
  catch "any extra sentence helps", not to carry the claim.
- **G4 — the instrument did not drift.** `reached(P)` on 8 rows must not differ
  from E177's own EVID verdicts on the same 8 rows by more than 3 rows.
  If it does, every number here is `not_established` and the cause is the
  instrument, not the world.
- **G5 — the treatment's precision.** On a blind re-read **after**
  `answers.jsonl` is committed, at least **80%** of A1's facts must be (a) absent
  from the question text and (b) load-bearing for the key answer. `EXT` may not
  see its own facts while grading; the re-read is blind to which arm scored what.

**Kill conditions.**
- **K1.** Fewer than 16 rows carry both an A1 fact and an A0 answer → the
  comparison does not run; report the counts and name which arm is short.
- **K2.** G4 fails → nothing here is a measurement about the world.
- **K3.** G1 fails → **the fact-supply route closes as a mechanism**, and the
  0.4000 is not explained by missing input. F136's *population* gap stands and
  its *mechanism* reading is withdrawn.
- **K4.** G1 passes and G2 fails → **an intervention exists and is not worth
  building**, because a user can already paste the thread and get the same
  accuracy. The population gap is real, the mechanism is real, and the product
  is not. This is the outcome that would leave the mission with a number and no
  invention, and it is named here so it cannot be mistaken for the other one.

## Scoring order, declared in advance

`SCORE` works in a fixed order and the order is part of the protocol, because a
session that runs out of budget must still have produced the headline:

**A1 → A0 → B1 → C1 → P**, all inside one shuffled set so that no reader ever
sees two arms of the same pair adjacently, and the arm label appears in no
filename and in no input file.

## What this experiment does not claim

- **No novelty.** Asking an assistant for missing context is old art and this
  experiment measures its value, not whether it is new. The prior-art screen is
  the named next action **if G1 and G2 both fire**, and it is not run here.
- **No product.** No artifact is proposed by this protocol. It decides whether a
  mechanism is load-bearing and whether targeting it beats pasting.
- **No prevalence**, because the draw is reused and E177 declared that.
- **No cross-venue claim.** One venue, one question shape, high arrival only.
- **Not an adoption result.** Nothing here measures whether anyone would use it.

## Ceilings, declared up front

- **`ANS` and `EXT` and `SCORE` are the same agent on the same day.** E177
  declared that three blinded roles reduce shared bias but do not remove it;
  here there are still three roles with disjoint inputs, and the ordering is
  committed, but one agent is behind all three. A reader should treat a large
  effect as suggestive and a small one as nothing.
- **`ANS` has no retrieval.** That is E177's incumbent and this experiment
  inherits it, so the comparison is fair and the reachability question stays
  open.
- **B1 is contaminated upward** and A1 is not. G2 is therefore biased *against*
  the treatment, which is the direction this protocol wants.
- **One reader labels staleness of nothing here**, but `EXT` is one reader with
  no second coder, and G5's blind re-read is the only check on it.