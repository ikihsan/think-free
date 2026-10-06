<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Findings F070-F074 (E041, `EXPERIMENTS/041-need-index/`)

Split out of [`FAILURES.md`](FAILURES.md) as part 28. One finding per section:
what happened, what it rules out, and the ceiling of the evidence. **Identifiers are
stable across all findings files.**

**Five are defects in this session's own instrument or protocol; one is a defect in
a published sentence of this repository's record.** Four of the five were caught
before they reached a conclusion. The one that was not was caught by a check
written for a different reason, and that is the transferable part of F074.

## F070 — A by-name list of famous repositories yields no positive control at all

**What happened.** E041's protocol declared ten established libraries by name as
the corpus for a duplicate-detection control. `pallets/click`, captured completely
and reconciled against the API's own `total_count`, holds **1,809 issues, 16 of
them labelled `state_reason: "duplicate"` — a share of 0.0088 — and exactly one
whose body names another issue in the same repository.** Fourteen named no issue at
all; they cite pull requests, documentation URLs, and other projects.

So the declared selection yields **1 positive pair per 1,809 issues**. At that rate
G1's paired-difference interval and G2's top-1 accuracy resolve nothing.

**What it rules out.** It rules out the inference that a repository's issue count
predicts its usefulness as a control population. **Triage volume and
duplicate-closure rate are different properties of a repository**, and a list of
famous libraries is a list of the wrong one — `d3/d3` carries 2,247 issues at a
duplicate share of **0.0009**, six times worse than `pallets/click`.

**The repair, and why it is not selection-for-the-answer.** Screening is a
*mechanism* question, not a measurement of the claim: ten search requests of
`reason:duplicate "duplicate of #"` counted parseable references per repository and
the top six by that count were captured completely. The by-name list was **kept and
reported as its own arm**, and the pooled verdict is taken on the arm with the
larger positive population with both printed. Selecting a population *capable of
producing the control* is not selecting the control's outcome.

**Ceiling.** Repositories selected for duplicate closure differ from repositories
selected for being famous, in moderation culture, user base and text. A gate *met*
on them would be evidence about the instrument on screened repositories. A gate
*failed* on them is evidence about the instrument full stop — and that is what this
run has.

## F071 — A repository-scoped search qualifier silently discarded 99.97% of the population

**What happened.** The screening query was written with `stars:>500`, as a free
precision filter against mass-issued repositories. It returned **89 rows in total**.
That is not a plausible population, so the qualifier was measured rather than
trusted:

| query | `total_count` |
|---|---|
| `is:issue reason:duplicate` | **358,471** |
| `is:issue reason:duplicate "duplicate of"` | 96,971 |
| `is:issue reason:duplicate stars:>500` | **107** |
| `is:issue reason:duplicate stars:>500 "duplicate of #"` | 89 |
| `is:issue reason:duplicate in:body "duplicate of #" stars:>100` | **0** |

**A qualifier that looks like it narrows a population took it from 358,471 to 107,
and combined with `in:body` to zero.**

**What it rules out.** It rules out reading any screened population size as a
property of the world while a qualifier is in the query. Left in place, the run
would have reported "89 issues, 3 repositories, 1 pair" and the honest-looking
conclusion would have been that no reachable repository supplies pairs — **a
conclusion about the query presented as a conclusion about the world.**

**This is the tenth instance of the shape F055, F058 and F059 record, and the first
caught before the measurement rather than after it.** It cost seven requests and
changed the design. Withdrawn, and **not replaced by a heuristic**: no substitute
filter was invented to occupy the space, because a substitute carries the same
unverifiable assumption the withdrawn one carried. The automation guard is the 0.20
duplicate-share exclusion, computed on the capture itself.

**Ceiling.** The cause is not established — it may be a documented interaction
between `stars:` and `reason:` — only the effect is. **Not replaced by a
qualification:** a differently-spelled filter might behave differently, and
asserting that without measuring it is the error this finding is about.

## F072 — A status code is not a condition, and treating 403 as fatal lost four repositories

**What happened.** A correction to the capture's retry rule, made on the evidence
that `tiangolo/typer` returns **422** (a renamed repository), also listed **403** in
the same fatal set **on no evidence at all**. On restart the capture hit GitHub's
unauthenticated search limit — **10 requests per minute**, read from the response
headers:

```
HTTP/1.1 403
{"message":"API rate limit exceeded for 140.245.241.183. ..."}
X-RateLimit-Limit: 10   X-RateLimit-Remaining: 0   X-RateLimit-Reset: 1791303915
```

**Every one of those 403s was the rate limit, and the run treated them as fatal.**
Four repositories were recorded `{"error": "HTTPError 403"}` and skipped
permanently: `pl0n3r/brvtal`, `buchochelliq-labs/rs-rich-cli`,
`unvde/CP3407-Assessment`, and by-name `pytest-dev/pytest`, `vuejs/vue`, `d3/d3`.
**Three of the six were screened repositories — the ones the gates are read on.**

