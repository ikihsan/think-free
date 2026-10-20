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
## ADDENDUM (same day, after landing) — the baseline was weaker than the strongest alternative

A closing check on the 24 threads that cost one regex: **20 of 24 answer
sets link out to an external source**, and the destination is overwhelmingly
an issue tracker — `github.com` in 15 of 24, plus `developer.android.com`,
`tailwindcss.com`, `visualstudio.com`, `rubygems.org`, and in one case a fix
shipped as a shell script on a gist that the top answer tells the reader to
`curl | bash`.

**This is the incumbent mechanism, and it is already served.** For a
version-pinned failure the working resolution is: search the project's issue
tracker with the exact error string, read the linked fix, apply it. Developers
do it by hand today and it takes minutes.

**It also bounds what E168's G2 measured.** The attempt arm is this mission's
standard instrument — written from general knowledge, **with no retrieval**,
the same instrument E091, E092, E126 and E143 used. That keeps the comparison
internally consistent with 0.6750, and it is the correct comparison *within
this record*. It is not a comparison against the strongest accessible
alternative in the sense the brief requires, because an assistant that can
search is a strictly stronger alternative than one that cannot, and the
threads themselves show the answer is sitting in a searchable tracker.

So the correct reading of E168's G2 is narrower than the gate's wording: a
free general assistant **without retrieval** serves this class at 0.4583
against 0.6750 on the pool at large. It does **not** establish that the class
is unserved by a retrieval-enabled assistant, and it should not be quoted as
though it did.

**What this changes about the next action.** G3 as declared — a grounded arm
allowed the post plus the component's published version history — would test
"add version grounding", and grounding is what search already does. G3 is
therefore not sufficient on its own and must gain a third arm: the same
question put to the alternative **with** search over the issue tracker and
release notes. If that arm matches the grounded arm, the class is real,
large, and served, and this closes as the thirteenth service closure with a
sharper reason than the other twelve: the alternative wins once it is allowed
to look things up.

**Cheap decisive alternative, if that arm is judged too expensive to run
honestly:** compare on these same 24 rows how often the top answer's linked
source is reachable by the exact error string as a query. That is measurable
from `threads.json` alone, with no assistant in the loop, and it bounds the
search arm's ceiling before anyone spends an attempt budget on it.

Nothing else in this RESULT changes: G1 is a property of the population and
does not depend on the baseline; the G2 numbers stand as written, with the
scope of the claim narrowed to what the instrument actually was.

## ADDENDUM 2 — how far the missing fact is from the post (13 unserved rows)

Measured offline from `threads.json`, no assistant in the loop. For each of
the 13 rows the unaided arm failed, the **top** answer was checked for three
retrieval handles:

| handle in the top answer | count |
|---|---|
| a URL (issue tracker or vendor doc) | **8 of 13** |
| a literal configuration key or setting name | 5 of 13 |
| a version token | 2 of 13 |

**What it says.** In 8 of 13 the resolution is *a pointer to a document that
exists somewhere other than the post* — the same figure as the 20-of-24
link-out count above, restricted to the rows that matter. In 5 of 13 it is a
literal key a tool could set. Only 2 of 13 name a version, which is the
surprise: **the missing fact is usually not a version number**, it is a
behaviour that changed and where it was written down.

**What it does not say, and why this measurement is not G3.** It counts
handles in an answer a human already found; it does not show that an
alternative could find the same document from the post alone. That is the
search-arm question, and **it could not be run here: web search returned
`Web search cancelled` on every attempt from this VM.** So the third arm's
ceiling is still unmeasured, and the cheapest way to measure it remains the one
named above — take the exact error string from each post, query, and check
whether the linked source surfaces. That needs a host with search, not a
script, and it is the first thing the next session should attempt.

The 5 rows with neither URL nor key nor version — 43, 60, 67 among them — are
the ones where the resolution is an action on the asker's own machine
(Rosetta installed, a manifest tag added, a NuGet package upgraded). Those are
a third mechanism, not a retrieval failure, and a version-grounding tool would
not serve them.
