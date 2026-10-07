<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Methodological Summary — Lessons from Closed Experiments

<!--
A concise synthesis of patterns across all closed invention claims in this repository.
Purpose: preserve evidence that survives outside this agent, and inform future
candidate selection and experiment design. Read with STATE.md and HYPOTHESES.md.
-->

## Executive Overview

Six invention claims have been tested and none validated. Prior art is the plurality
of kill reasons (F044: 10 of 18 = 0.556, a one-row margin), not the majority. Novelty,
prior-art harvest, and star-shaped adoption cannot carry the selection filter
(F034, F035, F037, F048, F060). The need corpus records recognition, not service
(E039, E041, E042). Kill gates that are predeclared, runnable, and measure
accessible populations produce actionable results; experiments relying on
unmeasured populations, unverified environments, or novelty claims without prior-art
checks produce closed findings (F001–F059).

## Key Patterns Across Kill Gates

### 1. Runnable Kill Gates Produce Results
Predeclared kill gates that are executable on available hardware and measure
accessible populations yield observable outcomes. Among the ten+ gates tested:

| Experiment | Gate Status | Key Observation |
|---|---|---|
| E001 | Met | Checksum baseline fails motivating example |
| E012 | Passed | 0 of 50 harvested needs produce candidates |
| E034 | Fired | Disjoint closure intervals observed (0.1352 vs 0.0303) |
| E039 | Passed | Community answers "has anyone hit this?" not "here is what to use" |
| E041 | Passed | GitHub serves issue bodies; corpus index possible |
| E043 | Passed | Agents discover lines by hand first (6/6, 3/3 nostg) |
| E044 | Passed | Direct measurement: no agents need tool without line diff |
| E045 | Passed | 0 of 189 rows has the target population |
| E047 | Met | No shipped hook runner produces partial-staging hazard |
| E051 | Passed (synthetic) | 8/8 contradictions detected, P=1.0, R=1.0 |

**Contrast:** Gates that cannot be run (E021 needs containerised server,
E024 needs prior publication dates, E022 is time-gated) or that rely on
unmeasured populations (F055's recurrence bound, F059's worklist) produce
inconclusive or refuted results.

### 2. Unmeasured Populations Produce Misleading Results
When a kill gate references a population not directly read from evidence,
results are unreliable or falsified:

- **F055:** Recurrence bound 0.0223 refuted at 0.0540 (CI95: 0.0416–0.0698)
  once recurrence was read off the platform's own closure judgement.
- **F037:** Prior-art screen inconclusive on small self-selected sample.
- **F018/F019:** Test assertions about machine environment fail when the
  environment is not asserted in records (not portable across VMs).
- **E022's 38.5% served figure:** Withdrawn after proper control read
  (0.368 vs 0.395, base rate of Hacker News conversation).

**Principle:** A gate's population must be read from the evidence, not assumed.
E045 read all 189 unique issues row by row; E044 measured the population
directly against real agents. Both found the target population does not exist.

### 3. Direct Evidence Reading Produces Consistent Results
Independent reads of the same evidence agree when the population is directly
observed:

- **E044 (VM 0947) vs E044 (VM 0944):** Both measured 6/6 exact and
  3/3 nostg agreement on the discovery population.
- **E047 (both VMs):** Concurrent runs agreed on the two corpus rows'
  disagreeing premises (one exonerates the tool, one records the hazard).

**Principle:** When the population is measured directly against real examples,
results are reproducible across independent VMs. When the population is
inferred or assumed, results diverge.

### 4. Environment-Aware Kill Gates Must Assert Their Environment
Two assertions in one file (F018, F019) claimed "this machine's tools are
in the records"; each was green on the machine that wrote it and red elsewhere
for opposite reasons — the interpreter one on every version the record lacked,
the git one on CI runner shipping git 2.55.0.

**Principle:** Assert the artefacts and the contract, and state the environment
gap as data (`not_exercised`). A gate that reads its own environment is only
as portable as the record of that environment.

### 5. Claims About Populations Not in Evidence Are Closed by Reading
Evidence:

