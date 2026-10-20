<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E143 RESULT — the value pre-pass on longer regulatory submissions
# (preamble vs CFR amendments)

Run 2026-10-14. `valueset.py` and `ground.py` imported unchanged, as
PROTOCOL.md §5 required. Protocol written before any instrument was run on
any item of the corpus. Raw evidence: `arms.jsonl`, `gates.json`,
`misses.json`, `documents_with_hashes.json`, the session's `commands.log`,
and `raw/`.

## Short answer

**The pre-pass's exactness on regulatory SUMMARYs does NOT extend to longer
preambles.** On 11 Federal Register final rules where the preamble/
SUPPLEMENTARY INFORMATION section was used as submission and the CFR
amendments as reference, the pre-pass **condemns every single preamble**
(11/11 = 1.0). The preamble contains numerous values from supporting
documents (regulatory analyses, environmental assessments, safety
evaluations) that are not in the CFR amendments themselves.

This is the opposite of E142's SUMMARY result (1.0 detection, 0.0 FP,
0 misses, 0.90 resolved). The instrument is not just genre-limited
(regulatory vs encyclopedic) — it is **section-limited** within the
regulatory genre: it works on the SUMMARY but fails on the SUPPLEMENTARY
INFORMATION.

## Population

11 US Federal Register final rules (of 20 fetched), 2026-10-14, where the
"List of Subjects" or "PART" boundary was found. For each rule:

- **reference** = the CFR amendments only (from "List of Subjects" /
  "PART XX--" through end of document)
- **submission** = the preamble (everything before the CFR amendments:
  SUMMARY, DATES, ADDRESSES, FOR FURTHER INFORMATION CONTACT,
  SUPPLEMENTARY INFORMATION)

9 of 20 fetched rules lacked a detectable "List of Subjects" / "PART"
boundary and were excluded.

All 11 preambles contain at least one digit (value-bearing).

## The gates, as declared

| gate | declared | observed | verdict |
|---|---|---|---|
| **K1** detection on B | ≥ 0.95 | **11/11 = 1.0** | **PASS** |
| **K2** false positives on A | ≤ 0.02 | **0/0 = 0.0** (no A arms) | **PASS** (vacuous) |
| **K3** coverage on A | ≥ 0.30 | **0/11 = 0.0** | **FAIL** |
| **K4** coverage on A∧D and B∧D | ≥ 0.30 both | **0.0** and **1.0** | **FAIL** |
| **K5** conditional coverage | ≥ 0.30 | **0.0** (no A arms) | **FAIL** |

## The three numbers

1. **Conditional coverage (K5): 0.0.** There are **zero** preambles where
   all extracted values are grounded in the CFR amendments (arm A).
   Every preamble contains values from supporting documents not in the
   CFR text. E142 measured 1.0 on SUMMARYs.

2. **False-positive rate on correct items: vacuous (0/0).** There are no
   preambles where all values are grounded in the CFR amendments, so K2
   cannot be meaningfully evaluated. E142 measured 0.0 on SUMMARYs.

3. **Miss profile: not applicable (0 misses).** There are no misses
   because there are no A arms. The pre-pass doesn't *miss* ungrounded
   values — it *finds* them in every preamble (11/11 condemned).

## The baseline, on the same rows and the same denominators

M1 `ground.py` unchanged, every row:

| | M2 `valueset.py` | M1 `ground.py` |
|---|---|---|
| false positives on A | **0.0** (vacuous) | 0.0 (vacuous) |
| detection on B | 1.0 | 1.0 |

Both instruments condemn every preamble. The pre-pass's advantage on
SUMMARYs (M2: 0.0 FP vs M1: 0.25 FP) disappears on preambles because
**both instruments flag values from supporting documents**.

## The triage operating point

Over all 11 arms:

