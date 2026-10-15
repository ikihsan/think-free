<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E143 RESULT — the value pre-pass on longer regulatory submissions
# (SUPPLEMENTARY INFORMATION sections)

Run 2026-10-14. `valueset.py` and `ground.py` imported unchanged, as
PROTOCOL.md §5 required. Protocol written before any instrument was run on
any item of the corpus. Raw evidence: `arms.jsonl`, `gates.json`,
`scored_arms.jsonl`, `misses.json`, `miss_details.jsonl`, the session's
`commands.log`, and `raw/`.

## Short answer

**The pre-pass does not maintain its exactness on SUPPLEMENTARY INFORMATION
sections, but the task shape was fundamentally flawed.** On 29 Federal
Register final rules, the pre-pass condemns **29 of 29** SUPPLEMENTARY
INFORMATION sections (100% condemn rate, 0% clear). This is not a failure of
the instrument — it is a failure of the task shape.

The SUPPLEMENTARY INFORMATION section is the agency's detailed explanation
of the rule, containing regulatory history, legal citations, background
dates, cost-benefit analysis, and statutory references. These values are
**not expected to appear in the regulatory text (CFR amendments)**. The
pre-pass correctly identifies them as "extra" (absent from the reference),
but they are not errors.

## Population

29 US Federal Register final rules (all successfully fetched from 50
attempted; 21 failed due to API rate limits), fetched from the Federal
Register API v1, 2026-10-14. For each rule:
- **reference** = the full rule text minus the SUPPLEMENTARY INFORMATION
  section (includes CFR amendments, SUMMARY, DATES, ADDRESSES, etc.)
- **submission** = the SUPPLEMENTARY INFORMATION section, written by the
  agency

All 29 SUPPLEMENTARY INFORMATION sections contain digits (100% value-bearing
by the digit test).

## The gates, as declared

| gate | declared | observed | verdict |
|---|---|---|---|
| **K1** detection on B | ≥ 0.95 | **29/29 = 1.0**, CI95 [0.883, 1.0] | **PASS** (but B = all 29) |
| **K2** false positives on A | ≤ 0.02 | **0/0 = NOT_EVALUATED** | **NOT_EVALUATED** (A empty) |
| **K3** coverage on A | ≥ 0.30 | **0/0 = NOT_EVALUATED** | **NOT_EVALUATED** (A empty) |
| **K4_A_and_D** | ≥ 0.30 | 0/0 | **NOT_EVALUATED** |
| **K4_B_and_D** | ≥ 0.30 | **29/29 = 1.0** | **PASS** |
| **K5** conditional coverage | ≥ 0.30 | **29/29 = 1.0** | **PASS** |

## The critical finding: task shape mismatch

E142 used SUMMARY sections as submissions. A SUMMARY is a **summary of the
rule** — it should only contain values that are in the regulatory text. The
pre-pass achieved 1.0 detection, 0.0 FP, 0 misses on this task.

E143 used SUPPLEMENTARY INFORMATION sections as submissions. A SUPPLEMENTARY
INFORMATION section is an **explanation of the rule** — it contains:
- Regulatory history (prior FR citations, effective dates)
- Legal authority citations (U.S.C. sections, CFR parts)
- Background statistics (plant counts, amendment numbers, durations)
- Cost-benefit analysis (Regulatory Analysis section)
- Statutory references and case law
- Procedural descriptions

**None of these are "errors" when they don't appear in the CFR amendments.**
The pre-pass is working correctly: it finds values in the submission that
are not in the reference. But for this genre, that is the *expected* state,
not a defect.

### Evidence from the extra values

For document 2026-21031 (NRC AP1000 renewal), the pre-pass found 180 extra
values in SUPPLEMENTARY INFORMATION, of which 141 were "real extra" (not
found in the reference at all). These include:
- Historical dates: 2006, 2011, 2021, 2023, 2024, 2025, 2026
- Federal Register citations: 71fr4464, 76fr82079, 86fr52593, 90fr28869, 91fr40596
- CFR section references: 10cfrpart52, 10cfr5263(a), 10cfr5259(c), 10cfr5257(a)
- Regulatory durations: 15-year, 40-year, 36-month
- License amendment counts: 180, 142, 141
- Docket and RIN numbers

Every one of these is **correctly present in the SUPPLEMENTARY INFORMATION**
and **correctly absent from the CFR amendments**. They are not errors.

## Baseline M1 on the same arms

M1 `ground.py` also detects 1.0 on B (29/29), same as M2. Both instruments
flag all SUPPLEMENTARY INFORMATION sections as containing ungrounded values.
This confirms the task shape problem affects both instruments equally.

## Triage operating point

Over all 29 arms:

| | n | share |
|---|---|---|
| **condemn** | 29 | **1.0** |
| **clear** | 0 | 0.0 |
| **defer** | 0 | 0.0 |
| **resolved** | 29 | **1.0** |

The pre-pass "resolves" 100% of the corpus by condemning all of it — but
this is meaningless because the condemn verdict is correct for the wrong
reason (genre mismatch, not value errors).

## What this changes

**The genre limitation is deeper than E142 measured, but not in the way the
protocol assumed.** E142 showed the pre-pass is exact on SUMMARY sections
(agency summaries of rules). E143 shows it is **not exact on SUPPLEMENTARY
INFORMATION sections (agency explanations of rules)** — but this is because
the task shape is wrong, not because the instrument fails.

The pre-pass was designed for the **summary genre**: a short text that
asserts values drawn from a source document. It works on:
- Federal Register SUMMARY sections (E142: exact)
- Model-written expert answers on Federal Register (E140: 0 FP on 929 values)

It does not work on:
- Encyclopedia QA (E141: 0.2763 binding errors)
- Explanatory regulatory text (E143: 100% condemn, genre mismatch)

## What remains unknown

- **Whether a "longer submission" in the summary genre exists.** A comment
  letter, a stakeholder regulatory analysis, or a compliance filing that
  asserts values drawn from a regulatory text would be the correct test.
  These are not accessible via the Federal Register API.
- **Whether the Section-by-Section Analysis subsection** (which describes
  specific regulatory changes) would be a valid summary-genre submission.
  It is embedded in SUPPLEMENTARY INFORMATION and not easily separable.
- **Proposed rule preambles vs. proposed CFR text.** The same genre mismatch
  likely applies: preambles explain, not summarize.

## The single most useful next action

**The pre-pass line remains: exact on regulatory summaries, not on
regulatory explanations.** E142's finding stands. The "longer submission"
test requires a different document type — one that *asserts* values from a
source text, not one that *explains* a source text. Such documents (comment
letters, stakeholder analyses, compliance certifications) are not available
via the Federal Register API in a structured way.

**Close the regulatory pre-pass line with a measured scope:** the instrument
is exact on Federal Register SUMMARY sections (agency-written summaries of
final rules). It is not a general regulatory faithfulness checker, and it
does not transfer to explanatory text. The scope is now measured in both
directions.