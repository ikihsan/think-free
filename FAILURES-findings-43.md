<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-17
-->

# Failure findings 43 - an arm in the raw file and absent from the write-up

Continued from [`FAILURES-findings-42.md`](FAILURES-findings-42.md), split at
the 300-line cap.

## F134 — a gate that declared its own product constraint fired and was never reported, and the closure went out on 2 of the experiment's 7 arms (E174)

**Date:** 2026-10-17. `EXPERIMENTS/174-scoped-reach-recompute/`. Raw:
[`results.json`](EXPERIMENTS/174-scoped-reach-recompute/results.json).

### What was asked

Whether the version-pinned closure (F132) follows from E170's own committed
evidence. E170 stored seven arms in `raw/summary.json`; its write-up reported
two.

### What happened

`raw/summary.json` reports **seven** arms. `RESULT.md` reports **two** — the two
**global** ones — and F132, the `HYPOTHESES.md` status row and `STATE.md` all
inherit the conclusion built on them. Recomputed from E170's raw responses with
rank re-derived from the returned URL lists (never read from a stored rank), all
seven reproduce exactly (**G1 pass**) and the row-to-record alignment is proven
from both sides: 97 of 97 records consumed, 0 leftover, **0** mismatches on
either the replayed query string or the log's own `arm` label (**G2 pass**).

| | global | repo-scoped |
|---|---|---|
| quoted error string | 1/13 = 0.0769 | **5/13 = 0.3846**, median `total_count` **1** |
| component + symptom words | 2/13 = 0.1538 | **5/13 = 0.3846** |
| union of arms | 2/13 = 0.1538 | **6/13 = 0.4615** [0.2321, 0.7086] |

Paired on the same 13 rows: union comparison **4 scoped-only, 0 global-only**,
McNemar exact **p = 0.125**; per arm, p = 0.25 / 0.125 / 0.25. The best scoped
point estimate, **0.3846**, clears E170's own declared **0.30** build bar; its
Wilson lower bound, **0.1771**, does not.

The protocol had asked for exactly this. **G1** — "A0 hit rate, bare and quoted,
**globally and repo-scoped**" — is a declared measurement of the incumbent arm.
**G3** — "Global versus repo-scoped, for both arms. **If repo-scoped succeeds
where global fails for both arms**, the mechanism needs the developer to already
know the repository, which is a product constraint and **is recorded as one**" —
fired. Neither G1's scoped rows nor G3 appears anywhere in `RESULT.md`.

The kill itself was also scoped without declaration: G2 is "paired comparison of
A1 against A0 on the same rows, **same scope**", and the comparison reported is
`A1_global_vs_A0_quoted_global` — the global scope, chosen after the fact, which
is the scope at which the mechanism looks worst.

### Why it happened

The arms were computed, stored and summarised correctly; the reporting stage
selected the arms that supported the sentence the file was written to make. The
number of arms in `summary.json` (7) and in the prose (2) disagreeing was visible
to any reader of both files, which is the cheapest possible check.

### What it changes

- **F132, E170's `RESULT.md`, the `HYPOTHESES.md` row and `STATE.md` are
  corrected in place** on 2026-10-17. The vocabulary finding stands; the closure
  does not.
- **The version-pinned line is reopened for a fresh-sample measurement**, and the
  open question is the one G3 named: the mechanism requires knowing the
  repository. **E175** asks whether the repository can be derived from a failure
  report — mechanical, registry-backed, no search engine.
- **Rule: an arm present in `summary.json` and absent from the write-up is a
  defect in the write-up, and the check is a count.** Declare the number of arms
  in the protocol and reconcile it against the number reported *before* the
  sentence is written. A gate that predicts a product constraint is a **result**,
  and reporting only the gates that closed the line is how a line gets closed on
  one cell of a 2×2.
