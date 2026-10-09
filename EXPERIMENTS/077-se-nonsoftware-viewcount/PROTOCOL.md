<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E077 — Non-software Stack Exchange view_count + unserved-open measurement

## Objective

Measure the view_count (arrival) instrument and unserved-open-like fraction across a stratified sample of non-software Stack Exchange sites. This is a fresh observation in a new domain, following the finding that `view_count` is Stack-Exchange-shaped (E071, F101) and the need-harvest route is retired (F098, F100).

## Background

- E062 found the confound: "requester never came back" ≠ unserved need. A free general assistant answers 17/20 highest-arrival unremedied non-software needs.
- E063 ran the answerability instrument on GitHub issues and HN corpus: served share 0.676/0.969, 0 of 103 unserved-open.
- E071 confirmed `view_count` is only available on Stack Exchange (80/80), not HN (0/60) or GitHub Issues (0/8).
- E076 measured Discourse (keebtalk.com): 30 topics, 100% view_count > 0, 2 need topics, 0 unserved-open-like.
- The candidate seat is empty; all derived actions from previous candidates are spent.

## Population

Non-software Stack Exchange main sites that:
1. Are not in beta
2. Have measurable activity (questions_per_minute > 0 or total_questions > 1000)
3. Are not software/developer-focused

Stratified by domain category:
- **Home/DIY**: cooking, diy, gardening, woodworking, homebrew, coffee, beer
- **Travel/Outdoors**: travel, outdoors, bicycles, motorcycles, aviation, drones
- **Creative/Arts**: photography, video, sound, graphicdesign, crafts, arts, music, movies, tv, scifi, fantasy, puzzling
- **Science/Academic**: physics, chemistry, biology, earthscience, astronomy, space, academia, history, politics, philosophy, skeptics, economics, law
- **Language/Culture**: english, ell, japanese, chinese, french, german, spanish, russian, italian, portuguese, latin, greek, hebrew, arabic, korean, hindi, turkish, polish
- **Health/Lifestyle**: fitness, nutrition, baking, wine, tea, parenting, pregnancy, babies, lifeskills, productivity
- **Professional/Financial**: money, personalfinance, workplace, entrepreneurship, careers, patents
- **Technical/Hobby**: 3dprinting, woodworking, mechanics, cars, landscaping, sustainability

## Sampling

Target: 10 sites, 100 questions each (1000 total), stratified across categories.
Sites selected (pre-declared, before measurement):
1. cooking (Home/DIY)
2. diy (Home/DIY)
3. travel (Travel/Outdoors)
4. gardening (Home/DIY)
5. photography (Creative/Arts)
6. physics (Science/Academic)
7. english (Language/Culture)
8. parenting (Health/Lifestyle)
9. money (Professional/Financial)
10. 3dprinting (Technical/Hobby)

Alternates (if any site fails): woodworking, homebrew, coffee, beer, video, sound, graphicdesign, ux, chemistry, biology, earthscience, astronomy, space, aviation, drones, workplace, academia, history, politics, philosophy, skeptics, economics, law, personalfinance, entrepreneurship, careers, productivity, languagelearning, japanese, chinese, french, german, spanish, russian, italian, portuguese, latin, greek, hebrew, arabic, korean, hindi, turkish, polish.

## Measurement

For each question, collect:
- question_id
- title
- view_count
- answer_count
- score
- creation_date
- last_activity_date
- tags
- is_answered
- accepted_answer_id (if any)
- owner.reputation

Classification (pre-declared, adapted from E074/E076):

**Need patterns** (title suggests a concrete problem/question):
- `\bhow (do|can|to|should|would|is|are)\b`
- `\bwhat (is|are|should|would|could|causes?|makes?)\b`
- `\bwhy (is|are|do|does|did|can|won|not)\b`
- `\bhelp\b`
- `\bissue|problem|error|broken|failure|not working\b`
- `\brecommend|suggestion|advice\b`
- `\bwhich (one|should|is best|to buy|to use|get)\b`
- `\bwhere (can|to|is|are)\b`
- `\bany (idea|suggestion|tip|advice|recommendation)\b`
- `\bcan (someone|anybody|anyone)\b`
- `\bstuck|confused|lost\b`
- `\btrying to\b`
- `\bwondering\b`
- `\bshould I\b`

**Non-need patterns** (title suggests sharing, showing off, meta, etc.):
- `\bIC\b` (in character / I see)
- `\bshow.*(off|me)\b`
- `\bmy (new|first|latest) (setup|build|project|purchase)\b`
- `\blook at (this|my)\b`
- `\bjust (got|bought|picked up|received)\b`
- `\bwhat.*(you|getting|ordering|buying)\b`
- `\bwelcome to\b`
- `\bthank(s| you)\b`
- `\bimage(s)?\s*(only|thread)\b`
- `\bpicture(s)?\s*(only|thread|uno)\b`
- `\bintroductions?\b`

**Unserved-open-like rubric** (three clauses, all must be true):
1. **No platform-recorded resolution**: No accepted answer AND (answer_count < 3 OR (answer_count >= 3 AND no answer with score >= 1))
2. **States a concrete need**: Title matches at least one need pattern AND no non-need pattern
3. **Not a request for content/service/price/access/human work**: Already filtered by non-need patterns

## Gates

**G1 (view_count validation)**: ≥95% of questions have view_count > 0
- This validates the arrival instrument works on this population

**G2 (need prevalence)**: ≥5% of questions classified as need topics
- Ensures the population has measurable need density

**G3 (unserved fraction measurable)**: unserved-open-like fraction < 50% with Wilson CI95 upper bound < 60%
- If unserved fraction is very high, the classification may be wrong
- If unserved fraction is very low (like E076's 0%), the population may be well-served

**G4 (cross-site variance)**: At least 3 sites have unserved-open-like fraction > 0
- Ensures the measurement captures real variance, not a systematic artifact

## Analysis

Primary outcomes:
- Per-site unserved-open-like fraction with Wilson CI95
- Pooled unserved-open-like fraction with Wilson CI95
- view_count distribution per site and pooled
- Need topic prevalence per site

Secondary:
- Correlation between view_count and unserved status
- Tag-level analysis within sites
- Comparison with E076 (Discourse) and E063 (GitHub/HN) results

## Falsification

The experiment fails (kills the fresh observation route) if:
- G1 fails: view_count is not available on non-software SE sites
- G2 fails: need prevalence < 5% (classification not working)
- G3 fails: unserved fraction > 50% or CI95 upper > 60% (classification likely wrong)
- All 10 sites show 0% unserved (population uniformly served, no candidate opportunity)

## Deliverables

- `raw/questions_<site>.jsonl` — raw question data per site
- `raw/classified_<site>.jsonl` — classified questions per site
- `results.json` — aggregated results with gates assessment
- `README.md` — experiment summary and interpretation

## Resource constraints

- Stack Exchange API: 300 requests/day unauthenticated, 10,000 with key
- 10 sites × ~2 pages (50 questions/page) = ~20 requests
- Well within limits
- Stdlib Python only, no external dependencies