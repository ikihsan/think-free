<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# Findings — failures and negative results, part 39

Split out of [`FAILURES-findings-38.md`](FAILURES-findings-38.md). The split is
by invariant: **F116 is about an instrument's sampling design producing its own
result**, which is the same family as F115's denominator defect and D088's
"enumerate the reachable set" — a measurement whose design decides its verdict
before any row is read. Nothing was shortened to make room.

Finding **F116**.

## F116 — the view-count effect is a harvest artifact: matched arms give δ=+0.075, p=0.183 against E107's 0.826 (E110)

**Status: closed negative for the claim tested, on the platform tested.**
Session `2026-10-12-001`. Evidence:
`EXPERIMENTS/110-viewcount-matched-harvest/` — `PROTOCOL.md` (gates declared
before the first fetch), `AMENDMENT-1.md`, `AMENDMENT-2.md`, `AMENDMENT-3.md`,
`raw_pool.json`, `results.json`, `stratified.json`.

### The claim being withdrawn

The record carries ~15 experiments reporting where the view-count principle
"generalizes", on results as strong as E107's `Cliff's δ = 0.826` and a
"need median 8.6× random". E110 re-tested E107's own platform with a matched
harvest and the effect does not survive.

### Two defects, either sufficient on its own

**1. Asymmetric harvest — the published number is a tautology.** E107 drew its
need arm from `topic:web-framework` and its random arm from `topic:utils`, both
sorted by stars. From `raw_data.json`, before any classifier runs: **80/80** need
rows carry `web-framework`; **80/80** random rows carry `utils`. The comparison
is the most-starred web frameworks against the most-starred utility libraries.
Nothing about need-relatedness is being measured.

**2. Unanchored substring matching.** E107's classifier fires `ai` inside
`email`, `ml` inside `html`, `cli` inside `client`, `base` inside `database`,
`learning` inside `machine learning`. On E110's 700-row pool the rule sends
**504 of 700 rows (72%)** to `unlabelled`.

### What survives, precisely

| quantity | value |
|---|---|
| E107 published δ, **recomputed exactly** | **+0.826010** |
| E110, pooled over star strata | +0.2048, p = 0.0146 |
| **E110, within-stratum** | **+0.0746** |
| **E110, stratified permutation** | **p = 0.1835** (20 000 iters) |

The arithmetic is not in question: E110's `cliffs_delta` reproduces E107's
published δ to 6 decimal places from E107's own committed data. The pooled
effect is carried by need-labelled rows **sitting in higher star strata**, not
by need labels winning at equal fame — 5 of 7 strata are negative or zero.

### The coverage result, which matters more than the effect size

The vocabulary labels **196 of 700 rows = 28.0%**; **458** of the unlabelled
match neither list. E107 reported 100% coverage implicitly, by reporting only
the rows it labelled. **No effect size computed on the surviving 28% transfers
to the population.** This is the larger obstacle to the line.

### Consequences for the record

- **E107's `ALL GATES PASS` is withdrawn.** `STATE.md` and
  `STATE-next-actions.md` also reported E107 incompatibly (FAIL vs PASS) for
  one experiment id; the passing half is the one that fails here.
- **The other sweeps are not independent confirmations.** E090, E095, E102,
  E103 and E108 copy this classifier and sort their "random" arm by the
  outcome metric. Their verdicts are `untested` on a matched harvest, not
  confirmed.
- **D083's sweep is stopped.** The next action it named — "fresh observation in
  a new domain" — would have inherited both defects. E109 (Pub.dev) is
  superseded, not run.

### What this does NOT close

- **Not** a claim that need-related repositories get no arrivals. Only that
  *this screen* cannot show it, on this platform, with this classifier.
- **Not** PyPI, Hex.pm, NuGet or the rest, on their own populations.
- **Not** the view-count idea as a measurement. A classifier that covers its
  population, on a matched harvest, is a buildable thing and may well find an
  effect. What is withdrawn is the *published evidence* for one.

### The weakest link, named

G0 fired twice. AMENDMENT-3 records a **one-word deletion to a probe after
seeing it fail**. It changes no need term, threshold or statistic, and the whole
comparison is re-run under E107's unanchored rule as a sensitivity arm — but it
is an edit made with knowledge of the outcome, and a reader who discounts it
should discount the G0 pass. The stratified refutation does not depend on G0:
it is a within-stratum comparison on rows the labeler accepted under both rules.