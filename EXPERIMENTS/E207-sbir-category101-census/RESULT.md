<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E207 result: E204's category-101 finding reproduces exactly; the record was defective, the number is real

**Date:** 2026-10-21. **Session:** 2026-10-21-001.

## What was tested

E204 and E206 (2026-10-20) sit at `STATE.md`'s reload point reporting that NIH
SBIR spending category **101** holds **147 grants across 134 distinct orgs with
top-5 vendor share 11.6%** — "the most fragmented market measured in this
repository." Three facts made that unverifiable from the repo:

1. `EXPERIMENTS/E204-*` and `EXPERIMENTS/E206-*` each hold only a `RESULT.md` —
   **no script, no raw data** (the F142/D121 pattern).
2. The committed prototype (`tools/nih_accessibility_prototype.py`) that encodes
   the derived IC consensus has a `fetch_grants()` with **no `activity_codes`
   filter**: it pulls from all 85,133 FY2023 projects, caps at 2,000 in default
   order, then filters that slice for a category string. It cannot produce a
   368-row population, and a 2,000-row default slice is not a census.
3. The API does report exactly **368** for FY2023 `R41`/`R42`, so a correct
   census is reachable.

E207 ran that census (`census.py`, complete `R41`/`R42` FY2023 fetch stopped by
the API's own `meta.total`, no row cap, no sampling) and recomputed the headline.
Protocol and gates were written before the census ran
([`PROTOCOL.md`](PROTOCOL.md)).

## The result — all five predeclared gates PASS

| Gate | Criterion | Census | Verdict |
|---|---|---|---|
| G1 | population = API total = 368 | 368 fetched / 368 reported | **PASS** |
| G2 | cat-101 grants within 132–162 (E204: 147) | **147** | **PASS** (exact) |
| G3 | distinct orgs within 121–147 (E204: 134) | **134** | **PASS** (exact) |
| G4 | top-5 share within 6.6%–16.6% (E204: 11.6%) | **0.1159** | **PASS** |
| G5 | E204's five categories all present | 101, 108, 176, 525, 701 all top-5 by grants | **PASS** |

The census total for category 101 is **$63,254,235** — matching E204's claimed
figure **to the dollar**. The top-5 organizations by award amount match to the
dollar as well: BIOCHIP LABS $1,779,044, INOVODEL $1,467,953, PASCALL SYSTEMS
$1,456,255, BIOPTICSTECHNOLOGY $1,317,009, LYSSN.IO $1,308,426. The top five
categories by grant count are exactly E204's claimed set.

**One ordering note, reported not buried:** E204's rank table listed 701 (99
grants) above 176 (104 grants) — a rank error in E204's table, since 104 > 99.
The census puts 176 fourth and 701 fifth. The *set* is identical; only the order
within it was misstated.

## What this decides

- **The mechanism/replication question is settled: E204's category-101 numbers
  are real and now source-supported** (they were previously *untested* from the
  repo because no script or raw data existed behind them). The "most fragmented
  market" claim on this population survives its own replication.
- **This does not validate a product.** It says nothing about whether a small
  program should target NIH SBIR, whether anyone wins these grants, adoption, or
  the value of the IC-consensus recommendations. Those were never tested here.
  The accessibility *pattern* is a measured property of this population, not a
  candidate.

## The record defect this exposes, and the smallest repair

E204/E206 were written as claims with no runnable instrument and no raw data —
a reader could not reproduce them, and the only committed code that touches this
domain (`tools/nih_accessibility_prototype.py`) uses a **sampling method that
cannot produce the reported population** (no `activity_codes` filter, 2,000-row
cap). The prototype's IC consensus (NIAID, NCI, NHLB, NIA) is therefore derived
from an unfiltered 2,000-row slice of 85,133, **not** from the 368-grant
population the RESULT.md names — its provenance does not match its stated basis,
even though the headline it quotes is independently correct.

E207 supplies the missing artifact: a committed census script and the full
368-row `raw/census.json`, so the number is now reproducible from the repo. The
prototype's sampling defect is a **separate, un-repaired** instrument problem —
it does not change E204's correctness, but it means the IC-consensus
recommendations rest on a population that was never the one described.

## Raw data and instrument

- [`census.py`](census.py) — the census (stdlib `urllib`, deterministic).
- [`raw/census.json`](raw/census.json) — all 368 rows plus `reported_total`.
- `summary.json` — per-category grants/orgs/top-5-share/total.
- Gates evaluated via a committed-adjacent check; all five PASS.

## Bound

One census, one comparison. No re-run on unchanged parameters. This closes only
the replication question. It does not reopen the closed accessibility-repair or
view-count lines, and it proposes no product.
