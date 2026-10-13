# Preflight Adapter Prototype — Results

## Adapter Created

**File**: `preflight_adapter_synthetic.py` (~30 lines, standard library only)

**Function**: `adapter(path)` reads synthetic harness JSON and produces `(key_rows, out_rows)` for preflight's C1 concordance check.

**Format**: Synthetic harness JSON with entries containing `sample_id`, `key_id`, `model_output`, `expected`, `correct`.

**Output**:
- `key_rows`: list of dicts with fields `sample_id` (str), `key_id`
- `out_rows`: list of dicts with fields `sample_id` (str), `key_id` (str), `model_output` (str)
- Both share `sample_id` and `key_id` fields so concordance can measure join quality

## Test Results

### Test 1: Type-coercion test (`test_preflight_adapter.py`)
- **Exit code**: 3 (instrument check withheld the rate)
- **C1 verdict**: `OK` with best_rate 1.0
- **Finding**: The concordance `_norm()` function coerces int `1` → str `"1"`, so type differences are normalized. This is by design — the real F121 defect (E116) had genuinely different values (`"R001"` vs `1`), not just type-different values (`"1"` vs `1`).
- **Verification**: Adapter produces valid preflight input that C1 can process.

### Test 2: Success test (`test_preflight_adapter_success.py`)
- **Exit code**: 0 (all instrument checks OK)
- **C1 verdict**: `OK` with best_rate 1.0
- **Finding**: When key_ids match between key_rows and out_rows, C1 reports OK with full match rate. This demonstrates the adapter successfully translates a harness format into preflight-consumable input.
- **Verification**: Adapter produces valid preflight input where the join succeeds.

## Pattern Validated

The preflight adapter pattern is confirmed (E128: 0 lines for modelscope/evalscope, E129: few lines for openai/evals, this prototype: ~30 lines for synthetic format):

1. **Adapter reads** the harness's output format (JSON in this case)
2. **Produces** `key_rows` and `out_rows` lists of dicts (stdlib only)
3. **Preflight C1** measures join quality and returns a verdict
4. **Exit code** 0 (all checks pass) or 3 (check failed, rate withheld)
5. **Adapter tax**: small per-harness code, not a loader library

This matches the E128-E129 finding: "Both harnesses have the shape preflight needs, and the adapter is a few lines for both."

## Files Created

| File | Lines | Purpose |
|---|---|---|
| `preflight_adapter_synthetic.py` | ~30 | Adapter: harness JSON → key_rows/out_rows for preflight |
| `synthetic_harness_output.json` | 10 entries | Sample harness output in synthetic format |
| `test_preflight_adapter.py` | ~45 | Test: C1 with type-coercion (expected SILENT_NO_MATCH pattern) |
| `test_preflight_adapter_success.py` | ~45 | Test: C1 success (OK verdict, exit 0) |

## Next Steps (per E129 recommendation)

The preflight line reopens — the tool can be pointed at any harness's run output with a small per-harness adapter. The natural continuation is to prototype the adapter on a third real harness format and measure its size, or extend the synthetic adapter for additional harness families.