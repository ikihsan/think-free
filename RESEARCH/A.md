# Research A — Fundamental Thinker

<!-- origin-meta
owner: RESEARCH.md
status: sealed
last-verified: 2026-10-03
-->

Research date: 2026-10-03. Independent first pass; only `MISSION.md` was consulted from this workspace. No personal memories or other research reports were consulted. Public sources were retrieved on this date. No contacts, external writes, installations, or purchases. One standard-library Python experiment ran in memory; its code and complete output are below.

## Decision

**Advance one hypothesis to a falsification experiment: a sidewalk survey planner that identifies which missing measurements can change the next infrastructure decision.** Working description: “Survey before concrete.” Do not yet select it as the project. Confidence is moderate in the problem, low in differentiation, and very low in adoption until tested with practitioners.

The useful output would be concrete: “Before selecting between these two repair packages, measure curb X and slope Y. Those observations decide which package actually connects these homes to this bus stop. Here are the affected paths and all assumptions.”

This is deliberately narrower than another accessibility map, routing app, or generic optimization platform. Those already exist. No claim of mathematical novelty is warranted. The proposed contribution is a usable, inspectable workflow joining uncertain physical measurements, combinations of repairs, and community-specific access outcomes.

## First-principles exploration across three domains

The starting question was: **Where does a small amount of scarce effort fail because the system rewards counting assets instead of restoring a capability?**

| Domain | Fundamental constraint | Possibility examined | Evidence-driven disposition |
|---|---|---|---|
| Repair of small appliances | A working device is a conjunction of functioning subsystems. An observation can avoid unnecessary part replacement, but diagnosis requires reliable symptom-to-fault knowledge. | Choose the next cheap diagnostic measurement by information gained per unit effort. | Not advanced: this is old decision-theoretic troubleshooting. ORDS lacks standardized sequential diagnostic traces and even removed its model field for data quality reasons. Data capture and model-specific expertise would likely dominate engineering. |
| Electricity during outages | Stored energy is finite; maintaining a capability can require several loads, while some loads can be deferred. | Optimize useful household functions rather than treat all electricity demand as one critical load. | Not advanced: REopt already provides open energy sizing, dispatch, outage analysis and critical-load construction. A household-facing wrapper may help, but this pass did not establish a substantive gap or real user demand. |
| Neighborhood accessibility | An origin-to-destination trip requires every relevant path segment to be traversable. Two individually unhelpful curb repairs can jointly unlock a route. Unknown dimensions can invalidate an apparent benefit. | Spend the next survey hour where its result changes a feasible repair decision. | Advance for testing: a primary-source agency partnership documents missing sidewalk information preventing concrete plans. Existing graphs and schemas provide a plausible substrate. Strong related prior art means differentiation must be demonstrated, not asserted. |

The cross-domain abstraction is **decision value of an observation**, not information volume. A highly uncertain fact can be irrelevant to the decision; one low-entropy measurement at a bottleneck can reverse it. This abstraction is established mathematics. Its usefulness here remains a hypothesis.

## Hypothesis A1: decision-directed sidewalk surveys

### Observation and proposed mechanism

**Source-supported:** TCAT reports that King County needs to improve sidewalks near transitional housing but lacks enough condition information to form concrete project plans [S1, S2]. The OpenSidewalks schema explicitly permits generic curbs whose type is unknown, and width, surface, and incline are optional footway fields [S3]. These are real representational gaps, not an invented data model.

**Inference:** A complete city inventory may be unnecessary for choosing the next small repair package. Identify the measurements most likely to resolve that particular choice, then collect those first.

**Proposed mechanism, unimplemented:**

1. Import an existing pedestrian network, preserving absent attributes as unknown. Start with one neighborhood and a manually reviewed set of origins, destinations, and candidate interventions.
2. Keep physical observations separate from user-specific traversal requirements. Show several explicit profiles and sensitivity ranges; do not label every person using a particular mobility aid identically.
3. Evaluate feasible **sets** of repairs under a budget. Return reachable destinations and witness paths, not a citywide accessibility score alone.
4. For each inspectable unknown, compute the expected reduction in decision regret, with probabilities supplied or estimated transparently. When probabilities are indefensible, report scenario bounds and whether an observation can flip the preferred decision rather than invent precision.
5. Produce a short fieldwork list with the measurement needed, its location, and a before/after explanation. Update recommendations when observations return. Export ordinary geospatial files and a human-readable report.

The candidate's technical core is smaller than a worldwide mapping platform. A first implementation could use JSON/GeoJSON and exhaustive enumeration on small fixtures; no AI, cloud service, phone sensors, or special hardware is required.

### Exact prior-art threats and proposed difference

