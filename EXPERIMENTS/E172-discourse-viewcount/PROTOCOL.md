<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E172 PROTOCOL — View-count Principle on Discourse Forum (community.home-assistant.io)

**Date opened:** 2026-10-16. **Status:** pre-declared.

## The question

Does the view-count principle generalize to Discourse forums: specifically, does need-related content on community.home-assistant.io have systematic activity advantages (view counts) over random content?

## The population

The population consists of topics from the Discourse `/latest.json` endpoint, which returns the 30 most recent topics on the Home Assistant community forum. Each topic has a `title`, `tags` (list of tag objects with `name` and `slug`), and `views` metric.

## The arms

- **Arm A (need-related)**: Topics whose title or any tag name contains a whole-word match from the mission's `NEED_INDICATORS` vocabulary (from tools/viewcount_core.py).
- **Arm B (random)**: All other topics classified as random by the same rule.

## Classification rule

1. Extract the topic `title` and `tags` (list of tag names).
2. Lowercase both.
3. If any word in the title or any tag name matches a whole-word entry from `NEED_INDICATORS`, classify as `"need-related"`.
4. Otherwise, classify as `"random"`.

This mirrors the word-boundary matching used for package descriptions, applied to forum title and tag text.

## Gates (G1–G4), using `compute_gates` from tools/viewcount_framework.py

- **G1**: need-related active rate / random active rate >= 0.55
  - Active = topic has `views > 0`
  - need-related active rate = (need-related topics with views > 0) / (total need-related classified)
  - random active rate = (random topics with views > 0) / (total random classified)
- **G2**: total classified >= 100
- **G3**: both categories represented (need-related > 0 and random > 0)
- **G4**: total classified >= 50

**Kill condition**: G1 fails AND G2 fails (both the activity advantage and the sample size are insufficient). If G1 passes, the principle is supported for this domain (subject to G2+G3+G4).

## Activity metric

- **Primary**: `views` per topic (from Discourse topic metadata)
- A topic is considered "active" if `views > 0`

## Data fetch

- Endpoint: `https://community.home-assistant.io/latest.json`
- Sample: All available latest topics (30 in first page)
- Fields per topic: `title`, `tags`, `views`, `reply_count`, `created_at`

## Procedure

1. Write this PROTOCOL.md and commit.
2. Fetch data from the Discourse JSON API.
3. Classify each topic using the rule above.
4. Compute gates G1–G4 and active rates.
5. Compute Cliff's delta on `views` between need-related and random groups.
6. Record RESULT.md with full results.
7. Update STATE.md and FAILURES-findings.md with outcomes.

## Notes

- This is the first view-count principle test on a Discourse forum platform.
- The need-indicator vocabulary was designed for package descriptions; its applicability to forum titles/tags is part of the experiment.
- If classification yields very few need-related topics (< 10), the experiment should note this as a vocabulary-inapplicability finding.
- The declared bar for a "supported" result is G1 pass (ratio >= 0.55) with at least G2 passing (classified total >= 100).