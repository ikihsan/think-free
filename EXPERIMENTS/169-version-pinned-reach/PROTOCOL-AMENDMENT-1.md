<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E169 AMENDMENT 1 — widen the reachability target from the accepted answer to
the thread; add a null-query control

Recorded **before a single search request was issued** and after reading only
`--dry-run` counts, not any query result.

## What the dry run showed

The protocol's target was "the first `github.com` issue/PR/commit URL in the
**highest-scored answer**". Over the 78 measurable rows that yields **6** rows
— below the floor of 8 the protocol itself set for G2, so as written G2 would
have returned `not_exercised`.

That count is not a defect in the rows; it is a finding about the premise. E168
reported "`github.com` in 15 of 24" from **all answers** in each thread, and
this session's recount (G0) puts that figure at 12–13 by `href` and 13 by
any-text URL, in any answer. The accepted answer links to a tracker in 4 of
E168's 24; the *thread* contains a tracker link in 13 of 24. So **the fix is
usually described inline by the person whose answer was accepted, and the
tracker link is in someone else's answer.** E168's summary figure described
the thread and read as though it described the resolution.

## The change

- **Target = the first `github.com` issue/PR URL in the thread, accepted answer
  first.** The incumbent developer reads the whole thread, so "does the
  developer's own query reach the source the thread points to" is the right
  question, and it is the question the gate was written for.
- **Denominator = every measurable row whose thread contains a tracker link**,
  whatever the accepted answer does.
- `issuetracker.google.com` and vendor trackers stay `not_exercised`: they have
  no public search API, and a dead end is recorded as one.

## Why this does not bias the result in the direction that flatters the class

It does bias toward a *reachable* population, and the bias is stated: rows
whose thread contains no tracker link are excluded, so G2 says nothing about
them. They are counted and reported separately, and their count is the size of
the population where the incumbent's tracker step is not the mechanism at all.
A G2 share near 1.0 over tracker-linked rows is a statement about tracker-linked
rows.

## Added control: G5, the null query

For each queried row the run also issues the query a developer would plausibly
type **without** the error literal — the question title's first eight words. The
exact literal must beat it, or the measurement is not measuring the literal.
Declared in advance: if the null query reaches the target at a rate not
materially below the exact-literal rate (within 0.10 absolute), the result is
reported as `not_attributable_to_the_literal` and no reach claim is made.

## Not changed

Population, gates, thresholds, the extractor's rules, and the "one-sided"
reading of a miss. A miss is still evidence about this index and this query,
never about search at all.