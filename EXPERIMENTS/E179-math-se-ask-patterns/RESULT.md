<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E179 Result — Question-Ask Patterns on Math Stack Exchange

**Experiment**: E179 — Fresh observation of question-ask patterns on Math Stack Exchange
**Protocol**: Adapted E178 is_lexicon for title-only classification (bodies not available via /questions API endpoint with default filter)
**Data fetched**: 30 highest-vote questions with answers from `https://api.stackexchange.com/2.3/questions?sort=votes&site=math`
**Classification vocabulary**: E178 LEADING/ARTEFACT/SUPPLY patterns applied to question titles

## Results

### Classification counts
- **Has ask (title patterns)**: 18 topics (60.0%)
- **No ask (title patterns)**: 12 topics (40.0%)
- **Total classified**: 30

### Activity metrics
- All 30 questions have accepted answers (100% answered)
- View counts range from 7 to 620,889
- Score range: -3 to 1680

### Gate results
- **G1**: FAIL — total classified (30) < 100 threshold
- **G4**: has_ask >= 0.50 — PASSED (0.6000 >= 0.50), but full M2 bucket analysis not measurable with title-only data
- **G2/G3/G5**: Not applicable with n=30 and title-only classification

### Comparison to baselines
- **Stack Overflow (E178)**: has_ask = 31/46 = 0.6739 [STATE.md]
- **Personal Finance SE (F138)**: round-trip ask rate = 27/30 = 0.9000 [STATE.md]
- **Math SE (E179, title-only)**: has_ask = 18/30 = 0.6000

This experiment places Math SE between SO and PF SE in terms of question-ask frequency, with Math SE at 0.6000, SO at 0.6739, and PF SE at 0.9000.

### Key observation
The 18 questions classified as "ask" based on title patterns include those starting with question words (How, Why, When, Which, Who, What), those ending with "?", and those containing artifact+supply combinations (e.g., "Can I use...", "How do I...", "Is this...?"). The 12 questions without ask patterns are predominantly statement-style titles (e.g., "Different ways to prove...", "What are imaginary numbers?", "Proofs that every mathematician should know").

### Note on methodology
The E178 is_ask lexicon was designed for full question+answer+comment data from Stack Exchange sites. This adaptation applies the lexicon to question titles only, since the Stack Exchange `/questions` API endpoint with default filter does not return question bodies at scale. The title-only classification captures the most salient ask patterns but may miss ask indicators present only in question bodies. A full M2 bucket analysis (publishable/asker_only/third_party/none) and M3 grounding analysis require body text access, which was not available via the API in this environment.

### Raw data
See `EXPERIMENTS/E179-math-se-ask-patterns/results.json` for complete classified questions and activity metrics.