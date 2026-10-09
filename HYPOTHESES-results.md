<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Hypotheses — experiment results

What each experiment returned, with its numbers, its classification, and what it
does not cover. The live candidate list, their predeclared kill gates, and the
witnesses are in [`HYPOTHESES.md`](HYPOTHESES.md); negative results are in
[`FAILURES.md`](FAILURES.md).

**The invariant that makes the split sensible.** A hypothesis says what would
have to be true and what would end it; a result says what happened. They are read
at different moments — the first before an experiment, the second after — and
merging them made this file exceed its line cap while adding an outcome.

## The one experiment that has run

### E001 — Is a plain checksum baseline sufficient?

**Claim under test.** The published four-image photo-migration failure requires a
relationship-aware mechanism to reveal its missing media.

**Kill gate (predeclared).** If checksum identity alone finds all missing media
described in the trace, without original/edit inference, the example establishes a
failure of importer reporting and **not** an advantage for a semantic auditor.

**Baseline.** The cheapest available: source-relative checksum set difference
between the Takeout fixture and the destination model implied by the published API
trace. No relationship inference, no importer-specific instrumentation.

**Controls.** Complete destination yields no missing identities; renamed identical
bytes yield no missing identities; accepted-operation model reproduces the reported
missing filenames; operation counts match; relationship-only damage with all
identities retained is invisible to the baseline.

**Result.** `observed`, 2026-10-03. The kill gate was met. The baseline recovered
the exact reported pair; all controls behaved as predicted. Artifacts:
`EXPERIMENTS/001-photo-baseline/results.json`, including the pinned source
revision and SHA-256 of every downloaded input.

**Conclusion.** `FAILURES.md` F001. The example does not support building the
verifier.

**Remaining uncertainty.** Whether relationship-only loss occurs in real archives
at a rate that matters; whether the importer bug still exists; whether users need a
standalone product at all.

**Reconsider when.** A real case is found in which all bytes survive and important
relationships do not, **and** the existing reporting does not already surface it.

## The information-sufficiency gate (E002, run 2026-10-03)

Before any candidate is implemented, two realities that give it identical
permitted inputs but require different outputs must be constructed. A passive
system fails this gate outright; an active system fails only if no permitted
observation separates the pair. Experiment `EXPERIMENTS/003-information-sufficiency/`
runs one small synthetic witness per held candidate. All inputs are synthetic;
the witness can falsify an unbounded claim but measures no prevalence.

| Witness | Candidate | Result | Consequence |
|---|---|---|---|
| W1 | Decision-directed sidewalk survey | **Survives** (`observed`) | The mechanism is not structurally information-insufficient given known OD pairs; the A1 masking experiment supplies the measured comparison |
| W2 | Knitting repair planner | **Spec was insufficient; repaired** (`observed`) | The original input set omitted loop orientation (F007); adding mount makes the two realities distinguishable (T-0009) |
| W3 | Adaptive ventilation measurement | **Survives** (`observed`) | An ordinary permitted action (`co-locate`, `close-internal-door`) separates two realities whose passive traces coincide within noise |

Full claim, oracle, and limits per witness:
[`EXPERIMENTS/003-information-sufficiency/README.md`](EXPERIMENTS/003-information-sufficiency/README.md).

**W2 finding.** `observed`, 2026-10-03. Two stitch states with identical
chart-level inputs (same symbols, connectivity, live stitches, and facing side)
require different repairs because one is mounted twisted and the other is not.
Mount is not in the candidate's stated input set, so the planner cannot choose
between "re-form in place" and "re-form and untwist" from its permitted input.
This is not a refutation of the mechanism: a knitter can observe orientation, so
the fix is to add orientation to the input (or refuse). It bounds the input and
rules out the current, narrower claim. Recorded as `FAILURES.md` F007.

**W2 repair (T-0009).** `observed`, 2026-10-03. Adding each loop's mount to the
input distinguishes the two realities: the witness reports `silent_pair_found`
`true → false` and `permitted_encoding_can_represent_the_difference`
`false → true`. The specification is now sufficient for the decision; the
algorithmic-advantage question is untouched and awaits the Stage-A planner
comparison.