| Primary prior art inspected | What already exists | Proposed difference that still needs verification |
|---|---|---|
| AccessMap [S4] | Preference-sensitive routing; enriched sidewalk graphs; outdoor/indoor transit connections. | Choose observations for an investment decision rather than provide a current route. Do not rebuild its graph pipeline. |
| Bolten & Caspi, PPNA, 2021 [S5] | Personalized graph interpretation, walksheds, amenity access, comparative accessibility metrics, centrality; public code/data. | Add explicit unknown-world scenarios, repair-set decisions, and the value of collecting a particular missing attribute. Its existing metrics should be baselines. |
| Halabya & El-Rayes, 2019 online / 2020 issue [S6] | Multiobjective optimization of pedestrian upgrade schedules, interrupted trips, duration, budget, and maps; case with 4,178 noncompliant facilities. | Choose what to inspect before committing to a schedule. Merely optimizing repair packages would duplicate this work. Full paper access was blocked; unexamined details may eliminate this distinction. |
| Li et al., CHI 2025 [S7] | Five mobility-aid groups, barrier perception data, personalized maps and routing demonstrations. | Use explicit human-selected needs and show differing outcomes. This paper undermines any universal “wheelchair accessibility” scalar. |
| General decision-theoretic inspection [S10] | Information gained per unit inspection cost was already described in 1995. | Domain integration and public auditability, not a new information-theoretic principle. |

**Closest threat is a combination of PPNA, an upgrade optimizer, and an existing value-of-information algorithm.** If an ordinary notebook joining those already answers the actual practitioner question adequately, contribute upstream or abandon the standalone project. Search non-results do not establish originality. This pass did not inspect all municipal GIS extensions, consulting products, dissertations, or research software.

### Strongest failure case

Survey prioritization may not be the binding constraint at all. Procurement, utility relocation, legal requirements, right-of-way, funding rules, inaccessible building entrances, and residents' actual destinations may dominate. A beautifully optimized curb list could have no effect on any funded decision. Missing data may also be spatially correlated; a nominally optimal measurement policy built on arbitrary independent priors could waste field visits.

Other important objections:

- Incorrect graph connectivity can outweigh attribute uncertainty. Measuring the right curb in the wrong network proves little.
- Repair cost and constructability are uncertain too. If these dominate uncertainty, the product must prioritize engineering feasibility information or fail the test.
- Accessibility is person-specific. Aggregating weighted trips can sacrifice a small underserved group; expose per-profile outcomes and allow hard constraints rather than burying this choice in one objective.
- Street-level imagery may not reveal cross slope or exact width. No inferred field value should silently become verified ground truth.
- A planning model cannot certify safe navigation or statutory compliance. The initial output should support planning and fieldwork, not direct vulnerable travelers along unverified paths.
- Civic users may prefer a QGIS extension or contribution to OpenSidewalks over a separate application. Stars are particularly weak as a utility proxy here.

### Adoption hypothesis

An initial adopter would be a small accessibility advocacy group partnered with a municipal planner, selecting a short list of improvements near a school, housing site, or transit stop. Delivering one agreed survey itinerary plus an inspectable recommendation may create value before citywide deployment. This is an inference from the stated planning problem, not validated demand; no practitioner was contacted.

## Small experiment actually run

**Purpose:** Test whether missing-data entropy and decision value can differ, and whether complementary repairs matter. This is an intentionally engineered sanity fixture, not an unbiased benchmark or evidence of real-world impact.

There are two independent binary observations, `x` and `y`, with 50/50 priors. Budget is 2. Repairs `a1` and `a2` each cost 1; both plus passable curb `x` are needed to reach a destination with weight 10. Repair `b` costs 2 and opens a destination with weight 6. Observation `y` controls an unrelated destination with weight 1, requiring no repair. Every destination weight and prior is synthetic.

Run command (Python standard library only):

```bash
python3 - <<'PY'
from itertools import product, combinations
worlds = list(product((False, True), repeat=2))
actions = [frozenset(c) for r in range(4) for c in combinations(('a1','a2','b'), r) if sum({'a1':1,'a2':1,'b':2}[i] for i in c) <= 2]
def score(action, world):
    x, y = world
    return 10 * (x and {'a1','a2'} <= action) + 6 * ('b' in action) + int(y)
def best(ws):
    return max((sum(score(a,w) for w in ws)/len(ws), tuple(sorted(a))) for a in actions)
base = best(worlds)
print('base expected reachable weight and repairs:', base)
for obs in (0,1):
    values=[]
    for value in (False,True):
        ws=[w for w in worlds if w[obs] == value]
        answer=best(ws)
        values.append(answer[0])
        print('observe', 'xy'[obs], '=', value, ':', answer)
    ev=sum(values)/2
    print('expected post-observation score:',ev,'value of information:',ev-base[0])
print('uniform random one-observation expected score:',(8.5+6.5)/2)
print('full-information score:',sum(best([w])[0] for w in worlds)/len(worlds))
assert base == (6.5, ('b',))
assert sum(best([w for w in worlds if w[0] == v])[0] for v in (False,True))/2 == 8.5
assert sum(best([w for w in worlds if w[1] == v])[0] for v in (False,True))/2 == 6.5
print('all assertions passed')
PY
```

