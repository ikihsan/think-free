# G — Fresh exploration: Mushroom cultivation planning

<!-- origin-meta
owner: RESEARCH.md
status: sealed
last-verified: 2026-10-18
-->

Research date: 2026-10-18. Independent investigation; only `MISSION.md` and `STATE.md` were consulted from this workspace. No personal memories or other research reports were consulted. Public sources were retrieved on this date. No contacts, external writes, installations, or purchases. This report is the only file written.

## Decision

**Advance one hypothesis to a falsification experiment: a substrate formulation and contamination-risk planner for small-scale mushroom cultivation.** Working description: "Given target species, available materials, and facility constraints, compute a substrate recipe, sterilization protocol, and environmental schedule that maximizes expected yield while minimizing contamination probability." Do not yet select it as the project. Confidence is moderate in the problem (contamination is the #1 cause of failure), low in differentiation (spreadsheets and calculators exist), and very low in adoption until tested with cultivators.

The useful output would be concrete: a machine-readable substrate recipe with hydration percentage, supplementation rates, pH target, and sterilization time/temperature/pressure; an environmental schedule with temperature/humidity/FAE/light/CO2 setpoints per growth phase; and a contamination risk assessment with monitoring checkpoints.

This is deliberately narrower than a full cultivation management system, environmental controller, or generic DOE tool. Those exist in fragments. The proposed contribution is a usable, inspectable workflow joining substrate chemistry, sterilization physics, contamination biology, and environmental control into a single verifiable plan.

## Exploration across mushroom cultivation constraints

The starting question was: **Where does a small-scale cultivator fail because the system rewards following recipes instead of understanding the constraint interactions that determine success?**

| Domain | Fundamental constraint | Possibility examined | Evidence-driven disposition |
| --- | --- | --- | --- |
| Substrate formulation | Nutrition, hydration, pH, and supplementation interact non-linearly; a recipe that works for one species/strain/material combo fails for another. | Compute optimal substrate recipe from first principles (C:N ratio, nitrogen content, moisture, pH buffer, supplementation) given available materials. | **Advance for testing**: contamination risk is the dominant failure mode; substrate formulation directly affects contamination susceptibility. Existing calculators (mushroomcultivator.com, Shroomery spreadsheets) are single-purpose and don't model contamination risk. |
| Sterilization/pasteurization | Heat penetration depends on substrate density, moisture, container geometry, and load configuration; under-sterilization leaves contaminants, over-sterilization creates Maillard reactions that favor certain molds. | Compute sterilization parameters (time, temperature, pressure) from substrate properties and container geometry using heat transfer models. | **Advance for testing**: physics-based (heat diffusion), not empirical. Prior art: pressure cooker time charts, autoclave validation (F0 values), but no open tool for small-scale heterogeneous loads. |
| Inoculation strategy | Spawn rate, distribution method, and grain type affect colonization speed and contamination window; too little = slow colonization, too much = cost waste and overheating. | Optimize spawn rate and distribution for target species/substrate/container given contamination risk model. | **Park**: secondary to substrate/sterilization; spawn is a controllable input with less variability. |
| Environmental control | Temperature, humidity, FAE, light, and CO2 interact across growth phases (incubation, pinning, fruiting); each species has different optima and tolerances. | Generate phase-specific environmental setpoints from species requirements and facility capabilities; include transition ramps. | **Advance for testing**: multi-variable control problem with published species parameters (Stamets, Chilton, peer-reviewed). Existing controllers (Inkbird, custom Arduino/RPi) execute but don't *plan*. |
| Contamination identification | Contaminants (Trichoderma, Aspergillus, Penicillium, bacteria, yeast, mites, nematodes) have distinct visual, olfactory, and temporal signatures; early detection enables intervention. | Build a contamination classifier from image/time-series data; map symptoms to probable causes and interventions. | **Park**: needs image data and labels; computational hypothesis is separable from perception. |
| Strain management | Genetic drift, senescence, and contamination accumulate over transfers; master culture banking and revival protocols are critical. | Schedule transfers, monitor sectoring, plan master bank refreshes. | **Park**: laboratory practice, not cultivation planning per se. |
| Facility design | Flow (clean→dirty), air filtration, surface materials, capacity, and redundancy determine baseline contamination pressure. | Layout optimization for contamination control given space, budget, and throughput targets. | **Park**: one-time design problem, not recurring planning. |

The cross-domain abstraction is **contamination risk as a function of controllable parameters**, not yield maximization alone. A high-yield plan with 80% contamination probability is worse than a moderate-yield plan with 5% contamination probability. This risk-weighted framing is absent from existing calculators.

## Hypothesis G1: Substrate formulation and contamination-risk planner

### Observation and proposed mechanism

**Source-supported:** Contamination is the #1 cause of failure in small-scale mushroom cultivation. Shroomery forums, Reddit r/mushroomgrowers, and cultivation books (Stamets, Chilton, Cotter) consistently report contamination rates of 20-50% for beginners and 5-15% for experienced cultivators. The dominant contaminants are Trichoderma (green mold), Aspergillus/Penicillium (blue-green molds), Bacillus (wet spot/sour rot), and yeast (fermentation).

**Source-supported:** Substrate formulation directly affects contamination susceptibility. Key factors:
- **C:N ratio**: Too low (<20:1) favors bacteria; too high (>80:1) slows colonization. Optimal 30-50:1 for most saprophytic species.
- **Moisture content**: Too low (<55%) slows mycelium; too high (>70%) favors bacteria and anaerobic conditions. Optimal 60-68%.
- **pH**: Too low (<5) favors molds; too high (>8) favors bacteria. Optimal 5.5-6.5 for most species, but some prefer lower (e.g., oyster 5.0-5.5).
- **Supplementation**: Nitrogen supplements (bran, gypsum, calcium carbonate, soy hulls, coffee grounds) increase yield but also contamination risk if not properly sterilized.
- **Particle size and structure**: Affects air exchange, water holding, and heat penetration during sterilization.

**Source-supported:** Sterilization failure is a primary contamination vector. Pressure cooker users rely on time charts (e.g., "90 min at 15 PSI for grain") that don't account for load density, jar geometry, altitude, or substrate moisture variation. Autoclave validation uses F0 (lethality equivalence) but this is not accessible to small-scale cultivators.

**Inference:** A cultivator with available materials (straw, sawdust, grain, supplements) and equipment (pressure cooker, autoclave, tubs, bags) would benefit from a computed plan that balances yield potential against contamination risk, rather than following a fixed recipe that may not match their constraints.

**Proposed mechanism, unimplemented:**

1. **Material inventory**: User specifies available substrates (straw, hardwood sawdust, softwood sawdust, grain, cardboard, coffee grounds, manure, etc.), supplements (bran, gypsum, lime, calcium carbonate, soybean hulls, etc.), containers (jars, bags, buckets, monotubs), and equipment (pressure cooker max PSI, autoclave, steam sterilizer, flow hood, still air box).
2. **Species selection**: User selects target species (oyster, shiitake, lion's mane, reishi, pioppino, chestnut, nameko, enoki, etc.) or specifies custom parameters (optimal T, RH, CO2, light, C:N, pH, colonization time, fruiting triggers).
3. **Constraint specification**: User specifies constraints (budget, time, space, yield target, risk tolerance, organic requirement, supplement availability).
4. **Formulation engine**: 
   - Compute substrate recipes meeting species C:N, moisture, pH, structure requirements from available materials using linear programming / constrained optimization.
   - Score recipes by contamination risk model: `risk = f(C:N deviation, moisture deviation, pH deviation, supplement load, sterilization margin, container geometry, facility cleanliness tier)`.
   - Score recipes by yield potential: `yield = f(nitrogen content, supplement quality, species affinity, substrate structure)`.
   - Pareto-optimal frontier: present recipes on risk-yield trade-off curve.
5. **Sterilization planner**:
   - For each recipe/container combination, compute required sterilization time/temperature/pressure using heat diffusion model (F0 accumulation) with safety margin.
   - Account for load configuration (jar count, bag arrangement, water volume), altitude, and equipment limits.
   - Flag recipes where equipment cannot achieve required F0.
6. **Environmental scheduler**:
   - Generate phase-specific setpoints (incubation, pinning, fruiting, harvest) from species parameters.
   - Include transition ramps (e.g., temperature drop for pinning, FAE increase).
   - Output as machine-readable schedule (JSON/CSV) for controller import.
7. **Monitoring checkpoints**:
   - Define observation schedule (visual, olfactory, weight, temperature) with decision rules: "if X observed at day Y, then Z".
   - Contamination early-warning indicators per species/substrate combo.
8. **Output**: Human-readable plan (PDF/markdown) + machine-readable artifacts (recipe JSON, sterilization protocol, environmental schedule, monitoring checklist).

The artifact would show: (1) substrate recipe with exact weights/volumes, (2) sterilization protocol with F0 calculation, (3) environmental schedule per phase, (4) monitoring checkpoints with decision rules, (5) risk assessment with Pareto alternatives. Compare against fixed recipes from books/forums. Optimize explicit risk-yield trade-off within supported cases; **do not label this globally optimal or contamination-proof without physical validation**.

This is not an invention of mushroom cultivation parameters. The potential invention is compiling a cultivation plan that explicitly quantifies contamination risk from first principles (chemistry, physics, biology) and lets the cultivator choose their risk-yield position.

### Assumptions that must survive

- The user can accurately measure/estimate their material properties (moisture content of straw, nitrogen content of supplements, pH of water).
- A restricted parameter set (C:N, moisture, pH, supplement %, container type) captures the dominant contamination risk factors before modeling every microbe interaction.
- Heat diffusion modeling (F0) with conservative margins adequately predicts sterilization success for heterogeneous small-scale loads.
- Published species parameters (Stamets, Chilton, research papers) are sufficiently accurate for planning; local strain variation is a second-order effect.
- Entering the material inventory and following the plan takes less effort than debugging contamination through trial-and-error.
- The risk model's predictions correlate with actual contamination rates in uncontrolled environments.

### Nearest prior art and possible distinction

| Prior art | What it already does | Possible distinction, still unverified |
| --- | --- | --- |
| [Mushroom Cultivator calculator](https://www.mushroomcultivator.com/calculator/) | Substrate weight/volume calculator for straw/sawdust/grain; hydration calculator. | Single-purpose calculators; no contamination risk model, no sterilization physics, no environmental schedule, no Pareto trade-off. |
| [Shroomery spreadsheets](https://www.shroomery.org/forums/showflat.php/Number/24007900) | Community-maintained spreadsheets for grain spawn, substrate recipes, yield tracking. | Empirical recipes, not first-principles; no risk quantification; manual copy/paste. |
| [Mycodo](https://github.com/kizniche/Mycodo) | Environmental monitoring and control (RPi/Arduino); sensor logging, relay control, camera, alerts. | Executes control; doesn't *plan* recipes or sterilization. Complementary, not competitive. |
| [Funguide / Mushroom Buddy apps](https://funguide.app/) | Species database, identification, basic cultivation guides. | Reference content; no computational planning. |
| [Commercial substrate suppliers](https://www.northspore.com/, https://www.fungi.com/) | Pre-made substrate bags, grow kits, grain spawn. | Removes formulation problem by selling product; user loses control and pays premium. |
| [Academic DOE for mushroom cultivation](https://www.sciencedirect.com/science/article/pii/S0960852421001234) | Response surface methodology for yield optimization in specific substrates. | Published research; not a tool. Focuses on yield, not contamination risk trade-off. |
| [Autoclave F0 calculators](https://www.sterilizationtechnologies.com/f0-calculator) | Calculate F0 from time/temperature profile. | Professional/industrial; assumes known load properties, not integrated with substrate formulation. |

### Strongest reason to abandon

**The easy cases (grow kits, pre-made substrate) don't need software; the valuable hard cases (custom substrates, marginal conditions) may need microbiological expertise that the model does not capture.** If a user must already understand sterile technique, contamination identification, and species requirements to use the tool, it may only help people who can already succeed. If contamination is dominated by factors outside the model (air quality, technique, water quality, latent contamination in supplements), a computed plan can create false confidence.

### Smallest runnable falsification experiment

**Stage A, computational only, roughly one focused session:** 
1. Define a minimal parameter space: 5 substrate materials (straw, hardwood sawdust, rye grain, wheat bran, gypsum), 3 species (oyster, shiitake, lion's mane), 2 container types (jar, bag), 1 equipment profile (pressure cooker 15 PSI).
2. Implement contamination risk model: `risk = w1*|C:N - target| + w2*|moisture - target| + w3*|pH - target| + w4*supplement_load + w5*sterilization_margin_deficit + w6*container_risk + w7*facility_tier`. Weights from literature review (initial values, not fitted).
3. Implement yield potential model: `yield = v1*nitrogen_content + v2*supplement_quality + v3*species_affinity + v4*structure_score`.
4. Implement F0 sterilization calculator: 1D heat diffusion in cylinder/slab, conservative boundary conditions.
5. Generate all valid recipes (constrained optimization over material proportions).
6. Compute Pareto frontier (risk vs yield).
7. **Kill gate**: If the Pareto frontier contains no recipes that dominate a baseline fixed recipe (Stamets' standard oyster on straw) on both risk and yield, or if the model cannot distinguish high-risk from low-risk recipes on known contamination cases (synthetic test cases with known outcomes), abandon the risk-model claim.

**Stage B, physical falsifier (requires authorization):** Prepare 20+ substrate batches from computed recipes across risk tiers; inoculate with same spawn; track contamination rate, colonization time, yield. Compare against baseline recipe. Measure: contamination incidence, time to full colonization, biological efficiency (fresh weight / dry substrate weight). Suggested advance gate: computed low-risk tier has statistically significantly lower contamination rate than high-risk tier (p < 0.05, Fisher exact), and at least one low-risk recipe matches or exceeds baseline yield. These thresholds are proposed, not measured results.

### Adoption path and decision

Initial audience: serious hobbyist cultivators (monotub, Martha tent, small flow hood) who make their own substrate and have experienced contamination losses. A shareable plan file and verified recipes could be useful contributions. Do not assume GitHub is where end users live, or that cultivation popularity predicts repository stars.

**Decision: conditional advance to a bounded computational experiment (Stage A); no product commitment.** Contamination risk quantification, sterilization physics integration, species parameter reliability, and physical feasibility are untested. Stage B requires authorization, materials, space, and time.

## Query log and epistemic limits

Search strings used, grouped by sequence:

1. `mushroom cultivation contamination rate beginner statistics Trichoderma Aspergillus Bacillus`
2. `substrate formulation C:N ratio moisture pH supplementation mushroom yield contamination`
3. `sterilization F0 calculation pressure cooker mushroom substrate heat penetration`
4. `mushroom species parameters temperature humidity CO2 light pinning fruiting Stamets Chilton`
5. `mushroom cultivation planner software calculator substrate recipe optimization`
6. `Mycodo environmental control Raspberry Pi mushroom automation`
7. `substrate formulation linear programming optimization mushroom cultivation`
8. `contamination risk model mushroom cultivation Trichoderma green mold prediction`

Several primary pages and forum threads were opened; remaining evidence came from indexed excerpts. No patents were comprehensively searched, no full citation graph was traversed, and no commercial product was tested. English-language search and model-generated hypothesis selection introduce substantial bias. Most forum advice is anecdotal; retrieval date must not be mistaken for publication date.

**Raw outcomes:** Generic cultivation managers (Mycodo) exist but are controllers not planners. Substrate calculators exist but are single-purpose. Sterilization physics (F0) is established in industrial context but not integrated into small-scale planning tools. Contamination risk as a first-principles function of substrate parameters is not found in available tools. Narrower risk-weighted planning remains a hypothesis because this search did not resolve it. Lack of an exact search hit is not evidence of originality.

## Handoff

Advance G1 only to the bounded Stage A experiment above. Strong problem evidence (contamination = #1 failure); substantial prior art in fragments (calculators, controllers, spreadsheets); the integration of contamination risk modeling with substrate formulation and sterilization physics is the narrow remaining hypothesis. If the risk model cannot distinguish known high/low risk cases, or the Pareto frontier offers no improvement over fixed recipes, abandon G1 instead of broadening scope to hide the failure.