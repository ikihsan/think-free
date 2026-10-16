<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E171 AMENDMENT 2 — the G0 probe as built was single-class, which would have made G0 vacuous

Found **by reading the probe output**, before any class label existed and before
any gate ran. Recorded here because the protocol is the instrument; a defect in
the probe is a defect in the gate.

## The defect

`g0_probe.py` built the probe as

```python
probe = (with_v[:5] + with_v[-2:-7:-1] + without_v[:5] + without_v[-2:-7:-1])
probe = probe[:10]
```

The docstring's intent is *"ten rows, five with a version number in the
operative sentence and five without"*. The code does not implement that. There
are **12** rows in `with_v`, so `with_v[:5] + with_v[-2:-7:-1]` already
produces 10 rows — every one of them `any_version=True` — and the final
`probe[:10]` drops every `without_v` row. The probe written to
`raw/g0-probe.json` at 06:48 is **10 of 10 constructed `version_fact`**.

## Why this would have corrupted the gate

G0 requires the classifier to recover **≥ 8 of 10** labels on a probe *"whose
classes were fixed by the presence of an explicit operative sentence in the
answer (a version number in the operative step, **or the absence of any**)"*.
On a single-class probe the gate is **vacuous**: a classifier that labels every
row `version_fact` scores 10/10 without discriminating anything. A pass would
have been worthless and, worse, would have been recorded as evidence the
instrument works.

## The repair, declared before any label

- **Selection.** 5 highest-scoring rows from `with_v` + 5 highest-scoring rows
  from `without_v`, score = the top answer's score, ties broken by `idx`
  ascending. Highest-scoring is chosen because the resolution is most visible
  there; the rule is mechanical and fixed before labelling.
- **Construction signal unchanged.** `any_version` = any answer in the thread
  carries a version number (the `VER` regex). This is the same judgement-free
  signal the probe was built with; only the row selection changes.
- **No bar moves.** G0 ≥ 8/10, G1 ≥ 0.40 over the 13 unserved rows, G2
  reported over the 11 served rows, and the kill gate (G1 failing withdraws
  E168's G3) are exactly as declared in `PROTOCOL.md` and `AMENDMENT 1`.

## What this does not change

The defect was in the probe's row selection, not in the population, the
reading rule, or the gates. No label exists yet, so nothing measured is
affected. The rebuilt probe overwrites `raw/g0-probe.json`; the defective
build's output is described here rather than deleted, so a reader can check
the defect against the repair.
