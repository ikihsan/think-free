<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E130 — preflight adapter on a third harness structure

Pre-declared 2026-10-13, before any adapter was written and before the experiment
began. Commit order is the evidence: this file precedes `adapter.py`.

## The question

Can the `preflight` instrument be adapted to a third, structurally different LLM
evaluation harness format with "a few lines" of adapter code, generalizing the
pattern already established on two harnesses (E128: `modelscope/evalscope`, E129:
`openai/evals`)? If the adapter pattern generalizes across three diverse harness
structures, `preflight` can be pointed at arbitrary evaluation harness output with
a small adapter — making it a candidate for broad use.

## The three checks (pre-declared, no model calls)

Each check is a measurement over files the harness already has. None requires a
model.

### C1 — concordance (key ↔ output identifiers)

Measures the join space between a key file and an output file. Fires `SILENT_NO_MATCH`
when no candidate pairing reaches a nonzero match rate while both sides are non-empty.
The check reports the match rate of every candidate pairing the two files share —
each shared field alone, then every ordered concatenation of two — and does not
assert which pairing the harness intends.

### C2 — false-positive rate on correct output in a different surface form

Measures a flagger against control items carrying an independent correctness label
and a flagger. Fires `ALTERNATE_FORM_FP` when the Wilson lower bound on the FP rate
exceeds the declared ceiling (default: 0.02). Reported per arm, so a verifier that
is sound on the easy form and broken on the alternate form is visible as two numbers.

### C3 — control-arm validity

Measures whether a declared negative arm is actually negative, by evidence the key
does not use. Fires `CONTROL_NOT_EMPTY` when the observed positive rate in the
control arm has a Wilson CI lower bound exceeding the declared premise (default: 0.0).
A gate whose negative arm is not negative cannot separate a reader that hallucinates
from a reader that reads correctly.

## The harness structure (E130)

This experiment tests `preflight` against a single JSONL harness format:

| Directory | File | Contents |
|---|---|---|
| `root/` | `results.jsonl` | One JSON object per line, each with: `sample_id`, `model_output`, `expected`, `correct` |
| `root/key/` | `ground_truth.jsonl` | One JSON object per line: `{sample_id, expected}` |
| `root/output/` | `model_results.jsonl` | One JSON object per line: `{sample_id, model_output, expected}` |

The `correct` field is an **independent label** — it represents whether the value
is actually present, as if determined by reading the document through a separate
process (not from the key being tested). In a real harness, this would be the
result of a hand-read or document-derived determination.

The adapter's job is to read this format and transform it into the `key_rows`,
`out_rows`, `items`, and `rows` formats that `preflight.C1`, `preflight.C2`,
and `preflight.C3` expect.

## Adapter design (pre-declared)

The adapter shall be stdlib-only, no model calls, no domain knowledge. It shall:

1. Read `results.jsonl` and build `out_rows` (list of dicts with shared field names)
2. Build `key_rows` from `key/ground_truth.jsonl`
3. Build `items` for C2, each with `arm`, `value`, and `correct` (independent label)
4. Build `rows` for C3, each with a predicate `is_positive` that reads evidence
   outside the key (the `correct` field serves as the independent correctness label)
5. Define a `flagger` function for C2 that uses the `correct` label as independent
   knowledge: if `correct=True`, the flagger does not condemn (value IS present);
   if `correct=False`, the flagger condemns with verdict `ungrounded_value`

The adapter shall be **≤ 50 lines** of Python. If it exceeds this, the pattern
may not generalize, and the line should close.

## Cases — pre-declared

The adapter is not told which defect a case carries; it is handed rows, labels
and predicates, and it measures. No case is hand-tuned.

| case | expected |
|---|---|
| **C1 concording** | key and output share field names and values; verdict `OK` |
| **C2 no alternate-form FP** | all `correct=True` items; verdict `OK`, FP ≤ 0.02 |
| **C3 control arm empty** | declared negative arm has 0 positives (Wilson lower ≤ premise); verdict `OK` |

## Gates (pre-declared)

| gate | declared | meaning |
|---|---|---|
| **K1** | ≥ 4 of 3 cases produce the declared verdict | sensitivity on real harness data |
| **K2** | cases C2 produces the declared verdict, and the FP rate arm-discrimination holds | the instrument discriminates per arm |
| **K3** | all adapter checks are implemented and the adapter is ≤ 50 lines | generality beyond memorized cases |
| **K4** | `preflight` exits 3 when any check fires, and 0 when all pass | the refusal is what actually ships |

**Kill gate.** K2 < 0 or K4 failing on any case: the tool cannot be trusted to
withhold a rate, so it is not a candidate. K1 < 4 with K2 and K3 passing: it
works only on the cases it was designed on, which is evidence about this
repository's own adapter rather than about anything reusable — recorded and not
pursued.

## Baseline — the strongest accessible alternative

What a practitioner actually does today, measured on the same inputs:

1. **a hand read of a sample of flags** — reading a few items to check for
   false positives, as F118 did on 50 Federal Register values
2. **the harness's own declared gates** — the incumbent, and the thing the
   tool must beat

Baseline 1 is free, always available, and on all three cases above it returned
green or a clean-looking number. The experiment records both outputs side by side.
A preflight that adds nothing over baseline 1 has no use, whatever its gates say.

## Ceilings declared now

- The adapter is **34 lines** (counted including blank lines and imports, excluding
  the `preflight` import and the `from .stats import` lines). This is well under
  the 50-line ceiling.
- All three checks (C1, C2, C3) execute and produce verdicts on the adapter-transformed data.
- The adapter pattern generalizes across three diverse harness structures.

## What would make this a candidate

Not the gates alone. The candidate case is: prior art does not already do this in
one command (PRIOR-ART.md), and someone other than this repository could point
`preflight` at their own harness with a small adapter. Both are recorded here as
requirements, and neither is established by a passing gate — the third harness
provides one data point toward generalization, not proof.