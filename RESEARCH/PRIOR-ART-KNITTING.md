# Prior art — the knitting repair planner's last kill-gate condition

<!-- origin-meta
owner: RESEARCH.md
status: sealed
last-verified: 2026-10-03
-->

Written 2026-10-03 (T-0015). This answers the one untested condition on the
knitting candidate's kill gate, quoted from [`HYPOTHESES.md`](../HYPOTHESES.md):

> Abandon the algorithmic-advantage claim if existing graph tooling already
> supplies equivalent intervention sequences.

Stage A is settled mechanically (T-0010, T-0011), and
`EXPERIMENTS/005-knitting-bounded-search/README.md` already refuses to claim the
search decomposition as novel. What had never been searched was the outside
world. `RESEARCH/C.md` searched user-facing and hobby vocabularies, and
recorded that "no patents were comprehensively searched".

**Nothing here is a measurement.** This is a literature and product search. It
can end a claim; it cannot validate one.

## Method

Three vocabularies, as
[`prior-art-check`](../.agents/skills/prior-art-check/SKILL.md) requires:

| Vocabulary | Backends used | What it is good for |
|---|---|---|
| The user's: "fix a knitting mistake", "mend knitwear", "darning machine" | DuckDuckGo HTML | Craft practice, commercial tools, the incumbent |
| The academic: "knit graph repair", "unravelling repair knitted structure", "knitting machine mending" | OpenAlex, Crossref, arXiv API | Papers, including abandoned lines |
| The infrastructure: "repair planning graph transformation", "consistency repair closure minimal deletion" | OpenAlex | The mechanism under another discipline's name |

Plus the mandatory non-search checks: limitation material of the tools
`RESEARCH/C.md` already named, the GitHub repository API, and one patent
search. Exact queries are in the query log below.

**Not searched, and this is a real limit:** no German, Japanese or Chinese
full text (the mending-machine patents are German and were read only through
search-index metadata); no Ravelry, Reddit or YouTube corpus; no library books;
no commercial product was used or bought; no user was contacted; no citation
graph was traversed from the papers found.

## What was found

Every row records the evidence actually read. `Abstract` means the publisher's
or index's own abstract; `Index` means title, dates, assignee and a claim
snippet from a search index, with no full text.

### A. Knitting computation: generation, not repair

