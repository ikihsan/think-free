<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E143 PROTOCOL — does the value pre-pass keep its operating point on
# longer regulatory submissions a person wrote?

Written 2026-10-14, before any instrument was run on any item of the
corpus. Standard library only, deterministic, no network after the fetch.

## 0. What E142 left open, and what this run is for

E142 measured `valueset.py` (M2) on Federal Register final-rule SUMMARY
sections — 20 documents, 18 with values, all grounded — and found it
resolves 0.90 of the corpus, with **0 misses**, **0.0 false positives**,
and **1.0 detection** on the 4 genuinely unsupported SUMMARYs.

E142's named next action is one measurement:

> **The next measurement is not another genre. It is whether the pre-pass's
> exactness on regulatory text survives a longer submission — a full
> regulatory analysis or comment letter, not a SUMMARY. If it does, the
> pre-pass is a tool. If it does not, the genre limitation is deeper than
> E142 measured.**

This protocol does that. It changes one thing about the task shape, forced
by a lesson the record has already paid for:

1. **The submission is longer.** E142's SUMMARY sections are 1,000–2,000
   characters. This run uses the **SUPPLEMENTARY INFORMATION** sections of
   final rules (typically 10,000–500,000 characters), which are the agency's
   detailed explanation of the rule, written by the same staff. The
   reference remains the regulatory text (the CFR amendments).

## 1. The question, and the one that is not being asked

