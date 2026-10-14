<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E137 PROTOCOL — cross-model agreement on a free-text, multi-run HELM aggregate cell

Pre-declared 2026-10-14, before any leaderboard byte is fetched. Commit order
is the evidence: this file precedes the fetch log.

## The question

E136 recomputed the `math_chain_of_thought` cell for `01-ai/yi-34b` and
achieved an exact AGREE (437/437 row verdicts, macro mean diff 0.0). The
calibrated instrument (last-`\boxed` extraction, normalized-string equality)
was stressed against two parser bugs and one over-permissive operator, each
fixed against the harness's per-instance verdicts. The named next action from
E136: *point the calibrated instrument at a second model's
`math_chain_of_thought` cell — cross-model agreement is the one reach question
still untested.*

## Claim labels in this file

`untested` unless marked `observed` (this VM, this session) or
`source-supported` (a retrieved page, cited with URL and date).

## Scope (declared in advance)

- Leaderboard: HELM lite, release `v1.0.0` — the same release E135 and E136
  validated end to end.
- Primary model: **`01-ai/yi-6b`** — the first model in the release inventory
  other than `01-ai/yi-34b` (selection rule pre-declared in E136's RESULT,
  no substitution).
- No host or release substitution: if the pre-named cell's bytes are absent,
  it is recorded `absent`, not replaced by another release or an easier host.

## Target cell

| cell | target | shape expected (`untested`) | stressor |
|---|---|---|---|
| M | `math_chain_of_thought`, model `01-ai_yi-6b` | free-text completions (chain-of-thought generation, `max_tokens: 400`); published as the mean over 7 subject runs | parser + weighting rule + cross-model |

## Declared rules (before any fetch)

**Parse rule** (calibrated in E136, fixed against 437 harness verdicts):
- Gold = last `\boxed{...}` in the correct reference
- Pred = last `\boxed{...}` in the completion
- A completion with no `\boxed` scores 0
- Verdict = 1.0 iff `normalize(pred) == normalize(gold)` exactly (latex-to-plain
  canonical forms, brace-insensitive `\frac`, `\left/\right/$/\circ/\%` stripped)
- **No numeric-equivalence fallback** (E136: 3/2 vs 1.5 scores 0 in the harness)

**Weighting hypothesis** (verified in E136 for yi-34b, to be re-verified for
yi-6b): the published MATH row is the unweighted mean of the 7 per-subject
valid-split means. The RESULT will read the site's aggregation code (the
`helm.js` bundle E135 fetched and hashed) and cite it before comparing. Both
the macro-mean-of-means and the pooled micro-mean are computed and reported.

## Gates (declared before the run)

- **G1 inventory.** The lite v1.0.0 run inventory confirms `math` runs exist
  for `01-ai_yi-6b` across all 7 subjects. Evidence: URLs, HTTP status, byte counts.
- **G2 reach.** For each of the 7 subject runs: `scenario_state.json` and
  `run_spec.json` fetch 200 unauthenticated; completion shapes characterized
  (free text confirmed via `max_tokens: 400`, completion lengths, finish reasons).
  Evidence: URLs, byte counts, schema note.
- **G3 recomputation.** Report agree/disagree between the calibrated
  recomputation (never reading a verdict column) and the published number,
  per subject and as the macro mean.

## Kill gate (declared before the run)

If `math_chain_of_thought` runs for `01-ai/yi-6b` are **absent from the
release** (any of the 7 subject runs missing), then E137 records `absent for
this model` and the cross-model question is `not_exercisable`. The model
substitution rule from E136's protocol applies: the same cell is then re-run
for the next model in the inventory that has it, and the model switch is
recorded as an explicit deviation.

## What would reopen D111

G3 disagreeing with a published number on a cell whose per-run bytes are
complete and public: a leaderboard number that does not recompute from its own
published bytes is a real defect in the wild, and it is the first external
value the R1 instrument has had (D111, E134). Agreement on both models is the
weaker, stated outcome: reach demonstrated further across models, value still
unobserved; D111 stands.

## What this does not show (declared in advance)

- Anything about scoring quality or any model's behaviour.
- Any prevalence claim: one release, two models, one group — not a survey of
  leaderboards.
- That the recomputation is correct in general: agreement with the harness's
  own per-instance verdicts (E135: 111/111, E136: 437/437) is the correctness
  anchor; agreement with a published number is reach, not proof.