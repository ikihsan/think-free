<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E172 Protocol — View-count Principle on Discourse Forum (community.home-assistant.io)

## Arms

- **Arm A**: Topics classified as "need-related" (title or tags contain a need indicator from the mission's vocabulary)
- **Arm B**: Topics classified as "random" (no need indicator found in title or tags)

## Classification Rule

Each topic from the `/latest.json` endpoint is classified as follows:

1. Extract the topic `title` and `tags` (list of tag texts).
2. Lowercase both.
3. If any word in the title or any tag text matches a whole-word entry from `NEED_INDICATORS` (viewcount_core.py), classify as `"need-related"`.
4. Otherwise, classify as `"random"`.

This mirrors the word-boundary matching used for package descriptions, applied to forum title and tag text.

## Gates (G1–G4)

Using the standard `compute_gates` function from `tools/viewcount_framework.py`:

- **G1**: need-related active rate / random active rate >= 0.55
  - Active = topic has non-zero `views` (primary activity metric for forums)
  - need-related active rate = (need-related topics with views > 0) / (total need-related classified)
  - random active rate = (random topics with views > 0) / (total random classified)
- **G2**: total classified >= 100
- **G3**: both categories represented (need-related > 0 and random > 0)
- **G4**: total classified >= 50

**Kill condition**: G1 fails AND G2 fails (both the activity advantage and the sample size are insufficient). If G1 passes, the principle is supported for this domain.

## Activity Metric

- **Primary**: `views` per topic (from Discourse topic metadata)
- **Secondary**: `reply_count` per topic

A topic is considered "active" if `views > 0` (every topic has views, but the rate difference between categories is the signal).

## Data Fetch

- Endpoint: `https://community.home-assistant.io/latest.json`
- Sample size: All available latest topics (minimum 50 desired for G4)
- Fields per topic: `title`, `tags`, `views`, `reply_count`, `created_at`

## Procedure

1. **Write PROTOCOL.md** (this file) and commit.
2. **Fetch data** from the Discourse JSON API.
3. **Classify** each topic using the rule above.
4. **Compute gates** G1–G4 and active rates.
5. **Compute Cliff's delta** on `views` between need-related and random groups.
6. **Record RESULT.md** with full results.
7. **Update STATE.md** and `FAILURES-findings.md` with outcomes.

## Notes

- This is the first view-count principle test on a Discourse forum platform.
- The need-indicator vocabulary was designed for package descriptions; its applicability to forum titles/tags is part of the experiment.
- If classification yields very few need-related topics (e.g., < 10), the experiment should note this as a vocabulary-inapplicability finding.
- The declared bar for a "supported" result is G1 pass (ratio >= 0.55) with at least G2 passing (classified total >= 100).