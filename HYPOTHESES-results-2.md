<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Hypotheses — results, part 2: the three proposed kill gates and their witnesses

Split out of [`HYPOTHESES-results.md`](HYPOTHESES-results.md) on 2026-10-06 at its
300-line cap, by invariant (hypothesis vs result), intact:

## The three proposed kill gates and their witnesses

Moved here from [`HYPOTHESES.md`](HYPOTHESES.md) on 2026-10-06 at that file's line cap,
**verbatim and by invariant**: a hypothesis says what would have to be true and what would
end it, a result says what happened, and these three now have results. All three were
written in T-0001, all three witnesses were run in T-0008, and **none survived** — the
sidewalk entry on its cost regime (F006), the ventilation entry on its design gate (F008),
and the knitting entry's algorithmic claim as prior art (F009). The live candidate list,
their objections and their *reconsider when* clauses stay in
[`HYPOTHESES.md`](HYPOTHESES.md).

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
