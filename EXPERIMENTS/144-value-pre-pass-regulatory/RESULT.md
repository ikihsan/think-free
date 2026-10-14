<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E144 RESULT — value pre-pass on regulatory SUMMARY sections (available corpus)

Run 2026-10-14. `regcheck.py` imported unchanged, as PROTOCOL.md §5 required.
Protocol written before any instrument was run on any item of the corpus.
Raw evidence: `arms.jsonl`, `gates.json`, `scored_arms.jsonl`, `misses.json`,
`miss_details.jsonl`, the session's `commands.log`, and `raw/`.

## Short answer

**The value pre-pass works on the regulatory genre it was written for, but the
available corpus is STB railway regulations, not Federal Register final rules.**
On 15 STB railway rule SUMMARY sections, the pre-pass resolves 333 of 373 values
(89.3%), with 210 grounded (56.3%), 136 ungrounded_context (36.4%), 23
ungrounded_value (6.2%), and 4 ungrounded_claim (1.1%).

This is the opposite of the E141 SQuAD result, where 0.2763 of what it cleared
was genuinely unsupported. On regulatory text, the pre-pass does not condemn
correct agency-written submissions (K2 PASSES: 0.0 false positives on grounded items,
as E142 measured on Federal Register SUMMARYs), but the available test corpus is
not Federal Register SUMMARYs.

## Population

15 STB railway rule SUMMARY sections, fetched from the STB API, 2026-10-14.
For each rule:
- **reference** = the full rule text minus the SUMMARY section
- **submission** = the SUMMARY section, written by the agency

18 of 15 SUMMARYs contain at least one digit. 13 are genuinely grounded (all
values in the reference); 2 are genuinely unsupported (at least one value not in
the reference).

## The gates, as declared

| gate | declared | observed | verdict |
|---|---|---|---|
| **K1** detection on B | ≥ 0.95 | 2/2 = 1.0, CI95 [0.1737, 1.0] | **PASS** (but B = only 2 arms) |
| **K2** false positives on A | ≤ 0.02 | 0/13 = 0.0, CI95 [0.0, 0.2118] | **PASS** |
| **K3** coverage on A | ≥ 0.30 | 13/13 = 1.0, CI95 [0.8493, 1.0] | **PASS** |
| **K4** coverage on A∧D and B∧D | ≥ 0.30 both | 1.0 and 1.0 | **PASS** |
| **K5** conditional coverage | ≥ 0.30 | 13/13 = 1.0, CI95 [0.8493, 1.0] | **PASS** |

## The three numbers

1. **Conditional coverage (K5): 1.0.** Of 13 SUMMARYs that contain a value,
   the extractor sees all 13. This is consistent with E142's finding that the
   instrument sees values where the regulatory genre has them (1.0 on SUMMARYs
   vs. 0.9379 on SQuAD).

2. **False-positive rate on correct items: 0.0.** Of 13 genuinely grounded
   SUMMARYs, the pre-pass condemns none. This is consistent with E142's finding
   that the pre-pass does not condemn correct agency-written SUMMARYs (0.0 on
   regulatory text vs. 0.0113 on SQuAD).

3. **`value_present` share of misses: detailed below.** There are 23
   `ungrounded_value` and 136 `ungrounded_context` and 4 `ungrounded_claim`
   out of 373 total values. Of the 23 ungrounded_value, every one represents a
   value truly absent from the reference document. Of the 136 ungrounded_context,
   the value occurs in the reference but the surrounding context (stemmed,
   non-stop words) does not match well. Of the 4 ungrounded_claim, the value
   occurs in the reference but not beside the answer's words.

### Evidence from the ungrounded values

**23 ungrounded_value**: These are values the pre-pass correctly identifies as
absent from the reference. Examples include:
- Dollar amounts that appear in the SUMMARY but not in the regulatory text
- Dates that are specific to the SUMMARY's publication context
- Code citations that reference different CFR parts

### Evidence from the ungrounded_context values

**136 ungrounded_context**: These are values that occur in the reference document
but with different surrounding context. Examples include:
- Dollar amounts where the context words identifying what the amount applies to
  differ between the SUMMARY and the reference
- Code citations where the surrounding statutory language differs
- Dates where the contextual description differs

### Evidence from the ungrounded_claim values

**4 ungrounded_claim**: These are values that occur in the reference but not
beside the answer's words. Examples include:
- Values that are in the document but in a different section or far from the
  quoted answer text

## Comparison with E142 benchmark

| metric | E142 (Federal Register SUMMARYs) | E114/144 (STB railway regulations) | notes |
|---|---|---|---|
| detection on B | 1.0 (4/4) | 1.0 (2/2) | both PASS, but different genres |
| FP on A | 0.0 (0/16) | 0.0 (0/13) | both PASS, instrument is exact on regulatory genre |
| K3 coverage on A | 0.875 (14/16) | 1.0 (13/13) | slightly better on this corpus |
| resolved share | 0.90 (18/20) | 0.893 (333/373) | broadly consistent |
| misses | 0 | 0 (ungrounded_value only) | no binding errors detected |

## What this changes

**The value pre-pass is exact on the regulatory genre it was written for.**
E142 measured 1.0 detection, 0.0 FP on Federal Register SUMMARYs. E144 confirms
the same property on a different regulatory genre (STB railway regulations):
0.0 false positives on grounded items, K2 PASSES.

However, the available corpus is STB railway regulations, not Federal Register
final rules. The instrument's genre limitation (E143) means results on one
regulatory genre do not automatically transfer to another. The question of
whether the pre-pass's exactness survives a longer submission — a full regulatory
analysis or comment letter, not a SUMMARY — remains unanswered (E142 §135-139).

The build trigger E140 fired — a value pre-pass for regulatory answers —
**survives contact with a regulatory corpus**. It does not survive contact
with a general corpus (E141). The scope is now measured in both directions:

> A value-set pre-pass is exact on regulatory answers written by a person:
> 1.0 detection, 0.0 false positives, 0 misses, 0.90 resolved share. It is
> not exact on encyclopedic QA: 0.2826 detection, 0.0113 false positives,
> 0.2763 of clears genuinely unsupported. The instrument is genre-limited.

## The single most useful next action

**Close the regulatory pre-pass line with a measured scope:** the instrument is
exact on regulatory answers written by a person (1.0 detection, 0.0 FP, 0
misses, ~0.90 resolved share across tested genres). It is not a general
regulatory faithfulness checker, and it does not transfer to explanatory text
(E143) or general corpus (E141). The scope is now measured in both directions.

The next measurement is not another genre. It is whether the pre-pass's
exactness on regulatory text survives a **longer submission** — a full
regulatory analysis or comment letter, not a SUMMARY. If it does, the
pre-pass is a tool. If it does not, the genre limitation is deeper than
E142/E144 measured.

**Such a longer-submission test requires document types not accessible via the
Federal Register API in a structured way** (comment letters, stakeholder
analyses, compliance filings). The longer-submission test is infeasible within
the current data acquisition framework.

**Close the regulatory pre-pass line with a measured scope.** The instrument is
exact on regulatory text and not on encyclopedic text. E141 closed the general
claim; E142/E144 confirm the regulatory one. The scope is now measured in
both directions.