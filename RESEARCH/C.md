# C — Cross-domain exploration

<!-- origin-meta
owner: RESEARCH.md
status: sealed
last-verified: 2026-10-03
-->

Research date: 2026-10-03. Independent first pass; only `MISSION.md` was read from the project. No personal memory, unrelated repositories, or other agents' research informed this report. Public sources were retrieved on this date. No prototype, physical test, interview, or external mutation was performed. Search results establish prior art and possible experiments, not demand, originality, or correctness.

## Result

Two hypotheses survived preliminary scrutiny. **A local knitting-repair planner deserves the cheaper first experiment.** A ventilation experiment planner is a secondary possibility with much stronger existing competition and harder field validation. Neither is ready for product selection.

The useful transfer is not merely putting software around a craft or sensor. It is taking an existing physical process and exposing its hidden constraints: which fabric loops can be safely released, or which airflow parameters a measurement can actually distinguish.

## Exploration across disciplines

| Discipline | Observation and mechanism considered | Result of prior-art check |
| --- | --- | --- |
| Textile craft and soft-matter physics | A knitter can release selected columns and reconstruct them, preserving most of a garment. A loop's connectivity, orientation, and available yarn constrain the repair. | Knitting graphs, pattern compilers, interactive charts, repair tutorials, and marketed AI repair advice already exist. A verified *intervention plan for an already-knitted structure* is the narrow remaining hypothesis, not graph-based knitting itself. |
| Building ventilation and environmental metrology | CO2 concentration is an indirect tracer. A good-looking decay curve may combine outdoor exchange, exchange with other rooms, changing occupancy, and sensor errors. | NIST tools, multi-box research, and an open adaptive-particle-filter application already cover substantial ground. The remaining hypothesis concerns choosing the next informative measurement and refusing unidentifiable estimates. |
| Pharmacokinetics and experimental science | Compartment models infer hidden transport from sparse tracer observations; optimal experimental design chooses samples to reveal parameters. | PopED already implements optimal design. Transfer its information-budget mindset to practical ventilation measurements; do not claim new mathematics or clinical utility. |
| Archaeological conservation | Fragment reconstruction uses relationships between pieces and preserves uncertain alternatives rather than assuming an intact original is known. | RePAIR and earlier pottery-reassembly research establish substantial prior art. Scanning, incomplete fragments, and expert interpretation make an independent consumer reconstruction tool a poor first bet. The useful analogy for knitting is explicit state reconstruction before intervention. |
| Sheet manufacture and salvage | Irregular offcuts invite nesting with grain, holes, defects, and reusable-remnant value. | Generic nesting was discarded: several open-source tools already cover irregular remnants. A nicer interface alone is not enough evidence of meaningful differentiation. |

