<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# AMENDMENT-2 — the first checker failed its own negative control; the run is `not_evaluated`

**Date:** 2026-10-12. This is the record the protocol requires before any repair,
because a checker that fails a control, is quietly improved, and is then reported
as having measured something is the shape of a false result.

## What happened

`ground.py` v0 was written, the controls were built, and the controls were run
**first**, as `KG-D` requires. Arm C — verbatim sentences lifted from the document
itself — was flagged at **99 of 270 values (0.367)** against a declared ceiling of
**0.02**.

| arm | values | grounded | flagged | rate |
|---|---|---|---|---|
| B1 corrupted with a value that really occurs elsewhere in the same document | 301 | 122 | 179 | 0.595 |
| B2 corrupted with a same-shape value occurring nowhere | 301 | 122 | 179 | 0.595 |
| C verbatim sentences of the document | 270 | 171 | 99 | **0.367** |

`KG-C2` fails by a factor of 18. Under `KG-D` the run therefore returns
**`not_evaluated`**, and **no rate is reported for arm A**, because an instrument
that cannot separate B from C cannot be asked about A.

## The three defects, each isolated from the committed run

1. **Sentence splitting cuts inside citations.** The splitter breaks on `[.;:]`,
   so `49 CFR 1002.3(a) provide` becomes the fragments `3` and `(a) provide`. The
   context window for a value is then one or two content words taken from the
   middle of a citation, and no window around the matching occurrence contains
   them. This alone accounts for the 37 `ungrounded_claim` verdicts on arm C.
2. **`canonical()` deletes the comma, so no date can ever match.** `"October 16,
   2008"` canonicalises to `october 16 2008`, which does not occur in a document
   that spells it `october 16, 2008`. 22 arm-C dates were reported
   `ungrounded_value` while being verbatim. A checker's normalization must be
   tested against its own control's most ordinary input.
3. **The `code` pattern is over-broad.** `\b[A-Z]{2,5}\s+\d+\b` matches
   `Page 64617`, `Part 1308` and `Section 402` — which is why arm A's raw counts
   were 58% ungrounded before any of this was checked.

## Disclosure, recorded because it is required to be fair

**Arm A's raw counts were seen once before the instrument was validated**:
624 values, 260 grounded, 153 `ungrounded_claim`, 211 `ungrounded_value`. That
number is meaningless — the same run flags 36.7% of verbatim text — and it is
recorded here so a reader does not later find it quoted anywhere as a result. No
conclusion in this experiment rests on it.

## What the repair has to demonstrate

Same three controls, same seeds, same declared thresholds. `KG-C1` (recall on
both B arms >= 0.90) and `KG-C2` (false alarms on C <= 0.02) must be met by
`ground.py` v1 **before** arm A is scored at all.
