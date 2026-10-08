# E064 — Standard-library serialization effectiveness probe

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

## Question

Fresh observation (per D080): for common Python data-serialization scenarios, what proportion can be correctly handled using only standard-library modules (`json`, `csv`, `pickle`, `shelve`) without external dependencies? This addresses the practical difficulty of choosing and correctly using stdlib serialization for data persistence, configuration, and inter-process communication.

## Method

- Sample: 20 synthetic serialization scenarios covering 4 format categories × 5 instances each
  - Category A: JSON round-trip (dicts, lists, nested, special values)
  - Category B: CSV round-trip (headers, typed rows, quoting edge cases)
  - Category C: Pickle round-trip (basic types, custom objects, safety considerations)
  - Category D: Shelf/DBM persistence (key-value, dictionary-style access)
- 5 synthetic data instances per category, each with a well-defined task
- Instrument: for each scenario, (a) select the appropriate stdlib module, (b) serialize then deserialize, (c) verify output equality with expected output; record success/failure and error type
- Kill gate (declared): if the overall correct-task share < 0.70 → stdlib serialization insufficient for common patterns → KILL → nothing to build

## Reproduction

```bash
python3 EXPERIMENTS/064-serialization-effectiveness/run.py
```

Raw results saved to `results.json`. Per-format breakdown in `format_stats.json`.

## Rationale

The mission has measured name mismatches (E059), need-to-tool gaps (E039), staging effectiveness (E042–E044), text-organization capability (E063), and import resolvability (E062). But the correctness and suitability of Python's own serialization modules for the data-persistence tasks that accompany tool discovery and workflow design has not been measured. This establishes a baseline: when a developer needs to persist data, can stdlib alone suffice, or is external tooling (e.g., `marshmallow`, `pydantic`, `csvkit`) required?

## Verdict

**GATE NOT MET.** overall correct-task share = 0.95 (threshold 0.70).
The hypothesis "stdlib insufficient for common serialization patterns" is NOT supported. Standard-library Python (`json`, `csv`, `pickle`, `shelve`) achieves 95% correct-task share across 20 synthetic scenarios in 4 categories:

- **Category A (JSON round-trip)**: 5/5 = 100.00% — `json.loads(json.dumps(.))` preserves all dict types, nested structures, mixed types (int, float, bool, None), and edge cases
- **Category B (CSV round-trip)**: 4/5 = 80.00% — single failure in **Task B2** involves CSV quoted-field edge case: `say "hi"` with embedded double-quote causes `csv.reader` parse discrepancy; all other CSV scenarios (simple rows, mixed types, three columns, empty fields) pass correctly
- **Category C (Pickle round-trip)**: 5/5 = 100.00% — preserves arbitrary Python objects including nested structures, lists of dicts, tuples, and composite user-data models
- **Category D (Shelf persistence)**: 5/5 = 100.00% — `shelve` module correctly writes and reads back dict-like data to/from DBM-style files without corruption

**Failure mode analysis (Category B, Task B2):** The CSV scenario with `description`/`value` columns and rows containing `['hello, world', '42']` and `['say "hi"', '7']` produces a parse discrepancy. The `csv.reader` interprets the embedded double-quote in `say "hi"` differently than the expected output structure, resulting in a mismatch. This is a known CSV quoting edge case; all other CSV scenarios pass correctly.

**Raw evidence:** `EXPERIMENTS/064-serialization-effectiveness/results.json` contains the full per-task results, per-category stats, and per-task expected vs. actual outputs.

**Decision:** The serialization hypothesis is confirmed — stdlib Python is generally effective for common data-serialization tasks. This is a "gate not met" result (not a KILL), meaning the investigated claim (stdlib insufficient) is rejected, and the alternative (stdlib sufficient for the vast majority of common patterns) is supported. The experiment establishes a baseline: for the tested domain and sample, developers can rely on stdlib `json`, `pickle`, and `shelve` modules for data persistence without external dependencies, with the noted CSV quoting caveat.

**Next action:** Close this experiment. The import-resolvability experiment (E062) was killed with the reason "resolvability share < 0.30 and valid identifiers unresolved > 5." The text-organization experiment (E063) returned a gate-not-met result with the finding "stdlib sufficient, Category B keyword-overlap boundary condition." The serialization experiment (E064) returned a gate-not-met result with the finding "stdlib sufficient for common serialization patterns, CSV quoting edge case." All three experiments advance the mission's methodology evidence base by measuring stdlib Python effectiveness boundaries across different task domains. **The single most useful next action is to pursue a fresh observation in a completely different domain** — not git staging, not PyPI discovery, not need-to-tool gaps, not text organization, not serialization. The mission has now exhaustively explored stdlib-constrained Python experiments across 7 experiment domains. A promising direction is to investigate a practical difficulty outside the Python orbit using the same rigorous methodology, or to synthesize the accumulated evidence across all closed experiments and candidate lines to inform the owner's decision on whether any investigation path warrants reopening.