**What it rules out.** It rules out a skipped repository being read as a repository
that legitimately returned nothing. The two are indistinguishable in the log, which
is why the loss was silent.

**The generalisation, which is the eleventh instance of this record's most repeated
shape.** F055, F058 and F059 are all *"a fact about the instrument's own selection,
read after the measurement rather than before"*. This one is the same shape one
level down: **a fact about the instrument's own error handling, read by treating one
status code as one condition.** A 403 is not a condition; it is a code that a dozen
conditions arrive under. **An instrument's failure modes must be enumerated from its
responses, not from its status vocabulary.**

**The repair.** 403 is classified by its headers: `X-RateLimit-Remaining: 0` is the
rate limit and is slept through until `X-RateLimit-Reset`; any other 403 is fatal;
401 and 422 stay fatal. Pacing is read from `X-RateLimit-Remaining` on every response
rather than assumed from a constant. **A repository recorded with an error is
retried, not skipped** — the resume set is now `{reconciled: True}`, because the
first version's resume set made the loss permanent.

**Ceiling.** `tiangolo/typer` is still unreachable under its declared path and stays
excluded. Two screened repositories reached a duplicate share above 0.20 and were
excluded as automated, so **the gate-bearing arm is smaller than the screening rule
selected**, and that shortage is reported rather than absorbed.

## F073 — An all-zero curve is indistinguishable from a bug in the draw

**What happened.** `subsample_indices` returned **row ids** — strings — where its
callers expected **row positions**. Every downstream lookup then missed the corpus
and contributed no edges. The result was a clean, plausible, entirely fictional
table of **0.00 across all nine corpus sizes, both arms, all eight thresholds**, with
`alpha = 0.0` and `S1 = false` — a result indistinguishable from a real finding that
the corpus does not densify.

**What it rules out.** It rules out reading an all-zero measurement as a negative
result before the draw is shown to be addressing the population at all. The failure
was silent because a missing position simply contributes nothing.

**The repair.** `subsample_indices` returns positions hashed by id, and two guards
were added because one was not enough: the full-size subsample is asserted to **be**
the whole arm, and its result is asserted to equal the dense pass. **This is the
sixth defect of this session and the sharpest, because the guard that would have
caught it — "is the instrument actually looking at the data?" — is a different
question from every other gate in the run.**

**Ceiling.** Neither guard can detect a draw that is well-formed and in the
population but *not representative*; that is what the 40 resamples and the
percentile interval are for, and neither substitutes for reading the table.

## F074 — E040's README states a G4 number its own artifact contradicts

**What happened.** The reproduction check AMENDMENT-3 requires before the scaling
curve is reported — at n = 1391 the subsample is the whole arm, so the curve's
rightmost point must reproduce E040's own published number — was written against
E040's **prose** and fired. The cause was not drift:

| tau | 0.15 | 0.20 | 0.25 | 0.30–0.50 |
|---|---|---|---|---|
| E040 `README.md` prose | 8 | **0** | **0** | 0 |
| E040 `raw/tally.json` | 8 | **1** | **1** | 0 |
| this run, E040's own `vectors()` and `cluster_stats` | 8 | **1** | **1** | 0 |
| this run, edge list | 8 | **1** | **1** | 0 |

**The artifact and the code agree with each other and disagree with the prose.**
`EXPERIMENTS/040-need-clustering/raw/tally.json` records
`clusters_size_ge_3_stories_ge_3_authors_ge_3` as **1** at both 0.20 and 0.25.

**What it rules out, and what it does not.** It rules out nothing about E040: the
bar is 20, the maximum anywhere on the grid is 8, and **1 at 0.20 and 0.25 instead
of 0 changes no verdict.** E040's G4 stands as `not met at any tau`. This is a false
number in a summary, **not a false conclusion** — and the distinction is why it was
cheap to record and expensive to ignore: a reader trusting the sentence would have
believed the resolution was *sharper* than the run found, and drawn the same
conclusion for the wrong reason.

**The pattern, and it is the fourth instance.** F013, F018, F019 — a gate asserting a
fact about the record rather than about the code. F021 — a status declared `unmeasured`
on a run whose steps never ran. F064 — a positive control whose arms did not contain
the pair members. **This one: a summary sentence that is not what the run produced,
sitting beside an artifact that is.** In every case the discrepancy was invisible to
every gate in the repository, **because the artifact was correct and the prose was
what drifted.**

**The transferable part.** A published number should be reproducible from the
artifact it came from, and **the reproducibility test belongs inside the experiment
that depends on the number, not in a separate audit.** It cost four minutes here and
it was already on the critical path — it was written to guard the scaling curve and
found a stale sentence instead.

**Ceiling.** No gate in this repository reads a README's prose, and adding one is not
proposed: the fix is that the check exists and ran, not that a new gate is declared.
