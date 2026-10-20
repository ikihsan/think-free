<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E182 AMENDMENT 2 — residualise against the question, once, against the same bar

**Declared 2026-10-18, after `overlap.py` rejected the instrument and before
the run that tests it.** Commit this file first.

## 1. What the calibration showed

AMENDMENT 1 §4 rule 1 fitted τ on the hand-read rows and rule 2 accepted the
instrument at balanced accuracy ≥ 0.80. The run returned **0.6500** —
sensitivity 0.8000, specificity **0.5000**, confusion `(tp,fp,tn,fn) =
(4,2,2,1)`, τ = 0.67 — so **the instrument is rejected and G2 is
`not_evaluated`** by the pre-declared rule. Specificity at exactly chance means
the threshold is not tracking the construct at all on the `same` side.

The nine calibration rows, sorted by measured overlap:

| qid | overlap | tokens P0 / P1 | truth | predicted | |
|---|---|---|---|---|---|
| 79843062 | 0.0000 | 8 / 1 | differ | differ | ✓ |
| 79589468 | 0.1250 | 10 / 48 | same | differ | ✗ |
| 79796450 | 0.4286 | 13 / 14 | same | differ | ✗ |
| 79824381 | 0.4643 | 54 / 28 | differ | differ | ✓ |
| 79556333 | 0.6364 | 66 / 11 | differ | differ | ✓ |
| 79408101 | 0.6667 | 29 / 3 | differ | differ | ✓ |
| 79600161 | 0.6923 | 24 / 13 | same | same | ✓ |
| 79663905 | 0.7143 | 127 / 14 | same | same | ✓ |
| 79791886 | 0.9091 | 26 / 11 | differ | same | ✗ |

## 2. The failure is one mechanism, not three mistakes

Every error is the same error, and it is diagnosable from the token counts:

- **79589468** — the runner-up carries **48** tokens against the top's 10. It
  is a long warning answer quoting the question's own type names
  (`uint32_t`, `uint64_t`). Its prescriptions are diluted by the problem's
  vocabulary.
- **79796450** — both answers name the same C++ library, so shared symbols
  (`std`, `views`, `zip`, `MyData`) inflate the numerator even though the
  prescriptions differ.
- **79791886** — both answers name `rand`, `RAND_MAX`, `sqrt`, `R`. Ten of the
  runner-up's eleven tokens are the *problem's* tokens. A high overlap here
  means both answers are discussing the same program, not proposing the same
  fix.

**Shared problem vocabulary is being counted as shared prescription.** That is
a defect in the construct, stated in one sentence, and it is fixable without
touching τ or the acceptance bar.

## 3. The repair

> **`P_residual(A) = P(A) \ P(question)`**

A token the question already contains cannot be a prescription *of a fix* — it
is the reporter's own vocabulary. Residualising both sides removes the
confound the three errors share and nothing else changes:

- τ is still fitted on the same 9 hand-read rows, maximising balanced accuracy.
- The acceptance bar is **unchanged: balanced accuracy ≥ 0.80**.
- The calibration rows are still excluded from G2.
- Eligibility is unchanged: ≥ 2 answers, runner-up score > 0, runner-up
  residual token set non-empty.

**This is the last attempt, declared as such.** If the residualised instrument
is also rejected, the conclusion is not "try a third thing": the disagreement
explanation of F136's gap is reported **`untested`, with two instruments and
two declared rejections as the reason**, and E181's named next action retires
as *not executable with the instruments this mission has* — which is itself a
result, and a much better one than a closure produced by an instrument that
did not measure its construct.

A second structural fact is already measured and is not a threshold problem:
**`qid 79537353` is ineligible because its runner-up contains no prescriptive
tokens at all.** That is a conceptual C-standards question with no fix to
prescribe, so the construct does not exist on the row. 16 of 60 rows are
`single_answer` and 2 are `runner_up_not_positive`, so **the instrument can
address at most 42 of 60 rows of this population** however well it is built —
`untested` on a third of the population regardless of outcome, which is the
ceiling this whole line carries.

## 4. What G2' would decide, restated

If accepted, G2' keeps the original bar — Fisher exact two-sided, `p < 0.05`
**and** difference ≥ 0.20, EVID missed against EVID hit, calibration rows
excluded:

- **fires** → the EVID gap is substantially a disagreement about resolutions.
  No context pipeline closes it, consistent with E181's two nulls, and the
  ground-truth-quality direction becomes live enough to earn a prior-art
  screen.
- **does not fire** → resolutions are *not* differentially divergent on missed
  rows, which closes the last explanation F136's gap has left and closes the
  EVID line as a genuine reasoning deficit.
- **instrument rejected** → `untested`, as above.