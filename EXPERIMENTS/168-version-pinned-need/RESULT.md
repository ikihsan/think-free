<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E168 RESULT — the version-pinned class is 28% of a high-arrival pool, and the
# strongest alternative serves it materially worse

**Date:** 2026-10-16. **Gates: G1 PASS, G2 PASS, G3 NOT RUN.**

## What prompted it

E126 graded 40 blind attempts on Stack Overflow and read 13 unserved. The
record wrote "Stack Overflow is served at 0.6750" and never said what those
13 had in common. Reading the 13 reasons on 2026-10-16, the shape is uniform:
the attempt named the fault *category* and got the **version-pinned fact**
wrong — "I do not know the exact new package", "the plugin does not read
.copilot-instructions.md" (it does, from build 722431), "no public API to
revert" (there is, in Info.plist). Every one of the eight software-venue
failures in E126's 13 is a fact about *what is true in some version of a
component*, not a fact the assistant could not reason to.

This is the first **positive** structural reading this mission has produced
in seven service closures: every previous venue closed with "the strongest
alternative serves it", which is a statement about the world, not about why.

## G1 — sizing: the class is large, not a residue

299 non-dropped rows of E126's high-arrival pool, classified on title + tags
only (a deliberate choice: the candidate is a tool, so the label is the label
a tool could produce).

| | |
|---|---|
| `version_pinned = 1` | **85 of 299 = 0.2843** |
| Wilson 95% | **[0.2361, 0.3379]** |
| sub-label `docs` (published in the component's version history) | 74 |
| sub-label `local` (the asker's own resolved dependency state) | 11 |
| **G1 gate** (≥ 5.0% and Wilson lower bound > 2.0%) | **PASS** |

For scale: E126 measured the program-shaped residue at 6/299 = 2.0% and wrote
that it was "not a candidate population on its own". This class is **14× that
share** and its Wilson lower bound (0.2361) clears the 2% bar by more than an
order of magnitude. On E126's own arrival rule this is a population of
thousands of high-arrival rows, not a tail.

**Cross-check against an independent prior classification.** E126 already
labelled the same pool `answerable` / `specific` from the full post. That is a
different instrument on the same rows, so it is a real check:

| | count |
|---|---|
| E126 `specific` | 88 |
| E168 `version_pinned` | 85 |
| intersection | 53 |
| Jaccard | **0.4417** |

The two screens agree on the large middle and disagree at both edges:
**32 rows E126 called `answerable` are version-pinned here** (the exact class
E126's own 0.675 baseline was measured on), and **35 rows E126 called
`specific` are not**. Both are unserved-about rows, and they are not the same
rows. That disagreement is the finding, not a nuisance: "needs the asker's
versions or environment" and "the truth differs by version" are two different
reasons an answer cannot come from general knowledge.

## G2 — the strongest alternative serves this class worse

24 rows: the highest-`view_count` `version_pinned` rows not among E126's own
graded 40. One unaided attempt each, written before any thread, answer or
comment was read (`attempts_written_before_fetch.json` records that the
attempt modules' mtimes predate the fetch). Graded against the threads with
E126's rubric, one reader, each grade carrying a reason.

| | |
|---|---|
| unaided served | **11 of 24 = 0.4583** |
| Wilson 95% | [0.2789, 0.6493] |
| E126 baseline, same pool, same instrument | 27 of 40 = **0.6750** [0.5202, 0.7992] |
| difference | **−0.2167** |
| Fisher two-sided p | **0.1168** |
| **G2 gate** (≤ 0.50 and gap ≥ 0.20) | **PASS on both clauses** |

**The margin is thin and the p is not significant.** 0.4583 clears 0.50 by
0.042; the 0.20 gap is cleared by 0.017; Fisher p = 0.1168 does not exclude
chance at this n. The gate is met as declared, and the honest reading is that
the direction and rough size match the prediction while this run alone cannot
establish them. Four rows (36, 60, 66, 69) were near misses; the served share
moves between 0.3750 and 0.5417 depending on how those four are read, which is
the same caution with numbers.

**Why not re-measure the baseline in this run.** E126's 40 graded rows include
20 that are in this pool. Re-reading them would mean reading threads after
writing this run's attempts, which destroys this run's blinding. The
comparison is therefore across-run, on a different day, with a different
sample of the same pool. That is a real limitation of the number and it is
why the gate's second clause was declared as a gap rather than a test.

## Classifier self-falsification

Declared: a re-read of sampled `vp = 1` rows must reproduce the label on
≥ 18 of 20. Run instead over the 13 rows the headline depends on — the
unserved ones, whose bodies are now readable. **13 of 13 hold** under C1 and
C2: in each, the varying fact is a component's behaviour in a named release
or the asker's resolved graph, and in each it is knowable outside the post.

Two defects were found and repaired in this session's own instruments rather
than in the numbers:

1. **The exclusion check silently intersected zero rows.** E126 wrote
   `question_id` as strings in `grading-results.jsonl` and as ints in
   `screening.jsonl`. The set comparison reported "none of the graded rows are
   in the pool", which would have dropped this protocol's blinding for all 20
   overlapping rows. Found by checking the arithmetic rather than the code.
2. **The first thread fetch returned no answers at all.** `filter=withbody`
   on `/questions/{ids}` populates the question body, not the answers
   collection, so all 24 threads graded as having no thread. Repaired by
   fetching `/questions/{id}/answers` per question; `answers_empty_first_fetch:
   24` and `threads_with_answers: 24` are both recorded in the fetch output.
   Had this not been caught by the 24-vs-0 arithmetic it would have read as a
   clean, confident finding that these questions are unanswerable.

## G3 — NOT RUN, and it is the gate that decides the product

G3 asks whether an attempt grounded in only the post and the component's
**published version history** recovers rows the unaided attempt fails. It is
not measured here, and it cannot be measured on these 24 rows: this session
has read all 24 threads, so a grounded attempt written now would be
contaminated by the answer. It needs a fresh blinded sample.

G3 is worth its cost because G1 and G2 alone do not license a build. They say
the class is large and that the alternative does worse on it. They do not say
the missing fact is *retrievable*, and a fact that only exists in the asker's
head is not servable by anything. G3 is the only gate here whose failure would
close a product rather than a population.

## What this does not establish

- **Not a candidate.** No artifact is proposed, and prior art is unchecked.
- **Not significance.** Fisher p = 0.1168; the G2 comparison is a point
  estimate across runs.
- **Not a rate for the venue.** 24 rows of one stratum of one pool. The
  classifier's precision over the other 72 `vp = 1` rows is unmeasured.
- **Not a service rate for version-pinned rows generally.** The sample is
  descending `view_count`, so it is the high-arrival end of the class.
- **Nothing about adoption, packaging, or cost.** A tool that retrieves the
  right version history is unbuilt, unpriced, and uncompared with the things
  developers already do: read the changelog, paste the error into a search
  engine, shell out and read the lockfile.

## Next action

Run G3 on a fresh blinded `version_pinned` sample, with the grounded arm
allowed to consult only the component's own release notes, migration guide and
versioned API reference. If G3's ≥ 0.60 fires, the class becomes a build
candidate and the prior-art screen runs against it. If it does not, the class
closes as a population without a mechanism — which is the F-number this
record already has twelve of, and would be the cleanest one yet, because it
would name a population that is genuinely unserved and still not servable.

[`PROTOCOL.md`](PROTOCOL.md) ·
[`grades.py`](grades.py) ·
[`grades-unaided.jsonl`](grades-unaided.jsonl)