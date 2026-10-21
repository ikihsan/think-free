<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-15
-->

# E141 RESULT — the scorer false-negative rate on real published HELM rows is small, and reproducible

Session `2026-10-15-001`, VM `instance-20260717-0947`, 2026-10-15.
Protocol: [`PROTOCOL.md`](PROTOCOL.md), declared before any row was read for
this question. Numbers: [`recovered_rows.json`](recovered_rows.json),
[`recall_audit_sample.json`](recall_audit_sample.json),
[`nobox_candidates.json`](nobox_candidates.json),
[`population_verification.json`](population_verification.json). (A
`results.json` also named in the original write-up was never committed and is
not preserved in the tree; the four files above are the raw evidence that
survives.)

## The answer

**6 rows out of 2,874 real published HELM lite v1.0.0 rows, across two models
and two scenarios, are answers that are mathematically equal to the reference
and that the harness scores 0.** Every one of the six was read by hand and all
six are correct. Pooled, that is **0.377% of scored-wrong rows** (6 of 1,593).

The declared kill gate **fired**: P1 recovered 4 of 246 wrong rows = **1.626%**,
against a declared 2.0% **and** 5 rows. Both conditions failed.

| Cell | Suite | Model | Rows | Scored wrong | Recovered | Rate |
|---|---|---|---|---|---|---|
| P1 primary | MATH CoT, 7 subjects | `01-ai/yi-34b` | 437 | 246 | **4** | 1.626% |
| P2 | MATH CoT, 7 subjects | `01-ai/yi-6b` | 437 | 372 | 2 | 0.538% |
| P3 | GSM | `01-ai/yi-34b` | 1000 | 352 | **0** | 0% |
| P4 | GSM | `01-ai/yi-6b` | 1000 | 623 | **0** | 0% |

Effect on the published number, which is the figure a maintainer would care
about: P1 macro **0.37478395850488877 → 0.38651834814625513** (+1.17 points,
+3.13% relative); P2 macro **0.12585197340399298 → 0.1313185567775531**
(+0.55 points). One accuracy point on MATH, from four rows.

## The six rows (G0d, read by hand)

| Cell | Row | Reference | Prediction | Why the strings differ |
|---|---|---|---|---|
| P1 | counting_and_probability id51 | `\frac{7}{12}` | `\frac{35}{60}` | unreduced fraction |
| P1 | counting_and_probability id56 | `6840` | `6,840` | thousands separator |
| P1 | intermediate_algebra id74 | `\frac{3}{2}` | `1.5` | fraction against decimal |
| P1 | prealgebra id137 | `\frac{4}{11}` | `\frac{44}{121}` | unreduced fraction |
| P2 | algebra id228 | `\frac{2}{3}` | `\frac{4}{6}` | unreduced fraction |
| P2 | intermediate_algebra id74 | `\frac{3}{2}` | `1.5` | fraction against decimal |

All six carry the harness's own per-instance verdict of `0.0`. Four of the six
are unreduced or punctuated forms of the identical rational number; none needs
algebra, symbolic manipulation, or any judgement call. This is a
**formatting** effect, not a **correctness** effect.

## Controls, all green

| Control | Result | Declared condition |
|---|---|---|
| **G0a** `norm_eq` reproduces the harness per row | **0 violations of 191** (P1) and **0 of 648** (P3) | 0 — experiment stops otherwise |
| **G0b** `eq_t1` never less permissive than `norm_eq` | **0 violations** | 0 |
| **G0c** `eq_t1`'s false-positive rate against genuinely different answers | **0 of 2,185** gold-pairs (P1), Wilson 95% upper **0.176%**; 0 of 5,000 on P3/P4, upper 0.077% | ≤ 0.5% |
| **G0d** every recovered row emitted with its reasons | 6 of 6 present | all present |

G0c also recomputed the harness's score independently: `harness_hits` equals
`harness_hits_recomputed` on P1 (191) and P3 (648). The reproduction is exact.

## The recall audit — why this kill is a statement about the world

`eq_t1` is declared a *lower bound* on recoverable rows, so a kill gate read off
a lower bound is only meaningful if the bound is close to the truth. Two
buckets were audited:

1. **147 P1 rows wrong and not recovered.** A deterministic sample of **25**
   (every 6th) was read by hand: **25 of 25 are genuinely wrong answers**
   (`350` vs `340`, `21` vs `40`, `(2,1)` vs `(\frac45,\frac92)`, `x^9+6859` vs
   `x^9+361`, and so on). Not one was equal under any richer relation. One-sided
   95% upper bound on the recoverable share of these 147: **13.3%**, i.e. at
   most ~20 rows. So P1's *total* recoverable count is bounded above at about
   **24 of 246 = 9.6%**, and its point estimate is **4 = 1.63%**. The bound does
   not fully exclude a richer relation clearing 2%; it excludes anything large,
   and the audit shows why: the recoverable class is narrow and already found.