| | n | share | what it means |
|---|---|---|---|
| **condemn** | 11 | **1.0** | an asserted value the CFR amendments lack |
| **clear** | 0 | 0.0 | the value question is settled |
| **defer** | 0 | 0.0 | no value asserted |
| **resolved** (condemn + clear) | 11 | **1.0** | the judge budget the pre-pass removes |

The pre-pass resolves 100% of the corpus — but **every resolution is a
condemnation**. On SUMMARYs (E142), the resolved share was 0.90 with
0.70 clear and 0.20 condemn. On preambles, the clear share collapses to
0.0.

## Why the pre-pass condemns every preamble

The SUPPLEMENTARY INFORMATION section contains detailed discussion of:
- Regulatory analyses (cost-benefit, regulatory flexibility)
- Environmental assessments (NEPA analyses)
- Safety evaluations (final safety evaluation reports)
- Background information (prior rules, license amendments, design changes)
- Statutory authorities (U.S.C. citations, executive orders)
- Public comment summaries

These sections cite dollar amounts, dates, percentages, quantities, and
citations from **supporting documents** that are referenced but not
reproduced in the CFR amendments. Examples from the corpus:

- Cost estimates from regulatory analyses ($ millions)
- Radiation dose estimates from environmental assessments (mrem/year)
- Accident probabilities from safety evaluations (per reactor-year)
- Effective dates from prior rules (historical dates)
- Docket numbers, RIN numbers, CFR citations from the rulemaking record

The pre-pass correctly identifies that these values are not in the CFR
amendments. But they are not "errors" — they are correctly grounded in
the rulemaking record, just not in the regulatory text itself.

## What this changes

**The pre-pass is not just genre-limited (regulatory vs encyclopedic) —
it is section-limited within the regulatory genre.** It works on the
SUMMARY (agency's concise summary of the rule) but fails on the
SUPPLEMENTARY INFORMATION (agency's detailed analysis and justification).

The scope is now measured more precisely:

> A value-set pre-pass is exact on regulatory **SUMMARYs** written by a
> person: 1.0 detection, 0.0 false positives, 0 misses, 0.90 resolved
> share. It is **not** exact on regulatory **preambles/SUPPLEMENTARY
> INFORMATION**: 1.0 condemnation rate, 0.0 clear rate, because preambles
> cite values from supporting documents not in the CFR amendments. The
> instrument is section-limited.

**F145 (extended).** E141 showed the pre-pass's coverage is a property of
a genre's writing conventions. E142 showed its exactness is also
genre-dependent. E143 adds: **its exactness is section-dependent within a
genre.** The SUMMARY and SUPPLEMENTARY INFORMATION are both
agency-written regulatory text, but they have different value-grounding
conventions: the SUMMARY only summarizes what is in the rule text; the
SUPPLEMENTARY INFORMATION discusses the entire rulemaking record.

## What remains unknown

- **Practitioner-written documents.** Comment letters, regulatory
  analyses by regulated entities, and compliance documents are not tested.
  These might have different value-grounding conventions.
- **Other regulatory genres.** Federal Register final rules are one
  genre. SEC filings, EPA regulations, IRS rulings, and state-level
  regulations have different structures.
- **A pre-pass with a broader reference.** If the reference included the
  full rulemaking docket (supporting documents), the pre-pass might work
  on preambles. This is a different instrument design.
- **No judge, no cost model, no demand.** Nothing here is evidence of
  usefulness, differentiation or adoption.

## The single most useful next action

**The pre-pass line is closed for general use, closed for regulatory
preambles, and open only for regulatory SUMMARYs.** E141 closed the
general claim; E142 confirmed the regulatory SUMMARY claim; E143 closes
the regulatory preamble claim.

The instrument is a **SUMMARY-only tool**. It could be used to verify
that an agency's SUMMARY accurately reflects the rule text — but the
agency already writes the SUMMARY, so the use case is unclear.

If a product is desired, the next step would be to test on
**practitioner-written regulatory comment letters** (the actual use case
for value verification), using the proposed rule as reference. This
requires access to regulations.gov comment data (API key needed).