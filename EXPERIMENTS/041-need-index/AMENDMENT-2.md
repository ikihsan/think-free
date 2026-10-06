<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — AMENDMENT-2: the metric is also read against the pair's own repository

**Written after the screening pass returned its repositories and before any
similarity between two rows was computed.** The numbers read before this file
existed are the screening pass's counts — which repositories duplicate-close, and
how many issues each holds — all of them properties of what the source can
serve.

## The problem this fixes

**AMENDMENT-1's selection rule trades one bias for another, and the trade has to
be visible in the result.**

The screened set was chosen *for* duplicate-closure rate, which is why it can
supply pairs. The by-name set was chosen for being established, which is why it
holds many issues. Those two facts pull the metric in opposite directions,
because **partner rank is measured against a pool**:

- a pair from a **small screened repository** is scored against the whole corpus,
  which will be large — a hard test; but
- the **within-repository** pool it competes in is small, and a repository with
  40 issues is a different task from one with 5,000.

Reporting one number over both arms would hide that. A top-1 accuracy of 0.6 could
mean "the instrument is right most of the time" over a 12,000-row pool or "the
instrument is right most of the time among 40 issues", and those support very
different conclusions about a needs index over tens of thousands of rows.

## The addition

**Every partner-rank statistic is reported at two pool sizes.**

- **`pool = corpus`** — the whole captured corpus, the headline number. This is
  the gate-bearing statistic, unchanged from `PROTOCOL.md`.
- **`pool = own repository`** — only the other rows of the pair's own repository.
  Reported alongside, and **never a gate.**

The second is reported because it is the *easiest* task the instrument faces in
this design: the target is in the repository, so the pool is small and every
candidate is a genuine issue from the same project. If the instrument loses on
the own-repository pool, it does not detect repeats even where the search space is
narrow and the text is topically homogeneous, and that is a strong statement
about the instrument rather than about the pool size.

**The gap between the two is itself the reported quantity.** `top1_corpus` minus
`top1_own_repo` is a direct measurement of how much of the instrument's accuracy
is bought by a small candidate set, which is the single number a reader needs in
order to judge whether a needs index over a large corpus is viable.

## What this does not change

- The gates, the bars, the grid, the metric, and the frozen-`tau` rule are all as
  declared. `pool = corpus` remains the gate-bearing statistic; adding a second
  pool is a reporting addition and cannot move a gate.
- The `tau` used for the own-repository pool is the **same frozen value**. Fitting
  a second threshold to the second pool would be calibrating on the arm under
  test, which is the thing this protocol exists to prevent.
- Repository identity is a **corpus selection variable**, so it is reported next
  to the statistic, per F055: the per-repository pair count, the per-repository
  `top1`, and the per-repository own-pool size go in the readout whether or not
  they are read as gates.

## What this amendment does not decide

It does not claim the screened repositories are a fair sample of software issues.
They are repositories selected for duplicate closure, which is a moderation
practice, not a random draw, and the by-name arm exists so a reader can see the
same instrument on a selection made for a different reason. **Neither arm is a
population estimate of anything**, and neither is used as one.
