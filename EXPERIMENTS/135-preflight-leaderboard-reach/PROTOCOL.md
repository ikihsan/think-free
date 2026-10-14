<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E135 PROTOCOL — does R1 recomputation reach the number a leaderboard publishes?

Pre-declared 2026-10-14, before any leaderboard byte is fetched. Commit order
is the evidence: this file precedes the fetch log.

## The question

E134 closed the release question (D111) on run-output shape: a real
`lm-evaluation-harness` run is clean, its printed rates recompute from its own
shipped bytes, and `preflight` has no observed external value there. E134's
decision names the one next action worth making: *does the same adapter and
the same R1 reach the format a **leaderboard** publishes, where the number is
read by people who never open `results.json`?* This experiment is that action.

## Claim labels in this file

`untested` unless marked `observed` (this VM, this session) or
`source-supported` (a retrieved page, cited with URL and date).

## Pre-named cells (chosen before any fetch, for diversity of shape)

| cell | leaderboard | number as published | shape expected (`untested`) |
|---|---|---|---|
| C1 | HuggingFace Open LLM Leaderboard v2 | per-model average + per-benchmark scores | aggregates only; raw runs live in submitters' repos, not beside the cell |
| C2 | Stanford HELM (CRFM) leaderboard | per-scenario metrics (e.g. MMLU) | HELM publishes per-instance predictions and golds beside the number |
| C3 | LMSys Chatbot Arena leaderboard | Bradley-Terry / Elo rating per model | votes published as a public conversations dataset; rating recomputable in principle |

No substitution: if a cell's front page is unreachable, the cell is recorded
`unreachable`, not replaced by an easier host.

## Gates (declared before the run)

- **G1 locatability.** ≥1 of the 3 pre-named cells yields a stated numeric
  score via unauthenticated fetch. Evidence: URL, HTTP status, quoted number.
- **G2 reach.** For a cell with a score, per-row model outputs + gold labels
  (or votes, for C3) + the scoring rule reach unauthenticated, in enough form
  that R1-style recomputation (never reading the verdict column) is
  implementable in principle. Evidence: URLs, byte counts, schema note.
- **G3 recomputation (conditional).** If G2 passes on ≥1 cell, run the
  recomputation and report agree/disagree with the published number.

## Kill gate (declared before the run)

If G2 fails on **all 3** cells — no leaderboard cell ships per-row outputs,
golds, and scoring rule unauthenticated — then R1 does not reach
leaderboard-published numbers, the leaderboard direction **CLOSES**, and D111
stands with this reason recorded. No fourth host is added afterwards; adding
one after a negative would be indistinguishable from shopping for a positive.

## What would reopen D111

G2 passing on ≥1 cell **and** G3 disagreeing with a published number (a real
defect observed in the wild), or G2 passing with recomputation agreed (reach
demonstrated, value still unobserved — a weaker, stated outcome, not a
reopening by itself).

## What this does not show (declared in advance)

- Anything about scoring quality or any model's behaviour.
- Any prevalence claim: 3 cells are a reach probe, not a survey.
- Anything about run-output shape: that was E134 and it is closed.
