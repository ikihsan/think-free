<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E136 PROTOCOL — does R1 recomputation reach a free-text, multi-run HELM aggregate cell?

Pre-declared 2026-10-14, before any leaderboard byte is fetched. Commit order
is the evidence: this file precedes the fetch log.

## The question

E135 named one next action: *point R1 at a leaderboard cell whose completions
are free text and whose published number is an aggregate over multiple runs,
where a parser and a weighting rule are both exercised.* E135's own cell
(MMLU `abstract_algebra`, 111 single-letter completions) validated the
plumbing — join, gold, split, aggregation — but never stressed the parser or
the weighting rule. This experiment is that action, inside the same leaderboard
and release E135 validated end to end: **HELM lite, release `v1.0.0`**.

## Claim labels in this file

`untested` unless marked `observed` (this VM, this session) or
`source-supported` (a retrieved page, cited with URL and date).

## Scope (declared in advance)

- Leaderboard: HELM lite, release `v1.0.0` — the suite E135 showed renders
  from public GCS bytes (`crfm-helm-public`, `lite/benchmark_output/`).
- Primary model: `01-ai/yi-34b` — the model E135 ran; at least one of its runs
  is known to exist (`observed`, E135).
- No host or release substitution: if a pre-named cell's bytes are absent, it
  is recorded `absent`, not replaced by another release or an easier host.

## Pre-named candidate cells

Named from public knowledge of HELM's scenario structure; every shape claim
below is `untested` until the inventory fetch records what the release
contains.

| cell | target | shape expected (`untested`) | stressor |
|---|---|---|---|
| F | `gsm8k:default,model=01-ai_yi-34b` | free-text completions (chain-of-thought ending in `#### N`); metric `exact_match`-family on an extracted number | parser |
| A | the `mmlu` scenario row for `01-ai/yi-34b` | published number is the aggregate over the 57 subject runs (`mmlu:subject=*,method=multiple_choice_joint,model=01-ai_yi-34b`) | weighting rule |
| B | any other scenario in the release whose completions are multi-token | to be recorded from the inventory | whichever applies |

Cell selection rule (declared in advance): if the inventory contains a
scenario that is *both* free-text and a multi-run aggregate, that scenario is
the primary cell and F/A are recorded as not needed. Otherwise F and A run
separately, each testing its own stressor. If the inventory contains no
free-text scenario at all, the parser stressor is recorded `not exercisable`
and only A runs.

**Model substitution rule** (`inferred` need, declared here): the stressor is
the cell's shape, not the model. If a pre-named cell has no run for
`01-ai/yi-34b`, the cell is recorded `absent for this model`; the same cell is
then re-run for the first model in the release inventory that has it, and the
model switch is recorded as an explicit deviation, never a silent
substitution.

## Declared rules (before any fetch)

**Parse rule for cell F** (GSM8K's public evaluation convention): extract the
number after the *last* `####` in the completion; if no `####`, take the last
number in the completion; strip commas and surrounding whitespace; correct iff
the extracted number equals the gold number (the reference answer after its
own final `####`, comma-stripped). The metric's comparison operator is read
from `run_spec.json`'s `metric_specs` and quoted in the RESULT before
comparison; the extraction rule above is operator-independent. Also recorded:
how often the naive rule (first number in the completion) would change the
score, to show the parser choice moves the number.

**Weighting hypothesis for cell A** (`untested`): the site's MMLU scenario row
is the unweighted mean of the per-subject valid-split means. The RESULT reads
the site's aggregation code — the `helm.js` bundle E135 already fetched and
hashed — and cites it before comparing. Both the macro-mean-of-means and the
pooled micro-mean are computed and reported, so a wrong weighting shows as a
named disagreement, not an unexplained one.

## Gates (declared before the run)

- **G1 inventory.** The lite v1.0.0 run inventory is locatable unauthenticated
  (GCS listing of `lite/benchmark_output/runs/v1.0.0/`). Evidence: URL,
  HTTP status, and the scenario names it yields.
- **G2 reach.** For each cell run: every needed run's `scenario_state.json`
  and `run_spec.json` fetch 200 unauthenticated; completion shapes
  characterized (free text confirmed via `max_tokens`, completion lengths,
  finish reasons). Evidence: URLs, byte counts, schema note.
- **G3 recomputation.** For each cell: report agree/disagree between the
  R1-style recomputation (never reading a verdict column) and the published
  number, per split where the published number is split-specific.

## Kill gate (declared before the run)

If **no** stressor is exercisable in lite v1.0.0 — no free-text scenario in
the inventory AND no multi-run aggregate cell — then E136 closes the
stress-test step of the leaderboard direction with that reason recorded, and
no other release is added afterwards (adding one after a negative would be
indistinguishable from shopping for a positive).

## What would reopen D111

G3 disagreeing with a published number on a cell whose per-run bytes are
complete and public: a leaderboard number that does not recompute from its own
published bytes is a real defect in the wild, and it is the first external
value the R1 instrument has had (D111, E134). Agreement on both cells is the
weaker, stated outcome: reach demonstrated further, value still unobserved;
D111 stands.

## What this does not show (declared in advance)

- Anything about scoring quality or any model's behaviour.
- Any prevalence claim: one release, at most two models, two stressors — not
  a survey of leaderboards.
- That the recomputation is correct in general: agreement with the harness's
  own per-instance verdicts (E135: 111/111) is the correctness anchor;
  agreement with a published number is reach, not proof.
