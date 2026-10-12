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