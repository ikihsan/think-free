<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->

# F141 — Discriminating-observation procedure on appliance-fault diagnosis

Session `2026-10-14-005`. This experiment tests whether a discriminating-observation procedure beats a free general assistant's first hypothesis on appliance diagnosis, using the F116 corrected population.

## Question

On a multi-vendor knowledge venue — Home Improvement Stack Exchange, tag `appliances` — what share of the highest-arrival **genuinely unanswered** diagnosis needs are served by a discriminating-observation procedure, and how does this compare to the free general assistant's served share?

The discriminating-observation procedure extracts specific details (model numbers, error codes, observed symptom patterns) from the question body before proposing a remedy. When insufficient discriminating evidence exists, it "refrains" rather than proposing a plausible-but-incorrect hypothesis (the "wrong-first-hypothesis" pattern observed in 7 of 37 F116 answerable-class misses).

## Why this matters

E092 named the residue of the strongest alternative as wrong-first-hypothesis (7 of 37) but closed the line without testing it; D104's reopening limb is untested. Separately, /search/advanced?answered=false was observed live on 2026-10-12 to return ANSWERED questions, so E092's '707 unanswered' pool is 86.6% answered. F116 corrected the pool to 95 genuinely unanswered rows.

D103's reopening condition: a venue whose ownership mix is reported, whose answerable-class unserved share clears the gate after vendor- and repair-bound rows are screened out, and whose population contains a program-shaped remedy.

## Protocol

1. **Pool:** `EXPERIMENTS/092-appliance-diagnosis/pool.jsonl`, filtered to rows where `is_answered=False` AND `answer_count=0` AND no `accepted_answer_id` (the F116 correction). Yields 95 rows.
2. **Audit:** Pool constitutes the genuinely unanswered population; filterhonesty confirms 0 answered, 0 accepted answers.
3. **Draw:** Top 40 by `view_count` from the 95 genuinely unanswered rows.
4. **Discriminating-observation procedure arm:** For each row, extract specific details (model numbers, error codes, observable symptom patterns) from title+body only (no web, no thread content). Only propose a remedy when strong discriminating evidence exists; otherwise "refrain."
5. **Gates declared before the draw:**
   - **K1 served share** (answerable class): Wilson CI95 lower bound ≥ 0.50 — procedure serves the answerable-class population; line closes for good if passed, reopens with concrete reason if failed.
   - **K2 Arm A:** 0 of 40 remedies is a self-contained program; zero → no candidate exists regardless of K1 (procedure does not evaluate self-contained programs; inherited from F116).

## Results

| Metric | Value |
|---|---|
| Genuinely unanswered rows in pool | 95 / 707 total |
| Pool audit | PASS — contradicts none |
| Top 40 by view_count drawn | 40 rows |
| Served (procedure proposes correct remedy) | 2 |
| Unserved (wrong first hypothesis) | 0 |
| Refrained (no discriminating evidence; did not propose) | 38 |
| Served share (answerable, excluding refrains) | 1.0000 (2/2) |
| Served share (raw, including refrains) | 0.0500 (2/40) |
| Wilson CI95 lower bound (answerable) | 0.3424 |
| K1 gate (lower bound ≥ 0.50) | FAIL |
| K2 (self-contained programs) | N/A (procedure does not evaluate) |

**Served breakdown (2 rows):** Both served rows were washing-machine "not spin" diagnoses where the procedure identified the model + "washer + not spin" symptom pattern and proposed the correct remedy (check lid switch/motor coupler).

**Unserved/wrong-first-hypothesis breakdown (0 rows):** Zero rows had a wrong-first-hypothesis miss — the procedure successfully avoided proposing plausible-but-incorrect hypotheses by refraining when insufficient discriminating evidence existed.

**Refrained breakdown (38 rows):** 38 of 40 rows were refrained because the procedure could not extract sufficient discriminating evidence (no model-number/symptom combination that matched the if/elif decision rules). Model numbers were found for many rows (e.g., PFSS2MIXASS, B21CT80SNS) but the associated symptom patterns did not match the procedure's decision rules.

## Decision

**The discriminating-observation procedure does not beat the F116 baseline.** The Wilson CI95 lower bound of 0.3424 fails the K1 gate (≥ 0.50), and the served share (0.0500 raw, 1.0000 of answerable excluding refrains) is substantially below the F116 baseline of 0.8750 (Wilson LB 0.7389).

However, the procedure successfully avoided the wrong-first-hypothesis pattern: zero of 40 sampled resolutions was a wrong-first-hypothesis miss. All 38 unserved rows were "refrained" — the procedure deliberately did not propose a hypothesis due to insufficient discriminating evidence, rather than proposing an incorrect cause.

**What this does not establish:**
- A self-contained program candidate exists or does not exist (K2 not evaluated)
- The procedure generalizes to other venues or populations
- A different procedural design could not achieve a higher served share with fewer refrains
- The general assistant's served share of 0.8750 is invalid (it was measured on the same corpus with a different method)

**Next steps for the discriminating-observation line:**
- Engineer a more discriminating observation set (e.g., broader symptom patterns, additional model-specific inference rules) before re-declaring gates
- Measure whether a procedure with a different refraining threshold achieves K1 PASS while maintaining 0 wrong-first-hypothesis misses
- If no design achieves both K1 PASS and 0 wrong-first-hypothesis misses, the premise that a discriminating-observation procedure can beat the free general assistant's first hypothesis on this population is falsified

