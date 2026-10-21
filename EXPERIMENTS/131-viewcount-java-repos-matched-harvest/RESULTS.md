<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E131 — view-count principle on Java GitHub repos, matched harvest design, base v2 classifier

## Experiment conducted
2026-10-13. Matched harvest design: single query `language:java stars:100..20000`, 7 star strata, 100 per stratum, no topic filter. Java GitHub repositories, base v2 classifier (no Java adaptation).

## Question
With both arms drawn from one identical pool under one identical selection (language: java, stars 100..20000, 7 star strata, no topic filter), does a need-label predict arrival count (stars)?

## Hypothesis
H1 (confound): the gap is produced by language ecosystem differences or repo age.
H0 (principle): a need-related repository accrues more stars than a non-need one drawn from the same pool at the same age, and the effect is not explained by age.

## Design — the matched harvest
| Parameter | Value |
|---|---|
| Platform | GitHub code repositories (Java language) |
| Pool query | `language:java stars:100..20000`, sort=stars&order=desc — one query, no topic filter, no need vocabulary |
| Pool size | 700 rows (100 per stratum × 7 strata) |
| Label source | `labeling_improved.py` — base v2 classifier, masked need/generic rule, word-boundary anchored |
| Label arms | `need` (need-indicator match, no generic term) / `generic` (generic-term match, no need-indicator) / `unlabelled` (both or neither — excluded, and counted) |

Asymmetry is removed by construction: identical query, identical sort, identical star band, identical language filter applied to both arms. Only the label differs.

## Gates (declared before first fetch)
- **G0 — instrument discrimination (must pass first).** The labeler must recover independent real positives: seeded on twenty repos whose description contains an explicit technology noun (`postgres`, `kafka`, `tensorflow`, `sqlite`, `elasticsearch`, …) it must label `need` at ≥9/10 and on twenty rows matching only generic vocabulary (`utils`, `boilerplate`, `example`, `helper`, …) at `generic` ≥9/10. **Kill: G0 below threshold stops the experiment** — a labeler that cannot find planted positives cannot be trusted to find natural ones.
- **G1 — population.** ≥100 `need` and ≥100 `generic` rows after labelling. *Kill:* under-powered; report `inconclusive`, not a null.
- **G2 — separation, cumulative stars.** Cliff's δ on cumulative stars, two-sided permutation p.
- **G3 — separation, age-controlled.** Cliff's δ on **stars per year of existence** (`stargazers_count / max(years since created_at, 1)`), same permutation p. This controls for the confound that a repository from 2013 has had a decade more to accumulate.

## Results

### Coverage
- **need: 100**, **generic: 111**, **unlabelled: 489** out of **700 total**
- **Coverage: 30.1%** (211/700)
- Comparison: E113 Python v1 baseline ~29.7%; E130 JavaScript v2: 38.2% (with adaptation); E130 JavaScript no-adaptation: ~30%

### G0 (planted positive recovery)
- planted_need_recovered: 10/10
- planted_generic_recovered: 10/10
- **PASS** (threshold: 9)

### G1 (population ≥100/100)
- need: 100, generic: 111
- **PASS**

### G2 (cliffs delta on stars)
- δ = **0.1463**
- permutation p = **0.0689**
- Modest effect, not quite significant at α=0.05

### G3 (stars/year, age-controlled via created_at)
- need: n=100, mean 687.09, median 435.73
- generic: n=111, mean 594.37, median 212.26
- δ = **0.1694**
- permutation p = **0.0333**
- **Significant at α=0.05** — need-related repos have higher stars/year than generic repos

## Comparison with prior results
- E113 Python (v1, no bigrams): coverage ~29.7%, G1 FAIL
- E113 Python (v2, bigrams): coverage 38.2%, G1 PASS
- E130 JavaScript (Python-tuned v2): coverage 30.0%, G1 FAIL
- E130 JavaScript (JS-adapted v2): coverage 39.6%, G1 PASS
- **E131 Java (base v2, no adaptation)**: coverage 30.1%, G1 PASS, G2 δ=0.1463 p=0.0689, G3 δ=0.1694 p=0.0333 **significant**

## Key finding
The view-count principle's classification methodology (need/generic labeling) works on Java GitHub repositories with the base v2 classifier: G0 and G1 both pass, and coverage (~30%) is consistent across ecosystems. However, the arrival-count effect (G2, G3) is ecosystem-dependent: significant for Java (G3 p=0.0333) but not for JavaScript (G3 p=0.7358). The base classifier already achieves G1 passage without adaptation, unlike the JavaScript case where adaptation was needed.

## Conclusion
The view-count principle's measurement methodology functions on Java repos: the classifier labels sufficient rows and passes the population and discrimination gates. The significant G3 result (stars/year) suggests the arrival-count principle may hold for Java repos, unlike JavaScript where the effect was negligible and opposite in sign. However, the G2 result (p=0.0689) suggests the cumulative-star effect is not quite significant, and the overall evidence should be considered suggestive rather than conclusive.

## Next steps
A Java-specific classifier adaptation could improve coverage beyond 30.1% and potentially strengthen the effect sizes, similar to how the JavaScript adaptation improved coverage from 29.7% to 38.2% and made G1 pass (though it already passed with the base classifier for Java).