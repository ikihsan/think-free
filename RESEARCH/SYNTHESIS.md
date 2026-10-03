# Cross-report synthesis — the screen applied to all six investigations

<!-- origin-meta
owner: RESEARCH.md
status: active
last-verified: 2026-10-03
-->

Written 2026-10-03, after all six investigation reports were sealed (T-0002,
T-0003) and after E002, F006 and F007. This is the screen `STATE.md` asked for:
compare the six investigations and keep E's and F's criteria as a screen.

**Nothing here is new evidence.** Every row is a restatement of a sealed report
or of a recorded experiment result. The only original work is the comparison
itself, which is `inferred` throughout. Labels follow
[`docs/policy/evidence-labels.md`](../docs/policy/evidence-labels.md).

## The method, and its one weakness

Two criteria are applied because they are the only ones the reports supply.

1. **E's entry criterion** (`RESEARCH/E.md`): a mechanism qualifies only if
   *the experiment that could kill it is smaller than the argument for keeping
   it*. E's rules 2–4 add: a simulator falsifies and never validates; prefer an
   experiment whose uninformative case is also informative; absence of a result
   is not a result.
2. **F's C1–C6** (`RESEARCH/F.md`): six binary pre-release checks on a
   repository — runnable README example, README commands exercised in CI, one
   command installation, demonstrated user-visible change, doc linter, README
   alone sufficient.

**The weakness, stated up front.** C1–C6 are a *release* gate. They describe a
built repository and cannot discriminate between six unimplemented candidates:
each one scores **not applicable**, so the screen would have produced no ranking
had I pretended otherwise. The usable part of F for a screen is the earlier
observation, not the checklist: **time to first value** and **comprehension
cost**, applied to the artifact each candidate would hand a user. F's own text
supports this limitation — its sufficiency is `speculative` until validated.

## The candidate inventory

Every candidate any report proposed, promoted or parked. `Outcome` cites the
record; nothing is re-judged here.

| Candidate | Source | Outcome in the record | Physical-world validation this VM cannot do |
|---|---|---|---|
| A1 decision-directed sidewalk survey | A | Count-budget gate met, **fieldwork-cost gate fails 6/6** (F006) | A municipal planner and residents (A step 7) |
| Appliance diagnosis by information gain | A | Not advanced; ORDS exists | — |
| Household critical-load optimisation | A | Not advanced; REopt exists | — |
| B1 photo-migration witness | B, E001 | **Motivating example disproved** (F001) | A disposable Immich instance |
| Heat-pump silent-fallback detector | B | Parked | Labelled field data, equipment access |
| Sewing-projector auto-calibration | B | Rejected | — |
| Care-handoff discrepancy packet | B | Rejected; direct prior art | — |
| C1 knitting repair planner | C, E002 | Local planner valid 9/9, suboptimal on 1 case; bounded-neighbourhood test running as T-0011 | **An experienced knitter's hands** (C Stage B) |
| C2 adaptive ventilation measurement selection | C, E002 | Witness survives (W3); measurement claim **untested** | A room, sensors, and controlled interventions |
| Archaeological fragment reconstruction | C | Rejected; RePAIR et al. | Fieldwork |
| Irregular-remnant nesting | C | Rejected; OpenNest, ironnest | — |
| Universal accessibility certification | D | Rejected; information-insufficient and unfalsifiable | Disability users (D step 9) |
| Appliance disaggregation from aggregate power | D | Rejected; executed non-identifiability witness | — |
| Trustworthy maps for underserved places | D | Rejected; HOT Tasking Manager, fAIr | Reviewer study with participants |
| Capture any computation once, reproduce forever | D | Rejected; ReproZip, reprotest | — |
| Universal local-first sync layer | D | Rejected; CRDT convergence ≠ business invariants | — |
| E1 retry storms are a synchronisation failure | E | `untested` | — |
| E2 lockfiles are weak witnesses of reproducibility | E | `untested` | Registry history over months |
| E3 build timestamps are the cheapest determinism violation to count | E | `untested` | — |

Sixteen candidates; thirteen are rejected, disproved, or parked by the record.
Three are live: **C2**, **E2**, **E3**. One of those, C1, is being tested by
another worker (T-0011). F proposed no candidate by design.

## Screen 1 — is the killing experiment smaller than the argument?

`inferred` ranking, grounded in each report's own stated experiment and in what
this machine can run (`EXPERIMENTS/000-capabilities/`, `tools/origin doctor`).

| Candidate | Killing experiment as its report states it | Runnable here? | Verdict |
|---|---|---|---|
| A1 | Masking experiment on the PPNA extract | **Already run** | Gate failed under cost (F006) |
| B1 | Reproduce issue 1422 in a disposable Immich instance, compare to Immich integrity checks | **No** — needs a containerised server the VM does not have | Argument larger than experiment; also needs the destination, not the source |
| C1 | Tiny grids, local planner vs exhaustive search | Already run (T-0010) | In progress on another VM |
| C2 | Two-room mass-balance simulator, three protocols, one kill gate | **Yes** — stdlib Python, seeded, bounded | Qualifies |
| E1 | ~100-line deterministic retry simulator | **Yes** | Qualifies mechanically — see Screen 3 |
| E2 | Hash two lockfile snapshots and count drift | **No, yet** — needs snapshots days apart | Time-gated, not effort-gated |
| E3 | Download 200 recent wheels, count non-normalised zip dates | **Yes** — one command, minutes | Qualifies |

