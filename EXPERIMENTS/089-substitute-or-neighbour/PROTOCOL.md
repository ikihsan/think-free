<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-10
-->

# E089 — PROTOCOL: are E064's 93 "false accepts" substitutes, or distinct projects?

Declared 2026-10-10, session `2026-10-10-005`, VM `instance-20260717-0944`,
**before the descriptions were labelled**.

## The decision this changes

`STATE.md`'s dashboard and F099 quote **0.1615** — "93 of 576 plausible near-miss
package names resolve to a real, different artifact" — as the mission's evidence
that *the existence bit every installer, IDE and checker returns is materially
insufficient*. That sentence is load-bearing: it is why the package-name line is
closed **against** building rather than left open.

E064's own `PROTOCOL.md` is explicit about how the labels were made:

> Ground truth is definitional, so no labeller is involved and no label can be
> argued with: mutate a real package name the way a model does … and the
> *intended* artifact of every mutated name is the original. Any mutation that
> resolves is a **false accept by construction**.

"By construction" is an assumption about human behaviour, made by the mutation
operator, and **nothing measured whether anyone who installs `requests-utils`
means `requests`**. This experiment is the measurement that was skipped, and it
uses bytes E064 already committed and nobody read.

## The question, stated so it can fail

Of the 93 packages E064 counts as false accepts, **how many describe themselves
as the thing the mutated-from package provides** — a reimplementation, a
drop-in replacement, a clone, or an alternative to it?

- If **most** are distinct projects that merely have adjacent names, then
  0.1615 counts name adjacency, not mistaken installs, and the dashboard must
  say so. The package-name line stays closed, now for a measured reason.
- If **most** claim to be the seed, the figure stands and a checker is worth
  building.

## Population and instrument

- **Population:** exactly the 93 rows of
  `EXPERIMENTS/064-remedy-existence/raw/metadata-falseaccepts.json`
  (npm 40, pypi 32, crates 15, gem 6; Packagist contributed 0).
- **Instrument:** the package's **own description**, as E064 already fetched it.
  Primary, human-written, published by the package's author. No classifier, no
  search, no labeller model. Committed bytes, sha256 recorded in `analyze.py`.
- **Control:** the 30 rows of `metadata-real.json` — the intended artifacts
  themselves. The same rule is applied to them unchanged. A rule that calls a
  package's own author a "substitute" is not measuring the phenomenon.

## Labels, defined before any row is read

Each of the 93 rows is labelled **by hand** into exactly one of three classes,
from its description alone. `analyze.py` never classifies; it counts the
committed label file and fails if a row is missing (D061, F049).

| label | definition | would a reader who typed the seed and got this package have been misled? |
|---|---|---|
| `equivalent` | the description claims to **provide the seed's capability under its own name** — reimplementation, drop-in replacement, clone, alternative, or a rewrite of it | **yes** |
| `derivative` | the description says it **builds on, adapts, wraps or extends the seed** for some stated purpose, and is its own thing | no |
| `other` | neither: a separate project with an adjacent name, or **parked** (no description, `Reserved`, `security holding package`) | no |

A parked name is split out in the reporting, not the labelling: it is a *loud*
failure (the install succeeds and imports nothing), not a silent substitution.

## Gates, and what each one's passing value can be made of

Enumerated in advance, per D088/D095. Each is written with a reachable region on
both sides.

- **G1 population** — metadata present for ≥ 80 of 93 rows. Reachable: all 93
  resolve, so 93 is the only likely outcome and 0 is the only failing one.
  Below 80 the experiment reports `not_evaluated`; it does not extrapolate.
- **G2 the rule discriminates** — applied unchanged to the 30 controls, **≤ 4
  are labelled `equivalent`**. Reachable both ways: `hashbrown` ("a Rust port of
  Google's SwissTable hash map") is not equivalent to itself, while a control
  genuinely described as a replacement of another package would be. **If G2
  fails, no correction is made** and the labels are reported as unvalidated.
- **G3 the decision** — the `equivalent` share of the 93, with a Wilson CI95.
  Reported whatever it is. The declared reading: **≥ 0.50** means 0.1615 counts
  adjacency; **< 0.10** means 0.1615 stands as a hazard rate.

There is no kill line on the *build*: E085 (F108) already measured the
real-dependency rate at 0.6% silent and closed the line. What E089 changes is
whether the record's most-quoted number means what the dashboard says it means.

## Falsification of the instrument itself

The rule is one reader, so the load-bearing weakness is a reader who labels to
fit. Three guards, declared in advance:

1. the labels file records the **exact description text** each label rests on,
   so every judgement is auditable against the bytes (D061);
2. `analyze.py` verifies the **sha256** of `metadata-falseaccepts.json` and
   fails on a difference, so the labels cannot be fitted to different bytes;
3. the labels are produced and written **before** `analyze.py` is run, and the
   run's output is a count, not a classification.

## Ceiling

93 rows, 4 ecosystems, and descriptions as fetched on 2026-10-08. It does not
measure installs, intent, or harm; it measures what package authors say their
package is. Packagist is `not_exercised` (E064 resolved 0 of 48 there).