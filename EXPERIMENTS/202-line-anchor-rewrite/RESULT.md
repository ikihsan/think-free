<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 RESULT — the line-anchor rewrite works, and is dominated by the CSS route

**Date:** 2026-10-20. **Outcome: the kill gate did NOT fire on the measured
pages, but the declared baseline-dominance clause did.** The deterministic
rewrite eliminates **83 of 83** empty-self-link `link-name` instances, adds
**0** strings, introduces **0** regressions and keeps **260 of 260** targets
resolvable — and the upstream CSS mitigation does the same without touching the
DOM, so arm 1 is **dominated** and the rewrite route is not worth building.
The population was also far too thin to validate: **G4 fires** (3 qualifying
pages / 3 hosts against a declared ≥ 12 / ≥ 6).

Protocol [`PROTOCOL.md`](PROTOCOL.md), prior art and demand
[`PRIOR-ART.md`](PRIOR-ART.md), amendments
[`AMENDMENT-1`](AMENDMENT-1.md)–[`3`](AMENDMENT-3.md). Harvester `fetch.js` /
`fetch2.js`, oracle run `run-arms.js`, gate computation `analyze.js`, G0 merge
`merge-g0.js`. Corpus hashed in `corpus-manifest.json` before any arm existed.

## 1. The gate vector, exactly

| gate | declared | result |
|---|---|---|
| **K1** oracle sees CSS | bare self-link reported in arms 0 and 2; CSS-hidden one not reported in arm 2 | **PASS** — arm 0 reports 3 `link-name` (2 codelineno + 1 bare), arm 2 reports 1 (bare only) |
| **G0 clause 1** oracle validity | axe completes on ≥ 90% of fetched pages (D200, AMENDMENT-2) | **PASS** — **76/79 records = 0.9620**, **70/73 files = 0.9589** |
| **G0 clause 2** | ≥ 8 qualifying pages hold ≥ 1 AA-tagged instance | **FAIL** — **3** qualifying pages (all 3 hold instances) |
| **G4** population | ≥ 12 qualifying pages across ≥ 6 hosts | **FAIL** — **3 pages / 3 hosts** |
| **G1** elimination | arm 1 eliminates ≥ 90% of AA-tagged instances whose axe target is an empty self-link | **PASS** — **83/83 = 1.0000** (kill < 0.60 not fired) |
| **G2** no fabrication | 0 added strings, every arm, every page | **PASS** — **0** |
| **G3** no regression | no new rule id; no page's AA count increases | **PASS** — 0 new rules, 0 increases |
| **G5** target survival | arm 1 keeps 100% of rewritten targets resolvable | **PASS** — **260/260 = 1.0000** |
| **D** demand | ≥ 3 independent public reports naming the class survive re-checking | **PASS** — 3 of 3 (see [`PRIOR-ART.md`](PRIOR-ART.md); one is duplicate-ID, not empty-anchor) |
| **baseline dominance** | if K1 passes and arm 2 removes as much of the class as arm 1, arm 1 is dominated | **FIRES** — arm 2 removes **83/83**, equal to arm 1 |

**Kill gate:** G1 < 60%, or G2 > 0, or G3 violated, or G5 < 100% → **NOT
FIRED**. The mechanism is real and clean. The route is still closed, on the
dominance clause the protocol declared for exactly this outcome.

## 2. The population, and the ceiling it imposes

Targeted `topic:mkdocs` harvest, fixed selection rule, no replacement after any
number was seen.

