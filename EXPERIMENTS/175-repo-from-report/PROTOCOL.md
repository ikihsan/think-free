<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E175 PROTOCOL — can the repository be derived from the failure report alone?

**Date opened:** 2026-10-17. **Status:** pre-declared before the extractor, the
registry map and the sample are written, and before any network request. The
extractor and the map are committed with this file; the queries and the drawn row
ids are committed in `queries.json` before the first request.

## The question

E170's G3 — declared, fired, and never reported (F134) — says the mechanism
needs the developer to already know the repository. E174 recomputed the arm that
says the rest of it works: given the repository, the developer's own quoted error
string reaches the fix on **5 of the 8** rows that have one, at a median of **one
matching document in the whole repository**; the union of scoped arms reaches
**6/13 = 0.4615** against the global arms' **2/13 = 0.1538**.

So the open part is exactly one step: **report → repository**. It is mechanical
if error reports name artifacts and registries say where each artifact's tracker
lives. Nothing here needs a search engine, an embedding model, or an LLM.

- **Q1 (pre-condition).** Given only the failure report — Stack Overflow title,
  body and the asker's own tags, which the asker chooses — can a deterministic
  extractor plus a public registry find the repository that owns the fix?
- **Q2 (the build decision).** Does the *end-to-end* pipeline — report → derived
  repository → the same scoped query E174 measured — reach the fix document as
  often as the oracle-scoped pipeline, and at least as often as the 0.30 bar?

## Arms

Every arm sees the report only. None sees the thread.

| arm | scope of the query | what it is |
|---|---|---|
| **A-oracle** | `repo:` + the gold repository | the **ceiling**: a person who already knows the tracker (E174's scoped arm) |
| **A-derived** | `repo:` + the repository the pipeline derives | **the candidate** |
| **A-global** | no scope | the naive form (E170's global arm), reported for continuity |

Query construction inside a scope is identical to E174's: the asker's quoted
literal where one exists, otherwise component + symptom words. One query per row
per arm, `per_page=10`, relevance order as returned. Reach = the gold document
appears in the first ten results.

## The extractor and the map (`derive.py`, committed here)

Deterministic, stdlib only, no model:

1. **Candidate artifacts**, in this fixed order, from title, body and tags:
   `node_modules/<pkg>` paths; `File "<path>.py"` frames; dotted module paths in
   backticks; `<name>@<version>` and `<name> <version>` forms; SO tags that name
   a distributable; bare product names from a **fixed list of 40 ecosystems**
   written into `derive.py` before the sample was drawn (Python, PyPI, Node,
   npm, Django, Flask, React, Vue, Angular, Docker, Kubernetes, Postgres,
   MySQL, SQLite, Redis, Nginx, Apache, Java, Spring, Kotlin, Swift, Xcode,
   macOS, Windows, Linux, Ubuntu, Debian, Chrome, Firefox, Safari, VS Code,
   Vim, Emacs, GCC, Clang, Maven, Gradle, pip, conda, Homebrew, Rust, cargo,
   Go, Ruby, Rails).
2. **Registry lookup**, in this fixed order: PyPI `pypi.org/pypi/<name>/json`
   (`project_urls` keys Bug Tracker / Source / Code / Repository / Issues, then
   `home_page`, then `package_url`); npm `registry.npmjs.org/<name>` then
   `/<name>/latest` (`repository.url`); crates.io
   `crates.io/api/v1/crates/<name>` (`repository`). The first `github.com/<o>/<r>`
   found is the candidate repository. Normalisation: lowercase, strip a `v`
   prefix, map `-` to `_` for Python only.
3. **No fallback.** If no registry resolves, the row's derived repository is
   `None` and the row scores as a miss. A guess from the name's shape is not a
   fallback.

Every HTTP response and URL tried is written to `raw/`, so the derivation can be
re-read without re-running it.

## Population

- **Source:** `EXPERIMENTS/126-stackoverflow-service-test/screening.jsonl`, the
  300-row high-arrival pool E168 used. **Reuse is declared.**
- **Excluded:** the 40 rows E126 graded (its `grading-results.jsonl`), and the 13
  rows E169/E170 read in full.
- **Draw:** 40 rows by a **seeded** shuffle of the remaining rows, seed written
  into `queries.json` before the first request. **No row is chosen by reading
  it.**
- **Declared exposure:** this session has read the pool's title and body fields
  as E168's classifier did. The screen is mechanical and no per-row judgement is
  made, but the rows are not virgin.
- **Gold repository:** the first `github.com/<owner>/<repo>` link in the
  **accepted** answer; failing that, the first such link in the highest-scored
  answer; failing that, the row has no gold and is reported, not dropped.

## Gates, all declared now

| gate | condition | meaning |
|---|---|---|
| **G0** | every gold repository is confirmed to exist via one API call each | a wrong derived repo cannot be confused with an unreachable one |
| **G1** (pre-condition) | derived repository equals the gold, over rows that have a gold | **kill below 0.20** |
| **G2** (build decision) | **A-derived reaches the fix on ≥ 0.30 of all drawn rows with a gold**, and **≥ 0.50 × A-oracle on the same rows** | the bar inherited from E170 |
| **G3** | Wilson 95% on every rate; paired McNemar exact on A-derived vs A-oracle and A-derived vs A-global | stated with its uncertainty |

**Kill condition, as declared:** **G1 < 0.20.** The mechanism cannot be
automated from a failure report, the version-pinned line closes for good, and
nothing is built. **If G1 passes but G2 fails**, the derivation works and the
retrieval does not — a narrower, differently-shaped conclusion, recorded as such
rather than as a pass.

## What would make this experiment wrong

- The pool's rows are all *tracker-linked* by construction, so every rate is
  conditioned on "the answer links a tracker". The **population share is not
  measured** and no usefulness or adoption claim follows from any gate here.
- The extractor was written by the same agent that wrote the protocol, over
  ecosystems it already knows. That is a real bias and the reason G1's bar is a
  kill, not a pass: an extractor tuned on the population it is measured on is the
  defect this record has already paid for twice (D105, F116).
- An LLM would do this task better. That is not a reason to skip it: the point is
  whether the step is *mechanical*, and an extractor that needs no model is the
  only version that could be a tool anyone runs.