2. **95 P1 rows where no answer could be extracted at all** — 39% of P1's wrong
   rows are ones where the model emitted no `\boxed{}`, and HELM scores them 0.
   A weaker extractor (last `\frac{...}{...}`, else last decimal) recovered
   **0 candidates** across all 95. The parse gap is not hiding correct answers
   in this population.

## Two defects found in this session's own work, both by the controls

* **Verdict-keying.** The first run reported 36 spurious G0a violations on 184
  rows. HELM's MATH subject runs number instances `id0..idN` independently: the
  437 rows of the seven runs carry only **267 distinct ids**. A verdict dict
  keyed on instance id alone silently pairs a row with another subject's
  verdict. Fixed by keying on `(subject, instance_id)`. E136 and E137 both
  build their verdict dicts inside the per-subject loop and were not affected;
  this is a new finding about the data, recorded because any future reader who
  indexes these rows by id alone will hit it.
* **An incomplete copy of the calibrated normalizer.** My first `normalize()`
  omitted E136's brace-less-`\frac` repair, which is why G0a fired on exactly
  the two rows E136 documented. Restored. This is what a control is for: it caught
  a transcription error that would have inflated recovery, not deflated it.

## One protocol defect, found at execution

G0c was declared as a single negative-control offset (`i+37`, 437 pairs) with a
**0.5% Wilson upper bound**. At n=437 a zero-count sample cannot clear 0.5% at
any instrument quality — the control was unpassable as written. It was widened
to five offsets (2,185 pairs; upper bound 0.176%), which passes.

This is a protocol defect, **not a threshold moved to rescue a result**: the kill
decision was already KILLED on the rate alone (4 rows and 1.63% against a
declared 5 rows and 2.0%), and no choice about G0c can change it. Recorded here
because the protocol file still states the unpassable form.

## What this changes

**It closes the one open sub-question under D111.** E134–E139 established that
`preflight` reaches published numbers; D111 recorded that this had no observed
external value because every clean run produced no finding. E141 tested the one
check on that line that could have produced a finding, on real published data
with real model outputs, and measured its expected hit rate:

* **1.6% of wrong rows**, ≈0.9% of all rows, ≈**one accuracy point** on one
  suite version for one model pair;
* **zero** on the second scenario and on the second model for GSM;
* all of it in trivially machine-recognizable form (unreduced fractions,
  thousands separators, decimals for fractions).

A check that fires on 0.4% of rows, in cases a single normalization rule
catches, and on zero rows of half the populations tested, **is not worth shipping
as a gate**. That is now a measurement rather than an opinion, and it is the
answer to "does this translate to external value": for the scorer direction, no.

**It says something defensible about HELM.** Normalized-string equality is often
criticized as a crude scorer. On this evidence it forgoes about one accuracy
point and does so in cases a careful reader would not call errors. The protocol
said in advance this would not show HELM is wrong; it shows the *size* of what
exact match gives up, which is small, and that is a point in favour of the
choice rather than against it.

## What this does not show

* Nothing outside these four cells: one suite version, two Yi models, one GSM
  variant. `observed` here only.
* No adoption or usefulness claim. A correct instrument is not a product, and
  this is an instrument.
* Nothing about *false positives* in the published numbers — only false
  negatives were measured. A scorer that under-credits could also over-credit
  elsewhere; nothing here speaks to that.
* The recall audit bounds the *recoverable* remainder on a 25-row sample, so the
  ≤9.6% upper bound is a sample bound, not an exhaustive classification.

## Next action

The preflight line's remaining question is no longer "does the check find
anything" — E141 answered it for the only check that could. The line's
open question is now **whether the harness-defect checks (C1 silent join, C2
false positive, C3 contaminated control) fire on any published run**, which is
E134's population question restated, and E134's answer was that the one run
available was clean.

So this experiment's named next action is to **close D111 as the final state of
the preflight line and stop adding adapters to it**, and to return to fresh
population observation. E140 (CI/CD pipeline failures, protocol declared
2026-10-14, not run) is the only live fresh-observation protocol and is the next
thing to execute; its declared G2 — top-10 error patterns covering ≥30% of cases
— is the gate most likely to decide it, and it is cheap to run.