Sources for the rejected branches: [RePAIR, 2024](https://arxiv.org/abs/2410.24010) provides a real archaeological fragment benchmark and reports the substantial fieldwork required for ground truth; [pottery thickness-profile reconstruction, 2016](https://arxiv.org/abs/1601.05824) establishes geometry-based reconstruction well before this investigation. [OpenNest](https://petrasvestartas.github.io/OpenNest/) explicitly supports nonrectangular remnants and holes; [ironnest](https://github.com/TexasCoding/ironnest) claims deterministic irregular-remnant nesting; [OpenMarker](https://github.com/Weilei424/openmarker) describes grain-constrained garment layout. Repository and product claims were not executed or independently benchmarked.

## Hypothesis 1 — Plan a local repair in knitted fabric

### Observation

**Source-supported:** selective unravelling and rebuilding is an established repair technique. The difficulty increases when stitch columns interact through shaping or cables. Craft explanations give techniques, but a particular repair also needs correct identification of rows, loop order, which face is presented, and neighboring dependencies. [Knit with Henni, 2020](https://knitwithhenni.com/2020/09/07/drop-to-fix/amp/) demonstrates intentional laddering and multiple-stitch repairs. A [KnittingHelp thread, 2023–2024](https://forum.knittinghelp.com/t/found-a-loop-in-a-ladder-down/158241) documents a concrete case where an unexpected loop exposed a different underlying error and ordinary ladder repair was not sufficient. The thread is an anecdote, not a prevalence estimate.

**Inferred opportunity:** a knitter with a known pattern and a localized mistake may benefit from a repair map specific to that pattern, rather than another generic tutorial. Recognition from photographs is deliberately outside the initial hypothesis.

### Mechanism and transfer

Combine the craft's existing local-unravelling technique with ordered graph transformations and constrained inverse assembly. Represent each loop, yarn adjacency, pull-through relation, and relevant crossing. Input the intended chart, the actual local error, the current live stitches, and the side facing the user. Compute a supported set of loops to release, secure the boundary loops, and reconstruct the intended subgraph in an explicit order.

The artifact would show: (1) where to place holders, (2) which stitches to release and how far, (3) which loose bar belongs to each reconstruction step, and (4) a checkpoint after every step. Compare affected stitches and estimated operations with a complete-row rollback. Optimize an explicit operation cost within supported cases; **do not label this globally minimal or physically safe without proof and physical validation**.

This is not an invention of knitting graphs. The potential invention is compiling a correction into a constrained, checkable physical intervention while preserving unaffected fabric and available yarn.

### Assumptions that must survive

- The user can identify the relevant error and position accurately enough to supply a small chart patch.
- A restricted operation vocabulary can represent useful repairs before general lace, brioche, short rows, colorwork, and arbitrary cables are supported.
- Graph reachability plus explicit yarn order gives an adequately conservative repair boundary; naive descendant closure may be insufficient.
- Existing yarn has enough slack for the requested replacement. A topologically valid result can still pucker or be impossible to manipulate.
- Entering the patch and following the map takes less effort than searching for a tutorial, consulting a teacher, or unravelling full rows.

### Nearest prior art and possible distinction

| Prior art | What it already does | Possible distinction, still unverified |
| --- | --- | --- |
| [KnitPick, UIST 2019](https://textiles.cs.cmu.edu/publications/2019-knitpick/) and [author-hosted paper](https://make4all.org/wp-content/uploads/2019/09/KnitDown_UIST_2019_access.pdf) | Parses hand-knitting notation into graphs; transforms and combines textures; emits hand/machine instructions. | Repair an existing, partially incorrect physical graph instead of designing a fresh textile. Must inspect its full transformation vocabulary before claiming a technical gap. |
| [knit_graph](https://github.com/mhofmann-Khoury/knit_graph) | MIT-licensed loop/yarn/stitch/crossing representation and basic visualization. | Reuse it if suitable; add intervention planning and repair-state validation rather than create another graph library. |
| [Stitch Maps overview](https://stitch-maps.com/about/overview/) and [FAQ](https://stitch-maps.com/about/faq/) | Shows how rows and stitches connect, including increases and decreases. | Explicit undo boundary, preservation constraints, and ordered repair actions. Existing maps plus a short lesson may already provide equivalent value. |
| [A Graph Model and a Layout Algorithm for Knitting Patterns, 2024](https://arxiv.org/abs/2406.13800) | Models simple patterns and evaluates their visualization. | Planning physical edits rather than improving chart layout. |
| [KnittingFix](https://www.knittingfix.com/) | Markets image-based diagnosis and step-by-step repair advice, with human escalation. | A bounded, inspectable symbolic planner that verifies its supported transformations. Marketing claims are not evidence of actual accuracy; several paid plans were marked “Coming soon” when retrieved. |
| [TECHknitting cable repair, 2022](https://techknitting.blogspot.com/2022/10/cables-crossed-wrong-anchored-i-cord.html) | Demonstrates an alternative repair that disguises a cable error without reconstructing the original crossing. | A planner should eventually compare different repair objectives; strict reconstruction may be more work than a skilled cosmetic repair. |

### Strongest reason to abandon

**The easy cases do not need software; the valuable hard cases may need tactile expertise that the graph does not capture.** If a user must correctly understand the whole stitch structure to enter the problem, the tool may only help people who can already solve it. If slack, friction, or manipulation access dominate repair success, a symbolic certificate can create false confidence.

[Laddering of a knitted fabric: a topology-induced failure, submitted 22 April 2026](https://arxiv.org/abs/2604.20580) reports experimental and simulation dependence on tension, curvature, and friction. It is evidence against assuming topology alone governs physical behavior, not validation of this proposed planner. Only the abstract was inspected in this pass.

### Smallest runnable falsification experiment

**Stage A, local software, roughly one focused session:** construct tiny explicit knit/purl grids plus a small set of crossing operations; introduce known single errors; implement release/rebuild state transitions and a bounded search over permitted repairs. Start with handcrafted fixtures rather than a natural-language parser. For graphs small enough to enumerate, compare the proposed local planner against exhaustive search. Produce both an SVG repair map and machine-readable action sequence.

Check every transition for preserved boundary loops, correct yarn order, legal pull-through direction, and exact final supported topology. Include intentionally unsupported shaping and ambiguous observed states; refusal is a required output. A mere final stitch count is not an adequate oracle. **Abandon the claimed algorithmic advantage if existing graph tooling already supplies equivalent intervention sequences, or if the planner repeatedly needs to release the full row in the supposedly useful cases.**

**Stage B, unavoidable physical falsifier:** prepare 6–10 small swatches with known errors; an experienced knitter follows the generated maps without inventing missing steps. Record correctness, extra manual decisions, time, distortion, and stitches actually undone. Compare against the appropriate tutorial and full-row rollback. A model-generated simulation cannot substitute for this. Suggested advance gate: at least one nontrivial class saves substantial undo work, no unsupported operation is silently accepted, and physical repairs work without recurring undocumented interventions. These thresholds are proposed, not measured results.

### Adoption path and decision

Initial audience: knitting teachers and technically interested experienced knitters, with printable maps students can use without an account. A shareable repair patch and verified examples could be useful contributions. Do not assume GitHub is where end users live, or that craft popularity predicts repository stars.

**Decision: conditional advance to a bounded model experiment; no product commitment.** Demand, input burden, scope of existing implementations, and physical feasibility are untested.

## Hypothesis 2 — Choose the next ventilation measurement

### Observation and mechanism

**Source-supported:** room CO2 can inform ventilation estimation, but common methods rely on assumptions about mixing, sources, occupancy, and outside concentration. [NIST's ventilation-evaluation chapter](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=932281) discusses these constraints. The specific source was inspected through extracted search text, not a complete PDF reading.

**Proposed transfer:** pharmacokinetic experiment design asks when and where to observe a tracer to distinguish hidden transport parameters. [PopED's own introduction](https://andrewhooker.github.io/PopED/articles/intro-poped.html) documents optimizing designs for individual and population nonlinear models; the [original PopED paper, 2004](https://www.sciencedirect.com/science/article/pii/S0169260703000737) supplies the historical mechanism.

For a small number of rooms and commodity sensor CSVs, estimate which hypotheses remain indistinguishable: low outdoor exchange, exchange with an adjacent room, or a sensor offset. Suggest the next useful ordinary observation or controlled change, such as co-locating sensors first, recording an unoccupied decay with an internal door in a specified state, or adding a simultaneous reading in the neighboring room. Output both the estimated quantity and what remains unidentifiable. Use normal occupancy-generated CO2; no deliberate gas-release procedure is part of the proposal.

The product distinction would be **a small, reproducible measurement protocol and identifiability report**, not another air-quality dashboard or an infection-risk certificate.

### Assumptions, competitors, distinction

- Room volumes and intervention times can be recorded with tolerable error.
- Outdoor concentration, sensor offsets, and room-to-room exchange can be sufficiently constrained using the available sensors.
- Weather and mixing change slowly enough over paired measurements for the suggested comparison to be meaningful.
- Users will perform controlled observations, rather than want a passive dashboard.

[NIST QICO2, 2022](https://www.nist.gov/services-resources/software/quick-indoor-co2-qico2-tool) already calculates expected CO2 concentrations for comparison with measurements. [CONTAM](https://www.nist.gov/services-resources/software/contam) already models multizone air and contaminant transport; its [current download page](https://www.nist.gov/el/beed/nist-multizone-modeling/software/contam/download-contam) reports a January 2026 release. A replacement simulator would be unjustified.

[NVAPF, 2025](https://www.sciencedirect.com/science/article/pii/S0360132325009072) and its [GPL-licensed project page](https://github.com/Misaeon/CO2-Based-Natural-Ventilation-Rate-Estimation-Tool) describe CSV-based ventilation estimates that handle measurement uncertainty and changing natural ventilation. Therefore “uncertainty-aware CO2 estimation” is already occupied. The repository page links a downloadable application; its actual source distribution was not audited.

[A 2026 multi-box apartment study](https://www.sciencedirect.com/science/article/pii/S2590123026015987) studies window-only, door-only, and combined opening scenarios with occupant-generated CO2. Consequently neither multizone estimation nor comparing door/window interventions is itself a distinction. What might remain is selecting a cheap next observation specifically to separate competing explanations and making non-identifiability visible to nonexperts. This pass did not establish that existing engineering packages lack such workflows.

### Strongest reason to abandon

**Too little information may be available at household cost, while the people willing to collect the necessary information can already use established tools.** Optimal design cannot rescue unmeasured weather-driven changes, persistent poor mixing, or parameters that enter the observations only as inseparable combinations. The proposed interaction may be a useful extension to existing research software, not a standalone project.

### Smallest runnable falsification experiment

Simulate a two-room mass-balance model with known external and inter-room exchange, sensor offsets, noise, and source schedules. Construct paired parameter sets that yield nearly identical passive traces. Compare three protocols at the same observation/intervention budget: passive fitting, a fixed door-open/door-closed sequence, and adaptive selection from a small allowed-action menu. Evaluate parameter error, uncertainty coverage, and the rate of false precise answers; hold out changing-weather and poor-mixing cases that violate the estimator model.

**Kill gate:** if adaptive selection cannot distinguish the paired hypotheses more reliably than the fixed protocol, or produces confident wrong answers under common violations, stop this formulation. A gain on correctly specified synthetic models only establishes a mathematical possibility. Independent room measurements are required before any practical claim. Do not spend on hardware before the simulation changes the decision.

### Adoption path and decision

Potential initial users are community indoor-air groups and educators who already possess sensors. An importable CSV and downloadable protocol could fit their workflow. Their interest has not been tested; no contact was made.

**Decision: hold behind hypothesis 1; extend existing tools if possible.** Strong existing prior art and field variability weaken the case for a new standalone invention.

## Query log and epistemic limits

Search strings used, grouped by sequence (including the malformed first Stitch Maps query):

1. `carbon dioxide ventilation estimation occupancy mixing assumptions tracer gas decay open source software`; `open source nesting irregular remnants fabric grain defects cutting sequence software`; `repair broken object fragment fitting computational archaeology pottery open source`.
2. `knitting repair dropped stitch cable mistake algorithm software dependency graph ladder down`; `computational knitting repair mistakes stitch graph open source`; `3D printing repair broken objects generate repair jig software research repairability`.
3. `"KnitPicking Texture" programming modifying complex knitted textures`; `"Knitspeak" knitting repair`; `knitting repair software laddering down planner`; `"ventilation" "experiment design" "CO2" estimation`.
4. `site.stitch-maps.com repair mistakes stitch maps ladder down`; `"knitting" "repair" "planner" software`; `"knitting" "minimum" "unravel" algorithm`; `"ventilation" "113432" software`.
5. `site:stitch-maps.com "How" "stitch"`; `site:knitty.com "fix" "cable" "ladder"`; `site:techknitting.blogspot.com "cable" "fix"`; `"knitting repair" algorithm graph`.
6. `optimal experimental design tracer kinetic compartment model identifiability sampling pharmacokinetics open source PopED`; `CO2 decay ventilation experiment design uncertainty multi room sensor placement open source`; `site:nist.gov CONTAM multizone airflow contaminant transport software`.

Several primary pages and abstracts were opened; remaining evidence came from indexed excerpts. The UPC PDF for NVAPF returned HTTP 403 and the CMU KnitPick page returned HTTP 502 on direct opening; their indexed text was available, with the author-hosted KnitPick paper also found. No patents were comprehensively searched, no full citation graph was traversed, and no commercial product was tested. English-language search and model-generated hypothesis selection introduce substantial bias. Most competitor pages are undated; retrieval date must not be mistaken for publication date.

**Raw outcomes:** generic nesting was contradicted by existing implementations; uncertainty-aware ventilation estimation was contradicted as a novelty claim by NVAPF; knitting graph representation was contradicted as a novelty claim by KnitPick and `knit_graph`. Narrower repair planning and experimental-design workflows remain hypotheses because this search did not resolve them. Lack of an exact search hit is not evidence of originality.
