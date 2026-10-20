<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E195 PROTOCOL — can an organisation's actual spend be read from this host?

**Date declared:** 2026-10-19, before any request was sent.
**Instrument:** `probe.py` (stdlib only). **Raw:** `raw/probe.json`.
**Status:** running.

## Why this probe exists

D122 routes the mission's money axis through **spend** rather than price, because
E193 measured that every price-bearing marketplace is hard-blocked from this
host (Etsy/eBay/Reddit `403`, DuckDuckGo `202`, Census key-gated) while
USAspending and Comtrade both answered `200`. D121 requires the next candidate
to carry one measurement taken from outside the session that invents it.

**This probe does not measure spend.** It establishes whether the spend axis is
*reachable and shaped the way a screen would need* — specifically, whether a
query by a plain-language domain keyword returns **award amounts on the rows**,
which is the property E193's app-store scan lacked and the reason its headline
row turned out to be a PDF scanner.

## What is probed

| # | Source | Role | What it must answer |
|---|---|---|---|
| 1 | Stack Exchange API | control | known-reachable from this record |
| 2 | OpenAlex | control | known-reachable from this record |
| 3 | GitHub REST | control | reachable, but a valid zero-result body is 55 bytes — see E193 D1 |
| 4 | USAspending `references/toptier_agencies` | spend | does the reference vocabulary return at all? |
| 5 | USAspending `search/spending_by_award`, keyword `laundry` | spend | **does a plain-English keyword return rows carrying an award amount?** |
| 6 | USAspending `search/spending_by_award`, keyword `knitting` | spend | same, on a term chosen *before* any result was seen |
| 7 | Comtrade public preview | spend | control for the second spend source D122 names |

**Recording rule, unchanged from E193:** a `2xx` is a capture only if the body
parses as JSON and is non-empty. A body carrying a refusal marker is a
`refusal` whatever its length. Bytes, sha256 and a 200-character excerpt are
recorded for every row.

## Gates — declared before the run

- **G1 control integrity.** 2 of 3 controls capture. **Fails → every spend row is
  `not_evaluated`** and the axis is declared unreachable from this host.
- **G2 the spend axis is usable.** ≥2 of rows 4–7 capture **and** at least one
  award row carries a numeric amount. **Fails → D122's second branch is
  unreachable too, the money axis closes as inaccessible here, and the named
  next action moves to a domain where the price signal is not behind a block.**
- **G3 the keyword is a usable discriminator.** Rows 5 and 6 differ in total
  amount by at least a factor of two, **or** one returns rows and the other
  returns none. **Fails → the endpoint answers but a plain-English keyword does
  not select, so it cannot screen domains by money** and a narrower product-code
  vocabulary would be required. This gate exists because E194's single
  large-demand row was an off-target product that matched one word.

## Kill

**G3 not fired kills the keyword form of this axis**, not the source: US federal
spend is also addressable by product and service code (PSC/NAICS), which is a
different vocabulary and a different experiment. That would be stated, not
quietly retried with the same words.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/195-spend-axis-probe/probe.py
```