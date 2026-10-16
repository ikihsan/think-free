<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E170 PROTOCOL AMENDMENT 1 — the control was a bad query, not a bad index

**Declared 2026-10-16, after the arms ran and before G0r was executed.** No arm
query is changed by this amendment; the arm queries were committed in
`queries.json` before any fetch and are read-only from here.

## What happened

`PROTOCOL.md` declared the positive control as "the first verbatim 3-word run of
≥ 8 characters from the target document's own body". The implementation took the
first three **non-function** tokens of the body, which is the same idea and a
worse query: a technical issue opens with prose, so the phrase was generic.

| | |
|---|---|
| G0 as declared | **0 of 13** targets in the top 10 — **kill fired, arms void** |
| median `total_count` of the control query | **718 258** documents |
| minimum `total_count` | 190 |
| G5 placebo | 0 of 13, **passes** — grading is not trivially satisfiable |
| V1, V2, V3 | all pass — the index semantics are as probed |

A phrase that matches a quarter of a million documents cannot rank one of them
first, so G0 as declared measures the phrase, not the index.

## Why this is a repair and not a weakened check

E169 ran the same class of control on the same index and **passed it**: feeding
each target its own title returned the target at rank 1 on **13 of 13** after
the query was rewritten (F130). Ranking works on this index; the failure above
was in the query's selectivity. The repair therefore does not relax the bar — it
replaces an unselective query with a strictly more selective one, and the bar
stays where the protocol put it: **≥ 10 of 13**.

## G0r — strict rare-phrase control (new, must pass)

For each row, take the **longest token in the target body that is ≥ 8 characters
and not a function word**, plus its two immediately adjacent tokens. Long
technical tokens (`@rpath/libgfortran.5.dylib`, `authProvider`, `NamedTemporaryFile`)
are the most selective vocabulary in the document, so this is the strongest
phrase the target itself can supply, and it is chosen **offline and
deterministically** — it never consults the index, so it cannot be tuned toward
whatever the index happens to like.

**Kill, as in the protocol: fewer than 10 of 13 targets in the top 10.** If G0r
fails, the arms are void permanently and no reading of them is permitted.

## G0t — title control (replication, must pass)

`in:title "<the target's exact title>"` must return the target at **rank 1** on
≥ 10 of 13. This replicates E169's rule on E169's rows with a fresh run, and it
separates two failure modes that G0 as declared could not: *ranking is broken*
versus *the query was unselective*.

## Reading rule, fixed now

- **G0r passes** → the index is shown capable of ranking a known-present
  document with a selective lexical query, and the arm numbers in
  `raw/summary.json` become interpretable as written.
- **G0r fails** → every arm number in this experiment is reported as void, the
  index is recorded as unable to perform the lookup this experiment needs, and
  no product is proposed on it.
- **G0t fails while G0r passes** → the arms still stand; the defect is confined
  to title matching.

## Cost

26 search requests (13 × 2), about three minutes at the unauthenticated rate
limit. No new population, no new arms, no changed queries.