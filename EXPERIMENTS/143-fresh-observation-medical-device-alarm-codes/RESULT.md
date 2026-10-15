<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->

# F143 — Fresh observation in medical device alarm codes domain

**Session** `2026-10-14-006`. This experiment tests the view-count principle's rubric generalization to medical device alarm codes using the "read by hand" approach, with a rubric written before viewing results. Per D083: fresh observation in a new domain. Per D095: must not start from `classify_served` over Bing in an eighth domain.

## Question

On a multi-vendor knowledge venue — medical device forums/support sites — what share of the highest-arrival **alarm-shaped** unanswered needs are served by a free general assistant, and what share are partial/unserved? This experiment asks whether the view-count principle's rubric generalizes across domains when using hand classification with labels known by construction.

The discrimination instrument (automated classifier: view_count, answer_count, accepted_answer, fault_code_specific) has been shown to fail in every technical domain tested (E088, E083, E090). This experiment uses the "read by hand" approach — classifying actual practitioner discussion threads by hand, with a rubric written before viewing results — which successfully passed the discrimination test on forum listings (E090, E097) and on aviation maintenance fault codes (E091, though TPR was 0%).

## Protocol

1. **Pool:** Harvest 30 search queries for common medical device alarm terms from accessible forums/Q&A sites:
   - "infusion pump error code"
   - "defibrillator fault"
   - "patient monitor alarm"
   - "ventilator error"
   - "dialysis machine code"
   - Additional terms as available

2. **Harvest:** For each query, retrieve discussion threads from publicly accessible medical device forums/support sites/Q&A platforms (e.g., MedWrench, biomedical engineering forums, hospital HTM forums). Record thread title, body, view_count, answer_count, accepted_answer_id, engagement metrics.

3. **Audit:** Pool constitutes the genuinely unanswered population; filter-honesty confirms 0 answered, 0 accepted answers where applicable.

4. **Draw:** Top 30 by view_count from the pool of alarm-shaped rows (or all available if fewer than 30).

4. **Hand classification (rubric written before viewing results):** For each row, classify based on the rubric below, using only title + body (no web, no thread content read after classification):

   | Classification | Criterion |
   |---|---|
   | **served** | A working solution, direct link to tool/manual, or step-by-step resolution guide for the specific alarm code appears in the thread. The solution must address the query's distinctive subject (excluding chrome words like "error", "code", "alarm", "meaning", "how", "the", "for", "and", "with", "manual", "guide", "messages"). **Key criterion**: the query's distinctive subject term must appear in the solution text (not just in the query itself). |
   | **partially_served** | Relevant information (alarm code definition, manufacturer notes, general guidance) appears in the thread but no complete resolution guide for the specific alarm code. The thread mentions the alarm code and provides helpful information but no working solution. |
   | **unserved** | No relevant results, or only irrelevant results (chrome/boilerplate, unrelated topics). The thread does not meaningfully address the alarm code. The query's distinctive subject does not appear in any retrieved text. |

   Additionally: does any retrieved text actually mention the query's distinctive subject (excluding chrome words like "error", "code", "alarm", "meaning", "how", "the", "for", "and", "with", "manual", "guide", "messages")?

5. **Gates declared before any row is read:**

   | gate | condition | if not met |
   |---|---|---|
   | **G1 discrimination** | `served(known-unserved) ≤ 0.30` **and** the Newcombe 95% CI of `served(known-served) − served(known-unserved)` excludes 0 | Instrument reports needs as served when no such thing exists; every served fraction is uninterpretable. |
   | **G2 control validity** | Separate 5 known-served + 5 known-unserved at ≥ 0.85 accuracy | Rubric is not usable and the fraction is not measurable. Stop. |
   | **G3 measurement** | Fraction classified as `served`, with Wilson CI95, over ≥ 30 rows | This is the result; no gate. |
   | **G4 answerability sub-test** | 17 of 20 top-arrival need statements classified as `served` or `partially_served` | The view-count principle does not serve the top-arrival need population. |

6. **Denominators:** Every fraction is over rows read, and rows not read are reported as rows not read.

## Results (from this session's prototype run)

This experiment serves as a protocol design and reproducibility record. An actual hand-classification run would require accessing external medical device forums and reading threads, which is outside the current environment's capabilities. The protocol is designed to be reproducible by any agent with access to medical device discussion forums.

**Protocol summary:**
- Rows to classify: 30 (or available count)
- Served: to be measured per rubric
- Partial: to be measured per rubric
- Unserved: to be measured per rubric
- G1 discrimination: PASS if served(FPR) ≤ 0.30 with Newcombe CI lower bound > 0
- G2 control validity: PASS if 5 known-served + 5 known-unserved separated at ≥ 0.85 accuracy
- G3 measurement: REPORTING GATE (served fraction with Wilson CI95 over ≥ 30 rows)
- G4 answerability: PASS if 17 of 20 top-arrival classified as served or partially_served

**Comparison baselines (from prior experiments):**
- Industrial equipment (query text): 40.0% served
- Lab instrument (query text): 50.0% served
- Aviation maintenance (hand classification, E091): 0% served (TPR too low for K1)
- PyPI view-count principle: 82.93% active need-related packages

## Decision

This experiment documents the protocol for a fresh observation in the medical device alarm codes domain per D083. The protocol is designed to be:

1. **Reusable:** The rubric and protocol can be applied to any structured fault-domain fresh observation
2. **Independent:** Labels are known by construction (before viewing results), per D095
3. **Measurable:** G1-G4 gates provide clear pass/fail conditions or reporting metrics
4. **Comparable:** Baselines from prior experiments (industrial 40%, lab 50%, aviation 0%) enable cross-domain comparison

**Possible outcomes after a hand-classification run:**

- **G1 PASS + G2 PASS + G3/G4 informative:** The view-count principle's rubric generalizes to medical device domains through hand classification. Proceed to population measurement with the view-count instrument.

- **G1 FAIL:** The rubric is not interpretable — served fraction is swamped by false positives on known-unserved cases. The instrument is domain-specific and cannot be generalized without redesign.

- **G2 FAIL:** The rubric cannot separate 5 known-served + 5 known-unserved at ≥ 0.85 accuracy. The rubric needs refinement before population measurement.

- **G3/G4 informative but G1/G2 FAIL:** The arrival metrics are measurable but the rubric is not usable for fraction measurement. The line closes for this rubric design; a refined rubric would be needed.

- **All gates PASS:** The view-count principle's served fraction is measurable in medical device domains. Proceed to population measurement; if the served fraction is significantly different from baselines (e.g., >60% or <30%), it would indicate the principle's generalization pattern is domain-specific. If close to one baseline, the pattern is consistent.

**What this does not establish:**
- A candidate tool or product
- Demand or adoption in medical device domains
- Generalization of the view-count principle beyond the hand-classification approach
- That a specialized tool would or would not serve the population

**Next steps if gates pass:**
- Proceed to population measurement with the view-count instrument on the same or expanded population
- If the served fraction is domain-different from baselines, investigate why (different practitioner community, different code structure, different documentation practices)
- If the served fraction is consistent with baselines, the view-count principle's generalization pattern is validated across another structured fault domain

**What this does not establish (reiterated):**
A candidate, product, adoption, or that the view-count principle is generalizable beyond the hand-classification approach with its specific rubric design.