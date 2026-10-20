<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Screening decisions, part 22

Split out of [`DECISIONS-SCREENING-21.md`](DECISIONS-SCREENING-21.md), which held
D124. This part holds the decisions taken when a build trigger that fired on
one population is measured on a second one.

Decisions **D125, D126**. Each entry records a choice that was genuinely open,
the evidence behind it, the alternatives rejected, and the reason.

**Invariant:** the same as [`DECISIONS-SCREENING-12.md`](DECISIONS-SCREENING-12.md)
- a decision belongs to the file whose subject it is, the number is allocated
with `origin id next D` against the base, and the heading, `DECISIONS.md`'s row
and this file's own `Decisions **...**` header all move together.


**Identifier note (2026-10-20 lineage merge):** `E140` and `E141` in this file mean
`EXPERIMENTS/140-judge-form-invariance/` and `EXPERIMENTS/141-valueset-second-genre/`.
The upstream lineage carried two further directories under those numbers, so an
unqualified `E140`/`E141` is disambiguated by directory name from here on.

---

## D125 — a build trigger fires on a population, and is withdrawn by a second population rather than by a better one

**Decided 2026-10-14**, on E141's scoring pass. Evidence:
[`EXPERIMENTS/141-valueset-second-genre/`](EXPERIMENTS/141-valueset-second-genre/RESULT.md),
F145, AMENDMENT-1, AMENDMENT-2.

E140 ended with the first positive build trigger this line has produced:
`valueset.py` at 0 false positives in 929 values, 11/11 substitution, 11/11
omission, every declared gate green, and a protocol that said the next action
is a second genre. E141 ran it unchanged on a second genre — human-written,
11,873 items, no corruption by the experiment — and the trigger does not hold:
detection **0.2826** against a declared 0.95, corpus resolved **0.1647**, and
**0.2763** of what it clears is genuinely wrong.

**The rule.** A build trigger is a claim about an *(instrument, population)*
pair. A second population does not contradict the first measurement; it
**replaces the scope statement with the one that was actually measured.** The
artifact is not deleted — `ground.py` survived E114 the same way — but it is
re-described, and the description is the one the second population supports.

The scope statement E140 left is *value correspondence under rephrasing*. The
scope statement E141 supports is narrower and actionable:

> A value-set pre-pass is cheap and safe enough to **rank** with, is blind to
> binding at 0.2763 of what it clears, and on a corpus where 0.8353 of items
> assert no value it is not worth running at all.

**Alternatives rejected.**

- **Keep the trigger and re-run until a second genre passes.** Rejected: that is
  a search for the population the instrument likes, and the population is then
  part of the claim without being in the denominator. E140's protocol already
  said the next action is a second genre, and a second genre is allowed to say
  no.
- **Fix the two defects this run found — the `(kind, number)` key and the
  century/decade gap — and re-score.** Rejected *for this run*, and the
  rejection is procedural rather than principled: `valueset.py` is imported
  unchanged by protocol, and a fix written after seeing the real corpus's
  misses cannot be evaluated by the same gates. A fixed instrument is a
  different instrument and needs its own predeclared run. Both defects are
  recorded precisely enough that run is cheap to design.
- **Publish it as a tool anyway, with the limitations on the front page.**
  Rejected: this repository's standing rule is that a candidate is not called
  release-ready before its own limitations have been measured over real input
  (D076, F076–F080). This is that measurement.

**Bears on** D076, D109 (E140's own scope: a verifier's rate belongs to an arm),
F123, F144, F145.

---

## D126 — a control the builder did not write is part of the instrument, and its failure is the finding

**Decided 2026-10-14**, on the same run. Evidence: `test_squad.py`
`InstrumentControls`, AMENDMENT-2.

`test_squad.py` carries six positives: one document, the same values, written
the way a person writes them. **Four pass, two fail**, and the two failures are
one mechanism — `canonical()` keys a value by `(kind, number)`, so
`$12,500,000` and `12500000 dollars` are different keys for one number. The
population E140 used could not have found this: all 929 of its values came from
Federal Register rules, where dollar amounts carry a symbol.

**The rule.** A measurement of an instrument carries its own controls, and a
control **written by the same session that wrote the instrument is not a
control** — it is a restatement. Where a run's headline is a *rate*, the run
also owes at least one positive and one negative example that the builder did
not author, and a control that fails is reported by name and left in the suite
as an `expectedFailure` rather than deleted or tuned until it passes.

**The marker is load-bearing.** A fix to `valueset.py` turns the
`expectedFailure` into an unexpected success, which is exactly the signal that
the claim it was standing behind has been falsified and the marker should come
off. A control deleted after it fails is a control that will fail again in the
next run and cost another session to rediscover.

**Alternatives rejected.**

- **Rewrite the two failing positives into forms the instrument handles.**
  Rejected: that is a control rewritten to pass, which is the defect F010
  recorded on a declared gate that could not fail.
- **Drop the two and keep four.** Rejected: the four that pass are the ones the
  instrument already handled, so the surviving set measures nothing the run did
  not already know.

**Bears on** D076 (a control must include the case where the subject is right
and the form is different — F118's rule, now applied to the *builder* rather
than to the arm), D095, F079.
