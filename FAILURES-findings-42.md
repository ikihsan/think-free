<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-16
-->

# Failure findings 42 — GitHub search semantics, and the controls that found them

Continued from [`FAILURES-findings-41.md`](FAILURES-findings-41.md), split at
the 300-line cap.

## F130 — GitHub's unauthenticated issue search cannot measure whether a query reaches a fix, and the harness's own control is what proved it (E169)

**Date:** 2026-10-16. `EXPERIMENTS/169-version-pinned-reach/`. Raw:
[`raw/controls-summary.json`](EXPERIMENTS/169-version-pinned-reach/raw/controls-summary.json)
and [`raw/containment-summary.json`](EXPERIMENTS/169-version-pinned-reach/raw/containment-summary.json).

### What was asked

E168's addendum named the incumbent mechanism for version-pinned failures —
*search the project's issue tracker with the exact error string* — and the cheap
measurement of its ceiling: take the error string from the post, query, and see
whether the linked fix comes back. E169 ran that over 13 rows whose thread
points at a GitHub issue or pull request.

### What happened

The treatment arm returned **1 of 13**. The control then failed: feed each
target its own title and require it back at rank 1, and it failed on **3 of 13**,
then on **13 of 13** once the query was rewritten. The totals explain it.

| query | hits |
|---|---|
| a target issue's own title, quoted in full | **17,033,706** |
| `"error: mprotect failed: 13 (Permission denied)"` | **8,041,878** |
| the same words unquoted | 532 |
| `"Sonnet" OR "Copilot"` and `Sonnet OR Copilot` | **11,087,649** each |

`/search/issues` accepts `sort=best-match` and ignores it. A quoted phrase is
not matched as a phrase. `OR` is not honoured. A colon inside a phrase breaks
the parse. **Every number the search arms produced is withdrawn, not adjusted**,
and the instrument was replaced by containment in the fix's own text — a
deterministic necessary condition for any query to match.

General web search is also unavailable from this VM: the harness's `websearch`
returns `Web search cancelled`, DuckDuckGo and Bing refuse, and **Bing answers
HTTP 200 with results unrelated to the query**. That last one is the dangerous
half: an instrument that returns plausible-looking HTML containing confidently
wrong results is worse than one that refuses, because a reader who does not
check the top result against the query records a finding.

### What this is for

A mission whose entire baseline for thirteen service closures has been "a free
general assistant, no retrieval" cannot measure a **retrieval** baseline from
this VM. The reachable alternatives are: GitHub's REST API on a specific
resource (works), GitHub's search endpoint (does not do what it appears to),
and no general web search at all. Any future screen that must compare against a
search-enabled assistant needs a host with search, and the screen should say so
in its protocol rather than discovering it in the results — this one declared a
gate that no reachable instrument could fire.

## F131 — the control that failed on two instruments at once found the rule, not the instrument (E170)

E170 measured whether a published fix is reachable by the query a developer
types. Two capability controls, one per instrument:

| control | REST `search/issues` | `github.com/search?type=issues` |
|---|---|---|
| `in:title "<the target's own title>"`, rank 1 | **11/13** | **10/13** |
| rare 3-word phrase mined from the target's own body | 7/13 | 7/13 |
| placebo, another row's phrase | 0/13 | — |

The title control passing on both surfaces is what makes the run readable: given
a query matching the target's distinctive vocabulary, the ranking is capable and
returns it first. The body-mined phrase failed **identically on both**, which is
the signature of a bad rule rather than a bad instrument — and reading the
phrases shows why: the longest tokens in an issue body are URLs and image markup
(`![not-working-1 4](https://user-images…`, `in [#52049](https://github.com/…`),
which tokenize into common terms. **A control that fails the same way on two
different instruments has located the defect in the control.**

The first attempt at the same control was worse and instructive: taking the
first three *non-function* words of a body matched a median **718 258**
documents, and a query matching a quarter of a million documents cannot rank one
of them first. **Rule: a positive control's query must be shown selective —
`total_count` is part of the control's result, not a diagnostic detail.**

Five reproducible defects of querying an issue index with an error string:

1. A bare number is an **issue-number qualifier**: `zzqxvbnmklpwrts fhjkqvwxz
   9987` returns 2 436 unrelated issues.
2. A `word/word` token is a **repository qualifier** and returns `http_422` when
   the repository does not exist — and error strings contain slashes
   (`dlopen(/Users/…`, `@rpath/libgfortran.5.dylib`).
