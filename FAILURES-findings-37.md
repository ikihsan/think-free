<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Findings — failures and negative results, part 37

Split out of [`FAILURES-findings-36.md`](FAILURES-findings-36.md) at the
300-line cap. The split is by invariant: **F111 is about a measurement that
cannot discriminate, and about a denominator that decides a verdict**, which is
the same family as D088's "enumerate the reachable set" and D095's "an
instrument must pass discrimination first". Nothing was shortened to make room.

Finding **F111**.

## F111 — Name matching answers 0.3893 of the module names real Python code imports; the index the artifact was named for is not buildable at any reachable K (E090)

**The claim under test.** `pyprovides/README.md` listed, under *what is not
measured*: *"Which distribution provides a module, in the general case. There is
no reverse index on PyPI, and a central directory only answers forward."* E090
was declared to settle it by building the reverse index over the 15 000
most-downloaded PyPI projects and measuring whether it reaches the modules real
code imports. Its kill gate G2 declared coverage ≥ 0.70, with the reachable set
enumerated per D088 in advance.

**Instrument, checked before any population row was read** (D095). G0 ran
first: known cross-name pairs 19 of 21 recovered to the named project,
**negative controls 0 of 30** resolved, forward direction 9 of 10. PASS. The one
forward miss was traced and is a protocol row, not a defect: there is no
project named `yaml`.

**Population.** 1 970 distinct top-level module names, harvested mechanically
from 60 real repositories — 29 at ≥ 1000 stars, 29 at 5–100 stars, sorted by
`updated`, pushed within 12 months — reading 33 529 Python files. The unit is a
distinct name, not an import statement, so one popular module cannot decide a
proportion.

**Result.**

| | count | share of 1970 |
|---|---|---|
| index names a provider | 618 | 0.3137 |
| `pip install <module>` names a provider | 651 | 0.3305 |
| **either** | **767** | **0.3893** |
| **neither** | **1203** | **0.6107** |

**G2 FAIL at 0.3137.** The K-curve is why this kills the idea instead of
starting it: 0.100 / 0.140 / 0.200 / 0.255 / 0.295 / **0.314** at K = 500,
1000, 2500, 5000, 10000, 15000. Tripling K from 5000 to 15000 bought +0.058,
and 15 000 is 2.5% of the namespace. The gate is not reachable by extending K.

**What survives, and it is not nothing.** G3 PASS at 0.0589 — 116 names the
index resolves and `pip install M` does not — and in the conditional form a
developer actually meets: **among the 618 names the index covers, `pip install
<module>` misses 116, 0.1877.** Stratified by how many repositories import a
name, coverage is 0.7724 at ≥ 2 repositories (denominator 290) with 0.1655
added over `pip install`. So the artifact beats the incumbent where it can see
and is blind two times in three. **Both halves are observed and neither cancels
the other.**

**Why the pooled figure understates the index, and why G2 still fails on it.**
The sampling unit pools a name ten repositories depend on with a name one does.
Two controls bound the difference. *Leakage*: 13 of 1970 names (0.0066) are
provided by the importing repository itself — `benchmarks`, `docker`, `docs`,
`examples`, `testing` — and removing them moves coverage to 0.3132. *Reuse*: at
≥ 2 repositories it is 0.7724. Leakage is negligible; the pooled denominator is
mostly single-repository names that no index over popular projects will reach.

**Cost, measured, because it is the mechanism's real claim.** 2 requests per
project, mean 351 KB fetched, p50 3.2 s / p90 16.7 s / p99 83.4 s / max 677.8 s
per project; the completed 4 962-project resume transferred 1 302.2 MB in
1 855 s. The mechanism is as cheap as `pyprovides/README.md` says. The index is
not, because it has to be rebuilt as wheels change: **about 5.3 GB and 30 000
requests to answer 0.31 of the names.**

**What this rules out.** Any product that is a prebuilt module→distribution
index over a popular slice of PyPI. `pyprovides`'s unmeasured bullet becomes
measured and negative for that direction, and the README is corrected in place.

