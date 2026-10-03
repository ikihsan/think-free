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

## F010 — E3's predeclared timestamp gate is near-vacuous: prevalence measured, attribution not

Source: `EXPERIMENTS/007-build-timestamps/`, T-0013, following the kill gate
declared in `RESEARCH/E.md` mechanism E3.

**Observation.** E3 claims embedded build timestamps are the cheapest
determinism violation to count and therefore the cheapest to fix first. Its
predeclared experiment counts the fraction of 200 recent PyPI wheels with
"non-normalized" zip entry dates, and ends E3 below 5%.

**Experiment.** 200 wheels, one per release, from ten declared packages; the 20
most recently uploaded wheel releases per package, smallest wheel per release,
distinct releases enforced. Every value read from the artifact: each
`ZipInfo.date_time` in the zip, plus a scan of `METADATA` and `RECORD` for
unix-epoch integers. Zero failures over 205,305,241 bytes. Numbers reproduced
identically on three consecutive runs.

**Result.** `observed`, 2026-10-03. Gate metric 0.965 (95% CI 0.940–0.990)
against a 0.05 threshold, so the gate **passes at 19x**. Stricter fractions,
reported but not used to overrule the stated gate: 0.670 of wheels carry two or
more distinct entry dates, 0.535 span at least a minute, 0.145 span at least an
hour, and the widest is `requests-2.26.0-py2.py3-none-any.whl` at 23 entries
spanning 789 days. Zero of 200 wheels carried a unix-epoch integer in
`METADATA` or `RECORD`.

**Conclusion.** The gate passes, and passing it means very little. 1980-01-01
appears in a wheel only when the DOS epoch is *pinned*, which almost no builder
does; a builder that honours `SOURCE_DATE_EPOCH` with a real commit time still
produces non-1980 dates. So 0.965 mostly says "nobody pins the DOS epoch". The
measurement establishes **prevalence** and says nothing about **attribution**:
nothing here rebuilds an artifact, so no cause is assigned to a byte difference.
The second half of E3's own experiment — build the same source under two epochs
and attribute the difference — was not performed. E3's load-bearing claim
("worth fixing *first*") remains `untested`; only its cheap gate is now spent.

**Classification.** The measurement was inadequate, not the mechanism wrong. The
gate is met and should not be re-run in this form; the fix is a different
measurement, recorded as **T-0017**
(`EXPERIMENTS/008-build-timestamp-attribution/`).

**Limits.** Ten hand-picked packages, mostly pure-Python or source-heavy, sampled
from release history rather than downloads; it bounds nothing about npm, conda,
or Maven, and nothing about a user-weighted sample. Zip dates have 2-second
resolution, so the 27 wheels spanning under a minute are neither evidence nor
counter-evidence. Prevalence of a *detectable timestamp* is not prevalence of a
*reproducibility failure*: `diffoscope` and `reprotest` attribute diffs per
cause and nothing here does. An earlier run of the same census with a weaker
selection rule returned 0.975 / 0.69 / 0.245 against 0.965 / 0.67 / 0.145, so
the verdict is not an artefact of sampling.

**Lesson.** A kill gate should be written so that a plausible world fails it.
E3's threshold was 5% against a metric that only a builder pinning the DOS epoch
to 1980 can pass; the gate could have been met by any ecosystem-wide turn of
policy that changed nothing about reproducibility. The heterogeneity is the
real finding — only `cryptography` ships 1980-normalised wheels (7 of 20, all
`win_amd64`), and `urllib3` stamps every entry with one build instant while
`jinja2` carries checkout mtimes — which means "the" ecosystem-wide rate is not
even well defined. The same shape of near-vacuous gate appeared in F008.
