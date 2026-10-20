<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E194 RESULT — twelve recurring consumer jobs are served by free apps, and the one paid "hit" is the wrong product

**Date:** 2026-10-19. **Outcome: G2 FIRED in both panels — the declared gates
report no demand finding.** One descriptive fact survives, and it is the
first money-side observation in 188 experiments.

Protocol [`PROTOCOL.md`](PROTOCOL.md), corrections
[`AMENDMENT-2.md`](AMENDMENT-2.md). Panels: `scan.py` (1),
`scan2.py` (2). Raw: [`raw/scan2.json`](raw/scan2.json).

## 1. The question

Every candidate this record has selected was chosen by a *question being asked
in public*. Six service closures in a row ended with the finding that the need
was already served (F075, F081–F083, F096, F104). **Not one of the 187 earlier
experiments asked whether anyone pays.** E193 found the marketplaces carrying
prices unreachable from this host and the iTunes Search API reachable, so this
scan asked the money question where a price exists.

## 2. Gates — both panels

| Gate | Bar | Panel 1 | Panel 2 |
|---|---|---|---|
| G1 positive controls | each control yields ≥1 app ≥ $0.99 | PASS | PASS |
| **G2 negative control** | **nonsense term returns 0 results** | **FAIL** | **FAIL** |
| G3 money exists | ≥4 of 12 have ≥5 paid apps | FAIL | FAIL |
| G4 thin supply, high demand | ≥1 row: ratings ≥ 100k, paid ≤ 10 | PASS | PASS |
| G5 fetch reproducible | two terms identical twice | PASS | PASS |
| G6 relevance in every row | ≥60% of returned apps name a term token | — | FAIL |

**Under the declared protocol, G2 firing makes every difficulty row
`not_evaluated`, so this experiment reports no demand finding.** Panel 1's
G4 pass is void; panel 2's is explained in §4 and is also void.

## 3. What G2 actually fired on, and the third instrument defect

Panel 1's negative control was `zzqxqv glorb tapestry`, and **`tapestry` is a
dictionary word** — the API returned 19 real knitting apps and the control
failed for the wrong reason (D3). Panel 2 used `zzqxqv glorbwump`, which has no
dictionary word, and the API returned **4 results: `ZX Globus`, `Gigabull`,
`WHACKO`, `Goofballs: Fling & Fly Game`.** All four are free games.

**D5 — this API pads every query with about four irrelevant apps.** It is a
property of the source, so a `resultCount == 0` negative control is a bar this
source **cannot** meet at any limit. The useful consequence, which is a fact
about the contamination rather than a rescue: **the padding is free**, so `paid`
counts are less contaminated than `free` counts — 0 of the 4 padded apps were
paid.

Panel 1 also measured the wrong window: `limit=200` returns ~190 results where
`limit=20` returns ~18, and the extra 170 are filler (D4). Panel 1's numbers
were measurements of the padding and are not quoted.

## 4. The one number the experiment was built to get

Panel 2, `limit=25`, whole returned set, per-row relevance checked:

| term | returned | paid | median paid $ | ratings on paid apps |
|---|---|---|---|---|
| shift schedule | 25 | 0 | — | 0 |
| receipt scanner | 23 | 1 | 12.99 | 297,092 |
| warranty tracker | 22 | 2 | 0.99 | 2 |
| home inventory | 25 | 1 | 3.99 | 0 |
| meal plan | 21 | 0 | — | 0 |
| pet medication | 24 | 0 | — | 0 |
| chore chart | 25 | 0 | — | 0 |
| moving checklist | 24 | 1 | 2.99 | 494 |
| plant watering | 23 | 0 | — | 0 |
| reading list | 24 | 0 | — | 0 |
| sourdough | 25 | 1 | 2.99 | 40 |
| pool care | 25 | 0 | — | 0 |

**286 on-topic apps across twelve recurring household jobs. Six are paid
(2.1%).** The five that are genuinely in-niche are `Warranty Tracker: Easy
Track` (0 ratings, $0.99), `My Homes Vault` (0, $3.99), `BreadMe` (40, $2.99),
`Paperless: Lists + Checklists` (494, $2.99), `Purchase Warranty Tracker`
(2, $0.99) — **paid competition exists and nobody buys it.**

**The 297,092 ratings that made panel 2's G4 pass are `TurboScan™ Pro`
($12.99), a general PDF scanner**, returned because it matches the word
*receipt*. It is not a receipt archiver, and its ratings are not demand for
one. **G4's pass was a mis-attributed market**, which is the same failure shape
as E175's `hapijs/code` → `microsoft/vscode` (F135): a word collision returned
a confident wrong answer.

**G6 is miscalibrated and cannot be used as declared.** Its bar is 60% token
match on app name and seller; the positive control `todo` — whose results are
unambiguously on-topic (`Microsoft To Do`, `Todoist`, `Google Tasks`) —
scores **0.1304**. A metric with a floor below 0.13 cannot separate padding
from synonym mismatch, so `pet medication` (0.5833) and `chore chart` (0.48)
failing it is **not evidence of contamination**. Recorded as an instrument
limit, not a row-level finding.

## 5. What this decides

**Descriptive only, because G2 fired:** in the US iOS store, twelve
pre-declared recurring household jobs are served by **dense free supply** —
23–25 on-topic apps each, with category leaders at 4,000–500,000+ ratings —
and by **paid supply that does not sell**. Two thirds of the difficulties have
**no paid app at all**.

**The decision it changes.** Candidate shapes are no longer drawn from
consumer app-store categories. Two reasons, both measured here rather than
argued: there is no revenue upside in these niches, and — the part that matters
more for an open-source project — the free alternatives are already dense, which
is the "the need is served" result (F096, F104) arriving through a completely
different instrument. A mission whose output is an open-source tool should look
where people **already pay for software** at the level of an organisation:
infrastructure, professional and B2B, not household chores.

**What this does not decide.** It does not say those twelve jobs are unserved by
open source, that iOS is the wrong channel for them, or anything about any
difficulty outside the declared list. It does not bound prevalence for anything.
Its population is 15 hand-declared terms, which is a hypothesis about the space
and not a sample of it.

## 6. The instrument, for a later reader

Reachable from this host: **iTunes Search API** (`limit ≤ 25`, whole returned
set; 4 junk results on a nonsense term; all free). Not reachable: Etsy, eBay,
Reddit, DuckDuckGo, Census without a key, Google Books (429),
Open Collective (the only working query needs one written against its schema),
GitHub (200 but unauthenticated budget, and a zero-result response is 55 bytes —
a length rule calls it a refusal). Full table in
[`E193`](EXPERIMENTS/193-source-capability-probe/RESULT.md).

**The money axis is therefore open in one place only so far: the iTunes store.**
The stronger money source that this host can still reach is *spend*, not
*price* — USAspending contract amounts and Comtrade trade values both answered
`200`. That is the named next action.

## 7. Artifacts

- `PROTOCOL.md` — terms, window, metrics and gates, declared before any fetch
- `AMENDMENT-2.md` — D3, D4 and the unchanged bars
- `scan.py`, `scan2.py` — the two panels
- `raw/scan.json`, `raw/scan2.json` — every fetch, hashed
- [`E193`](EXPERIMENTS/193-source-capability-probe/) — the reachability probe
  and its two panels