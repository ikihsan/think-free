<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E144 PROTOCOL — value pre-pass on Federal Register SUMMARY sections

## Question

On Federal Register final-rule SUMMARY sections written by a person, with the full rule text minus SUMMARY as the source of truth:
- does the value pre-pass (ground.py + valueset.py M2) find a value the source does not contain, when the submission asserts one (K1)?
- does it stay silent when the submission is correct (K2)?
- what is its miss profile — the share of misses that are `value_present` (binding errors) vs. `not_extracted` (extraction failures)?

## Population

US Federal Register final rules, fetched from the Federal Register API. For each rule:
- **reference** = the full rule text minus the SUMMARY section (CFR amendments, DATES, ADDRESSES, etc.)
- **submission** = the SUMMARY section, written by the agency

Standard library only, deterministic, no network after the fetch.

## Task shape

- **reference** = full rule text minus SUMMARY section
- **submission** = SUMMARY section

The pre-pass is scored one-directionaly, as in E141/E142:

- `extra` = canonical values the **submission** asserts and the **reference** does not contain. Non-empty ⇒ **condemn**.
- `missing` = values the reference carries that the submission does not mention. **Not scored.** Reported as a count.

## Arms, fixed before any instrument runs

| arm | definition | ground truth |
|---|---|---|
| **A** | SUMMARY sections where all values are grounded in the reference | grounded |
| **B** | SUMMARY sections where at least one value is not in the reference | unsupported |

A and B are determined by the pre-pass itself. The question is whether the verdict is *correct* — which requires an independent check.

Independent check. For each submission, every value it asserts is checked against the reference by a separate, simpler test: does the canonical rendering of the value appear in the reference text? This is `ground.py`'s `judge()` at threshold 0.0 — a bare membership test, with no binding requirement. A value that passes this test is grounded; a value that fails is unsupported.

## Arms, declared before any instrument runs

| arm | definition |
|---|---|
| **A** | SUPPLEMENTARY INFORMATION sections where all values are grounded in the reference | grounded |
| **B** | SUPPLEMENTARY INFORMATION sections where at least one value is not in the reference | unsupported |

**A and B are determined by the pre-pass itself.** A submission where the pre-pass finds no `extra` is in A; a submission where it finds an `extra` is in B. This is not circular: the pre-pass's verdict is the instrument's output, and the arms are defined by that output. The question is whether the verdict is *correct* — which requires an independent check.

**Independent check.** For each submission, every value it asserts is checked against the reference by a separate, simpler test: does the canonical rendering of the value appear in the reference text? This is `ground.py`'s `judge()` at threshold 0.0 — a bare membership test, with no binding requirement. A value that passes this test is grounded; a value that fails is unsupported.

## Gates, declared before the run

| gate | declared | what a failure means |
|---|---|---|
| **K1** | `extra` non-empty on **≥ 0.95** of B | the pre-pass does not find a real agency-written value error at the rate it found on SUMMARYs |
| **K2** | `extra` empty on **≥ 0.98** of A (FP ≤ 0.02) | the pre-pass condemns correct agency-written SUMMARYs |
| **K3** | M2 extracts **≥ 1 value** from the submission on **≥ 0.30** of A | the genre does not carry a value population |
| **K4** | M2 extracts ≥ 1 value on **≥ 0.30** of A∧D and on **≥ 0.30** of B∧D | the digit-bearing subsets are value-bearing to the instrument |
| **K5** | M2 extracts ≥ 1 value on **≥ 0.30** of A∧N (conditional coverage) | the instrument sees values where the genre has them |

**Kill condition.** K3 < 0.30 ⇒ the genre does not carry a value population and the mechanism is not disproved. K1 < 0.95 on a K4-passing arm ⇒ the real detection rate is below the SUMMARY rate, and the pre-pass claim is withdrawn. K2 > 0.02 ⇒ the pre-pass is not exact on this genre.

## The three numbers the build decision turns on

1. **Conditional coverage (K5-style).** Of SUMMARY sections that contain a value, what fraction does the extractor see? This is the E141/E142 K5 number, which was 0.9379 on SQuAD and 1.0 on SUMMARYs.

2. **False-positive rate on correct items.** Of submissions where all values are grounded (arm A), what fraction does the pre-pass condemn? This is the E141/E142 K2 number, which was 0.0113 on SQuAD and 0.0 on SUMMARYs.

3. **`value_present` share of misses.** Of submissions the pre-pass clears but are genuinely unsupported (misses), what fraction are binding errors — the value is real, in the reference, but attached to the wrong subject — vs. extraction failures — the value is not extracted at all? This is the E141/E142 `explain_misses` analysis, which found 0.5830 `value_present` and 0.1343 `not_extracted` on SQuAD, and **0 misses** on SUMMARYs.

## What this run cannot show

- **One corpus, one country, one language, one time period.** The extractor was written against US federal rules. A pass here is evidence about a mechanism, not about generality.
- **Free prose.** SUMMARYs are summaries. A regulatory answer that asserts a wrong value in a full sentence is not this shape and was not tested.
- **Longer submissions.** SUMMARYs are 1,000–2,000 characters. A longer regulatory answer might produce binding errors the SUMMARY does not.
- **Other regulatory genres.** Federal Register final rules are one genre. SEC filings, EPA regulations, and IRS rulings are different genres with different writing conventions.
- **No judge, no cost model, no demand.** Nothing here is evidence of usefulness, differentiation or adoption, and the run is not read as any of those.

## Commands

```bash
python3 fetch.py              # fetch corpus from Federal Register API -> raw/
python3 build_arms.py         # raw/ -> arms.jsonl, splits SUMMARY from reference
python3 score.py              # arms.jsonl -> gates.json, runs M2 and M1
python3 explain_misses.py     # classify misses by mechanism
python3 -m unittest test_e144 # the checks the numbers depend on
```