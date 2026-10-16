<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E169 — can the developer reach the fix with the error string? (prototype +
reachability measurement of the incumbent mechanism)

Predeclared **before any thread body of the additional 61 rows is read, and
before a single search request is issued.** E168 named this as its cheaper
decisive version; this protocol fixes the population, the query, the ranking
rule, and the numbers that would change a build decision.

## What it replaces, and why

E168's G3 ("ground an attempt in the component's published version history")
was declared unrunnable on its own 24 rows, because that session had read
every thread and a grounded attempt would be contaminated. **Contamination is
a property of writing an answer, not of measuring a search.** No assistant
attempt is graded here: the instrument is a script plus a recorded reader, so
the 24 rows are usable and so are the other 61.

E168's addendum named the incumbent mechanism explicitly: *search the project's
issue tracker with the exact error string and read the linked fix*, already
done by hand in minutes. It also named the cheap measurement of that
mechanism's ceiling: take the exact error string from each post, query, and
check whether the linked source surfaces. That is this protocol.

## The question

For a version-pinned failure post, **what share of the posts contain a literal
error string that a developer could paste into a search engine**, and **of the
posts where the resolution lives in a public issue tracker, what share does
querying that tracker with the post's own error literal return the resolution
within the first 10 results?**

## Population

- **All 85 `vp = 1` rows** of E168's pool
  (`EXPERIMENTS/168-version-pinned-need/classified.jsonl`), not the 24.
  Declared: `in_e126_graded40` reads `false` on all 85 because E168 wrote
  `question_id` as a string in one file and an int in the other (its recorded
  defect 1); the 20 overlapping rows are therefore included here.
- The 24 rows already fetched are **reused, not refetched**
  (`threads.json`). The other 61 are fetched from the Stack Exchange API,
  bodies and answers both, answers sorted by votes.
- No new pool, no new classifier. `vp` labels are E168's, unchanged.

## Instrument — `vpsearch.py`

A prototype of the mechanism, so the measurement and the artifact are the same
thing. Per row:

1. **Extract error literals** from the question body (HTML-stripped). A
   *literal* is a quoted or code-delimited span of ≥ 15 characters, or a line
   matching `error|exception|warning|fail` case-insensitively. The **primary
   literal** is the longest candidate; ties break toward the one containing a
   digit or an all-caps token.
2. **Classify the row's reachability target** from the accepted answer: the
   first `github.com` issue/PR/commit URL in the highest-scored answer. Rows
   without one are `no_tracker_target`, not "unreachable".
3. **Query** `api.github.com/search/issues?q="<literal>"` and record the
   1-based rank at which the target URL's path appears, up to 10 results.

Unauthenticated search is 10 requests/minute, so the run paces at 6.5 s/query.
No credential is used, so the run is reproducible on any machine with the same
public API.

## Gates, declared before the run

- **G0 — population integrity.** The record's summary figures ("20 of 24 answer
  sets link out, `github.com` in 15 of 24") must be recomputed from
  `threads.json`. Whatever rule reproduces them is recorded. A figure that no
  rule reproduces is recorded as **not reproducible**, with the nearest
  reproducing figures beside it.
- **G1 — extractor validity.** On 20 `vp = 1` rows drawn by a stated rule
  (every 4th row of the population in descending `view_count`), the reader
  assigns `literal_in_post` by hand and the script's label is compared.
  **≥ 18 of 20 agree, or the script's rate is not reported.** Below 16 of 20
  the extractor is void and the run stops here; between 16 and 18 the rate is
  reported with the agreement figure attached, and **the extractor is not
  retuned and re-reported.**
- **G2 — incumbent reach (one-sided).** Over rows with a GitHub tracker
  target: share returned within the top 10 by the single exact-literal query.
  - **≥ 0.70 → closure.** GitHub's issue index is what a general engine
    indexes for this content, so a single query reaching the fix is a *lower
    bound* on the incumbent, and the class is served by the workflow developers
    already use.
  - **< 0.40 → open.** The fix exists and the developer's own query does not
    return it. That is a candidate direction; prior art runs before any code.
  - 0.40–0.70 → **inconclusive**, reported as such. No build.
  - Fewer than 8 rows with a target → `not_exercised`, not 0.
- **G3 — no-literal residue.** Over all 85 rows, share where the post contains
  **no literal the extractor can find** — where "paste the error string" is
  not available as the first move. **≥ 0.25 names a residue with a mechanism**
  (the symptom is not text) and the next action is to size it on a fresh pool.
  < 0.25 → no residue by this mechanism.
- **G4 — query variant.** The single exact-literal query is primary. A
  secondary arm re-queries with the literal plus the most specific tag as a
  second query, up to 2 retries, because a human iterates. Reported separately;
  it can only raise G2 and is reported as `inferred` reach.

## Failure conditions declared in advance

- The G0 figures do not reproduce → recorded, and the run continues; the
  reachability number does not depend on them.
- A row's question body is empty or missing → `not_measured`, counted, never
  silently dropped.
- GitHub returns 403 or a rate-limit body → the row is retried once at double
  the delay, then recorded `unreadable`. **Unreadable is never counted as
  "not reached"** — a read failure is not an outcome.
- Any G2/G3 number reported from a population smaller than the gate's
  denominator is reported as the number it is, with the denominator visible.

## What this cannot decide

- **It is not a product test.** Nothing is built here except the prototype that
  performs the queries.
- **It is not a measure of a retrieval-enabled assistant.** GitHub issue search
  is a lower bound on that arm, not the arm. A result of "reached" closes the
  class; a result of "not reached" does **not** by itself open a candidate.
- **It is not a rate for Stack Overflow.** These are high-arrival rows of one
  stratum of one pool, selected by E126's arrival rule.
- **The reader in G1 is me**, and the extractor was written by the same reader.
  G1 is the falsification of that, not an independent check.