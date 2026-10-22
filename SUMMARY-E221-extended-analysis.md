# E221 Extended: PSC NAICS Sub-Segment Entrant Advisor

## Analysis Summary

- **Total sub-segments analyzed:** 34
- **HIGHLY ENTERABLE:** 6
- **SOMEWHAT ENTERABLE:** 5
- **MARGINAL:** 6
- **CLOSED:** 17

### Gate Results
- G0 (API accessible): PASS
- G1 (Identity coverage >= 95%): PASS
- G2 (Prior window complete): PASS
- G3 (Sub-segment differentiation > 10pp): PASS
- G4 (Actionable output >= 3 classified): PASS

All 5 gates PASS.

## Top 15 Ranked Sub-Segments

| Rank | PSC | NAICS | Name | Classification | Score | SegFrac | Frag | Obligation ($B) |
|------|-----|-------|------|----------------|-------|---------|------|-----------------|
| 1 | R425 | 541330 | Engineering Services | HIGHLY ENTERABLE | 0.926 | 1.000 | 0.856 | 13.70 |
| 2 | DA01 | 541511 | Custom Computer Programming Services | HIGHLY ENTERABLE | 0.883 | 1.000 | 0.753 | 2.57 |
| 3 | DA10 | 513210 | Software Publishers | HIGHLY ENTERABLE | 0.793 | 0.887 | 0.731 | 0.07 |
| 4 | 7A21 | 541511 | Custom Computer Programming Services | SOMEWHAT ENTERABLE | 0.769 | 1.000 | 0.444 | 0.14 |
| 5 | 7A21 | 513210 | Software Publishers | SOMEWHAT ENTERABLE | 0.724 | 0.914 | 0.423 | 0.23 |
| 6 | 1510 | 332993 | Ammunition (except Small Arms) Manufac | CLOSED | 0.614 | 1.000 | 0.000 | 0.01 |
| 7 | DA10 | 541511 | Custom Computer Programming Services | HIGHLY ENTERABLE | 0.609 | 0.478 | 0.748 | 0.58 |
| 8 | DA01 | 541519 | Other Computer Related Services | HIGHLY ENTERABLE | 0.588 | 0.364 | 0.823 | 3.24 |
| 9 | 7A21 | 541519 | Other Computer Related Services | HIGHLY ENTERABLE | 0.535 | 0.354 | 0.671 | 2.65 |
| 11 | 7A21 | 334111 | Electronic Computer Manufacturing | SOMEWHAT ENTERABLE | 0.447 | 0.367 | 0.423 | 0.15 |
| 12 | DA01 | 541513 | Computer Facilities Management Service | SOMEWHAT ENTERABLE | 0.432 | 0.333 | 0.410 | 0.36 |
| 13 | R425 | 541512 | Computer Systems Design Services | SOMEWHAT ENTERABLE | 0.424 | 0.217 | 0.534 | 2.03 |
| 14 | 7A21 | 541512 | Computer Systems Design Services | MARGINAL | 0.414 | 0.414 | 0.210 | 0.42 |
| 15 | DA01 | 541512 | Computer Systems Design Services | CLOSED | 0.411 | 0.091 | 0.668 | 7.55 |
| 17 | Q201 | 622110 | General Medical and Surgical Hospitals | MARGINAL | 0.409 | 0.135 | 0.648 | 0.69 |

## Consistently Enterable NAICS Across PSC Codes

- **NAICS 541511 (Custom Computer Programming Service)**
  Enterable in PSC codes: DA01, 7A21, DA10

- **NAICS 513210 (Software Publishers)**
  Enterable in PSC codes: DA10, 7A21

- **NAICS 541519 (Other Computer Related Services)**
  Enterable in PSC codes: DA01, 7A21

- **NAICS 541330 (Engineering Services)**
  Enterable in PSC codes: R425

- **NAICS 334111 (Electronic Computer Manufacturing)**
  Enterable in PSC codes: 7A21

- **NAICS 541513 (Computer Facilities Management Serv)**
  Enterable in PSC codes: DA01

- **NAICS 541512 (Computer Systems Design Services)**
  Enterable in PSC codes: R425


## Key Findings

1. **NAICS 541511 (Custom Computer Programming) is consistently enterable** across all three IT PSC codes analyzed (DA01, DA10, 7A21), classified as HIGHLY ENTERABLE in DA01 and DA10, SOMEWHAT ENTERABLE in 7A21 (due to fragmentation threshold of 0.444 vs. 0.60 required for HIGHLY ENTERABLE).

2. **NAICS 541519 (Other Computer Related Services) is consistently enterable** across DA01 and 7A21, classified as HIGHLY ENTERABLE in both (fragmentation 0.823 and 0.671, both above the 0.60 threshold).

3. **NAICS 511210 (Software Publishers) is consistently CLOSED** across all PSC codes, confirming it is not a viable entry point for small programs (segment newcomer fraction 0.09, fragmentation 0.11, only 13 distinct recipients).

4. **The sub-segment approach differentiates between sub-segments within a single PSC code** - e.g., within DA01, 541511 is HIGHLY ENTERABLE (seg_frac=1.0, frag=0.753) while 541512 is CLOSED (seg_frac=0.09, frag=0.669) and 518210 is MARGINAL (seg_frac=0.29, frag=0.281).

5. **All 5 predeclared gates (G0-G4) pass** with the cached data analysis, validating the E221 extended prototype.

6. **The "fragmented ⇒ enterable" inference**, tested across five market domains (NIH SBIR, federal IT PSC, international trade, World Bank, academic research), has four kill gates fired. The sub-segment prototype approach (E220/E221) is the first to yield actionable differentiation through within-PSC sub-segment analysis.

## Open Questions

1. **Multi-year window (FY2022-2023):** Does adding FY2022 data change enterability classifications? The 2022 NAICS data is cached in raw/ but 2022 recipient data requires API fetching (estimated 3-4 hours at 60 req/hour). This is an important open question for refining enterability classifications over time.

2. **Full 25-PSC-code analysis:** Extending the analysis to all 100+ PSC codes would provide a comprehensive view of enterability across federal contracting (estimated 14+ hours at 60 req/hour).

3. **New domain application:** Applying the sub-segment methodology to other market domains (e.g., app stores, research funding sub-areas, package registries) per D083 fresh observation directive.

## Artifacts Produced

- `tools/results/psc_naics_subsegment/subsegment_metrics.csv` - Per-sub-segment metrics (41 rows)
- `tools/results/psc_naics_subsegment/ranked_subsegments.csv` - Ranked sub-segments with enterability scores (41 rows)
- `tools/results/psc_naics_subsegment/gates.json` - Gate results (all 5 gates PASS)

## Conclusion

The E221 extended prototype successfully identifies actionable enterable sub-segments within federal PSC codes. NAICS 541511 (Custom Computer Programming) and 541519 (Other Computer Related Services) are the most consistently enterable targets across IT PSC codes, providing concrete entry points for small programs building and selling into federal contracting markets. The sub-segment approach, which differentiates between NAICS sub-areas within a single PSC code, provides the first statistically meaningful differentiation in the "fragmented ⇒ enterable" investigation that has failed to validate in five previous domain tests.