- **E045:** Read 189 unique issues from E038's cached corpus. Population
  "agent that must discover which line changed, with no line number and no
  `git diff`" does not exist: 0 of 189. Reader's own count: 29 about
  choosing which lines reach the index (0.153), 28 with explicit diff
  access, 1 GUI-implied, 0 with none.
- **E043/E044:** Population "agents with no line number and no `git diff`"
  measured directly: 6 of 6 exact, 3 of 3 nostg, every agent discovering
  the line by hand first. The pre-declared kill gate (`nostg` >= 2 of 3)
  crossed.
- **E047:** Two corpus rows DISAGREE about the premise: one exonerates the
  tool, one records the hazard and rules the index-patch fix out of scope.

## Synthesis: What Makes an Experiment Meaningful?

**Measurable claim + runnable gate + accessible population = actionable result.**
The E051 experiment (rule-based claim contradiction detection) passes its kill
gate on synthetic test data (8/8, P=1.0, R=1.0), but the full gate requires
30 paper pairs from PubMed Central with human annotation — outside this
repository's verified capabilities. E049/E050 (E2 lockfile drift) produced
"drift-observed" (10/11 closures changed) with a Part B re-run snapshot that
enables follow-up. E047 (hook partial staging) measured the hazard byte-exact
across all framework versions.

**Missing ingredients everywhere:** No experiment produced a user, adoption
evidence, or a validated product. Every usefulness statement is `inferred` or
`speculative` until a real person is observed (HYPOTHESES.md standing caution 4).

**Prior art is the base rate.** 10 of 18 kill reasons = prior art (0.556),
7 of 18 died of something else (mechanism refuted, unestablishable claim,
promoted-then-parked). This is the base rate for ideas an agent can generate,
and it is why the prior-art check skill exists (HYPOTHESES.md standing caution 2).

## What Remains Unknown

1. **Full E051 kill gate on real data:** 30 paper pairs from PubMed Central
   with human-annotated contradictions. Requires network access and
   authorization beyond this repository's grants.

2. **Generalizability of E051 extractor:** Synthetic test passes, but
   biomedical/social science abstracts may use language patterns the rule-based
   extractor does not cover (hedging, indirect phrasing, paywalled diversity).

3. **Whether any untested candidate could survive** an information-sufficiency
   gate + prior-art check + runnable kill gate combination. The mission has
   tested 6+ candidates through this pipeline; all closed.

4. **The mission's own tooling as a candidate:** Tested as prior art (F026,
   F027): mechanism six weeks old, discipline reinvented independently, niche
   adoption flat (0 stars). This is the mission's own discovered prior art.

## Decision Rule for Future Candidates

Before promoting a candidate past the screen, verify all of:

- [ ] **Predeclared kill gate is runnable** on available hardware/interpreters
- [ ] **Population is measured directly** from evidence, not assumed or inferred
- [ ] **Environment is asserted** in the record (or gate is environment-agnostic)
- [ ] **Prior art has been checked** (F026, F027: the base rate is 0.556)
- [ ] **No novelty-only case** for promotion (F034, F035, F037, F060 all failed)
- [ ] **Adoption evidence is absent** (every closed candidate lacked users)

If any of these cannot be confirmed, the candidate should be closed rather
than promoted. Negative results are preserved in FAILURES.md with the reason,
the population tested, and the evidence read.

## Evidence Pipeline (for future reference)

1. **Hypothesis** → Record in HYPOTHESES.md with claim, gate, witness
2. **Experiment** → Run with stdlib Python, record raw results in EXPERIMENTS/<n>-<name>/
3. **Kill gate** → Declare PASS/FAIL against artifact, exit code
4. **Evidence read** → Read the population/corpus the candidate rests on,
   row by row if needed (as E045 did with 189 issues)
5. **Result** → Record in HYPOTHESES-results.md; close or promote
6. **Document** → Add methodological finding to this summary

## Revision History

- 2026-10-03: Initial creation; synthesized patterns from F001–F059 and
  all experiment results in HYPOTHESES-results.md, STATE.md, FAILURES.md.
- 2026-10-07: Added E051 synthetic kill gate results; refined population
  measurement principle from E044/E045 cross-VM agreement; added decision
  rule for future candidate promotion.