Observed output; exit status 0:

```text
base expected reachable weight and repairs: (6.5, ('b',))
observe x = False : (6.5, ('b',))
observe x = True : (10.5, ('a1', 'a2'))
expected post-observation score: 8.5 value of information: 2.0
observe y = False : (6.0, ('b',))
observe y = True : (7.0, ('b',))
expected post-observation score: 6.5 value of information: 0.0
uniform random one-observation expected score: 7.5
full-information score: 8.5
all assertions passed
```

**Interpretation:** Both observations have identical entropy; only `x` changes the repair decision. A single-repair marginal-gain heuristic also cannot discover `a1+a2` by its first individual gain. The fixture verifies that the proposed problem is distinct from “map the most uncertain point” and “repair the largest isolated defect.” It provides no estimate of how often this occurs in real neighborhoods. The printed random-policy mean is calculated directly from the two observation-policy means, not Monte Carlo sampling.

## Next falsification experiment, bounded and reproducible

**Available substrate confirmed:** `https://github.com/OpenSidewalks/PLoS-cities-complex-systems` contains the PPNA study's data, notebooks, and code [S11]. A live unauthenticated GitHub contents request returned its `data`, `artifacts`, `reach_metrics`, and notebook directories. The README identifies `data/seattle.geojson` as public-domain data, while some OSM-derived artifacts carry ODbL. No dataset was downloaded or parsed in this pass; exact graph schema, size, completeness, and compatibility remain unverified.

1. Pin a commit and inspect a small complete-enough neighborhood extract from this repository. If no extract contains the attributes required for a meaningful masking experiment, record that failure; do not synthesize plausible attributes and call it real-data validation.
2. Select 10–20 feasible candidate interventions and a small set of origin/destination pairs. Label intervention costs as synthetic unless sourced. Hide observed curb/incline/width facts at random and in contiguous blocks to test correlated gaps. Preserve truth separately.
3. Compare decision-directed observation selection against random selection, highest topological centrality, highest missingness/entropy, and shortest fieldwork-tour heuristics. Use identical observation and travel-time budgets.
4. Measure realized repair-decision regret relative to the full-observation optimum, regret after each field visit, fieldwork distance, runtime, and whether witness paths reproduce the stated benefits. Include a simple exhaustive optimizer on tiny subgraphs to check approximations.
5. Pre-register a provisional go/no-go gate: at least 25% lower median regret than the strongest simple baseline across 30 fixed masking seeds, including block-missingness cases, without greater fieldwork cost. Report distributions, not only the mean. This threshold is a proposed product hurdle, not a published standard.
6. Failure if gains disappear under modest cost/profile/priors changes, if most recommendations depend on unmeasured structural data, or if useful regret cannot be defined without arbitrary demand assumptions. Even a passing result only supports computational potential.
7. Before product engineering, have a planner and affected residents independently review one anonymized planning case: can the requested measurements actually change a decision they control, and are the outcomes meaningful? This human validation remains unperformed and requires a later authorized engagement plan.

## Source ledger

All URLs below were inspected through public web results/pages on 2026-10-03. Page retrieval date is not publication date. Search-engine relative ages were not used as publication dates. Exact quantitative claims are restricted to what the identified source supports.

