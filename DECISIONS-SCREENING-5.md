<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Decisions — screening candidates and judging experiments, part 5

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

Decisions **D062**. Split from
[`DECISIONS-SCREENING-4.md`](DECISIONS-SCREENING-4.md), which held D059–D061, at
the point where its own invariant — *what a verdict's own evidence must be* —
gained a second family of member: what a **linkage rule** must be able to do
before its output is read as a finding about the world.

## D062 — A linkage rule is part of the instrument and is tested for power before its output is read (2026-10-05)

Observed: F051, from E031's AMENDMENT-3; with F010 and F050.

**Context.** E030 declared a recurrence rule over rare shared tokens and it fired
on ordinary English (F050). E031 was built to replace the *unit* — a
reader-extracted clause rather than a whole comment — so that a clause could be
compared as a clause. That change fixed the coincidence problem: 216 rows, one
reader wording in identical bytes across three arms, and the length-matched
recomputation moves the arm difference from 0.1667 to **0.1698**, the opposite of
F050's sign flip. But swapping the unit silently broke the **linkage rule**
declared alongside it. Requiring two independent authors, on different stories,
departing from different artifacts, to share **≥ 2 rare content tokens** yields
**4 candidate pairs out of 63 clauses, against a chance expectation of 4.9**.
Reader clauses are short — median 11 words against the 90-word comments E030's
rule was tuned for — so almost no pair can clear the bar by chance and none did.

The gate built on it required ≥ 2 adjudicated-same pairs **and** a clear of the
permutation null. At 4 candidates, with the null's 95th percentile at 2, **no
arrangement of the world could have made the gate fire.** It was not refuted; it
was unreachable.

**Decision.** A linkage rule is part of the instrument, not a preprocessing
convenience, and is subject to two checks **before** any adjudication result is
read:

1. **Power.** State the candidate count the rule produces on the observed units,
   and the count chance alone would produce, and confirm the rule can return a
   non-empty result set. A rule whose observed count is at or below its chance
   expectation has measured its own threshold, not the world.
2. **A control the instrument must pass.** The reader's judgement decides
   sameness; lexical overlap only *selects* candidates. The comparison is against
   **reader-adjudicated random pairs** drawn from the same arms through the same
   independence filters, not a permutation of the candidate set.

**Why the permutation is the wrong control here, which F043 already paid for.**
A permutation holds the candidate set fixed and therefore cannot say what the
reader would have answered about pairs nobody selected for overlap. That is
precisely the shape of F043: this record's most influential number, E022's
`38.5% served`, had no control, and its control read 0.368 against the arm's
0.395. A null that cannot move the selection cannot price the selection.

**Relation to what came before.** This completes a triad of distinct ways an
instrument is wrong about the thing it measures: **F010**, a declared gate that
could not fail; **F050**, a statistic that fired on coincidence; and now a
declared linkage rule that cannot fire. The third is the mirror of the first, and
only running the gate before trusting it separates them — AMENDMENT-3 was written
from a pair count, before one pair was adjudicated, which is exactly the window
in which the correction was legitimate.

**Consequence.** E031's recurrence verdict is `does_not_survive` on an
instrument that passed A3 (κ = 0.7189), A4 (0/24), A5 (0.486) and A6 (20/20
positives, 0/10 negatives). E031's H1 also fails its declared margin (0.1667
against 0.20) and, more decisively, **the seek and move strata are identical at
0.347 against 0.347** — so the population has no "unfilled" property to recur
across, and a fourth demand-side generator closes on its premise rather than on
prior art.

**Ceiling.** This governs the *linkage and comparison* half of an instrument. It
does not make a reader better: E031's κ = 0.7189 is two sub-agent contexts of one
model family, evidence the question is answerable from the text and not evidence
that two people would agree. A6's positive pairs share nearly all their content
words with their source, so A6 shows the instrument can return a positive and
rejects matched negatives — it does **not** validate semantic paraphrase
discrimination, and the instrument's ability to tell a genuine recurrence from
lexical resemblance is the question the result raises, not one this decision
settles.