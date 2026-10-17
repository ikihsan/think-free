<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E174 PROTOCOL — every arm of E170, recomputed from its own raw responses

**Date opened:** 2026-10-17. **Status:** pre-declared, before the recomputation
was written. No network access; every input is a file committed by E170.

## The observation that prompted this

`EXPERIMENTS/170-fix-reachability-rank/raw/summary.json` reports **seven** arms.
`EXPERIMENTS/170-fix-reachability-rank/RESULT.md` reports **two** — the two
global ones, `A0_quoted_global` (1/13) and `A1_global` (2/13 = 0.1538) — and
builds its conclusion, F132, the `HYPOTHESES.md` status row and the `STATE.md`
entry on those two. The five unreported arms include the two **repo-scoped**
variants of the same queries, at **5/13 = 0.3846** each with Wilson lower bound
0.1771, which is above E170's own declared **0.30 bar for building anything**.

E169 named the incumbent for this class as *"search the project's issue tracker
with the exact error string"* and withdrew it on a control failure. A repo-scoped
search is that mechanism. So the closure may have been decided on the arms that
excluded the incumbent.

## Question

1. **Q1 (reproduction).** Do E170's seven arms recompute to the same numbers from
   the committed raw responses, when the ranks are re-derived from the returned
   URL lists rather than read from any stored rank?
2. **Q2 (the comparison the write-up omits).** Scoped versus global, paired on the
   same 13 rows: what is the difference in reach, and is it distinguishable from
   zero at this N?
3. **Q3 (the build decision).** Does the repo-scoped arm clear E170's declared
   0.30 bar, and does its Wilson lower bound?

## What this is not

This is a **recomputation of committed data**, not a new measurement. It can
establish that a published conclusion does not follow from its own evidence. It
cannot establish that scoped retrieval works on a population this record has not
touched — the 13 rows are all tracker-linked by construction, so every rate here
is conditioned on "a tracker link exists in the thread". That is the next
experiment, declared there.

## Gates

| gate | condition | meaning |
|---|---|---|
| **G1** | every recomputed arm equals the stored arm for hits/of/rate | the recomputation reproduces the record |
| **G2** | every replayed query string equals the query string in the raw log | the row-to-record alignment is proven, not assumed |
| **G3** | paired McNemar exact p and Wilson interval reported for scoped vs global | the comparison is stated with its uncertainty |

A gate that fails is reported as a defect in E170's harness, not repaired
silently.

## Kill

There is no candidate here, so there is no kill gate. The decision this feeds is
stated up front: **if G1–G3 hold and the scoped arms clear 0.30, the
version-pinned line's closure is reopened for a fresh-sample measurement, and the
documents that state the closure are corrected in the same commit.**