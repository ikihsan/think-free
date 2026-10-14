<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E137 RESULT — cross-model agreement on a free-text, multi-run HELM aggregate cell

Cell (selected by the protocol's pre-declared rule): **`math_chain_of_thought`**,
HELM lite `v1.0.0`, model **`01-ai/yi-6b`** — the first model in the release
inventory other than `01-ai/yi-34b` (selection rule pre-declared in E136's
RESULT, no substitution). Every URL below was fetched unauthenticated from
this VM on 2026-10-14; every byte is in `fetched-manifest.json` by sha256.

## Gates

- **G1 inventory: PASS.** The E136 inventory (868 run dirs, 9 families, 31
  models) confirmed `math` runs exist for `01-ai_yi-6b` across all 7 subjects
  (`observed`; `inventory.json`).
- **G2 reach: PASS.** 28/28 fetches 200: 7 math runs × 3 files
  (`run_spec.json`, `scenario_state.json`, `stats.json`) + 1 group table +
  7 `per_instance_stats.json`. Free text confirmed (`observed`): `method:
  generation`, `max_tokens: 400`, `max_train_instances: 8`; completion lengths
  mean 179 / max 1188 chars in algebra; 437 rows total.
- **G3 recomputation: AGREE** (below).

## The weighting rule, re-verified before comparison

The protocol's hypothesis: the published MATH row is the unweighted mean of
the 7 per-subject valid-split means. `observed` from the bytes:

- The 7 per-subject group tables' Yi (6B) values equal each run's own
  `stats.json` mean to full printed precision.
- Their unweighted mean = **0.12585197340399298** = the aggregate table's
  value, difference **0.0**.
- Corroboration: the aggregate table's `# eval` column for Yi (6B) is
  62.428571… = 437/7 — exactly the pooled instance count over the 7 runs.

So the site's aggregation is confirmed as macro-mean-of-subject-means, and
the grouping key is part of the instrument (the pooled micro-mean is
0.14645308924485126 — a recomputation that ignored the subject key would
falsely report disagreement, the same lesson as E135's split key and E136's
subject key).

## G3 recomputation — agree

R1 discipline held throughout: every verdict was recomputed from
`scenario_state.json` alone; `stats.json` and `per_instance_stats.json`
were loaded only after, for comparison and reconciliation. Extraction
(calibrated against the harness's own verdicts in E136, fixed against 437
per-instance verdicts): gold = last `\boxed{...}` in the correct reference;
pred = last `\boxed{...}` in the completion; a completion with no `\boxed`
scores 0. Verdict = 1.0 iff `normalize(pred) == normalize(gold)` exactly
(latex-to-plain canonical forms, brace-insensitive `\frac`,
`\left/\right/$/\circ/\%` stripped, **backslash stripped only before
letters** — not before digits, which fixed one yi-6b-specific case where
`\37` ≠ `37`).

| subject run | recomputed | printed run mean | match | row verdicts agree |
|---|---|---|---|---|
| algebra | 27/135 = 0.2 | 0.2 | exact | 135/135 |
| counting_and_probability | 3/39 = 0.07692307692307693 | 0.07692307692307693 | exact | 39/39 |
| geometry | 5/38 = 0.13157894736842105 | 0.13157894736842105 | exact | 38/38 |
| intermediate_algebra | 3/52 = 0.057692307692307696 | 0.057692307692307696 | exact | 52/52 |
| number_theory | 3/30 = 0.1 | 0.1 | exact | 30/30 |
| prealgebra | 15/86 = 0.1744186046511628 | 0.1744186046511628 | exact | 86/86 |
| precalculus | 8/57 = 0.14035087719298245 | 0.14035087719298245 | exact | 57/57 |

- **Row-level verdict agreement: 437/437** (`per_instance_stats.json` ids
  match the scenario ids exactly, no extra verdict rows).
- **RECOMPUTED macro (mean of the 7 subject means): 0.12585197340399298.**
- **PUBLISHED group macro for yi-6b: 0.12585197340399298.**
- **AGREE — equal to full printed precision, diff 0.0.**
- 153 completions carry no `\boxed`; the harness scored 0 of them — the
  no-box fallback question is closed for this population (no evidence of a
  non-boxed extraction path).

## Calibration record (yi-6b-specific fix)

The yi-6b model produced one completion containing `\37` (lone backslash
before digits) where the gold was `37`. The harness scored this 0.0. The
E136 normalization rule (strip all backslashes) would have incorrectly
scored this 1.0. The fix: backslash stripping is now **only before letters**
(LaTeX commands like `\frac`, `\boxed`), not before digits. This was
calibrated against the harness's per-instance verdict for this row, never
against the published aggregate.

## Kill gate

**Not fired.** The `math_chain_of_thought` runs for `01-ai/yi-6b` were
present in the release (all 7 subject runs), and the recomputation agreed.
Per the protocol's declared rule this is the stated outcome: **cross-model
reach demonstrated, external value still unobserved. D111 stands.** This is
the third exact AGREE on this line (E135: single-letter cell; E136:
free-text aggregate cell, parser + weighting both exercised; E137: second
model on the same cell).

## Limitations

- One release, two models, one group. No prevalence claim (as declared).
- The operator (normalized-string equality) was **inferred** from the
  harness's own verdicts, not read from HELM's source; it is validated on
  437/437 rows here (yi-6b) and 437/437 rows (yi-34b), and could differ on
  answer forms absent from these populations.
- The extraction convention (last `\boxed`) is calibrated on these
  populations; 153 (yi-6b) and 95 (yi-34b) no-boxed completions all score 0
  in both my rule and the harness's, so the population does not exercise a
  fallback path.
- Whether a differently-styled model's completions recompute equally well is
  `untested` — the named next action from E136 was cross-model agreement,
  which is now tested. The `gsm` cell (free-text, `####` number-extraction
  parser, single run) remains the named second target for a different parser
  stressor.

## Decision

No build decision changes. `preflight` remains unreleased (D111). The
leaderboard line stays open with one named next action:

**E138: point the calibrated instrument at the `gsm` cell** (free-text,
`####` number-extraction parser, single run) — the parser stressor that
E136's pre-named cell F identified but was not needed because the
`math_chain_of_thought` cell exercised both stressors.

## Raw evidence (committed with this result)

- `fetch_cells_yi6b.py` + `manifest.json` — G2 (28 fetches, all 200).
- `manifest_fetched_yi6b.py` + `fetched-manifest.json` — sha256 of all 29
  third-party bytes this experiment read.
- `recompute_math_yi6b.py` + `recompute_math_out.json` — the R1-style
  recomputation, the 7-subject table, macro/micro, and the calibration
  record's inputs.
- Fetched bytes retained in this VM's `/tmp/opencode/e137/`; the session
  log records URLs, HTTP statuses (200 on all 28), and byte counts.