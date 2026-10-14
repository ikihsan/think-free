<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E141 — AMENDMENT 2

Written 2026-10-14, **after `test_squad.py` ran and before `score.py` ran.** No
declared gate is changed, and none is added. This amendment discloses a control
failure and adds one *reported distribution*, because the failure's only
consequence worth having is a number measured on the real corpus.

## What the control found

`test_squad.py` carries six hand-written positives: a document and a
submission that assert **the same values, written differently**. They are not
copies of the arms that built the canonicalizer, and they are the shapes a
person actually writes. Four pass. Two do not:

| positive | document writes | submission writes | the instrument says |
|---|---|---|---|
| thousands separator dropped | `$12,500,000` | `12500000 dollars` | **condemn** — `('num', 12500000.0)` is not `('money', 12500000.0)` |
| currency word instead of the sign | `$12,500,000` | `12.5 million dollars` | **condemn** — `('num', 12.5)` is not `('money', 12500000.0)` |

The mechanism is small and it is in the data model, not in the surface rules:
`valueset.canonical` keys each value by its **kind** as well as its number, so
the same magnitude reached without a currency sign is a different key. The
canonicalization of a money value is exact; the *type* attached to it is not
invariant under rewriting.

**Why E140 did not see this.** E140 measured 0 false positives in 929 values
across three correct arms, all on Federal Register final rules, where a dollar
amount is written with a `$` essentially always. A false-positive rate quoted on
one arm does not transfer by assumption — F123 said so, F125 sharpened it, and
this is the first measurement in this repository where that rule cost the
instrument rather than the report. **E140's 0.0000 was a true measurement of
that corpus, and it is a statement about the corpus's writing convention as
much as about the canonicalizer.**

The control stays in the suite as an expected failure. `valueset.py` is not
edited, per PROTOCOL.md §5: a fix written before the real corpus is scored
would be a fix written against a hand-built example.

## What follows from it, and the one thing added

The failure is on a hand-built example. Its consequence for the build decision
is entirely a question about the **real** corpus: SQuAD2's correct answers are
crowdworkers' own words, so they should occasionally write a number the way the
paragraph does not. Whether they do, and whether that is the dominant false-
positive class or a curiosity, is measurable and was not.

So `score.py` gains one reported distribution: **a taxonomy of every
condemnation on arm A** — for each correct item the pre-pass condemned, the
`extra` keys, whether the matched reference value was the same number under a
different **kind**, and whether the same numeric magnitude appears in the
reference under some other kind at all. That last column is the one that
separates "the instrument was right and the corpus is genuinely inconsistent"
from "the instrument cannot tell two renderings of one number apart".

It is a distribution. It carries no threshold, because the threshold that would
make it a gate — what share of A may be condemned for a kind mismatch before
K2 fails — would be a gate chosen after seeing its own input.

## What this amendment does not do

It does not touch K1, K2, K3, K4, or K5, and it does not lower any of them. If
the taxonomy comes back saying that most of arm A's false positives are
kind-mismatches, then K2 fails for a reason this amendment has already named
in advance, and the report will say the canonicalizer is a pre-pass for
regulatory text rather than for general prose — which is a narrower, more
useful claim than the one E140 left standing, not a softer one.