**W2 Stage-A comparison (T-0010, `EXPERIMENTS/004-knitting-stage-a/`).**
`observed`, 2026-10-03. The candidate's cheap local heuristic and an
exhaustive minimum-cost oracle agree on 8/9 solvable synthetic cases and the
heuristic is valid (never misses an error, never emits an illegal closure) on
all 9; it refuses the unsupported-shaping case. It is suboptimal on the
deliberately constructed `same_column_stack_4x4` shared-release case (local 5
vs. optimum 3): the per-error rule cannot see that one release covers two
errors. No full-row-release degeneration, no missing action sequence, no
silent acceptance. Verdict `narrow`, not `abandon` — recorded in the
experiment README; next test is a bounded-neighbourhood planner against the
same oracle before any Stage-B physical work.

**W2 Stage-A follow-up (T-0011, `EXPERIMENTS/005-knitting-bounded-search/`).**
`observed`, 2026-10-03. The bounded-neighbourhood planner — group errors whose
release closures intersect, take each group's minimum-cost local plan, charge the
union of the releases once — is **valid and cost-identical to the exhaustive
optimum on 115/115 checked cases** (116/116 with the opt-in `--slow` oracle), on
both the development and the holdout fixture seed and at every patch cost swept,
and it **refuses** both unsupported states. 004's per-error rule is optimal on
85/115 of the same cases. The decomposition's per-chunk costs were separable on
every case, which is the mechanism the design predicts, so this checks that the
implementation matches its design rather than discovering anything. Two limits
matter more than the headline: any *cheaper* setting is suboptimal (chunk cap 1
fails on 20/115, fourteen of them holdout cases; cap 3 on 2 holdout cases), and two
settings that look optimal (`cap=1, beam=2`, `cap=2, beam=4`) enumerate exactly
the oracle's own search space and are exhaustive search in disguise. On T-0010's
own fixtures the bounded planner does **1.28x more** work than the oracle; the
saving appears only where closures fragment. Verdict: the Stage-A planner question
is **answered at the mechanism level** — narrow, not abandoned — and the
candidate's remaining gate is prior art plus unperformed Stage-B physical work,
not more synthetic planner search. Recorded in `DECISIONS-PRACTICE.md` D021.

**W2 prior-art check (T-0015, `RESEARCH/PRIOR-ART-KNITTING.md`).**
`observed` for what was retrieved, `inferred` for the judgement. The kill gate's
prior-art condition conflates two claims, and the report separates them. **The
domain condition is not met:** no tool, paper, repository or patent was found
that supplies an ordered, checkable intervention sequence for a structure
someone has already knitted by hand — KnitPick (UIST 2019) and `knit_graph`
provide the graph layer, EnvisioKnit's Chart Checker catches unknittable charts
*before* knitting, KnittingFix diagnoses from photos, and the 1929–1953
mending-machine patents show the physical capability existed as hardware. **The
novelty condition is met and decisive:** computing a minimum-cost set of
interventions under constraints, decomposed over neighbourhoods that cannot
interact, is established work from 2007 to 2026 (optimal repairs for functional
dependencies, repair *programs* as ordered operation sequences, graph repair
ranking). T-0011 had already recorded that its own optimality follows from the
model's structure.

**Consequence.** The algorithmic-advantage claim is abandoned (`FAILURES.md`
F009); no third synthetic planner experiment is warranted. What survives is a
craft-tool question — would a knitter follow a generated plan and save real
work — which is Stage B, needs an experienced knitter and authorization, and
cannot run in this repository.

**W1 and W3.** `observed`, 2026-10-03. No silent pair was found within the
permitted input set: in each case an askable observation separates the realities,
so next-observation selection carries decision-relevant information. This is
`observed` for the witness construction and `inferred` for the wider claim; it
does not measure usefulness, differentiation, or adoption, and one construction
cannot exclude a different silent pair.

