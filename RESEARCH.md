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
| [`E.md`](RESEARCH/E.md) | Experimental engineer | Sealed | Retry synchronization, lockfile closure drift, timestamp determinism — three cheap falsifiable mechanisms |
| [`F.md`](RESEARCH/F.md) | Adoption researcher | Sealed | Time-to-first-value, distribution, comprehension cost, six pre-release checkable criteria |
| [`SYNTHESIS.md`](RESEARCH/SYNTHESIS.md) | Cross-report screen | Active | All six reports screened with E's falsifiability criterion and F's time-to-first-value lens; ranked survivor list |

[`EXPERIMENT-PROTOCOL.md`](RESEARCH/EXPERIMENT-PROTOCOL.md) was promoted to
[`docs/process/experiment-protocol.md`](docs/process/experiment-protocol.md);
this path is kept as a pointer.

## Method, and its known weakness

**Initial reports must not read other researchers' reports.** Evidence
consolidation begins only after every report is saved, so that anchoring does not
shape the exploration.

The weakness: agents share a model's priors. All six reports are
procedurally independent and **not** epistemically independent. Agreement among
them is weak evidence; disagreement is strong. Two consequences:

1. Two further roles (E, F) were added on 2026-10-03 (T-0002, T-0003), which
   raises the number of perspectives without raising their independence.
2. Convergence on any candidate should be treated as a prompt to look harder for
   prior art, not as confirmation.

The adversarial protocol in `D.md` was written to compensate for exactly this. Its
reusable form is in
[`docs/process/review-protocol.md`](docs/process/review-protocol.md).

## What the reports agree on

`inferred`, and consistent across six independent passes:

- Every candidate has substantial prior art. That is the base rate for ideas an
  agent can generate, and it is the reason a prior-art check precedes any novelty
  claim.
- The hard problems are not implementation. They are deciding what is worth
  building, and distinguishing a real gap from an imagined one.
- Several attractive proposals die at the information-sufficiency test: two
  underlying realities with identical inputs and different required outputs. This
  is cheap to test, and it has now been applied to the three held candidates
  (`003-information-sufficiency`, F007).
- Adoption evidence is the missing ingredient everywhere. No report could produce
  a validated user, and none claimed one.
- E's report adds a constraint the others never stated: a mechanism is only worth
  keeping if the experiment that could kill it is smaller than the argument for
  keeping it. Applied to all six reports in [`SYNTHESIS.md`](RESEARCH/SYNTHESIS.md).

## Where the evidence disagrees

Recorded rather than resolved:

- `A.md` advances sidewalk survey prioritisation; `D.md` would treat a
  similar-shaped claim as a proxy-versus-outcome confusion unless the decision
  owner is named. Unresolved, and testable: it turns on whether the recommended
  measurement can change a decision a planner actually controls. Partly answered
  by `002-a1-masking`: the policy beat simple baselines under a count budget and
  lost to them under a fieldwork-cost budget (F006). The decision-owner half of
  the disagreement is still unobserved.
- `C.md` holds two candidates that `D.md`'s standard would likely reject on
  information-sufficiency grounds. Both were `untested` on exactly that point;
  both have now been tested (`003-information-sufficiency`): the ventilation
  candidate survives, and the knitting spec was insufficient until mount was
  added to the input (F007).
- `B.md` finds real normalised struggles; `D.md` finds that in each case the
  mechanism is already served. The disagreement is about whether an
  implementation gap inside an existing product is worth a new repository. The
  one instance that was tested went the way `D.md` predicted (F001).

## The next research action

Apply the screen in [`SYNTHESIS.md`](RESEARCH/SYNTHESIS.md): the surviving
locally-falsifiable candidates are the ventilation measurement protocol (C2) and
E's two untested software mechanisms (E2, E3). `STATE.md` carries the ordering;
the protocol is in
[`docs/process/hypothesis-lifecycle.md`](docs/process/hypothesis-lifecycle.md).

Sealing rule: a sealed report is not edited. Corrections are appended to
`HYPOTHESES.md` or `FAILURES.md`, leaving the original reasoning intact and
auditable. Metadata blocks were added to sealed reports on 2026-10-03 without
altering their content.