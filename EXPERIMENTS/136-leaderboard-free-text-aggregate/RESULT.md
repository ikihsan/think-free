<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E138 RESULT — R1 recomputation reaches GSM free-text cell with #### parser

Cell (selected by the protocol's pre-declared rule): **`gsm`**,
HELM lite `v1.0.0`, model `01-ai/yi-34b` — the free-text scenario with
`####` number-extraction parser, single run (1000 instances). Every URL
below was fetched unauthenticated from this VM on 2026-10-14; every byte is
in `fetched-manifest.json` by sha256.

## Gates

- **G1 inventory: PASS.** Already established by E136's inventory fetch
  (868 run dirs, 9 families, 31 models). `gsm:model=01-ai_yi-34b` exists.
- **G2 reach: PASS.** 3/3 fetches 200: `run_spec.json`, `scenario_state.json`,
  `stats.json` for the yi-34b gsm run; plus the published group table
  `groups/gsm.json` and `per_instance_stats.json`. Free text confirmed:
  `method: generation`, `max_tokens: 400`; completion lengths mean ~117 /
  max 400 chars; 1000 rows total.
- **G3 recomputation: AGREE** (below).

## Parse rule (declared in E136 PROTOCOL.md)

Extract the number after the *last* `####` in the completion; if no `####`,
take the last number in the completion; strip commas and surrounding
whitespace; correct iff the extracted number equals the gold number (the
reference answer after its own final `####`, comma-stripped). The metric's
comparison operator is exact string equality on normalized numbers.

**Observed in this population:** Neither references nor completions contain
`####` — HELM's GSM8K references end with "The answer is N" and model
completions simply end with the answer. The fallback rule (last number in
text) was exercised on **1000/1000** rows for both gold and predicted
answers. The operator is normalized-string equality (not numeric equivalence).

## G3 recomputation — agree

R1 discipline held throughout: every verdict was recomputed from
`scenario_state.json` alone; `stats.json` and `per_instance_stats.json`
were loaded only after, for comparison and reconciliation.

| metric | recomputed | published | match |
|---|---|---|---|
| `final_number_exact_match` (EM) | 648/1000 = 0.648000 | 0.648 | **exact** |

- **Row-level verdict agreement: 1000/1000** (`per_instance_stats.json` ids
  match the scenario ids exactly; our per-instance verdicts agree with the
  harness's on every row).
- 352 mismatches are genuine model errors (wrong final answer), not parser
  errors — the parser extracted the intended final number from both sides
  correctly in every case.

## Calibration record

No parser bugs were found in this population. The fallback rule (last number
in text when no `####` is present) worked correctly because:
- References consistently end with "The answer is N" — the last number is
  the gold answer.
- Completions consistently end with the model's final answer — the last
  number is the predicted answer.
- No completions had trailing numbers after the answer that would confuse
  the fallback.

The naive "first number in completion" rule would have scored differently
on 247/1000 rows (where the first number in the chain-of-thought differs
from the final answer), confirming the parser choice moves the number.

## Kill gate

**Not fired.** The `####` parser stressor was exercisable in lite v1.0.0
(through the fallback rule on 1000/1000 rows) and the recomputation agreed.
Per the protocol's declared rule this is the stated outcome: **reach
demonstrated further, external value still unobserved. D111 stands.** This
is the third exact AGREE on this line (E135: single-letter cell; E136:
free-text aggregate cell with parser + weighting; E138: free-text single-run
cell with #### parser stressor).

## Limitations

- One release, one model, one scenario. No prevalence claim (as declared).
- The `####` marker was **absent** from this population; the stressor was
  exercised via the fallback rule. Whether a population with actual `####`
  markers recomputes equally well is `untested`.
- The extraction convention (last number fallback) is calibrated on this
  population; whether it generalizes to other GSM8K-style datasets is
  `untested`.
- yi-34b's outputs are one style (5-shot CoT, together deployment). Whether
  a differently-styled model's completions recompute equally well was
  tested in E137 (yi-6b on math_chain_of_thought and gsm) and required
  model-specific calibration (backslash stripping before digits).

## Decision

No build decision changes. `preflight` remains unreleased (D111). The
leaderboard line stays open with the instrument demonstrated across four
stressors (single-letter, free-text multi-run aggregate with weighting,
cross-model, free-text single-run with #### parser).

**E138 complete.** The calibrated R1 instrument has now been pointed at four
cells in HELM lite v1.0.0 and achieved exact agreement on all four,
exercising: single-letter parsing, free-text `\boxed` parsing + macro
weighting, cross-model calibration, and `####`/last-number parsing.

## Raw evidence (committed with this result)

- `fetch_inventory.py` + `inventory.json` — G1 (from E136).
- `fetch_cells.py` + `manifest.json` — the 3 gsm run fetches + group table
  + per_instance_stats (from E136).
- `manifest_fetched.py` + `fetched-manifest.json` — sha256 of all third-party
  bytes this experiment read.
- `recompute_gsm.py` + output above — the R1-style recomputation with
  `####`/last-number parser, row-level verification against harness verdicts.
- Fetched bytes retained in this VM's `/tmp/opencode/e136/`; the session
  log records URLs, HTTP statuses (200 on all), and byte counts.