**W3 measured (T-0014, `EXPERIMENTS/006-ventilation-measurement-design/`).**
`observed`, 2026-10-03. The witness says an askable observation separates the
realities; the experiment asked the follow-up question, which the witness cannot
answer: does *choosing* that observation beat *being told* one? On 6 paired
hypothesis families whose passive trace in the measured room is identical by
construction, with one shared fitter and an identical budget of 12 sample slots
and one decision, pairwise discrimination accuracy was passive 0.333 (chance),
prescribed door-open 0.833, adaptive 0.792. The predeclared gate required
adaptive to beat fixed and was **not met**, so the formulation is stopped. One
narrower observation survives: under poor mixing, reading a second sensor holds
0.708 where acting on the measured room drops to 0.542. Recorded as
`FAILURES.md` F008. **This is a failed claim, not a failed mechanism** — the
question of which hypotheses remain distinguishable is still answerable, and
this experiment only shows that the proposed advantage over a fixed protocol did
not appear.

## E3 — Build timestamps (census run 2026-10-03)

**Claim under test (`RESEARCH/E.md`, mechanism E3).** Embedded build timestamps
are the dominant, cheap-to-count determinism violation in Python packaging, so
they are worth fixing first.

**Kill gate (predeclared in `RESEARCH/E.md`).** Below 5% of sampled wheels with
non-normalised timestamps, E3 is a weak lead and the experiment ends.

**Result.** `observed`, 2026-10-03, T-0013,
`EXPERIMENTS/007-build-timestamps/`. 200 wheels over 200 distinct releases from
ten declared packages, every value read from the artifact, zero failures over
205 MB, reproduced identically on three consecutive runs. Gate metric 0.965
(95% CI 0.940–0.990) — the gate **passes at 19x**. Stricter fractions beside it:
0.670 of wheels carry two or more distinct entry dates, 0.535 span a minute or
more, 0.145 span an hour or more (the widest: 23 entries across 789 days). Zero
of 200 wheels carried a unix-epoch integer in `METADATA` or `RECORD`, so E3's
stated assumption that timestamps hide in embedded strings as well as zip
headers is **half false** on this population.

**Conclusion.** The gate is met and the mechanism is still `untested`. 0.965
measures that almost nobody pins the DOS epoch, not that 96.5% of wheels
are irreproducible because of timestamps; and nothing here rebuilds an artifact,
so no cause is assigned. Recorded as `FAILURES.md` F010 — the measurement was
inadequate, not the mechanism wrong. The prevalence is also not one ecosystem
rate: only `cryptography` ships 1980-normalised wheels (7 of 20, all
`win_amd64`), `urllib3` stamps every entry with one build instant, and `jinja2`
carries checkout mtimes.

**Attribution measured (T-0017, `EXPERIMENTS/008-build-timestamp-attribution/`).**
`observed`, 2026-10-03. Five pure-Python sdists, 35 real builds with setuptools
45.2.0 + wheel 0.34.2, two checkouts identical in content and 34 months apart in
mtime. Attribution is causal: rewriting only the four DOS bytes in each local
header and each central-directory entry of one artifact to the other's values.
With `SOURCE_DATE_EPOCH` unset, **398 of 398 differing bytes pooled lie inside
zip timestamp fields** and the patch reproduces the other artifact exactly on
5 of 5 sources, so timestamps were the only cause. With it set, builds are
bit-identical (0 differing bytes, 5 of 5). A second timestamp route was found and
identified: the `.dist-info` files the builder generates carry the wall clock, so
two builds across a 2-second DOS tick differ in exactly those entries.
Predeclared gate met: `timestamps-first`.

**Decision.** `FAILURES.md` F012. E3's ordering claim is **supported for this
builder** — fixing timestamps is sufficient, not merely worthwhile — and the
candidate is **abandoned anyway**, because the remedy is `SOURCE_DATE_EPOCH`, a
standard this builder already honours. The remaining gap is adoption, and
adoption of an existing standard is not a new repository. E1 and E2 are still
`untested`; **do not run E1** (D020, Screen 3). E2 is time-gated, not effort-
gated: two resolver runs today measure nothing, so snapshot one side of that
comparison while a VM is idle.

