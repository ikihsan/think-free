<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 — AMENDMENT-2, declared before the sharded sweep ran

**Declared 2026-10-20, after `gates.json` already existed and before any shard
of this amendment executed.** The reason is wall-clock, not measurement: the
single-process `sweep.js` had recorded 50 of 79 pages in ~89 minutes, three of
them `axe timeout` at the instrument's own 240 s ceiling, and the process was
killed at 52 minutes of elapsed time on its second invocation (session event
15). G0 clause 1 was still unmeasured.

## What changes

> **Sharding.** The remaining todo set — every HTTP-200 page with no successful
> record yet in `results-sweep-arm0.json`, which is `79 − 47 = 32` pages
> including the three timeouts — is partitioned `todo[k] → shard (k mod 3)`.
> Each shard writes `results-sweep-arm0-part<i>.json` after every page, so an
> interruption loses at most one page. Merge rule, declared here: main record's
> successful pages first, then every part file, **deduplicated by `file`**, in
> `corpus-manifest.json` order; a page appearing in two records with different
> outcomes is a defect and stops the merge.

## What does not change

- The oracle: `shard-sweep.js` imports `applyArm`, `withAxe`, `axeRun` from
  `run-arms.js` — the same functions `sweep.js` used. No second implementation.
- The page set (HTTP-200, `corpus-manifest.json`), the 240 s per-page timeout,
  the record shape, and every gate threshold.
- `gates.json`'s already-computed arm verdicts (G1, G2, G3, G5, K1, dominance)
  are untouched by this amendment; G0 clause 1 is the only thing it can move.

## What would have been cheating (named so it is checkable)

Running the sweep only on pages likely to be small, dropping the three
`axe timeout` pages from the denominator instead of retrying them once, changing
the 90% threshold, or re-running axe on any page already recorded as complete.
None of these happens.

## Denominator ambiguity, declared before the verdict is read

PROTOCOL.md writes "axe completes on ≥ 90% of **fetched** pages" while
`sweep.js` filters `status === 200`. The corpus holds 98 fetched pages, 79 with
HTTP 200, and 85 stored bodies (13 fetch failures have no body at all). G0
clause 1 is therefore reported under **all three denominators** in `RESULT.md`,
with the HTTP-200 one labelled the sweep's declared denominator, and the
literal all-fetched reading labelled as counting 13 pages the oracle was never
handed. The verdict line names which reading it uses; it does not pick the
larger rate silently.
