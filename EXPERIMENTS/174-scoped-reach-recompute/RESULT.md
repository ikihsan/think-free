<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E174 RESULT — the closure of the version-pinned line was decided on 2 of E170's 7 arms

**Date:** 2026-10-17. G1 pass, G2 pass, G3 pass. **No network access; every
number is recomputed from responses E170 committed.** The documents that state
the closure are corrected in the same commit.

## The question

E170's `raw/summary.json` reports **seven** arms. `RESULT.md`, F132, the
`HYPOTHESES.md` status row and the `STATE.md` entry report **two** — the two
global ones — and build "the class closes" on them. The five omitted arms
include the repo-scoped form of the *same queries*, and E170's own protocol
required both:

> **G1 — incumbent (measurement, no kill).** A0 hit rate, bare and quoted,
> **globally and repo-scoped**, with the numeric-token subset separated.
>
> **G3 — scope ablation (measurement).** Global versus repo-scoped, for both
> arms. **If repo-scoped succeeds where global fails for both arms**, the
> mechanism needs the developer to already know the repository, which is a
> product constraint and **is recorded as one**.

## G1, G2 — the recomputation reproduces the record

| gate | result |
|---|---|
| **G1** every arm's hits / of / rate equals the stored value | **pass**, 7 of 7 |
| **G2** alignment proven from both sides: the query this driver would send now equals the logged query, and the log's own `arm` label equals the expected arm | **pass** — 97 of 97 raw records consumed, 0 leftover, 0 mismatches |

Rank is re-derived from each response's `html_url` list by target identity; no
stored rank is read. That is what makes this a recomputation rather than a
restatement.

## G3 — the omitted comparison

Same 13 rows, `top-10`, one query per arm. Primary denominator is all 13 rows,
the conservative choice E170 itself made when it reported `A0_global` as 1/13.

| arm | scope | in top 10 | rate | Wilson 95% | median `total_count` |
|---|---|---|---|---|---|
| `A0_quoted_global` — quoted error string | global | **1** / 13 | 0.0769 | [0.0137, 0.3331] | 99 |
| `A1_global` — component + symptom words | global | **2** / 13 | 0.1538 | [0.0433, 0.4223] | 70 |
| `A0_quoted_repo` — **same literal, scoped** | repo | **5** / 13 | **0.3846** | [0.1771, 0.6448] | **1** |
| `A0_bare_repo` — bare literal, scoped | repo | **4** / 13 | 0.3077 | [0.1268, 0.5763] | 12 |
| `A1_repo` — **same words, scoped** | repo | **5** / 13 | **0.3846** | [0.1771, 0.6448] | 3 |

Paired on the same rows, per arm:

| comparison | both | scoped only | global only | McNemar exact |
|---|---|---|---|---|
| `A1_repo` vs `A1_global` | 2 | 3 | 0 | 0.25 |
| `A0_quoted_repo` vs `A0_quoted_global` | 1 | 4 | 0 | 0.125 |
| `A0_bare_repo` vs `A0_bare_global` | 1 | 3 | 0 | 0.25 |
| **union** — any scoped form vs any global form | 2 | **4** | **0** | **0.125** |

Union reach: **scoped 6/13 = 0.4615** [0.2321, 0.7086] against **global
2/13 = 0.1538** [0.0433, 0.4223]. Not one row is reached by a global query and
missed by a scoped one.

Each literal arm's own population is the 8 rows that *have* a quoted literal,
because the query does not exist otherwise. On that denominator the scoped
literal reaches **5/8 = 0.625** [0.3057, 0.8632] against the global literal's
**1/8 = 0.125** [0.0224, 0.4709]. Both denominators are reported; the 13-row one
is the headline, because it is the one E170 used.

## The build decision this changes

E170 declared a **0.30 bar for building anything**. The best scoped arm's point
estimate, **0.3846**, clears it; its Wilson **lower bound, 0.1771, does not**.
At n = 13 this is a point estimate, not an established effect — the same standard
this record applied to E168's p = 0.1168 — and no McNemar test here reaches
p < 0.05. What *is* established is the direction and its consistency: **eight
scoped-only rows against zero global-only rows across three comparisons**, and
the protocol's own predicted condition for G3 ("repo-scoped succeeds where global
fails **for both arms**") is met exactly.

So three statements in the record are false as written and are corrected:

1. "neither lexical query reaches the fix" — true of the two global queries,
   false of the experiment: the scoped form of the identical literal reaches 5 of
   the 8 rows that have one, at a median of **one matching document in the whole
   repository**.
2. "Lexical retrieval of this class is not a tuning problem" — the scope was the
   whole difference, and it is not tuning.
3. "No retriever is proposed, so no prior-art screen is run" — the mechanism that
   survives is E169's own named incumbent (*search the project's issue tracker
   with the exact error string*), which E170 measured and did not report.

E169 withdrew that incumbent on a **global** control failure: a target's own
quoted title returns 17 033 706 hits. **Repo scoping is precisely what removes
that failure**, and E170 ran it. So the incumbent was never falsified; it was
measured at the scope where it works and left out of the table.

## What this does not establish

- **The scope is an oracle.** `A*_repo` is handed the gold document's repository.
  This measures *given that you know the tracker, the developer's own error string
  finds the fix about half the time.* It is **not** a measurement of any tool: the
  person holding the error message usually does not know which repository owns
  the fix, and nothing here shows that can be derived.
- **n = 13, and every row is tracker-linked by construction**, so every rate is
  conditioned on "the thread contains a tracker link". Population share is
  unmeasured.
- **Top-10 on GitHub issues in one corpus.** A fix in a changelog, mailing list
  or closed wiki is outside it. Reaching a document is not being helped by it.
- **Still one population, read by this mission.** The 13 rows were selected and
  read by E168–E170; E175 draws fresh ones.

## The next experiment, named here

**E175 — can the repository be derived from the failure report alone?** The
product constraint G3 predicted is now the only open part, and it is mechanical:
error reports name artifacts (a module path, a package name, a stack frame, an
OS component), and registries publish where each artifact's tracker lives
(PyPI `project_urls`, npm `repository`, crates.io, Maven). Declared in
[`PROTOCOL.md`](../175-repo-from-report/PROTOCOL.md) with its gates, kill and
sample committed before any fetch.

## Raw evidence

[`PROTOCOL.md`](PROTOCOL.md) · [`recompute.py`](recompute.py) ·
[`results.json`](results.json) — input is E170's committed
`raw/rawlog.json` and `raw/rows.json`; the row-level rank table is in
`results.json` under `row_ranks`.