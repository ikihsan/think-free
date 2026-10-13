<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E128 RESULT — the run output directory has the shape preflight needs; the tax is an adapter, not a library

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0947`.
Answered E125 §7's open question: *does a harness's run output
directory have the shape preflight needs?*

## The answer

**Yes.** The `modelscope/evalscope` output writer (read end to end in
`evalscope/api/evaluator/cache.py`, 542 lines) produces exactly the
shape `preflight` inspects:

| file | path | key field | contents |
|---|---|---|---|
| predictions | `predictions_dir/{model}/{benchmark}_{subset}.jsonl` | `index` | model output, messages, metadata |
| reviews | `reviews_dir/{model}/{benchmark}_{subset}.jsonl` | `index` | score, target, messages |

**The join is `predictions[index] ↔ reviews[index]`**, within one
task directory (same `model` and `benchmark`). The `index` is the
sample index in the dataset — a stable identifier shared by both
files.

This is the mechanism E125 §5 inferred from committed files: "the
sample that carries the expected answer is the same object the output
is scored against." The run output confirms it.

## The tax

The tax is **an adapter**, not a loader library. To point `preflight`
at this harness's run output, the caller supplies:

1. **The predictions directory** and **reviews directory** (two paths)
2. **The join key** (`index`)
3. **The task-directory constraint** (both files must be in the same
   `{model}/{benchmark}_{subset}` directory)

This is a few lines of adapter code — not the 0 lines E125 measured
on committed files. The difference: committed files are the wrong
surface to measure the tax on. The tax exists at run time, not at
commit time.

## Why this matters

E125 concluded `preflight` stays internal because "the population it
would be released *for* does not supply a working example." That is
true of **committed** state — external harnesses commit their task
data and almost none of their model output (21 of 857 sampled files
carry an output-shaped field).

But **run-time** output is different. A harness writes its predictions
and reviews to disk at run time, in the shape `preflight` needs. The
tool can be pointed at a run output directory with a per-harness
adapter that specifies the directories and join key.

The finding: **`preflight` can be made useful to anyone running LLM
evaluations, with a small per-harness adapter.** The adapter is the
tax, and it is a tax the harness's own code already pays — the
directories and join key are properties of the harness's output
writer, not new information the caller must supply.

## What this does not establish

- **That the adapter is always small.** One harness was read. The
  adapter for a harness with a different output structure (e.g.,
  `openai/evals`, which writes an append-only event stream with no
  key file) may be larger or impossible.
- **That `preflight` should be released.** The tool works on the
  mission's own harnesses and can be pointed at run output with an
  adapter. Whether anyone outside this repository would use it is
  `untested`.
- **That the join is always `index`.** The join key is a property of
  the harness's output writer. A different harness may use a
  different key.

## The decision

**The preflight line reopens, conditionally.** E125's conclusion —
"preflight stays internal" — is corrected: the tool can be pointed
at a harness's run output directory with a per-harness adapter. The
adapter is the tax, and it is a tax the harness's own code already
pays.

The next step is to prototype the adapter and measure its size on a
second harness. If the adapter is a few lines per harness, `preflight`
is a useful tool for anyone running LLM evaluations. If it is larger,
the line closes again.

No candidate. The tool stays internal until the adapter is measured.
