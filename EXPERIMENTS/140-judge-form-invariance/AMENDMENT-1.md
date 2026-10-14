<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E140 — AMENDMENT 1

Written 2026-10-14 **before any instrument was run on any arm**. No judge call
and no instrument call had happened; what had happened is one execution of
`build_arms.py`, whose output is quoted here because the rule it revealed was
wrong. `arms.jsonl` as first written is overwritten and is not evidence.

## 1. K4 caught the surface transform changing values. The transform is repaired.

First run, `k4_dropped` on **6 of 15 items** — `P` on four items and `C` on two.
Inspecting them: `P` **gained** numeric values and lost none. The gain was
concentrated in citation answers and looked like sections of title 49 being
re-counted — `21.0`, `812.0`, `871.0`, `956.0`, `1641.0`, `553.0`, `1801.0`,
`260305.0` — i.e. `ground.extract`'s longest-match-wins grouping of a citation
run was **being broken by the sentence split**, so digits that had been consumed
inside one `code` match became separate `num` matches.

So the `P` arm was not form-varied, it was **value-altered**, and K4 said so
before any instrument saw it. That is the gate doing its declared job.

**Repair:** `surface_paraphrase` now replaces every `code` span with a
private-use-area placeholder (`U+E000`, `U+E001`, …) before touching the text,
applies the surface changes to what remains, and restores the spans afterwards.
The citation set is therefore preserved by construction rather than by luck, and
sentence splitting can no longer reach inside a citation. Shuffling still
reorders whole items, which is the move intended to break M1's proximity check.

**Consequence for the arm's meaning, stated plainly:** `P` now varies
formatting, unit spelling, punctuation, and item order, and does not vary
vocabulary. That was already declared; this makes it true.

## 2. The corrupter could not fire on 2 of 15 items, so the `C` arm gets a fallback.

E114's `corrupt` requires the replacement's last three digits to occur in the
document. It declined on two items. **Repair:** `B1_from_document` first,
`B2_absent` as fallback. Both replace exactly one value and both are therefore
wrong relative to the expert answer, which is what the `C` arm tests. The mode
used is recorded per item in `arms.jsonl`.

**What this does not change:** the corrupter, its seed discipline, and its
plausibility criterion are E114's, imported unchanged. The fallback widens which
corruptions are *available*; it does not make them easier.

## 3. The judge-subset rule was written against documents, and there are only five.

PROTOCOL.md §deviations said the judge subset is
`random.Random(20261014).sample(sorted(document_numbers), 10)`. The corpus is
**15 answers over 5 documents**, three questions each, so `sample` of 10 from a
5-element list returned all 5 and every item entered the judge arm. The rule was
not wrong by accident: it shows the corpus's shape was not checked before the
rule was written.

**Repair:** the unit is the **answer**, not the document —
`random.Random(20261014).sample(range(15), 10)` over the answers sorted by
`(document_number, question)`. Document numbers are drawn independently so that
all five documents stay represented; without that, a ten-answer sample from five
documents could leave one document out and the judge arm would silently carry
four documents instead of five.

## 4. `K` exists on 11 of 15 items, not 15.

The truncation rule needs at least three sentence-delimited parts, and four
answers do not have them. `K` is therefore **not built** for those four rather
than built by a different rule, because two different truncation rules would
make the arm's rate a mixture of two mechanisms. `K` is excluded from the judge
arm in any case (PROTOCOL.md §arms), so this changes no gate; the count is
recorded so the arm's denominator is not mistaken for 15.
