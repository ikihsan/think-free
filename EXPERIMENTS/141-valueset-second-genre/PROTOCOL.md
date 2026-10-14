<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E141 PROTOCOL — does the value pre-pass keep its operating point on a
# human-written genre with real ungrounded values?

Written 2026-10-14, before the corpus was fetched into the repository and
before any instrument was run on any item of it. Standard library only,
deterministic, no network after the single fetch.

## 0. What E140 left open, and what this run is for

E140 measured a deterministic value canonicalizer (`valueset.py`, called M2
there) at **0 false positives in 929 values** and perfect detection of
substitution and omission, on Federal Register final rules, against answers a
model wrote. It then measured the canonicalizer's declared blind spot —
**binding** — and found 0 of 6 mechanical misattributions detected. The
proposal E140 left standing is therefore not "a faithfulness check" but a
**pre-pass**: settle the value question cheaply, hand only the binding
question to the expensive check.

E140's own next action was to run `valueset.py` unchanged on a second genre.
This protocol does that, and it changes three things about how, each forced by
a lesson the record has already paid for:

1. **The genre's wrongness is not constructed here.** E140's `C`, `K` and `X`
   arms were corruptions written by the same session that wrote the
   canonicalizer. A pre-pass validated only on its builder's own corruptions is
   validated on near-copies. This run takes a corpus in which the ungrounded
   cases were written by other people and never touched afterwards.
2. **A coverage floor is declared before the run.** E113 found a whole line of
   experiments reporting a 28% screen as a 100% measurement, because nothing
   measured the fraction of the population the instrument labels at all
   (F116). K3 and K4 below exist because of that, not because of anything
   observed in SQuAD.
3. **Every denominator is the items in which the condition can hold, and the
   exclusion is checkable from the arm file** (D110). K1's denominator is
   stated as a one-line regex over the corpus, readable before any instrument
   runs.

## 1. The question, and the one that is not being asked

**Asked.** On a genre whose questions, paragraphs and answer spans were all
written by people, and where the unsupported items are unsupported because a
person made them so:

- does the pre-pass find a value the source does not contain, when a person
  asserted one (**K1**);
- does it stay silent when the answer is correct (**K2**);
- and what is its **triage operating point** on the whole corpus — the
  fraction of items it can settle without an expensive check at all.

**Not asked.** Whether a pre-pass is a faithfulness checker. E140 measured that
it is not one, on its own corpus, and repeating it here would buy nothing.
Whether this is a product. Nothing in this run establishes demand, adoption, or
a distribution channel, and no result below is read as doing so.

## 2. Population and provenance

| | |
|---|---|
| corpus | SQuAD v2.0 **dev** — 11,873 questions over 1,204 paragraphs |
| file | `dev-v2.0.json` as served at `rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json` |
| sha256 | `80a5225e94905956a6446d296ca1093975c4d3b3260f1d6c8f68bc2ab77182d8` |
| bytes | 4,370,528 |
| fetched | 2026-10-14, once, and committed with its digest |
| fields used | `context`, `question`, `is_impossible`, `answers[].text` |
| labels | answerable 5,928; `is_impossible` 5,945 |

Every byte of the population is human-written: Wikipedia paragraphs by
thousands of authors, questions and answer spans by crowdworkers instructed to
ask about the passage in their own words. That last instruction is what makes
the false-positive arm a **paraphrase arm** — the question restates a fact in
words the passage does not use — which is E140's `P2` arm with a different
author.

**Disclosed before predeclaration.** The counts above, the field names, and one
item's text (`"Who gave their name to Normandy in the 1000's and 1100's"`,
whose plausible answer is `"Normans"`) were read from the file before this
protocol was written, while checking that it is reachable and has the structure
the design assumes. **No instrument was run on any item**, and no rate,
coverage or verdict is known. The single item is a useful reminder of what the
corpus contains: it asserts `1000` and `1100` where the passage says *10th* and
*11th* centuries, which is a value error a human made and no builder planted.

## 3. Task shape

- **reference** = the paragraph, the human-written source of truth.
- **submission** = the question, a space, then the answer span. Both halves are
  human-written; the answer span is a literal substring of the paragraph, and
  the question is a human restatement of it.

A submission therefore carries two kinds of value claim: one the source
provably contains (the answer span) and one it may not (the question). The
second is where the false positives live and where the real errors live.

## 4. Arms, fixed before any instrument runs

| arm | definition | ground truth |
|---|---|---|
| **A** | every answerable question | grounded |
| **B** | every `is_impossible` question | unsupported |
| **A∧D** | A items whose question contains a digit | grounded |
| **B∧D** | B items whose question contains a digit | unsupported |

`D` is `\d` over the question text. It is one regex, readable from
`arms.jsonl` without running anything, which is what D110 requires of an
exclusion.

**K1's denominator is B∧D, not B.** A B item whose question asserts no value
cannot carry a value error, so scoring it as a miss would charge the
instrument for a population the pre-pass was never written for — F125's own
error, in the same shape. Such items are `not_evaluated` for K1 and are
reported with their count.

## 5. The instrument, unchanged, and one declared change in how it is used

