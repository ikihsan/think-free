<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E136 — UltraEval-Audio preflight adapter measurement

Measures the adapter size for UltraEval-Audio harness output format.

## Protocol

1. Create test fixture mimicking UltraEval-Audio output structure
2. Implement adapter in preflight CLI
3. Measure adapter lines (code lines, excluding docstrings/comments)
4. Verify adapter works with preflight's three checks (C1, C2, C3)
5. Record result in adapters_catalog.json

## Artifacts

- `RESULT.md` — this result
- Adapter code in `EXPERIMENTS/124-eval-harness-preflight/preflight/__main__.py` (function `adapter_ultraeval`)
- Test fixture generator in `EXPERIMENTS/124-eval-harness-preflight/test_ultraeval_adapter.py`
- Updated `EXPERIMENTS/adapters_catalog.json`
- Updated `EXPERIMENTS/134-preflight-prototype` (prototype README)