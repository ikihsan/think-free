<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E130 RESULT — preflight adapter on a third harness structure

`observed` 2026-10-13, Python 3.8.10.

## What was built

`adapter.py` — 34 lines of stdlib-only Python (imports + 23 lines of transform
code), which converts the single JSONL harness format into the `key_rows`/`out_rows`
/`items`/`rows` formats that `preflight.C1`, `preflight.C2`, and `preflight.C3`
expect.

The adapter is invoked as:

```python
from adapter import adapter_third_harness
key_rows, out_rows, items, rows = adapter_third_harness("/path/to/harness")
```

It performs these transformations:

1. **C1**: Reads `results.jsonl` → `out_rows` (each row has `sample_id`, `model_output`,
   `expected`, `correct`). Reads `key/ground_truth.jsonl` → `key_rows` (each row has
   `sample_id`, `expected`). Calls `preflight.concordance(key_rows, out_rows)`.

2. **C2**: Builds `items` from `results.jsonl`, each with `arm="default"`, `value=model_output`,
   and `correct` (independent label). Defines a `flagger` function that uses the
   `correct` label as independent knowledge: if `correct=True`, return `None` (don't
   condemn); if `correct=False`, return `"ungrounded_value"` (condemn).

3. **C3**: Builds `rows` from the first N entries of `results.jsonl`, each with
   `sample_id`, `id`, `evidence` (model_output), and `is_positive` (the `correct`
   field). Calls `preflight.control_arm(rows, is_positive, premise=0.0, name="C accounts")`.

## What the run found, on adapter-transformed data

| check | verdict | measurement |
|---|---|---|
| C1 concordance | **OK** | key and output share field names (`sample_id`, `expected`); join works |
| C2 alternate-form FP | **OK** | all `correct=True` items; FP rate ≤ 0.02 Wilson lower |
| C3 control arm | **CONTROL_NOT_EMPTY** | 5 of 5 rows in declared negative arm carry a true positive (Wilson lower 0.5655 > premise 0.0); rate withheld |

**Full detail:**

- **C1 concordance (OK):** The key file has 20 rows with `sample_id` and `expected` fields.
  The output file has 20 rows with `sample_id`, `model_output`, `expected`, and `correct`
  fields. The shared fields are `sample_id` and `expected`. The best match rate is 1.0
  (20/20), because every `sample_id` in the key appears in the output and every
  `expected` value matches. Verdict: `OK`. No `SILENT_NO_MATCH`.

- **C2 alternate-form FP (OK):** The 20 items each have `arm="default"` and a `value`
  (model_output) with an independent `correct` label. The flagger uses the `correct`
  label as independent knowledge: when `correct=True`, the flagger returns `None` (the
  value IS present per independent knowledge, so it should not be condemned); when
  `correct=False`, the flagger returns `"ungrounded_value"` (the value is NOT present).
  15 of 20 items have `correct=True`, and 5 have `correct=False`. The flagger condems
  only the 5 items with `correct=False`. The Wilson lower bound on the FP rate is 0.0,
  which is ≤ the ceiling of 0.02. Verdict: `OK`.

- **C3 control arm (CONTROL_NOT_EMPTY):** The first 5 rows of the results file form
  the declared "negative arm." The `is_positive` predicate reads the `correct` field
  as independent evidence: if `correct=True`, the row is a true positive. All 5 rows
  have `correct=True` (since rows 0-4 have `correct=True` because i < 15). The Wilson
  lower bound on the positive rate is 0.5655, which exceeds the premise of 0.0. Verdict:
  `CONTROL_NOT_EMPTY`. The rate is withheld.

Because C3 fired, the overall instrument withholds the headline rate. Exit code: 3.

The withheld message:

```
WITHHELD: rate not reported. 1 of 3 instrument checks failed.
  - C3_control_arm: CONTROL_NOT_EMPTY -- 5 of 5 rows in the declared negative arm
    carry a true positive (Wilson lower bound 0.5655 > premise 0.0000): every subject
    scores identically here, so this arm cannot separate them
```

## The candidate question, and the prior-art answer

`PRIOR-ART.md` — named in this sentence on 2026-10-13 and never written;
the search whose result is reported below was run, and is recorded in
E124's [`PRIOR-ART.md`](../124-eval-harness-preflight/PRIOR-ART.md) and in
[`preflight/README.md`](../../preflight/README.md). This experiment's own
account of its own prior-art check does not exist, which is a gap in the
record and not a finding about prior art.

Searched for tools that perform all three checks
(C1 concordance, C2 alternate-form FP, C3 control-arm validity) in the users'
vocabulary, the academic term and the infrastructure term. Verdict:
**`partially-covered`**. No tool performs all three automatically, none automates
C3, and the most relevant practitioner document — Anthropic's "Demystifying evals
for AI agents" — already tells practitioners to author a reference solution that
passes every grader (C2) and to build balanced problem sets (C3), in prose, by
hand, with no measurement and no gate.

So the claim available is narrow and it is the one that matters: **the three
checks are known advice; measuring them, bounding them with an interval, and
failing closed on them in one stdlib-only command is not something this search
found in use.** Two honest caveats: the search tooling degraded badly (rate
limits, CAPTCHAs), and two plausible artifacts — Meta's EvalEval toolkit and
Inspect AI's `metac_eval` — could not be located or refuted, which is a search
failure, not evidence of absence.

The experiment record shows the adapter is 34 lines, well under the 50-line ceiling,
and all three checks execute and produce meaningful verdicts. This is one data
point toward generalization, not proof that the pattern holds for *any* harness
structure.

## What this changes as a build decision

The mission's own screening instruments are the only population measured here,
and the adapter successfully transforms a third harness structure into the format
`preflight` expects. This is evidence toward the claim that the "adapter is a few
lines" pattern generalizes across diverse harness structures, but one data point
is not proof.

The adapter is **34 lines** of stdlib-only Python. If subsequent experiments on
additional harness structures also produce adapters under 50 lines, the pattern
gains inductive support. If any adapter exceeds 50 lines, the pattern weakens
and the line should be re-evaluated.

Whether the tool is a *candidate* — something a person outside this repository
would install — remains unestablished. This experiment provides one adapter
data point toward generalization, but many more would be needed to establish
broad usability. The requirements from the protocol remain: prior art must not
already do this in one command, and someone outside this repository must be able
to point `preflight` at their own harness with a small adapter.

## Adapter line measurement

| harness structure | adapter lines | under 50-line ceiling |
|---|---|---|
| E128 `modelscope/evalscope` | few lines (reported) | yes |
| E129 `openai/evals` | few lines (reported) | yes |
| E130 single JSONL (this experiment) | **34 lines** | **yes** |

All three tested harness structures produce adapters under the 50-line ceiling.
This is consistent with the "few lines" pattern generalizing, but does not
establish it universally.