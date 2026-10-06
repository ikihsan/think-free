# E031 — Amendment 4

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the adjudicator labelled all 200 pairs and before any
rate was computed from those labels.** This adds the one control the amended C1
gate lacks, and it is the same mistake E022 made and F043 measured: an arm whose
instrument had never been shown capable of returning a positive.

## What the labels say, and why that is not yet a finding

The adjudicator marked **0 of 100 candidate pairs** and **0 of 100 control pairs**
as `same` — 95 `different` / 5 `unclear` on the candidates, 100 `different` on
the control. On its face the amended gate fails: it required ≥ 2 adjudicated-same
independent pairs and got 0.

**That is not yet a measurement of the world.** An instrument that answers `no`
to everything, for any reason — a reader who reads "same" too strictly, a rubric
whose bar is unreachable, pairs that genuinely never match — produces exactly this
output. The screen cannot distinguish those three cases, and E022's
`38.5% served` figure survived a decade of this repository's records before F043
showed it was the base rate of ordinary comments.

## The gate added: A6, a positive control the instrument must pass

A fourth view, `raw/view_e031_pairs_poscontrol.txt`, of **20 pairs built to contain
the same requirement twice**, paired with a second reader who has seen none of the
candidate or control pairs.

Construction, fixed here, mechanical, and applied to clauses that were **not** in
either pair set:

1. Take each q1-`yes` clause in the three arms that is **at least 6 words** long.
2. For each, build a **second rendering** by a declared deterministic transform
   (`build_poscontrol.py::paraphrase`): drop **every** stopword token and every
   token of the departing artifact's own name, lower-case the first remaining
   character, strip a trailing full stop, and prepend `no way to`.

   *Corrected 2026-10-05, before the positive control was adjudicated.* This
   amendment first described the transform as producing "a second phrasing
   without reusing the original's wording". It does not: the pair shares nearly
   all of its content words, so **a reader could pass these positives by string
   matching rather than by reading**. The mechanism is stated accurately now and
   **A6's claim is narrowed to match it**:

   **A6 tests that the instrument can return a positive at all, and — through
   the matched negatives — that it does not return one indiscriminately. It does
   not validate semantic paraphrase discrimination, and a reader that recognises
   these pairs by eye has still satisfied the gate.** The instrument's ability to
   separate a genuine recurrence from lexical resemblance is therefore **not**
   established by A6. That ability is the very thing the 100/100 real-pair
   `different` answers dispute, so the dispute survives a passing A6 and is
   recorded as a ceiling on the verdict rather than settled by it.
3. A positive pair is that clause with its paraphrase, ordered so the paraphrase
   is clause B. **20 pairs**, drawn by `random.Random(3123)`.
4. **Matched negative pairs** are drawn from the same pool, each pairing two
   clauses from **different** stories, different authors and different departing
   artifacts, at the same clause-length band as the positives, with no transform.
   The declared count is 20; the first run produced **10**, because the median
   length band (9.5–15.5 words) admitted too few eligible partners. A6's negative
   threshold is therefore evaluated on **whichever count the build produced**, and
   `poscontrol_build.json` records it. The *rate* threshold (≤ 0.20) is unchanged;
   only the denominator is whatever exists, and a smaller denominator widens the
   interval, which is the conservative direction.

A6 fires only if the adjudicator marks **≥ 16 of 20** positive pairs `same` **and
≤ 4 of 20** matched negatives `same`. The 0.80 / 0.20 thresholds are declared
here, before the view exists and before the reader runs, and they are the same
shape as the separation gates A5 and E029's C1.

**Why these thresholds.** A6 does not need to be a precise instrument; it needs
to be shown capable of a positive at all. A reader that cannot recover 16 of 20
synthetically-identical pairs has not read the task, and its 200 `no` answers
carry nothing about the world. A reader that marks the matched negatives `same`
at a high rate is answering "yes" without discrimination, and its zeroes on the
real pairs carry nothing either.

## What each outcome changes

| A6 | reading |
|---|---|
| **fires** | the instrument is shown capable of a positive and of rejecting matched negatives. Its 0/100 on the candidate pairs is then **a finding about the corpus**, subject to the sample ceiling below. |
| **fails** | the pair instrument is named blind. The recurrence verdict is **`not_evaluated`**, the 0/100 is reported as an instrument reading and not as evidence about public accounts, and E031 joins E028 in this record's set of named-blind instruments. |

## The ceiling, restated because it now carries the whole verdict

216 rows across three arms yields 63 clauses. Even with a working instrument, a
real-but-small recurrence — two people who needed the same thing twice — has a
low probability of both landing in one arm sample of 25 clauses. **A null here is
a statement about 63 clauses, not about public technical discussion.** A6
establishes whether the instrument works; it cannot make this sample large
enough, and no gate here claims it can.

## Unchanged

The candidate and control pair sets, their seeds, their sizes, the q4 wording,
A3's κ floor, H1's margins, and A5's separation are as declared in
AMENDMENT-3. This amendment adds one view and one gate. It does not re-draw any
pair, re-judge any of the 200 labels, or move the ≥ 2 same-pair requirement.