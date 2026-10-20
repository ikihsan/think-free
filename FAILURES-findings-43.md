<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# Failure findings 43 - an arm in the raw file and absent from the write-up

Continued from [`FAILURES-findings-42.md`](FAILURES-findings-42.md). F137, F138
and F139 continue in [`FAILURES-findings-44.md`](FAILURES-findings-44.md).

## F134 — a gate that declared its own product constraint fired and was never reported, and the closure went out on 2 of the experiment's 7 arms (E174)

**Date:** 2026-10-17. `EXPERIMENTS/174-scoped-reach-recompute/`. Raw:
[`results.json`](EXPERIMENTS/174-scoped-reach-recompute/results.json).

### What was asked

Whether the version-pinned closure (F132) follows from E170's own committed
evidence. E170 stored seven arms in `raw/summary.json`; its write-up reported
two.

### What happened

`raw/summary.json` reports **seven** arms. `RESULT.md` reports **two** — the two
**global** ones — and F132, the `HYPOTHESES.md` status row and `STATE.md` all
inherit the conclusion built on them. Recomputed from E170's raw responses with
rank re-derived from the returned URL lists (never read from a stored rank), all
seven reproduce exactly (**G1 pass**) and the row-to-record alignment is proven
from both sides: 97 of 97 records consumed, 0 leftover, **0** mismatches on
either the replayed query string or the log's own `arm` label (**G2 pass**).

| | global | repo-scoped |
|---|---|---|
| quoted error string | 1/13 = 0.0769 | **5/13 = 0.3846**, median `total_count` **1** |
| component + symptom words | 2/13 = 0.1538 | **5/13 = 0.3846** |
| union of arms | 2/13 = 0.1538 | **6/13 = 0.4615** [0.2321, 0.7086] |

Paired on the same 13 rows: union comparison **4 scoped-only, 0 global-only**,
McNemar exact **p = 0.125**; per arm, p = 0.25 / 0.125 / 0.25. The best scoped
point estimate, **0.3846**, clears E170's own declared **0.30** build bar; its
Wilson lower bound, **0.1771**, does not.

The protocol had asked for exactly this. **G1** — "A0 hit rate, bare and quoted,
**globally and repo-scoped**" — is a declared measurement of the incumbent arm.
**G3** — "Global versus repo-scoped, for both arms. **If repo-scoped succeeds
where global fails for both arms**, the mechanism needs the developer to already
know the repository, which is a product constraint and **is recorded as one**" —
fired. Neither G1's scoped rows nor G3 appears anywhere in `RESULT.md`.

The kill itself was also scoped without declaration: G2 is "paired comparison of
A1 against A0 on the same rows, **same scope**", and the comparison reported is
`A1_global_vs_A0_quoted_global` — the global scope, chosen after the fact, which
is the scope at which the mechanism looks worst.

### Why it happened

The arms were computed, stored and summarised correctly; the reporting stage
selected the arms that supported the sentence the file was written to make. The
number of arms in `summary.json` (7) and in the prose (2) disagreeing was visible
to any reader of both files, which is the cheapest possible check.

### What it changes

- **F132, E170's `RESULT.md`, the `HYPOTHESES.md` row and `STATE.md` are
  corrected in place** on 2026-10-17. The vocabulary finding stands; the closure
  does not.
- **The version-pinned line is reopened for a fresh-sample measurement**, and the
  open question is the one G3 named: the mechanism requires knowing the
  repository. **E175** asks whether the repository can be derived from a failure
  report — mechanical, registry-backed, no search engine.
- **Rule: an arm present in `summary.json` and absent from the write-up is a
  defect in the write-up, and the check is a count.** Declare the number of arms
  in the protocol and reconcile it against the number reported *before* the
  sentence is written. A gate that predicts a product constraint is a **result**,
  and reporting only the gates that closed the line is how a line gets closed on
  one cell of a 2×2.

## F135 — a package registry is keyed by distributable name and a failure report carries a symptom name, so the pipeline returns a plausible wrong repository instead of abstaining (E175)

**Date:** 2026-10-17. `EXPERIMENTS/175-repo-from-report/`. Raw:
[`derivation.json`](EXPERIMENTS/175-repo-from-report/derivation.json) and
[`raw/http.jsonl`](EXPERIMENTS/175-repo-from-report/raw/http.jsonl).

### What was asked

E174 reopened the version-pinned line and left one open step: `report →
repository`. Could it be mechanical — no model, no search engine — by asking a
public registry where the artifact a failure report names is developed?

### What happened

**G1 = 0 of 21 = 0.0000**, Wilson [0.0000, 0.1546], against a **declared kill at
0.20**. Failure classes: **20 `wrong_repo`, 1 `not_in_registry`, 0 correct**. The
wrong repositories are real and reachable through real registry lookups:
`hapijs/code` for `microsoft/vscode`, `rumpl/c` for
`microsoft/vs-solutionpersistence`, `pcattori/namespaces` for `cplusplus/draft`,
`christkv/node-git` for `powershell/powershell`, `orsinium/advice` for
`fmtlib/fmt`, `alexfernandez/performance` for `more-itertools/more-itertools`.

**Coverage and collision, both measured.** The 17 gold repositories are
applications, runtimes, standards bodies and working groups — `microsoft/vscode`,
`powershell/powershell`, `fmtlib/fmt`, `cplusplus/draft`,
`itanium-cxx-abi/cxx-abi`, `rust-lang/libs-team`, `git-for-windows/git` — and
none is a registry entry under the name a report would use. Where a name *is* a
registry name it is a common word owned by an unrelated package, so **collision
is worse than absence**: an abstention is honest, `hapijs/code` is not.

### The number that bounds the whole line