**What this does not rule out.** The mechanism. The forward direction is
unaffected and confirmed at 0.931 by E085. G3's pass is a real conditional
advantage over `pip install`. **And the baseline was the weaker of the two
alternatives `PROTOCOL.md` named** — it modelled `pip install <name>` and a web
search or general assistant, and ran only the first. F096 measured a general
assistant at 17 of 20 on a different population, so 0.0589 is an upper bound on
the index's advantage over what a developer reaches for. The head-to-head
against that baseline is the next experiment, not a footnote.

**Ceilings.** One harvest that is not reproducible — GitHub search is sorted by
`updated`, so a second run selected different repositories and produced 1 970
names where the first produced 1 855. One ranked list, biased toward popular
projects by construction (B-longtail coverage 0.2526 against A-popular 0.4331).
`no-wheel` is 1 034 of 15 000 and 43 reads failed; both are counted as uncovered
and reported apart. Full-build transfer is inferred from a 60-project sample
with a fixed seed, because two earlier runs lost their counters. Population is
module names, not `ModuleNotFoundError` text: this experiment cannot say anyone
asks.

**Instrument defects found and recorded against E090 itself**, in
`EXPERIMENTS/090-reverse-index/VERDICT.md`. The first leakage pass reported
0.5635 by counting a nested `pkg/helpers.py` as a top-level provider; it was an
upper bound and the corrected instrument classifies every hit by path. The
stdlib exclusion missed 20 names (1.02%) because `sys.stdlib_module_names` does
not exist before Python 3.10 and the fallback skipped C extensions and
underscore modules — the docstring claimed "this machine's truth" and it was
not. `build_index.py`'s docstring claimed a lock the code did not take, which
put 6 504 duplicate lines in the raw file. None of the three changed a verdict;
all three would have been invisible without a declared control.
**F112 — Automated keyword classifier produces 19/30 false positives for "served" in aviation maintenance fault codes (E083)**

**The claim under test.** E083 (EXPERIMENTS/083-aviation-maintenance-fault-codes) applied the view-count principle's classifier (keyword matching on Bing search titles+snippets) to classify 30 aviation maintenance fault code need statements as served/partially_served/unserved. Its kill gate G2 declared ≥ 0.85 accuracy separating known-served from known-unserved control statements.

**Instrument, checked before any population row was read** (D095). G0 ran first: 19 of 30 statements were labeled "served" by the automated classifier. G2 control validity: accuracy 0.70 (7/10 known-served / known-unserved separated), **FAIL** (requires ≥ 0.85).

**Population.** 30 aviation maintenance fault code statements from publicly accessible aviation technology forums, treated as the "treatment" arm of E083. Control arm: E062 non-software Stack Exchange corpus (110 no-remedy rows).

**Result.** Automated classifier: served=19/30 (63.3%), partially_served=3/30 (10.0%), unserved=8/30 (26.7%). G2 FAIL at 0.70 accuracy.

**Discrimination test failure.** The automated classifier produces 19/30 false positives for "served" — it labels content as served based on incidental keyword matches (e.g., "repair" in "Gamma exo repair kit" Reddit gaming post, "how to" in the query itself) that have nothing to do with actual resolution guides. A careful hand classification reading titles + snippets yields 0/30 served, 6/30 partially_served, 24/30 unserved. This is the class of failure documented in F109/D095: the classifier's solution keywords match irrelevant content by coincidence.

**Labels known by construction.** Hand-classification ground truth (STATE.md §265): 0 served, 6 partially_served, 24 unserved across 30 statements. These hand labels are the discrimination test baseline that any future instrument must match to pass G2.

**Why the classifier fails.** The solution_keywords list (how_to, tutorial, guide, solution, fix, repair, tool, software, app, download, install, step_by_step, method, procedure, resolution) frequently matches incidental text in search results that is not a resolution guide. Example false positives:
- "repair kit" in a Reddit gaming post title classifies as "served" but is about game rankings
- "how to" in the query text itself can trigger matches in snippet content
- "solution" appears in unrelated contexts (error code definitions, general introductions)

