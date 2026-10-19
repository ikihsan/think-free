<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E196 RESULT — federal contract spend is metered, and the IT cells are the densest; but "ten thousand awards" is not "ten thousand purchases"

**Date:** 2026-10-19. **Outcome: G2 PASS, G3 fires (p = 0.00416), G4 fires
(25 of 100 codes), G1 FAIL and G5 not evaluated**, both for reasons this file
names. The federal-contract money axis stays open; it now has a money-sized,
code-addressed list of cells, and a measured reason why the next instrument
cannot be a count of awards.

Protocol [`PROTOCOL.md`](PROTOCOL.md), amendments
[`AMENDMENT-1.md`](AMENDMENT-1.md) (sort direction and the G4 statistic),
[`AMENDMENT-2.md`](AMENDMENT-2.md) (the walk's cap and G5's source),
[`AMENDMENT-3.md`](AMENDMENT-3.md) (the cap censored the decisive end; G4
restated on order statistics). Panels `panel1.py`, `panel2.py`; statistics
`stats.py` + `analysis.py`; instrument measurement `pagecap.py`;
recomputation from committed bytes `recompute.py`.

## 1. The gate vector, exactly

| gate | declared question | result |
|---|---|---|
| **G1** source shape | every code returns an amount, an integer count, ≥ 1 award row | **FAIL** — 9 of 100 have no median stratum, all `422`; cause measured, §4 |
| **G2** zero control | a non-existent code and a nonsense keyword both return a well-formed empty `200`, with no ignored-filter message | **PASS** — 7 of 7 panel-1 checks green |
| **G3** discrimination | families differ in median award amount, α = 0.01, no direction declared | **FIRES** — H = 40.63, **p = 0.00416**, 21 families, 91 codes |
| **G4** addressability | ≥ 10,000 awards ≤ $100,000 inside a cell of ≥ $1B | **FIRES** — **25 of 100** codes, of which **16 have a 10,000th award at or above $100** |
| **G5** description control | the family's own vocabulary appears at ≥ 2× the head-100 base rate | **NOT EVALUATED** — `Y1` and `S2` pass decisively, the `3` arm had **no members**; §5 |

`raw/panel2.json` holds the vector; `recompute.py` rebuilds every one of these
fields from the committed response bytes and **agrees with the live run on all
four comparisons** (`raw/recompute.json`), which is the F049/D061 tieback: a
judgement over fetched data that cannot be tied to the bytes it was read from
is not a measurement.

**A readability defect of my own, reported rather than renamed:** `panel2.json`
carries both `"fire"` and `"pass"` per gate, and for a discrimination gate they
mean opposite things — G3 shows `"fire": true, "pass": false` because `fire` is
"families are distinguishable, the axis survives" and `pass` is `not (p < α)`.
Read the gate names, not the boolean names.

## 2. The finding: the IT and software cells are bought in tens of thousands of small purchases

Head-100 PSC base codes by total obligation, FY2020–FY2025, `spending_level:
awards`: **$5.65T across 100 codes.** 16 of them hold **at least 10,000 separate
awards of $100,000 or less**, in a cell carrying **at least $1B**, and their
10,000th-smallest award ranges from **$204.84** (`8905`) to **$86,286** (`U099`). The densest
cluster is IT and software, and it is the one part of this distribution a small
open-source program could compete in:

| code | what the code is | cell total | awards | 10,000th smallest |
|---|---|---:|---:|---:|
| `R425` | Support-Professional: Engineering/Technical | $334.19B | 42,347 | $79,430 |
| `DA01` | IT & Telecom — app development support (**labour**) | $94.91B | 27,425 | **$27,519** |
| `2840` | Gas turbines and jet engines | $76.40B | 15,756 | $73,712 |
| `1680` | Misc. aircraft accessories and components | $59.59B | 71,312 | $807 |
| `S206` | Housekeeping — guard | $47.30B | 21,452 | $11,445 |
| `S216` | Housekeeping — facilities operations support | $34.80B | 15,920 | $45,080 |
| `DA10` | IT & Telecom — app development, **SaaS** | $33.01B | 26,656 | **$30,903** |
| `4220` | Marine lifesaving and diving equipment | $32.45B | 89,901 | $247 |
| `Q999` | Medical — other | $31.10B | 19,441 | $60,838 |
| `7A21` | IT & Telecom — business application software, **perpetual licence** | $29.21B | 50,777 | **$14,313** |
| `2320` | Trucks and truck tractors, wheeled | $27.61B | 23,594 | $10,603 |
| `7030` | **Information technology software** | $25.83B | 24,492 | **$40,320** |
| `D304` | IT & Telecom — telecommunications and transmission | $20.37B | 29,072 | **$11,544** |
| `8905` | Meat, poultry and fish | $17.86B | 440,857 | $204 |
| `Z2AA` | Repair or alteration of office buildings | $16.23B | 23,147 | $57,487 |
| `U099` | Education/training — other | $15.55B | 14,321 | $86,286 |

