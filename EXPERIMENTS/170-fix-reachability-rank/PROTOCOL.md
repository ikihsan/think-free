<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E170 PROTOCOL — is a published fix reachable by the query a developer types?

**Date opened:** 2026-10-16. **Status:** pre-declared, arms not yet run.

## The question

E169 closed the version-pinned class as served, and left one question it could
not close: *does the mechanism work at all?* Its own measurement says the error
string never matches the document that carries the fix — **0 of 13 rows share a
3-word run with it** — and that coverage against the whole thread is ≥ 0.8. So
the fix is present and the incumbent query misses it. Containment is a
necessary condition, not a ranking measurement, so "present" has never been
turned into "retrievable".

**This experiment asks the retrieval question directly, on an index that is
reachable from this host.** GitHub's issue search is live here
(`api.github.com` 200; unauthenticated, 10 requests/minute for search,
60/hour for core). For 13 real rows, with a real ranked index, one real
question:

| | |
|---|---|
| **population** | the 13 tracker-linked rows of E169's `version_pinned` stratum — all of them; E169 measured that this pool contains no more |
| **outcome** | target `owner/repo#number` present in the **top 10** returned |
| **incumbent arm (A0)** | the developer's pasted error string, verbatim — E168's named incumbent mechanism |
| **treatment arm (A1)** | component + symptom words — E169's design rule, and the opposite of A0 |
| **ablation (A2)** | A1 minus the component's own name — does success need repo identity? |

A0 is built from E169's `hand-queries.jsonl` `phrase` field and A1 from its
`keyword` field. **Those queries were written at 03:58 on 2026-10-16; E169's
first read of any fix document was at 04:14 (`raw/target-titles.json`) and the
containment run at 04:17.** They are reused verbatim rather than rewritten, so
the treatment arm is not this session's guess. E169's *automated* literal
extractor is not used: it selected prose, and using it would have weakened the
incumbent — the defect E169 recorded and did not retune.

## What the instrument probe already found (declared before any arm)

Four probes, recorded in this session's `commands.log`, fix the instrument's
semantics:

| probe | query | total_count | what it establishes |
|---|---|---|---|
| V1 | `zzqxvbnmklpwrts fhjkqvwxz` | **0** | terms are required; a non-matching query returns nothing |
| V3 | `zzqxvbnmklpwrts fhjkqvwxz 9987` | **2 436** | **a bare number is not a term — it is parsed as an issue-number qualifier**, so an error string containing a number retrieves unrelated issues by number |
| V2 | `"pasting text" in:title repo:microsoft/vscode` | 80 | `repo:` and `in:` qualifiers are honoured |
| V2 | `paste slow in:title repo:microsoft/vscode` | 13 | scope narrows (13 title < 130 body), and quotes are **not** enforced as phrases — this is term-AND within a scope, not phrase matching |

**Consequence declared in advance:** quoting an error string buys no phrase
semantics on this index. A0 is therefore run both bare and quoted, and the
numeric-token subset of A0 is reported separately, because V3 predicts that
subset is contaminated by number-matching.

## Gates

All gates are declared before the arms run. `top10` = target in the first 10
results of a single query, `per_page=10`, relevance order as returned.

- **V1 — semantics (must pass).** Re-run V1 and V3 inside the experiment run and
  write both counts to `raw/verify.json`. Pass = V1 count is 0 **and** V3 count
  is > 0 (the hazard is demonstrated, not assumed).
- **V2 — qualifiers (must pass).** For one fixed row, the counts for
  `in:title`, `in:body`, and unqualified queries over the same three terms must
  be strictly ordered `title < body < unqualified`, or at minimum
  `title < body`. Fail = qualifiers are not honoured and the scope factor is void.
- **G0 — positive control (must pass, or the whole experiment is void).** For
  each row, take the **first verbatim 3-word run of ≥ 8 characters from the
  target document's own body** as the query and require the target in the top
  10, globally scoped. This is E169's control redesigned so that it *can* pass:
  the phrase is maximally specific to the target and is guaranteed present by
  containment. **Kill: fewer than 10 of 13.** A control that cannot pass
  measures the index, and every arm number would be uninterpretable (F130).
- **G5 — placebo (must pass).** Each row is queried with a rare phrase lifted
  from a **different** row's target document, assigned by a fixed rotation.
  **Kill: more than 1 of 13 placebo queries returns its own row's target** — that
  would mean any query of this shape can return anything, and a hit rate
  measures nothing.
- **G1 — incumbent (measurement, no kill).** A0 hit rate, bare and quoted,
  globally and repo-scoped, with the numeric-token subset separated.
- **G2 — the decision (kill).** Paired comparison of A1 against A0 on the same
  rows, same scope, McNemar exact two-sided on the discordant pairs.
  **Kill: A1 ≤ A0 at the declared primary scope.** That would falsify E169's
  design rule *as a retrieval rule*, which is the open question, and would
  close the line.
- **G3 — scope ablation (measurement).** Global versus repo-scoped, for both
  arms. If repo-scoped succeeds where global fails for both arms, the mechanism
  needs the developer to already know the repository, which is a product
  constraint and is recorded as one.
- **G4 — not runnable today (declared, not passed).** Replication on a fresh
  blinded `version_pinned` sample is **NOT RUN**: the Stack Exchange daily quota
  on this host is **7 of 300 remaining**, and E169 consumed the rest fetching
  the pool. Reported as not run, never as a pass.

**Primary scope is `global`** — no repository hint — because a repository hint is
information the developer usually does not have when a version-pinned failure
happens; the repo-scoped numbers are reported as G3 and are the *easier*
variant, never the deciding one. G2's primary comparison is therefore A1-global
against A0-quoted-global, since a developer pasting an error into a search box
quotes it.

## Decision rule, declared before the run

If **G0, V1, V2, G5 pass** and **G2 does not fire** and A1 ≥ 0.30 of rows at
the primary scope, the mechanism is both real and large enough to build on, and
the next session runs the prior-art screen for a symptom-first retriever before
any product code is written. If A1 < 0.30, or G2 fires, the class closes as
served by the thread and no retriever is proposed. **At N = 13 the power is for
large effects only**, and a non-firing G2 is not evidence of no difference.

## Limits, declared

- **N = 13**, one venue (Stack Overflow), one stratum, and rows that are
  tracker-linked — a population biased *toward* having a findable fix.
- One index. Fixes that live only in a forum or a changelog are outside this
  measurement, and E169 measured that the thread, not the tracker, is where this
  population's fixes actually are.
- A hit in the top 10 is reachability, not usefulness, and not adoption.
- Unauthenticated and rate-limited; results are recorded with the query, the
  total count and the returned `html_url`s so anyone can re-run them.

[`RESULT.md`](RESULT.md) will hold the outcome.