| label | records | distinct files |
|---|---:|---:|
| `D200` — HTTP 200 (the sweep's declared denominator) | 79 | 73 |
| `DALL` — every fetched record | 98 | 85 |
| `DBODY` — records with a stored body | 94 | 82 |

Stage 1: 69 fetched, **65 HTTP 200, 3 qualifying**. Stage 2: 29 targets, 14
HTTP 200, **0 qualifying**. **Only 3 of 65 stage-1 HTTP-200 pages contain
`__codelineno` or `anchor_linenums`** — a property of this query, not of the
web, and reported as such (protocol §"What this experiment cannot decide").

This is the ceiling. The declared G4 (≥ 12 pages / ≥ 6 hosts) is not met and
**no threshold is moved**. What survives is a mechanism demonstration on the
three pages where the class appears, not a population result.

**The contrast with E162 is the finding, and it is a population finding.** E162
§4 measured that **90 of 125 (72.0%)** of the WCAG-tagged instances on its
27 pages were one highlighter's line anchors — but those 27 pages were selected
for fame and defect density. A fresh, mechanically-selected mkdocs sample puts
the pattern on **3 of 65 pages (4.6%)**. E162's "every accessibility number is
computed on a denominator that is mostly plumbing" is a property of *its*
corpus, not a property of mkdocs sites.

## 3. The arms, per qualifying page

| page | AA arm 0 | AA arm 1 | empty self-links | eliminated by arm 1 | eliminated by arm 2 (CSS) | G1 rate | targets kept | targets arm 3 destroys |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `johnthagen.github.io/python-blueprint` | 8 | 1 | 7 | 7 | 7 | 1.0 | 7/7 | 7 |
| `fasthttp.ndugram.dev` | 53 | 3 | 50 | 50 | 50 | 1.0 | 227/227 | 227 |
| `h4m5t.top/SecNotes` | 28 | 2 | 26 | 26 | 26 | 1.0 | 26/26 | 26 |
| **total** | — | — | **83** | **83** | **83** | **1.0** | **260/260** | **260** |

Arm 0 is the fetched page round-tripped through the serializer; arm 1 rewrites
each empty self-link to `<span id="…"></span>`; arm 2 injects the CSS rule;
arm 3 deletes the anchors (the `anchor_linenums: false` route, simulated).
**Arm 3 destroys every target — 260 of 260 line permalinks stop resolving** —
which is the price of the configuration route the protocol named.

## 4. What this decides

1. **The rewrite is dominated, and the answer is negative about it.** Arm 2
   (upstream CSS) removes exactly the same class, changes nothing in the DOM,
   loses no target, and needs no migration. The rewrite's only claim is that it
   works where the stylesheet is not shipped (a raw HTML export, a pasted
   fragment) — a **scope statement, not a score**, as the protocol declared.
2. **The remedy is the build configuration.** `anchor_linenums: false`, or the
   CSS rule, or authored text inside the anchor. None of these is a new tool,
   and prior art already ships the CSS rule. **No candidate is proposed.**
3. **E162's headline is scoped, not withdrawn.** The deterministic repairer
   still eliminates 0 of 125 because the nodes carry no author-written string
   (F148); E202 adds that the *class* is common only where the highlighter's
   option is on, which a fame-selected corpus overstates.

## 5. Instrument defects, declared

- **`fetch2.js` overwrote its own files** (AMENDMENT-3 §2): it computed the
  output index inside concurrent callbacks, so 13 files carry two records and
  **6 of them have differing `sha256`** — one stored body was overwritten and
  is gone. None of the three qualifying pages is in the collision set, so no
  arm measurement is affected; the defect changes the denominator vocabulary
  (HTTP-200 is 79 records but 73 distinct files).
- **AMENDMENT-2's census sentence mislabelled the collision as fetch
  failures**; the arithmetic was the collision's, the label was wrong
  (AMENDMENT-3 §3).
- **The merge rule had an ambiguity**, resolved to "the retry supersedes the
  timeout" before the verdict existed, with the literal reading reported
  beside it (AMENDMENT-3 §1).
- **`pages/054-smilingwayne.github.io.html` got one axe attempt, not two.**
  It is an HTTP-200 page in the declared todo set, and AMENDMENT-2 put the
  timeouts in scope for one retry; it received only the `part0` attempt. It is
  one of the three records behind G0 clause 1's 76/79.
- **The oracle's determinism is a by-product, not a gate** (AMENDMENT-3 §1):
  six files carry two *completed* sweep records and all six agree exactly.

## 6. Identifier note — the experiment was renumbered from 200 to 202

The directory was built at `EXPERIMENTS/200-line-anchor-rewrite/`, and the
recorded commands (`commands.log` seq 4–20) name that path. It is renumbered
here to **202** because **E200 is already referenced by a pushed record**:
[`STATE-next-actions.md`](../../STATE-next-actions.md) line 68 names
"E200 (size-screen: small sub-segment …)" as a completed money-axis screen. The
unpushed side yields under the standing rule (F133, F146), and the internal
references (`fetch.js`, `fetch2.js`, `package.json`, `corpus-manifest.json`,
fixture, amendments) were updated to match.

**The referenced money-axis E199–E201 has no committed experiment directory in
any fetched ref**, and the committed `EXPERIMENTS/199-…` is a different
experiment (a PyPI view-count matched harvest). The claim is unsubstantiated in
this tree and is corrected in `STATE-next-actions.md` by this session; it is
recorded as F149.

## 7. What this experiment cannot decide

- **Real-browser behaviour.** jsdom performs no layout or navigation; whether a
  line permalink still *scrolls* is asserted from target survival, not measured.
- **Assistive-technology outcomes.** `link-name` eliminated is a rule verdict,
  not a screen-reader measurement (E162's ceiling, unchanged).
- **Prevalence.** A `topic:mkdocs` sample says nothing about the web; 3/65 is
  the query's qualifying rate.
- **The 6 overwritten bodies.** They are gone; nothing downstream depends on
  them, and the defect is bounded by the census.

## 8. Reproduce

The fetched pages are **not committed** — they are pinned by url, sha256 and byte
count in `corpus-manifest.json` (the F004 rule: pin the inputs by hash, do not
commit the bodies), and re-fetch with the committed scripts:

```bash
tools/x -- node EXPERIMENTS/202-line-anchor-rewrite/fetch.js    # stage 1
tools/x -- node EXPERIMENTS/202-line-anchor-rewrite/fetch2.js   # stage 2
tools/x -- node EXPERIMENTS/202-line-anchor-rewrite/run-arms.js arms
tools/x -- node EXPERIMENTS/202-line-anchor-rewrite/analyze.js   # G1..G5, K1..K3, dominance
tools/x -- node EXPERIMENTS/202-line-anchor-rewrite/merge-g0.js  # G0 clause 1
```

Committed beside this file: the prior-art and probe captures under `raw/`
(13 files), `corpus-manifest.json`, the four `results-*.json` arm/sweep/G0
records, `gates.json`, `fixtures/k1.html`, and the scripts. The `pages/` bodies
are re-fetched, not stored.

