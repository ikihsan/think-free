# E030 — Amendment 1

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, before `harvest.py` was run and before any account was read.**
Amendments are numbered and dated because a protocol edited after the data exists
cannot be told from one edited before it.

## What is fixed, and why it had to be

The protocol says "one pass per framing phrase" without saying how many pages a
pass is. Two facts, both known before the fetch:

1. **The Algolia `search` endpoint will not page past 1000 hits** for one query.
   `nbPages` saturates at 10 pages of 100. Six of the seven framings have far more
   than 1000 post-2024 comments, so a pass is a **truncation**, not a census.
2. Truncation in `search` order is by **relevance**, so the 1000 are the rows the
   index scored highest for that phrase. That is a different sample from a random
   one and it is not corrected for anywhere.

**Amendment.** Each framing is fetched for **5 pages of 100** (500 attempts,
3 500 in total). `raw/fetch_log.jsonl` records `nbHits`, `nbPages`, `page`, `status`
and `exhaustiveNbHits` per request so the truncation is readable from the record
rather than from this file.

**Why 5 pages.** Gate A4 needs ≥ 300 treatment accounts, and each framing's pages
are filtered by three mechanical conditions (framing present, artifact resolvable,
≥ 40 words). Five pages leaves a wide margin over A4 without paging to the API
ceiling, and a fixed count cannot be accused of having been chosen to reach a
threshold: the pass is the same length for every framing regardless of its volume.

**Consequence for the claim.** The treatment arm is **not a random sample of
departure accounts** and this experiment does not estimate how many departure
accounts exist. It estimates whether clauses recur *within* a relevance-ranked
draw, which is the question H1 asks. Recurrence inside a truncated sample is if
anything *under*-stated relative to the full population, because the highest-ranked
rows for one phrase are the ones that mention that phrase most; the direction of
that bias is not established and is not claimed.
