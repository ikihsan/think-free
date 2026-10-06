<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Hypotheses — experiment results

What each experiment returned, with its numbers, its classification, and what it
does not cover. The live candidate list, their predeclared kill gates, and the
witnesses are in [`HYPOTHESES.md`](HYPOTHESES.md); negative results are in
[`FAILURES.md`](FAILURES.md).

**The invariant that makes the split sensible.** A hypothesis says what would
have to be true and what would end it; a result says what happened. They are read
at different moments — the first before an experiment, the second after — and
merging them made this file exceed its line cap while adding an outcome.

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

**W2 Stage-A comparison (T-0010, `EXPERIMENTS/004-knitting-stage-a/`).**
`observed`, 2026-10-03. The candidate's cheap local heuristic and an
exhaustive minimum-cost oracle agree on 8/9 solvable synthetic cases and the
heuristic is valid (never misses an error, never emits an illegal closure) on
all 9; it refuses the unsupported-shaping case. It is suboptimal on the
deliberately constructed `same_column_stack_4x4` shared-release case (local 5
vs. optimum 3): the per-error rule cannot see that one release covers two
errors. No full-row-release degeneration, no missing action sequence, no
silent acceptance. Verdict `narrow`, not `abandon` — recorded in the
experiment README; next test is a bounded-neighbourhood planner against the
same oracle before any Stage-B physical work.

**W2 Stage-A follow-up (T-0011, `EXPERIMENTS/005-knitting-bounded-search/`).**
`observed`, 2026-10-03. The bounded-neighbourhood planner — group errors whose
release closures intersect, take each group's minimum-cost local plan, charge the
union of the releases once — is **valid and cost-identical to the exhaustive
optimum on 115/115 checked cases** (116/116 with the opt-in `--slow` oracle), on
both the development and the holdout fixture seed and at every patch cost swept,
and it **refuses** both unsupported states. 004's per-error rule is optimal on
85/115 of the same cases. The decomposition's per-chunk costs were separable on
every case, which is the mechanism the design predicts, so this checks that the
implementation matches its design rather than discovering anything. Two limits
matter more than the headline: any *cheaper* setting is suboptimal (chunk cap 1
fails on 20/115, fourteen of them holdout cases; cap 3 on 2 holdout cases), and two
settings that look optimal (`cap=1, beam=2`, `cap=2, beam=4`) enumerate exactly
the oracle's own search space and are exhaustive search in disguise. On T-0010's
own fixtures the bounded planner does **1.28x more** work than the oracle; the
saving appears only where closures fragment. Verdict: the Stage-A planner question
is **answered at the mechanism level** — narrow, not abandoned — and the
candidate's remaining gate is prior art plus unperformed Stage-B physical work,
not more synthetic planner search. Recorded in `DECISIONS-PRACTICE.md` D021.

**W2 prior-art check (T-0015, `RESEARCH/PRIOR-ART-KNITTING.md`).**
`observed` for what was retrieved, `inferred` for the judgement. The kill gate's
prior-art condition conflates two claims, and the report separates them. **The
domain condition is not met:** no tool, paper, repository or patent was found
that supplies an ordered, checkable intervention sequence for a structure
someone has already knitted by hand — KnitPick (UIST 2019) and `knit_graph`
provide the graph layer, EnvisioKnit's Chart Checker catches unknittable charts
*before* knitting, KnittingFix diagnoses from photos, and the 1929–1953
mending-machine patents show the physical capability existed as hardware. **The
novelty condition is met and decisive:** computing a minimum-cost set of
interventions under constraints, decomposed over neighbourhoods that cannot
interact, is established work from 2007 to 2026 (optimal repairs for functional
dependencies, repair *programs* as ordered operation sequences, graph repair
ranking). T-0011 had already recorded that its own optimality follows from the
model's structure.

**Consequence.** The algorithmic-advantage claim is abandoned (`FAILURES.md`
F009); no third synthetic planner experiment is warranted. What survives is a
craft-tool question — would a knitter follow a generated plan and save real
work — which is Stage B, needs an experienced knitter and authorization, and
cannot run in this repository.

**W1 and W3.** `observed`, 2026-10-03. No silent pair was found within the
permitted input set: in each case an askable observation separates the realities,
so next-observation selection carries decision-relevant information. This is
`observed` for the witness construction and `inferred` for the wider claim; it
does not measure usefulness, differentiation, or adoption, and one construction
cannot exclude a different silent pair.

