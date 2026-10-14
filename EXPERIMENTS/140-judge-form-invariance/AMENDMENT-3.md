<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E140 — AMENDMENT 3

Written 2026-10-14, still **before any instrument has been run on any arm**, and
before any judge has seen an item. No M1 verdict, no M2 verdict, no grade and no
P2 rewrite exists. Three corrections, all of them counts.

## 1. G0's denominator is 7, and the item is not added to reach 8

AMENDMENT-2 §4 excluded the un-corrupted `C` rows from the judge arm and set
G0's denominator to "the corrupted `C` items", at the unchanged declared rate of
≥ 0.667. Its arithmetic said that number is 8. It is **7**.

The rule that counts them is `len(valueset.numeric_multiset(answer)) == 0`, and
it fires on **four** of the fifteen answers, not three:

| document | no extractable value | in judge subset |
|---|---|---|
| 2026-20748 | yes | yes |
| 2026-20834 | yes | yes |
| 2026-20860 | yes | no |
| 2026-20861 | yes | yes |

So three of the four fall in the judge subset and the judge arm carries **10 V,
10 P, 7 C = 27 items**. The declared *rate* is kept and the denominator follows
it: **≥ 5 of 7 = 0.714 clears 0.667.** The smallest non-zero rate distinguishable
from zero at n = 7 is 0.10 and 0 of 7 has a Wilson 95% upper bound of 0.412.

**Why the eighth item is not added.** Taking a second corrupted `C` item from
outside the seeded judge subset would restore the number AMENDMENT-2 wrote
before it had run the subset rule. That is denominator-shopping in a
pre-measurement costume: the choice of which extra item, and the fact that an
extra item was wanted at all, would both be made after seeing a shortfall and
before seeing any outcome. A weaker gate is preferable to a gate tuned to hit a
previously stated count.

## 2. The judge arm carries P2 as well, so the batches are rebuilt over 31 items

AMENDMENT-2 §5 states that the judge "sees the P2 text blind", so P2 is part of
the judge's population and the batch set is rebuilt over the **whole** judge
population with the same `JUDGE_SEED = 20261015` and the same
five-per-generation batching. The 27-item `judge_batches.json` is therefore
**superseded**, not used. No grade has been written, so nothing is invalidated
by replacing it; the superseded file stays in git at the pre-measurement commit
so the change is auditable.

The final size is **31 items in seven batches** — 10 `V`, 10 `P`, 7 `C`, 4 `P2`
— not the 28 or 32 guessed here first, because §4's K4 drop and §1's corrected
denominator both reduce it.

## 3. The value denominators are 241 and 40, not ~374 and ~120

The protocol estimated M2's unit at n ≈ 374 and P2's at n ≈ 120. Both were
inherited from E114's counts of *values asked about*, not measured on this
corpus, and both are wrong for the gates that use them.

Measured by `len(valueset.numeric_multiset(answer))` over all 15 verbatim
answers: **241**. Over the four admitted P2 items: **40** (13 + 12 + 8 + 7).

K1 and K2 are therefore gates on 241 and 241 values, not on ~374. This is stated
because a gate is only interpretable against the denominator it was declared on,
and because the declared denominator was not a measurement.

## 4. `finalize_p2.py` applied K4 to P2 as an ordered list, and the writer was told to reorder

Written before any measurement, in the run that admitted the first P2 rewrite:
`finalize_p2.py` compared `valueset.canonical(rewrite) == valueset.canonical(V)`,
which is order-sensitive, while the declared rule (PROTOCOL.md §Arm-construction
gate, K4) is a **multiset** comparison and AMENDMENT-2 §5 explicitly tells the
writer it may reorder. The two disagree, and the difference fell on document
2026-20834, whose rewrite reports the same dates in the same content with a
different sentence order.

**Repair:** compared as `Counter`s, matching the rule as declared. Re-run.

**What the repair exposes, which is a result about the writer and not about any
instrument:** on document **2026-20748** the rewrite dropped the citation
paragraph reference `(h)(88)` while rewriting "which is the paragraph being
revised" as "the paragraph under revision". K4 caught it as one missing value
(`('num', 88.0)`) and the item is dropped and counted, exactly as the protocol
requires. **4 of the 5 P2 rewrites were valid; 1 was not.** The admitted P2
items carry **40 numeric values** (7 + 8 + 12 + 13); the writer emitted 53
across all five, the missing 13 being the dropped item's own value set.

The protocol's own rule did its job here for the second time in this
experiment, which is worth stating plainly rather than filing under defects:
an arm-validity gate that is checked before anything is measured is what keeps
a drifting rewrite from being scored as an instrument's error.