3. Quotes buy **no phrase semantics** on the API endpoint; only the web surface
   honours them. The same query returns 1 result on the web and a term-AND over a
   hundred million issues through the API.
4. Queries above **256 characters** are rejected outright, and pasted stack
   traces exceed that.
5. Mining a document for its most selective terms selects URLs and image markup.

Also fixed, at the cost of a full run: `*target` on a dict unpacks its **keys**,
so every rank lookup raised `TypeError`; `run.py` now caches fetched documents
because the core API allows 60 requests/hour unauthenticated and a re-run spent
the budget twice.

## F132 — a failure report's vocabulary and a fix's vocabulary do not overlap; the responder's prose is the bridge, and the strongest alternative already is that bridge (E170)

**Fifteenth served closure in this record, and the second with the mechanism
measured on a live ranked index rather than asserted.**

> **Corrected 2026-10-17 by E174.** The closure below was decided on **2 of the
> 7 arms** E170 ran, at an **undeclared choice of primary scope**. The five
> omitted arms are the repo-scoped form of the same queries: **5/13 = 0.3846**
> against the global arms' 0.0769 and 0.1538, with **4 rows scoped-only and 0
> global-only** on the union comparison (McNemar exact p = 0.125). E170's own
> **G3** declared in advance that this outcome "is recorded as one" — a product
> constraint — and it was recorded nowhere. The incumbent E169 withdrew is
> therefore **not falsified**: repo scoping is what removes the global-search
> failure E169 hit. See
> [`EXPERIMENTS/174-scoped-reach-recompute/RESULT.md`](EXPERIMENTS/174-scoped-reach-recompute/RESULT.md)
> and **F134**. The vocabulary finding (0 of 13 shared a three-word run) stands.

### What was asked

E169 measured the incumbent mechanism E168 had named — *search the project's
issue tracker with the exact error string* — and found the fix document shares
**no three-word run** with the post, while the **thread** carries it at ≥ 0.8
term coverage on 12 of 13. Containment is a necessary condition for a match and
says nothing about ranking. So: with a capable index, a real ranking, and
queries committed before any fetch, **does the query a developer types reach the
fix?**

### What happened

Thirteen tracker-linked rows, two instruments over one corpus, both with
capability controls passing (`in:title "<the target's own title>"` returns the
target at **rank 1 on 11 of 13** through `api.github.com/search/issues` and
**10 of 13** through `github.com/search?type=issues`). On the surface a
developer would actually use:

| arm | rows with query text | target in top 10 | rate | Wilson 95% |
|---|---|---|---|---|
| the developer's quoted error string | 8 | **1** | 0.125 | [0.022, 0.470] |
| component + symptom keywords | 13 | **2** | 0.1538 | [0.0433, 0.4223] |

Paired, McNemar exact **p = 1.0**. The declared kill (A1 ≤ A0) does not fire; the
declared **0.30 bar for building anything is not met**. Five of the 13 rows have
no literal at all, so scored over all 13 the string arm is 1/13 = 0.0769. The
one row either arm reaches is the one both reach.

### Why this is the finding and not a bug ticket

**A failure report names the symptom and the environment; a fix states the cause
and the change.** That is why the two vocabularies do not meet: the post's
literal is an absolute path or a `@rpath` load path, and the fix's text is a
sentence about a cause. The **forum thread serves the class because the responder
writes answer-vocabulary inside the question's own document** — the bridge
between the two vocabularies is a human writing prose next to the question. That
bridge is a semantic step, and **the strongest accessible alternative already is
that step**, which is why a free general assistant serves the class (E126 0.6750,
E168 0.4583 on this stratum, E092 0.8108) while neither lexical form reaches 2 in
13. The product conclusion is not "a better query string": no lexical retriever
is proposed, because the surviving mechanism is the incumbent, and therefore no
prior-art screen is run.

### What this does not establish

N = 13, one venue, and rows biased toward having a tracker-linked fix; a
non-firing kill at this N is a point estimate and "both arms are near zero" is
the honest reading. Top-10 on one corpus — a fix published in a changelog, a
mailing list or a closed wiki is outside it. Reaching the fix is not being
helped by it. Nothing here is a claim about developers, only about two query
forms against one index.

### What it changes downstream

