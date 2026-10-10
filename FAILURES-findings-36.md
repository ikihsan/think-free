<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Findings — failures and negative results, part 36

Split out of [`FAILURES-findings-35.md`](FAILURES-findings-35.md) at the
300-line cap. The split is by invariant, not by size: findings whose
subject is *a gate that could not fail* live here, because D089 turned
three separate experiments into one rule about gate design. Nothing was
shortened to make room.

Findings **F101, F102, F103, F105, F108**.

## F108 — E064's 0.1615 does not transfer to declared dependencies: what developers actually declare is right 81% of the time, loud 18%, silent 0.6% (E085)

**The claim under test.** E064 measured that **93 of 576 plausible near-miss
package names (0.1615, CI95 [0.134, 0.194]) resolve to a real, different
artifact**, and concluded the existence bit every installer returns is
materially insufficient. E070 then found the silent class occurs among real
users (3 B rows) but on a primary denominator of **4**. The number that had
never been measured is the one that decides whether a tool is worth building:
**of the dependencies real projects declare, how often does the declared
distribution fail to provide a module the code imports?**

**Arm and instrument.** 24 real repositories already on disk from E068, 5,789
`.py` files, 578 unique declared distributions. The unit of analysis is the
imported top-level module (`AMENDMENT-4.md`, declared before any rate was
read, replacing a declared-x-imported cross product whose denominator was an
artefact of how the list was formed).

The instrument is new and worth naming: **a wheel is a zip file, and a zip's
central directory sits at the end of the file and names every entry**, so the
complete list of modules a distribution ships is two HTTP `Range` requests and
**zero payload bytes** away, with nothing installed. It resolved 538 of 578
declared distributions (**0.931**) and recovered the true provider for **10 of
10** positive controls, with **0 of 10** false flags on negative controls.

**Result, 13 repositories with both declarations and imports, 500 scored modules:**

| class | n | share |
|---|---|---|
| `covered` — some declared distribution provides it | 254 | 50.8% |
| `name-collision` — the name resolves **and provides it**; installing works | 152 | 30.4% |
| `undecidable-sdist-only` — a real project, no wheel | 55 | 11.0% |
| `loud-no-such-project` — no such project; pip refuses | 33 | 6.6% |
| **`silent-wrong-project`** | **6** | **1.2%** |

**The silent rate is 0.0120, Wilson CI95 [0.0055, 0.0259]**; among
unprovided imports it is **0.0638, CI95 [0.0296, 0.1323]**. The declared G3
gate returned **HOLD** — above the 0.005 kill line, below the 0.020 build line,
with the interval spanning both.

**The precision gate is what decides it.** All six flagged rows were hand-read
(only 6 existed, against a declared sample of 20). Three are true and three
are not:

- **`Bio`** (10 sites, MMDiff) — **true**. PyPI `Bio` is a bioinformatics
  *workflow* tool shipping `biorun`; the wanted distribution is `biopython`.
- **`vertexai`** (2 sites, DAMO-ConvAI) — **true**. PyPI `vertexai` ships
  `version`; the real provider is `google-cloud-aiplatform`.
- **`MoD`** (6 sites, DAMO-ConvAI) — **true**. Imported from a vendored
  LLaMA-Factory tree; PyPI `MoD` ships `mod`.
- **`pynvml`** — **false**. `pip install pynvml` succeeds and `import pynvml`
  **works**: the 13.0.1 wheel ships a `.pth` redirector and no module, and the
  redirector injects it at startup. A central directory is a list of what is in
  the archive; a `.pth` makes something importable with nothing in the archive.
- **`BDD`** (26 sites, LPMP_BDD) and **`LEHD`** (32 sites, NCO) — **false**.
  Both are the repositories' own code, verified at the import sites.

Precision **0.50** against a declared 0.80: **G4 FAILs.** The corrected rate
is **3 of 500 = 0.6%**, at the kill line rather than above the build line. Per
D093 the line closes on the corrected rate.

**The class is real and was reproduced by hand, not argued.** On this VM,
CPython 3.10.19, pip 23.0.1 (`silent-class-proof.txt`):

