# E058 — The remaining Stack Exchange survivors: does a recurring unserved
# step appear there?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

## What this is

E057 enumerated 365 sites, kept ~50 after its published exclusion list, and
ran its protocol on the **12 alphabetically first** survivors. It answered
for that slice: G1 fired on three independent sites, G2 failed on every one,
G3 failed on the third. The same rules were never run on the remaining
survivors. E058 runs the identical protocol on that remainder: it is a
continuation of the same instrument and population, not a new screen.

## Difference from E057, and only difference

Population = the survivors **after** the 12 E057 picked
(`kept[12:]` in `fetch.py`). Same stratum, same arms, same gates, same
instrument, same reading order: G1 clusters are read for G2 first, G3 never
reached for a cluster G2 kills.

## Gates (identical to E057, declared here before the fetch)

| gate | condition |
|---|---|
| **G1 population** | a cluster of the same step across ≥8 distinct users in one site, or ≥5 distinct users across ≥2 sites |
| **G2 serving** | an enumeration built from the population's own vocabulary names 0 incumbents that perform the step |
| **G3 verdict** | the step's correctness is decidable from artifacts, and no incumbent's primary output reveals it (D081) |

**Decision rule: build nothing unless G1, G2 and G3 all hold for the same
cluster.** `KILL` if G1 fails for every cluster, or if G2 fails for every
cluster that passes G1.

## Ceilings

Same as E057's: self-selected English questioners, a question is a
formulable need, title-level clustering reads framing not practice, nothing
is contacted or published. E057's three-site G1 hits make a `G1` pass here
cheap to expect; as in E057, the discriminating gates are G2 and G3.

## Reproduction

```
python3 EXPERIMENTS/058-se-remaining-sites/fetch.py
python3 EXPERIMENTS/058-se-remaining-sites/cluster.py
```
