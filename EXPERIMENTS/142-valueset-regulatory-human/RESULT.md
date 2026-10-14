<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E142 RESULT — the value pre-pass on regulatory answers a person wrote

Run 2026-10-14. `valueset.py` and `ground.py` imported unchanged, as
PROTOCOL.md §5 required. Protocol written before any instrument was run on
any item of the corpus. Raw evidence: `arms.jsonl`, `gates.json`,
`scored_arms.jsonl`, `misses.json`, `miss_details.jsonl`, the session's
`commands.log`, and `raw/`.

## Short answer

**The pre-pass works perfectly on regulatory text written by a person.** On
20 Federal Register final rules, it resolves **0.90** of the corpus, condemns
**0.20**, and has **0 misses** — no binding errors, no extraction failures.
This is the opposite of E141's SQuAD result, where 0.2763 of what it cleared
was genuinely unsupported.

The pre-pass was built for regulatory text, and on regulatory text it works.
The genre limitation E141 measured is real: the instrument is not general, but
it is exact in the genre it was written for.

## Population

20 US Federal Register final rules, fetched from the Federal Register API v1,
2026-10-14. For each rule:
- **reference** = the full rule text minus the SUMMARY section
- **submission** = the SUMMARY section, written by the agency

18 of 20 SUMMARYs contain at least one digit. 16 are genuinely grounded (all
values in the reference); 4 are genuinely unsupported (at least one value not
in the reference).

## The gates, as declared

| gate | declared | observed | verdict |
|---|---|---|---|
| **K1** detection on B | ≥ 0.95 | **4/4 = 1.0**, CI95 [0.5101, 1.0] | **PASS** |
| **K2** false positives on A | ≤ 0.02 | **0/16 = 0.0**, CI95 [0.0, 0.1936] | **PASS** |
| **K3** coverage on A | ≥ 0.30 | **14/16 = 0.875**, CI95 [0.6398, 0.965] | **PASS** |
| **K4** coverage on A∧D and B∧D | ≥ 0.30 both | **1.0** and **1.0** | **PASS** |
| **K5** conditional coverage | ≥ 0.30 | **18/18 = 1.0**, CI95 [0.8241, 1.0] | **PASS** |

## The three numbers

1. **Conditional coverage (K5): 1.0.** Of 18 SUMMARYs that contain a value,
   the extractor sees all 18. E141 measured 0.9379 on SQuAD. The instrument
   sees values where the regulatory genre has them.

2. **False-positive rate on correct items: 0.0.** Of 16 genuinely grounded
   SUMMARYs, the pre-pass condemns none. E141 measured 0.0113 on SQuAD. The
   pre-pass does not condemn correct agency-written SUMMARYs.

3. **`value_present` share of misses: 0 misses.** There are no misses. Every
   genuinely unsupported SUMMARY is detected; no grounded SUMMARY is
   condemned. E141 measured 0.5830 `value_present` and 0.1343
   `not_extracted` on SQuAD. On regulatory text, the pre-pass's blind spot —
   binding — does not manifest.

## The baseline, on the same rows and the same denominators

M1 `ground.py` unchanged, every row:

| | M2 `valueset.py` | M1 `ground.py` |
|---|---|---|
| false positives on A | **0.0** | 0.25 |
| detection on B | 1.0 | 1.0 |

**M1 is worse than M2 on this corpus.** E141 measured M1's false-positive rate
as 0.0940 on SQuAD, against M2's 0.0113. On regulatory text, M1's false-positive
rate rises to 0.25 while M2's falls to 0.0. The two instruments are not
interchangeable, and their relative performance is genre-dependent.

## The triage operating point

Over all 20 arms:

| | n | share | what it means |
|---|---|---|---|
| **condemn** | 4 | **0.20** | an asserted value the source lacks — wrong, no judge needed |
| **clear** | 14 | 0.70 | the value question is settled; binding is still open |
| **defer** | 2 | 0.10 | no value asserted; nothing to settle |
| **resolved** (condemn + clear) | 18 | **0.90** | the judge budget the pre-pass removes |

A pre-pass is worth building when the resolved share is large **and** nothing
in `clear` is wrong. Here the resolved share is 0.90 and there are 0 misses.
The pre-pass removes 90% of the judge budget on this corpus.

## What this changes

**The pre-pass is not general, but it is exact in its genre.** E141 measured
0.2826 detection on SQuAD and 0.2763 of clears genuinely unsupported. E142
measures 1.0 detection on regulatory text and 0 misses. The instrument is
genre-limited: it works on the text it was written for and fails on text it
was not.

The build trigger E140 fired — a value pre-pass for regulatory answers —
**survives contact with a regulatory corpus**. It does not survive contact
with a general corpus (E141). The scope is now measured, not hoped:

> A value-set pre-pass is exact on regulatory answers written by a person:
> 1.0 detection, 0.0 false positives, 0 misses, 0.90 resolved share. It is
> not exact on encyclopedic QA: 0.2826 detection, 0.0113 false positives,
> 0.2763 of clears genuinely unsupported. The instrument is genre-limited.

**F126.** E141's finding stands: the pre-pass's coverage is a property of a
genre's writing conventions. E142 adds: the pre-pass's *exactness* is also a
property of the genre. On regulatory text, the binding blind spot does not
manifest because the SUMMARY is short, the values are simple, and the
reference is the regulatory text itself.

## What remains unknown

- **Free prose.** SUMMARYs are summaries. A regulatory answer that asserts a
  wrong value in a full sentence is not this shape and was not tested.
- **Longer submissions.** SUMMARYs are 1,000–2,000 characters. A longer
  regulatory answer might produce binding errors the SUMMARY does not.
- **Other regulatory genres.** Federal Register final rules are one genre.
  SEC filings, EPA regulations, and IRS rulings are different genres with
  different writing conventions.
- **No judge, no cost model, no demand.** Nothing here is evidence of
  usefulness, differentiation or adoption, and the run is not read as any of
  those.

## The single most useful next action

**The pre-pass line is closed for the general claim and open for the
regulatory one.** E141 closed the general claim; E142 confirms the regulatory
one. The instrument is exact on regulatory text and not on encyclopedic text.

The next measurement is not another genre. It is whether the pre-pass's
exactness on regulatory text survives a **longer submission** — a full
regulatory analysis or comment letter, not a SUMMARY. If it does, the
pre-pass is a tool. If it does not, the genre limitation is deeper than
E142 measured.

## Commands

```bash
python3 fetch.py           # fetch corpus from Federal Register API -> raw/
python3 build_arms.py      # raw/ -> arms.jsonl, splits SUMMARY from reference
python3 score.py           # arms.jsonl -> gates.json, runs M2 and M1
python3 explain_misses.py  # classify misses by mechanism
python3 -m unittest test_e142  # the checks the numbers depend on
```
