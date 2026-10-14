<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E140 — AMENDMENT 5

Written 2026-10-14, **after** the declared gates were evaluated. Nothing below
changes a gate, a threshold, a denominator or an arm of the declared experiment.
It adds one exploratory arm, with no gate, to settle the single weakness the
protocol declared in advance and then did not test.

## What the protocol declared and did not measure

PROTOCOL.md §M2, "M2's declared weakness, stated before the run":

> Comparing value *multisets* binds nothing to what the value is said to be
> about. An answer that lists every right number attached to the wrong
> descriptions passes M2 and fails M1's `ungrounded_claim` verdict.

Every other arm measures substitution (`C`), omission (`K`) and form (`P`,
`P2`). Misattribution — the right value attached to the wrong subject — was
named as the weakness and left unmeasured, so the RESULT would have had to
report the artifact's central limitation as `inferred by construction`. That is
the one claim here worth an hour, because it decides whether the artifact is a
usable first pass or a misleading one.

## The arm, and its construction rule, fixed here before it was built

`misattribution.py`, arm `X`:

1. split the verbatim answer into clauses;
2. keep clauses holding exactly **one** extracted value;
3. swap the values between the first two such clauses whose values are of the
   same kind;
4. touch no other character.

K4 applies to `X` exactly as to `P` and `P2`: the canonical value multiset must
equal `V`, and an item that fails is dropped and counted. So every value in an
`X` row is present, correctly written, and correctly formatted — each is simply
attached to the wrong subject. That isolates exactly one property: **binding**.

## Observed

Six of the fifteen items could carry the arm; nine were dropped and the reasons
are in `misattribution.json`.

| instrument | items flagged of 6 |
|---|---|
| M2 `valueset.py` | **0 of 6** |
| M1 `ground.py` | 6 of 6 |

K4 held on all six (`k4_all_preserved: true`), so the zeros are not an arm that
failed to be built.

## What this changes

The protocol's proposal — M2 as the cheap pass that runs **first**, with M1's
slower check behind it — is supported in the right order and contradicted in the
second half. M2 is blind to binding, and M1, which is not blind to it, flags
every `X` row **and** 37 to 60 per cent of the correct ones. The instrument that
covers the weakness is the one this repository has now measured twice and found
unusable as a gate (F118, F123), and the instrument that is usable is the one
that cannot see the weakness. That is the finding, and it is a statement about
the pair, not about either instrument alone.

## Status

Exploratory, no gate, no threshold, nothing else in the protocol altered. Its
ceiling is mechanical misattribution by transposition on one genre; a swapped
value, a paraphrased binding and a binding that is wrong in prose rather than by
transposition are `untested`.
