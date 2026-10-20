<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 AMENDMENT 3 — how the three roles are executed, and G0a restated

**Declared before any reader saw a row.** The census ran first and is reported
separately; nothing in it is a role's output.

## CLF's population: the 100 highest-`view_count` keyed rows

PROTOCOL.md says "CLF labels all 200 rows". 145 carry a key answer and all 145
would be one reader pass of ~150k tokens of question-plus-answer text. **CLF
labels the 100 highest-`view_count` keyed rows**, split into two batches of 50
run as two independent passes, each emitting labels for its own batch only.

Selection is by arrival, fixed before CLF sees anything, so it cannot select on
what CLF is about to judge. **Cost:** the comparison's population is the
top-100 by arrival of one draw, so it is a **higher-arrival** slice than the
200-row pool and every rate here is conditional on that slice.

## G0a restated

The protocol's G0a as written conflated the treatment's capability with its
arms. Replaced with two items, both declared now:

- **G0a (the treatment is an assistant, not a refuser).** Of the 60 questions
  `ANS` is asked, at least **55** must get a substantive answer — a proposed
  cause, a proposed fix, or a requested next step — rather than a refusal or a
  pure clarification request. Below that, **K2 fires** and nothing downstream is
  reported as a measurement.
- **Abstention by arm is reported, not gated.** If `ANS` declines materially
  more EVID questions than SELF questions, that is a *result about the
  population*, and it is reported next to the reach rates. It is not treated as
  instrument failure, because declining is one of the correct behaviours for a
  question whose evidence is absent and scoring it as `not_reached` is the
  conservative reading.

## Why roles run as passes, and what that costs

`CLF`, `ANS` and `SCORE` each run as separate passes with their own context.
That is what makes the three blinding claims checkable — none of them can see
the other's output — and it is the direct answer to E115's declared single-reader
ceiling and to F049.

**Ceiling, stated plainly:** all three are the same model family. MISSION.md
already records that agents are not independent human validation. Three blinded
passes remove the *ordering* bias that contaminated E170 and E174's arms; they
do not create three independent readers. No claim here may be described as
human-validated.