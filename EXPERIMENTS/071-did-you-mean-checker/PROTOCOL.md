<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E071 — did-you-mean-a-different-project checker

Declared 2026-10-09, session `2026-10-09-007`, VM
`instance-20260717-0944`, before any repository was scanned.

## The practical difficulty

A developer names a dependency from memory — `sklearn`, `telegram`,
`beautifulsoup` — and pip installs a *different real project* that happens
to occupy that name. The install succeeds, nothing warns, and the first
signal is a downstream `ImportError` or an unexpected API, possibly minutes
or a CI cycle later. E070 measured that this silent wrong-project class is
real: 3 of 4 declared-B near-misses in arm M, and 3 B rows in 105 generic
rows in arm W, across PyPI and conda (F103, D089).

The population that experiences it: every package-manager user who names
a dependency from memory. The evidence that the mechanism exists is E064's
G5/G6 (0.1615 of near-misses resolve to a real different artifact) and
E070's occurrence measurement. What is untested is whether a *deterministic
checker* can catch the case before the ImportError.

## The claim under test

**E071.** A checker that reads a project's declared dependencies and
actual imports can flag a declared name whose near-miss is the package
actually providing the import — and it can do so with a false-positive
rate low enough to be useful in CI.

The strongest accessible alternative, named in advance: **the status quo**,
which is no checker at all. The developer discovers the wrong project at
ImportError time. A checker that does not fire before the ImportError is
worthless; one that fires on every dependency is noise.

## What "the project actually providing the import" means

A project declares `foo` in `requirements.txt`. The code imports `bar`.
The checker flags `foo` when:

1. `foo` resolves to a real PyPI project (so it is not a typo that pip
   would catch), **and**
2. `bar` is a near-miss of `foo` (prefix, suffix, or synonym mutation per
   E064's families), **and**
3. `bar` resolves to a real PyPI project (so the near-miss is also a real
   project, not a phantom), **and**
4. `bar` is the project that actually provides the import the code uses.

Condition 4 is the load-bearing one. It is what separates "you declared
`sklearn` and you import `sklearn`, but `scikit-learn` is the real package"
from "you declared `requests` and you import `reqests`, which does not
resolve." The checker must determine which package *provides* the module
the code imports, not just whether the name resolves.

**How the checker determines the providing package.** For each import
`bar` in the code, the checker queries PyPI for the package whose
`top_level.txt` or `info.name` matches `bar`. PyPI's JSON API exposes
`info.name` (the canonical package name) and the wheel's `top_level.txt`
lists the top-level modules the package provides. The checker builds an
`import → package` map from PyPI metadata and flags a declared name whose
near-miss is the package that actually provides the import.

This is the mechanism. It is deterministic, model-free, and costs one HTTP
request per candidate package. It is falsified if the `import → package`
map cannot be built from PyPI metadata, or if the map is so noisy that the
false-positive rate exceeds the gate.

## Arms

| arm | source | what it carries |
|---|---|---|
| **A** | 11 repos with requirements.txt in E068's corpus (63 requirements files, 5809 .py files) | the test population; real repositories with real declared deps and real imports |
| **B** | 4 known silent-class near-misses from E070 (`sklearn`→`scikit-learn`, `telegram`→`python-telegram-bot`, `beautifulsoup`→`beautifulsoup4`, `clip`→`openai-clip`) | positive controls; the instrument must fire on these |

**Why these arms.** Arm A is the population sample — real repos with real
deps. Arm B is the instrument-recovery control (the record's rule: an
instrument must recover independent real positive examples, not only
synthetic near-copies). The four B pairs are chosen from E070's arm M and
arm W, not invented here.

## Denominators and honesty rules

- Every fraction is over repositories **successfully scanned** (requirements
  parsed, imports extracted, PyPI metadata fetched). Repositories where any
  of these steps fails are reported as missing observations, never as zeros
  and never as denominators (D082).
- A declared dependency that pip cannot resolve is **not** a false positive;
  it is a typo that the existing guard catches. The checker's population is
  declared deps that resolve.
- The `import → package` map is built from PyPI metadata only. A package
  whose metadata is unavailable is a missing observation, never a match.

## Gates, all declared before any repository was scanned

| gate | condition | if not met |
|---|---|---|
| **G1 population** | arm A yields ≥ 8 repositories with parseable requirements and extractable imports | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 instrument recovery** | the checker fires on ≥ 3 of the 4 arm B positive controls | the instrument cannot recover known silent-class cases; the mechanism is falsified. Stop. |
| **G3 false-positive rate** | among arm A repositories, the checker flags ≤ 20% of declared deps that resolve | the checker is too noisy to be useful in CI. The candidate is killed. |
| **G4 the catch** | among arm A repositories, the checker flags ≥ 1 declared name that is a real silent-class case (verified by reading the PyPI metadata for both the declared name and the near-miss) | the checker fires only on synthetic controls, not on real repositories. The mechanism does not transfer. The candidate is killed. |

**G3 and G4 are the kill gates.** G3 kills the candidate if the false-positive
rate is too high (the checker is noise). G4 kills the candidate if the
checker does not fire on any real repository in arm A (the mechanism does
transfer from synthetic controls to real code). Both must pass for the
candidate to survive.

**Rationale.** A gate whose only passing region consists of vacuous cases
cannot fail — the E069 lesson (D088). G3 has a non-vacuous passing region
(≤ 20% false positives) and a non-vacuous failing region (> 20%). G4 has a
non-vacuous passing region (≥ 1 real catch) and a non-vacuous failing
region (0 real catches). Both regions are enumerated before the run: the
set of declared deps that resolve and the set of imports that map to a
providing package are both determinable from the repository files and PyPI
metadata.

## What changes on the verdict

| verdict | decision |
|---|---|
| G1, G2 met, G3 ≤ 20%, G4 ≥ 1 | candidate survives: a deterministic did-you-mean checker has a population and a usable false-positive rate. A reversible prototype is built and tested against the strongest accessible alternative. |
| G1, G2 met, G3 > 20% | the checker is noise. The mechanism is falsified. The next session starts a fresh observation in a new domain (D083). |
| G1, G2 met, G4 = 0 | the checker fires only on synthetic controls. The mechanism does not transfer. The next session starts a fresh observation in a new domain (D083). |
| G2 not met | the instrument cannot recover known cases. No prevalence claim is made; repair the instrument or abandon the route. |
| G1 not met | the route is not measurable at this cost. Record the ceiling. |

## Ceilings

One VM, one Python 3.8 interpreter, one pip. PyPI JSON API only (no npm,
no conda). The `import → package` package map is built from PyPI metadata
only; it does not handle packages that provide modules under a different
name (e.g., `beautifulsoup4` provides `bs4`). The 4 arm B controls are
chosen, not sampled — they test whether the guard exists, not how often
it is reached. The E068 corpus is deep-learning GitHub code from one
arXiv year; it does not speak to other domains.

## Revision History

- 2026-10-09: Initial creation.