## Screen 2 — time to first value and comprehension cost

From `RESEARCH/F.md`, applied to the artifact each candidate hands a user.
`inferred`; no user has been observed for any row, which is exactly the
limitation F records.

| Candidate | Artifact delivered | Steps to first value | Comprehension cost for the intended user |
|---|---|---|---|
| A1 | Fieldwork list plus decision report | One neighbourhood, manual origin/destination set | Moderate; planner vocabulary |
| B1 | Discrepancy packet | Export, import, wait for async jobs, snapshot | High; requires trusting the semantics |
| C1 | SVG repair map and action list | **Enter a correct chart patch** | High — the report's own abandon reason is that the user must already understand the structure |
| C2 | Identifiability report plus next action | Sensors, room volumes, paired observations | **Highest of the three** — and C records that the willing users already have NIST and NVAPF |
| E1 | None; jitter is a library default | — | — |
| E2 | Stability verdict for a dependency closure | Extract closure, hash artifacts, resolve | Low for engineers |
| E3 | Timestamp-violation count per artifact set | Download, unzip, read dates | Low for engineers |

## Screen 3 — would a surviving result change a build decision?

E's rule 2 and D's step 10 in one question: if the experiment passes, what gets
built? This is the screen that actually discriminates the software candidates.

| Candidate | If the gate passes, the honest next step | Verdict |
|---|---|---|
| E1 | Nothing new. Jitter is in every modern client library; E's own strongest objection says so. A pass confirms a 2015 AWS blog post. | **Fails.** Cheap to run, uninformative about product value. Not next. |
| E2 | A closure verifier that re-resolves and diffs installed artifacts, so a lockfile stops being treated as proof. Nobody occupies that position directly; D §4's ReproZip limits are about *recording* a run, not *auditing a witness* over time. | **Qualifies**, but blocked on elapsed time, not effort. |
| E3 | A timestamp-violation counter. D §4 and reproducible-builds.org already own the diagnosis; only the *rate* is unknown. | **Marginal.** The measurement is worth having because it is nearly free and the number is genuinely unmeasured; the product is a clone. |
| C2 | A small reproducible measurement protocol and identifiability report — which is exactly what `RESEARCH/C.md` already concludes should be **an extension to existing tools** if it survives. | **Qualifies as an experiment, not as a project.** |

## What the screen actually found

`inferred`, and this is the part no single report contains.

1. **Every promoted candidate in A, B and C depends on a person or a room this
   repository cannot reach.** A needs a planner; B needs a disposable Immich and
   a real export; C1 needs an experienced knitter's hands (its own Stage B gate);
   C2 needs sensors and controlled interventions. Three tasks (T-0005, T-0006,
   T-0007) bought A1 a falsification, not a decision. That is not bad luck — it is
   the shape of the candidate set those reports produced.
2. **Only D, E and F proposed things testable on this machine**, and D proposed
   nothing at all: it rejected five families. The only candidates that are both
   locally falsifiable and not already dead are **C2, E2, E3**.
3. **A simulator cannot move C2 past "technical hypothesis survives".** E's rule 2
   and C's own kill gate say so. Running it can only narrow the set, which is the
   stated preference in `docs/process/hypothesis-lifecycle.md` ("Prefer to
   abandon").
4. **The screen cannot fix the shared-prior problem.** `RESEARCH.md` already
   records that four independent reports share one model's priors, so agreement is
   weak evidence. Adding E and F raises the count, not the independence.
5. **F's checklist stays a gate, not a screen.** It becomes applicable at stage D
   of the lifecycle. No candidate is anywhere near it.

## Ranked next actions

Ordered by information gained per unit of effort, with the honest ceiling on each.

1. **Run C2's simulation kill gate** (`RESEARCH/C.md` "Smallest runnable
   falsification experiment"). Stdlib Python, seeded, three protocols at one
   budget, paired parameter sets, held-out weather and mixing violations. W3 says
   the mechanism is information-sufficient, so a result is possible at all. Ceiling:
   a pass means "mathematically possible on correctly specified synthetic models"
   and nothing more; the prior-art problem in C is untouched by it.
2. **Run E3's timestamp census** because it is the cheapest thing in the
   repository — one command, minutes, hard kill gate at 5% — not because it is
   promising. Ceiling: a PyPI-wheel rate. It cannot bound npm, conda or Maven.
3. **Schedule E2, do not run it now.** It is time-gated: the informative
   comparison is two snapshots of the same closure weeks apart, and single-machine
   resolver runs twice today measure nothing. Start it, then leave it.
4. **Do not run E1.** Screen 3 shows a pass changes no build decision.
5. **Do not build a product.** Nothing is selected. C2's own report already says
   the outcome should be an extension to NIST or NVAPF if it survives.

## Limits of this synthesis

- `inferred` throughout: it reorders and screens existing claims and adds no
  measurement of its own.
- It reads the reports as written. A sealed report is not edited, so a candidate
  whose report understates its own prospects stays understated here.
- The screens are decidable from prose, which makes them cheap and also makes
  them vulnerable to a persuasive report. A candidate the screen rejects could
  still be good; what the screen guarantees is that the *next* experiment is
  worth running.
- No user evidence, no prior-art re-check, and no novelty claim appears anywhere
  in this document.