- **S1 — TCAT project page:** https://sidewalks.washington.edu/ . Publication date not displayed. Directly opened. Supports an agency-reported planning problem caused by incomplete sidewalk information and the existence/purpose of OS-CONNECT. Does not establish demand for this proposed product or that the problem remains unresolved at every site today.
- **S2 — TCAT proviso brief:** https://sidewalks.washington.edu/wp-content/uploads/2024/12/tcatprovisobrief.pdf . Document dated November 2024; URL upload directory December 2024. Parsed both pages. Supports the King County example and resource constraints collecting/updating sidewalk data. Its historical coverage statements are not treated as current coverage.
- **S3 — OpenSidewalks schema:** https://sidewalks.washington.edu/2024/05/30/schema/ . URL date 2024-05-30; includes schema history for 2023/2024. Directly inspected relevant node/edge definitions. Supports unknown curb types and optional width/surface/incline fields. Does not quantify real dataset missingness.
- **S4 — AccessMap documentation:** https://sidewalks.washington.edu/2024/06/03/accessmap/ . URL date 2024-06-03; current page retrieved. Supports configurable mobility preferences, enriched graphs and OSM/TDEI inputs. It is product documentation; route quality was not tested.
- **S5 — PPNA paper:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0248399 . Published 2021-03-19. Directly inspected abstract and methodology. Supports mature personalized graph metrics and linked reproducibility code. Its profile examples are explicitly stereotyped and are not universal physical limits.
- **S6 — Upgrade optimization paper's university record:** https://experts.illinois.edu/en/publications/optimizing-the-planning-of-pedestrian-facilities-upgrade-projects/ . University record says issue publication 2020-01-01; publisher search result says online 2019-10-30. Directly inspected university abstract. Supports prior optimization of interruption, schedule and budget; full publisher text at https://doi.org/10.1061/(ASCE)CO.1943-7862.0001730 returned 403, so details beyond abstract were not verified.
- **S7 — Accessibility for Whom?:** https://arxiv.org/html/2502.19888v1 . Submitted 2025-02-27; CHI conference 2025-04-26 to 2025-05-01. Directly inspected abstract, methods overview and application descriptions. Supports variation in barrier perceptions among 190 respondents across five mobility groups and publicly linked data/code. It does not establish a safe physical traversal rule from an image rating.
- **S8 — ORDS:** https://openrepair.org/open-data/open-standard/ . Undated page; identifies v0.3 as released December 2021. Directly inspected. Supports field scope, free-text problems/outcomes and removal of model field for collection/quality difficulties. It does not prove no partner has richer internal diagnostic data. Dataset repository also inspected: https://github.com/openrepair/data ; its README's 305,649 powered-item count differs in scope from the site's >400,000-all-items headline, so neither is used as a blanket current count.
- **S9 — REopt:** https://github.com/NatLabRockies/REopt.jl and https://natlabrockies.github.io/REopt.jl/dev/ . README undated; retrieved documentation footer says generated 2026-09-30. Supports open-source sizing/dispatch/resilience optimization. https://www.nlr.gov/reopt/curriculum/videos/reopt-lite-tutorial-module-4-text additionally describes critical-load percentage/upload/component-builder inputs. No REopt optimization was executed.
- **S10 — Historical diagnosis prior art:** https://www.sciencedirect.com/science/article/abs/pii/095183209500022T . Publisher abstract/search excerpt identifies a 1995 paper, “General inspection strategy for fault diagnosis—minimizing the inspection costs.” Supports information gain per inspection cost as old prior art. Full text was not inspected; this is not a claim about available community-repair software.
- **S11 — PPNA code/data:** https://github.com/OpenSidewalks/PLoS-cities-complex-systems . Undated README; connected to the 2021 paper. Directly inspected README and GitHub root contents API. Confirms an existing reproducibility package and differentiated licenses. Dependencies were not installed and notebooks were not run.

Additional lead not relied upon: a University of Saskatchewan thesis search result, “Risk-Based Decision Policy to Aid Prioritization of Unsafe Sidewalk Locations for Maintenance and Rehabilitation,” discusses sensitivity/value of information. Its retrieved bitstream URL returned 410. This is a specific unresolved prior-art threat requiring recovery before any novelty language.

## Search log

Queries actually submitted, in order of research batches:

1. `site.opensidewalks.com accessibility network sidewalk planning barriers`
2. `site.openrepair.org data standard repair barriers diagnosis`
3. `site.nrel.gov resilience critical load outage household power planning REopt`
4. `"sidewalk" "optimization" "curb ramps" accessibility network`
5. `"OpenSidewalks" "prioritize"`
6. `"REopt" "load shedding" priority`
7. `"repair" "diagnosis" "information gain" open source`
8. `sidewalk accessibility "value of information"`
9. `pedestrian network "survey" "uncertainty" "optimization"`
10. `site.github.com NREL REopt loads priority outage load shedding`
11. `site.openrepair.org repair fault finding diagnostics time`
12. `"Optimizing the Planning of Pedestrian Facilities" Halabya pdf`
13. `"sidewalk" "survey prioritization" accessibility`
14. `"pedestrian" "value of information" accessibility network`
15. `site.github.com sidewalk intervention optimization survey`

## Handoff

Advance A1 only to the bounded experiment above. Strong value story; substantial prior art; missing data and decision ownership are the main risks. Reject another accessible router or generic repair optimizer as the invention. If the survey-policy advantage or practitioner decision relevance fails, abandon A1 instead of broadening its scope to hide the failure.
