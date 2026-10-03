<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures — recorded findings, part 2 (F009 onwards)

Continues [`FAILURES-findings.md`](FAILURES-findings.md), which holds F001–F008
and reached the 300-line cap at F008. **Identifiers are stable across the two
files**: a reference to `F008` means the same entry wherever it appears, and so
does `F009`. New findings are appended here.

## F009 — The knitting planner's algorithmic advantage is prior art, not a gap

Source: `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015),
[`FAILURES.md`](FAILURES.md) kill-gate condition for the knitting candidate.

**Observation.** Stage A settled the mechanics: the bounded-neighbourhood
planner is valid and cost-identical to the exhaustive optimum on 116/116
solvable fixtures (T-0010, T-0011). That experiment explicitly refused to claim
novelty, noting that the decomposition is textbook separable optimisation over a
closure operator. The candidate's kill gate carried one untested condition:
"abandon the algorithmic-advantage claim if existing graph tooling already
supplies equivalent intervention sequences".

**What was run.** A prior-art check in the three vocabularies the skill
requires — the user's ("fix a knitting mistake", darning machines), the academic
("knit graph repair", "unravelling repair knitted structure"), and the
infrastructure one ("repair planning over graph transformation", "consistency
repair") — using DuckDuckGo HTML, OpenAlex, Crossref, the arXiv API, the GitHub
repository API, and one Google Patents query. Full query log, with what was and
was not read, is in the report.

**Result.** `observed` for retrieval, `inferred` for the judgement.

1. **The domain condition is not met.** Nothing found supplies an ordered,
   checkable intervention sequence for repairing an already-knitted hand-worked
   structure. Computational knitting (KnitPick 2019; Knit sketching 2021;
   KnitUI 2021; Wooly Graphs 2024) *generates* structures. Chart software
   (EnvisioKnit's Chart Checker) checks a chart before knitting. KnittingFix
   diagnoses from photos. Five 1929–1953 patents describe machines whose purpose
   was re-knitting a damaged region of existing fabric.
2. **The novelty condition is met.** Minimum-cost repair under constraints,
   decomposed over independent regions and emitted as an ordered sequence, is
   published work from 2007 to 2026 — optimal repairs for functional
   dependencies (TODS 2018), repair *programs* as ordered operation sequences
   (2007), repair of graph transformations ranked by weakest application
   conditions (LMCS 2026), rule-based graph repair without side effects (2024).
   Two targeted OpenAlex queries on the knitting-specific vocabulary returned
   nothing on the subject, and five GitHub repository-API queries returned
   `total_count: 0`.

**Conclusion.** The algorithmic-advantage claim is **disproved**. There is no
algorithmic contribution to defend: the mechanism is a standard constraint-repair
decomposition wearing a knitting dataset. This is F009 by the rule that a claim
which cannot be defended against its own field's prior art must not be carried.

**Classification.** A failed *claim*, not a failed candidate. The physical
question — whether a knitter follows a generated plan and saves real work — is
untested and untestable here. `RESEARCH/C.md`'s own abandon reason is untouched:
if supplying the patch already requires understanding the structure, the tool
serves only people who can already solve it.

**Limits.** One agent, one day, English-language sources, no patent full text
(Google Patents returned HTTP 503 after five requests, so only identifiers,
dates and claim snippets are recorded), no Chinese, Japanese or German
literature, no forum corpus, no books, no product used, no user contacted. Six
computer-science papers were seen by title and metadata only. The claim that
*no* repair planner exists anywhere is therefore `inferred`, not `observed`.

**What would reopen it.** A current machine-knitting product that mends knitwear
and publishes its intervention logic; a paper computing repair sequences over
knit graphs that this search missed; or a demonstration that a knitter follows
a generated plan and saves measurable work (Stage B).

**Lesson kept.** The graph layer was prior art (C.md), the algorithm was prior
art (here), and the hardware capability was prior art (the patents). What
remained was a report format and an unobserved user. That is the shape most
agent-generated candidates have, and it is cheaper to discover in a day of
searching than in weeks of building.