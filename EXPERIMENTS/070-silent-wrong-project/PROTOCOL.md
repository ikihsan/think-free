<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E070 — does the silent wrong-project install occur among real users?

Declared 2026-10-09, session `2026-10-09-004`, VM
`instance-20260717-0947`, before any arm ran.

## The question

E064 measured, on definitional ground truth (576 mutations of
37 real names, 5 ecosystems), that **0.1615 of plausible
near-miss package names resolve to a real, different
artifact** — and that 24 of those 93 false accepts carry
healthy metadata (popular, maintained projects such as
`jinja2-cli`, `django-click`, the `sklearn` placeholder).
Installers' own guards — pip's "did you mean", npm's typo
protection — key on names that **do not resolve**. So the
silent class — *the install succeeds, the project is wrong,
and nothing warns* — is exactly the population those guards
cannot see, and E064's G6 showed a metadata rule cannot
separate the classes (recall 0.742; the misses are healthy).

`STATE.md`'s open question, verbatim: *"the installers' own
guards key on names that do not resolve ... so the 24
healthy-metadata false accepts are exactly the population
those guards cannot see. Whether that gap is observed
anywhere, and whether a 'did you mean a different project'
warning has a population that wants it, is untested."*

**Two sub-questions:**

- **Q1 (mechanism).** When a user installs a silent-class
  near-miss on a default setup, does any guard fire? E064's
  premise says no; this arm states it as a prediction and
  runs it on bytes.
- **Q2 (occurrence).** Among real reports of package-name
  confusion, what share is the silent class?

**Practical difficulty, and who experiences it:** a developer
names a dependency from memory, receives a *different real
project*, the install succeeds, and the first signal is a
downstream `ImportError` or an unexpected API — possibly
minutes, or a CI cycle, later. Every package-manager user is
the population. The evidence that the mechanism exists is
E064's G5/G6. What is untested is whether it *reaches*
anyone.

## Arm M — the mechanism, on bytes

Four known silent-class near-misses and one guard-caught
control, each installed in a **fresh** virtualenv with
pip's defaults, recording stdout+stderr verbatim and the
exit code:

| name | class | why |
|---|---|---|
| `sklearn` | B (silent) | PyPI placeholder, "deprecated ... use scikit-learn instead"; a different artifact than the one intended |
| `telegram` | B (silent) | an abandoned 0.0.1 project, not `python-telegram-bot` |
| `beautifulsoup` | B (silent) | Beautiful Soup **3**, not `beautifulsoup4` |
| `color` | B (silent) | a different colorize library, not `colour` |
| `reqests` | A (guard-caught) | does not resolve; the class pip's own guard is built for |

Prediction under E064's premise: the four B installs print
**nothing** that names the intended project, and the A
install does. The arm is falsified if any B install prints a
warning that identifies the intended project.

## Arm W — occurrence, sampled

**Venues:** the Stack Exchange API (`stackoverflow`,
unauthenticated) and the GitHub issue-search API
(unauthenticated, 10 req/min). Both are read-only; no
external message is sent.

**Query classes, fixed before fetching:**

- **PC — positive controls** (4 queries, one per B pair
  above, e.g. `sklearn scikit-learn`). The instrument
  **must** recover B rows here; this is the
  instrument-recovery control (the record's rule: an
  instrument must recover independent real positive
  examples, not only synthetic near-copies).
- **G — generic** (6 queries about install-then-confusion,
  e.g. `pip install succeeded but import failed`,
  `installed wrong package`, `pip install wrong package`,
  `pip install typo`, `different pypi package than
  intended`, `pip install similar name`). The population
  sample; no query names a specific pair, so a B row here
  is found, not planted.
- **PL — placebo** (2 queries with no plausible near-miss
  confusion). Expect ~0 B rows.

**Sampling:** up to 25 items per query, deduplicated by
`question_id`/`issue id`; every returned row is classified,
no row is dropped for being uninteresting. Target ≥ 100 G
rows.

**Classification, one label per row, fixed before reading:**

| label | meaning |
|---|---|
| **A** | the name the user typed **does not resolve**; the installer refused (often with a suggestion) |
| **B** | the name typed **resolves to a different real project** than intended; the install **succeeded**; the report shows the confusion (import failure, unexpected API, wrong behavior) |
| **C** | both names are the **same project** (rename/alias) |
| **D** | correct distribution, but its **top-level module** differs from the distribution name (`beautifulsoup4`→`bs4`); user error, same project |
| **E** | not a package-name-confusion report |

The typed name's existence is checked against the registry
with E064's own `registry.py` (reused, stdlib), not by
eye. A row is B only if the registry confirms the typed name
exists **and** the report names a different intended project.

**Second reader:** a 20% sample is re-coded independently
(inter-rater κ; the record's convention is E023's κ = 0.923,
gate here ≥ 0.75).

## Gates (pre-declared)

- **K1 — instrument recovery.** ≥ 3 of the 4 PC queries
  yield ≥ 1 B row **and** κ ≥ 0.75. If not met, the verdict
  is `instrument_failed`: the pipeline cannot recover known
  silent-class reports, so it cannot certify anything about
  prevalence, and no prevalence claim is made.
- **K2 — occurrence.** The B share among G rows.
  - **B ≥ 0.10** → the silent class recurs in real reports:
    a deterministic "did you mean a different project" check
    has a population, and a reversible prototype is
    authorized (tested against the strongest accessible
    alternative on E068's on-disk corpus of real
    repositories).
  - **B < 0.05 with A the plurality** → the observed
    confusion population is dominated by the class the
    guards already catch; the E064 thread closes (F103) and
    the next session starts a fresh observation in a new
    domain (D083).
  - **0.05 ≤ B < 0.10** → inconclusive; narrow the
    population (one venue, one query family) rather than
    building.

**Denominators are reports, not installs.** This measures
whether the failure is *observed at all*, never its
incidence rate — the record's standing rule (F096/F098)
against reading a statement count as a service level.

## What changes on the verdict

| verdict | decision |
|---|---|
| K1 met, K2 ≥ 0.10 | prototype authorized: a checker that reads a project's declared dependencies and actual imports and flags a declared name whose near-miss is the project actually providing the import |
| K1 met, K2 < 0.05 | close the thread (F103); the guards plus self-diagnosis cover the observed population |
| K1 not met | instrument failed; no prevalence claim; repair the instrument or abandon the route |

## Ceilings

One host, one installer (pip; npm is absent on this VM),
English-language Stack Overflow and GitHub only, search
ranking is relevance-based and not exhaustive, and a
self-selected reporter population. The mechanism arm's four
B cases are chosen, not sampled — it tests whether the
guard exists, not how often it is reached.