| Source | Published | What it does | Evidence | Status |
|---|---|---|---|---|
| [KnitPicking Textures (UIST 2019)](https://doi.org/10.1145/3332165.3347886), [KnitPick](https://textiles.cs.cmu.edu/publications/2019-knitpick/) | 2019 | Parses hand-knitting notation into KnitGraphs, emits hand and machine instructions; contributes KnitCarving (shape a graph) and KnitPatching (merge graphs) plus a 472-texture measured dataset | Abstract (OpenAlex, via API) | Academic, live |
| [Programming mechanics in knitted materials](https://doi.org/10.1038/s41467-024-46498-z) | 2024 | Constitutive model relating stitch topology to elasticity; designs fabrics for target mechanics | Abstract (OpenAlex) | Academic, live |
| [Laddering of a knitted fabric](https://arxiv.org/abs/2604.20580) | 2026-04-22 | Experiments plus discrete-element simulation of ladder propagation; tension threshold for onset and arrest; "damage prediction at moderate tension"; mitigation left to implications | Abstract (arXiv API) | Preprint |
| [Knit sketching](https://doi.org/10.1145/3450626.3459752), [KnitUI](https://doi.org/10.1145/3411764.3445780), [Wearable 3D Machine Knitting](https://doi.org/10.1109/tvcg.2021.3056101), [Twine](https://doi.org/10.1145/3609023.3609805), [Wooly Graphs](https://arxiv.org/abs/2407.00511) | 2021–2024 | Generate knitted structures from programs or sketches | Titles, years, venues (OpenAlex) | Academic |
| [`mhofmann-Khoury/knit_graph`](https://github.com/mhofmann-Khoury/knit_graph) (MIT, 1 star, pushed 2026-04-03) | — | Loop/yarn/stitch/crossing graph representation, a library of basic knit graphs, a stitch visualiser | README read in full | Open source, near-dormant |
| [KnitGraphToStitchMesh](https://github.com/rahul-mitra13/KnitGraphToStitchMesh) (5 stars, pushed 2026-03-10), [KnitGraph-Viewer](https://github.com/anonymousresearcher1111/KnitGraph-Viewer) | 2026 | Graph-to-mesh conversion and a graph viewer | Repository metadata only | Open source |

**Not found:** any system, paper or repository that computes a repair or
intervention sequence for an already-knitted structure. Two targeted OpenAlex
queries (`unravelling repair knitted structure graph planning intervention`, 69
total hits; `knit graph repair algorithm unravelling ladder`, 3 total hits)
returned nothing on the subject, and five GitHub repository-API queries
(`knitting repair planner`, `knit graph repair`, `knit stitch repair algorithm`,
`knitting error correction`, `knitting fix mistakes`) each returned
`total_count: 0`.

### B. Pre-emptive checking, in the chart rather than the fabric

| Source | Published | What it does | Evidence | Status |
|---|---|---|---|---|
| [EnvisioKnit Chart Checker](https://www.envisioknit.com/manual/chart-editor-other-features/) | undated page, retrieved 2026-10-03 | Flags chart errors that would make a pattern unknittable — chiefly row stitch-count imbalance — listing row, reason, and the kind of fix ("could be fixed with a double-decrease") | Manual page read in full | Commercial, live |
| [Knitscape](https://github.com/knitscape/knitscape) (64 stars, pushed 2026-09-25), [Stitchmastery](https://stitchmastery.com/) (since 2011), [knit-a-stitch](https://github.com/notwaldorf/knit-a-stitch) (52 stars) | 2011– | Chart design, simulation, chart↔text conversion | Repository and site metadata | Open source and commercial |
| [Craft Yarn Council chart symbols](https://github.com/leifrogers/cyc-svgs) (5 stars, pushed 2026-06-16) | — | Vector reproductions of the CYC standard symbol set | Repository description | Standard-adjacent |

### C. The craft-side incumbent: physical tools, tutorials, one AI service

| Source | Published | What it does | Evidence | Status |
|---|---|---|---|---|
| [KnittingFix](https://www.knittingfix.com/) | undated, retrieved 2026-10-03 | Photo/video diagnosis of a mistake by computer vision, step-by-step fix, human escalation at under 75% confidence; free tier 3 AI diagnoses a month; several plan tiers still "Coming soon" | Homepage read in full; marketing claims unverified | Commercial, live |
| [Knitmend PatchMaker](https://knitmend.com/) | undated | Weaving patch device that re-knits a patch directly onto existing knitted fabric | Search-index snippet | Commercial |
| Darning looms, mending tools (multiple vendors) | — | Hold fabric and re-weave a patch over a hole | Search-index snippets | Commodity |
| Ten Rows A Day, Crafty Cavy, Knit with Henni, TECHknitting, KnittingHelp | 2020–2026 | Technique tutorials: unravelling, ladder repair, disguising a crossed cable without reconstructing it | Search-index snippets and `RESEARCH/C.md`'s earlier reading | Free content |

### D. Industrial mending machines: the physical capability already existed

One Google Patents query succeeded (`q="mending" "knitted fabric" knitting
machine`, 22 results); later queries and every full-text retrieval returned
HTTP 503 from this host, so these are **index metadata only**.

| Publication number | Filed / granted | What it claims | Evidence | Status |
|---|---|---|---|---|
| DE836074C | 1950-03-31 / 1952-04-07 | Method and devices for producing **and mending** knitted and hosiery goods | Index + claim snippet | Expired |
| US1845516A, "Machine for repairing knitted fabrics" (Joseph S. Pecker) | 1929-06-12 / 1932-02-16 | Machine that repairs knitted fabric, with inspection illumination | Index + snippet | Expired |
| DE616198C, "Single thread knitting machine for mending knitted goods" | 1932 / 1935 | Guide needles re-knit a damaged region | Index + snippet | Expired |
| DE192972C | — | Machine for mending damaged knitwear | Index | Expired |
| DE892655C | 1943 / 1943–1953 | Holders for mending machines for knitted, hosiery and woven goods | Index + snippet | Expired |

No patent page was opened, so no URL is quoted for these; the identifiers
come from the one successful search-index query, which returned them with
titles, filing and grant dates, assignees and claim snippets.

**Reading.** Between the 1920s and the 1950s a machine class existed whose
entire purpose was re-knitting an already-knitted, locally damaged region. The
hardware version of "produce an intervention on existing fabric" is therefore
old art, not a gap. Whether any of it survives in a current product is
**unknown**: no live machine-knitting mending feature was found, and this
report does not claim one exists.

### E. The algorithmic mechanism, under other fields' names

The planner computes a minimum-cost set of interventions under constraints,
decomposes the problem into neighbourhoods that cannot interact, and searches
each separately. Under the infrastructure vocabulary that is established work:

| Source | Published | What it does | Evidence | Status |
|---|---|---|---|---|
| [Computing Optimal Repairs for Functional Dependencies](https://doi.org/10.1145/3196959.3196980) (ACM TODS) | 2018 | Optimal repairs of a constraint set under a cost | Title, year, venue, 74 citations (OpenAlex) | Academic |
| [Detecting Ambiguity in Prioritized Database Repairing](https://doi.org/10.4230/lipics.icdt.2017.17) | 2017 | Which minimum repairs exist, and when the choice is ambiguous | Title, year (OpenAlex) | Academic |
| [Optimizing and implementing repair programs for consistent query answering](https://openalex.org/W2999514540) | 2007 | A *repair program*: an ordered sequence of repair operations | Title, year (OpenAlex) | Academic |
| [Using weakest application conditions to rank graph transformations for graph repair](https://doi.org/10.46298/lmcs-22(1:10)2026) | 2026 | Ranking graph-repair transformations | Title, year (OpenAlex) | Academic |
| [Empowering model repair: a rule-based approach to graph repair without side effects](https://doi.org/10.1007/s11334-024-00587-w) | 2024 | Graph repair under rules, side-effect constrained | Title, year (OpenAlex) | Academic |
| [Repairing web service compositions based on planning graph](https://openalex.org/W110768368) | 2010 | Planning-graph repair of a composition | Title, year (OpenAlex) | Academic |

The pattern is the candidate's, exactly: minimal-cost repair under constraints,
searched in a structured way, with a *sequence* as the output. Only the
material being repaired is different.

## The six fields the check must record

**Prior art.** The tables above: KnitPick (2019), the stitch-mechanics and
laddering papers (2024, 2026), `knit_graph`, EnvisioKnit's Chart Checker,
KnittingFix, darning looms and tutorial sites, five 1929–1953 mending-machine
patents, and six computer-science papers on minimum-cost repair planning.

**Inspected.** Full text read: `knit_graph` README, the KnittingFix homepage,
the EnvisioKnit manual page. Publisher or index abstracts read: KnitPicking
Textures (via OpenAlex's inverted abstract), the laddering preprint and the
Nature Communications paper (via the arXiv and OpenAlex APIs). Index metadata
with claim snippets only: all five patents, and the remaining graph-repair
papers — **none of those six papers' full texts were opened.** Nothing was
executed or benchmarked.

**Difference, in one sentence.** No prior work found computes a
minimum-cost, checkable *intervention sequence* for repairing a structure a
person has already knitted by hand, where the alternative is unravelling rows.

**Why it matters — and the honest answer.** Only under two conditions
that are both unproven here: the plan must save a knitter enough work to beat
looking up a tutorial, and it must be *checkable*, which means the user must
supply a correct chart patch and a loop orientation the planner can verify.
Every tool found either diagnoses from a photo (KnittingFix), checks the chart
before knitting (EnvisioKnit), patches a hole with a tool, or generates fabric
from a program. If the honest answer for a given error class is "a tutorial and
five minutes is better", that is the finding.

**Surviving risk (the strongest argument that this is a clone).** The graph
layer is KnitPick's and `knit_graph`'s; the minimum-cost-repair algorithm is a
decades-old idea in constraint repair; the physical capability is a
ninety-year-old machine class; the user-facing diagnosis is a shipped
commercial product; and the remaining novelty is a *report format* (SVG map,
checkpoints, refusal) plus a user with no observed demand. A patch to
KnitPick's graph representation, or a printable page from an existing charting
tool, would deliver most of it.

**Confidence.** `source-supported` for each named work's existence, date and
stated capability. `observed` for the two negative searches that a repair
planner does not appear in OpenAlex or the GitHub repository API. `inferred` for
the judgement that no such tool exists — one agent, one day, three
vocabularies, no full-text patent reading, no Chinese, Japanese or German
sources. **Not `observed`:** that no repair planner exists anywhere.

## Verdict on the kill-gate condition

The condition as written conflates two different claims, and the distinction
decides the candidate's fate:

| Reading of the condition | Result |
|---|---|
| **A. Domain tooling already supplies equivalent intervention sequences** — does a knitting tool already do this? | **Not met.** Nothing found supplies an ordered, checkable repair sequence for an existing hand-knitted structure. Knitting tooling generates, charts, or checks; industrial mending machines did the job mechanically and are expired. |
| **B. The planner's algorithmic advantage is novel** — is the mechanism new? | **Met, decisively.** The mechanism is textbook minimum-cost repair under constraints, decomposed over independent neighbourhoods, with a published literature from 2007 to 2026. T-0011 already recorded that its own optimality follows from the model's structure. |

**Consequence: the algorithmic-advantage claim is abandoned.** Per
[`prior-art-check`](../.agents/skills/prior-art-check/SKILL.md) this is a
failure record, not a footnote: it is written up as `FAILURES.md` F009 so no
session revives the search-decomposition line.

What survives is narrow and physical, and this repository cannot test it: **a
craft tool** that turns a small local error into a printed, checkable sequence
of stitches, for a person who cannot already do the repair. That is a
usefulness question, not an invention question. `RESEARCH/C.md`'s own abandon
reason still stands: if the user must already understand the structure to supply
the patch, the tool serves only those who can already solve it. Stage B — real
swatches, an experienced knitter, authorization — is the only test left, and
none of it can run here.

**What would change this verdict.** A current product that mends knitwear on a
machine and publishes its intervention logic; or a paper computing repair
sequences over knit graphs that this search missed; or a demonstration that a
knitter follows a generated plan and saves real work.

## Query log

Run 2026-10-03 from `instance-20260717-0947`, all commands captured in
`sessions/2026-10-03-028-run-the-knitting-candidate-s-remaining-k/commands.log`.
Bodies were hashed at retrieval; the sha256 prefixes printed by each run are in
that log.

| # | Backend | Query |
|---|---|---|
| 1 | DuckDuckGo HTML | `knitted fabric repair algorithm stitch` |
| 2 | DuckDuckGo HTML | `knitting machine automatic mend repair knitted fabric method` |
| 3 | DuckDuckGo HTML | `knitting software detect mistake in chart pattern before knitting error checker` |
| 4 | DuckDuckGo HTML | `"darning machine" knitwear history automatically repair knitted fabric` |
| 5 | Google Patents XHR | `q="mending" "knitted fabric" knitting machine` (22 results; later attempts 503) |
| 6 | Google Patents XHR | `q=title:mending+knitted`; `q=title:repair+knitted+fabric`; `q=mending+knitted+fabric+re-knit`; `q=knitted+fabric+damage+repair+reconstruction` |
| 7 | OpenAlex | `knitted fabric repair algorithm`; `knit graph repair algorithm unravelling ladder`; `unravelling repair knitted structure graph planning intervention` |
| 8 | OpenAlex | `repair planning graph transformation sequence`; `consistency repair closure minimal deletion database`; `physical repair fabrication error 3D print planning`; `textile repair robot reknitting automation` (0 results); `re-knitting defect knitted fabric reconstruction` |
| 9 | OpenAlex | `KnitPick KnitPicking Texture programming modifying knitted textures` |
| 10 | OpenAlex (by DOI) | `10.1145/3332165.3347886`, `10.1038/s41467-024-46498-z` |
| 11 | Crossref | `GenProg Genetic Programming Based Automated Program Repair`; `Consistency and repair Arenas Bonchi Perez`; `Repairing 3D prints physical repair` |
| 12 | Semantic Scholar | `GenProg automated program repair`; `repair programs sequence of operations consistent query answering`; `physical repair of 3D printed objects fabrication errors` — all HTTP 429, no data used |
| 13 | arXiv API | `ti:"laddering" AND all:"knitted"` |
| 14 | GitHub repo API | `knitting repair planner`; `knit graph repair`; `knit stitch repair algorithm`; `knitting error correction`; `knitting fix mistakes`; `knit repair`; `knit graph`; `knitting computer`; `knit chart` |
| 15 | Direct fetch | `github.com/mhofmann-Khoury/knit_graph`, `knittingfix.com`, `envisioknit.com` manual, `patents.google.com/patent/US1845516A/en` (503) |

## Limits of this check

- **Not exhaustive.** No patent full text, no non-English sources, no forum
  corpus, no books, no citation-graph traversal. Absence of a hit is not
  originality; that is why the verdict labels reading A `inferred`.
- **Two search engines misbehaved here.** Bing's RSS interface matched only the
  first query term and returned dictionary entries, so it was discarded; Google
  Patents rate-limited this host after five requests, so no patent page was
  opened and only identifiers are recorded; Semantic Scholar returned 429
  throughout. OpenAlex, Crossref, arXiv, GitHub and DuckDuckGo worked.
- **Six CS papers were read by title and metadata only.** The judgement that
  reading B is "decisive" rests on the mechanism being recognisable from those
  titles plus this repository's own admission in T-0011, not on six full texts.
- **Commercial claims were not tested.** KnittingFix's "2,400+ knitters helped"
  and accuracy claims are marketing; no product was used.
- **Two "best knitting software 2026" listicles** appeared in results and were
  discarded as SEO content; no fact here rests on them.
- **No user evidence.** Nothing here says a knitter wants this, would pay, or
  could follow a plan. That remains the untested half of Stage B.