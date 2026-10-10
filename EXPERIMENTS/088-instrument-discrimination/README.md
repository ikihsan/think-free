<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E088 — the E081–E087 instrument cannot tell a real answer from a nonexistent one

`observed` 2026-10-10, session `2026-10-10-004`, VM `instance-20260717-0944`.
Finding **F109**, decision **D095**. Gates in [`PROTOCOL.md`](PROTOCOL.md),
declared before the harvest ran; raw bytes in
[`raw/probe-results.jsonl`](raw/probe-results.jsonl); everything regenerates
with `python3 analyze.py`.

## Result

| gate | result |
|---|---|
| G1 discrimination | **FAIL** — 8 of 20 nonexistent products classified `served` (0.40); 11 of 20 genuinely-served questions classified `served` (0.55); difference +0.150, Newcombe CI95 **[−0.148, +0.414]**, spanning 0 |
| G2 retrieval relevance | PASS — 164 of 215 committed rows (0.763) had an on-topic result |
| G3 gradient survives | PASS — the ordering E081 ≤ E082 ≤ E083 ≤ E084 ≤ E085 holds on all rows and on relevant rows |
| G4 keyword attribution | (reported) 102 of 215 treatment rows called `served`; 18 of those stop being `served` when weak-keyword page titles are removed |

The predeclared kill gate was "a candidate only if G1 **and** G3 pass". G3
passed, G1 failed by a wide margin, so **the E081–E087 generalisation line is
closed** and `EXPERIMENTS/synthesis-view-count-principle.md` is corrected.

## What the instrument actually is

E081–E087 each ship an `outcome.py` whose `classify_served()` joins the five
retrieved titles and snippets into one string and returns `served` if **any
substring** from a 19-word solution list — including `app`, `tool`, `method`,
`guide`, `fix`, `solution` — appears anywhere in it. The string
`view_count` appears in those seven directories only inside `PROTOCOL.md`
prose; no code path and no data file reads an arrival count.

The corpora are also not what the protocols declare. All **500** corpus rows
match `<term> <verb> <integer>`, the integer running 1…N as a sequence
counter (`"centrifuge E01 error 1"`, `"pipettometer error code 2"`). E081's
protocol names its control arm as "E062 non-software Stack Exchange corpus
(110 no-remedy rows) … title, body, `view_count`, `is_answered`"; **no Stack
Exchange row is present in any of the seven directories**, and
`raw/control-needs.jsonl` is byte-identical (md5 `848be7f5…`) across E083–E087.

## The mechanism, measured rather than assumed

The post-hoc diagnostic separates retrieval failure from classifier failure.
For each probe, does any retrieved page actually mention the subject?

| arm | subject mentioned | called `served` | called `served` **while off-topic** |
|---|---|---|---|
| known-served | 13/20 | 11/20 | 2/20 |
| known-unserved | **0/20** | 8/20 | **8/20** |

Every one of the eight false positives is a page set that never mentions the
thing asked about. The instrument's `served` verdict fires on generic web
chrome alone. Reading the raw rows:

- `Brantmore Trellis-9 startup checklist` → clipart icon vectors
- `Halberdix Ferrolux-6 coolant mixing ratio` → *"Is it bad idea to disable
  apps from running in the background?"* (Windows 10 tutorials)
- `Corvane Stellarium-19 bearing tolerance` → adult-content spam

All three are classified `served`. The firing keyword is `app` in 7 of 8 cases
— in `"disable apps"`, in app-store boilerplate.

## A second, independent defect: the scrape is not returning search results

A real Bing result carries a title; an ad slot, nav block, or spam panel does
not. Empty-title rate over the committed treatment rows:

| domain | empty titles | rows with ≥1 real title |
|---|---|---|
| E081 | 54/163 = 0.331 | 35/35 |
| E082 | 60/148 = 0.405 | 28/30 |
| E083 | 81/145 = 0.559 | 29/30 |
| E084 | 96/150 = **0.640** | 24/30 |
| E085 | 65/149 = 0.436 | 29/30 |
| E086 | 66/135 = 0.489 | 20/30 |
| E087 | 72/150 = 0.480 | 26/30 |

A third to two-thirds of the extracted blocks were never results. E084, the
domain the gradient places mid-slope, has the worst retrieval of the seven.

## Why G3 passing does not rescue the synthesis

G3's ordering holds, and that is reported as observed. It is also
uninformative about domains: `partially_served` is produced by
`classify_served` and relevance restriction never touches the classifier, so
restricting rows cannot move the ordering. What the ordering measures is which
query template happens to trip the chrome list. The synthesis read that
ordering as *how code-structured each domain is*; nothing in these runs
connects a domain's structure to any number in the table.

## Limits of this experiment

- **G2 was too lenient and I am recording that against myself.** It asked
  whether any non-chrome content token appeared anywhere in five HTML blocks,
  and passes at 0.763 while a third to two-thirds of those blocks are not
  results. A gate whose passing region is that wide cannot fail — F101's shape,
  one layer down, in a gate written *after* reading F101.
- One search engine, one classifier, 40 probes, n=20 per arm. This shows the
  instrument fails to discriminate; it does not show no instrument could.
- The probes were frozen before the harvest, but they were written by the same
  agent that interprets them. They are independent of the E081–E087 corpora,
  not independent of me.
- A pass on G1 would not have validated E081–E087's numbers either; only made
  further work on them reasonable.

## What this closes and what it does not

Closed: seven experiments, one committed cross-domain synthesis, and the route
that produces them — "fresh observation in a new domain" applied to
`classify_served` over Bing. Running an eighth domain would repeat a
measurement already shown not to measure its own variable.

Not closed: that needs exist which structured fault/error-code domains have,
or that no domain has. This run never measured a real need statement — it
measured a classifier against 40 probes. The population question is untouched
and is where a successor should start.