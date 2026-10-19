<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E197 AMENDMENT 1 — the geometric scan is replaced by a direct binary search

**When:** 2026-10-19, after a three-code development run and **before**
`panel1.py` was written. **What is declared unchanged:** every gate, every
threshold, the population, the control list and the panel assignment in
`PROTOCOL.md`.

## What was declared

`PROTOCOL.md` §4 and §5 panel A described the search as "one geometric scan of
ascending blocks (ranks 100, 200, 400, … 50,000) then a bounded binary search
inside the bracket each threshold's scan established", and `thresholds.py`
carried `SCAN_RANKS` as the probe list.

## What the development run showed

Three codes were read end to end before the population run: `DA01`, `R499` and
`1510`. The first version produced numbers that were **exactly wrong rather
than noisy**, in three separate ways.

1. **Skipped pages.** The scan returns the first *probe* that reaches the
   threshold, and the pages between two probes are never examined. Summing the
   blocks it happened to read omits those pages. `DA01`'s ascending `t=1` count
   came out **200** this way; the correct value is **281**.
2. **`page_metadata.hasNext` is a constant, not a statement.** It turns
   **False at row 10,000** and stays False. `DA01` has 27,424 awards across 275
   pages and `hasNext` is False from page 100 on. A first version that treated
   `has_next is False` as "the cell ended" stopped every cell at rank 10,000 and
   reported the truncation as a census.
3. **The last page is a short block, not an empty one, and pages past it return
   `200` with zero rows.** For `DA01`, page 275 holds 24 rows and page 276 holds
   zero with status `200`; page 501+ returns `422`. Both mean "past the end" and
   neither is a value.

Defect 2 is the expensive one, because it produces a *complete* table. A record
that stopped every cell at 10,000 rows and published a median would have looked
measured.

## The replacement

A single binary search over `[1, min(500, ceil(N/100))]` per threshold, with the
lower invariant checked on each page rather than assumed. `hasNext` is not read
anywhere. "The cell ended" is `rows < 100`; "past the cell" is `rows == 0` at
status `200` or `422` at any page. The count is `100 × (turn_page − 1)` plus the
rows of the turning block that match, because every page before the turning one
is entirely on one side of the threshold — so no page is read twice and none is
skipped.

**Cost:** at most nine requests per threshold instead of ten scan requests plus
a search, and one shape instead of two.

## The development run is disclosed, not hidden

`DA01`, `R499` and `1510` have final numbers already captured, produced by the
repaired instrument. They are in the population (`DA01` and `R499` are in
E196's 25, `DA01` is in the five IT codes), so their captures are reused rather
than re-fetched. **What this costs:** the instrument was written and repaired
while looking at three cells of the population it will report on, so those three
rows are development rows. Panel B's independent arm was implemented and run on
them in the same breath, and the two arms agree exactly on all three
(`27,143 = 27,143`, `2,200 = 2,200`; `R499` is censored in the descending arm at
the 500-page ceiling, which is reported rather than reconciled). The gate vector
is computed over the whole population regardless of which captures predate this
amendment.

`probe.py`'s capture of a three-code question and this development run are the
only work done before the population run; `raw/t_*` and `raw/probe*` are on disk
with their sha256 and are part of the record.