<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E195 AMENDMENT 1 — a 422 was my request, and G3 passed on 0 ÷ 0

**Declared:** 2026-10-19, after panel 1 ran and before panel 2 was sent.
**No bar is moved.** G1, G2 and G3 keep their numeric conditions; **G4 is added
and it can only make the result harder to pass.**

## 1. Panel 1 stands as declared

`G1 PASS, G2 FAIL, G3 PASS`. Under the declared protocol, **G2 failing means
every spend row is `not_evaluated` and the axis is declared unreachable**, and
this experiment reports no spend finding. Panel 1's G3 pass is void, and §3 says
why it should never have been possible.

## 2. Two defects, both in the instrument

**D6 — the 422 is about my request, not about the source.**
`api.usaspending.gov` answered `422 Unprocessable Entity` with
`"Missing value: 'filters|award_type_codes' is a required field"`. A 4xx that
names the missing field is the endpoint working correctly and the caller
getting it wrong. The same defect E193 recorded as D2. **The reference endpoint
in the same run returned 52,950 bytes of agency vocabulary**, so reachability
was never in question; only the query was.

**D7 — G3 as written cannot fail, and it fired on two zeros.**
The declared condition was `ratio >= 2.0` **or** one arm non-zero and the other
zero. With `amount_total = 0` on *both* arms the division yields `inf`, `inf >=
2.0` is true, and the gate passed **having observed nothing at all** — because
both requests had failed. This is the same shape as E017's `H2` (0 hits satisfied
"dead at ≤ 2" on an unread population) and as F061's share over a growing
denominator: **a gate whose pass condition is satisfied by an empty
denominator.**

## 3. What panel 2 changes

Only the request: `filters.award_type_codes: ["A", "B", "C", "D"]` is added, and
`keywords_search_logic: "any"` with it. Terms, endpoint, time window, fields and
bar all unchanged. **Both keyword arms are re-queried**, because a repaired arm
compared against an unrepaired one measures the repair, not the world.

**G4 (new, declared before the run):** *both* keyword arms return at least one
row carrying a numeric award amount. **Without G4, G3 is not evaluable at all** —
which is the entire defect this amendment exists to record, so it is written into
the gate rather than left in this file.

## 4. What panel 2 decides

Unchanged from panel 1. **G3 without G4 kills the keyword form of the spend
axis**, not the source: federal spend is also addressable by product and service
code (PSC/NAICS), which is a different vocabulary and a different experiment,
and is stated rather than quietly retried with the same words.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/195-spend-axis-probe/probe.py    # panel 1, unchanged
tools/x -- python3 EXPERIMENTS/195-spend-axis-probe/probe2.py   # panel 2
```