**Five IT/software codes — `DA01`, `DA10`, `7A21`, `7030`, `D304` — carry
$203.32B between them, and each of them buys the same thing tens of thousands
of times in the $11k–$40k band.** That is metering at the scale a small program
operates at, in cells a program could plausibly be bought from, and it is the
first money-sized, addressable population this record has produced. Nothing
here says which of those five, or any of them, is an opportunity.

## 3. The finding that constrains the next experiment: a federal "award" is often not a purchase

**9 of the 25 codes clearing G4 clear it only because their 10,000th-smallest
award carries no money:** `R499` $9.98, `6505` $0.01, `R706` $9.75, `9130`
$53.40, `6515` $0.00, `1560` $0.00, `5342` $36.30, `8915` $23.10, `6640` $6.94.

And the ceiling of that is worse than the nine. `spending_by_award` answers
`200` for page 500 and `422` for page 501 — **the 50,000th award is the deepest
any code can reach** (`raw/pagecap.json`, bisection). At that depth:

| code | cell total | awards | the 50,000th award |
|---|---:|---:|---:|
| `R499` Support-Professional: Other | $270.27B | 302,317 | **$51.93 – $52.04** |
| `R706` Support-Management: Logistics | $146.26B | 238,191 | $43.56 – $43.71 |
| `8915` Fruits and vegetables | $18.66B | 4,807,422 | $57.21 – $57.28 |
| `8905` Meat, poultry and fish | $17.86B | 440,857 | $853.49 – $854.91 |
| `6640` Laboratory equipment and supplies | $15.49B | 1,450,656 | $23.10 – $23.14 |

**Half a million federal awards worth about fifty dollars each, inside a
$270B cell.** `R499` is the fifth-largest code in US federal contracting by
money and it holds at least 50,000 records whose total obligation is under a
dollar.

**So the honest reading of G4 is: 16 codes, not 25, and the difference is the
whole finding.** The 16 are reported as clearing, not as "real money" — the
floor of that split is $204.84, which is a judgement about records and not
about purchases, and it is the same judgement applied to all 100 codes rather
than a threshold invented after seeing which side a code landed on. Award count is not a proxy for purchasable units in this data
because a large share of award records carry no money, and no endpoint here
distinguishes "an award for $52" from "a record that was never funded". G4 as
restated in AMENDMENT-3 guarantees *ten thousand awards below $100,000*; it
cannot guarantee *ten thousand purchases*. That gap is the next experiment, and
it is instrument-limited rather than answer-limited.

## 4. G1's failure, measured rather than described

Nine codes — `R499`, `6505`, `R706`, `9130`, `6515`, `1560`, `8915`, `8905`,
`6640` — are exactly the nine with **more than 100,000 awards**. G1 requires a
median stratum from every code; for these, the median page is 1,512 and above,
and the endpoint refuses past page 500. Every one of them is `422`, every count
and every rank checkpoint up to 10,000 returned `200`, and no ignored-filter
message appeared on any of the 100 count requests or on the head request.

**G1 FAIL is an instrument ceiling on one instrument (I4), not a defect in the
source**, and it costs exactly what it says: those nine codes contribute no
median to G3, which is why G3 runs on 91 codes, and their rank-100,000 and
rank-1,000,000 checkpoints are null **by construction** rather than by absence.

## 5. G5: two arms pass, one had no population, and the gate is not evaluated

`Y1` (construction) — **`construct` at 1.000 of its codes against a 0.090 base
rate, ratio 11.1; `remodel` ratio 20.0.** `S2` (housekeeping) — **`cleaning`
ratio 5.88, `custodial` ratio 50.0, `guard` ratio 2.38.** The mechanism G5 was
written to detect — a code-addressed read that is really procurement vocabulary,
E195's `TurboScan` defect — **is not supported**: the descriptions a code's
awards carry are about what the code says they are.

