<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-15
-->

# E142 — the incumbent probe for CI-failure diagnosis (E140's G5, and the baseline E140 omits)

Session `2026-10-15-002`, VM `instance-20260717-0947`, declared 2026-10-15,
**before any search or fetch in this experiment.**

## Why this exists

`STATE.md`'s named next action is E140, the only live fresh-observation
protocol (CI/CD pipeline failures), declared 2026-10-14, never run. E140 plans
~7,500 GitHub API requests and hours of harvesting to answer G1–G4. Its G5 —
"no existing free tool automatically diagnoses and fixes ≥50% of the top 10
patterns" — can kill the direction for the cost of a survey. Running the
cheapest gate first is the falsification discipline E140 itself demands
(AGENTS.md: "design the falsification before the implementation"), and it
answers the gate most likely to decide.

## Two defects in E140's G5, found by reading it, fixed here before measuring

**Defect 1 — the baseline omits the strongest known alternative.** G5 surveys
*free CI/CD diagnostic tools* (`act`, `dagger`, local CI runners, GitHub's own
annotations). It does not include the alternative this mission has already
measured twice: **a free general assistant with the log in front of it**. E091
measured 5/20 = 0.2500 on one venue; E092 measured **30/37 = 0.8108**, Wilson
CI95 [0.6580, 0.9052], on another, and D104 recorded it as the reason the
diagnosis line closed. CI-failure logs are diagnosis-shaped text with a known
fix; that is the exact class the assistant was measured serving. A gate that
compares a proposed tool only against *other tools* is not the gate that decides
adoption. Arm B exists to put that baseline back.

**Defect 2 — "top 10 patterns" is undefined until the harvest runs.** G5 is
stated over the top 10 of a population nobody has sampled. This probe therefore
tests G5 over a **superset**: the 14 catalog categories in
[`../140-github-actions-ci-failures/ERROR_CATALOG.md`](../140-github-actions-ci-failures/ERROR_CATALOG.md)
and [`ERROR_CATALOG-2.md`](../140-github-actions-ci-failures/ERROR_CATALOG-2.md).
Any top 10 a harvest produces is a subset of those 14, so a kill at the
superset level kills the direction without harvesting; a pass at the superset
level does **not** clear the gate and still requires the harvest. The asymmetry
is deliberate: the probe is cheap and biased toward not killing prematurely.

## Pre-declared structural prediction (falsifiable, and the real prize)

The 14 categories split by **who owns the failure**:

- **Pipeline-configuration categories** (3 permission/auth, 4 timeout,
  5 resource exhaustion, 6 workflow syntax, 7 missing secret, 8 cache/artifact,
  10 network, 11 container, 12 deploy/release) — 9 of 14: the failure is in
  the *workflow file or runner setup*. A tool can read the YAML and propose a
  change to it.
- **Project-code categories** (1 dependency resolution, 2 test failure,
  9 build/compile, 13 lint, 14 flaky/intermittent) — 5 of 14: the pipeline
  **worked correctly** and reported a real defect in the user's own code or a
  runtime property of it. There is no tool-shaped opportunity, because the fix
  is in the repository's source and requires knowing the intent.

