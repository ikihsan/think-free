<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — the scaling law item 0f assumes

Split out of `PROTOCOL.md` on 2026-10-06 at its line cap, **by invariant**: that
file holds the declaration for instrument validity, this one holds the declaration
for a different claim with its own parameters. Written and fixed before any
subsample was drawn or any cluster count was computed.

## The question

Item 0f — the ranked top of this mission's next actions — proposes building a
needs index over a **second public venue**, on the reasoning that recognition is
**"thin only because 1391 rows is a small population"**, that *"recognition is a
rate over a population"*, and therefore that *whether it scales is arithmetic
before it is anything else.*

**That reasoning has never been checked, and it is the load-bearing assumption of
the top item.** E040 measured one point on the curve — 8 G4-qualifying clusters
at n = 1391, against a bar of 20 — and read the shortfall as a population-size
problem. A corpus of 1391 rows is equally consistent with:

- a curve that is still climbing steeply, so 5× or 10× the rows reaches the bar
  and a second venue is worth building; or
- a curve that **saturates near 10**, because cross-story recurrence in this
  population is bounded, in which case *no second venue reaches 20* and the line
  closes for a reason no amount of harvesting will change.

**These two readings call for opposite actions and the record currently supports
both.** The measurement that separates them costs no new fetch: it re-runs E040's
own arm A at a ladder of corpus sizes and reads the curve.

**This is the higher-information step and it is ordered first**, because building
a second venue's harvest — the expensive part of item 0f — is wasted effort if
the curve is flat. Item 0f stays the top item; this measures the premise under
it before any of its cost is spent.

## Fixed before computation

**Population.** E040's captured arms, read from bytes and nothing else:
`EXPERIMENTS/040-need-clustering/raw/arm_A.jsonl` (1391 need statements) and
`arm_B.jsonl` (1391 matched near-miss controls from the same stories, same length
band, no trigger literal). **Both arms are read.** B is the null, and E040
measured its `partner_rate` at exactly **0.000 of 1391** at every `tau ≥ 0.25`,
so it is a control that is known to be silent and a null that cannot flatter the
answer.

**Instrument.** The one from [`PROTOCOL.md`](PROTOCOL.md) — the same
normalisation, tokenisation, stoplist, TF-IDF over unigrams (1.0) and bigrams
(0.5), cosine — re-implemented by importing E040's own `tally.py` symbols where
they exist, so this arm is not compared against a different instrument than the
one E040 reported with. Sublinear term frequency is **not** used here, because
E040's instrument did not use it and the comparison is against E040's number.

**Grid, fixed:** `n ∈ {100, 175, 275, 400, 550, 750, 1000, 1250, 1391}`.
`R = 40` subsamples per `n` per arm, drawn **without replacement**, sorted by a
fixed hash of the row id with seed `20261006` so the subsample for a given `n` is
the same set on a re-run and nested subsamples are avoided by drawing each
independently from the full row set.

**Clustering.** Single-link agglomerative at each `tau` on E040's grid
`{0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50}`, full pairwise within the
subsample. **No `tau` is frozen**; the curve is reported across the grid, per
D069, because here the calibration population is unavailable (F066) and the arms
under test are the only population there is.

**The counted quantity.** G4's definition, unchanged and not redefined to suit the
curve: a **qualifying cluster** holds **≥ 3 rows from ≥ 3 distinct stories written
by ≥ 3 distinct authors**. The reported curve is
`qualifying_clusters(n)` = mean over the `R` subsamples, with the 5th and 95th
percentiles across subsamples as the interval — an interval over *draws*, not over
rows, and labelled as such.

**The growth exponent.** `alpha` is the slope of
`log(count + 1)` on `log(n)`, fitted by ordinary least squares over the grid
points with `count + 1 > 0`, and its interval by the same deterministic bootstrap
as [`PROTOCOL.md`](PROTOCOL.md) (10,000 resamples, seed `20261006`).

## Gates, declared in advance

- **S1 — the curve is measured at all.** Arm A yields a qualifying-cluster count
  above zero at some `n` and some `tau`. Fail ⇒ nothing to extrapolate and item
  0f's premise is already wrong at one point.
- **S2 — resolution scales.** `alpha ≥ 1.0` with the bootstrap CI's lower bound
  **> 0.75**, on arm A, at **every** `tau` on the grid whose pooled count is
  non-zero. `alpha ≈ 1` means linear: doubling the corpus doubles the clusters and
  the bar of 20 is reached at roughly `n = 1391 × 20/8 ≈ 3500`. `alpha < 0.75`
  means sub-linear: **the bar is not reachable by growing the corpus**, which
  closes the scale premise of item 0f and leaves a needs index unsupportable from
  this population at any size.
- **S3 — the curve is about content, not about crowding.** At every `n`, arm B's
  qualifying-cluster count stays at or below arm A's, and arm B's own `alpha` is
  not larger than arm A's. Fail ⇒ the curve measures how many rows are present,
  not what they are about, and S2 is withdrawn regardless of its own result.

**Interpretation ceiling, stated with the gates.** A fitted `alpha` over `n ≤
1391` is a local exponent. Extrapolating it to `n ≈ 3500` is an **extrapolation**,
recorded as such, and the `n = 3500` figure in any readout is labelled `inferred`,
never `observed`. **A met S2 is not a candidate and not a product.** It means the
premise of item 0f survives contact with its own numbers, which is the most this
measurement can establish.

## What would make this a bad use of the session

If the curve turns out to be flat, this experiment closes item 0f's premise in
about the time one fetch takes, and the mission stops paying for harvests whose
yield is bounded by the population rather than by its size. That is worth an hour.
A second venue's harvest, without this number, is not — because item 0f's own
text says the scale question is *"arithmetic before it is anything else"*, and
this is the arithmetic.

## Reproduction

```
python3 EXPERIMENTS/041-need-index/scaling.py
python3 EXPERIMENTS/041-need-index/verify_manifest.py    # covers both claims
```
