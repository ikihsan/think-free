<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E141 RESULT — the value pre-pass on human-written text, and the three
# things that decide whether it is a tool

Run 2026-10-14. `valueset.py` and `ground.py` imported unchanged, as
PROTOCOL.md §5 required. Protocol, AMENDMENT-1 and AMENDMENT-2 written before
any gate was evaluated; AMENDMENT-2 written after a control failed and before
the scoring pass, and it moved no threshold. Raw evidence: `arms.jsonl`,
`gates.json`, `verdicts.jsonl`, `misses.json`, `population.json`, the session's
`commands.log`, and `SOURCES.md`.

## Short answer

**The pre-pass does not generalise to this genre, and the reason is the one it
declared in advance.** On 11,873 real human-written questions it resolves
**0.1647** of the corpus, condemns **0.0244**, and of the items it clears,
**0.2763** are genuinely unsupported. It is not accurate enough to be a gate and
not broad enough to be a cheap substitute for one.

Two of the three numbers that matter are the **artifact's real strengths** — it
does not condemn correct human answers (K2, 0.9887) and it does see values
where the genre has them (K5, 0.9379 conditional on the answer being a value) —
and the third, detection, fails at **0.2826** against a declared 0.95.

## Population

SQuAD v2.0 dev, fetched once, 11,873 questions over 1,204 paragraphs, digest
recorded in [`SOURCES.md`](SOURCES.md) and enforced by `build_arms.py`. Answerable
**A 5,928**, impossible **B 5,945**. Digit-bearing subsets **A∧D 498** and
**B∧D 789**; arm N (answerable, answer span is a value) **853**; arm C
(impossible with a human-written plausible answer) **5,930**.

No item was corrupted by this experiment. Every wrongness is a person's.

## The gates, as declared

| gate | declared | observed | verdict |
|---|---|---|---|
| **K1** detection on B∧D | ≥ 0.95 | **223/789 = 0.2826**, CI95 [0.2523, 0.3150] | **FAIL** |
| **K2** false positives on A | ≤ 0.02 | **67/5928 = 0.0113**, CI95 [0.0089, 0.0143] | **PASS** |
| **K3** coverage on A | ≥ 0.30 | **1272/5928 = 0.2146**, CI95 [0.2043, 0.2252] | **FAIL** |
| **K4** coverage on A∧D and B∧D | ≥ 0.30 both | **0.8956** and **0.8657** | **PASS** |
| **K5** coverage on A∧N (AMENDMENT-1) | ≥ 0.30 | **800/853 = 0.9379**, CI95 [0.9196, 0.9522] | **PASS** |

K3's failure is **not** the extractor's: only 853 of 5,928 answerable SQuAD
answers are a number or a date at all. **Conditional on the answer being a
value, coverage is 0.9379** (K5) against 0.2146 unconditionally. AMENDMENT-1
exists to make that distinction measurable, and it is the difference between
"the instrument cannot see values" and "this genre is mostly not about
values". It is the second.

## Why K1 failed, decomposed

`explain_misses.py` classifies every miss by a fact about the row, not by a
judgement. The 566 misses of 789 split into two mechanisms and nothing else:

| mechanism | n | share of B∧D | what it is |
|---|---|---|---|
| `value_present` | **460** | 0.5830 | the value is real, in the paragraph, and attached to the wrong subject. The pre-pass says `clear` and the item is wrong. |
| `not_extracted` | **106** | 0.1343 | the question contains a digit and the canonicalizer returned **no value at all**, so there was nothing to compare. |

`not_extracted` is a defect nobody had named. The expressions the extractor
cannot see, in order of frequency, are **century and decade forms**: `19th` (12),
`20th` (8), `10th` (6), `11th` (5), `1980s` (6), `1100s` (4), `18th` (4),
`1950s` (4), `1990s` (3), `21st` (3), `17th` (2), `1900s` (2), `1960s` (2). A
bare `\b\d…\b` cannot match `19th` or `1980s` because the trailing letters break
the word boundary. **On an encyclopedic corpus the most common way of stating
a time period is invisible to this extractor.**

`value_present` is the blind spot PROTOCOL.md declared and E140 measured at
0 of 6 on arms it built. **This is 460 items of the same thing, written by
people who never saw the instrument, on a corpus chosen before the run.** The
declared weakness is confirmed at a scale two orders of magnitude larger, and
independently.

## The triage operating point, and the number that decides it

Over all 11,873 items:

| | n | share | what it means |
|---|---|---|---|
| **condemn** | 290 | **0.0244** | an asserted value the source lacks — wrong, no judge needed |
| **clear** | 1,665 | 0.1402 | the value question is settled; **binding is still open** |
| **defer** | 9,918 | 0.8353 | no value asserted; nothing to settle |
| **resolved** (condemn + clear) | 1,955 | **0.1647** | the judge budget the pre-pass removes |

