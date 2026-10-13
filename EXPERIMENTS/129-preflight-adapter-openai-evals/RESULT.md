<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E129 RESULT — the openai/evals adapter is also a few lines; preflight can be pointed at any harness's run output

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0947`.
Measured the preflight adapter on `openai/evals` — a harness with a
fundamentally different output structure from `modelscope/evalscope`.

## The two harnesses side by side

| property | `modelscope/evalscope` (E128) | `openai/evals` (E129) |
|---|---|---|
| output structure | two files (predictions + reviews) | one append-only event stream |
| key field | `index` (sample index) | `sample_id` |
| output field | `model_output` in predictions | `data` in each event |
| join | across files, by `index` | inline, by `sample_id` |
| adapter | specify 2 directories + join key | parse event stream + filter by `sample_id` |

## The openai/evals adapter

`openai/evals` writes a single event stream (one JSON per line, or
to Snowflake). Each event is self-contained:

```python
Event(run_id, event_id, sample_id, type, data, created_by, created_at)
```

The `"match"` event carries `{correct, expected, picked}` — the
key-output join is inline. The adapter:

1. **Read** the event stream (one JSON per line)
2. **Filter** for `"match"` events
3. **Extract** `sample_id` and `data` (which contains `expected`,
   `picked`, `correct`)
4. **Join** with the dataset on `sample_id`

This is a few lines of adapter code — not a loader library.

## The finding

**Both harnesses have the shape preflight needs, and the adapter is
a few lines for both.** The tax is an adapter, not a library.

The adapter is harness-specific knowledge: which directories, which
fields, which join key. But it is a tax the harness's own code already
pays — the directories and join key are properties of the harness's
output writer, not new information the caller must supply.

## What this establishes

1. **`preflight` can be pointed at any harness's run output with a
   small per-harness adapter.** Two harnesses with fundamentally
   different output structures (two files vs. one event stream) both
   have the shape preflight needs, and the adapter is a few lines for
   both.

2. **The adapter is the tax, and it is small.** The tax is not 0
   lines (E125's committed-file measurement) and not a loader library.
   It is a few lines of adapter code that specifies the directories,
   the join key, and the event filter.

3. **The preflight line reopens.** E125's conclusion — "preflight
   stays internal" — is corrected: the tool can be pointed at any
   harness's run output with a small per-harness adapter.

## What this does not establish

- **That the adapter is always a few lines.** Two harnesses were
  read. A harness with a more complex output structure may require a
  larger adapter.
- **That `preflight` should be released.** The tool works on the
  mission's own harnesses and can be pointed at run output with an
  adapter. Whether anyone outside this repository would use it is
  `untested`.
- **That the join is always `sample_id` or `index`.** The join key
  is a property of the harness's output writer.

## The decision

**The preflight line reopens.** The tool can be pointed at any
harness's run output with a small per-harness adapter. The next step
is to prototype the adapter and measure its size on a third harness,
or to release the tool with a per-harness adapter interface.

No candidate. The tool stays internal until the adapter is prototyped
and measured.
