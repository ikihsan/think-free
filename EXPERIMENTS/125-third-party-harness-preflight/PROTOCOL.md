<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E125 — can a third party point `preflight` at their own harness?

Pre-declared 2026-10-13, **before any third-party repository was fetched and
before one `preflight` input was built from outside this repository**. Commit
order is the evidence: this file precedes `run.py` and the first clone.

## Why this experiment and not another

E124's `PROTOCOL.md` ends by naming what no gate of that run could establish:

> The candidate case is: prior art does not already do this in one command
> (PRIOR-ART.md), and someone other than this repository could point it at their
> own harness. Both are recorded here as requirements, and neither is
> established by a passing gate.

K1–K4 say the tool works on five cases from one repository. The remaining
requirement is a build decision — **release it, keep it internal, or withdraw
it** — and this run exists only to inform that one decision. It measures
third-party code, not this repository's instruments, and it is not an audit of
a discovery method.

## The two questions, with scope

**Q1 (usability).** Given a third-party harness's own committed files, can
`preflight.concordance` be handed a key row set and an output row set
**without harness-specific code**, where the only free operations are: read a
JSON array, read JSON-Lines, or read a CSV with a header row, of flat records?

**Q2 (existence).** Does the defect C1 detects — a join between a scoring key
and a set of scored outputs that matches nothing, raising nothing — occur in a
third-party harness at all?

**Declared ceiling, to be read with every number below.** The population is the
most-starred harnesses reachable by three declared search queries. Those are the
best-tested and best-maintained in the population, so **every incidence figure
in this run is a lower bound on prevalence among harnesses generally** and must
be quoted as one.

## The population — declared before it is drawn

One pass. No redraw, no cherry-picking, no addition after a verdict is known.

1. GitHub repository search, `sort=stars&order=desc&per_page=40`, for exactly
   three queries: `llm eval framework`, `llm evaluation harness`,
   `agent evaluation framework`.
2. Union by `full_name`; deduplicate.
3. Keep repositories with **≥ 300 stars** — a declared floor: a repository below
   it is not one a third party is plausibly holding a harness for.
4. Keep repositories passing the screen below.
5. Take the **30 highest-starred** survivors, in one pass. That is the
   inspection set.

A repository that cannot be read is recorded `unreadable` with its reason and
is **never counted as clean** (F016, F036).

### The screen, and its measured coverage

A repository passes if its GitHub description **or** its README (fetched from
`raw.githubusercontent.com`) contains, case-insensitively, at least one scoring
verb — `score`, `scoring`, `grade`, `grading`, `metric`, `judge` — **and** at
least one evaluation noun — `eval`, `evaluation`, `benchmark`, `test suite`.

Screen coverage — the fraction of the pool where the screen could decide at all
— is reported as a number, and is the first term of G1. A repository the screen
cannot decide is `unclassified`, never `clean`.

## What is measured, per repository

| id | measurement |
|---|---|
| **M1** | **adapter tax** — lines of harness-specific Python written to turn two committed files into `key_rows, out_rows`. Generic loading is free; nested reshaping, custom serialisation and schema mapping are counted. Every such line goes into a committed ledger; the ledger is the evidence and the figure is recomputable from it. |
| **M2** | **join kind**, read from the harness's own scorer: `field` if it indexes a lookup by a value carried in each record; `position` if it joins by row order or enumeration. This is the information-sufficiency attribute — see the witness below. |
| **M3** | **C1's verdict** on the harness's own committed pair, `preflight.concordance` run unmodified. |
| **M4** | **pair qualification** — a pair counts as one run only when the two files carry a shared identifier or shared run label and the row counts are within an order of magnitude. An unqualified pair is `not_qualified`, never `clean`. |
| **M5** | **the baseline** — the strongest accessible alternative is the harness's own test suite for its scorer, read statically: does a committed test exercise the scorer's join on a fixture with ≥ 2 distinct values in the joined field and an expectation that is not the degenerate default? Recorded `protected` / `unprotected` / `no_test`. |
| **M6** | **the comparison that decides the build question** — rows where C1 fires **and** the harness's own tests do not protect the join. Rows where the baseline protects the join are rows preflight adds nothing to, and are reported with equal prominence. |

### The information-sufficiency witness, before measurement

Two realities produce identical inputs to C1:

- a harness whose scorer joins by **position**, shipping a key and outputs whose
  identifiers are unrelated names — the join works perfectly;
- a harness whose scorer joins by **field**, where the two files name the same
  entities in different types — the join matches nothing.

The files can be byte-identical between the two worlds. C1 cannot tell them
apart, so **no C1 verdict may be reported without M2 beside it.** The witness is
ten lines of construction and is committed as `witness.py` with its output.

## Gates

| gate | declared | meaning |
|---|---|---|
| **G1 coverage** | ≥ 20 repositories inspected, ≥ 10 with a qualified committed key/output pair, and screen coverage ≥ 0.90 | the study measured harnesses, not my inability to find files |
| **G2 tax** | zero-adapter fraction ≥ **0.30** over the qualified set | a third party can point it at their own harness often enough to be worth releasing |
| **G3 existence** | ≥ 1 qualified pair with C1 `SILENT_NO_MATCH` **and** `join_kind: field` | the defect C1 catches occurs outside this repository |
| **G4 precision** | of the rows C1 flags, the fraction whose join kind is `field` ≥ **0.50** | C1 does not fire mostly on positional joins, so the refusal is informative |
| **G5 baseline** | ≥ 1 row in M6 | preflight adds something the harness's own tests do not |

**Kill gate.** G2 < 0.30 → the shipped form is not pointable by a third party;
`preflight` stays an internal instrument and the record says so in those words.
G1 not met → the verdict is `not_evaluated` and no claim is made from it. G3 = 0
with G1 met → the external premise is **not observed**; the defect remains a fact
about this repository and the candidate case is withdrawn on its merits, not on
effort. G4 < 0.50 → C1 fires mostly on positional joins; it is usable only with
M2 beside it, which is a different tool with a different interface.

These thresholds are declared here and are **not** moved after the run. A gate
written after seeing results is a rationalisation.

## Negative controls that must pass

1. **Sound pair.** On E116's repaired key (`EXPERIMENTS/116-berka-service-test/`)
   C1 stays `OK` — E124's case B, re-run here unmodified.
2. **Positional control.** A two-file pair with disjoint identifier names and a
   working positional join must be reported `unqualified`, never clean. If the
   pipeline reports it `OK`, M4 is broken.
3. **Pool reproducibility.** The queries, the star floor and the screen are
   fixed, and the pool is committed as data. Not drawn twice — that would be a
   second population, not a check.

## Ceilings declared now

- Prevalence among harnesses below 300 stars is not measured; see the ceiling
  above.
- M3 reads committed files. It does not show that anyone's *reported rate* is
  wrong in production.
- M5 is a static reading of a test file, not a test execution.
- G3 and G4 are counts over a small qualified set. A 0 of 6 is not a bound on
  the population and will not be reported as one.

## The build decision this run changes

Stated before the run so it cannot be written to fit: **release `preflight` as
a pointable tool, keep it internal, or withdraw it.** G2 and G4 decide release
against internal; G3 = 0 withdraws the candidate case on its merits. Nothing else
moves that decision, and no gate above was chosen because it would make some
particular result look decisive.