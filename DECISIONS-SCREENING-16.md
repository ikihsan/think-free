<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Decisions — screening candidates and judging experiments, part 16

Split out of [`DECISIONS-SCREENING-15.md`](DECISIONS-SCREENING-15.md) on
2026-10-09. The rule is unchanged: a decision is recorded when the choice was
genuinely open, with evidence, alternatives, and reason.

Decisions **D090, D091**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

## D090 — A detector's error budget is read by cause, and a mechanism is closed on the population that breaks it rather than the one that confirmed it (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-002, E072, F185.

**The situation.** E065/E066 was the only line in this record with all four
predeclared gates passing on real data, and its own README named the axis it
had not tested: merchant strings. `STATE.md` made closing that axis "the single
most useful next action". E072 closed it, and the answer was not the expected
one. Recall against a hand-read watchlist was 0.394. Decomposing the 20 misses
gave **6 from the merchant axis the protocol went in to measure** and **14 from
an amount-consistency gate nobody had questioned**: five accounts paying for
the same subscription monthly on the same day, where the only difference
between the one that is detected and the four that are missed is whether the
price ever changed.

**The decision.**

1. **A detector's errors are attributed to a cause before a rate is compared.**
   Recall alone cannot distinguish "the grouping shattered it" from "the
   scoring rejected it", and the repair is different in each case. Every miss
   in E072 is now printed with its raw strings and its normalized names
   (`inspect_errors.py`), which is what turned "recall 0.394" into "six
   fragments of three digits, and fourteen price changes".
2. **A mechanism is closed on the population that breaks it, and the closing
   names the population.** E065's detector is closed *on real modern
   subscription exports with price movement*. It is not closed on standing
   orders, and E066's result stands for the population it was measured on —
   which is the whole reason the record kept E066's numbers rather than
   replacing them.
3. **A precision figure computed against a positives-only label set is not a
   precision figure.** E072's watchlist-scored precision is 0.100 and a
   hand-read stratified sample reads 0.91 on the same detections; the gap is
   the label set, not the detector. Both are reported. E065's headline 1.0000
   was measured the same way and survives only because its synthetic corpus had
   no unclaimed groups in it — **a lower bound that happened to sit at 1.0.**

**Rejected: fix the merchant axis, because it is the axis E066 named.**
Adopting the predicted failure would have closed the line with the wrong reason
recorded, and the next session would have rebuilt a normalizer to fix a problem
worth 6 of 20 misses while the 14-miss defect sat untouched.

**Rejected: report recall 0.394 as the mechanism's quality.** It is a floor
produced by a 33-family watchlist on accounts whose readers hold mortgages and
meal plans. The recall figure is real; the precision figure beside it was not,
until it was hand-read.

**Rejected: treat Actual Budget's F1 0.150 as a competitor benchmark.** It is a
**lower bound on the incumbent**, because in production Actual matches on a
payee its importer has already cleaned and this experiment hands it raw
strings. Two detectors within 0.01 F1, both far below usefulness, is a
statement about the population. `actual_shared` — both engines given the same
merchant axis — is the arm that can compare engines, and it says the engines are
within noise: **the merchant axis is the mechanism, not the interval/amount
scoring.**

**Ceiling.** This governs how a detector's failures are read and how a closed
line is written up. It does not decide whether the repair is worth building —
that is the next experiment, and it is named in `STATE.md`: replace the CV
ceiling with a **piecewise-constant price** model. The evidence that this is a
specification defect rather than a retune is already in E072: 9 × $20.00 with
CV 0.000 and interval regularity 0.922 **is** detected today, and the identical
mechanism with one price step is not.

## D091 — The recurring-expense detector line is closed, and the closure names the repair and the population (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-003, E073, F186.

**The situation.** F185/D090 named one bounded repair for E065's detector —
replace the 0.15 amount-CV ceiling with a piecewise-constant price model —
and `STATE.md` made it the single most useful next action. E073 ran it on
E072's frozen corpus with two predeclared gates: G1 recall ≥ 0.50, G2 F1
margin over the incumbent ≥ +0.05. **Both fail.** The pwc arm scores recall
0.455 and F1 margin +0.048. It is strictly better than the CV ceiling on
every count (+2 TP, −13 FP, −2 FN, precision 0.100 → 0.126), and the 17
added groups are real price-change subscriptions (P1b hand-read) — but it
recovers only **2 of the 14** CV-gate misses.

**The decision.**

1. **The recurring-expense detector line is closed.** Not just E065's
   implementation (F185), but the repair F185 named (F186). The remaining 12
   misses have amount shapes a one-step model cannot capture — drift,
   oscillation, or multiple price changes — or are not recurring at all
   (payroll, mortgage escrow with varying amounts). No predeclared gate in
   this experiment tests those, and the line does not reopen on this
   population.

2. **A mechanism is closed when its predeclared repair fails its predeclared
   gates, even when the repair is strictly better than the mechanism it
   replaces.** The pwc model is a better detector than E065's. It is not a
   useful one. Closing on the gates rather than on the improvement direction
   is what keeps the record from accumulating a graveyard of "better but not
   good enough" mechanisms.

3. **Even a pass would not have started the differentiation question.** Per
   D090/F185, `actual_raw` is a *lower bound* on Actual Budget's production
   detector, and the useful/differentiated/adopted stack above the detector
   has not been started. A pass would have licensed the next question
   (does a person pay for this), not a candidate.

**Rejected: keep iterating on the amount model.** The pwc model recovers
2/14 misses. A richer model (drift, seasonality) might recover more, but
each iteration is a new mechanism on the same frozen corpus, and the line is
closed on this population. The remaining misses are a different problem.

**Rejected: treat the pwc model's strict improvement as a reason to build.**
Every metric improved and the gates still failed. Improvement without a
gate met is not a candidate.

**Ceiling.** This closes the detector line on 36 real bank exports with a
33-family hand-read watchlist. It does not close recurring-expense detection
as a domain — it closes one implementation and one repair on one population
of 36 public exports that are public because their owners were building
something else. The candidate seat is empty and every derived action from
every candidate is spent.