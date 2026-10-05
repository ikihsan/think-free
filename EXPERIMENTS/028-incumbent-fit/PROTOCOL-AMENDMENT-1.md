<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E028 — protocol amendment 1

Written 2026-10-05 **after** reading the two captures' structure and after one
feasibility probe of `raw.githubusercontent.com` (200 for three repositories),
and **before any fit label, before any reader, and before any reader saw an
artifact's documentation**. The base protocol's question, population rule, gates
and decision map are unchanged. This amendment fixes three things the base
protocol left undefined, which were found undefined while making the
instrument runnable:

## 1. Labelling is per row, with bundle semantics — not per pairing

The base protocol named a "pairing" and a four-category fit label but never said
how six labels over six artifacts become one verdict about a row. Deciding it
now, because it changes what the number means:

**A row is labelled once.** The reader receives the requirement text, the Step A
attribute, and a **bundle**: each named artifact with the head of its own
published documentation. The label is `serves` if **any** artifact in the bundle
does what the attribute asks, `partial` if an artifact does part of it,
`does_not_serve` if no artifact in the bundle does it, and `unreadable` if no
artifact's documentation was fetchable.

Any-artifact semantics is the rule a prior-art screen actually uses — the
verdict is *"a tool already serves this"* — so the aggregation is the one the
recorded verdict should have used and did not state.

**Why this is cheaper and sounder, not merely cheaper.** Per-pairing labels
multiply the reader's work by the artifact count and invite the reader to
reconcile six judgments into one. The decisive quantity in this mission's record
is the row-level verdict, because that is what a kill is.

## 2. The fit population is the pairings whose documentation is stored as text

Fetching is attempted for **every** named artifact, by corpus:

| corpus | source attempted | on failure |
|---|---|---|
| `github` | `raw.githubusercontent.com/<repo>/HEAD/README.md`, then `master`, then `main`, then `README.rst`, `README.txt` | recorded `unfetchable`, not silently dropped |
| `registries` | the package's own homepage `repository` link, then the registry page | recorded `unfetchable` |
| `openweb` | the recorded URL itself | recorded `unfetchable` |

An artifact whose documentation could not be stored is **not evidence either
way**, so a bundle with no stored text is `unreadable` and never
`does_not_serve`. The per-artifact fetch status is published in `results.json`
for every artifact in the population, including those no reader saw.

**Documentation is stored at 12,000 characters of the artifact's own text**, head
first. A capability claim in a README is at the top; this cap is a cost decision
and is recorded as a ceiling, not as a finding.

## 3. The lexical index is per pairing, the human label is per row — and they are not conflated

The base protocol declared a lexical attribute-match index and a reader label in
the same list of steps, which invited reading one as the other. They are
different measurements and are reported in different fields:

- **lexical**: one number per (requirement, artifact) pair, over every pair in
  the population including the controls. Its base rate is measured on the
  mismatched pairs (C1) and printed beside it, every time it is quoted.
- **reader**: one label per row, over the stored bundle.

A lexical index that cannot separate matched from mismatched pairs is reported
as uninformative and is **not** used to support any gate. The gates in the base
protocol are read off the reader labels alone.

## 4. The mismatched control is one foreign bundle per fit row

Declared before the first label, so the threshold in the base protocol (A1, C1:
both readers label ≥ 90% of mismatched pairings `does_not_serve`) has a
denominator. The pairing rule is fixed and mechanical: **row *i* is paired with
the bundle of row *(i + 1) mod n***, so every fit row contributes exactly one
control and no artifact is ever paired with its own requirement. The control
denominator is therefore the fit population, not a sample of it.

## What this amendment does not do

It does not change the population (29 prior-art deaths), the gates (A1, A2, A3,
B1, A4), the falsifications, or the decision map. It does not add a gate. The
`not_evaluated` state declared as A4 covers the case where the fit population
falls below ten rows once `unreadable` rows are removed — which is a real
possibility, because three of the 19 harvest rows name no artifact at all and
were already `no_prior_art_found` in E016.