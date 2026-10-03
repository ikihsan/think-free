<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Hypotheses — what is being considered and what would kill it

The live index. One row per candidate, the predeclared kill gate and witness for
each held candidate, and the cautions that apply to all of them.

What an experiment actually returned, with its numbers and limits, is in
[`HYPOTHESES-results.md`](HYPOTHESES-results.md).

No candidate has been selected. This file records what is being considered, what
would kill it, and what has actually been observed. Format and required fields:
[`evidence-record` skill](.agents/skills/evidence-record/SKILL.md).

Labels: `observed`, `source-supported`, `inferred`, `speculative`, `untested`.
Full definitions: [`docs/policy/evidence-labels.md`](docs/policy/evidence-labels.md).

## Experiments that have run

Every result lives in [`HYPOTHESES-results.md`](HYPOTHESES-results.md). The
experiment directories are `001-photo-baseline` (E001),
`003-information-sufficiency` (the E002 witness gate),
`004-knitting-stage-a` and `005-knitting-bounded-search` (the knitting Stage-A
pair), `006-ventilation-measurement-design` (C2), and
`007-build-timestamps` (E3's census, whose attribution half is T-0017,
`EXPERIMENTS/008-build-timestamp-attribution/`).

## Status summary

| Candidate | Source | State | Next experiment |
|---|---|---|---|
| Photo-migration auditor | `RESEARCH/B.md`, E001 | **Motivating example disproved** (`FAILURES.md` F001) | Needs a real case where bytes survive and relationships do not |
| Knitting repair planner | `RESEARCH/C.md`, E002 | **Algorithmic-advantage claim abandoned** (`FAILURES.md` F009): minimum-cost repair planning is prior art from 2007–2026, and no tool was found that supplies an intervention sequence for an existing hand-knit structure. Stage A was already settled (T-0010, T-0011) | Nothing software-side. Only Stage B physical work with an experienced knitter, and only after checking that entering the chart patch does not already imply the user can do the repair |
| Adaptive ventilation measurement | `RESEARCH/C.md`, E002 | **Stopped as formulated** (`FAILURES.md` F008, T-0014): a prescribed door-open protocol beats adaptive action selection at equal budget, 0.833 vs 0.792 | Only if the surviving robustness observation (read a second sensor under poor mixing) is tested against existing tools |
| Decision-directed sidewalk survey | `RESEARCH/A.md`, E002 | **Falsified in its motivating regime**: count-budget gate met, fieldwork-cost gate fails (`FAILURES.md` F006) | No product build; treat A1 as a negative result and require a real cost model up front |
| Python packaging determinism (E1–E3) | `RESEARCH/E.md` | E3's prevalence census ran and passed its 5% gate at 0.965, but the metric is near-vacuous and attribution is untested (`FAILURES.md` F010); E1 and E2 remain `untested` | E3 attribution via T-0017; **do not run E1** (D020 Screen 3); E2 is time-gated |
| Care-handoff discrepancy packet | `RESEARCH/B.md` | Rejected: prior art too direct | — |
| Sewing-projector auto-calibration | `RESEARCH/B.md` | Rejected: no material gap shown | — |
| Automated accessibility certification | `RESEARCH/D.md` | Rejected: universal claim unfalsifiable | — |
| Appliance disaggregation from aggregate power | `RESEARCH/D.md` | Rejected: information-insufficient | — |
| Automated trustworthy map building | `RESEARCH/D.md` | Rejected: coordination cost dominates | — |
| Capture-and-reproduce-any-computation | `RESEARCH/D.md` | Rejected: ReproZip and reprotest prior art | — |
| Universal local-first sync layer | `RESEARCH/D.md` | Rejected: invariants not preserved | — |

## Candidates awaiting a falsification experiment

Each entry below carries the kill gate it was written with; the full reasoning is
in the sealed investigation report. Kill gates for all three were written in
T-0001 and the information-sufficiency gate (E002) was applied to all three in
T-0008. All three have since been measured and none survived: the sidewalk entry
fails its cost regime (F006), the ventilation entry fails its design gate (F008),
and the knitting entry's algorithmic claim is prior art (F009). What is left is
not another experiment on this file's account — it is the question each entry's
*reconsider when* clause names, and for two of the three that question needs a
person this repository cannot reach.