A high-arrival Stack Overflow question records its fix as a **repository** link
in **21 of 145 answered rows = 0.1448**, and as a specific **tracker document**
in **10 of 145 = 0.0690** (of the 200 drawn: 0.1050 and 0.0500). E174's 0.3846
was measured on rows drawn from that 1-in-14 population, and E175 measures the
step that would have to be automatic at **0**. Composing the two is an
inference across two populations and is labelled one. **79% of answered
high-arrival questions record no repository link at all** — the largest bucket,
and the one this line has never had a handle on.

### The instrument cost, declared in full

The 0 was wrong four times, and each repair was declared and committed before the
next run: document-order candidates with first-hit-wins (so the generic word
`npm` beat the project's own package name); a 20-entry package whitelist that
contradicted the protocol and excluded every package the author had not thought
of; a loose body sweep that treated any hyphenated word as a package name (F131
had already measured that strategy as noise); and finally the ordering and
tag-spelling repairs that left the number unmoved. G0's later runs are withdrawn
as instrument-limited — `403 rate limit exceeded` on the 60/hour core API — and
the first run's 17 of 17 stands.

### What it changes

- **The registry route is closed, and the step is redirected rather than
  abandoned**: a *project index* is the right source shape, and those exist
  (libraries.io, ecosyste.ms, Homebrew and winget manifests, GitHub topics), so
  no prior-art screen is run and nothing is proposed to build.
- **Rule: a tool that returns a wrong answer confidently is worse than one that
  abstains, and an evaluation that only scores correctness hides that.** A
  candidate pipeline on this population should be scored on **wrong-repo rate** as
  a first-class number, because 20 of 21 wrong answers with 0 abstentions is a
  different product from 20 wrong answers and 1 abstention.
- **Rule: a zero repaired N times is not a zero.** Declare the repairs, declare
  the last one, and then stop — an instrument that needs a fifth repair against
  the population it is measured on is measuring its author.
- **The next candidate may not be a retriever or an extractor over tracker
  documents** (D117): the population is 7% of high-arrival questions and the
  reachable share of it is 0.

### Lint note (2026-10-17)

Landing F133's unlogged work cost three `origin-meta` blocks, added here rather
than invented for them: `CLASSIFICATION-PROTOTYPE.md`, `PROTOCOL-E172.md` and
`EXPERIMENTS/171-resolution-fact-locus/RESULT.md` were written by other sessions
and had none, so `doc lint` was red on all three the moment they were committed.
The blocks record what those files already were, and change nothing in them.

---

## F136 — six service closures in a row each measured a mixture and reported it as one number (E177)

**Date:** 2026-10-17. `EXPERIMENTS/177-evidence-gated-need/`.

### What was asked

Whether a free general assistant is measurably worse at reaching a real
question's community answer when that answer's resolution depends on a fact or
artefact the question does not contain. Stated and declared before any answer
body was read: [`PROTOCOL.md`](EXPERIMENTS/177-evidence-gated-need/PROTOCOL.md).

### What it found

Same venue, same key, same treatment, same reader roles, **the only difference
being whether the question carried its own evidence**:

| arm | n | reached | rate | Wilson 95% |
|---|---|---|---|---|
| SELF — resolution reachable from the question's text | 30 | 26 | **0.8667** | [0.7032, 0.9469] |
| EVID — resolution needs something the question does not contain | 30 | 12 | **0.4000** | [0.2459, 0.5768] |

**gap +0.4667, Fisher exact two-sided p = 0.000368**, against a bar declared as
`gap >= 0.25` and `p < 0.05`. All four controls green on the same run.

CLF's labels put the class at **46 of the 100 highest-arrival rows carrying a
key answer** — 0.46 of high-arrival answered questions — composed of
`upstream_source` 19, `other` 8, `version` 7, `configuration` 6, `data_value` 4,
`platform` 2. Reached rows are spread across the kinds in proportion, so **no
single mechanical kind carries the failure**.

### Why this is recorded as a failure of the record and not of the assistant

Six populations in this record closed on service — E062 0.85, E091 0.25, E092
0.81, E126 0.6750, E143 1.0, E115 14/14 — and every one of them reported a
single number for a pool that contains both classes. **0.4000 is the lowest rate
a free general assistant has scored on a real question population here**, and it
was inside all six of those pools, unmeasured. D107 built the mission's only
standing constraint on the inference that the undecidable population was the
open region; that inference is now measured and **supported**, and the thing
that was wrong was the screens' arithmetic: a stratified quantity was being
reported unstratified, five times, and read as a verdict about each population.

E091 did stratify, by answerability — and got 0.25, which is why it looked like
an outlier and why the record's explanation was *composition of what the
community owns*. **Composition is real (F114) and E143's venue-shape result
stands; but composition of the venue is not the only composition in the pool.**
E177 finds a second, larger one inside a single venue.

### Rules that come out of it

- **A service screen must stratify on evidence-completeness before it reports a
  pool rate.** This is D113's rule (stratify on version-dependence, not one
  pool rate) applied to a second variable, and it is now a general rule: **report
  the arm, not the pool, whenever the arms differ.** Two arms differing by 0.47
  at p = 0.00037 is not a pool.
- **An abstention rate is reported beside every reach rate.** Here it was
  **0 of 30 against 0 of 30** — the assistant does not notice that the evidence
  is missing, it answers anyway and is wrong 60% of the time. A confident-wrong
  rate is a first-class number for any candidate on this population, and this is
  the same rule F135 reached from the other end (wrong-repo rate with 0
  abstentions).
- **No control in a reader protocol tests the arithmetic.** All four of this
  protocol's controls passed on a run whose p-value was wrong by a factor of
  2,700 (`AMENDMENT-6`). A hand-written test must be checked against a table
  with a published value before its output is reported, and the check is
  committed beside the result.