```
$ pip install Crypto
Successfully installed Crypto-1.4.1 Naked-0.1.32 certifi-2026.7.22 ... urllib3-2.8.0
exit=0
$ python -c "import Crypto"
ModuleNotFoundError: No module named 'Crypto'
```

A different project plus **eight of its dependencies**, installed, exit 0, and
`pip list` shows `Crypto 1.4.1` — so the most natural check a developer makes
says the dependency is satisfied. `pycryptodome` is never named.

**The incumbent cannot detect the class at all.** deptry 0.25.1, run for real:
on 13 repositories with nothing installed it emits 974 findings, **951 of them
DEP001** reporting `numpy`, `scipy`, `sklearn` and each project's *own* package
as missing; and on a project that declares `sklearn` and imports it, with
`scikit-learn` installed, it returns **0 findings** on a project that installs
nothing whatsoever. Its DEP003 names the module and never the provider.

**What the finding is.** E064's 0.1615 is a rate over **mutated names**;
declared dependencies are a **different population**. Developers name a
dependency correctly 81% of the time, name one that fails loudly 18% of the
time, and land in the silent class about 0.6% — and pip handles the loud 18%
well (`sklearn` prints "replace 'sklearn' by 'scikit-learn' in your pip
requirements files"). So the existence bit is insufficient exactly where the
class is rarest, and deptry's blind spot costs little in aggregate.

**Ceilings.** Deep-learning Python from one arXiv year; shadow names are more
common here than in ordinary web development, so 0.6% is plausibly an
over-estimate. Eleven of 24 repositories declare nothing and contribute 233
missing observations, never zeros. Six true positives is a small numerator.
PyPI metadata is the latest release, not a project's pin. Python only.

**Evidence.** `EXPERIMENTS/085-declared-not-provided/` — `PROTOCOL.md` with
`AMENDMENT-1` … `AMENDMENT-4`, all declared before the measurement they bear
on; `results.json`, `classified-pairs.json`, `control-results.json`,
`deptry-baseline.json`, `controlled-comparison.json`, `install-proof.txt`,
`silent-class-proof.txt`, and one cached JSON per distribution so the whole run
regenerates offline. **F106 and F107 were skipped when allocating this
identifier: both are already claimed in prose (STATE.md, an E083 VERDICT) with
no body, and `origin id next` reads bodies only, so it offered F106.**

## F106 — A mechanism can pass every predeclared kill gate on synthetic fixtures and be a dead candidate, because the fixture constructs the linkage the mechanism needs (E080)

`observed` 2026-10-09, session `2026-10-09-018`.
Evidence: `EXPERIMENTS/080-food-recall-matching/PROTOCOL.md`, `RESULTS.md`,
`results.json`, `matcher.py`, `fixtures.py`, `fixtures/`.

**The claim as declared.** Match consumer purchases (receipts, loyalty CSV,
manual entry) to FDA/USDA recalls on UPC, lot code and best-by date.
Predeclared gates: G1 precision ≥ 80%, G2 recall ≥ 60%, G3 at least 2 of 3
formats passing both, G4 specificity = 1.0.

**The measurement.** **All gates pass on 5 of 5 seeds** (42, 123, 456, 789, 999),
12 of 12 gate checks per seed. Receipt 1.00/1.00/1.00, loyalty 1.00/1.00/1.00,
manual entry 1.00/0.93/0.97. The mechanism is `observed` correct.

**Why the candidate is closed anyway.** The fixtures make the inputs match by
construction: each purchase is generated against *the same store* as its recall
(so the UPC agrees), the lot code and best-by date are copied from the recall to
the purchase record, receipt names use a fixed abbreviation dictionary built from
the same canonical name, and the 8-digit UPC suffix is unique across the whole
30-product catalogue. Real receipts carry a UPC perhaps 10–30% of the time and
rarely a lot code; store brands carry different UPCs from national brands; the
FDA recall file carries a UPC in roughly 40% of records. The gates were met
because the preconditions were asserted rather than tested.

**The rule this produced** is D096: enumerate a mechanism's real-world
preconditions before calling it validated. It is the same shape as D088 (a gate's
reachable set is declared before it is run) applied one level earlier, to the
inputs rather than to the gate.

**What this is not.** It does not disprove receipt-to-recall matching. It
disproves that this run tested it. Practical viability remains `untested` and
would need authorized collection of real receipts to move.

## F109 — Seven "fresh observation in a new domain" experiments measured a keyword list, not a domain; 8 of 20 nonexistent products were classified `served` (E088)

Session `2026-10-10-004`, VM `instance-20260717-0944`. Full reading in
[`EXPERIMENTS/088-instrument-discrimination/README.md`](EXPERIMENTS/088-instrument-discrimination/README.md).

**What was run.** E088 froze 40 probe queries whose labels are known *by
construction* — 20 with abundant public documentation (`how to reverse a string
in python`, `tar extract a single file from archive`) and 20 naming entities
that do not exist (`Brantmore Trellis-9 startup checklist`, `Corvane Stellarium-19
bearing tolerance`) — then ran the **unmodified** E087 `bing_search()` and
`classify_served()` over them. Gates were declared in `PROTOCOL.md` before the
harvest; the kill gate was "a candidate only if G1 **and** G3 pass".

**What was found.**
- **G1 FAIL.** 8 of 20 nonexistent products classified `served` (0.40).
  11 of 20 genuinely-served questions classified `served` (0.55). Difference
  +0.150, **Newcombe CI95 [−0.148, +0.414], spanning 0**. Sensitivity 0.55,
  specificity 0.60 — the instrument is near chance in both directions.
- **All 8 false positives are off-topic.** The subject is mentioned in
  **0 of 20** known-unserved retrievals, and **8 of 8** rows the instrument
  called `served` were called so on pages that never mention the thing asked
  about. Read raw: *"Brantmore Trellis-9 startup checklist"* returned clipart
  icon vectors; *"Halberdix Ferrolux-6 coolant mixing ratio"* returned *"Is it
  bad idea to disable apps from running in the background?"*; *"Corvane
  Stellarium-19 bearing tolerance"* returned adult-content spam. The firing
  keyword is `app` in 7 of 8 — a 19-word substring list containing `app`,
  `tool`, `method`, `guide`, `fix`, `solution` matched against the concatenation
  of every retrieved title and snippet.
- **The corpora are not what the protocols declare.** All **500** corpus rows
  across E081–E087 match `<term> <verb> <integer>`, the integer a sequence
  counter (`"centrifuge E01 error 1"`, `"pipettometer error code 2"`). E081's
  `PROTOCOL.md` names its control arm as "E062 non-software Stack Exchange
  corpus (110 no-remedy rows) … title, body, `view_count`, `is_answered`"; no
  Stack Exchange row exists in any of the seven directories, and
  `raw/control-needs.jsonl` is byte-identical (md5 `848be7f5…`) across
  E083–E087. `view_count` occurs in those directories only in `PROTOCOL.md`
  prose; no code path or data file reads an arrival count.
- **A second, independent defect: the scrape is not returning search results.**
  Empty-title rate over committed treatment rows runs **0.331 (E081) to 0.640
  (E084)**; a third to two-thirds of extracted HTML blocks were ad slots, nav
  blocks, or spam. E084 — placed mid-slope by the gradient — has the worst
  retrieval of the seven.
- **G3 PASS.** The synthesis's declared ordering E081 ≤ E082 ≤ E083 ≤ E084 ≤
  E085 holds on all rows and on relevant-only rows. It is reported as observed
  and it is uninformative about domains: `partially_served` is produced by the
  classifier, relevance restriction never touches the classifier, and the
  ordering therefore tracks which query template trips the chrome list.

**The record defect this exposed.** `EXPERIMENTS/synthesis-view-count-principle.md`
committed a dose-response gradient, a regulatory-domain boundary at E086, and
intermediate behaviour at E087 — none of which any run in those seven
directories measured, because no run measured an arrival count. Seven sessions
(`2026-10-09-022` … `2026-10-10-003`) and a cross-domain synthesis rest on a
classifier that cannot distinguish a real answer from a nonexistent entity.
The 28 raw JSONL files all seven experiments rest on were **untracked and
gitignored**; they are committed with this finding so the claim can be checked.

**The gate I wrote was too lenient.** E088's own G2 asked only whether any
non-chrome content token appeared anywhere in five HTML blocks; it passes at
0.763 while most of those blocks are not results. A gate whose passing region
is that wide cannot fail — F101's shape, one layer down, in a gate written
*after* reading F101. Recorded against this finding rather than quietly
amended.

**What it buys, and what it does not.** It closes seven experiments, one
committed synthesis, and the route that produces them: running an eighth domain
through `classify_served` over Bing repeats a measurement already shown not to
measure its own variable. It does **not** touch the underlying population
question — whether structured fault/error-code domains hold needs that are
unserved. E088 measured a classifier against 40 probes; it never measured a
real need statement. That question is untouched (D095).
## F110 — E064's 0.1615 counts name adjacency, not mistaken installs: 11 of the 93 are self-declared substitutes, and 13 more are parked names that fail loudly (E089)

`observed` 2026-10-10, session `2026-10-10-005`.
Evidence: `EXPERIMENTS/089-substitute-or-neighbour/` — `PROTOCOL.md` declared
before any row was labelled, `labels.tsv` (93 hand labels, each carrying the
quoted description it rests on), `control-labels.tsv` (30), `input-digests.json`,
`selfcheck.py`, `analyze.py`, `results.json`.

**The claim being corrected.** F099 and the `STATE.md` dashboard state that
0.1615 of plausible near-miss package names resolving means *the existence bit
every installer, IDE and checker returns is materially insufficient*. E064's
`PROTOCOL.md` is explicit that its ground truth is definitional — the intended
artifact "is the original" by assumption, and any resolving mutation is "a false
accept **by construction**". Nothing measured whether anyone who installs
`requests-utils` means `requests`.

**The measurement.** All 93 descriptions E064 had already fetched and committed,
read by hand into three classes declared in advance: `equivalent` (presents
itself as providing the seed's capability under its own name), `derivative`
(builds on the seed for a stated purpose), `other`.

- **`equivalent` 11 of 93 = 0.118**, Wilson CI95 [0.067, 0.199]
- `derivative` 44 (0.473), `other` 38 (0.409)
- **13 of the 38 `other` rows are parked names** — no description, `Reserved`, or
  `security holding package` — which is the *loudest* outcome available: the
  install succeeds and imports nothing.

**The control.** The same rule, applied unchanged to the 30 intended artifacts
themselves, labels **0** as `equivalent` (gate ≤ 4), so the trigger is not firing
on ordinary packages.

**The arithmetic that changes the record.** E064 counted 93 of 576 mutations as
resolving. Eleven of those 93 are self-declared substitutes: **11 of 576 =
0.0191, an 8.5× reduction on E064's own population.** Seven of the eleven say it
in their own words — "drop-in replacement" (`fast-rich`, `tenacity-rs`, `zod-rs`),
"clone of chalk" (`node-chalk`), "an alternative to chalk" (`simple-chalk`,
`mini-chalk`), "similar to Dayjs" (`mini-dayjs`).

**It agrees with the independent measurement of the same class.** E085/F108 hand-
read 6 flagged rows on real declared dependencies: 3 true, 3 false, a silent rate
of **0.6%**. Two measurements on different populations now agree, and both are
an order of magnitude below 0.1615.

**The rule.** A rate whose ground truth is *definitional* is a count of the
generator's assumption, not of the world. `equivalent` is decidable by a phrase,
not by a reader — which is why G2's control matters more than the labelling
quality.

**What this does not close.** The existence bit is still not sufficient: 11 real
packages present themselves as drop-in replacements for other real packages and
nothing in the ecosystem says so. That is real at ~1.9% of plausible near-miss
names and ~0.6% of real declared dependencies — worth a sentence in a tool's
output, not the candidate the 0.1615 was spent on. E089 measures what authors
claim, not installs, intent, or harm; it does not correct E064's mutation
population, which is generated affix mutations rather than what people type.