A pre-pass is worth building when the resolved share is large **and** nothing
in `clear` is wrong. Here **460 of 1,665 cleared items — 0.2763 — are genuinely
unsupported.** Read the two numbers together: the pre-pass removes 16% of the
judge budget and, of the 16% it claims to have settled, 28% was never settled
at all.

**That is the finding, and it is a statement about the instrument in this
position, not about the corpus.** 83.5% of a real QA corpus asserts no value
at all; of the 16.5% that does, more than a quarter of the "clear" verdicts are
binding errors the pre-pass is blind to by construction. Used as a gate it is
unsafe. Used as a **ranker** — a flagged item is worth a glance — its condemn
path is 223 correct against 67 wrong, **0.7690 precision** over the whole
corpus, at zero marginal cost.

## The baseline, on the same rows and the same denominators

M1 `ground.py` unchanged, every row:

| | M2 `valueset.py` | M1 `ground.py` |
|---|---|---|
| false positives on A | **0.0113** | 0.0940 |
| detection on B∧D | 0.2826 | **0.7174** |

**E140's reading does not transfer, and the direction of the trade is the
opposite of what it looked like there.** On the regulatory corpus M1's
detection was inseparable from its noise. On human-written encyclopedic prose
M1 detects **2.5× more** of the real errors while flagging **8× more** correct
ones. M2 is not better than M1 here; it is a different point on a
precision-recall curve, and on this population that point is much less
favourable than E140's corpus made it look. Quoting M2's 0.0000 without this
table would be F123 exactly: a rate belonging to one arm, presented as a
property of an instrument.

## What the hand-built control found, and what it cost

AMENDMENT-2's six hand-written positives — the same document, the same values,
written the way a person writes them, not copies of the arms that built the
canonicalizer — **four pass, two fail**, and both failures are the same
mechanism: `canonical()` keys a value by **(kind, number)**, so `$12,500,000`
and `12500000 dollars` are different keys for one number, and
`12.5 million dollars` is a third.

**E140's 0 false positives in 929 values could not have found this.** All 929
came from Federal Register rules, where a dollar amount carries a `$`. The
false-positive rate was a true measurement of that corpus and a statement about
its writing convention.

**On the real corpus the class does not occur: 0 of 67 arm-A false positives
is a kind mismatch.** All 67 are `num` (64) or `qty` (8) magnitudes the
paragraph genuinely does not carry — disagreements about the answer, not
instrument defects. So the defect is real, reproducible, and **latent**: the
kind a genre writes money in decides whether it fires, which is an argument
for making the key kind-free, not an argument that the number was wrong.

The control stays in the suite as an expected failure. A fix to `valueset.py`
turns it into an unexpected success, which is the signal to remove the marker.

## What this changes

**The build trigger E140 fired does not survive contact with a real corpus.**
`valueset.py` stays what E114's `ground.py` stayed: a correct, deterministic,
stdlib-only checker, `status: draft`, unreleased, and now with a **measured
scope** instead of a hoped one. That scope is not "value correspondence under
rephrasing" as E140 left it. It is narrower and more useful:

> A value-set pre-pass is cheap and safe enough to **rank** with, and it is
> blind to binding on real text at 0.2763 of what it clears. It is not a gate,
> and on a corpus where 83.5% of items assert no value it is not worth running
> at all.

**F126.** And the generalisable rule, which is the run's only durable output:
*an extractor's coverage is a property of a genre's writing conventions, and a
coverage number measured on one genre does not license the instrument on
another — but a coverage number measured conditional on the population that
carries the phenomenon is the one that transfers.*

## What remains unknown

- **Third genre, and the one that matters.** This closes the *general* claim
  and leaves the *regulatory* one untested. Federal Register text may well be
  the genre where a value pre-pass earns its cost, because dollar amounts,
  thresholds and effective dates are the answer, not a minority of it. That is
  a measurement, not a conclusion, and it has not been made.
- **Whether the decade/century gap is the whole extraction story.** 106 items
  were not extracted at all; fixing century and decade forms would move
  detection, and by how much is unmeasured, because fixing it would be a
  different instrument and this run's gates do not apply to it.
- **Free prose.** SQuAD answers are spans. A QA answer that asserts a wrong
  value inside a written sentence is not this shape and was not tested.
- **No judge, no cost model, no demand.** Nothing here is evidence of
  usefulness, differentiation or adoption, and the run is not read as any of
  those.

## The single most useful next action

**Close or re-open the pre-pass line with one measurement, not a product.** Run
`valueset.py` unchanged on a corpus of *regulatory* answers that a person wrote
— not the model-written expert answers E140 used — and read three numbers: the
conditional coverage (K5-style), the false-positive rate on correct items, and
the `value_present` share of the misses. If the misses there are mostly
`not_extracted`, the pre-pass is genre-limited and should be described that
way. If they are mostly `value_present` at a rate like this run's, the line
closes for good, because the failure would be the declared blind spot in the
one genre where the instrument was most likely to work.
