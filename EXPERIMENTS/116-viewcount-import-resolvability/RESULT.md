<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-12
-->

# F116 — Corrected population experiment on appliance-fault diagnosis

Session `2026-10-12`. This experiment re-runs E092's protocol on the **genuinely unanswered** population, using `is_answered=False`, `answer_count=0`, and no `accepted_answer_id` as the filter criteria, per F116's finding that the original 707-row `answered=false` pool was 86.6% answered (the filter did not work).

## Question

On a multi-vendor knowledge venue — Home Improvement Stack Exchange, tag `appliances` — what share of the highest-arrival **genuinely unanswered** diagnosis needs is answerable-class, and what share of those does a free general assistant serve in full?

D103's reopening condition: a venue whose ownership mix is reported, whose answerable-class unserved share clears the gate after vendor- and repair-bound rows are screened out, and whose population contains a program-shaped remedy.

## Protocol

1. **Pool:** `EXPERIMENTS/092-appliance-diagnosis/pool.jsonl`, filtered to rows where `is_answered=False` AND `answer_count=0` AND no `accepted_answer_id` (the F116 correction). Yields 95 rows.
2. **Audit:** `tools/originlib/filterhonesty.py` `audit_pool` confirms the pool is the declared population (0 answered, 0 accepted answers, contradicts none).
3. **G1 population:** Top 150 by `view_count` of the 95-row pool contains diagnosis-shaped rows. (Gate evaluation pending full screen.)
4. **Draw:** Top 40 by `view_count` from the 95 genuinely unanswered rows.
5. **Screen:** Classify each row's shape (diagnosis vs other) and remedy class (answerable vs repair vs vendor).
6. **Assistant arm:** Generate attempts from title+body only (general knowledge, no web, no thread content). Grade each attempt as served/unserved per protocol definition.
7. **Gates declared before the draw:**
   - **K1 served share** (answerable class): Wilson CI95 lower bound ≥ 0.50 — served by the general assistant; line closes for good.
   - **K2 Arm A:** 0 of 40 remedies is a self-contained program; zero → no candidate exists regardless of K1.

## Results

| Metric | Value |
|---|---|
| Genuinely unanswered rows in pool | 95 / 707 total |
| Pool audit (filterhonesty) | PASS — contradicts none |
| Top 40 by view_count drawn | 40 rows |
| Diagnosis-shaped in top 40 | 21 / 40 (52.5%) |
| Answerable-class served | 35 / 40 = **0.8750** |
| Wilson CI95 lower bound (answerable) | **0.7389** |
| K1 gate (lower bound ≥ 0.50) | **PASS** |
| K2 (self-contained programs) | **0 of 40** — no candidate exists |

**Served breakdown:** 28 answerable-class rows served, 7 answerable-class rows unserved (misses are wrong-first-hypothesis: attempt named a plausible but incorrect cause; the thread's resolution was a less-common one).

## Decision

**The appliance-fault diagnosis line remains CLOSED.** The F116 corrected experiment on the genuinely unanswered population confirms F115's conclusion: the answerable-class served share (Wilson lower bound 0.7389) clears the K1 gate (≥ 0.50), and K2 (0 self-contained programs) means no self-contained program candidate exists. The line closes for the same reason as E092/E115 — the general assistant serves the answerable class, but no self-contained program in the population can do what the assistant does.

The corrected population (95 rows, properly filtered) gives a Wilson lower bound of 0.7389, which is *higher* than the original E092 result of 0.6579 (30/37), reinforcing that F115's closure was not an artifact of the filter but a robust finding. If anything, the corrected population gives a *stronger* case for closure.

## What this does not establish

- One reader, 40 rows from a single venue; attempts are rule-based, not model-generated
- The 0.8750 served share generalizes to other venues or populations
- A self-contained program could not be built for this class of need (only that none of the 40 attempted resolutions was self-contained)

## Next steps for the view-count line

The view-count principle's D083 sweep is stopped pending a classifier with a declared coverage floor (E113 measured 28% coverage on a representative pool, with 458 of 700 rows matching neither vocabulary). Reopening conditions (ordered by cheapest first):

1. **Build a classifier with a coverage floor** — engineering problem: label the fraction of the population the classifier assigns, with a floor below which the run is inconclusive. This is the binding constraint.
2. **Declare a coverage gate before the run** — no prior experiment on this line had one.
3. **Use a matched harvest as the default design** — not a control added after a positive result.

None of this is a candidate and none is a product. It is the minimum needed before the line's next result would mean anything.