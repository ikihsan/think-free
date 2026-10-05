<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# E023 protocol — what is the base rate of "served"?

Written 2026-10-05, **before any reply was read for this experiment**. T-0067.

## Why this and not the next thing on the list

`STATE-next-actions.md` item 0 rests on E022's reading, and E022's reading rests
on one number: **15 of 39 hand-labelled replies named an artifact serving the
clause, 0.385, CI95 [0.249, 0.541]**. From that the record concludes the corpus
is "a population of needs the world **absorbed conversationally** rather than
one awaiting a builder", and on that basis narrows the mission's only untouched
asset.

**That number has no control.** E022 declared three outcome classes and three
controls, and two of the controls (C1, C2) measure `answered` — whether a reply
exists — not `served`. The protocol's own line is that "`answered` is not
`served`", and the cell that carries the conclusion is exactly the one with no
counterfactual. A rate is not a rate until something is compared to it.

## The claim under test

**H.** Ordinary comments in these same threads receive replies naming an artifact
that serves what the comment said at a materially lower rate than comments
stating an unmet need do. Falsifier: if the control arm's rate is
statistically indistinguishable from 0.385, then "served" measures **thread
conversations rather than needs**, E022's conclusion does not follow from its
evidence, and the `answered` control arms are the wrong control for the cell
that carries the finding.

Scope: Hacker News comment threads, one community, observed 2026-10-05. Nothing
here generalises to unmet need in general. This is a **baseline measurement**,
not a candidate generator, and it licenses no product.

## Arms, all three required

- **A1 — need arm, re-read blind.** Re-sample 39 need comments by E022's stated
  rule and seed, re-label them under the same rubric, by a reader who does not
  consult E022's `raw/labels.tsv`. This measures **label reliability** and is
  the arm that makes B and C interpretable.
- **A2 — control arm.** Comments in the same stories matching **none** of the 23
  trigger phrases, sampled at the same size, labelled identically. E022's
  `raw/control.jsonl` holds 13,409 of these and 9,748 are answered; the sample
  is drawn from the **answered** ones so both arms share the "a reply exists"
  condition and the comparison isolates `served` from `answered`.
- **A3 — nonsense control (C3, repeated).** The reply reader is asked for the
  reply tree of a fabricated comment id. A `200` with content falsifies the
  reader.

## Gates, declared before observing

- **Gate B1 (population read, ≥95%).** At least 95% of each arm's rows resolve
  to a readable item record. A failed row is `unreadable`, never `not_served`.
- **Gate B2 (the headline comparison).** The arms differ if the Wilson 95%
  intervals of the two `served` proportions do not overlap. Overlap reads
  **`not informative`**, which is a real verdict and not a failure of the run.
- **Gate B3 (label agreement).** Report Cohen's kappa between A1 and E022's
  labels on the same rows. Below 0.4 the comparison in B2 is reported **as a
  disagreement between readers, not a difference between populations**.

## The strongest alternative, named now

**The alternative is that this is a labelling artifact, not a population
difference.** Two readers applying a subjective "does this reply serve what was
asked" rubric to short Hacker News text will disagree, and the disagreement can
easily span the whole 0.25-wide interval. A3 cannot detect that — it only tests
the fetcher. So the instrument's own reliability is measured (A1, B3) *before*
the population difference is believed (A2, B2), and a difference that appears
only when agreement is high is reported as provisional.

## Limits, declared before running

- **One reader, no second coder.** The same limitation E022 recorded, and this
  experiment measures it rather than removing it. A1 gives the magnitude.
- **The control arm is not a random comment.** It is defined by *not matching
  the trigger vocabulary*, which is a real selection: a comment matching no
  trigger may still be a need phrased unusually. The arm therefore measures a
  **lexically-defined** baseline, and a gap between the arms is a lower bound on
  the need effect.
- **`partial` is counted as not served**, exactly as E022 counted it
  (15/39, not 25/39). A different choice changes the headline, so it is fixed
  here.
- **No claim is made about whether 0.385 is high in absolute terms.** Only about
  whether the need arm differs from ordinary comments in the same threads.