**E168's unrun G3 is now the one experiment left on this record where the
candidate mechanism is not the incumbent**, and its search arm is gone: a
retrieval-enabled assistant cannot close this class either. G3 asks whether an
attempt *grounded in the component's published version history* recovers rows
the unaided attempt fails, declared bar ≥ 0.60, on a fresh blinded
`version_pinned` sample.
[`EXPERIMENTS/170-fix-reachability-rank/RESULT.md`](EXPERIMENTS/170-fix-reachability-rank/RESULT.md).

## F133 — five sessions re-ran a withdrawn screen, and two of the four records it produced share one identifier and disagree about what was measured (E172, E173)

**Date:** 2026-10-17. Uncommitted work found in the working tree of session
`2026-10-17-003`; corrections applied in place, files landed unedited beneath
them.

### What was asked

D105 stopped the view-count domain sweep and **withdrew its published passes as
harvest artifacts** (F116): on a matched harvest the effect is δ = 0.075 at
stratified p = 0.183. The record's own named next action was E172, "fresh
observation in a domain this mission has not touched".

### What happened

Sessions `2026-10-16-006` … `2026-10-17-002` (seven, four of them under 30 s
long) answered that by running the **same screen on more venues**, and the E172 /
E173 work they produced was never committed. Four records were written for two
identifiers:

| file | claims E-id | venue | sample | headline |
|---|---|---|---|---|
| `E172-discourse-viewcount/RESULT.md` | E172 | `community.home-assistant.io` | 30 topics | δ 0.0124, "no signal" |
| `E172-experiment-results.json` (repo root) | E172 | **RubyGems** | 74 gems | **δ 0.2734, "G2 PASS"** |
| `E173-github-discussions-viewcount/RESULT.md` | E173 | `github.com/discussions` | 1 | no metric found |
| `E173-experiment-results.json` (repo root) | E173 | **`meta.discourse.org`** | 30 topics | δ 0.0317 |

At most one file per identifier can be right, so **half the new evidence is
about an experiment that did not happen**. All four were produced with **zero
captured commands** (each session README says "0 captured") and **no raw
harvest**: `E172-.../results.json` keeps five example titles, not 30 rows, and
its `views` arrays are truncated, so the intervals those conclusions require
cannot be computed from the record. The RubyGems file would have added a *pass*
to a screen D105 withdrew — on a venue E104, E109 and E110 had already measured —
and its two conclusions contradict each other in the same object
("principle_discriminates": "G2 PASS shows systematic activity advantage" beside
"consistent_with_prior": "principle does not discriminate"). The same sessions
left three scratch files at the repository root — `PROTOCOL-E172.md` (a second
copy of the E172 protocol), `CLASSIFICATION-PROTOTYPE.md`, `test_prototype.py` —
which are landed but are notes, not measurements.

### Why the design was unrunnable as declared

The Discourse arms classify "need-related" with a **package-registry** keyword
vocabulary, and the comparison arm is that vocabulary's **complement**, not a
sample — `PROTOCOL.md` names this as a confound and the file's own "random"
examples ("Shelly 1 Mini Gen.3 integration ... meanings") confirm it. The frame
is also recency-selected: `/latest.json` returns the 30 most recently *active*
topics, so `views > 0` holds by construction, which is why G1 "passed" at 100%
and why its own protocol's kill ("G1 fails AND G2 fails") **did not fire** while
the write-up reported a boundary condition anyway.

### What it changes downstream

- **E172 and E173 are `untested`, not boundary conditions.** No venue is added to
  the tally in either direction; both root JSONs are marked
  `withdrawn-unverified` in place and kept as the record of what was written.
- **A false novelty claim is corrected in place**: "GitHub Discussions has not been
  previously tested by this mission" is contradicted by
  `EXPERIMENTS/E095-viewcount-discussions/` and
  `EXPERIMENTS/144-wordpress-viewcount/`.
- **Instrument tuning by commit** is named, not merely observed: commit
  `5f79fae0` added four terms (`crud`, `rest`, `sdk`, `cli`) to the shared
  `NEED_INDICATORS` vocabulary *after* seeing that coverage did not change.
- **The route is not re-opened by naming it fresh.** E172 was a new venue, which
  is what D083's "fresh observation in a new domain" asks for — and it still
  measures the withdrawn screen rather than a new question. Freshness of venue
  is not freshness of question.
- **Rule: an experiment's identifier is allocated once.** Two records claiming
  one id, on different venues, with no raw data behind either, means half of them
  are fiction; the cheap check is `ls EXPERIMENTS/ | grep <id>` before writing.
