# Decisions — screening candidates and judging experiments, part 6

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

Decisions **D063, D064**. Split from [`DECISIONS-SCREENING-5.md`](DECISIONS-SCREENING-5.md)
at its cap. Read [`DECISIONS.md`](DECISIONS.md) for the index. **Identifiers are stable
across the parts.**

## D063 — A label is read as a set of literals, and a rate over one literal is a floor (2026-10-06)

**Decision.** Any rate computed over an enumerated field — a platform's
`closed_reason`, a status column, a triage bucket — names the **literal set** it counts,
not the concept it means, and reports the count of the literals it deliberately excludes
beside the rate. A concept reading ("closed as a duplicate") is a declared union of
literals, and the primary figure is the **exact** literal so the declared rate is a floor.

**Where it comes from.** E034 (`EXPERIMENTS/034-reask-tail/`) declared the label as
`closed_reason == "Duplicate"` and the run returned **ten** distinct literals over
2514 rows. `Duplicate` is 222 rows. **`exact duplicate` is 9 rows of the same moderation
act under a legacy spelling**, and the declared label excluded it; including it moves the
pooled tail rate from 0.1352 to 0.1462. Five more literals are lowercase legacy spellings
of closures the platform now names in title case (`off topic`, `not a real question`,
`not constructive`, `too localized`), so **the normalisation problem is a direction, not
one row.**

**The same fact was already published and missed.** E033 reported 0.0540 across "5
distinct reasons", which is the same shape at smaller scale: a reason *count* was read as
a reason *set*. **E033's 0.0540 is a floor, and F055's tertile table built on it is a
floor too.** Neither is refuted by this; both are stated higher than the bytes support,
which is the defect.

**The second half of the decision, which is the load-bearing one.** A field that is
**absent** must be shown to mean "does not apply" rather than "not recorded", or the
denominator is not the population it claims. E034's substitution gate is that **no row is
closed without stating a reason**: `closed_reason` was absent on all 1790 open rows and
present on every one of the 724 closed rows, 0 exceptions. **A key-presence rule declared
against an API that omits the key on inapplicable rows is a gate that fires on the
API's normal behaviour** — E034's declared A1 said "100% of rows carry the key" and it
was unsatisfiable; the substitution was declared in the gate table and disclosed, which
is what a declared-but-wrong gate is supposed to cost.

**Consequence.** Every enumeration-based rate in this record is re-readable as a floor.
`tools/origin`'s own gates do not depend on this, and no committed result changes.

**Ceiling.** It says nothing about *meaning* — `Duplicate` and `exact duplicate` being the
same act is a judgement, not a measurement, and a platform that renamed a literal for a
different reason would be miscounted by this rule. It also does not make floors useful:
a floor still bounds the rate from below and cannot support a claim of the form "at most".

## D064 — A decision rule over a relation between candidates must be an exclusive partition, and a threshold over one pair is not one (2026-10-06)

**Decision.** When a gate is a predicate about how one candidate relates to **several**
others — disjoint from A, disjoint from B, better than C — it is declared either as an
**exclusive partition** (each data shape routes to exactly one branch) or as a
**statistic over the whole relation** (a density, a count, a range). It is never declared
as a single conjunction or disjunction over a subset of comparators.

**Where it comes from.** E034's AMENDMENT-1 declared R2 as *"R2-tag: `baggage`'s tail
CI95 is disjoint from **both** math tags"* against *"R2-site: it **overlaps a** math
tag"*. The data gave `baggage` disjoint from `probability` and `linear-algebra` and
overlapping `calculus`. **Both branches were true**, and the gate therefore could not
decide anything while appearing to. It was declared before the fetch, which is the only
reason the defect is cheap: the fix was written down in advance too, as D6 — the fraction
of **within-site** tag pairs that separate at all, against the cross-site fraction — and
that statistic answers a question the binary form could not.

D6's answer was that within-site pairs separate **4/10** of the time against **14/26**
cross-site, so **site and tag both carry real variance and three to five tags per site
cannot apportion them.** F057.

**Relation to D062.** D062 governs a *linkage rule* — the relation an instrument builds
between candidates — and requires it to be shown capable of firing. This governs the
*decision rule applied to a relation between candidates*, one level up, and the failure
is the mirror: a rule that fires on **every** shape. D062's rule could not fire; this one
could fire twice.

**Consequence.** F057's per-tag reading is `not_established`, and the run's kill gate
A4 — which fired, on the numbers — is recorded as not sufficient for the claim it was
gated on. Any future per-tag or per-community reading must declare its comparators as a
partition or count over the relation before the fetch.

**Ceiling.** It is a rule about how a *declared gate* is written, and it says nothing
about whether within-site disjointness would have been a good statistic. D6 is a proxy
for "the site does not determine the tag", chosen because it is unambiguous and cheap; a
variance decomposition with three or four tags per site would be the better instrument and
is exactly what F057 names as the next action.