`EXPERIMENTS/140-judge-form-invariance/valueset.py` is imported **unchanged**,
and so is the extractor it imports, `EXPERIMENTS/114-value-grounding/ground.py`.
Neither is edited, forked, or re-tuned for this corpus. Its
Federal-Register-shaped patterns — CFR and U.S.C. citations, docket and RIN
numbers — are expected not to fire here, and a general bare-number or
hyphenated-range match is expected to fire on things that are not values at
all. **Both are reported, not fixed.** A genre-specific extractor is a
different instrument and would be a different experiment.

**The one declared change is in the comparison, not the code.** E140 scored
M2 as a **multiset equality**: a complete list of values against a complete
list. A QA answer is not a complete list — it is not supposed to mention every
value in the paragraph — so equality would score the answer as an omission
error for being an answer.

Here the pre-pass is scored one-directionally:

- `extra` = canonical values the **submission** asserts and the **reference**
  does not contain. Non-empty ⇒ **condemn**.
- `missing` = values the reference carries that the submission does not
  mention. **Not scored.** Reported as a count, so a reader can see how much of
  the reference each answer ignores.

E140's substitution arm produced both directions, so this is strictly weaker
than what M2 already passed: a substitution still yields an `extra`, a pure
omission yields none. That is the correct semantics for the job and it is a
concession, declared before the run, not after it.

## 6. Baseline

M1 — `ground.py`'s own `judge()`, unchanged — on the same arms and the same
denominators. E140 measured M1's false-positive rate as 0.3727 → 0.4651 →
0.6019 as rephrasing deepened on the regulatory corpus. **What is asked here
is whether that transfers**, on a genre whose values are years, counts and
quantities rather than dollar amounts, thresholds and citations. A number
quoted on one arm does not transfer by assumption (F123, F125); it transfers
only by measurement.

No LLM judge runs in this experiment. E140's `model_graded_fact` arm is the
comparison and it was measured on a different corpus at n = 24, which is too
thin to carry a second-genre claim.

## 7. Gates, declared before the run

| gate | declared | what a failure means |
|---|---|---|
| **K1** | `extra` non-empty on **≥ 0.95** of B∧D | the pre-pass does not find a real human value error at the rate it found a synthetic one |
| **K2** | `extra` empty on **≥ 0.98** of A (FP ≤ 0.02) | the pre-pass condemns correct human answers |
| **K3** | M2 extracts **≥ 1 value** from the submission on **≥ 0.30** of A | the genre does not carry a value population; the second-genre test is `not_evaluated` on the mechanism |
| **K4** | M2 extracts ≥ 1 value on **≥ 0.30** of A∧D and on **≥ 0.30** of B∧D | the digit-bearing subsets are value-bearing to the instrument, and coverage is reported at both denominators rather than only the flattering one |

**Kill condition.** K3 < 0.30 ⇒ the genre does not carry a value population and
`valueset.py` stays an experiment artifact; the mechanism is not disproved,
because it was not exercised. K1 < 0.95 **on a K4-passing arm** ⇒ the real
detection rate is below the synthetic one, and the pre-pass claim is withdrawn
rather than re-tuned.

K3 and K4 are floors, not targets. They are the two gates whose absence F116
traced to a line of confident wrong answers, so they are here to be failed.

## 8. The number the build decision turns on

Declared now, so it cannot be selected after the numbers are visible.

Over **all 11,873 items**, the pre-pass returns one of:

- **condemn** — the submission asserts a value the source does not contain.
  The item is wrong on the value question. No expensive check is needed for
  that question.
- **clear** — every value the submission asserts is in the source. The value
  question is settled; **binding is untouched and still open.**
- **defer** — no value asserted at all, so there is no value question to
  settle.

The **triage operating point** is `condemn + clear`: the share of a real
corpus the cheap pass resolves without an expensive check. A pre-pass is worth
building when that share is large **and** K2 holds, because that share is the
judge budget it removes.

**A large `clear` share is not by itself a win, and this protocol will not read
it as one.** `clear` is where the instrument is blind, by construction and by
E140's measurement. The decisive companion number is **how many genuinely
unsupported items sit inside `clear`** — that is the pre-pass's real exposure
on real data, and it is the single figure that decides whether a pre-pass in
this position can be shipped to anyone.

## 9. What this run cannot show

Declared before the run, as the protocol requires:

- **One genre, one dataset, one threshold, no held-out split.** The extractor
  was written against a different corpus (F114, F118). A pass here is evidence
  about a mechanism, not about generality.
- **The answers are spans, not free prose.** A QA answer that asserts a wrong
  value in a full sentence is not this shape.
- **SQuAD2's ungroundedness is mostly semantic**, not numeric. The honest prior
  is that `clear` will contain many genuinely wrong items. If it does, that is
  a measurement of the blind spot on a real population, not a defect of the
  canonicalizer, and the report will say so in those words.
- **No judge, no cost model, no demand.** Nothing here is evidence of
  usefulness, differentiation or adoption.

## 10. Commands

```bash
python3 build_arms.py     # corpus -> arms.jsonl, plus the K4 exclusion report
python3 score.py          # arms.jsonl -> gates.json, run after build_arms
python3 test_squad.py     # the checks the numbers depend on, against the corpus
```
