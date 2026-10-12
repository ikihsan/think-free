<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# Screening decisions, part 20

Split out of [`DECISIONS-SCREENING-19.md`](DECISIONS-SCREENING-19.md), which held
D106. This part holds the decisions taken when a candidate is closed by
**measuring the incumbent on a task it already performs**, and the one about
what to do when that happens five times running.

Decisions **D107**. Each entry records a choice that was genuinely open, the
options considered, and what was decided.

| id | decision |
|---|---|
| [`DECISIONS-SCREENING-20.md`](DECISIONS-SCREENING-20.md) | D107 — the applicability-threshold line closes on a served population (E115, F119), and "served is the modal outcome" becomes a standing constraint on how the next candidate is chosen: the screen must target a task whose answer is **not** decidable from the rule text plus the facts, because that is the only region E115 leaves open |

## D107 — the applicability line closes, and the standing constraint that comes from five closures

**Date:** 2026-10-12. **Evidence:** E115, F119.
**Supersedes:** nothing. **Depends on:** D104 (close on service, not on
population), D105 (stop a sweep that measures its own sampling design), D106 (a
verifier is validated on the population it will be used on).

### The choice

CFR applicability thresholds are a population the mission had never touched, in
a domain the mission had never touched: not software, not a forum, not a
registry. Two things could be done.

1. **Harvest more.** Title 29 gave 81 spans; the CFR has 50 titles and the same
   threshold style appears in each. Counting them costs one unauthenticated API
   and would make the harvest a better catalogue.
2. **Close the line on what M2 measured, and record what the closure means for
   how the next candidate is chosen.**

**Chosen: option 2, and the harvest stops.** Not because 81 spans is too small —
it is not the binding constraint. Because **M2b already answered the question
the harvest would be extended to answer.** D105 stopped the view-count sweep
for measuring its own sampling design; the same reasoning applies here with the
roles reversed. Extending the harvest would produce a better catalogue of a
population the incumbent already serves, which is not progress toward a
candidate.

### What E115 measured

The applicability question is decidable from **the rule text plus the facts**,
and on 14 hand-keyed fact patterns a free general assistant answered **14/14**
with the deciding clause supplied and **14/14 with no clause, no citation, and
no search performed** — including **6 of 6** on the six cases where the
counting rule changes the answer. The plain-headcount reading scores **0 of 6**
there. Declared kill gate 0.95: met. **The population is real, large,
reachable, and served.**

### The standing constraint this earns

Five real populations have now been closed on service, in a row, by five
different experiments:

| population | served share | finding |
|---|---|---|
| non-software Stack Exchange needs | 17/20 | E062, F096 |
| Anova appliance forum | 5/20 — vendor-bound composition | E091, F114 |
| Home Improvement SE diagnosis class | 30/37 = 0.81 | E092, F115 |
| Federal Register document values | 0 of 374 fabricated | E114, F118 |
| **CFR applicability counting rules** | **6/6, 14/14 overall** | **E115, F119** |

**So: for any next candidate, a screen must establish that the answer is not
already decidable, before the population is harvested.** The specific region
E115 leaves open, and the only one, is a population whose answer **cannot be
computed from the text plus the facts** — because the missing input is
*evidence*, not *arithmetic*. E115's own design excluded exactly that
population: cases whose correct answer turns on facts no rule states cannot be
keyed by hand, so they cannot be scored against a committed key.

**This is a constraint on where to look, not a reason to stop looking.** It does
not license another instrument audit, and it does not make the CFR closed —
`M2.md` names two unmeasured leads in the same title (the per-establishment ×
company-wide conjunction in §§ 1904.1/1904.2, and amendment-tracking: whether
a tool could report a user's *current* exemption rather than the text as
published). The second is the stronger of the two, because the answer to
"which text applies to me today" is not a fixed function of the facts.

### Alternatives rejected

- **Keep harvesting the CFR.** Rejected: it buys catalogue depth for a
  population M2b shows is served, and it is D105's mistake pointed the other way.
- **Treat the fifth closure as evidence that no candidate exists.** Rejected:
  each closure is a statement about the population actually tested. E115's is a
  statement about *decidable-from-text* applicability in one title on one date,
  with a single-reader ceiling. It does not generalise to the CFR, to
  undeducible populations, or to the non-text inputs the record keeps finding.
- **Publish a tool anyway.** Rejected, and it is the standing rule
  (`STATE-next-actions.md`): E091's closure stopped `pyprovides` being
  published, E092 stopped the diagnosis line, E114 kept `ground.py` as a
  ranker rather than a gate. A tool with no measured unserved population is
  work, not a candidate.
- **Rewrite the closed lines.** Rejected: the record preserves what was believed
  at the time and what falsified it, which is F052's opposite and the reason
  F116 was recoverable at all.

---

## D108 — the recurring-payment line closes: the free general assistant is the best reader of standing orders on a real bank extract, and the detector has no unserved population (E116)

**Decided 2026-10-12, VM 0947.** Evidence: E116,
[`EXPERIMENTS/116-berka-service-test/`](EXPERIMENTS/116-berka-service-test/README.md),
F121, F122.

**The question.** E066 validated a deterministic recurring-payment detector
(interval+amount core, F1 0.8194) on the Berka bank extract. E116 asked the
complementary discriminating question: handed the same extract as rows of
`date | amount | counterparty`, can a free general assistant find the recurring
payments — the ones the bank itself codes as standing orders?

**What was measured.** 80 accounts (60 R, 20 C), 75 positive groups, three
readers on the same accounts and the same key. The assistant read each
committed extract and named the counterparties it judged recurring; the
answers were committed before any scoring; the detector was E066's
`detect.py`, unmodified; the naive baseline was any group with ≥3 debits.

**The result.** The assistant found **75 of 75 positive groups (recall 1.0)**
and is the most precise reader — F1 **0.8242** against the detector's 0.5769
and the naive rule's 0.4225. K1 (recall ≥ 0.95) and K2 (F1 within 0.05 of the
detector) both pass. The assistant is not merely adequate; it is the best of
the three readers by a wide margin.

**Why the predeclared "served" condition is not met, and why that does not
change the conclusion.** G0_C_precision failed at 0.0. F122 establishes why:
the control accounts contain real standing orders whose `k_symbol` is outside
the positive set, so the gate — which assumes controls are standing-order-free
— fails *every* reader identically (detector 0.0, naive 0.0). The gate was a
proxy for hallucination and the proxy's premise is false. The reader-validity
question the gate was meant to answer is answered on the R arm (recall 1.0)
and on the assistant's C-arm answers, all of which are real standing orders
verifiable in the committed extracts. The substantive question D107's
constraint asks — *is the answer already decidable by the incumbent?* — is
answered **yes**.

**The decision.** The recurring-payment line **closes on service**, the sixth
line to do so after E062, E091, E092, E114 and E115. E066's detector has no
unserved population: the strongest accessible reader is a free general
assistant, and it is better than the detector. The detector stays in the
repository as a correct tool, unreleased, `status: draft`, on the standing rule
that a tool with no measured unserved population is work, not a candidate.

**Relation to D107.** D107 recorded that five lines had closed on an
incumbent-served population and that the record's own named next action was
E066's merchant-name axis. This is that axis, and it closes the same way. The
pattern is now six-for-six: on every population where the mission has run the
strongest accessible alternative, the alternative has served it. The seat for
a candidate remains empty, and the reason is not a lack of trying.