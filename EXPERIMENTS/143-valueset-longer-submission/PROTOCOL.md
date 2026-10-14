<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E143 PROTOCOL — does the value pre-pass keep its exactness on
# longer regulatory submissions (preamble vs CFR amendments)?

Written 2026-10-14, before any instrument was run on any item of the
corpus. Standard library only, deterministic, no network after the fetch.

## 0. What E142 left open, and what this run is for

E142 measured `valueset.py` (M2) on 20 Federal Register final rules, using
the agency-written SUMMARY (1,000–2,000 characters) as submission and the
full rule text minus SUMMARY as reference. It found **1.0 detection, 0.0
false positives, 0 misses, 0.90 resolved share**. The pre-pass is exact on
SUMMARYs.

E142's named next action is one measurement:

> The next measurement is not another genre. It is whether the pre-pass's
> exactness on regulatory text survives a **longer submission** — a full
> regulatory analysis or comment letter, not a SUMMARY. If it does, the
> pre-pass is a tool. If it does not, the genre limitation is deeper than
> E142 measured.

This protocol tests the pre-pass on the **preamble** (SUPPLEMENTARY
INFORMATION and other explanatory sections) of final rules, using the
**actual CFR amendments** as the reference. The preamble is 10–50× longer
than the SUMMARY and contains detailed discussion, background, analysis, and
justification — the kind of text a practitioner might write in a regulatory
comment or analysis.

## 1. The question, and the one that is not being asked

**Asked.** On a corpus of final rules where the submission is the **entire
preamble** (everything before the CFR amendments) and the reference is the
**CFR amendments only** (the regulatory text that actually changes the Code
of Federal Regulations):

- does the pre-pass find a value the CFR amendments do not contain, when the
  preamble asserts one (**K1**);
- does it stay silent when the preamble's values are all in the CFR
  amendments (**K2**);
- and what is its **miss profile** — the share of misses that are
  `value_present` (binding errors) vs. `not_extracted` (extraction failures)?

**Not asked.** Whether a pre-pass is a faithfulness checker. E140 measured
that it is not one. Whether this is a product. Nothing in this run
establishes demand, adoption, or a distribution channel.

## 2. Population and provenance

| | |
|---|---|
| corpus | US Federal Register **final rules**, fetched from the Federal Register API v1 (`www.federalregister.gov/api/v1/documents.json`) |
| filter | `conditions[term]=final rule`, `order=newest`, 20 documents |
| fields used | `document_number`, `title`, `abstract`, `publication_date`, `raw_text_url` |
| fetched | 2026-10-14, once, and committed with digests |
| reference | the **CFR amendments only** — the regulatory text starting from "List of Subjects" or "PART" through the end |
| submission | the **preamble** — everything before the CFR amendments (SUMMARY, DATES, ADDRESSES, CONTACT, SUPPLEMENTARY INFORMATION) |

Every byte of the submission is human-written: the preamble is drafted by
the agency's staff as a detailed explanation of the rule. The reference is
the regulatory text the preamble explains.

**Disclosed before predeclaration.** The API endpoint, the filter, the field
names, and the document structure (preamble vs CFR amendments separated by
"List of Subjects") were read before this protocol was written, while
checking that the API is reachable and the documents have the structure the
design assumes. **No instrument was run on any item**, and no rate, coverage
or verdict is known.

## 3. Task shape

- **reference** = the CFR amendments only. This is the regulatory text that
  actually changes the Code of Federal Regulations: the "List of Subjects"
  line, the "PART X--" header, and all subsequent amendatory instructions.
- **submission** = the preamble. This is the agency's detailed explanation
  of the rule, including SUMMARY, DATES, ADDRESSES, FOR FURTHER INFORMATION
  CONTACT, and SUPPLEMENTARY INFORMATION.

The preamble is supposed to be grounded in the CFR amendments (and
supporting documents). If the preamble contains a value not in the CFR
amendments, that may be a real error — or it may be a value grounded in a
supporting document (safety evaluation, environmental assessment, regulatory
analysis) that is not part of the CFR amendments. The pre-pass cannot
distinguish these cases; it only checks membership in the reference text.

The pre-pass is scored one-directionally, as in E141/E142:

- `extra` = canonical values the **submission** asserts and the **reference**
  does not contain. Non-empty ⇒ **condemn**.
