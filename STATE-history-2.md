<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Session history, continued

What each older session changed, newest first. Continues
[`STATE-history.md`](STATE-history.md), which holds sessions 005 through 037 and
reached the 300-line cap on 2026-10-04. Identifiers here are the same ones
`STATE.md` uses.

## What changed in session 025, VM 0944

The screen `STATE.md` had been carrying as next action 3, run and recorded.

- `RESEARCH/SYNTHESIS.md` — all sixteen candidates from A–F in one table, three
  screens, and a ranked shortlist. Applying F's C1–C6 literally yields six
  "not applicable": they describe a built repository and cannot discriminate six
  unimplemented candidates. A third question does the work — *if the gate
  passes, what gets built* — and it is what rules out E1, the cheapest
  experiment in the repository, because jitter is already in every client
  library and a pass would confirm a 2015 blog post.
- Finding no single report contains: **every promoted candidate in A, B and C
  needs a person or a room this repository cannot reach** — a planner, an
  experienced knitter's hands, sensors in a room. Three tasks (T-0005/6/0007)
  bought A1 a falsification, not a decision. Only D, E and F proposed things
  testable on this machine, and D proposed nothing.
- `DECISIONS.md` reached the 300-line cap and was split by invariant into
  `DECISIONS-FOUNDATION.md` (mission, workspace, evidence) and
  `DECISIONS-PRACTICE.md` (recording, verifying, publishing, gating). Entries
  moved verbatim; numbering unchanged.
- D020 records the screen as a gate and keeps C1–C6 as a stage-D release check
  rather than a candidate screen that cannot fail.
- `reconcile.IMPLICATIONS` gained an explicit `any`/`all` mode per event kind, so
  the decision gate survives the split without weakening the `experiment_result`
  gate, which still demands both `HYPOTHESES.md` and `FAILURES.md`. Five new
  tests in `tests/test_doc_gaps.py`; 173 tests pass.
- Repaired two tracked documents that were false: `RESEARCH.md` and `ROADMAP.md`
  both described investigations E and F as "not run" although both are sealed
  and their tasks are done.

## What changed in session 020, VM 0947

- `EXPERIMENTS/003-information-sufficiency/` — one synthetic witness per held
  candidate: two realities with identical permitted inputs and a required
  divergent output. W1 and W3 survive; W2 is information-insufficient as
  specified. `task verify T-0008` exit 0.
- `HYPOTHESES.md` records the E002 gate and its per-candidate outcome;
  `FAILURES.md` F007 records the knitting input-set finding.
- Push credentialing repaired **on that VM only**: App ID recovered, JWT generator
  added under `~/.config/github-app/`. It never reached `instance-20260717-0944`,
  which is what session 040 found.

## What changed in session 022, VM 0947

T-0010 completed: `EXPERIMENTS/004-knitting-stage-a/` runs the knitting
candidate's own Stage A. A cheap per-error local heuristic was compared against an
exhaustive minimum-cost oracle on 10 synthetic cases (9 solved, 1 refused). The
heuristic is valid on all 9 solved cases (never misses an error, never emits an
illegal closure), refuses unsupported shaping, and is suboptimal on exactly one
constructed shared-release case (local 5 vs optimum 3) — the
`same_column_stack` case a per-error rule cannot see. No full-row-release
degeneration. Verdict `narrow`, not `abandon`; the next test is a
bounded-neighbourhood planner against the same oracle before Stage-B physical
work. `task verify T-0010` exit 0.
