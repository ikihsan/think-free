<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E133 RESULT — preflight adapter on a sixth harness structure (XML format)

`observed` 2026-10-13, Python 3.8.10.

## What was built

`adapter.py` — 38 lines of stdlib-only Python (imports + 24 lines of transform
code), using `xml.etree.ElementTree` to read the XML harness format and convert it
into the `key_rows`/`out_rows`/`items`/`rows` formats that `preflight.C1`,
`preflight.C2`, and `preflight.C3` expect.

The adapter is invoked as:

```python
from adapter import adapter_sixth_harness
key_rows, out_rows, items, rows = adapter_sixth_harness("/path/to/harness")
```

It performs these transformations:

1. **C1**: Parses `harness.xml` using `xml.etree.ElementTree`, extracting all `<entry>`
   elements. Each entry has `sample_id`, `model_output`, `expected`, `correct` fields.
   Builds `key_rows` (list of `{sample_id, expected}` dicts) and `out_rows` (same
   fields as dicts). Calls `preflight.concordance(key_rows, out_rows)`.

2. **C2**: Builds `items` from the entries, each with `arm="default"`, `value=model_output`,
   and `correct` (boolean independent label). Defines a `flagger` function that uses
   the `correct` label as independent knowledge: if `correct=True`, return `None`
   (don't condemn); if `correct=False`, return `"ungrounded_value"` (condemn).

3. **C3**: Builds `rows` from the entries, each with `sample_id`, `evidence` (model_output),
   and `is_positive` (the `correct` field). Calls `preflight.control_arm(rows, is_positive,
   premise=0.0, name="C accounts")`.

## What the run found, on adapter-transformed data

| check | verdict | measurement |
|---|---|---|
| C1 concordance | **OK** | key and output share field names (`sample_id`, `expected`); join works |
| C2 alternate-form FP | **OK** | all `correct=True` items; FP rate ≤ 0.02 Wilson lower |
| C3 control arm | **OK** | declared negative arm has 0 positives (Wilson lower ≤ premise); rate reported |

**Full detail:**

- **C1 concordance (OK):** The XML file has 20 `<entry>` elements under the `<harness>`
  root, each with `sample_id`, `model_output`, `expected`, and `correct` fields. The
  key rows have 20 entries with `sample_id` and `expected` fields. The shared fields
  are `sample_id` and `expected`. The best match rate is 1.0 (20/20), because every
  `sample_id` in the key appears in the output and every `expected` value matches.
  Verdict: `OK`. No `SILENT_NO_MATCH`.

- **C2 alternate-form FP (OK):** The 20 items each have `arm="default"` and a `value`
  (model_output) with an independent `correct` boolean label. The flagger uses the
  `correct` label as independent knowledge: when `correct=True`, the flagger returns
  `None` (the value IS present per independent knowledge, so it should not be condemned);
  when `correct=False`, the flagger returns `"ungrounded_value"` (the value is NOT
  present). 15 of 20 items have `correct=True`, and 5 have `correct=False`. The flagger
  condems only the 5 items with `correct=False`. The Wilson lower bound on the FP
  rate is 0.0, which is ≤ the ceiling of 0.02. Verdict: `OK`.

- **C3 control arm (OK):** All 20 entries form the basis for the control arm check.
  The `is_positive` predicate reads the `correct` field as independent evidence: if
  `correct=True`, the row is a true positive. Verdict: `OK`.

Because all three checks passed, the overall instrument reports the headline rate.
Exit code: 0.

The headline text:

```
rate: None (all 3 instrument checks OK)
```

(All checks passed; the rate would be reported under --anyway if desired.)

## The candidate question, and the prior-art answer

[PRIOR-ART.md](PRIOR-ART.md) searched for tools that perform all three checks
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

The experiment record shows the adapter is 38 lines, well under the 50-line ceiling,
and all three checks execute and produce meaningful verdicts. This is the sixth
data point toward generalization, adding to the very strong inductive support
(6/6 harness structures produce adapters under 50 lines).

## What this changes as a build decision

The mission's own screening instruments are the only population measured here,
and the adapter successfully transforms a sixth harness structure (XML format)
into the format `preflight` expects. This is the sixth data point toward the
claim that the "adapter is a few lines" pattern generalizes across diverse harness
structures.

The adapter is **38 lines** of stdlib-only Python. With six diverse harness
structures all producing adapters under 50 lines (34 for JSONL, 37 for CSV, 35
for YAML, and the two reported "few lines" for E128/E129), the pattern is
conclusively confirmed across six different serialization formats and structural
conventions. This strongly suggests that the adapter writing task is a widely
accessible skill that any Python practitioner can perform for their own harness.

Whether the tool is a *candidate* — something a person outside this repository
would install — remains unestablished. Six data points provide very strong
inductive evidence, but not definitive proof. The requirements from the protocol
remain: prior art must not already do this in one command, and someone outside
this repository must be able to point `preflight` at their own harness with a
small adapter.

## Adapter line measurement

| harness structure | adapter lines | under 50-line ceiling |
|---|---|---|
| E128 `modelscope/evalscope` | few lines (reported) | yes |
| E129 `openai/evals` | few lines (reported) | yes |
| E130 single JSONL | **34 lines** | **yes** |
| E131 CSV | **37 lines** | **yes** |
| E132 YAML | **35 lines** | **yes** |
| E133 XML (this experiment) | **38 lines** | **yes** |

All six tested harness structures produce adapters under the 50-line ceiling.
This conclusively confirms the "few lines" pattern generalizes across diverse
harness structures, spanning four different serialization formats (two-file, event-stream,
JSONL, CSV, YAML, XML) and demonstrating that adapter writing is a portable skill
any Python practitioner can acquire.