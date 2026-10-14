<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E136 RESULT — R1 recomputation reaches a free-text, multi-run aggregate cell

Cell (selected by the protocol's pre-declared rule): **`math_chain_of_thought`**,
HELM lite `v1.0.0`, model `01-ai/yi-34b` — the scenario family that is BOTH
free-text (chain-of-thought generation completions, `max_tokens: 400`) AND a
multi-run aggregate (published as the mean over 7 subject runs). Every URL
below was fetched unauthenticated from this VM on 2026-10-14; every byte is
in `fetched-manifest.json` by sha256.

## Gates

- **G1 inventory: PASS.** GCS listing of
  `lite/benchmark_output/runs/v1.0.0/` (JSON API, delimiter `/`, one page)
  yields **868 run dirs, 9 scenario families, 31 models** (`observed`;
  `inventory.json`). Families: `commonsense`, `gsm`, `legalbench`, `math`,
  `med_qa`, `mmlu`, `narrative_qa`, `natural_qa`, `wmt_14`. `yi-34b` has 28
  runs, including one per `math` subject, `gsm`, and 5 `mmlu` subjects.
- **Cell selection (protocol rule applied).** `math` is the both-properties
  cell → **primary**. Pre-named cell F (`gsm`) and cell A (`mmlu`) are
  recorded **`not needed`**: F is free-text but a single run; A is an
  aggregate but single-letter. Their existence is `observed` (inventory) and
  their bytes are fetched (manifest); recomputation was not run on them, per
  the rule.
- **G2 reach: PASS.** 48/48 fetches 200: 40 run files (7 math runs +
  gsm + 5 mmlu runs × `run_spec`/`scenario_state`/`stats`), the published
  group table `groups/math_chain_of_thought.json`, and 7
  `per_instance_stats.json`. Free text confirmed (`observed`):
  `method: generation`, `max_tokens: 400`, `max_train_instances: 8`;
  completion lengths mean 179 / max 1188 chars in algebra; 437 rows total.
- **G3 recomputation: AGREE** (below).

## The weighting rule, verified before comparison

The protocol's hypothesis: the published MATH row is the unweighted mean of
the per-subject valid-split means. `observed` from the bytes:

- The 7 per-subject group tables' Yi (34B) values equal each run's own
  `stats.json` mean to full printed precision.
- Their unweighted mean = **0.37478395850488877** = the aggregate table's
  value, difference **0.0**.
- Corroboration: the aggregate table's `# eval` column for Yi (34B) is
  62.428571… = 437/7 — exactly the pooled instance count over the 7 runs.

So the site's aggregation is confirmed as macro-mean-of-subject-means, and
the grouping key is part of the instrument (the pooled micro-mean is
0.43707093811510296 — a recomputation that ignored the subject key would
falsely report disagreement, the same lesson as E135's split key).

## G3 recomputation — agree

R1 discipline held throughout: every verdict was recomputed from
`scenario_state.json` alone; `stats.json` and `per_instance_stats.json`
were loaded only after, for comparison and reconciliation. Extraction
(calibrated against the harness's own verdicts): gold = last `\boxed{...}` in
the correct reference; pred = last `\boxed{...}` in the completion; a
completion with no `\boxed` scores 0.

| subject run | recomputed | printed run mean | match | row verdicts agree |
|---|---|---|---|---|
| algebra | 76/135 = 0.562962962962963 | 0.562962962962963 | exact | 135/135 |
| counting_and_probability | 12/39 = 0.3076923076923077 | 0.3076923076923077 | exact | 39/39 |
| geometry | 12/38 = 0.3157894736842105 | 0.3157894736842105 | exact | 38/38 |
| intermediate_algebra | 20/52 = 0.38461538461538464 | 0.38461538461538464 | exact | 52/52 |
| number_theory | 5/30 = 0.16666666666666666 | 0.16666666666666666 | exact | 30/30 |
| prealgebra | 46/86 = 0.5348837209302325 | 0.5348837209302325 | exact | 86/86 |
| precalculus | 20/57 = 0.3508771929824561 | 0.3508771929824561 | exact | 57/57 |

- **Row-level verdict agreement: 437/437** (`per_instance_stats.json` ids
  match the scenario ids exactly, no extra verdict rows).
- **RECOMPUTED macro (mean of the 7 subject means): 0.37478395850488877.**
- **PUBLISHED group value: 0.37478395850488877.**
- **AGREE — equal to full printed precision, diff 0.0.**
- 95 completions carry no `\boxed`; the harness scored 0 of them — the
  no-box fallback question is closed for this population (no evidence of a
  non-boxed extraction path).

## Calibration record (what the stress found, and what fixed it)

The first rule (normalize + a numeric-equality fallback) agreed with the
harness on 432/437 rows and would have **disagreed** with the published
number (macro 0.3775312112521415). The 5 disagreeing rows decomposed into
two kinds of my own error, each fixed against the harness's per-instance
verdicts — never against the published aggregate:

| row | gold | pred | first rule | harness | the fix |
|---|---|---|---|---|---|
| counting…/id51 | `\frac{7}{12}` | `\frac{35}{60}` | 1 | 0 | numeric fallback was wrong: the operator is normalized-string equality, not numeric equivalence |
| counting…/id87 | `\frac14` | `\frac{1}{4}` | 0 | 1 | parser bug: brace-less `\frac14` unhandled |
| intermediate…/id74 | `\frac{3}{2}` | `1.5` | 1 | 0 | same as id51 — 3/2 and 1.5 are not equivalent to this operator |
| prealgebra/id137 | `\frac{4}{11}` | `\frac{44}{121}` | 1 | 0 | same as id51 |
| prealgebra/id168 | `8\frac47` | `8\frac{4}{7}` | 0 | 1 | parser bug: brace-less mixed number |

Final rule: gold/pred = last `\boxed{...}`; verdict = 1.0 iff
`normalize(pred) == normalize(gold)` exactly (latex-to-plain canonical
forms, brace-insensitive `\frac`, `\left/\right/$/\circ/\%` stripped).
437/437 after the fix. The calibration direction is recorded because it
matters: the anchor was 437 per-instance verdicts, not the one published
number, and the first rule's error pointed toward a false disagreement.

## Kill gate

**Not fired.** Both stressors were exercisable in lite v1.0.0 and the
recomputation agreed. Per the protocol's declared rule this is the weaker,
stated outcome: **reach demonstrated further, external value still
unobserved. D111 stands.** This is the second exact AGREE on this line
(E135: single-letter cell; E136: free-text aggregate cell, parser +
weighting both exercised).

## One published-coverage gap, recorded as an observation

The release holds `math` runs for 31 models; the published
`math_chain_of_thought` group table has 30 rows. The model with runs and
no published row is **`anthropic_claude-instant-v1`** (all 7 subject runs
present in the release; no row under any display variant). For that model
there is no published number to recompute — a coverage gap in the
published table, not a recomputation disagreement, and not explained by
these bytes (the site's model-selection rule is not in them). Recorded
because it bounds what "recompute the leaderboard" can ever be asked to
do: the instrument can only check cells the leaderboard publishes.

## Limitations

- One release, one model, one group. No prevalence claim (as declared).
- The operator (normalized-string equality) was **inferred** from the
  harness's own verdicts, not read from HELM's source; it is validated on
  437/437 rows here, and could differ on answer forms absent from this
  population.
- The extraction convention (last `\boxed`) is calibrated on this
  population; 95 no-boxed completions all score 0 in both my rule and the
  harness's, so the population does not exercise a fallback path.
- yi-34b's outputs are one style (8-shot CoT, together deployment). Whether
  a differently-styled model's completions recompute equally well is
  `untested` — that is the named next action.

## Decision

No build decision changes. `preflight` remains unreleased (D111). The
leaderboard line stays open with one named next action:

**E137: point the calibrated instrument at a second model's
`math_chain_of_thought` cell** — the first model in the release inventory
other than `01-ai/yi-34b` (selection rule pre-declared in E137's protocol,
no substitution). This is the strongest remaining reach question: E135 and
E136 both recomputed one model's outputs, so agreement across models is
`untested`. The `gsm` cell (free-text, `####` number-extraction parser,
single run) is the named second target.

## Raw evidence (committed with this result)

- `fetch_inventory.py` + `inventory.json` — G1 (868 run dirs, 9 families).
- `fetch_cells.py` + `manifest.json` — the 40 run/group fetches, by URL.
- `manifest_fetched.py` + `fetched-manifest.json` — sha256 of all 48
  third-party bytes this experiment read.
- `recompute_math.py` + `recompute_math_out.json` — the R1-style
  recomputation, the 7-subject table, macro/micro, and the calibration
  record's inputs.
- `disagree_rows.py` — dumps the 5 first-rule disagreements with forms.
- Fetched bytes retained in this VM's `/tmp/opencode/e136/`; the session
  log records URLs, HTTP statuses (200 on all 48), and byte counts.
