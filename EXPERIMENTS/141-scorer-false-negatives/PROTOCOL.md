<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-15
-->

# E141 — Do published exact-match scores under-credit correct answers?

Session `2026-10-15-001`, VM `instance-20260717-0947`, declared 2026-10-15,
before any row of the population was read for this question.

## The question

E136 found, while calibrating its recomputation, that HELM's MATH scorer is
normalized-**string** equality: it scores `1.5` against `3/2` as 0. It removed a
numeric-equivalence operator from its own instrument to match the harness, and
recorded the case in `RESULT.md`. E138 then asserted "352 mismatches are genuine
model errors" for GSM. Neither statement measured the thing that matters: **how
many rows the harness scores wrong are in fact correct.**

That is the measurement this experiment makes. It is the one thing the preflight
line has never produced. E134–E139 established four exact agreements between an
independent recomputation and published numbers, and D111 records why that is
still not value: on every clean run the tool found nothing. This experiment
asks whether `preflight`'s question has a non-empty answer anywhere, using the
population the line already fetched and hash-verified.

## Claim under test

> Among rows a published benchmark scores **incorrect**, a non-trivial share are
> answers mathematically equal to the reference but not equal to it as strings.
> If so, the published number understates the model by a measurable amount, and
> the rows are recoverable without a human in the loop.

## Populations (all already on disk, none fetched for this question)

| Cell | Suite | Model | Rows | Path |
|---|---|---|---|---|
| **P1 primary** | MATH chain-of-thought, 7 subject runs | `01-ai/yi-34b` | 437 | `/tmp/opencode/e136/math__math:subject=*__scenario_state.json` |
| P2 | same, 7 subject runs | `01-ai/yi-6b` | 437 | `/tmp/opencode/e137/math__math:subject=*__scenario_state.json` |
| P3 | GSM | `01-ai/yi-34b` | 1000 | `/tmp/opencode/e136/gsm__scenario_state_yi34b.json` |
| P4 | GSM | `01-ai/yi-6b` | 1000 | `/tmp/opencode/e137/gsm__scenario_state.json` |

P1 is the primary cell because E135/E136 named it the protocol's primary cell and
because it is the largest population with a single declared recovery rule applied
to symbolic answers. P2 and P3/P4 are declared in advance as replication and as a
contrast; neither can rescue or kill the primary cell.

**Provenance.** P1 and P3 verify against
`EXPERIMENTS/136-leaderboard-free-text-aggregate/fetched-manifest.json`; P2 and P4
against `EXPERIMENTS/137-leaderboard-cross-model-agreement/fetched-manifest.json`.
`verify_population.py` re-hashes every file before any measurement and exits 3 on
a mismatch. Note the cache trap found on 2026-10-15: E137 re-fetched GSM into the
paths E136 had recorded for `yi-34b`, so `/tmp/opencode/e136/gsm__*.json` now
holds `yi-6b` bytes and only the `_yi34b` copies match the E136 manifest. P3 is
therefore the `_yi34b` file, and `verify_population.py` fails loudly if that
inversion is reintroduced.

## The two operators

`norm_eq` is E136's calibrated reproduction of the harness's own rule:
normalized-string equality on the last `\boxed{...}` of the completion and of the
reference tagged `correct`. It reads no verdict column. E136 reproduced 437/437
per-instance verdicts and the published macro to full printed precision on P1.

`eq_t1` is a strictly-more-permissive relation, defined in advance:

1. `norm_eq(a, b)` — inherits the harness's operator; or
2. **exact rational equality.** Reduce both normalized answers under
   `fractions.Fraction` arithmetic, where the expression is a well-formed rational
   over decimal/integer literals, `+ - * /`, parentheses, and exponentiation by a
   non-negative integer. Anything else — variables, roots, matrices, tuples, unit
   text, `^` with a negative exponent, any subexpression that would need a float —
   makes the row **unrecoverable**, not equal. Exactness is arithmetic, not
   numeric: `0.333` does not equal `1/3`.

`eq_t2` (reported, **not** counted toward the gate) is `eq_t1` or float agreement
within declared relative tolerance 1e-9. T2 exists so the tier is visible rather
than silently folded in or dropped.

