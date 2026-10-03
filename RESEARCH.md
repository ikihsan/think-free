<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Research index

No discoveries imported. Independent reports live in `RESEARCH/`; factual claims
must cite a directly inspected source, describe its relevance, and distinguish
inference from evidence.

Labels: [`docs/policy/evidence-labels.md`](docs/policy/evidence-labels.md).
Method: [`docs/process/hypothesis-lifecycle.md`](docs/process/hypothesis-lifecycle.md).

## Reports

| Report | Role | State | Distinct contribution |
|---|---|---|---|
| [`A.md`](RESEARCH/A.md) | Fundamental thinker | Sealed | Decision value of an observation, not information volume; sidewalk survey prioritisation |
| [`B.md`](RESEARCH/B.md) | Problem archaeologist | Sealed | Photo-migration verification, heat pumps, sewing projectors, care handoffs |
| [`C.md`](RESEARCH/C.md) | Cross-domain explorer | Sealed | Knitting repair planning; adaptive ventilation measurement selection |
| [`D.md`](RESEARCH/D.md) | Adversarial skeptic | Sealed | Six rejected claim families; the reusable adversarial protocol |
| [`ROOT-SCOUTING.md`](RESEARCH/ROOT-SCOUTING.md) | Coordinator | Sealed | Accessibility remediation and CAD interoperability counterevidence |
| E | Experimental engineer | **Not run** | — |
| F | Adoption researcher | **Not run** | — |

[`EXPERIMENT-PROTOCOL.md`](RESEARCH/EXPERIMENT-PROTOCOL.md) was promoted to
[`docs/process/experiment-protocol.md`](docs/process/experiment-protocol.md);
this path is kept as a pointer.

## Method, and its known weakness

**Initial reports must not read other researchers' reports.** Evidence
consolidation begins only after every report is saved, so that anchoring does not
shape the exploration.

The weakness: agents share a model's priors. Four independent reports are
procedurally independent and **not** epistemically independent. Agreement among
them is weak evidence; disagreement is strong. Two consequences:

1. Two roles are missing (E, F), so the candidate set rests on four perspectives
   and is missing the experimental-engineering and adoption views entirely.
2. Convergence on any candidate should be treated as a prompt to look harder for
   prior art, not as confirmation.

The adversarial protocol in `D.md` was written to compensate for exactly this. Its
reusable form is in
[`docs/process/review-protocol.md`](docs/process/review-protocol.md).

## What the reports agree on

`inferred`, and consistent across four independent passes:

- Every candidate has substantial prior art. That is the base rate for ideas an
  agent can generate, and it is the reason a prior-art check precedes any novelty
  claim.
- The hard problems are not implementation. They are deciding what is worth
  building, and distinguishing a real gap from an imagined one.
- Several attractive proposals die at the information-sufficiency test: two
  underlying realities with identical inputs and different required outputs. This
  is cheap to test and has not yet been applied to the three held candidates.
- Adoption evidence is the missing ingredient everywhere. No report could produce
  a validated user, and none claimed one.

## Where the evidence disagrees

Recorded rather than resolved:

- `A.md` advances sidewalk survey prioritisation; `D.md` would treat a
  similar-shaped claim as a proxy-versus-outcome confusion unless the decision
  owner is named. Unresolved, and testable: it turns on whether the recommended
  measurement can change a decision a planner actually controls.
- `C.md` holds two candidates that `D.md`'s standard would likely reject on
  information-sufficiency grounds. Both are `untested` on exactly that point.
- `B.md` finds real normalised struggles; `D.md` finds that in each case the
  mechanism is already served. The disagreement is about whether an
  implementation gap inside an existing product is worth a new repository.

## The next research action

Write kill gates for the held candidates, then apply the information-sufficiency
test before any implementation. `STATE.md` carries the ordering; the protocol is in
[`docs/process/hypothesis-lifecycle.md`](docs/process/hypothesis-lifecycle.md).

Sealing rule: a sealed report is not edited. Corrections are appended to
`HYPOTHESES.md` or `FAILURES.md`, leaving the original reasoning intact and
auditable. Metadata blocks were added to sealed reports on 2026-10-03 without
altering their content.