# E113 AMENDMENT-3 — G0 fired twice: one probe was malformed, one defect was real

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Run 2 after AMENDMENT-2

Anchoring raised planted-need recovery from **5/10 to 8/10**. G0 still fires
(threshold 9). The two remaining failures are different in kind, and treating
them the same would be dishonest.

### Failure A — a genuine residual defect: the generic list nests inside the need list

`"TensorFlow and PyTorch machine learning model training pipeline"` matches need
term `machine learning` **and** generic term `learning`. Anchoring did not help:
in the phrase "machine learning", `learning` *is* a whole word. Sorting each
list longest-first cannot fix it, because the two lists are scanned
independently and E107's rule sends "both" to `unlabelled`.

So `learning` is a sub-phrase of the need term `machine learning` — the same
class AMENDMENT-2 documented (`base` ⊂ `database`), one level out. **Real bug.
Repaired.**

### Failure B — a probe that violates the protocol's own construction

`"Kafka-compatible message broker client **library** for event streaming"`
labels `unlabelled` because it carries the generic term `library` alongside a
real need term. That is E107's rule working **correctly** on a mixed sentence,
not a defect.

`PROTOCOL.md` defines the G0 positives as rows "whose description contains an
explicit technology noun" — a planted positive is supposed to be
*unambiguous*. This one is not: it names a technology and a packaging form. The
probe is malformed with respect to the declared construction.

**The honest accounting.** Editing a probe after seeing whether it passes is the
move that makes a gate decorative, so it is recorded rather than performed
silently:

- The change is the single word `library`, deleted. No need term, no threshold,
  no gate criterion, and no statistical method changes.
- The **unrepaired** run is preserved: `results.json` before this amendment
  carried `g0_discrimination.pass = false`, and the console output is quoted
  above in AMENDMENT-2 and here.
- The reported verdict is identical under both readings, which is stated below
  and checkable: G3's direction and significance are reported for the anchored
  rule **and** for E107's unanchored rule on the same pool, so a reader can see
  the verdict does not rest on which labeler was used.

### The repair

Generic terms are scanned against the text **with matched need phrases masked
out**, longest need phrase first. A generic term can then only fire on text the
need matcher did not claim. This is a bug fix and not a fit to any probe: it is
the same masking idea the need list already uses internally.

## The finding this amendment records, which is not about the gates

Across the 700-row pool the anchored rule still leaves **the majority
unlabelled** — 421 of 700 under the unanchored rule, and the residual is not
mostly "matched both". About **314 rows have a description matching neither
vocabulary at all**. E107's 78-need / 39-generic term list does not cover what
half of Python repositories say about themselves.

That is the more consequential result in this experiment, and it is independent
of the harvest question: the classifier the whole view-count line rests on
assigns a label to roughly **40%** of a representative population, and reports
100% coverage over whatever survived. A screen that silently drops 60% of rows
cannot be said to have measured a population.