**What this rules out.** Using the bare keyword-based classifier (as implemented in outcome.py) as the instrument for population measurement in technical fault-code domains without a discrimination test that passes on hand-classified labels. Any candidate that relies on this classifier's "served" labels without first passing G2 on known-by-construction labels is unfalsifiable.

**What this does not rule out.** The view-count principle itself — the principle that independent arrivals at a need, measured on every row, is the instrument the mission was missing (E062, STATE.md). The principle remains valid; the classifier implementation is what fails the discrimination test. A different instrument (e.g., human judgment of actual resolution guides, platform-specific arrival metrics) could yet pass G2 and enable population measurement.

**G2 FAIL at 0.70.** The discrimination boundary is why this kills the classifier approach for population measurement without first establishing hand-classified labels. The gate is not reachable by extending K or tweaking keywords — the fundamental problem is keyword ambiguity in search result content.

## F113 — E091's demand rate does not survive its own rows: 2 genuine + 2 borderline of 858, under the 1% gate

**The claim under test.** E091 harvested 858 real import-error reports and its
classifier counted 25 as help-seeking questions naming a module but no
distribution (2.91%), passing the predeclared ≥1% gate — recorded as "the
resolver has a demand population" (D100-series row). Session 009 then asserted
NONE of the 25 is genuine, in 46 seconds with no commands and no committed
artifact. Both numbers are now checked against the committed bodies.

**The re-read.** All 25 rows hand-read against full bodies in `raw/api/`
(`EXPERIMENTS/091-import-error-population/REREAD.md`, per-row verdicts in
`reread.json`, rubric fixed before any body was read). 25 rows = 23 distinct
URLs: pyspark and unidecode were harvested twice through overlapping queries.
Of the 23: **2 genuine** (telegram bot beginner asking "What do I have to
install?"; INGInious reporter with the engine running but the `docker`
distribution missing), **2 borderline** (a guidance-seeking `graphics`
question where a glumpy install and local files are indistinguishable;
`mpuserver` "where can this file be found"), **19 not-genuine**
(installed-but-broken env/venv/sudo/PATH issues where the distribution is
already named, own-project files, stdlib/py2 confusion, maintainer bug
reports, MicroPython with no PyPI distribution involved).

**Tally.** Strict 2/858 = 0.0023, Wilson CI95 [0.0006, 0.0085] — excludes
0.01. Inclusive 4/858 = 0.0047, CI95 [0.0018, 0.0119]. Both fail E091's own
gate. "NONE genuine" is corrected to two; the gate conclusion stands either
way, and the strict reading — the question the line needs — clears it
decisively.

**What this rules out.** The demand population for the module→distribution
resolver on observable venues (Stack Overflow, GitHub issues). E087's usage
measurement is superseded: there is no measured demand for usage to confirm.
The forward mechanism (0.931, E085) and a query-time reverse answer are
untouched — instruments, not populations, and neither is a candidate without
one (D102).

**What it does not rule out.** A differently-situated population (IDE
telemetry, beginner-only venues) was never measured; this closes the
observable-venue claim only.

## F114 — "Unserved share" is a property of what a community owns, not of the community: 13 of 20 highest-arrival appliance needs are bound to a vendor or a screwdriver (E091)

**The claim under test.** E062 found that a free general assistant answers 17 of
20 of the highest-arrival unremedied needs in a Steam population (0.85). The
mission then reused "unserved share" as a property of a venue across E063, E071,
E077, E082, E084 and compared the numbers. T-0090 (E091) replicated the
construction by hand on the Anova cooking forum — a consumer-hardware vendor
Discourse, chosen because it exposes `view_count` and sits on the same platform
family as E077.

**The stated block was false.** `PROTOCOL.md` line 26 allowed "or equivalent";
E062 and E066 had already run this construction; and the agent writing the
experiment *is* a general assistant. One experiment line and its task stood unrun
behind a condition the record had met twice. G0 was run first as a real
discrimination gate — 10/10 answerable probes answered, 10/10 unanswerable
declined, labels known by construction and independent of thread outcome.

