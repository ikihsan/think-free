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
| Knitting repair planner | `RESEARCH/C.md` | Hold; representation is prior art | Local planner vs. exhaustive search on small graphs |
| Adaptive ventilation measurement | `RESEARCH/C.md` | Hold; strong competition | Simulation comparing adaptive against fixed protocol |
| Decision-directed sidewalk survey | `RESEARCH/A.md` | Advance to bounded experiment | Masking experiment on the PPNA extract |
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

## Candidates awaiting a falsification experiment

Each entry below is summarised here; the full reasoning is in the sealed
investigation report. None has a kill gate yet, and writing one is the
precondition for the next experiment.

| Candidate | Claim | Strongest objection |
|---|---|---|
| Knitting repair planner | A bounded, checkable intervention plan for an already-knitted structure is useful and not yet served | Easy cases need no software; hard cases may need tactile judgement the graph does not capture. Topology alone does not govern physical behaviour (`RESEARCH/C.md` cites a 2026 arXiv laddering study) |
| Adaptive ventilation measurement selection | Choosing the next cheap observation to separate competing explanations beats a fixed protocol | Too little information may be available at household cost, and the willing users can already use established tools |
| Decision-directed sidewalk survey | Spending the next survey hour where it changes a feasible repair decision beats centrality or missingness heuristics | Procurement, utility relocation, and legal constraints may dominate survey prioritisation entirely; graph error may outweigh attribute uncertainty |

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