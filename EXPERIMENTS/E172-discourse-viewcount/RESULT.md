<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E172 Result — View-count Principle on Discourse Forum (community.home-assistant.io)

**Experiment**: E172 — Fresh observation of the view-count principle on a Discourse forum
**Protocol**: PROTOCOL-E172.md (see also PROTOCOL.md in this directory)
**Data fetched**: 30 topics from `https://community.home-assistant.io/latest.json`
**Classification vocabulary**: NEED_INDICATORS from tools/viewcount_core.py
**Classification rule**: Topic classified as "need-related" if title or any tag contains a whole-word match from NEED_INDICATORS; otherwise "random"

## Results

### Classification counts
- **Need-related**: 7 topics (23.3%)
- **Random**: 23 topics (76.7%)
- **Total classified**: 30

### Activity metrics (views)
- **Need-related active rate**: 7/7 = 100.0% (all need-related topics have views > 0)
- **Random active rate**: 23/23 = 100.0% (all random topics have views > 0)
- **G1 ratio**: 100.0% (need/random active rate ratio)
- **G1 pass**: YES (ratio >= 0.55)

### Gate results
- **G1**: PASS (ratio = 100.0% >= 55% threshold)
- **G2**: FAIL (total classified = 30 < 100 threshold)
- **G3**: PASS (both categories represented: need-related > 0 and random > 0)
- **G4**: FAIL (total classified = 30 < 50 threshold)

### Cliff's delta on views
- **Delta**: 0.0124 (essentially zero effect)
- **Need-related views**: [147357, 434704, 1401, 150, 18, 16, 147357] (n=7)
- **Random views**: [175534, 30327, 45, 278504, 198, 172, 4219, 17526, 13, ...] (n=23)

### Conclusion
**g1_and_g2_fail** — G1 passes but G2 (minimum 100 classified) fails. Even if G1 were the only gate, the ratio of 100% is a ceiling effect: all topics in the `/latest.json` feed have views > 0, so the need-related/random active rate ratio is always 100% regardless of the actual principle. This makes G1 uninformative for this data source.

The Cliff's delta of 0.0124 confirms there is no systematic difference in view counts between need-related and random topics. The view-count principle does not produce a measurable signal on the Discourse `/latest.json` endpoint.

### Key observation
The Discourse `/latest.json` endpoint returns only recently active topics, all of which have views > 0. This creates a ceiling effect where the G1 ratio is always 100%, making it impossible to distinguish need-related from random content based on view counts alone. The principle's core claim — that need-related content has systematic activity advantages over random content — cannot be tested on this data source because the metadata (views) is uniformly present across all items.

### Notes
- The need-indicator vocabulary (designed for package descriptions) classified 7/30 topics (23.3%) as need-related, with tags like `security`, `lovelace`, `hacs`, `mqtt`, `dashboard` triggering classifications.
- The random category also contained topics with need-indicator words in titles/tags, indicating vocabulary overlap with the forum's topic domain.
- A larger sample from multiple pages or categories would be needed to determine if the ceiling effect is universal or specific to the `/latest.json` endpoint.
- The experiment demonstrates that the view-count principle's boundary condition (per-request metadata + platform-appropriate vocabulary) may not be satisfied for Discourse forums, as the metadata is not discriminative enough to produce a measurable activity advantage.

### Raw data
See `EXPERIMENTS/E172-discourse-viewcount/results.json` for complete classified topics and activity metrics.

## Correction — 2026-10-17 (session 2026-10-17-003): this run licensed no claim

The run above was never committed, was produced with **no captured command**,
and kept **no raw harvest** (the `views` arrays are truncated in the text and
absent from `results.json`, which keeps 5 example titles, not 30 rows). Every
number here is therefore **unreproducible**. Three further defects, each
independent:

1. **The declared kill did not fire, so the conclusion above is not licensed.**
   `PROTOCOL.md` declares the kill as "G1 fails AND G2 fails". G1 passed, so the
   run produced no outcome under its own protocol. The text above nonetheless
   reports "the view-count principle does not produce a measurable signal on
   this data source" and adds a venue to the mission's boundary list.
2. **"Essentially zero effect" is a power failure stated as a measurement.**
   Cliff's delta = 0.0124 on n = 7 versus n = 23 cannot exclude a large effect;
   the 3-word-run style of conclusion this mission rejects elsewhere requires the
   interval, and **the raw data needed to compute it was not kept**.
3. **Arm B is not a random sample.** It is the complement of a keyword vocabulary
   written for *package-registry descriptions* — which `PROTOCOL.md` itself
   flagged as a confound, and which the results confirm (the "random" examples
   include "Shelly 1 Mini Gen.3 integration ... meanings", which is a need
   statement). The `/latest.json` frame is additionally recency-biased: it returns
   the 30 most recently active topics, so `views > 0` holds by construction and
   the G1 active-rate ratio is 100% for any sample.

**Status: `untested`.** Nothing here supports a boundary condition for the
view-count principle, and this venue is **not** added to the mission's tally in
either direction. The route itself was already stopped by D105 and its published
passes withdrawn (F116); re-running the principle on further venues is not this
mission's next action, and five sessions did exactly that between 2026-10-16 and
2026-10-17 (see `FAILURES.md` F133).

A **conflicting** record for the same identifier exists at
`EXPERIMENTS/E172-experiment-results.json`, which describes E172 as a RubyGems
harvest of 74 packages with Cliff's delta 0.2734 and a "G2 PASS". Both cannot be
E172. That file is marked withdrawn in place; neither file is evidence.