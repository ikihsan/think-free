<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — AMENDMENT-5: E040's README states a G4 number its own artifact contradicts

**Found by AMENDMENT-3's reproduction check, before any curve was computed.** The
check was written against E040's *prose*; it fired; and the cause turned out to be
that the prose and the artifact disagree.

## What the check found

`AMENDMENT-3` provision 1 requires this run to reproduce, at `n = 1391` on arm A:

> **8 clusters** at `tau = 0.15` and **0 at every `tau ≥ 0.20`**

— quoted from E040's `README.md`, *"G4 (the buildable primitive): not met at any
tau ... 8 at the most permissive threshold and 0 at every threshold from 0.20
up"*.

Running **E040's own `vectors()` and `cluster_stats()` on E040's own
`raw/arm_A.jsonl`** gives:

| `tau` | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 | 0.50 |
|---|---|---|---|---|---|---|---|---|
| README prose | 8 | **0** | **0** | 0 | 0 | 0 | 0 | 0 |
| `raw/tally.json` | 8 | **1** | **1** | 0 | 0 | 0 | 0 | 0 |
| **this run, dense** | 8 | **1** | **1** | 0 | 0 | 0 | 0 | 0 |
| **this run, edge list** | 8 | **1** | **1** | 0 | 0 | 0 | 0 | 0 |

**The artifact and the code agree with each other and disagree with the prose.**
`EXPERIMENTS/040-need-clustering/raw/tally.json` records
`clusters_size_ge_3_stories_ge_3_authors_ge_3` as **1** at both `0.2` and `0.25`.
So this is not a drift in the instrument and not a failure of the reproduction: it
is a sentence in E040's README that its own run did not produce.

## What is corrected, and what is not

**Corrected: the reproduction assertion.** It now checks the values in
**`raw/tally.json`**, which is the run's own record, rather than the values in a
prose summary of it. The assertion is unchanged in strength — a mismatch still
stops the run and reports `not_evaluated`.

**Not corrected: any gate, bar or conclusion of E040.** G4's bar is 20, the
maximum qualifying count anywhere on the grid is 8, and **1 at 0.20 and 0.25
instead of 0 changes no verdict**. E040's G4 stands as `not met at any tau`, which
is what its README says it is. **This is a false number in a summary, not a false
conclusion**, and the distinction is the whole reason it is cheap to record and
expensive to ignore: a reader who trusted the sentence would have believed the
resolution was *sharper* than the run found, and would have drawn the same
conclusion for the wrong reason.

## The pattern, because it is the fourth instance

- **F013, F018, F019** — a gate asserting a fact about the record rather than
  about the code, so every interpreter or runner failed while the record stayed
  self-consistent.
- **F021** — a status declared `unmeasured` on a run whose steps never ran.
- **E040 F064** — a positive control whose arms did not contain the pair members.
- **This one** — a summary sentence that is not what the run produced, sitting
  beside an artifact that is.

In each case **the discrepancy was invisible to every gate in the repository**,
because the artifact was correct and the prose was the thing that drifted. A gate
that reads `tally.json` cannot catch a sentence in a README; a gate that reads a
README cannot catch a computation. **The cheapest gate that would have caught it
is the one this run wrote for a different reason**: recompute a published number
from the bytes that produced it, and compare. That check was going to be run
anyway, as a guard on the curve, and it found a stale sentence instead.

**The generalisation worth keeping: a published number should be reproducible from
the artifact it came from, and the reproducibility test should be part of the
experiment that *depends* on the number rather than a separate audit.** It cost
four minutes here and it was already on the critical path.

## What this amendment does not decide

It does not reopen E040. E040's gates, its arms, its instrument and its verdicts
are untouched, and nothing in its cluster file is re-read. The correction is to
**one sentence of prose in one README**, and the record of what that sentence
should have said.
