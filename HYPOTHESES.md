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
`007-build-timestamps` (E3's prevalence census) and
`008-build-timestamp-attribution` (its cause attribution).

**E012, E021, E023, E024, E025, E026 and E027 tested this mission's own
methods rather than a candidate** — the generator, the serving channel, a rate
read without a control, a counting rule, a disclosure floor, the shape of a
corpus's tail, and a screen's own verdict. All seven moved to
[`HYPOTHESES-experiments.md`](HYPOTHESES-experiments.md) on 2026-10-09 at this
file's line cap. None produced a candidate; each named what its own instrument
had actually measured, and a reader asking that question should not have to load
the live candidate index to get it.

**E034 tested a generator, not a candidate** (`EXPERIMENTS/034-reask-tail/`,
T-0078). Its declared kill gate A4: if no two tags with `tail` n ≥ 50 have
disjoint duplicate-closure intervals, "sample the tail" is true and useless and
the candidate dies. **A4 fired** — 7 tags eligible, 12 disjoint pairs, pooled tail
**0.1352** against the `Active` tab's **0.0303** — so this is not a sampling note.
Two further declared claims failed and no candidate entered or left the table
because none was produced: **D6**, because duplicate closure is a *moderator act*
and at 3–5 tags per site the tag and the site are not separable (4/10 within-site
disjoint pairs against 14/26 cross-site), and **B1**, because the no-accepted-answer
share does not separate the two arms (CI95 [−0.0774, +0.3075]). What changed is the
inventory of levers: **the first demand-side instrument in this record that returned
positives**, on a platform-owned label rather than a linkage rule of this
repository's, with the strongest accessible alternative — the ordering that domain's
own readers see — as its control. Its contribution is a **per-domain** rate, which no
earlier draw had, and its cost is that the reading is `not_established` until tag is
separable from site (F057). Two facts outlive it: the **canonical edge is unreachable**
through nine named channels, so `closed_reason` is the only handle there is; and the
label is **ten literals**, which makes every enumeration rate in this record a floor
(D063).

**E036 killed the candidate E034's numbers were being collected for**
(`EXPERIMENTS/036-search-backlog/`, T-0080). The population is real and stands. The
tool was not: **one unauthenticated request** to
`/search/advanced?site=stackoverflow&tagged=git&sort=votes&order=asc&pagesize=100`
returns 100 questions ascending by score, **81 of them ids already in E034's committed
harvest**, with `closed_reason` in the payload — so **13 duplicate closures per tag per
page, no key and no computation** (**F059**). E035's stated differentiator was the
platform's own label over *a population no surface orders that way*; **the platform
orders it that way itself**, and F058's own evidence had said so about the wrong
interface. Two further corrections ride with it: `closed` is the one filter value
`/search/advanced` does **not** validate, so no closed-only control was ever
establishable from that route's behaviour; and *"the label needs an API key"* was a
per-route fact about `/questions/unanswered` and `/questions/{ids}` generalised to the
platform, when `/search/advanced`'s **default** filter carries it. **D066** requires a
reachability claim to name the interface surface it enumerated; **D067** requires a
candidate whose value is a mechanism to be tested against that mechanism's existing
source **before** a population is measured for it — three experiments and 1125 rows
described a population whose mechanism turned out to be a documented query. **The
population is untouched; what died is the claim that it is unreachable, and the
adoption question is now the whole question and has never been measured.**

**E039 measured what happened to the need corpus's statements, and found the
corpus records recognition, not service** (`EXPERIMENTS/039-need-statement-response/`,
T-0081). E012's 1401 Hacker News comments shaped like "is there a tool that X" were
never followed, and their reply subtrees are the only channel available that is
contemporaneous, demand-side and written by practitioners rather than by a search
engine. All 1276 parent threads captured — 278,686 comments, 1391 needs against
277,295 matched controls.

The declared kill gate fired on three estimators: **1.235x** the same-thread control
rate at all ages, 1.238x at ≥180 days, 1.286x within-story, against a bar of 1.5 fixed
before the first fetch. Attention to a need is not distinguishable from position in a
thread. **The two figures that carry the decision are about the channel rather than
the needs: 0 of 1391 needs drew a reply naming a tool new to its own thread, and 1 of
794 requesters whose need drew a reply replied again** (0 of the 77 that drew a link).

So the community answers "has anyone else hit this?" and almost never "here is what to
use" — which is why F029's 0-of-50 and F035's corpus silence are hard to contradict:
prior art is found by searching, and the reply is not where it lives. **D068 restates
the corpus as a recognition signal** rather than reusing it as an artifact one, and
closes the axis item 0 could propose: a return rate of 1 in 794 means the outcome of a
need is not recorded anywhere in the thread it was asked in. **No candidate was
produced and none is claimed.** The 597 unanswered needs are not a queue: 417 sit in
threads where ≥40% of other comments were answered, and a hand-read of 21 found
hardware requests, an article request, a platform request and several requests for a
toggle in someone else's product.

**E042 tested KILL-Q for the stg candidate via agent end-to-end simulation**
(`EXPERIMENTS/042-agent-staging-e2e/`). Eight realistic staging scenarios compared
four approaches: stg (100% success, 1 agent code line), shell baseline (100% success,
180 agent code lines), filterdiff (unavailable), naive git add -p (62% success, 38%
silent failures, 50 agent code lines). **Mechanism parity confirmed** — shell baseline
matches stg exactly, confirming E041. **Packaging is the differentiator**: 180× less
agent code for stg vs shell baseline. Naive approach fails on adjacent modifications,
multi-line insertions, and scattered changes — precisely where line-level splitting
matters. **This paragraph's reading was later overturned by the agent population
itself and must not be read as current.** E043 ran the stated caller — six real
agents — and the packaging advantage was not observed (F075); E044 ran the
discovery population E043's ceiling named, with no line number and no `git diff`,
and got 6 of 6 exact against `nostg` 3 of 3 (F083, D078); E045 read the demand
evidence row by row and found 0 of 189 rows is a population without diff access
(F081); and the two shipped incumbents F082 named from README prose were measured
in E055, which falsified the gap the prose implied (F088, D081). **`stg` is
withdrawn as a candidate and remains a correct unreleased tool.**

**The recurring-expense line is closed** (`EXPERIMENTS/065-*`,
`EXPERIMENTS/066-*`, `EXPERIMENTS/072-merchant-noise-raw/`,
`EXPERIMENTS/073-piecewise-price/`). E065 built a
recurring-payment detector and E066 validated it on 1,056,320 real Berka
transactions, passing all four predeclared gates; E066 then named its own open
axis — *Berka carries no merchant text, so grouping here is cleaner than any
real bank-export string.* E072 ran the detector **unmodified** on 36 real modern
bank exports (34,231 transactions, 29 public repositories, 2021–2026):
**recall 0.394, F1 0.160** (F185). G1 and G2
did not fire. E073 ran the bounded repair F185 named — a piecewise-constant
price model in place of the CV ceiling — and it too failed its predeclared
gates: recall 0.455, F1 margin +0.048 (F186). The pwc model is strictly better
than the CV ceiling on every count but recovers only 2 of 14 misses.

**The failure was not the axis E066 named.** Merchant under-grouping is worth
**6 of 20 misses**; a fixed **amount-CV ceiling of 0.15** is worth the other
**14**, because one price change makes a subscription invisible. The pwc repair
recovers the 2 one-price-step subscriptions (Spotify a35/a36, Comcast); the
other 12 have drift, oscillation, or multiple changes that a one-step model
cannot capture.

Two reading results ride with it. **Actual Budget ships `findSchedules()`**, and
ported onto the same rows it scores F1 0.150 against E065's 0.160 — within
noise, so **the engine is not the differentiator and the merchant axis is**
(but `actual_raw` is a *lower bound* on the incumbent, not a benchmark). And
**a precision figure against a positives-only label set is a lower bound that
happened to sit at 1.0**, which is how E065's headline was earned (D090).

**No candidate, and no usefulness, differentiation or adoption claim.** Actual
already ships the feature, so what is unmeasured is whether anyone pays for
this. Evidence:
[`EXPERIMENTS/072-merchant-noise-raw/README.md`](EXPERIMENTS/072-merchant-noise-raw/README.md),
[`EXPERIMENTS/073-piecewise-price/README.md`](EXPERIMENTS/073-piecewise-price/README.md).

## Status summary

| Candidate | Source | State | Next experiment |
|---|---|---|---|
| Photo-migration auditor | `RESEARCH/B.md`, E001 | **Motivating example disproved** (`FAILURES.md` F001) | Needs a real case where bytes survive and relationships do not |
| Knitting repair planner | `RESEARCH/C.md`, E002 | **Algorithmic-advantage claim abandoned** (`FAILURES.md` F009): minimum-cost repair planning is prior art from 2007–2026, and no tool was found that supplies an intervention sequence for an existing hand-knit structure. Stage A was already settled (T-0010, T-0011) | Nothing software-side. Only Stage B physical work with an experienced knitter, and only after checking that entering the chart patch does not already imply the user can do the repair |
| Adaptive ventilation measurement | `RESEARCH/C.md`, E002 | **Stopped as formulated** (`FAILURES.md` F008, T-0014): a prescribed door-open protocol beats adaptive action selection at equal budget, 0.833 vs 0.792 | Only if the surviving robustness observation (read a second sensor under poor mixing) is tested against existing tools |
| Decision-directed sidewalk survey | `RESEARCH/A.md`, E002 | **Falsified in its motivating regime**: count-budget gate met, fieldwork-cost gate fails (`FAILURES.md` F006) | No product build; treat A1 as a negative result and require a real cost model up front |
| Python packaging determinism (E1–E3) | `RESEARCH/E.md` | E3's mechanism **supported and its candidate abandoned** (`FAILURES.md` F012): timestamps are the only byte-level cause for the one builder here and `SOURCE_DATE_EPOCH` removes all of it, so there is nothing to build. E1 and E2 remain `untested` | Nothing software-side for E3. **Do not run E1** (D020 Screen 3); E2 is time-gated — snapshot one side while a VM is idle |
| Care-handoff discrepancy packet | `RESEARCH/B.md` | Rejected: prior art too direct | — |
| Sewing-projector auto-calibration | `RESEARCH/B.md` | Rejected: no material gap shown | — |
| Automated accessibility certification | `RESEARCH/D.md` | Rejected: universal claim unfalsifiable | — |
| Appliance disaggregation from aggregate power | `RESEARCH/D.md` | Rejected: information-insufficient | — |
| Automated trustworthy map building | `RESEARCH/D.md` | Rejected: coordination cost dominates | — |
| Capture-and-reproduce-any-computation | `RESEARCH/D.md` | Rejected: ReproZip and reprotest prior art | — |
| Need corpus as a candidate generator, and its reply subtrees as a serving signal | `EXPERIMENTS/012-candidate-harvest/` E012, `EXPERIMENTS/039-need-statement-response/` E039 | **Both generators closed, on measured grounds** (`FAILURES.md` F029, F060): 0 of 50 needs survive the screens, and the corpus's own threads name a tool in **0 of 1391** and record a requester returning in **1 of 794** | **Nothing to build from it.** D068 restates it as a recognition signal. The only route to a measured outcome is a prototype addressed to one named requester, which needs authorization |
| Non-interactive line staging (`stage-lines`, `stg`) | `EXPERIMENTS/037-*`–`048-*`, `EXPERIMENTS/055-index-postcondition/` | **Withdrawn as a candidate, on three independent closes** (F075, F081, F083), and the last named action from it spent (F084, F085, F088). Correctness is not in question: 37/37 tests, index byte-identical to a hand-built patch. **Not released**, `status: draft` | Nothing to build. The population was measured and does not need it. E055's postcondition checker survives as a reusable instrument, not a direction |
| Universal local-first sync layer | `RESEARCH/D.md` | Rejected: invariants not preserved | — |
| Recurring-payment detection on real bank exports | `EXPERIMENTS/065-recurring-expense-detection/` E065, `EXPERIMENTS/066-berka-real-validation/` E066, `EXPERIMENTS/072-merchant-noise-raw/` E072, `EXPERIMENTS/073-piecewise-price/` E073 | **Line closed** (`FAILURES.md` F185, F186): on 36 real exports E065's detector scores recall 0.394 / F1 0.160; the piecewise-constant repair F185 named scores recall 0.455 / F1 0.197 — strictly better on every count but short of both predeclared gates (G1 recall ≥ 0.50, G2 F1 margin ≥ +0.05). Recovers 2 of 14 CV-gate misses. **No usefulness or differentiation claim; the incumbent ships the feature** | Nothing to build. The remaining 12 misses need a richer model (drift, seasonality) or are not recurring; the line is closed on this population |
| Duplicate-closure rate of the score tail, and the worklist over it | `EXPERIMENTS/034-reask-tail/` E034, `EXPERIMENTS/036-search-backlog/` E036 | **The measurement stands and the candidate is prior art** (`FAILURES.md` F057, F059): pooled tail 0.1352 against the `Active` tab's 0.0303, per-tag 0.0000–0.4300, and the ordering plus the label both arrive from one unauthenticated `/search/advanced` query | **Nothing to build.** The one gap F059 names — whether the *rendered* site exposes this against the API — needs a browser or a user, not a request |

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

### The three kill gates and their witnesses

All three moved to [`HYPOTHESES-results-2.md`](HYPOTHESES-results-2.md) on 2026-10-06 at this
file's line cap: each candidate below was measured, each witness was run, and **none
survived**, so the gates and witnesses now belong with the results that closed them rather
than with a live candidate list. The table above keeps the objections and the *reconsider
when* clauses.

## Standing cautions

1. Agreement among the sealed investigations is weak evidence: they share a model,
  so they are procedurally independent and not epistemically independent.
2. Every candidate so far has substantial prior art, and **prior art is the
   plurality of kill reasons rather than the majority: 10 of 18 = 0.556, a
   one-row margin, over a population of 20 rows rather than the twelve this file
   previously carried (F044).** Of the 18, **7 died of something else** — a
   mechanism its own test refuted, or confirmed into uselessness (F001, F006,
   F008, F012); a claim no available observation could establish; or one promoted
   and then parked with no reason recorded. That
   is the base rate for the ideas an agent can generate, it is why the prior-art
   skill exists, and it is why prior-art survival cannot be the selection filter.
   A verdict also needs more than one phrasing on more than one corpus: one
   search query returned 502 irrelevant hits, another returned 0 for an idea with
   29–83 repositories behind it (F030).
3. No candidate has passed the information-sufficiency test yet. Two of the
   rejected proposals in `RESEARCH/D.md` were killed by it in ten lines of code.
4. Nothing here has a user. Every usefulness statement is `inferred` or
   `speculative` until a real person is observed.

## Candidate under consideration: ArXiv computational reproducibility (E067)

### H-01 — ArXiv reproducibility: a tool can generate machine-runnable environment specs from partial information

**Observation:** E067 measured 34 ArXiv computational papers with code links (sampled from 1,682 papers with code links, 10.9% of 15,397 harvested). Only 4/34 (11.8%) had machine-runnable specs (A1), 1/34 (2.9%) partial (A2), 11/34 (32.4%) docs-only (A3), 18/34 (52.9%) no env info (A4). All four kill gates passed: population ≥20 (34), severity A1<0.50 (0.118), differentiation A4>0.10 (0.529), baseline A5≤code-link (0≤0.118). `observed`.

**Mechanism:** A deterministic tool analyzes a paper's GitHub repository (source code, any existing config files, paper metadata like submission date) and generates a complete, pinned environment specification (conda `environment.yml` or `requirements.txt` with all `==` versions) that installs and runs the paper's main computational entry point.

**Assumptions:**
1. Source code imports and runtime behavior reveal sufficient version constraints
2. Paper submission date correlates with compatible package versions
3. Main entry point is identifiable (README, `main.py`, `__main__.py`, or setup.py `entry_points`)
4. A clean virtual environment can test install + smoke test within resource limits
5. The generated spec's correctness is verifiable by execution, not static analysis

**Prior art:** `repo2docker`/`binder` (builds Docker from existing config files, doesn't invent pinned versions), `pipreqs` (infers imports, no version pinning), `conda-lock`/`poetry lock`/`pip-tools` (resolve from existing specs, don't generate from scratch), `reprozip` (captures runtime deps, needs working env first). **Claimed difference:** Generates complete pinned spec from minimal/no starting spec, with install+run verification.

**Strongest objection:** Information insufficiency — two repos with identical `requirements.txt` (`numpy`, `pandas` unpinned) may need different pinned versions (`numpy==1.21.0` vs `numpy>=1.20`). Static analysis cannot distinguish; tool must run trials or abstain. Version search space is large; compute cost may be prohibitive.

**Kill gate:** On a held-out sample of 20 A2+A3 papers (partial/docs-only env info), the tool generates specs that **install successfully** (≥80% install success rate) **and pass a smoke test** (import main module, run `--help` or minimal execution) for **≥30% of papers**. Baseline (`repo2docker` + latest versions) must achieve <15% on same metric. If tool's install+run rate ≤ baseline + 10pp, abandon.

**Baseline:** `repo2docker` (v2024) run on each repo with no version constraints (uses latest compatible), followed by smoke test. Also: manual version selection by author (upper bound, not run here).

**Experiment:** `EXPERIMENTS/079-arxiv-reproducibility/` — harvest 20 new A2+A3 papers (stride sample from E067's population), run tool and baseline, measure install+run success. Reproduction: `cd EXPERIMENTS/079-arxiv-reproducibility && python3 run.py --sample 20 --gate`.

**Result:** `observed` (witness: FAIL as predicted), `untested` (full experiment)

**Uncertainty:** Whether version search via trial installation is feasible within time budget; whether smoke test (import + `--help`) correlates with full computational reproducibility; whether paper date heuristics narrow version space enough.

**Decision:** `hold` — witness passed (demonstrated information-sufficiency bound), full experiment infrastructure ready but not executed due to environment constraints (needs `python3.8-venv`). Tool prototype over-generates packages from import extraction; static analysis alone cannot resolve version ambiguity without trial installs.

**Reconsider when:** A cheaper version-inference method is found that passes the witness, or trial installation infrastructure is available. The witness FAIL is a structural bound, not an implementation defect.