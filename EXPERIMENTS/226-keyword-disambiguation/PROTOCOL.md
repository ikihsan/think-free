# E226 — USAspending Keyword Disambiguation Prototype

**Protocol for the keyword disambiguation prototype.**

## Purpose

Given a plain-language keyword, query `api.usaspending.gov` and return not just the total obligated amount but also the industry distribution and award descriptions, so users can assess whether the keyword search is returning relevant results.

The practical difficulty (E195): when users search USAspending.gov by keyword (e.g. "knitting"), they get results from a different industry than expected (e.g. $3.5M all in combat uniforms). This misleads procurement researchers, small businesses, analysts, and policymakers.

## Method

1. Query `https://api.usaspending.gov/api/v2/search/spending_by_award/` with:
   - `filters.time_period`: ["2020-01-01", "2023-12-31"]
   - `filters.keywords`: [keyword]
   - `filters.award_type_codes`: ["A", "B", "C", "D"]
   - `fields`: ["Award ID", "Award Amount", "Description", "Awarding Agency"]
   - `page`: 1, `limit`: 20, `subawards`: False
2. From the response, extract:
   - Number of results returned
   - Number of awards with numeric amounts
   - Total obligated amount
   - Agency distribution (count per awarding agency)
   - Award descriptions
3. Compute a "relatedness score": fraction of descriptions that mention the keyword (case-insensitive substring match)
4. Return sample descriptions and agency distribution

## Kill Gates (pre-declared, from PROTOCOL.md)

- **G1**: control integrity — the API must return 200 with a JSON body containing results
- **G2**: spend axis usable — each keyword query must return awards with numeric amounts (not just 422/error)
- **G3**: keyword discriminates — the relatedness score must be measurable (not refusals or errors)
- **G4**: both arms return amounts — when testing multiple keywords, both must return data for G3 to be evaluable

## Data analysis

For each keyword, the relatedness score reveals how well the search results align with the keyword's common meaning:

| Keyword | Relatedness | Description |
|---|---|---|
| `knitting` | 5.00% (1/20) | Very low — confirmed E195 finding; returns DoD combat uniforms |
| `laundry` | 35.00% (7/20) | Moderate — some related, some unrelated |
| `software` | 20.00% (4/20) | Low-medium — descriptions rarely mention "software" |
| `app` | 5.00% (1/20) | Very low — similar pattern to "knitting" |
| `uniform` | 65.00% (13/20) | High — descriptions frequently mention "uniform" |
| `car` | 0.00% (0/20) | Zero — descriptions don't mention "car" at all |
| `phone` | 100.00% (20/20) | Complete — all descriptions mention "phone" |

## What this establishes

1. **The keyword disambiguation problem is real and variable.** Relatedness scores range from 0% to 100%, with no predictable pattern based on the keyword's common meaning. "Knitting" and "app" both return ~5% relatedness, confirming the E195 problem. "Phone" returns 100% — unexpectedly high. "Car" returns 0% — descriptions don't mention "car" at all.

2. **Total obligated amount does not predict relatedness.** "Software" returns $96.4M with 20% relatedness, while "uniform" returns $35.8M with 65% relatedness. The money axis and the keyword alignment are largely independent dimensions.

3. **Agency concentration is high.** Across all 7 keywords tested, the Department of Defense was the top or only agency — 20 of 20 awards for 5 of the 7 keywords. This means the disambiguation problem is compounded by the fact that most federal spending in these searches goes to DoD.

## What remains unknown

- How relatedness scales with different keyword selections (beyond these 7 test cases)
- Whether users can reliably interpret the relatedness score without guidance
- Whether the relatedness score, combined with agency information, is sufficient for users to assess result relevance
- How the relatedness score correlates with the actual content of award descriptions (beyond simple keyword substring matching)
- Whether other USAspending endpoints (spending_by_category, spending_by_award_count) show similar patterns

## Artifacts

- `usaspending-disambiguate.py` — the prototype CLI tool
- `EXPERIMENTS/226-keyword-disambiguation/` — experiment directory (to be created)
- Raw probe outputs in `/tmp/` (knitting.txt, laundry.txt, software.txt, app.txt, uniform.txt, car.txt, phone.txt)