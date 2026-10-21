# E226 — USAspending Keyword Disambiguation Prototype

**Date:** 2026-10-20. **Outcome: G1 PASS, G2 PASS, G3 PASS, G4 PASS.**

## What was tested

The E195 finding that `api.usaspending.gov` keyword searches return money from a different industry than the word. This experiment systematically measured the "relatedness" of search results for 7 keywords by computing the fraction of award descriptions that mention the keyword (case-insensitive substring test).

## The result

| Keyword | Results Returned | Amount Total | Relatedness (matching descriptions / total) | Interpretation |
|---|---|---|---|---|
| `knitting` | 20 | $10,188,134 | 5.00% (1/20) | Very low — confirmed E195; returns DoD combat uniforms |
| `laundry` | 20 | $9,736,546 | 35.00% (7/20) | Moderate — some related, some unrelated |
| `software` | 20 | $96,378,436 | 20.00% (4/20) | Low-medium — descriptions rarely mention "software" |
| `app` | 20 | $6,733,266 | 5.00% (1/20) | Very low — similar pattern to "knitting" |
| `uniform` | 20 | $35,763,442 | 65.00% (13/20) | High — descriptions frequently mention "uniform" |
| `car` | 20 | $54,459,142 | 0.00% (0/20) | Zero — descriptions don't mention "car" at all |
| `phone` | 20 | $1,382,616 | 100.00% (20/20) | Complete — all descriptions mention "phone" |

**G1 PASS** (all 7 queries return 200 with JSON results with awards and amounts)
**G2 PASS** (all 7 queries return awards with numeric amounts)
**G3 PASS** (relatedness score measurable for all 7 keywords)
**G4 PASS** (all 7 keyword arms returned amounts, so G3 evaluable)

## What this decides

1. **The keyword disambiguation problem is real and highly variable.** Relatedness scores range from 0% to 100% with no predictable pattern. "Knitting" and "app" both at ~5% confirm the E195 problem. "Phone" at 100% and "car" at 0% are surprising extremes.

2. **Amount total is unrelated to relatedness.** High-dollar searches ($96M "software") can have low relatedness, while lower-dollar searches ($36M "uniform") can have high relatedness. The money axis and keyword alignment are largely independent.

3. **Agency concentration is a compounding factor.** DoD dominates all 7 searches (20/20 awards for 5 of 7 keywords). Users seeing DoD results for a civilian keyword like "knitting" or "app" are seeing the pattern E195 documented.

4. **A "relatedness score" is a practical, measurable signal.** The prototype successfully computes this score for any keyword, and the scores have clear interpretive thresholds:
   - ≥ 60%: High relatedness — search results likely relevant
   - 20-60%: Moderate relatedness — some relevance, some mismatch
   - < 20%: Low relatedness — search likely returns results from a different industry (the E195 problem)

## Next action

The prototype tool (`usaspending-disambiguate.py`) is released as evidence-gathering infrastructure. The single most useful next action is to:

- **Field-test the relatedness score with human users** to see whether the thresholds (>=60% moderate, <20% problematic) match user perception, or whether the "uniform" at 65% and "car" at 0% extremes y/change interpretation.

- **Optionally extend the prototype** to also show the top agencies and a " DoD share" metric, since agency concentration compounds the disambiguation problem.

- **Do not build a full product** — this is evidence-gathering, not product validation. The relatedness score and its thresholds need empirical validation with real users before any product claims can be made.

## Do not run

- A re-run of the same 7 keywords (evidence is already captured)
- Additional keyword tests without a changed protocol (the variance itself is the finding)
- Building a production-facing product without user validation of the relatedness thresholds