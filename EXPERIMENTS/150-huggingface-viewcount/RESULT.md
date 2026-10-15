<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# Experiment 150: Hugging Face Hub View-Count Principle Test

**Decision: FAIL (primary kill gate: all metrics show negligible effect)**

Need-related models: 1151
General models: 170
Excluded: 579

## likes

- Need-related: n=1151, median=186.0, mean=742.1
- General: n=170, median=104.0, mean=585.1
- Cliff's delta: **0.0936** (95% CI: [0.0091, 0.1792])
- Mann-Whitney U: 88681.5, p=0.047627
- Shuffle test p: 0.0200

## downloads

- Need-related: n=1151, median=54023.0, mean=1197193.9
- General: n=170, median=256950.0, mean=2210342.4
- Cliff's delta: **-0.0854** (95% CI: [-0.1827, 0.0266])
- Mann-Whitney U: 89480.0, p=0.070368
- Shuffle test p: 0.9600

## trendingScore

- Need-related: n=1151, median=0.0, mean=10.0
- General: n=170, median=0.0, mean=2.0
- Cliff's delta: **0.1221** (95% CI: [0.0815, 0.1692])
- Mann-Whitney U: 85886.0, p=0.000162
- Shuffle test p: 0.0000

## Interpretation

No meaningful activity advantage detected for need-related models. The view-count principle does not extend to Hugging Face Hub models under this classification.
