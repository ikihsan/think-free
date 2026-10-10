<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 Protocol — Hand replication of E062's answerability sub-test on Anova cooking Discourse

## Background

E062 (Steam/Stack Exchange) found 17 of 20 highest-arrival unremedied needs served by a free general assistant (F096). The population was technical (Stack Exchange), and the finding was that "unanswered on a platform is not unserved" — a general assistant answers most top-arrival needs.

E088 then tested a classifier-based generalization across 7 domains and failed discrimination: 8 of 20 nonexistent products classified `served` (0.40), difference from genuinely-served +0.150, CI95 [-0.148, +0.414] spanning 0. The classifier read no view counts and its G2 gate was too lenient.

This experiment hand-replicates E062's answerability sub-test on a **non-technical venue**: Anova cooking Discourse (community.anovaculinary.com). No classifier; human judgment only.

## Population

- Venue: Anova cooking Discourse (community.anovaculinary.com)
- Selection: Top 20 topics by view_count in the "Support" category (or equivalent), filtered to those with ≥1 reply and a clear problem statement
- Denominator: Topics where a user states a problem/need (not feature requests, not general discussion)
- Each row: one topic, human-judged for "served" vs "unserved"

## Served definition (pre-declared, from E062)

A topic is **served** if a free general assistant (tested: GPT-4o, Claude 3.5 Sonnet, or equivalent) given the topic title + first post body produces a correct, actionable answer that resolves the stated problem.

A topic is **unserved** if the assistant cannot produce a correct answer, or the answer requires information not in the topic, or the problem is inherently unsolvable (e.g., hardware failure requiring replacement).

**Partially served** is not used; binary judgment only.

## Calibration gates (must pass before population is read)

### G0 — Instrument discrimination (labels known by construction)

- 10 known-served probes: topics from Anova Discourse where the official solution is documented in the thread (staff reply with fix, or user confirms fix)
- 10 known-unserved probes: topics from Anova Discourse where the thread ends with "contact support" / "RMA" / "hardware failure" / no resolution after 30+ days
- Judge (human) must classify ≥8/10 known-served as served, and ≥8/10 known-unserved as unserved
- If G0 fails, the instrument (human + assistant) cannot discriminate; stop.

### G1 — Population accessibility

- Can fetch ≥20 topics with view_count, replies ≥1, clear problem statement
- If <20, venue insufficient; stop.

### G2 — Arrival signal validity

- Top-20 by view_count must have view_count > 0 (all do by construction)
- The view_count ordering must not be perfectly correlated with reply count (Spearman ρ < 0.9)
- If ρ ≥ 0.9, view_count adds no information over reply count; stop.

## Kill gates (measured on the 20-topic population)

### K1 — Served share lower bound

- Measured served share (Wilson CI95 lower bound) ≥ 0.50
- If CI95 lower bound < 0.50, the "general assistant serves most" claim fails for this venue.

### K2 — Difference from E062

- E062 served share: 17/20 = 0.85, Wilson CI95 [0.621, 0.948]
- If this venue's served share CI95 upper bound < 0.621, the generalization fails (this venue is significantly worse)
- If this venue's served share CI95 lower bound > 0.948, the generalization fails (this venue is significantly better — unlikely but possible)
- Otherwise, generalization holds (cannot reject same population)

## Reachable sets

- G0: 20 probes (10 served, 10 unserved) — fixed by construction, no sampling
- G1: All topics in Support category with view_count > 0, replies ≥1 — full census
- G2: Same as G1
- K1/K2: Top 20 by view_count from G1 set — fixed selection, no sampling

## Procedure

1. Fetch Anova Discourse Support category topics via Discourse API (public, no auth needed for read)
2. Filter: view_count > 0, reply_count ≥ 1, not pinned, not closed, clear problem statement in title/first post
3. Sort by view_count descending, take top 20
4. For G0: separately identify 10 known-served and 10 known-unserved from same venue (can be outside top-20)
5. Run G0 discrimination test — human judges each probe with assistant
6. If G0 passes, proceed to human judgment of top-20 population
7. For each of 20 topics: present title + first post to assistant, record answer, human judges served/unserved
8. Compute served share with Wilson CI95
9. Compare to E062 bounds (K2)

## Assistant configuration

- Model: GPT-4o (via API) or Claude 3.5 Sonnet (via API) — whichever is available
- Temperature: 0
- System prompt: "You are a helpful technical support assistant. Given a user's problem description, provide a clear, actionable solution. If you cannot determine the solution from the information given, say so."
- Input: Topic title + first post body (truncated to 4000 chars if needed)
- Output: Assistant's proposed solution

## Human judgment protocol

- Judge reads topic title + first post + assistant answer
- Judge knows the ground truth (for G0 probes) or searches the thread for resolution (for population)
- Binary decision: served / unserved
- Record reasoning for each

## Data products

- `probes.jsonl` — 20 G0 probes with ground truth and judgments
- `population.jsonl` — 20 population topics with assistant answers and judgments
- `results.json` — gate results, served share, Wilson CI, K2 comparison
- `VERDICT.md` — final build decision

## Pre-registration

This protocol is written before any population data is fetched. The G0 probes are identified after fetching but before any assistant queries. The population top-20 is fixed by view_count sort before any judgments.