> **Correction 2026-10-15, before any search or fetch in this experiment.** The
> split above was first written listing 8 + 4 categories: it silently dropped
> **6 (Configuration / Syntax Error)** and **14 (Flaky / Intermittent Failure)**
> from both halves while still asserting a "14-category superset" elsewhere in
> this file. Reading `../140-github-actions-ci-failures/ERROR_CATALOG.md` and
> `ERROR_CATALOG-2.md` — the two source catalogs, all 14 definitions read — puts
> 6 in the configuration half (an invalid workflow file is a workflow-file
> defect) and 14 in the project-code half (SIGSEGV and a bare `Killed` are
> runtime properties of the project's code, not of the YAML). Corrected totals:
> 9 configuration, 5 project-code. The correction is recorded here rather than
> in RESULT.md because it was made before measurement, which is the only moment
> it is not a self-serving edit.

**Prediction P1:** the tool-shaped surface is confined to the configuration
half, and the frequency distribution is dominated by the project-code half —
where no dedicated tool can help beyond what a general assistant with repo
access already does.

**If P1 holds, E140 is killed by G2** (top-10 error patterns cover ≥30% of
cases) or by the corrected G5-alt, and no harvest is needed. P1 is what makes
this session worth running; the tool survey alone would be an audit.

**Second prediction P2:** for the configuration categories, GitHub's own failure
annotations plus a free general assistant already close most of the gap, because
the fix for "missing secret", "job timed out", "OOMKilled", "403 on
`GITHUB_TOKEN`" is a one-line YAML change that the message itself states.

## Gates

| Gate | Threshold | Arm | Measurement |
|---|---|---|---|
| **G5-tool** | ≥7 of 14 categories (≥50%) already FIXED automatically by a free, existing, named tool | A | cited tool + URL + quoted claim per category |
| **G5-alt** | a free general assistant with the log reaches ≥0.80 on a real-row task | B | deferred to Stage 2; Stage 1 uses standing evidence only |
| **P1** | project-code categories dominate the observed frequency distribution | A + harvest | deferred to Stage 2 |

**Kill conditions, declared now:**

- G5-tool fails (≥7/14 covered) → **KILL** E140's direction. Decided this
  session, with no harvest.
- G5-tool passes but P1's structural read is not supported by anything I can
  source → **do not harvest**; return to fresh exploration.
- Either way, a kill here closes only CI/CD failure diagnosis. It does not close
  the CI domain, the LLM-eval line, or any other route.

## Arm A — classification rule (strict, biased against a kill)

A free existing tool counts for a category only if **both** are satisfied and
cited:

1. **Automatic diagnosis**: given the failing run, it names the cause without a
   human having authored the cause. A tool that prints an exit code, or that
   reports "step failed", is **not** a diagnosis.
2. **Automatic fix**: it produces an applicable change to the workflow YAML or
   repo config, without a human having authored that change. "Reproduces the
   failure locally so you can fix it" is **not** a fix. "Explains what to
   change" is **not** a fix.

The rule is deliberately strict, so a count of zero is a statement about this
definition and not about the market. Where the strict rule and the practical
alternative diverge, the divergence is recorded as `CLOSES_WITH_ASSISTANT`.

### Counting rule, declared before measuring

Two counts are kept side by side and both are reported; the gate fires on the
**strict** one, so a `claimed` capability cannot buy a kill:

- **G5-tool-strict** counts a category only where a fetched source shows the
  tool **actually producing the fix** — an applied change, a rewritten file, a
  merged/auto-merged PR, an automatic reconfiguration — on that category.
- **G5-tool-claimed** counts a category where a fetched source asserts the
  capability without showing it applied.

Kill requires `G5-tool-strict >= 7 of 14`. `G5-tool-claimed >= 7` is reported as
a *weaker* kill of E140's original gate phrasing (which says "automatically
diagnoses and fixes", i.e. asserted capability) and is discussed, not used
unilaterally.

## Controls

- **C1 source discipline**: every incumbent counted must be a fetched page, with
  URL, retrieval date (2026-10-15) and a quoted claim. Recalled knowledge is
  recorded as `recall-only` and never counts toward a gate.
- **C2 independence**: a tool's own README marketing its capability is
  `source-supported`, not `observed`. Any claim of "fixes X automatically"
  backed only by the vendor's page is downgraded to `claimed`.
- **C3 negative direction**: the probe must also look for evidence *against*
  P1 — a free tool that does automatically fix a configuration category. One
  credible counterexample is reported as prominently as seven confirmations.
- **C4 no laundering**: a GitHub Action that wraps an LLM and a tool that wraps
  the same LLM are **one** incumbent, not two.

## What Stage 1 cannot show (declared in advance)

- Anything about the population's size, diversity, or error concentration
  (E140's G1–G4). Those need the harvest.
- Anything about adoption, willingness to pay, or whether a fix would be correct.
- A G5-tool pass is **not** a pass for G5; only the harvest's own top 10 can
  produce that.

## Continuation

Stage 2 (`ARM-B.md`) is written only if Stage 1 does not kill. It must declare
the row sample, the assistant, the gold standard, and the row-level agreement
rule before any row is fetched, mirroring E141.