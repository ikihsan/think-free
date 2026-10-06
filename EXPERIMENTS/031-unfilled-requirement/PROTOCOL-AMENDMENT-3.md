# E031 — Amendment 3

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the candidate pairs were generated and before any
reader adjudicated any pair.** This withdraws the linkage rule declared in
`PROTOCOL.md` §"Recurrence" and replaces the C1 gate. The reason is a measured
power defect in the instrument, established without looking at a single
adjudication — the point at which changing a threshold is legitimate rather than
a rationalisation.

## What was measured

The declared linkage rule required two candidate accounts to share **≥ 2 rare
content tokens** after normalisation, with different authors, different
departing artifacts and different stories. Across the **63 reader-extracted
clauses** in the three arms:

Candidate pairs are drawn **pooled across the three arms** (a pair may join a
seek clause to a move clause), which is what `build_pairs.py` does. Counts on
that basis:

| shared content tokens | independent candidate pairs, pooled | within one arm only |
|---|---|---|
| ≥ 1 | **100** | 53 |
| **≥ 2 (as declared)** | **4** | 2 |
| ≥ 3 | 0 | 0 |

*Corrected 2026-10-05, before any pair was adjudicated.* The first draft of this
table carried the within-arm column as if it were the pooled one (53 and 2),
taken from a scratch count that compared clauses inside each arm separately.
`build_pairs.py` pools, and the first draft's figures would have understated the
candidate set by more than half. The argument below is unchanged and, if
anything, slightly stronger: at the declared threshold the pooled candidate set
holds **4 pairs out of a chance expectation of 4.9**.

Over the 1 953 unordered clause pairs, drawing pairs at random, the share of
pairs reaching each threshold is:

| threshold | P(at random) | expected pairs of 1953 |
|---|---|---|
| ≥ 1 | 0.0527 | 102.9 |
| ≥ 2 | 0.0025 | **4.9** |

The observed count at the declared threshold is **4**, at or below the 4.9 that
chance alone delivers — so even before a reader speaks, the declared linkage rule
has produced nothing above coincidence. The declared C1 gate additionally
required the observed count to exceed the permutation null's 95th percentile
(`raw/results.json`, `gate_C1_null`: observed 2 within-arm pairs, null mean
0.64, **null p95 = 2**, `clears_null: false`).

## Why this is a defect in the instrument and not a finding

C1 as declared required **≥ 2 adjudicated-same independent pairs** *and* a clear
of the null. With 4 candidate pairs in existence, sitting inside the chance
range, **no arrangement of the world could have made the gate fire**: the
candidate set is a near-empty sample of the pairs that matter, so the gate is
unreachable rather than refuted. This is the mirror image of F010 (a declared
gate that could not fail) and of F050 (a statistic that fired on coincidence),
and it is the third distinct way a recurrence instrument can be wrong about
recurrence.

The cause is arithmetic, not the corpus. Reader clauses are **short** — median 11
words, range 5 to 26 — so two independent clauses almost never share two rare
content words. A linkage rule tuned for 90-word comments (F050's setting) does
not transfer to a clause-sized unit. **The unit change that fixed E030's
coincidence problem introduced this power problem**, and neither could have been
seen without counting pairs at both thresholds before adjudicating any of them.

## What replaces it

**The reader's judgement decides sameness; lexical overlap only selects
candidates.** That is the division the whole design pointed at and the declared
rule got backwards.

| | declared in `PROTOCOL.md` | as amended here |
|---|---|---|
| candidate selection | ≥ 2 shared content tokens | **≥ 1** shared content token, plus the same author/artifact/story independence filters |
| decision | the overlap count | **the reader's answer to q4**, on printed clauses only |
| null | permutation of clause→account assignment | **a reader-adjudicated random-pair control**, same arms, same independence filters, no token selection |
| gate | clear the null **and** ≥ 2 same pairs | **P_same(candidates) − P_same(control) ≥ 0.20 with CI95 excluding 0**, **and** ≥ 2 adjudicated-same independent candidate pairs, **and** A3 and A5 passed |

**Why a reader-adjudicated random-pair control rather than a permutation.**
F043 measured, at ten times the scale, that this record's single most
influential number had **no control** and that its control read 0.368 against the
arm's 0.395 — the "served" figure was the base rate of ordinary conversation. A
permutation null cannot answer the question that matters here, because it holds
the candidate set fixed and therefore cannot say what the reader would have said
about pairs nobody selected for overlap. The control arm is the same reader, the
same q4 wording, the same printed-clause format, and **the same number of pairs**,
drawn from the same three arms and passing the same independence filters. If the
candidate pairs say `same` more often than random pairs do, overlap carries
information about shared requirements; if it does not, the ruler is the ordinary
base rate of two technical sentences resembling each other.

The candidate and control pair ids are drawn by two fixed seeds and **no pair
appears in both sets**.

## Sensitivity, declared before adjudication

The reader adjudicates all 100 candidate pairs and all 100 control pairs. **The
threshold sweep is reported whatever it shows**, including the declared ≥ 2 rows,
so the number of pairs the amendment recovered is visible rather than asserted.
`raw/results.json` carries `pair_threshold_sensitivity` and
`fold_rescued_rows` alongside every gate.

## Unchanged

H1's arms, sample sizes, the q1 wording, κ's 0.6 floor, the 0.20 margins, A4's
0.25 ceiling, A5's separation, the clause verbatim check, and the nonsense
control are all as declared. This amendment changes **which pairs a reader is
asked about and what the comparison is against**. It moves no rate that has been
computed and no threshold that was declared for a reader's judgement.