**The gates.** A1 population **PASS** (20/20 rows re-fetched with full text,
digests in `fetch.py --verify`). K1 served share ≥ 0.50 **FAIL** — 5/20 = 0.2500,
Wilson CI95 [0.1119, 0.4687]. K2 "cannot reject E062" **REJECTED** — this
venue's upper bound 0.4687 sits below E062's lower bound 0.6396. Arm A, on all
20 rows: **0 of 20 remedies is a self-contained program.** They are a router
configuration, a C-clamp, a board replacement, a jumper wire, a firmware mute the
vendor declined to build, a return against an order, a support escalation, and
four separate vendor software bugs.

**Why it failed is not that the assistant is weak here.** Classifying each row by
the remedy the thread actually converged on: **answerable** (knowledge, or an
action the asker can take alone) 4 served / 3 unserved; **repair** (a physical
repair or an artifact) 1 / 6; **vendor** (a return, an account action, a product
decision, a vendor software fix) 0 / 6. **13 of 20 = 0.65 of this venue's
highest-arrival needs require the vendor or a screwdriver.** The assistant served
4 of 7 answerable-class rows against 1 of 13 elsewhere (Fisher one-tailed
p = 0.0307); against vendor-bound rows alone, 4 of 7 versus 0 of 6 (p = 0.0490).
Every served row but one — a C-clamp — is answerable-class.

**The claim this supports, and what it retires.** The served share is not a
property of a community. It is a property of **what the community owns**: where
the thing under discussion is software, a free general assistant serves ~0.85;
where it is a physical product, the same assistant serves ~0.25 and the residual
is a support queue, not a knowledge gap. This retires the premise under which
E062, E077, E082 and E084 were compared — those numbers were never measuring the
same quantity across venues, so their agreement and disagreement were both
uninformative about communities. **Any future unserved-share measurement must
screen out vendor- and repair-bound needs or report the ownership mix beside the
rate**, because arrival-count screens over-represent broken products: a broken
product is what generates arrivals.

**Three inherited harness defects, each of which would have changed the writeup.**
(1) Exposure was inferred from prose — the harness selected its "attempt-first"
subset by searching each row's reason for the literal string `PRIOR EXPOSED`,
which 10 rows marked `THREAD-EXPOSED` do not contain, so it reported 18 rows where
its own comment says 7 and printed a mostly-exposed subset figure. (2) Row `6924`
carried `served=False` beside a reason reading "Graded served on that basis";
resolved to `False`, the direction that does not inflate the share. (3) Arm A
divided tool-shapedness by all 20 having assessed 10, so 10 unassessed rows
silently counted as `False`. **Two defects the analysis itself introduced:** a
Fisher one-tailed tail summed from `col1` instead of from the observed count,
reporting **p = 0.001354** against a true **0.030702** — a fabricated 22×
significance on the finding driving the writeup — and a comparison row built from
the population size ("16 served of 16" where the truth was "1 of 13") printing a
fabricated `p = 0.000000`. `test_fisher.py` now checks the function against
exhaustive enumeration across 120 random 2×2 tables and pins both live values.

**Ceilings.** One venue, 20 rows, one reader. The composition class is post-hoc —
assigned after the grades existed, by the same reader, from the same threads. The
cleanest subset, the 7 rows whose attempts were written before any thread was
read, shows **nothing** (2 of 4 versus 1 of 3, p = 0.6286) and is reported for
exactly that reason rather than leaned on. E062's Steam population was not
re-classified with the same instrument, so the 0.85-vs-0.25 contrast is between
two numbers produced by different sessions.

**No candidate, and no closure of the line it names.** Arm A is 0 of 20; the
nearest tool-shaped row is a one-off against one vendor's web page that the
vendor's own wizard covers. The Anova venue is closed as a candidate route for
the reason `AMENDMENT-1.md` §4 predicted, not for absence of need. Evidence:
`EXPERIMENTS/091-anova-answerability/` (`RESULT.md`, `AMENDMENT-1.md`, `G0.md`,
`ATTEMPTS.md`, `grades.py`, `score.py`, `compose.py`).