- `missing` = values the reference carries that the submission does not
  mention. **Not scored.** Reported as a count.

## 4. Arms, fixed before any instrument runs

| arm | definition | ground truth |
|---|---|---|
| **A** | preambles where all extracted values are grounded in the CFR amendments | grounded |
| **B** | preambles where at least one extracted value is not in the CFR amendments | unsupported |

**A and B are determined by the pre-pass itself.** A preamble where the
pre-pass finds no `extra` is in A; a preamble where it finds an `extra` is
in B. The question is whether the verdict is *correct* — which requires an
independent check.

**Independent check.** For each preamble, every value it asserts is checked
against the CFR amendments by a separate, simpler test: does the canonical
rendering of the value appear in the CFR amendments text? This is
`ground.py`'s `judge()` at threshold 0.0 — a bare membership test, with no
binding requirement. A value that passes this test is grounded; a value that
fails is unsupported.

**K1's denominator is B, not all preambles.** A preamble that asserts no
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
denominators. E142 measured M1's false-positive rate as 0.25 on regulatory
SUMMARYs, against M2's 0.0. **What is asked here is whether that transfers**
to the preamble genre.

## 7. Gates, declared before the run

| gate | declared | what a failure means |
|---|---|---|
| **K1** | `extra` non-empty on **≥ 0.95** of B | the pre-pass does not find a real preamble value error at the rate it found on SUMMARYs |
| **K2** | `extra` empty on **≥ 0.98** of A (FP ≤ 0.02) | the pre-pass condemns correct preambles |
| **K3** | M2 extracts **≥ 1 value** from the submission on **≥ 0.30** of A | the genre does not carry a value population |
| **K4** | M2 extracts ≥ 1 value on **≥ 0.30** of A∧D and on **≥ 0.30** of B∧D | the digit-bearing subsets are value-bearing to the instrument |
| **K5** | M2 extracts ≥ 1 value on **≥ 0.30** of A∧N (conditional coverage) | the instrument sees values where the genre has them |

**Kill condition.** K3 < 0.30 ⇒ the genre does not carry a value population
and the mechanism is not disproved. K1 < 0.95 on a K4-passing arm ⇒ the
real detection rate is below the SUMMARY rate, and the pre-pass's exactness
claim for longer submissions is withdrawn.

## 8. The three numbers the build decision turns on

Declared now, so they cannot be selected after the numbers are visible.

1. **Conditional coverage (K5-style).** Of preambles that contain a value,
   what fraction does the extractor see? This is the E142 K5 number, which
   was 1.0 on SUMMARYs.

2. **False-positive rate on correct items.** Of preambles where all values
   are grounded in the CFR amendments (arm A), what fraction does the
   pre-pass condemn? This is the E142 K2 number, which was 0.0 on SUMMARYs.

3. **`value_present` share of misses.** Of preambles the pre-pass clears but
   are genuinely unsupported (misses), what fraction are binding errors —
   the value is real, in the CFR amendments, but attached to the wrong
   subject — vs. extraction failures — the value is not extracted at all?
   This is the E141/E142 `explain_misses` analysis. On SUMMARYs, E142 found
   0 misses total. On SQuAD, E141 found 0.5830 `value_present` and 0.1343
   `not_extracted`.

## 9. What this run cannot show

Declared before the run:

- **One corpus, one country, one language, one time period.** The extractor
  was written against US federal rules. A pass here is evidence about a
  mechanism, not about generality.
- **The preamble is agency-written, not practitioner-written.** A regulatory
  comment letter that asserts a wrong value in a full sentence is not this
  shape and was not tested.
- **The reference is only the CFR amendments.** Values grounded in
  supporting documents (safety evaluations, environmental assessments,
  regulatory analyses) will appear as `extra` even if they are correct in
  context. This is a known limitation of the one-reference design.
- **No judge, no cost model, no demand.** Nothing here is evidence of
  usefulness, differentiation or adoption.

## 10. Commands

```bash
python3 fetch.py        # fetch corpus from Federal Register API -> raw/
python3 build_arms.py   # raw/ -> arms.jsonl, splits preamble from CFR amendments
python3 score.py        # arms.jsonl -> gates.json, runs M2 and M1
python3 explain_misses.py  # classify misses by mechanism
python3 -m unittest test_e143  # the checks the numbers depend on
```