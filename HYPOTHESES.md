<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Hypotheses

No candidate has been selected. This file records what is being considered, what
would kill it, and what has actually been observed. Format and required fields:
[`evidence-record` skill](.agents/skills/evidence-record/SKILL.md).

Labels: `observed`, `source-supported`, `inferred`, `speculative`, `untested`.
Full definitions: [`docs/policy/evidence-labels.md`](docs/policy/evidence-labels.md).

## Status summary

| Candidate | Source | State | Next experiment |
|---|---|---|---|
| Photo-migration auditor | `RESEARCH/B.md`, E001 | **Motivating example disproved** (`FAILURES.md` F001) | Needs a real case where bytes survive and relationships do not |
| Knitting repair planner | `RESEARCH/C.md` | Hold; **witness found the spec information-insufficient** (W2) | Add orientation to the input, then local planner vs. exhaustive search |
| Adaptive ventilation measurement | `RESEARCH/C.md` | Hold; **witness survives** (W3) | Simulation comparing adaptive against fixed protocol |
| Decision-directed sidewalk survey | `RESEARCH/A.md` | Advance; **witness survives** (W1), A1 masking gate met with caveats | Fieldwork-cost sensitivity and a planner review |
| Care-handoff discrepancy packet | `RESEARCH/B.md` | Rejected: prior art too direct | — |
| Sewing-projector auto-calibration | `RESEARCH/B.md` | Rejected: no material gap shown | — |
| Automated accessibility certification | `RESEARCH/D.md` | Rejected: universal claim unfalsifiable | — |
| Appliance disaggregation from aggregate power | `RESEARCH/D.md` | Rejected: information-insufficient | — |
| Automated trustworthy map building | `RESEARCH/D.md` | Rejected: coordination cost dominates | — |
| Capture-and-reproduce-any-computation | `RESEARCH/D.md` | Rejected: ReproZip and reprotest prior art | — |
| Universal local-first sync layer | `RESEARCH/D.md` | Rejected: invariants not preserved | — |

## The one experiment that has run

### E001 — Is a plain checksum baseline sufficient?

**Claim under test.** The published four-image photo-migration failure requires a
relationship-aware mechanism to reveal its missing media.

**Kill gate (predeclared).** If checksum identity alone finds all missing media
described in the trace, without original/edit inference, the example establishes a
failure of importer reporting and **not** an advantage for a semantic auditor.

**Baseline.** The cheapest available: source-relative checksum set difference
between the Takeout fixture and the destination model implied by the published API
trace. No relationship inference, no importer-specific instrumentation.

**Controls.** Complete destination yields no missing identities; renamed identical
bytes yield no missing identities; accepted-operation model reproduces the reported
missing filenames; operation counts match; relationship-only damage with all
identities retained is invisible to the baseline.

**Result.** `observed`, 2026-10-03. The kill gate was met. The baseline recovered
the exact reported pair; all controls behaved as predicted. Artifacts:
`EXPERIMENTS/001-photo-baseline/results.json`, including the pinned source
revision and SHA-256 of every downloaded input.

**Conclusion.** `FAILURES.md` F001. The example does not support building the
verifier.

**Remaining uncertainty.** Whether relationship-only loss occurs in real archives
at a rate that matters; whether the importer bug still exists; whether users need a
standalone product at all.

**Reconsider when.** A real case is found in which all bytes survive and important
relationships do not, **and** the existing reporting does not already surface it.

## The information-sufficiency gate (E002, run 2026-10-03)

Before any candidate is implemented, two realities that give it identical
permitted inputs but require different outputs must be constructed. A passive
system fails this gate outright; an active system fails only if no permitted
observation separates the pair. Experiment `EXPERIMENTS/003-information-sufficiency/`
runs one small synthetic witness per held candidate. All inputs are synthetic;
the witness can falsify an unbounded claim but measures no prevalence.

| Witness | Candidate | Result | Consequence |
|---|---|---|---|
| W1 | Decision-directed sidewalk survey | **Survives** (`observed`) | The mechanism is not structurally information-insufficient given known OD pairs; the A1 masking experiment supplies the measured comparison |
| W2 | Knitting repair planner | **Spec was insufficient; repaired** (`observed`) | The original input set omitted loop orientation (F007); adding mount makes the two realities distinguishable (T-0009) |
| W3 | Adaptive ventilation measurement | **Survives** (`observed`) | An ordinary permitted action (`co-locate`, `close-internal-door`) separates two realities whose passive traces coincide within noise |

Full claim, oracle, and limits per witness:
[`EXPERIMENTS/003-information-sufficiency/README.md`](EXPERIMENTS/003-information-sufficiency/README.md).

**W2 finding.** `observed`, 2026-10-03. Two stitch states with identical
chart-level inputs (same symbols, connectivity, live stitches, and facing side)
require different repairs because one is mounted twisted and the other is not.
Mount is not in the candidate's stated input set, so the planner cannot choose
between "re-form in place" and "re-form and untwist" from its permitted input.
This is not a refutation of the mechanism: a knitter can observe orientation, so
the fix is to add orientation to the input (or refuse). It bounds the input and
rules out the current, narrower claim. Recorded as `FAILURES.md` F007.

**W2 repair (T-0009).** `observed`, 2026-10-03. Adding each loop's mount to the
input distinguishes the two realities: the witness reports `silent_pair_found`
`true → false` and `permitted_encoding_can_represent_the_difference`
`false → true`. The specification is now sufficient for the decision; the
algorithmic-advantage question is untouched and awaits the Stage-A planner
comparison.

**W1 and W3.** `observed`, 2026-10-03. No silent pair was found within the
permitted input set: in each case an askable observation separates the realities,
so next-observation selection carries decision-relevant information. This is
`observed` for the witness construction and `inferred` for the wider claim; it
does not measure usefulness, differentiation, or adoption, and one construction
cannot exclude a different silent pair.

## Candidates awaiting a falsification experiment

Each entry below is summarised here; the full reasoning is in the sealed
investigation report. None has a kill gate yet, and writing one is the
precondition for the next experiment.

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