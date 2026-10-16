<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E170 RESULT — the vocabulary of the failure and of the fix do not overlap; the responder's prose is the bridge

**Date:** 2026-10-16. **V1–V3 pass. G0 fired as declared (0/13); the repaired
control G0r fails on both surfaces (7/13). The capability controls pass on both
(API 11/13 at rank 1, web 10/13 at rank 1), so the arms are read.**
**G2's kill does not fire (A1 2/13 > A0 1/8, McNemar p = 1.0); the declared
0.30 bar is not met, so the class closes.**

## The question

E169 measured that a published fix shares **no three-word run** with the post
that needs it, and that the forum thread — not the tracker item — carries the
fix at ≥ 0.8 term coverage. Containment is necessary, not sufficient. So: on a
real ranked index, does the query a developer types reach the fix?

## Two instruments, because they are not the same one

| | API `search/issues` | web `github.com/search?type=issues` |
|---|---|---|
| `"quoted phrase"` | **quotes not enforced** — a phrase is term-AND | honours the phrase: 1 result |
| bare number in the query | parsed as an **issue-number qualifier** — nonsense + `9987` = 2 436 hits | — |
| `a/b` in the query | parsed as a **repository qualifier**, `http_422` if it does not exist | — |
| query length | rejected above **256 characters** | — |
| rate limit | 10 requests/minute unauthenticated | none observed |

The API arm's "phrase" was therefore never a phrase, which is why its control
matched a median **718 258** documents. Both are fixed defects of the same
query, reproducible with the queries in `queries.json` and the probes in
`html_probe.py`. The web surface is the one a developer's mechanism would use, so
it is the one that decides.

## Controls — the instrument is capable

| control | API | web | bar |
|---|---|---|---|
| `in:title "<the target's own title>"` | **11/13 at rank 1** | **10/13 at rank 1** | ≥ 10/13 at rank 1 |
| rare 3-word phrase mined from the target's own body | 7/13 | 7/13 | ≥ 10/13 |
| placebo (another row's phrase) | 0/13 | — | ≤ 1/13 |

The title control passing on both surfaces establishes that **ranking works**:
given a query that matches the target's distinctive vocabulary, the target comes
first. The rare-phrase control fails on both, and the failure is the rule, not
the surface — the longest tokens in an issue body are URLs and image markup
(`![not-working-1 4](https://user-images…`, `in [#52049](https://github.com/…`)
which tokenize into common terms. **A control that fails identically on two
different instruments has found the rule, not an instrument.**

## G-A0 and G-A1 — the arms, on the surface a developer would use

| arm | query | rows with query text | target in top 10 | rate | Wilson 95% |
|---|---|---|---|---|---|
| **G-A0** | the developer's quoted error string | 8 | **1** | 0.125 | [0.022, 0.470] |
| **G-A1** | component + symptom keywords | 13 | **2** | 0.1538 | [0.0433, 0.4223] |
| G-A1 − G-A0 | paired, same rows | 12 | McNemar exact **p = 1.0** | | |

Five of the 13 rows have no literal at all (E169: symptom-only posts), so G-A0's
denominator is 8; scored over all 13 it is 1/13 = 0.077. Either way it is far
below the 0.30 the protocol set for building anything, and the only row either
arm reaches is the one the other also reaches.

The two rows G-A1 reaches are `docker/for-mac#7520` at rank 1 and
`firebase/firebase-ios-sdk#14643` at rank 5 — the two whose posts quote a
distinctive UI string rather than a stack trace.

## Why, in one sentence

**A failure report names the symptom and the environment; a fix states the cause
and the change.** The two vocabularies barely intersect — 0 of 13 rows share a
three-word run (E169) — so a lexical query of either kind cannot match the
document that carries the fix, and the surface's own ranking confirms it on both
instruments. The forum thread serves this class because the responder writes
answer-vocabulary *inside the question's own document*: the bridge between
question and answer vocabulary is a human writing prose next to the question.
That is the semantic step, and **the strongest accessible alternative already is
that step** — which is why the assistant serves the class (E126 0.6750,
E168 0.4583 on this stratum, E092 0.8108) while neither lexical form reaches 2 in
13.

## What this changes

- **The line closes.** Fifteenth served closure, and the second with the
  mechanism measured on a live ranked index rather than asserted. No retriever is
  proposed, because the only mechanism that works is the incumbent.
- **The design rule from E169 survives, reframed.** "Query what broke and where,
  not what the machine printed" is still right about *symptoms over literals* —
  and it is still not enough. Lexical retrieval of this class is not a tuning
  problem.
- **No prior-art screen is run**, deliberately: the surviving mechanism is the
  strongest alternative, so there is no differentiation to defend.

## What this does not establish

- **N = 13**, one venue, and rows biased toward having a tracker-linked fix.
  A non-firing G2 is a point estimate; at this N nothing below a very large
  effect is detectable, and the honest reading is "both arms are near zero".
- **Top-10 on one corpus.** A fix published in a changelog, a mailing list or a
  closed wiki is outside this measurement.
- **Not a claim about developers.** It is a claim about two query forms against
  one index.
- **Reaching the fix is not being helped by it.** This measures retrieval, not
  usefulness or adoption.

## The five reproducible defects, kept for whoever queries an index with an error

1. A bare number in the query is an **issue-number qualifier**, not a term —
   `zzqxvbnmklpwrts fhjkqvwxz 9987` returns 2 436 unrelated issues.
2. A `word/word` token is a **repository qualifier** and returns `http_422` when
   the repository does not exist. Error strings contain slashes (`dlopen(/Users/…`,
   `@rpath/libgfortran.5.dylib`).
3. Quotes buy **no phrase semantics** on the API endpoint — only on the web.
4. Queries above **256 characters** are rejected outright, and pasted stack
   traces exceed that.
5. Mining a document for its most selective terms selects **URLs and image
   markup**, because that is what technical issue bodies are longest in.

## Raw evidence

[`PROTOCOL.md`](PROTOCOL.md) · [`PROTOCOL-AMENDMENT-1.md`](PROTOCOL-AMENDMENT-1.md)
· [`PROTOCOL-AMENDMENT-2.md`](PROTOCOL-AMENDMENT-2.md) ·
[`queries.json`](queries.json) (committed before any fetch) ·
[`raw/summary.json`](raw/summary.json) (API arms) ·
[`raw/html-arms.json`](raw/html-arms.json) (web arms, ordered result lists) ·
[`raw/controls-g0rt.json`](raw/controls-g0rt.json) ·
[`raw/targets.json`](raw/targets.json) · [`raw/verify.json`](raw/verify.json) ·
[`ghsearch.py`](ghsearch.py) · [`run.py`](run.py) · [`html_run.py`](html_run.py)