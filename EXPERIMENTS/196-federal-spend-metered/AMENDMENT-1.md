<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E196 AMENDMENT 1 — the 100th-smallest award measures deobligations, not purchases

Declared 2026-10-19, **after panel 1 and before panel 2 runs at all**. Every
gate bar below is unchanged; only the *statistic G4 is written against* is
replaced, and the replacement is strictly more exact than the thing it replaces.

## What panel 1 found

`tools/x -- python3 EXPERIMENTS/196-federal-spend-metered/panel1.py` → exit 3,
captured in `raw/panel1.json`.

| check | result | what it means |
|---|---|---|
| C1 `QQQQ` returns 200 and 0 | **PASS** | a zero on this endpoint is a zero, not a refusal |
| C2 nonsense keyword returns 200 and `[]` | **PASS** | likewise |
| C3 keyword filter is *used* | **FAIL** | the API returned a *"filters not used"* message naming `keywords_search_logic` |
| C4 `sort="Award Amount"` is ascending | **FAIL** | first row **$8,571,555,254.92**, last **$366,531,199.50** — the default order is **descending** |
| C5 `limit` above 100 is refused | **PASS** | 422, so I3 stops at the 100th award |
| C6 the endpoints agree on existence | **PASS** | R425: 42,347 awards, $334,192,539,564.25 |

**C4 is the one that would have produced a confident wrong number.**
`PROTOCOL.md` declared I3 as *"the 100 smallest awards of a code"*; the
parameter that reads like a sort direction is a *descending* sort, so I3 was in
fact returning the 100 **largest** awards of every cell. Every cell would then
have been measured by its biggest purchases — the opposite end of the metered
spectrum from the one G4 asks about — and G3 would have compared families by
their extremes. Nothing downstream would have looked wrong.

**And the declared statistic is wrong even after the sort is fixed.** Probed
with `order="asc"` on the same code: R425's five smallest awards are
**−$11,448.00, $0.00, $0.00, $0.00, $0.00**. A cell's smallest awards are its
**deobligations and unfunded records**, not its small purchases. So
`a_100`, the 100th-smallest award, is a statistic about accounting hygiene.
G4 as written would have measured that.

## The replacement, declared before it is used

**I3 is replaced by the exact low tail.** For each code, walk
`spending_by_award/` with `sort="Award Amount"`, `order="asc"`, `page=1..k`,
`limit=100`, stopping when an amount exceeds the cutoff. Because the ordering is
ascending, that walk enumerates **every award of the code at or below the
cutoff** — it is not a sample and not an estimate, and the number of awards
found and the exact sum of their amounts are both recorded.

- **Cutoff: $100,000**, unchanged from `PROTOCOL.md`, and for the same declared
  reason.
- **Zero and negative awards are tallied separately and their sum is reported
  next to the positive total.** A negative total would be a net deobligation,
  not a market, and folding it into a small-purchase total would let a cell
  shrink itself below the bar.

**G4 is restated against the exact sum**, at the same $1,000,000,000 bar:

> At least one code has **≥ $1,000,000,000** in the exact sum of its awards
> `≤ $100,000`.

This is *stronger* than the condition it replaces. `PROTOCOL.md` inferred that
sum from `N × a_100`, which assumed every award in the code is at least as large
as its 100th smallest — an assumption that C4's `−$11,448` falsifies outright.

**C4 is restated, not deleted.** It now asserts ascending order **under
`order="asc"`**, the parameter the replacement uses. Its original form was
correct and its failure was informative; it is kept because a silent return to
the default order would again invert the measurement.

**G3's statistic is restated** as the median award amount of the I4 stratum —
unchanged in form — with a declared reporting obligation added: the number of
codes whose I4 stratum median is **≤ 0** is printed, because such a code has no
purchases to meter and would otherwise contribute a zero to a family median.

## The second defect, which is smaller and is my own request

C3 failed because `spending_by_award/` does not accept
`keywords_search_logic` — a field E195 used successfully against
`spending_by_category/`. The API named the ignored filter and returned a
confident, well-formed answer about a **different population than I asked
about**. It is removed from the control request.

This is the third time in this record that a USAspending response has named the
caller's error (E193 D2, E195 D6, here), and the first time the misreading would
have been silent rather than loud. **The `not used` check is therefore in
`client.py` and applies to every panel-2 request**, not only to the control.

## What is not changed

Population (head-100 PSC base codes, FY2020–FY2025, award type A–D, awards
level), every threshold ($100,000, $1B, α = 0.01, 2× base rate), G1, G5, and the
six declared limits.