The `3` arm **has no members**: no `3`-prefixed code reached the head-100, so
its arm rate is 0 over an empty set and no keyword can clear a 2× base rate.
The gate as declared does not pass, and this file does not report it as
passing. It is **not evaluated**, and the reason is structural: `PROTOCOL.md`
declared thresholds and a `not evaluable` rule for G3 and G4 and **none for
G5**, which is the *third* time in this record (E017 `H2`, E195 D7, here) that a
threshold was written without a third answer for **"the population was not
measured"**. The rule now earned: **a positive-control arm declared over a code
prefix needs an emptiness clause, declared before the run, that sends the gate to
`not evaluated` rather than to a zero.**

## 6. Five instrument defects, one of them would have inverted the result

1. **`sort: "Award Amount"` is descending.** `PROTOCOL.md` declared I3 as "the
   100 smallest awards"; the parameter that reads like a sort direction returns
   the 100 **largest**. Panel 1's C4 caught it before any gate ran. Every cell
   would have been measured by its biggest purchases — the opposite end of the
   spectrum from the one G4 asks about — and nothing downstream would have
   looked wrong. (AMENDMENT-1)
2. **A cell's smallest awards are its deobligations.** R425's five smallest are
   −$11,448.00, $0, $0, $0, $0. The declared statistic `a_100` was a measure of
   accounting hygiene. (AMENDMENT-1, C7)
3. **The walk's cost is paid in awards, and those awards carry no money.** A
   6-page cap censored **58 of 100** codes, including **all ten of the largest**,
   and it is *anti-correlated* with what G4 asks about. The declared rule (a
   censored code cannot satisfy G4) was correct and the result was unusable.
   (AMENDMENT-2, repaired by AMENDMENT-3.)
4. **A self-test against an exact permutation test caught a wrong
   Kruskal–Wallis.** The statistic is `(Σ ranks)² / nᵢ` summed over groups; the
   first version computed `Σ rank² / nᵢ`, produced **H = −51.93**, and would have
   reported p = 1.0 from a negative H — the axis closed as non-discriminating,
   with every other control green. `stats.py` now checks its own arithmetic
   against a full enumeration of the same permutation space (92,378 and 34,650
   permutations) and never against a remembered constant, because the first
   version compared against textbook figures from memory and **one of them was
   misremembered**. (E177's sixth defect, recurring as a design rule.)
5. **The recomputation disagreed with the run and the run was right.** The first
   `recompute.py` read "crossing the $100,000 cutoff" as censoring; the panel
   reads it as the walk succeeding. Four `G4` fields disagreed. The
   recomputation was fixed, which is the correct direction: it is the copy that
   is derived from bytes, and a derived copy that contradicts the primary
   measurement is the thing under suspicion.

Plus two defects of my own code, neither of which lost a capture:
`fetch_code` never carried `total_awards_level` onto the record, so every family
total and family label came from an absent field and the progress line printed
`$0` for a code the endpoint reports at $32.4B; and `analysis.py` used `median`
without importing it, so a run finished its 1,300 captures and then raised.

## 7. What this decides

**The federal-contract money axis is open and it has produced its first
addressable, money-sized list.** D122 routed the axis through spend because
price is unreachable; E195 showed the endpoint answers and that keywords buy the
wrong industry; **E196 shows the code-addressed shape of that money, and that
five IT/software cells alone account for $203B bought in tens of thousands of
separate sub-$40k purchases.**

**What is now closed:** the question G4 asked. **What is not closed, and is the
next experiment:** whether those tens of thousands of records are purchases.

**Named next action, and why it is the next one rather than a refinement.**
Every count in this file is an award count, and §3 shows award count and
purchase count are different quantities here by a factor nobody has measured.
The instrument for the difference exists and costs about ten requests per code:
**bisect the ascending order for the rank at which award amounts turn positive,
per code.** That returns, exactly and for all 100 codes, the number of awards
that carry money — the number the mission actually needs, because it is the
count of things a program could displace. It also settles whether the $203B in
§2 is tens of thousands of real purchases or tens of thousands of records.

The second thing that measurement makes possible, and which this file will not
pretend to have earned: **the recipient of that money** is reachable — verified
reachable from this host, with `spending_by_category/recipient/` accepting the
same `psc_codes` filter — so once the purchase count is exact, "who is paid for
ten thousand $27,519 software-development tasks" is a question with a public
answer.

**Do not run:** the keyword form of this axis (closed by E195, G3 fired against
it); a longer tail walk (superseded by AMENDMENT-3's order statistics); any
`rank_p × 100` checkpoint (the endpoint refuses past page 500); or a re-run of
panel 2 on the same parameters (`client.call` reuses any capture whose stored
request key matches, so it is free and would return the same bytes).