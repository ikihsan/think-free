<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E196 PROTOCOL — is federal contract spend metered?

Declared 2026-10-19, **before any run of this experiment's panels** and after
E195's `RESULT.md`. All three endpoints named here were reachable from this host
in throwaway reconnaissance on 2026-10-19 (USAspending `spending_by_category/psc/`,
`spending_by_award_count/`, `spending_by_award/`), which established *shape* and
nothing else; no gate below is a result of that reconnaissance, and no number in
it is reused.

> **Read [`AMENDMENT-1.md`](AMENDMENT-1.md) first.** Panel 1 falsified two
> instruments declared below — the sort direction of I3, and the statistic G4 was
> written against — and both were repaired before panel 2 ran. The text below is
> preserved unaltered as declared; where the amendment supersedes it, the
> amendment's version is the one that ran. No threshold was moved.

## The question, and why this question

D122 routed the money axis through **spend** because price is unreachable from
this host (E193: Etsy, eBay and Reddit `403`; DuckDuckGo `202`; Census
key-gated). E195 proved the endpoint answers and, more usefully, that **a
keyword's money belongs to a different industry than the word** — `knitting`
returned $3.58M of combat uniforms — so the keyword form of a spend screen
measures procurement vocabulary. It named the next action: address the same
money by **product and service code**.

A code-addressed rollup is not yet a screen. It ranks cells by how much money
passed through them, which is a fact about procurement, not about what a program
could do. **The shape of the money is the property that screens a candidate**,
and the shape that matters to a program is *metering*: money bought in many
small separate purchases is money a program could sit in front of; money bought
in a few giant multi-year vehicles is not.

So E196 asks one question, on data taken entirely from outside this session
(D121):

> **Addressed by code rather than keyword, does US federal contract spend
> contain cells where the money is bought in many small separate purchases —
> metered at a scale a small program operates at?**

## Population, declared

**The top 100 PSC base codes by total obligation, FY2020–FY2025**, award type
codes `A B C D`, one page of `spending_by_category/psc/` at
`spending_level: awards`, sorted by the endpoint's own descending amount.

The head is declared rather than the whole vocabulary because crawling every
page exceeded a 120 s command budget during reconnaissance. **Codes outside the
head are not measured**, and that is a ceiling on this experiment, stated here
and not revised after the run.

## Instruments

All five are public USAspending endpoints. None of them was written, chosen or
parameterised by hand inside this session beyond the fields listed here.

| id | quantity | endpoint and parameters |
|---|---|---|
| I1 | total obligation per code | `POST /api/v2/search/spending_by_category/psc/`, `limit=100`, `page=1`, `spending_level=awards` |
| I2 | exact award count per code | `POST /api/v2/search/spending_by_award_count/`, `filters.psc_codes=[code]` |
| I3 | the **100 smallest** awards of a code | `POST /api/v2/search/spending_by_award/`, `sort="Award Amount"`, `page=1`, `limit=100` |
| I4 | the **100 awards straddling the median** | same, `page=ceil(N/200)` |
| I5 | award descriptions | carried on I3 and I4 |

`limit` above 100 is refused (`422`), which is why I3 is an exact 100th-order
statistic and not a 1000th. **I3 and I4 are exact order statistics and exact
counts, not samples**, so no cell's headline number is an estimate.

## Gates, declared before the run

- **G1 — source shape.** Every one of the 100 codes returns an amount from I1, a
  non-negative integer from I2, and at least one row from I3. Anything less and
  the panel reports the shortfall rather than a total.
- **G2 — zero control.** Two declared negative controls run **first**: the
  non-existent code `QQQQ`, and a nonsense keyword. Each must return a
  well-formed `200` carrying an empty or zero result — **not** an error, and
  **not** the API's *"the following filters were not used"* message. Without
  this gate every zero below is indistinguishable from a malformed request, which
  is the third time in this record (E017 `H2`, F061, E195 D7) that a gate would
  have been satisfied by an empty denominator.
- **G3 — discrimination.** Kruskal–Wallis across toptier PSC families on the
  I4 median award amount, α = 0.01. **No directional prediction is declared**:
  the ordering between goods and services is not something this record holds
  evidence about, and a wrong directional prediction would produce a false kill
  that looked like a confirmation. A non-directional test can only *close* the
  axis, never open it. If p ≥ 0.01 the families are not distinguishable, the
  metered/lumpy distinction has no purchase in this data, and the axis closes.
- **G4 — addressability, the decision gate.** At least one code must satisfy
  **both** (a) its 100th-smallest award ≤ **$100,000**, and (b)
  `N_awards × a_100 ≥ $1,000,000,000`. Condition (b) follows exactly from (a)
  and the exact count — no estimation anywhere. **Declared arithmetic behind the
  bar:** a program capturing 0.1% of that $1B is $1M/year of value, which is
  more than a free or cheap open-source project needs to be worth building. If no
  code clears both, the federal-contract form of the money axis closes as
  declared.
- **G5 — description audit and positive control (E195's rule).** Every code
  reported carries its top description terms beside its total. And for two
  families chosen **before** the run from outside this data — `Y1*`/`3*`
  construction and `S2*` housekeeping — the I3 descriptions must contain a token
  from that family's own declared keyword set at a rate **≥ 2× the head-100 base
  rate** for the same token. A family whose descriptions are about something else
  is reported as a classifier failure, not as a market. Declared keyword sets:
  construction `{construct, repair, renovat, rehabilitat, remodel, construct}`,
  housekeeping `{housekeep, janitor, custodial, cleaning, guard}`.

## Kill conditions, in one place

G2 failing closes the axis as instrument-limited. G3 failing closes it as
non-discriminating. G4 failing closes it as unaddressable at program scale. G5
failing closes it as procurement vocabulary. Any one of the four closes the
federal-contract money axis as a candidate screen.

## Limits, declared before the run and not revised after it

1. **US federal only.** A real budget with real money; not a sample of what any
   industry pays, and not a sample of private spend, which is the larger pool.
2. **Head-100 only.** The tail of the code vocabulary is unmeasured.
3. **Aggregation level is a declared choice, and it is not a small one.**
   `spending_level=awards` counts full option periods; `transactions` counts
   obligation actions. On R425 reconnaissance returned **$334.19B** against
   **$178.86B** for the same code and window — a factor of 1.87. Every total in
   this experiment is on the `awards` level and both levels are reported for any
   code where the difference is read.
4. **Award size is not a price per unit.** Nothing here recovers a per-hour or
   per-unit rate. A cell metered in *awards* is not thereby metered in *hours*.
   This is the ceiling that keeps G4's result from being read as a valuation.
5. **Descriptions are unfiltered free text.** G5 reports token frequencies and
   makes no claim about meaning; E181's lesson — one reader disagreeing with
   itself on 4 of 10 — applies to anything built on top of them.
6. **One window**, FY2020–FY2025, on one host.

## What this is not

It is not a product, a prototype, or a candidate screen result. It is one
measurement on one axis that D122 opened and E195 half-answered. If G4 fires,
the finding is *"this much money is metered this finely in this cell"* — which
is a precondition for the next experiment, never a candidate in itself.