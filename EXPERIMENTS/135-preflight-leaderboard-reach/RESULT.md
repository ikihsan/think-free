<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E135 RESULT — R1 recomputation reaches a leaderboard's published number

Cell C2 (Stanford HELM, suite `lite`, release `v1.0.0`):
`mmlu:subject=abstract_algebra,method=multiple_choice_joint,model=01-ai_yi-34b`
(deployment `together/yi-34b`). Every URL below was fetched
unauthenticated from this VM on 2026-10-14; the fetch log is
`sessions/2026-10-14-003-probe-whether-preflight-r1-recomputation/commands.log`.

## Gates

- **G1 locatability: PASS.** The run's stated scores are public
  bytes: `stats.json` reports `exact_match` mean **0.2727272727272727**
  (`valid`) and **0.4** (`test`). The HELM website renders its
  numbers from the same public storage: `helm.js` fetches
  `${BENCHMARK_OUTPUT_BASE_URL}/releases/${RELEASE}/...`, and
  `BENCHMARK_OUTPUT_BASE_URL` is the `crfm-helm-public` GCS bucket
  (`observed`, this VM; `helm.js` retrieved 2026-10-14).
  C1's front page is reachable (`observed`: 44 KB HTML from the
  Open LLM Leaderboard space); C3's vote dataset is listed public
  but `gated: auto` (`observed` via the HF datasets API).
- **G2 reach: PASS on C2, FAIL on C1, FAIL on C3 as probed.**
  C2 ships, beside the number and unauthenticated: per-instance
  golds (`scenario_state.json`: 111 `request_states`, each with
  `references` where the gold carries tag `correct`), the model's
  raw completion (`result.completions[0].text`), the letter→choice
  mapping (`output_mapping`), the run's own spec (`run_spec.json`,
  incl. `max_tokens: 1`, `metric_specs: BasicMetric`), the
  per-instance verdicts (`per_instance_stats.json`), and the
  aggregates (`stats.json`). C1: the detail dataset
  `open-llm-leaderboard/gpt2-details` is auth-restricted
  (`observed`: "You must have access..."), and raw runs live in
  submitters' repos, not beside the cell — the shape the protocol
  declared in advance. C3: votes are gated and the published Elo
  is fit on the full vote population, not the published sample.
- **G3 recomputation: AGREE.** `recompute.py` scores from
  `scenario_state.json` alone — gold from the `correct`-tagged
  reference, parse = first completion character that is a key of
  `output_mapping`, correct iff parse == gold letter. It never
  reads a verdict column. Result: `valid` **3/11 = 0.272727…**
  and `test` **40/100 = 0.4000**, equal to the published means to
  the full printed precision. `reconcile.py` then recomputed all
  111 rows and compared against the harness's own per-instance
  verdicts: **111/111 agree, 0 mismatch**.

## Kill gate

Not fired. The gate required G2 to fail on **all three** pre-named
cells; it passed on C2. The leaderboard direction therefore stays
**open**, and per the protocol's declared rule this outcome — G2
passing with recomputation agreed — is a weaker, stated outcome:
**reach demonstrated, external value still unobserved. D111 stands.**

## What this establishes (`observed` unless noted)

1. A leaderboard cell's published number is recomputable from
   published per-row predictions and golds, unauthenticated, with a
   stdlib-only script (`recompute.py`, 71 lines). This is the
   format E134 said the next action should test, and the adapter
   shape is the one E128–E133 predicted: a few lines naming the
   directory and join key.
2. HELM's site and its run storage are the same bytes — the number
   a person reads on the leaderboard is the `stats.json` mean, so
   "recompute the run" and "recompute the leaderboard cell" are the
   same operation here (`source-supported`: `helm.js` fetch paths).
3. The published `valid`/`test` split of this cell is 11/100 rows;
   the pooled 111-row mean (0.3874) is **not** what the leaderboard
   publishes for either split. A recomputation that pooled splits
   would falsely report disagreement — the split key is part of the
   instrument, not a detail.

## Limitations (`declared before the run` in `PROTOCOL.md`, plus)

- **The parse rule was never stressed.** All 111 completions are
  single letters (`max_tokens: 1` in `run_spec.json`; finish reason
  `length` on 111/111; no completion contains two choice letters).
  Agreement therefore validates the *plumbing* (join, gold, split,
  aggregation), not a parser. A cell whose completions are free text
  is the honest next test.
- One cell, one suite, one release, one model. No prevalence claim
  (3 cells are a reach probe, as declared).
- The mapping-through-`BasicMetric` mechanism (letter → choice text
  inside the metric) is `inferred` from the 111/111 row agreement,
  not read from HELM's source.
- C1 and C3 are recorded as probed-and-failed-on-shape, not
  surveyed: one dataset URL and one dataset listing each.

## Decision

No build decision changes. `preflight` remains unreleased (D111).
The leaderboard line stays open with one named next action:

**Point R1 at a leaderboard cell whose completions are free text
and whose published number is an aggregate over multiple runs
(e.g. a HELM scenario aggregate or a suite mean), where a parser
and a weighting rule are both exercised.** That is the first cell
where recomputation could disagree with the published number for a
reason other than plumbing.

## Raw evidence (committed with this result)

- `recompute.py` — the R1-style recomputation (reads no verdict).
- `reconcile.py` — split-aware reconciliation and row-by-row check.
- `completion_shapes.py` — the parse-rule stress characterization.
- `manifest_fetched.py` + `fetched-manifest.json` — sha256, byte
  count, and URL of every third-party byte the recomputation read
  (repository rule: bulk third-party input is recorded by hash and
  never committed; re-fetching the URLs must reproduce the hashes).
- Fetched bytes retained in this VM's `/tmp/opencode/` (session
  log records URLs, HTTP statuses, and byte counts; 200 on every
  run-output fetch).
