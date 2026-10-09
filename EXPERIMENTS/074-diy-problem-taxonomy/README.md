<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Experiment 074: DIY Problem Taxonomy

Fresh observation in the DIY (home improvement) Stack Exchange domain to discover whether a concentrated, structured problem population exists that could support a computational tool.

## Documents

| Document | Purpose |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | Predeclared protocol with kill gates |
| [`VERDICT.md`](VERDICT.md) | Gate evaluation results and decision |
| [`analyze.py`](analyze.py) | Classification and gate evaluation logic |
| [`fetch.py`](fetch.py) | Data acquisition from Stack Exchange API |
| [`data/tool_check.md`](data/tool_check.md) | Existing tool survey for top problem types |
| [`data/taxonomy.jsonl`](data/taxonomy.jsonl) | Classified questions (676 rows, exempt from line cap) |
| [`data/distribution.json`](data/distribution.json) | Problem type distribution |
| [`data/structured_by_type.json`](data/structured_by_type.json) | Structured-input rates per type |
| [`data/verdict.json`](data/verdict.json) | Machine-readable gate results |

## Result

**FAIL** — Kill gate not met.

- **G1 (Population)**: PASS — PROC (Procedure/method) = 27.8% (188/676)
- **G2 (Structure)**: FAIL — PROC structured rate = 1.1% (2/188) << 50% threshold
- **G3 (Gap)**: Not evaluated (G2 failure)

No single problem type has both sufficient population concentration AND sufficient structured input to support a computational tool under the declared protocol.

## Key Finding

The DIY domain contains real, high-volume practitioner problems (top question: 713K views), but they are predominantly unstructured procedural questions ("How do I...?"). The more structured types (Diagnosis: 4.9% structured, Code compliance: 8.1% structured) lack population dominance. The domain does not yield a testable candidate.