**Asked.** On a corpus of longer regulatory submissions written by a person
(the agency's own SUPPLEMENTARY INFORMATION section of a final rule), with
the regulatory text as the source of truth:

- does the pre-pass find a value the source does not contain, when the
  submission asserts one (**K1**);
- does it stay silent when the submission is correct (**K2**);
- and what is its **miss profile** — the share of misses that are
  `value_present` (binding errors) vs. `not_extracted` (extraction failures)?

**Not asked.** Whether a pre-pass is a faithfulness checker. E140 measured
that it is not one. Whether this is a product. Nothing in this run
establishes demand, adoption, or a distribution channel.

## 2. Population and provenance

| | |
|---|---|
| corpus | US Federal Register **final rules**, fetched from the Federal Register API v1 (`www.federalregister.gov/api/v1/documents.json`) |
| filter | `conditions[term]=final rule`, `order=newest`, 50 documents |
| fields used | `document_number`, `title`, `abstract`, `publication_date`, `raw_text_url` |
| fetched | 2026-10-14, once, and committed with digests |
| reference | the full rule text **minus the SUPPLEMENTARY INFORMATION section** (i.e., the CFR amendments, SUMMARY, DATES, etc.) |
| submission | the **SUPPLEMENTARY INFORMATION** section, written by the agency |

Every byte of the submission is human-written: the SUPPLEMENTARY INFORMATION
is drafted by the agency's own staff as a detailed explanation of the rule.
The reference is the regulatory text the submission explains.

**Disclosed before predeclaration.** The API endpoint, the filter, the field
names, and the section structure (`SUMMARY:` … `SUPPLEMENTARY INFORMATION:` …)
were read before this protocol was written, while checking that the API is
reachable and the documents have the structure the design assumes. **No
instrument was run on any item**, and no rate, coverage or verdict is known.

## 3. Task shape

- **reference** = the full rule text minus the SUPPLEMENTARY INFORMATION
  section. This includes the CFR amendments (the actual regulatory
  requirements), SUMMARY, DATES, ADDRESSES, etc.
- **submission** = the SUPPLEMENTARY INFORMATION section. This is the
  agency's detailed explanation of the rule, written by a person.

The SUPPLEMENTARY INFORMATION is supposed to be grounded in the regulatory
text. If it contains a value not in the regulatory text, that is a real
error — either the explanation misstates the rule, or it references a value
from a different document.

The pre-pass is scored one-directionally, as in E141/E142:

- `extra` = canonical values the **submission** asserts and the **reference**
  does not contain. Non-empty ⇒ **condemn**.
- `missing` = values the reference carries that the submission does not
  mention. **Not scored.** Reported as a count.

## 4. Arms, fixed before any instrument runs

| arm | definition | ground truth |
|---|---|---|
| **A** | SUPPLEMENTARY INFORMATION sections where all values are grounded in the reference | grounded |
| **B** | SUPPLEMENTARY INFORMATION sections where at least one value is not in the reference | unsupported |

**A and B are determined by the pre-pass itself.** A submission where the
pre-pass finds no `extra` is in A; a submission where it finds an `extra` is
in B. This is not circular: the pre-pass's verdict is the instrument's
output, and the arms are defined by that output. The question is whether the
verdict is *correct* — which requires an independent check.

**Independent check.** For each submission, every value it asserts is checked
against the reference by a separate, simpler test: does the canonical
rendering of the value appear in the reference text? This is `ground.py`'s
`judge()` at threshold 0.0 — a bare membership test, with no binding
requirement. A value that passes this test is grounded; a value that fails
is unsupported.

**K1's denominator is B, not all submissions.** A submission that asserts no
value cannot carry a value error, so scoring it as a miss would charge the
instrument for a population the pre-pass was never written for.

## 5. The instrument, unchanged

`EXPERIMENTS/140-judge-form-invariance/valueset.py` is imported **unchanged**,
and so is the extractor it imports, `EXPERIMENTS/114-value-grounding/ground.py`.
Neither is edited, forked, or re-tuned for this corpus.

The instrument's Federal-Register-shaped patterns — CFR and U.S.C. citations,
docket and RIN numbers — are expected to fire here, because this is the
genre they were written for. A general bare-number or hyphenated-range match
is expected to fire on things that are not values at all. **Both are
reported, not fixed.**

## 6. Baseline

M1 — `ground.py`'s own `judge()`, unchanged — on the same arms and the same
denominators. E141 measured M1's false-positive rate as 0.0940 on SQuAD,
against M2's 0.0113. E142 measured M1's false-positive rate as 0.25 on
SUMMARYs, against M2's 0.0. **What is asked here is whether that transfers**
to the longer regulatory genre.

## 7. Gates, declared before the run

| gate | declared | what a failure means |
|---|---|---|
| **K1** | `extra` non-empty on **≥ 0.95** of B | the pre-pass does not find a real agency-written value error at the rate it found on SUMMARYs |
| **K2** | `extra` empty on **≥ 0.98** of A (FP ≤ 0.02) | the pre-pass condemns correct agency-written submissions |
| **K3** | M2 extracts **≥ 1 value** from the submission on **≥ 0.30** of A | the genre does not carry a value population |
| **K4** | M2 extracts ≥ 1 value on **≥ 0.30** of A∧D and on **≥ 0.30** of B∧D | the digit-bearing subsets are value-bearing to the instrument |
| **K5** | M2 extracts ≥ 1 value on **≥ 0.30** of A∧N (conditional coverage) | the instrument sees values where the genre has them |

**Kill condition.** K3 < 0.30 ⇒ the genre does not carry a value population
and the mechanism is not disproved. K1 < 0.95 on a K4-passing arm ⇒ the
real detection rate is below the SUMMARY rate, and the pre-pass claim is
withdrawn. K2 > 0.02 ⇒ the pre-pass is not exact on this genre.

## 8. The three numbers the build decision turns on

Declared now, so they cannot be selected after the numbers are visible.

1. **Conditional coverage (K5-style).** Of SUPPLEMENTARY INFORMATION sections
   that contain a value, what fraction does the extractor see? This is the
   E141/E142 K5 number, which was 0.9379 on SQuAD and 1.0 on SUMMARYs.

2. **False-positive rate on correct items.** Of submissions where all values
   are grounded (arm A), what fraction does the pre-pass condemn? This is the
   E141/E142 K2 number, which was 0.0113 on SQuAD and 0.0 on SUMMARYs.

3. **`value_present` share of misses.** Of submissions the pre-pass clears
   but are genuinely unsupported (misses), what fraction are binding errors —
   the value is real, in the reference, but attached to the wrong subject —
   vs. extraction failures — the value is not extracted at all? This is the
   E141/E142 `explain_misses` analysis, which found 0.5830 `value_present`
   and 0.1343 `not_extracted` on SQuAD, and **0 misses** on SUMMARYs.

## 9. What this run cannot show

Declared before the run:

- **One corpus, one country, one language, one time period.** The extractor
  was written against US federal rules. A pass here is evidence about a
  mechanism, not about generality.
- **SUPPLEMENTARY INFORMATION is explanatory, not free prose.** A stakeholder
  comment letter that asserts a wrong value in a full sentence is not this
  shape and was not tested.
- **No judge, no cost model, no demand.** Nothing here is evidence of
  usefulness, differentiation or adoption.

## 10. Commands

```bash
python3 fetch.py        # fetch corpus from Federal Register API -> raw/
python3 build_arms.py   # raw/ -> arms.jsonl, splits SUPPLEMENTARY INFORMATION from reference
python3 score.py        # arms.jsonl -> gates.json, runs M2 and M1
python3 explain_misses.py  # classify misses by mechanism
python3 -m unittest test_e143  # the checks the numbers depend on
```