## E041 (041-need-index) — the need-similarity instrument and its premise

**E041 validated the instrument on a control E040 could not build, and the ceiling
resolves against the corpus** (`EXPERIMENTS/041-need-index/`). The positive control
needed **both members of a judged pair** inside one corpus, which Stack Overflow's
duplicate graph does not serve from here. GitHub does, unauthenticated:
`GET /search/issues` returns full issue bodies, and a repository captured completely
contains its own duplicates *and* the issues they name. **77 pairs, both members
present in a 44,669-row corpus** reconciled against the API's own `total_count`, no
synthetic near-copy anywhere in it.

**G1 and G3 pass, G2 fails, and G4's separation is confirmed for the first time.**
The instrument separates judged repeats from matched cross-repository controls by
**+0.740 [+0.636, +0.831]** on titles and **+0.805 [+0.714, +0.883]** with body text
(the ratio form is `not_evaluated` — no control reached the frozen tau, which is a
third state per F067/D073, not a failure). But **the judged partner is the single most
similar row in the corpus only 0.390 of the time on titles and 0.143 with body text,
against a declared bar of 0.50**; median partner rank is **10th of 44,669**, and it is
**0 of 14** when the pair's titles share no content term. **Accuracy tracks pool size:
top-1 runs 0.706 at a 198-row pool and 0.083 at 8,315.** Applied unchanged to E040's own
arms, the instrument separates needs from their matched controls at **3.9× at tau=0.15
and 27.2× at tau=0.20** — the first independent confirmation of E040's G1 — and that
separation is a much weaker property than *this is the same need*.

**And the premise of item 0f is arithmetically false.** E041 re-ran arm A at a ladder of
corpus sizes with the instrument held constant, refusing to report unless it first
reproduced E040's own recorded G4 counts from E040's bytes (it did). **`alpha = 0.971`,
CI95 [0.632, 1.717]: resolution grows linearly, not super-linearly**, so the bar of 20
needs `n ≈ 3,500` — a 2.5× corpus, not a second venue — and every stricter threshold is
*worse* (`alpha` 0.346 at tau=0.20, 0.111 at tau=0.25). **Arm B yields 4 qualifying
clusters against arm A's 8**, so half the headline number is matched by its own control
and growing the corpus grows both. **Item 0f closes on its own arithmetic (D073).**

**What is closed and what is not.** Closed: the need corpus as an indexable signal, on
measured grounds for the third time and now on the instrument itself rather than on
resolution alone. **Not closed:** that a needs index built on a *different* instrument —
embeddings, a domain model, human review of a shortlist — is impossible. What this
establishes is that **the instrument this repository measured nine results through
cannot pick out a repeat a human identified**, and that the population it would index
does not densify with size. The finding is about a TF-IDF cosine over unigrams and
bigrams, and about that population.

## E065 — view-count measurement prototype result

**Result:** `untested`, 2026-10-08

**Gate evaluation:**

- **G1:** FAIL — only 10/30 treatment and 0/30 control statements yielded non-error web search results via DuckDuckGo. Route not measurable at this cost.
- **G2:** Not evaluable in pilot — requires separately labelled seeded control statements with known served/unserved labels.
- **G3:** FAIL — could not compute fraction classified as served with Wilson CI95 over ≥ 30 non-error rows per arm.
- **G4:** FAIL — only 6 of 20 top-arrival treatment statements classified as served/partial.

**Conclusion:** Web search via DuckDuckGo with need_text-as-query cannot recover -like arrival metrics for the tested needStatement corpora (DIY/home improvement needs from E062 and HN need-stating rows from E063). The principle requires platform-specific API access, as E062 used Stack Exchange API and E039 used Hacker News API.

**This closes the web-search-based operationalization route for these populations.**
