<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — AMENDMENT-3: the instrument is held constant across `n`, and the full-size
## point must reproduce E040's published number

**Written before any subsample was drawn, any cluster was formed, and any count
was computed.** Nothing in `PROTOCOL-scaling.md` is withdrawn; three provisions
are added, and the first of them is a check on the whole measurement.

## 1. The full-size point is a reproduction test

**At `n = 1391` the subsample is the whole arm, so the curve's rightmost point is
E040's measurement, computed again.** E040 published, for arm A at
`tau = 0.15`: **8 clusters** holding ≥3 rows from ≥3 stories by ≥3 authors, and
**0 at every `tau ≥ 0.20`**.

**This run asserts both numbers before it reports anything else.** If the
`n = 1391` point does not reproduce them, the instrument, the clustering or the
row selection has drifted from the code that produced the published figure, every
other point on the curve is measuring the drift rather than the population, and
the run is `not_evaluated`.

This is the F055/F058 shape taken head on: **an instrument's number is checked
against the instrument's own earlier output at a size where the two must agree,
before the new measurement is interpreted.** E040's own arithmetic here is the
reason the bar of 20 is 2.5× a number that was itself produced by this code.

## 2. Vectors and idf are computed once, on the full arm

`PROTOCOL-scaling.md` said the instrument is E040's, re-implemented by importing
its symbols. It did not say **at what population `idf` is estimated**, and the
question matters more than it looks: estimating `idf` separately inside each
subsample makes the instrument itself a function of `n`, so the curve would partly
measure the vectoriser's behaviour rather than the corpus's.

**Decision: vectors are built once on the full arm (all 1391 rows), and every
subsample is scored with those vectors.** Consequences, stated:

- The instrument is now **provably constant across the curve**, which is the only
  way a growth exponent means what S2 says it means.
- The `n = 1391` point is then bit-identical to E040's by construction, which is
  what provision 1 tests.
- A subsample's rows are scored with `idf` from 1391 documents rather than from
  `n`. This is a deviation from what E040 would have done had it subsampled, and
  E040 did not subsample, so **it deviates from no published measurement.**

## 3. Cosine is computed once, and the grid reuses it

This host has **2 CPUs, 952 MiB RAM, Python 3.8.10 and no NumPy**
(`tools/origin doctor` and an import check), and `R = 40` × 9 sizes × 8 taus ×
O(n²) clustering is hours of work — not a measurement, a denial of service.

**Decision: the thresholded edge list is computed once per arm, at the lowest
`tau` on the grid (0.15), and single-link components at every higher `tau` are
formed from that same edge list by union-find.**

This is not an approximation. Single-link at `tau` is exactly the connected
components of the graph whose edges are the pairs at or above `tau`, so if the
edge list holds every pair at or above the grid's minimum, the components at
every grid point are the same objects a fresh O(n²) pass would produce. **The
equivalent dense computation is run once, at `n = 1391`, and the two are asserted
equal** — if they disagree, the optimisation is wrong and the run is
`not_evaluated`.

`R = 40` is **kept as declared**. The optimisation is what makes it affordable,
not a smaller draw count.

## What this amendment does not decide

- It does not make the exponent predictive. A slope fitted over `n ≤ 1391` is
  still a local exponent, and the `n ≈ 3500` figure in any readout remains
  labelled `inferred`, never `observed`.
- It does not weaken S2, S3 or any bar. The assertions in provisions 1 and 3 can
  only stop the run; they cannot move it toward a result.