**W3 measured (T-0014, `EXPERIMENTS/006-ventilation-measurement-design/`).**
`observed`, 2026-10-03. The witness says an askable observation separates the
realities; the experiment asked the follow-up question, which the witness cannot
answer: does *choosing* that observation beat *being told* one? On 6 paired
hypothesis families whose passive trace in the measured room is identical by
construction, with one shared fitter and an identical budget of 12 sample slots
and one decision, pairwise discrimination accuracy was passive 0.333 (chance),
prescribed door-open 0.833, adaptive 0.792. The predeclared gate required
adaptive to beat fixed and was **not met**, so the formulation is stopped. One
narrower observation survives: under poor mixing, reading a second sensor holds
0.708 where acting on the measured room drops to 0.542. Recorded as
`FAILURES.md` F008. **This is a failed claim, not a failed mechanism** — the
question of which hypotheses remain distinguishable is still answerable, and
this experiment only shows that the proposed advantage over a fixed protocol did
not appear.

## E3 — Build timestamps (census run 2026-10-03)

**Claim under test (`RESEARCH/E.md`, mechanism E3).** Embedded build timestamps
are the dominant, cheap-to-count determinism violation in Python packaging, so
they are worth fixing first.

**Kill gate (predeclared in `RESEARCH/E.md`).** Below 5% of sampled wheels with
non-normalised timestamps, E3 is a weak lead and the experiment ends.

**Result.** `observed`, 2026-10-03, T-0013,
`EXPERIMENTS/007-build-timestamps/`. 200 wheels over 200 distinct releases from
ten declared packages, every value read from the artifact, zero failures over
205 MB, reproduced identically on three consecutive runs. Gate metric 0.965
(95% CI 0.940–0.990) — the gate **passes at 19x**. Stricter fractions beside it:
0.670 of wheels carry two or more distinct entry dates, 0.535 span a minute or
more, 0.145 span an hour or more (the widest: 23 entries across 789 days). Zero
of 200 wheels carried a unix-epoch integer in `METADATA` or `RECORD`, so E3's
stated assumption that timestamps hide in embedded strings as well as zip
headers is **half false** on this population.

**Conclusion.** The gate is met and the mechanism is still `untested`. 0.965
measures that almost nobody pins the DOS epoch, not that 96.5% of wheels
are irreproducible because of timestamps; and nothing here rebuilds an artifact,
so no cause is assigned. Recorded as `FAILURES.md` F010 — the measurement was
inadequate, not the mechanism wrong. The prevalence is also not one ecosystem
rate: only `cryptography` ships 1980-normalised wheels (7 of 20, all
`win_amd64`), `urllib3` stamps every entry with one build instant, and `jinja2`
carries checkout mtimes.

**Attribution measured (T-0017, `EXPERIMENTS/008-build-timestamp-attribution/`).**
`observed`, 2026-10-03. Five pure-Python sdists, 35 real builds with setuptools
45.2.0 + wheel 0.34.2, two checkouts identical in content and 34 months apart in
mtime. Attribution is causal: rewriting only the four DOS bytes in each local
header and each central-directory entry of one artifact to the other's values.
With `SOURCE_DATE_EPOCH` unset, **398 of 398 differing bytes pooled lie inside
zip timestamp fields** and the patch reproduces the other artifact exactly on
5 of 5 sources, so timestamps were the only cause. With it set, builds are
bit-identical (0 differing bytes, 5 of 5). A second timestamp route was found and
identified: the `.dist-info` files the builder generates carry the wall clock, so
two builds across a 2-second DOS tick differ in exactly those entries.
Predeclared gate met: `timestamps-first`.

**Decision.** `FAILURES.md` F012. E3's ordering claim is **supported for this
builder** — fixing timestamps is sufficient, not merely worthwhile — and the
candidate is **abandoned anyway**, because the remedy is `SOURCE_DATE_EPOCH`, a
standard this builder already honours. The remaining gap is adoption, and
adoption of an existing standard is not a new repository. E1 and E2 are still
`untested`; **do not run E1** (D020, Screen 3). E2 is time-gated, not effort-
gated: two resolver runs today measure nothing, so snapshot one side of that
comparison while a VM is idle.

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
