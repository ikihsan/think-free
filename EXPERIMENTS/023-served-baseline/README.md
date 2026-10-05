# 023 — what is the base rate of "served"?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

**Date:** declared and run 2026-10-05. **T-0067.** The declaration is in
[`PROTOCOL.md`](PROTOCOL.md), written before any reply was read. F043.

## The result in one sentence

**E022's 38.5% `served` figure is the ordinary base rate of a Hacker News
conversation and is not elevated by the need at all: 15/38 = 0.395 for comments
stating an unmet need against 14/38 = 0.368 for ordinary comments in the *same
threads*, whose Wilson intervals overlap almost entirely. The label rubric is
reliable — κ = 0.923 between this reader and E022's on the identical 39 rows — so
the null is about the population, not about the measurement.**

## Why this experiment, and what it does to

`STATE.md`'s next-action item 0 rests on E022's reading that the corpus is "a
population of needs the world **absorbed conversationally** rather than one
awaiting a builder". That reading rests on one number, 15/39 hand-labelled. **No
control was ever run on that cell.** E022's C1 and C2 both measure `answered` —
whether a reply exists — and its own protocol says "`answered` is not `served`".
The conclusion rested on the one cell with no counterfactual.

`served` at 0.385 with no baseline is not a rate. It could be a striking one or
an ordinary one, and nothing in the record could tell.

| | served | rate | CI95 |
|---|---|---|---|
| need arm — comments stating an unmet need, same stories | 15/38 | **0.395** | [0.256, 0.553] |
| **control arm — ordinary comments in those same stories** | 14/38 | **0.368** | [0.234, 0.527] |

Difference **0.026**. Gate B2 declared that overlapping intervals read `not
informative`, and that is the verdict. **H is dead.**

## Gates

| gate | requirement | result | verdict |
|---|---|---|---|
| **B3** label agreement | κ ≥ 0.4, else B2 is a reader disagreement | **κ = 0.9226**, raw agreement 0.9487 on 39 shared rows, 2 disagreements | **pass** |
| **B1** population read | ≥ 95% readable | 76/78 = 0.9744 | **pass** |
| **B2** arms differ | Wilson 95% intervals disjoint | overlap; difference 0.0263 | **not informative** |
| **C3** nonsense control | no reply tree for a fabricated id | Firebase answers **HTTP 200 with the body `null`**, Algolia 404; zero children on both | **pass** |

## The design decision that made this a test rather than a re-read

**The control arm is drawn from ANSWERED comments only.** `served` is conditional
on a reply existing, so sampling ordinary comments regardless of whether they
were answered would have re-measured `answered` — the cell E022 already
controlled and the cell its conclusion does not rest on. Both arms therefore
share the "a reply exists" condition, and the comparison isolates `served` from
`answered`. The eligible pool was **318** answered trigger-free comments in the
need arm's own stories, drawn at E022's seed with E022's rule.

The arms also share **stories**, which controls for the strongest alternative
here: a thread attracts one kind of comment and repels another, and thread
popularity could produce any rate difference at all.

## What this changes, and what it does not

**It changes the mission's evidence, not a decision to build.** The 0.385 figure
was doing a job no measurement supported — it was the number that made "the
world absorbed conversationally" sound like a finding about *needs* rather than
about Hacker News. It is a finding about Hacker News.

**What survives from E022 is untouched and worth stating plainly**, because the
falsification is narrow:

- **58.0% of 1401 stated needs drew a reply.** Not refuted, and this experiment
  says nothing about it.
- **0 of 24 requesters whose need went unserved built it themselves.** The
  sharpest number E022 produced, and untouched.
- The corpus **is** a population of needs the world mostly absorbed in thread.
  That conclusion is now supported by a *baseline* rather than by an
  uninterpretable rate, which is a different kind of support than it had.

**What is withdrawn:** the inference that a reply naming an artifact is evidence
that the **need** was served. On this population that inference does not
separate needs from ordinary conversation at all.

**E022's own gates are untouched.** Gate A2's finding — that the trigger
vocabulary carries no information about *being answered* (lift 0.703) — is the
same result in the neighbouring cell and now has a companion: the trigger
vocabulary carries no information about a reply *serving* the clause either.
Two cells, one reader, and the conclusion is that the **trigger vocabulary is
invisible to conversation outcomes**, not that needs go unserved.

## Instrument facts found on the way

1. **Firebase answers HTTP 200 with the literal body `null`** for an absent
   comment id; Algolia answers 404. The first `--verify` run asserted a 404 and
   failed the control **for the wrong reason** — a control that fails on a
   status code the API never uses would have been rejected while the reader was
   fine. Repaired to assert *no reply tree*, which is what the control is for.
   E022 had already classified this as `null_body`; this session re-derived it.
2. **My own control arm contained zero `partial` labels against the need arm's
   7.** The two arms do not have the same *distribution* of rubric outcomes, so
   the near-identical `served` rates are not an artifact of collapsing `partial`
   differently in each — collapsing would have *raised* the control rate if
   `partial` were common there. Reported because a reader who found 7 partials
   in one arm and 0 in the other is reporting something about the arms.
3. Both readers refused every fabricated id, so no `served` label rests on a
   reader that answers for an absent comment.

## Honest limits

- **One reader, again.** E022 recorded this and so does this. What changed is
  that its magnitude is now measured rather than assumed: two readers of the same
  39 rows agree at κ = 0.923, so the rubric is not the problem.
- **The control arm is lexically defined.** "Matches no trigger phrase" may
  still catch a need phrased unusually, which makes the difference (0.026) a
  **lower bound** on the need effect, not an estimate of it.
- **One community, one day, 38 rows per arm.** A 0.026 difference is well
  inside noise; so is a 0.1 difference at this sample size. The honest reading
  is that this experiment **cannot resolve** a need effect smaller than roughly
  0.2, and reports that limit rather than claiming the effect is zero.
- **`served` was labelled, not measured.** A reply naming an artifact is a
  pointer, not a resolution. Both arms carry that limitation equally, which is
  what makes the comparison fair and what keeps the absolute numbers unusable.

## What this does not open

- **The prior-art screen.** Nothing here reopens a candidate or a death.
- **The 589 unanswered statements.** Untouched; they remain the only
  outcome-marked unserved subpopulation and E022's reason for declining them
  still stands.
- **Product selection.** Item 12 of `STATE-next-actions.md` is not reopened.

Raw capture: `raw/need_arm.jsonl`, `raw/control_arm.jsonl`, `raw/labels.tsv`
(one note per row), `raw/nonsense_control.json`, `results.json`. Re-runnable;
the only external dependency is the public Algolia and Firebase APIs.