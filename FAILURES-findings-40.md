<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# Findings — failures and negative results, part 40

Split out of [`FAILURES-findings-39.md`](FAILURES-findings-39.md), which held
F116–F118. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are
stable across all findings files.**

## F119 — the CFR applicability-threshold population is real, mechanically diverse, and served: a free general assistant applies the counting rule on 6 of 6 cases with no clause supplied (E115)

**Date:** 2026-10-12. `EXPERIMENTS/115-applicability-thresholds/`. Protocol
declared before any regulation text was read.

### What was asked

Whether a numeric **applicability threshold** in a US federal regulation
carries a **counting rule** that changes the answer — a different numerator
(full-time, full-time equivalent, employees *on the payroll*), a different
window (*each working day of 20+ workweeks*, *peak employment during the last
calendar year*), or a different unit (NAICS industry code, 75-mile worksite)
— and whether a free general assistant gets it wrong.

This is not a hunt for an unserved need. It is a test of one mechanical
property of a task already performed, on real facts, with real consequences:
an OSHA penalty, an ACA penalty, a plan that should have been filed.

### What the population measurement found (M1)

CFR title 29 as of 2026-01-01, fetched unauthenticated from the eCFR
versioner API. **328 parts, 7,145 sections, 328 requests, ~30 MB.**
**81 applicability threshold spans across 60 sections**, each with its
citation and ±220 characters of context, committed as
`parts-title29.jsonl`. K1 (≥ 0.10 divergent) passed at **0.185**.

The divergences are real and quoted. FMLA coverage (§ 825.104(a)) is *"50 or
more employees for each working day during each of 20 or more calendar
workweeks in the current or preceding calendar year"* — so a company at 60 in
one week and 8 for the rest of two years is **not** covered, and § 825.111
adds a 75-mile worksite test. OSHA recordkeeping (§ 1904.1(a)(1)) turns on
*"10 or fewer employees at all times during the last calendar year"*, i.e.
**peak-ever employment, company-wide**, with a second independent exemption in
§ 1904.2 keyed to NAICS code. **In all of these the headcount and the answer
point in opposite directions, and in § 1904.1 the divergence is about the
past.**

**The extractor's precision on the rows it flagged is 11 of 15**, and both
artifact shapes are recorded: `\b` matching inside *"1,000 or more"*, and
*"salaries less than employees at the GS-11, step 1"* matching a threshold
vocabulary. This is **E064/E089's shape on a second population** — a cheap
text matcher produces candidates, and the candidate set needs a checker.

**A protocol gate was itself wrong and is recorded as corrected.** K2 declared
`extraction_coverage < 0.50` as a kill and the harvest reported 0.0084. That
statistic is the fraction of *all* sections labelled, and most CFR sections
contain no applicability threshold at all, so a low value is the expected
shape of a **correct** extractor. Reporting it as a coverage failure would
have been F116's error — a statistic that cannot fail standing in for one that
can.

### What the discriminating arm found (M2, M2b, null control)

14 fact patterns whose correct answer is **computable by hand from the rule
text**, keyed and committed at `ab5f9de8` **before any answer existed**. Every
key cites a clause. Selection was not by difficulty: four cases a naive
headcount also gets right are included on purpose, and `P7b` was added *after*
re-reading § 825.111(a)(1) because the first draft contradicted it.

| arm | given | overall | **counting-rule subset (6)** |
|---|---|---|---|
| M2 | verbatim deciding clause + facts | **14/14 = 1.0000**, CI95 [0.7847, 1.0000] | **6/6** |
| M2b | **facts only, no clause, no citation** | **14/14 = 1.0000**, CI95 [0.7847, 1.0000] | **6/6** |
| null control | the plain-headcount reading | 6/14 = 0.4286, CI95 [0.2138, 0.6741] | **0/6** |

**Kill gate 0.95 met in both treatment arms; the line closes.** The control
is what makes the two 14/14 rows mean something: the scorer fires, the key is
not satisfiable by a plausible wrong answer, and the separation is in the
direction predicted before any arm ran. `test_score.py` pins this (6 tests,
including that the null arm scores 0 on the subset and that the key cannot
drift from the committed Markdown).

### A pre-registered prediction that was wrong, in the hypothesis's favour

`M2-CASES.md` predicted the naive reading gets **8 of 14 right and 6 wrong**,
listing P2, P4, P6, P8, P10, P7b. **The control scored 6 right and 8 wrong** —
it also missed **P5** (paid or unpaid, both count) and **P7** (the other site's
headcount is not subtracted). Both are genuine counting-rule divergences I did
not enumerate. The error is in the prediction, not the key, and it runs
*against* the hypothesis: **there are 8 divergences, not 6.** Recorded because
a pre-registered number quietly dropped is F052's shape.

### The ceiling, unrepaired

**Both treatment arms are one reader, and that reader had already read §
825.104, § 825.105, § 825.111, § 1904.1, § 1904.2 and § 1910.38 in full during
M1.** So this cannot separate *"a free general assistant applies CFR counting
rules"* from *"this particular assistant, having read these six sections
minutes ago, applies them"*. `M2B-AMENDMENT.md` was written **before** M2b ran,
declared M2's number an upper bound on service rather than a measurement of
it, and named this as the defect the ablation does **not** repair. Repairing it
needs an arm that has not seen the harvest, which one session cannot produce.

### What this adds to the record

This is the **fifth consecutive real, measurable population found to be served
by a free general assistant**: E062 (17/20), E091 (5/20, vendor-bound
composition), E092 (30/37 = 0.81), E114 (0 of 374 values fabricated), E115
(6/6 counting-rule cases, 14/14 overall). **On this mission's evidence "served"
is the modal outcome and finding an unserved population is the hard part**, not
the default — and E115 adds the mechanism by which it stays closed: the hard
sub-problem is *finding* the counting rule, and removing the clause from the
prompt (M2b) did not change the answer.

### What is left, honestly labelled

The harvest stands and is reusable: 81 spans with citations and context, an
unauthenticated fetch recipe, and a measured extractor precision with both
artifact shapes named. **Neither is a candidate.** 81 spans in one title is not
a product, and the finding that the incumbent serves them is the reason.

Two leads, **neither measured**: (1) the population is not one thing — § 1904.2
applies per establishment while § 1904.1 applies company-wide, so "do I keep
records" is a **conjunction** of a part-level and an establishment-level test,
and M2 tested them separately; (2) these thresholds **change** — § 1904.1
carries `[85 FR 8731, Feb. 18, 2020]` against `[66 FR 6122, Jan. 19, 2001]` —
and telling a user their *current* exemption is a different question from
applicability. See [`EXPERIMENTS/115-applicability-thresholds/M2.md`](EXPERIMENTS/115-applicability-thresholds/M2.md),
D107.