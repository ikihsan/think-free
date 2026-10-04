<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Session history, continued

What each older session changed, newest first. Continues
[`STATE-history.md`](STATE-history.md), which holds sessions 005 through 037 and
reached the 300-line cap twice on 2026-10-04 — once at session 005, and again
when session 012 was added to it. Identifiers here are the same ones
`STATE.md` uses.

## What changed in session 027, VM 0947

T-0014 completed: `EXPERIMENTS/006-ventilation-measurement-design/` ran the kill
gate `RESEARCH/C.md` predeclared for its ventilation candidate, and **the gate was
not met**.

- **Design.** Two-room mass-balance world with an occupied neighbour, one sensor
  in the measured room, six paired hypothesis families whose passive trace in that
  room is identical by construction, three conditions (specified, changing
  weather, poor mixing), one shared grid fitter, and an identical budget for all
  three protocols: 12 sample slots and one decision. The adaptive rule was handed
  the surviving pair for free and chose from `door_open`, `co_locate_b`,
  `window_a_open`, `noop`.
- **Result.** Pairwise discrimination on specified cases: passive 0.333 (chance),
  prescribed door-open **0.833**, adaptive **0.792**. The gate required adaptive
  to beat fixed and it did not. Under poor mixing adaptive was better (0.708 vs
  0.542) and the false-precise gate was met but near-vacuously (0.000 vs 0.021).
  The unidentifiable control — hypotheses differing only in a sensor offset —
  failed for all three protocols, as it must.
- **Verdict.** The measurement-design advantage is not demonstrated and the
  formulation is **stopped**: `FAILURES.md` F008. The narrower observation that
  survives is that reading a second sensor is more robust under poor mixing than
  acting on the measured room.
- One design correction was made before any result was recorded: the first build
  paired hypotheses whose room-A traces differed by 32 ppm RMS against 6 ppm
  noise, which made the comparison vacuous. It was rejected and rebuilt so the
  passive trace is identical by construction.
- `FAILURES.md` reached the 300-line cap and was split by invariant into
  `FAILURES-findings.md` (F001–F008) and a stub carrying the live list.

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

## What changed in sessions 038–040, VM 0944

Moved here from `STATE.md` on 2026-10-04 (T-0033) when the reload point
passed 300 lines again. Newest first within the group.

- **Session 040, VM 0944 (T-0029, D030, F016, F017).** `doctor` reported a property it
  never read — `credentials none present` for a working App credential, for the recorded
  `instance-20260717-0947` failure, and for no credential at all. It now reports the
  configured `credential.helper`, whether it is executable, App key files by mode,
  dependencies outside `~/.config`, and whether `git credential fill` obtains a
  credential, with `configured` explicitly not meaning it can push. It found a live
  defect here: the helper invoked `/tmp/github-app-jwt.sh`, repaired and proven by
  deleting it. **F016:** this session's own harness overwrote the real
  `~/.gitconfig`. **F017:** clock-stamped generated dates, found independently of
  D029; the landed implementation was kept rather than shipping two.
- **Session 039, VM 0944 (T-0023).** Two public operations documents told a fresh
  VM something untrue: a Python floor of 3.11+ invented from one machine's 3.14.6
  (this VM runs 3.8.10 with the suite green), and `github-app.md` claiming no App
  exists while 123 of 133 commits carry a `[bot]` App identity. Both repaired.
  **The App's real permissions remain unverified** — no agent can read them.
- **Session 038, VM 0944 (T-0022).** `origin release check` enforces
  `RELEASE-MANIFEST.md`, which three times said nothing did. Nine top-level
  entries had been classified by neither table; three declared public paths did
  not exist; the front door had no declared state. All closed in the same commit
  as the check.
