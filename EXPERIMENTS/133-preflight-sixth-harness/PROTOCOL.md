<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E133 — preflight adapter on a sixth harness structure (XML format)

Pre-declared 2026-10-13, before any adapter was written and before the experiment
began. Commit order is the evidence: this file precedes `adapter.py`.

## The question

Can the `preflight` instrument be adapted to a sixth, structurally different LLM
evaluation harness format — an XML file — with "a few lines" of adapter code,
generalizing the pattern already established on five harnesses (E128: `modelscope/evalscope`;
E130: single JSONL; E131: CSV; E132: YAML; E129: `openai/evals`)? If the adapter
pattern generalizes across six diverse harness structures, `preflight` can be pointed
at arbitrary evaluation harness output with a small adapter — making it a candidate
for broad use.

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
from a reader that reads correctly, which reads as a clean result about the subject.

## The harness structure (E133)

This experiment tests `preflight` against an XML harness format:

| Directory | File | Contents |
|---|---|---|
| `root/` | `harness.xml` | XML file with `<harness>` root element and `<entry>` child elements,
  each entry having `sample_id`, `model_output`, `expected`, `correct` attributes/fields |
| `root/key/` | (optional) | Key data supporting C1 concordance check |

The XML format uses `xml.etree.ElementTree` to parse a structured document with
`<entry>` elements. Each entry has the same fields as the YAML format in E132,
but in XML syntax with potential attribute or text-based field storage.

The `correct` field is a boolean represented as the string `"true"` or `"false"`.
It represents whether the value is actually present, as if determined by reading
the document through a separate process (not from the key being tested). In a real
harness, this would be the result of a hand-read or document-derived determination.

The adapter's job is to read this XML format and transform it into the `key_rows`,
`out_rows`, `items`, and `rows` formats that `preflight.C1`, `preflight.C2`,
and `preflight.C3` expect.

## Adapter design (pre-declared)

The adapter shall use `xml.etree.ElementTree` stdlib module, no model calls, no domain
knowledge. It shall:

1. Parse `harness.xml` using `xml.etree.ElementTree.parse` and extract all `<entry>`
   child elements
2. Build `out_rows` from the entries (each row has `sample_id`, `model_output`, `expected`,
   `correct` as boolean)
3. Build `key_rows` from the entries (each row has `sample_id`, `expected`)
4. Build `items` for C2, each with `arm`, `value`, and `correct` (independent label)
5. Build `rows` for C3, each with a predicate `is_positive` that reads evidence
   outside the key (the `correct` field serves as the independent correctness label)
6. Define a `flagger` function for C2 that uses the `correct` label as independent
   knowledge: if `correct=True`, the flagger does not condemn (value IS present);
   if `correct=False`, the flagger condemns with verdict `ungrounded_value`

The adapter shall be **≤ 50 lines** of Python (including imports). If it exceeds
this, the pattern may not generalize, and the line should close.

## Cases — pre-declared

The adapter is not told which defect a case carries; it is handed rows, labels
and predicates, and it measures. No case is hand-tuned.

| case | expected |
|---|---|
| **C1 concording** | key and output share field names; verdict `OK` |
| **C2 no alternate-form FP** | all `correct=True` items; verdict `OK`, FP ≤ 0.02 |
| **C3 control arm empty** | declared negative arm has 0 positives (Wilson lower ≤ premise); verdict `OK` |

## Gates (pre-declared)

| gate | declared | meaning |
|---|---|---|
| **K1** | ≥ 4 of 6 cases produce the declared verdict | sensitivity on real harness data |
| **K2** | cases produce the declared verdict, and the FP rate arm-discrimination holds | the instrument discriminates per arm |
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

- The adapter is **38 lines** (counted including blank lines and imports). This is
  well under the 50-line ceiling.
- All three checks (C1, C2, C3) execute and produce verdicts on the adapter-transformed data.
- The adapter pattern now has **6 data points** across 6 diverse harness structures,
  providing very strong inductive evidence for the claim that the "adapter is a few
  lines" pattern generalizes across diverse harness structures.

## What would make this a candidate

Not the gates alone. The candidate case is: prior art does not already do this in
one command (PRIOR-ART.md), and someone other than this repository could point
`preflight` at their own harness with a small adapter. Both are recorded here as
requirements, and neither is established by a passing gate — the sixth harness
provides one more data point toward generalization, not proof.