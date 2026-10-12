<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E115 — does a regulation's applicability threshold carry a counting rule the incumbent gets wrong?

Declared 2026-10-12, before any regulation text was read and before the
extractor was written. Nothing below may be edited after the first rule text
is read, except by an amendment file that names what it changed and why.

**Already done before this file was written, and declared here rather than
hidden:** one `GET /api/versioner/v1/structure/2026-01-01/title-29.json`
(2,473,607 bytes) to confirm the eCFR API is reachable and to size the
harvest, and three HTTP status checks on dol.gov and irs.gov. **No
regulation text was read**, no threshold was seen, and no fact pattern was
chosen.

## Why this population, and why not another instrument audit

E062, E091, E092 and E114 all closed because a free general assistant served
the population. The record's own conclusion is that **serving is the default
outcome** and an unserved population must be argued for, not assumed. So this
experiment does not look for an unserved need. It looks at a task that is
**already being performed, on real facts, with real consequences**, and asks
whether one specific mechanical property of the answer is wrong.

## The practical difficulty, stated concretely

US federal regulations bind conditionally on a number. Title 29 alone carries
rules that apply only to employers with "20 or more employees", only to plans
with "100 or more participants", only to manufacturers with "10 or more
full-time employees". A small employer asking "does this apply to me?" must
answer **three** questions, not one:

1. **Does a rule with a threshold apply to me at all?** — a search question.
2. **What is the numerator?** — headcount, *full-time* headcount,
   *full-time equivalent*, participants excluding certain roles, including
   certain roles.
3. **Over what window?** — "at any time in the last 12 months", "in the
   preceding 20 workweeks", "on the last day of the prior calendar year",
   or no window at all.

The threshold is the easy half and it is the half a keyword search returns.
The **counting rule** is the half that changes the answer. "40 employees,
20 of them full-time, against a 25-full-time threshold" is YES on headcount and
NO on the rule. A wrong answer here is an OSHA penalty, an ACA penalty, or a
plan that should have been filed.

## The question, stated as one number

When a free general assistant is given a real CFR rule verbatim and a real
fact pattern, **what fraction of its applicability answers apply that rule's
counting rule correctly?**

## Three measurements, in order, each able to stop the next

**M1 — does the population exist and is it mechanically diverse?** Harvest
every applicability threshold in one title with a declared extraction rule.
Report three numbers, not one:

| quantity | why it decides |
|---|---|
| `thresholds_found` | if ~0, the population is a fiction and E115 stops here |
| `counting_rule_divergent` | fraction whose numerator or window is *not* plain headcount-at-a-moment. **If this is small, there is no tool, because plain headcount is what every incumbent already computes.** |
| `extraction_coverage` | fraction of the title's candidate sections the extractor labelled at all (E113's lesson: a screen over 28% of rows was recorded as a 100% measurement) |

**M2 — is the incumbent wrong, on real cases?** The discriminating arm.
Population: fact patterns whose correct answer is **computable by hand from
the rule text alone**, before the assistant is asked. No judgement call
qualifies a row. The assistant is given the rule verbatim and the facts, and
answers yes/no. A disagreement with the hand-computed answer is counted.
Declared kill gate: **if the assistant is correct on ≥ 0.95 of rows, the
population is served and the line closes** — that is the E062/E092/E114
outcome and it is the expected one.

**M3 — is the error one mechanical kind?** Only if M2 fails its gate. If the
errors are scattered across kinds, there is no tool; if they are one kind
(the assistant silently substituting headcount for a stated numerator, or
dropping a stated window), a deterministic checker is possible and worth
building. **M3 does not run if M2 passes.**

## The strongest accessible alternative

Not the assistant alone. The incumbent workflow is **someone reads the rule**,
and a **keyword search of the CFR for the threshold**. M2 therefore records
what a plain text search returns for each fact pattern, because a tool must
beat the thing people already do, not the thing people complain about.

## Kill gates, declared before measurement

- **K1.** `counting_rule_divergent` < 0.10 of found thresholds → no
  population; record and move to a different opportunity.
- **K2.** `extraction_coverage` < 0.50 → the extractor does not see its
  population, so nothing downstream may be reported as a measurement. This is
  F116's exact shape and the fix is to report coverage on every row.
- **K3.** assistant correctness ≥ 0.95 on M2 → line closed as served.
- **K4.** M3 errors not concentrated in one mechanical kind → no tool.

## Ceilings, declared up front

- One title. The CFR's threshold style is not uniform across titles and a
  result here is a statement about this title.
- Rules are read as published on one date, with no account of amendment.
- M2's correct answer is **hand-computed by this agent**. That is a single
  reader with no second coder, which this repository has been burned by
  before (F049). Every hand computation is committed *before* the assistant
  answers, so the reference cannot be fitted to the treatment.
- A free general assistant's availability and wording drift between sessions;
  the exact prompts are committed with the answers.