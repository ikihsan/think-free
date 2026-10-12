# E113 AMENDMENT-1 — the first pool was truncated on the outcome variable

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## What happened

The first harvest ran the query as declared in `PROTOCOL.md`
(`language:python stars:100..20000`, `sort=stars&order=desc`, take the first
300) and returned 300 rows spanning **13,422 to 19,962 stars** — the declared
band was 100 to 20,000. The pool is therefore the **top 1.5%** of the band.

## Why this is a defect and not a nuisance

Cumulative stars is the outcome variable of G2. Harvesting by sorting on it and
keeping the top N **conditions on the outcome**: the arms can only differ within
a range of roughly 6,500 stars, so a real effect is mechanically suppressed and
an apparent null is uninterpretable. It is the same error as E107's, one level
up: there, the arms were selected on topic; here, the pool was selected on the
metric being tested.

This is recorded rather than quietly corrected because the declared query is
what produced the artifact, and a reader comparing this protocol to its result
must be able to see the first design and why it was withdrawn.

## Repair

Replace the single descending page-walk with a **stratified sample across the
whole declared star band**: seven disjoint sub-bands, one page of up to 100 rows
from each, `sort=stars&order=desc` *within* a sub-band. Coverage is imposed by
stratum, not by the outcome; no sub-band is truncated relative to its
neighbours in a way that correlates with the need/generic label, because the
label is assigned after harvest and is independent of star count by construction
(it reads description text).

Sub-bands: 100–200, 200–500, 500–1000, 1000–2000, 2000–5000, 5000–10000,
10000–20000.

## Consequence for the gates

Unchanged. The sub-band is recorded on every row (`harvest_stratum`) so the
analysis can stratify and report whether the label distribution differs across
strata — if `utils`-ish text were concentrated in low-star strata, the label
would be partly a proxy for the stratum, and that must be visible rather than
hidden in a pooled average.

G1 stays at ≥100 per arm; with a stratified pool of ~700 rows and the E107 label
rates (77/80 need-side yield, 73/80 generic-side) both arms should clear it. If
it does not, the honest reading is `inconclusive`, as declared.