| Candidate | Claim | Strongest objection |
|---|---|---|
| Knitting repair planner | A bounded, checkable intervention plan for an already-knitted structure is useful and not yet served | Easy cases need no software; hard cases may need tactile judgement the graph does not capture. Topology alone does not govern physical behaviour (`RESEARCH/C.md` cites a 2026 arXiv laddering study) |
| Adaptive ventilation measurement selection | Choosing the next cheap observation to separate competing explanations beats a fixed protocol | Too little information may be available at household cost, and the willing users can already use established tools |
| Decision-directed sidewalk survey | Spending the next survey hour where it changes a feasible repair decision beats centrality or missingness heuristics | Procurement, utility relocation, and legal constraints may dominate survey prioritisation entirely; graph error may outweigh attribute uncertainty |

### Sidewalk survey — kill gate and witness (proposed, untested)

**Kill gate (transcribed from `RESEARCH/A.md` step 5).** Go only if the
decision-directed policy achieves at least 25% lower median repair-decision
regret than the strongest simple baseline (random, highest centrality, highest
missingness/entropy, shortest fieldwork tour) across 30 fixed masking seeds,
including contiguous block-missingness cases, at no greater fieldwork cost.
Report distributions, not only the mean. Failure (stop) if gains disappear
under modest cost/profile/priors changes, if most recommendations depend on
unmeasured structural data, or if useful regret cannot be defined without
arbitrary demand assumptions.

**Information-sufficiency witness.** Two underlying networks with identical
currently-observable measurements but different feasible next repair packages:
if no askable observation separates them in decision value, the policy has no
advantage over the existing data. Run this witness before the full
comparison.

**Reconsider when.** A planner and affected residents reviewing one anonymized
case confirm that no requested measurement could change a decision they
control. Until then this remains `speculative`.

**Outcome (E002, 2026-10-03, `EXPERIMENTS/002-a1-masking/`).** Under a
count budget (150 of 955 crossings, 30 seeds, random and block masks) the
gate **passed**: DD median regret 64.1 vs 109.9 for the strongest baseline.
The T-0006 sweep confirmed it across 18 configs, failing only at the
K~budget degenerate corner. Under a fieldwork-cost budget (T-0007,
`distance.json`), DD's regret stayed at 85.2 across D ∈ {40, 80, 160} km
while centrality reached 0–16.3; the gate failed 6/6. Recorded in
`FAILURES.md` F006: the A1 mechanism's advantage does not transfer to the
realistic cost model.

### Knitting repair planner — kill gate and witness (proposed, untested)

**Kill gate.** Stage A: the local planner must reproduce the exhaustive-search
repair set on enumerably small graphs, preserve boundary loops, yarn order,
pull-through legality, and exact final topology on every transition, and
refuse unsupported shaping/ambiguous states rather than accepting them
silently. Abandon the algorithmic-advantage claim if existing graph tooling
already supplies equivalent intervention sequences, or if the planner
repeatedly degenerates to full-row release in the supposedly useful cases.
Stage B (physical): at least one nontrivial error class saves substantial
undo work relative to tutorial and full-row rollback, with no unsupported
operation silently accepted and no recurring undocumented interventions.

**Information-sufficiency witness.** Two error configurations with identical
chart-level inputs but different valid repairs: if the local planner cannot
distinguish them from the patch alone, graph-level repair planning carries no
additional information for choosing the intervention.

**Reconsider when.** Stage B shows slack, friction, or manipulation access
dominates repair success, or users must already read the full stitch structure
to supply the patch (the tool then serves only those who can already solve
it).

### Adaptive ventilation measurement — kill gate and witness (proposed, untested)

**Kill gate (transcribed from `RESEARCH/C.md`).** Stop if adaptive selection
cannot distinguish the paired near-identical-trace hypotheses more reliably
than the fixed door-open/door-closed protocol at equal observation budget, or
if it produces confident wrong answers under common violations (changing
weather, poor mixing). A gain on correctly specified synthetic models only
establishes mathematical possibility; independent room measurements are
required before any practical claim. No hardware spend before the simulation
changes the decision.

**Information-sufficiency witness.** Two parameter sets that produce nearly
identical passive traces: if the adaptive action menu yields no observation
that separates them, next-observation selection adds nothing over the fixed
protocol. Run this witness before the paired-protocol comparison.

**Reconsider when.** Adequate observations prove unavailable at household
cost, or the willing users are already served by QICO2/NVAPF-class tools.

## Standing cautions

1. Agreement among the sealed investigations is weak evidence: they share a model,
  so they are procedurally independent and not epistemically independent.
2. Every candidate so far has substantial prior art. That is the base rate for
   the ideas an agent can generate, and it is the reason the prior-art skill
   exists.
3. No candidate has passed the information-sufficiency test yet. Two of the
   rejected proposals in `RESEARCH/D.md` were killed by it in ten lines of code.
4. Nothing here has a user. Every usefulness statement is `inferred` or
   `speculative` until a real person is observed.