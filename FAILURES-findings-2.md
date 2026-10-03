<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures — recorded findings, part 2 (F009 onwards)

Continues [`FAILURES-findings.md`](FAILURES-findings.md), which holds F001–F008
and reached the 300-line cap at F008. Continues into
[`FAILURES-findings-3.md`](FAILURES-findings-3.md) at F013. **Identifiers are
stable across the files**: a reference to `F008` means the same entry wherever
it appears, and so does `F009` or `F013`. New findings are appended to part 3.

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

## F011 — `sync land` broke on git ≥ 2.26, and 60 CI runs failed for that reason

Source: T-0016, `.github/workflows/ci.yml`,
`tools/originlib/sync.py`, `tests/test_sync.py`.

**What happened.** All 60 recorded CI runs failed, every one at the `Tests`
step. The step's log could not be downloaded — that needs repository admin
rights — and the only error text the code produced was `rebase could not be
completed; run 'git rebase --abort'`, which names a remedy but no cause. So
nothing in the repository said which test failed or why, for nine hours of
pushes.

**Diagnosis.** Two changes made the failure legible, then a reproduction made it
explainable. The workflow now re-emits each failing test as an `::error::`
annotation, which GitHub's public check-run API returns without credentials: the
failing test was `test_land_resolves_generated_index_conflicts_by_regenerating`.
That test failed only on a modern git, so git 2.56.0 was installed locally
(micromamba, conda-forge) and the suite was re-run against it. Two defects, both
assumptions about an older git:

1. **`git rebase --continue` is interactive from git 2.26.** It opens an editor
   for the commit message. `land` called it bare. On a VM whose stdin is an
   inherited pipe it blocked until the 60-second timeout; on a CI runner with no
   editor it failed immediately, leaving `REBASE_HEAD` behind and producing the
   error above.
2. **`REBASE_HEAD` no longer means "a rebase is waiting".** The merge backend
   leaves that pseudoref behind after a *successful* rebase, so the check
   reported failure immediately after the rebase had completed. The module
   already had the correct predicate — `rebase_in_progress`, which looks for
   `rebase-merge`/`rebase-apply` — and `land` had used the wrong signal.

**Consequence.** Not a test-suite problem. `origin sync land` — the one
operation D017 makes responsible for moving work onto the shared branch — could
not land on any VM whose git is 2.26 or newer, in exactly the case two VMs had
regenerated the same generated index. The dev machine recorded git 2.55.0 in
`EXPERIMENTS/000-capabilities/`, so the fleet's own capability record said the
dangerous version was already in use. Every VM that avoided the failure avoided
it by not colliding, which is luck, not a guarantee.

**Fix.** `gitutil.run` takes an `env` override; `land` continues the rebase with
`GIT_EDITOR=true`, `GIT_SEQUENCE_EDITOR=true`, `GIT_MERGE_AUTOEDIT=no`, which
outranks anything the VM exports (`-c core.editor=true` would not have: an
environment variable wins over configuration). `land` decides "rebase still
running" with `rebase_in_progress`. Failures now quote git's own first line
through the new `gitutil.detail`, so the next one needs no log download. Tests:
`test_land_never_opens_an_editor_to_continue_a_rebase` fails on git 2.56 without
the fix (verified by reverting it) and passes with it; the full suite is green
on git 2.25.1 and on git 2.56.0.

**Classification.** Tooling defect, found by reading CI's public annotations
rather than by a local gate. Both halves of it were untested assumptions about a
third-party program's behaviour on a version the repository had never exercised.

**Lesson kept.** A test suite that only ever runs on the developer's machine
cannot fail for the reason CI fails. The defect was in the one operation the
whole multi-VM contract depends on, and 60 red runs did not localise it because
the evidence needed credentials. The two changes that mattered were both about
*legibility*: emit failures where anyone can read them, and say what git said.

## F012 — E3's ordering claim holds, and that is why there is nothing to build

Source: `EXPERIMENTS/008-build-timestamp-attribution/`, T-0017, completing the
experiment declared in `RESEARCH/E.md`.

**Observation.** F010 recorded E3's declared census gate as near-vacuous: 0.965 of
200 recent PyPI wheels carry a non-1980 entry date, which measures whether a
builder pins the DOS epoch rather than whether a build is reproducible. The half
that was missing is the one E3's mechanism section actually names: build the same
source twice under different `SOURCE_DATE_EPOCH` values and attribute the byte
difference.

**Experiment.** Five pure-Python sdists (`six`, `toml`, `idna`, `packaging`,
`click`), each extracted into five checkouts, 35 real `setup.py bdist_wheel`
builds with setuptools 45.2.0 + wheel 0.34.2. Two checkouts are byte-identical in
content and 34 months apart in mtime. Attribution is **causal**, not
correlational: rewrite only the four DOS bytes in each local file header and the
four in each central-directory entry of artifact A to artifact B's values, and
check whether A becomes B.

**Result.** `observed`, 2026-10-03. In the epoch-unset arm, 398 of 398 differing
bytes pooled lie inside zip timestamp fields and the causal patch reproduces the
other artifact exactly on 5 of 5 sources — so timestamps were the *only* cause.
In the epoch-set arm, builds are bit-identical: 0 differing bytes on 5 of 5. The
noise floor was non-zero on three sources and the cause is a second timestamp
route, not a second kind of cause: the `.dist-info` files the builder generates
carry the wall clock, and DOS timestamps have 2-second resolution, so two builds
across a tick differ in exactly those entries. Controls: patching one header half
does not reach identity (5 of 5), and a planted content defect inside a packaged
file is attributed to `content-differs` (5 of 5). Predeclared gate met —
`timestamps-first`.

**Conclusion.** E3's ordering claim is **supported for this builder**: fixing
timestamps is sufficient for bit-reproducibility, not merely worthwhile. The
candidate is nevertheless **abandoned**, because the remedy is
`SOURCE_DATE_EPOCH`, a documented standard this builder already honours and which
needs one environment variable. A tool that counts these violations duplicates
`diffoscope` and `reprotest`; a tool that fixes them duplicates the variable. The
gap the census measured is an *adoption* fact — 0.965 of recent wheels are not
pinned although the builder can pin them — and adoption of an existing standard
is not a new repository.

**Classification.** A supported mechanism and a failed candidate. E3 is the first
mechanism in this repository whose load-bearing claim survived a gate written
before the run; nothing was validated, because the honest reading of a mechanism
that turns out to be one environment variable is that there is no product here.

**Limits.** One builder (the only wheel builder on this machine), pure-Python
sources, five small single-repository packages, Linux, CPython 3.8.10. Compiled
extensions embed a toolchain the wheel builder does not control. The census's own
per-package table — `cryptography` ships 1980-pinned wheels, `urllib3` stamps one
instant, `jinja2` carries checkout mtimes — is unexplained by this run, and that
spread is the obvious next question rather than a settled one.

**Lesson.** A pass and a product are different outcomes. The gate asked whether
timestamps come first in the cause ordering and the answer was yes; the
candidate died *because* the answer was yes, since the thing that fixes it
already exists as a standard the builder implements. Ask what the pass implies
for building, not only what it implies about the claim.

**What would reopen it.** A builder or ecosystem where timestamps are **not** the
whole story — the census's heterogeneity suggests one exists — or a user-facing
failure that setting `SOURCE_DATE_EPOCH` does not solve. Either would need its own
predeclared gate; neither is this candidate.
