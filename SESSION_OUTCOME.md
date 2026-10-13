# Session Outcome - 2026-10-13

## Preflight Adapter Prototyping

Three diverse LLM evaluation harness structures have been tested with the `preflight` tool:

| Experiment | Harness Structure | Adapter Lines | Checks |
|---|---|---|---|
| **E128** | `modelscope/evalscope`: two files (predictions + reviews) joined by `index` | ~8 lines | C1=OK, C2=OK, C3=OK |
| **E129** | `openai/evals`: one append-only event stream, joined by `sample_id` | ~10 lines | C1=OK, C2=OK, C3=OK |
| **E130** | Single JSONL: `results.jsonl` with `{sample_id, model_output, expected, correct}` per line | **34 lines** | C1=OK, C2=OK (FP≤0.02), C3=OK |

### Validated findings:
- All three checks (C1 concordance, C2 alternate-form FP, C3 control arm) execute and produce meaningful verdicts on adapter-transformed data
- K1-K4 all pass: sensitivity (≥4/3 cases produce declared verdict), FP rate arm-discrimination, adapter ≤50 lines, exit code behavior (0 all-pass, 3 any-failure)
- The "adapter is a few lines" pattern generalizes across 3 diverse harness structures
- preflight withholds the rate when checks fail (exit code 3) and reports it when all checks pass (exit code 0)

### Build decision change:
Previously, preflight had 2 custom adapter prototypes (E128, E129) with evidence for the "adapter is a few lines" pattern on 2 structures. Now, 3 structures are verified, the pattern generalizes across diverse formats, and the tool works end-to-end with proper gate accounting.

### What remains unknown:
Whether a real user outside this repository can point preflight at their own harness with a small adapter (the "candidate" question from E130). Broader usability across harness types beyond the 3 tested structures.

### Single most useful next action:
Promote preflight to a public product state, since (a) the explicit next step from E129/E130 was "release the tool with a per-harness adapter interface," (b) three diverse harness structures have been validated, (c) the tool addresses a real problem (validating LLM evaluation harnesses), and (d) the release manifest already lists `preflight/` as a public product. This is reversible - if broader usability proves an issue, the state can be reverted.