**Soundness bias.** The relation refuses anything it cannot prove equal. That
makes the recovery count a lower bound on the recoverable set, which is the right
direction for a claim that under-crediting is material and the wrong direction for
a claim that it is bounded. Both directions are stated in the result.

## Controls, declared before measurement

| Id | Control | Pass condition |
|---|---|---|
| **G0a** | `norm_eq` reproduces the harness per row: for every row the harness scored 1.0, `norm_eq` is True | 0 violations. Any violation means the operator is not reproduced and **the experiment stops** |
| **G0b** | `eq_t1` is never *less* permissive than `norm_eq` | 0 violations. A violation is a bug in `eq_t1` and **the experiment stops** |
| **G0c** | `eq_t1`'s false-positive rate against genuinely different answers: pair each row's gold with the gold of row `(i+37) mod n` within the same subject run | Wilson 95% upper bound ≤ **0.5%** |
| **G0d** | Every recovered row is emitted with its gold, its prediction, and the specific rule that recovered it, for reading by hand | all recovered rows present in `recovered_rows.json` |

G0a is the sharpest of these and is not a formality: it is the claim that this
experiment's reference operator still matches the shipped verdicts, tested per row
rather than on the aggregate. If G0a fails, the recovery set is meaningless.

The per-instance verdict files are read **only** for G0a reconciliation and are
never an input to `eq_t1`, to the recovery count, or to any threshold. This is
E136's R1 discipline carried forward.

## Kill gate (declared before measurement)

On **P1 only**:

* **recovery rate ≥ 2.0%** of harness-scored-wrong rows, **and**
* **≥ 5 recovered rows**,

⇒ the direction survives to a build decision. Both conditions, because a
percentage of a small wrong-row count and an absolute count of a large one are
the same thing wearing different clothes.

* otherwise ⇒ the product direction is killed and the number is kept as a bound
  on under-crediting for this suite, version and model pair.

0.5% is chosen against this repository's own precedent for a gate (F113: a 1%
rate did not justify a CI gate) and set **lower** than it, because the artefact
here is a published-number review rather than a per-commit gate, and because the
population is every published math score rather than one repository's imports.

P2, P3 and P4 are reported. They do not move the gate. A P1 kill is a kill; a P1
pass with P2–P4 at zero would be reported as suite-specific rather than general,
and would still not license a general claim.

## What this does not show (declared in advance)

* **That HELM is wrong.** Exact-match scoring is a deliberate, documented choice;
  the measurement is the *magnitude* of what that choice forgoes, which is an
  input to a maintainer's decision, not a verdict on it.
* **Anything about other suites, other models, or other versions.** Two Yi models
  and one suite version, `observed` only for these four cells.
* **That a recovered row was a reasoning success.** `eq_t1` proves the final
  answer is equal, not that the chain of thought that produced it was sound. A
  model can reach a correct answer by luck; these rows are therefore an upper
  bound on the model's true competence and the recovered *score* is the only
  number E141 claims.
* **That rounding is acceptable.** T2 rows are reported separately and never
  folded into the gate, because whether `0.333` counts for `\frac{1}{3}` is a
  convention question, not a correctness one.
* **Adoption.** A non-zero rate says the artefact is buildable, not that anyone
  will use it.

## AMENDMENT 1 (2026-10-15, after measurement, before the result was read)

The G0c row above is **unpassable as declared** and was corrected. It named one
negative-control offset (`(i+37) mod n`, 437 pairs on P1) and a bound of ≤0.5%
on the Wilson 95% *upper* limit of the false-positive rate. At n=437 a
zero-count sample has a Wilson upper limit of about 0.87%, so the control fails
for a perfect instrument. It is now five offsets — `(i+37)`, `(i+101)`,
`(i+211)`, `(i+307)`, `(i+401)`, 2,185 pairs on P1 — which puts the observed
zero at a Wilson upper limit of **0.176%**.

This changes no result. The kill gate had already fired on the rate alone
(4 rows and 1.626% against a declared 5 rows and 2.0%), and no choice about
G0c can alter that. It is recorded because the declared form is still wrong and
a reader comparing the two needs to know which one was run.

## Reproduction

```bash
tools/x -- python3 EXPERIMENTS/141-scorer-false-negatives/verify_population.py
tools/x -- python3 EXPERIMENTS/141-scorer-false-negatives/recover.py
```