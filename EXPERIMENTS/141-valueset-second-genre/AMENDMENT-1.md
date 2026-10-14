<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E141 — AMENDMENT 1

Written 2026-10-14, **after `build_arms.py` ran and before `score.py` existed.**
It changes no declared gate. It discloses one observation made outside the
protocol, and adds two supplementary arms with one new floor, because the
observation raises a question the declared design could not answer.

## What happened, plainly

`build_arms.py` ran and wrote `arms.jsonl` and `population.json`. Nothing has
been scored: no gate has been evaluated, no value extracted from any item, no
verdict computed. The population is 11,873 rows, **A 5,928 / B 5,945**, and the
digit-bearing subsets are **A∧D 498 / B∧D 789**. Those are the counts the
protocol's §4 implied and they are reported here so the reader has them before
the scoring pass.

While timing `ground.judge()` to see whether the baseline could run over the
whole corpus rather than a subsample, a 200-row prefix was run. The timing
answer was 0.02 s for 200 rows. The probe **also** counted how many of those
200 submissions the extractor found any value in: **17 of 200.**

That number is a coverage rate, which is what K3 measures, and it is low. It was
seen before K3 was evaluated. The disclosure is the whole point of writing
this; the response is the question.

## No gate is changed, and here is why K3 stands

Lowering K3 from 0.30 to below 0.085 would make the declared experiment report a
pass. That is tuning a floor to a measurement, which is the thing this
repository has been wrong about before (F010: a declared 5% gate that could not
fail; F116: a 28% screen recorded as a 100% measurement). **K1, K2, K3 and K4
are evaluated exactly as PROTOCOL.md declares them, and K3 is allowed to fail.**

What the probe may legitimately change is the *design's* completeness, because
it exposes a gap in the arms rather than a number to be scored: the protocol
assumed the genre carries a value population and made that assumption a gate
rather than an arm. Gates are for pass/fail claims; the population's shape is a
property to be measured and reported, and a run that can only say "fail" on it
is a worse run than one that measures it and says where the value-bearing
sub-population is.

So two supplementary arms are added. Both are defined by ordinary regexes over
corpus fields, both are checkable from `arms.jsonl` alone, and neither
touches K1–K4.

## Arm N — answerable items whose gold answer is itself a value

| | |
|---|---|
| definition | `arm == A` and the gold answer span starts with a digit or a currency sign, or matches a month name |
| regex | `^[\s$€£]*\d` or `^(January|February|…|December)\b`, case-insensitive |
| ground truth | grounded, as for A |
| why | the protocol's A arm is dominated by entity answers, which carry no value at all. Arm N is the part of A where the answer is a number or a date, so it is where the mechanism can actually be exercised on correct human content. |

**K5 (new, declared now): M2 extracts ≥ 1 value from the submission on ≥ 0.30
of A∧N.** A floor, not a target, and the same floor as K3 so the two are
readable against each other. A∧N is expected to clear it comfortably; if it
does not, the extractor cannot see the very answers it was built to check, and
that is the finding.

K1 and K2 are **not** restated on A∧N. They keep their declared denominators. A
second FP rate on a sub-population is a reporting convenience and will be
reported as one.

## Arm C — impossible items carrying a human-written plausible answer

| | |
|---|---|
| definition | `arm == B` and the row has a non-empty plausible answer span |
| submission | the question and the **plausible** answer, not the empty one |
| why | this is the closest thing in the corpus to M2's declared blind spot, on text nobody built for this experiment. A plausible answer is a human-written span from a **different** passage that answers the question as asked. Where its values are absent from the given paragraph, the pre-pass is right to condemn. Where its values are *present* in the paragraph but attached to the wrong subject, the pre-pass is blind — and the item is wrong. |

Arm C gets **no gate**, because its ground truth is genuinely mixed: a
plausible answer drawn from the same article can share values with the given
paragraph while still being wrong, and this run has no instrument that could
say which is which. It is reported as a distribution, not scored.

## What this amendment does not do

It does not move K3, and it does not add a pass that would have been reported
without it. The expected headline — that SQuAD2 dev is a thin value genre for
this instrument and the coverage number is low — is unchanged by this
amendment; what changes is that the run will also say **where the value-bearing
sub-population is and what the pre-pass does on it**, instead of stopping at
the word "fail".
