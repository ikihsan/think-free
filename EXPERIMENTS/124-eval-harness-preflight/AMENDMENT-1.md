<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# AMENDMENT-1 — the easy arm fired, and the reason is not surface form

Written 2026-10-13 after the first run, before case C' was written or run.

## What the first run showed

`PROTOCOL.md` declared case C as the **specificity arm**: E114's verifier over
values copied verbatim out of the documents, expected silent. It fired.

| case | declared | measured |
|---|---|---|
| A: committed integer key | fire | `SILENT_NO_MATCH`, 0/80 |
| B: repaired composed key | silent | OK, 80/80 |
| C: values in the document's own form | **silent, FP ≤ 0.02** | **`ALTERNATE_FORM_FP`, 100/107 = 0.9346** |
| D: values the reader wrote | fire | `ALTERNATE_FORM_FP`, 16/24 = 0.6667 |
| E: E116 control arm | fire | `CONTROL_NOT_EMPTY`, 4/20 = 0.2000 |

All 100 condemned values in C carry the verdict `ungrounded_claim`, never
`ungrounded_value`. That distinction is the whole diagnosis: the verifier found
every one of them **in the document** (`found` is true, score > 0) and still
condemned them, because `judge()` requires the answer's *context words* to
overlap the document's context by `threshold=0.6`, and the probe sentence was
mine — `"The document states $56.00."` — whose content words are
{document, states}.

So C did not fail because the verifier cannot read a verbatim value. It fired
because **a bare sentence containing the value has no content words in common
with the document**, and the verifier scores context, not just presence.

## Why this is not patched away

The obvious repair is to write a richer probe sentence, re-run, and report the
expected 0.02. That would be tuning the arm until the declared answer appears,
which is the thing F110 and F121 are about. It is also, on inspection, the
wrong conclusion: the run has identified a **second axis** of the same defect
family, and it is larger than the one F118 recorded.

F118's rule is about *surface form* — the model writes `49 CFR $2,600.
1150.31-1150.35`, the key says `49 CFR 2600.1150.31-1150.35`, the strings
differ. E114 measured 0.0069 false alarms on values carrying **real
surrounding prose**, and 1.00 on values read bare. **The false-positive rate is
a joint property of the value and the sentence it arrives in**, so it is not a
constant of the instrument at all:

| host text | false-positive rate | source |
|---|---|---|
| the reader's own prose, value in situ | 0.0069 | E114 `KG-C2`, 145 values |
| a bare sentence naming the value | 0.9346 | this run, 107 values |
| real reader prose, alternate surface form | 0.6667 | this run, 24 values |

An instrument's false-positive rate, measured on one arm, transfers to no other
arm. E114's 0.0069 is true and useless as a qualification of this verifier: it
was measured on the easiest host text available, and the tool was pointed at
the hardest.

## Amendment

1. **Case C stays as run.** The declared expectation was wrong and the
   measurement stands. K2 is recorded as **failed as declared**.
2. **Case C' is added**: the same verifier, over values taken from the real
   answers with their real surrounding sentences, labelled correct by an
   independent string search of the document rather than by the verifier's own
   score. Its purpose is the pair the protocol cares about — *does one
   instrument behave differently across arms?* — and it doubles as an
   independent reproduction of E114's "0 of 374 values fabricated" claim, since
   its label is string membership and nothing else.
3. **The tool's rule is restated**: C2 must be run on host text of the kind the
   instrument will actually be pointed at, and the arms must be reported
   separately. A single aggregate false-positive rate is a statement about the
   arms, not about the verifier.

Case C' is declared here and written after this file; the commit order is the
evidence.