<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E175 AMENDMENT 1 — the draw is 200 rows, because 40 cannot carry the bar

**Date:** 2026-10-17. **Before any arm was run and before any rate was
computed.** The only thing measured before this amendment is the **tracker-link
density** of the first draw, and it is reported here because it is a result:
`sample.py` with `DRAW = 40` named a GitHub repository in an answer for
**6 of 40 rows = 0.15**.

Two consequences, both stated rather than absorbed:

1. **The addressable population is small.** A high-arrival Stack Overflow pool
   records its fix as a GitHub link in an answer in about one row in seven. Every
   rate in E170, E174 and E175 is conditioned on that link existing, and this is
   the first direct measurement of the conditioning. It is a **ceiling on any
   product in this line**, stated before the mechanism is measured, so it cannot
   be mistaken for a property of the mechanism.
2. **40 rows cannot carry G2.** With a gold in ~15% of rows, 40 rows yield ~6
   golds; a 0.30 reach bar on 6 observations has a Wilson lower bound near 0.12
   whatever the true rate is. The draw goes to **200 rows**, which yields ~30
   golds and a lower bound that can clear or fail 0.30 informatively.

## Changes

| item | declared | amended |
|---|---|---|
| `DRAW` | 40 | **200** |
| seed | 17520261017 | **unchanged** — the 40 rows already drawn are a prefix of the 200, so the amendment cannot have discarded an inconvenient row |
| Stack Exchange request shape | one batched call | chunked at 100 question ids and 25 question ids per answers call, so `pagesize=100` still returns several answers per question. Total ~12 requests against a 300/day quota |
| registry lookups per row | unbounded by the candidate list | **capped at 8** per row, in the declared candidate order, so one long post cannot spend the run's request budget. Candidates beyond the cap are counted and reported |

Nothing else changes: the arms, the query forms, the gold rule, the gates and
the kill condition are as declared in [`PROTOCOL.md`](PROTOCOL.md).