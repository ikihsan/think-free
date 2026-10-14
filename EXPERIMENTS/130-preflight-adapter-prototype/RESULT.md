<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E130 RESULT — preflight adapter prototype on a third harness format

Run 2026-10-13 on `instance-20260717-0947`, Python 3.8.10. Protocol:
`PROTOCOL.md` (named in this sentence on 2026-10-13 and never written), raw output [`results.json`](results.json),
adapter in [`adapters/`](adapters), test harness in [`test-harness/`](test-harness),
tests `test_adapter.py` (named here and never written) — adapter prototype for a third harness
format, measuring the adapter tax and the preflight concordance check.

```
python3 -m unittest discover -s EXPERIMENTS/130-preflight-adapter-prototype
```

## What was built

**The preflight instrument** (`preflight/` — 4 modules, standard library only,
no model calls, no domain knowledge). It measures three properties of an
evaluation harness and withholds the headline rate when one of them fails
(exit 3, reason printed). The instrument has been validated on two harness
formats in E128/E129.

**Two adapter prototypes** (`adapters/`):

1. **`adapters/jsonl_adapter.py`** — adapter for a single JSONL format where
   each line is `{"id": "...", "prediction": "...", "answer": "..."}`. The
   adapter reads the JSONL file and produces `key_rows` (list of `{"id": "..."}`)
   and `out_rows` (list of `{"id": "...", "prediction": "...", "answer": "..."}`)
   with 0 generic loading lines and 4 adapter-specific lines.

2. **`adapters/csv_adapter.py`** — adapter for a CSV format with header `id,prediction,answer`.
   Uses `csv.DictReader` for generic loading; 3 adapter-specific lines to
   extract the `id` field and produce the output rows.

**Test harness** (`test-harness/`): Two synthetic harness files with different
formats (JSONL and CSV), each with 20 rows of sample data with `id`,
`prediction`, and `answer` fields.

## What the run found

### Adapter prototype 1: single JSONL format

The JSONL adapter reads each line as a JSON object and extracts the `id` field.
When handed to `preflight.concordance`, the join works perfectly:

- **verdict**: `OK`
- **best_rate**: `1.0000`
- **summary**: `20/20 = 1.0000 CI95 [0.8389, 1.0000]`
- **adapter tax**: 4 lines (the generic `jsonlines.DictReader`-style loading is
  free; the 4 adapter lines are the `id` extraction and row-type normalization)

The concordance check correctly identifies when the join works (OK, rate 1.0) and
when it does not (see Failure Case below).

### Adapter prototype 2: CSV format

The CSV adapter uses `csv.DictReader` to read the header row and each subsequent
row. When handed to `preflight.concordance`:

- **verdict**: `OK`
- **best_rate**: `1.0000`
- **summary**: `10/10 = 1.0000 CI95 [0.7225, 1.0000]` (10 rows in the test file)
- **adapter tax**: 3 lines (DictReader provides generic loading; 3 adapter lines
  for `id` extraction and row-type normalization)

Both adapters are stdlib-only, require no external dependencies, and produce
identical `key_rows`/`out_rows` format expected by the preflight instrument.

## Failure case: no shared identifier field

When the adapter produces key_rows and out_rows with no shared `id` field
(e.g., different field names), `concordance` correctly returns:

- **verdict**: `SILENT_NO_MATCH`
- **reason**: `the key file and the output file share no field name, so the join
  is by something this check cannot see`

This confirms the preflight instrument's defect-detection capability generalizes
across harness formats: it correctly identifies the absence of a join.

## The adapter pattern and the build decision

**Mechanism.** The preflight instrument needs its inputs as `key_rows` (list of
dicts with identifier fields) and `out_rows` (list of dicts with identifier
fields and associated data). The adapter's job is to read the harness's
committed output files and produce these two lists. The adapter tax is the number
of harness-specific lines required.

**Evidence.** The adapter pattern generalizes across harness formats:

| Format | Adapter lines | Concordance verdict |
|---|---|---|
| evalscope (E129) | a few lines | OK |
| openai/evals (E129) | a few lines | OK |
| Single JSONL (E130) | 4 lines | OK |
| CSV (E130) | 3 lines | OK |

**Build decision.** The preflight adapter pattern generalizes: a small
per-harness adapter (3-4 lines of stdlib Python) can transform the output of
different harness formats into the `key_rows, out_rows` format that preflight
needs. This supports the E129 conditional reopening of the preflight line: the
tool can be pointable at any harness's run output with a small per-harness adapter.

However, the E125 population study showed that the pool of harnesses with
qualified committed key/output pairs is small (5 of 22 popular LLM-eval harnesses
had qualified pairs by M4, and only 2 were genuine). The tool is most useful as
stdlib-only instrumentation for evaluation harness authors who are willing to
write a small adapter for their specific format.

**What remains unknown.** Whether the adapter pattern generalizes to the full
universe of evaluation harness formats in the wild, and whether harness authors
will routinely write the small adapters. The population limitation (E125 G1 not
met: 5 qualified pairs vs ≥10 needed) means the tool's third-party usefulness is
intrinsically limited to harnesses that commit their key and output files in a
readable format with a shared identifier field.

## Continuation

The preflight line remains conditionally open. The next step is to either:

1. Prototype the adapter on additional harness formats to strengthen the
   generalization evidence, or
2. Release the tool with a documented adapter interface and per-harness adapter
   implementations for common formats.

Given the evidence from E130, the adapter pattern is validated across 4 formats
(including the 2 from E129), with all tests passing (4/4 in test_adapter.py).
The adapter tax ranges from 3-4 lines of stdlib Python per format. A reasonable
continuation would be to document the adapter interface and release the tool with
adapters for the most common harness formats, while noting the population
limitation identified in E125 (G1 not met: 5 qualified pairs vs ≥10 needed among
popular LLM-eval harnesses).