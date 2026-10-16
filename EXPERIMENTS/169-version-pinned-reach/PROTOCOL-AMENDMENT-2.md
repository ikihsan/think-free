<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E169 AMENDMENT 2 — the reachability instrument is containment, not a search

Recorded **after two instruments failed and before containment was run.**

## What failed, and why it matters more than the number it produced

Step 4 measured reachability by querying GitHub's unauthenticated
`/search/issues` with the post's own error string and got **1 of 13**.
Step 5 ran the control that was supposed to license that number: feed each
target its own title and require it back at rank 1. The control failed on
**3 of 13**, then on **13 of 13** after the query was corrected, and it is the
control, not the treatment, that decided this. The totals say why:

| query | hits |
|---|---|
| `"Missing Anthropic Sonnet 4 model with Bring Your Own Key from Github Copilot Chat and Agentic mode"` (a target's own title) | **17,033,706** |
| `"error: mprotect failed: 13 (Permission denied)"` | **8,041,878** |
| the same words unquoted | 532 |
| `"Sonnet" OR "Copilot"` and `Sonnet OR Copilot` | **11,087,649** each |
| `/search/issues` with `sort=best-match` | the value is accepted and ignored; no usable ordering from here |

So a quoted phrase is not matched as a phrase, `OR` is not honoured, there is
no relevance ordering, and a colon inside a phrase appears to break the parse.
General web search is unavailable from this VM (`Web search cancelled`;
DuckDuckGo and Bing refuse, and Bing answers **200 with results unrelated to
the query**, which is worse than a refusal because it looks like an answer).

**The 1-of-13 and 0-of-13 numbers are withdrawn, not adjusted.** A measurement
whose own positive control cannot pass is not a measurement of the world.

## The replacement

For a developer's query to return a document, the document must contain
something the query names. That is a **necessary** condition, and it is
deterministic: no search engine, no ranking, no credential, and it reproduces
on any machine with the public API.

**Containment.** For each row, fetch the tracker item the thread points at
(issue title, body, and its first three comments) and measure what share of
the post's distinctive terms its text contains.

- a **miss is an obstruction**: a term absent from the fix's text cannot be
  matched by any query that names it, so the developer's first move cannot
  work, whatever engine is used;
- a **hit is a lower bound** on reachability: the fix is findable by whatever
  engine indexes that tracker;
- it needs no ranking, so it is not defeated by this VM's search defects.

## Two things containment cannot separate, recorded before the run

1. **A bad link from a bad answer.** If an answer points at a tracker item that
   has nothing to do with the post, containment reads low — and the cause is the
   answer, not the need. The decomposition is measured too: coverage against
   **the whole thread**, which separates "the tracker is unreachable" from
   "the answer never needed a tracker because it stated the fix inline".
2. **Containment is necessary, not sufficient.** Full containment says a
   phrase search *could* match; it does not say the result is ranked first.
   Every claim below is written as a necessary-condition result.

## A defect in the containment instrument, found and repaired

The first run compared each post term **raw** against text that had been
normalised, so every dotted identifier (`Docker.app`, `libgfortran.5.dylib`)
was scored absent however prominently it appeared. Four rows read zero coverage
partly because of the world and partly because of the instrument, and the two
were not separable. Terms are now normalised the same way the fix text is.
The first run's numbers are superseded by the second; the instrument's own
progress log records the failure rather than hiding it.

## Also recorded: the declared G1 gate could not fire

G1 was "the extractor's `literal_in_post` label must agree with a hand label on
20 rows". On the 20-row sample **both** columns are 1 on every row, so the
agreement statistic cannot differ from 20 of 20 whatever the extractor's
quality. The gate is **vacuous as declared** — the fifth such gate in this
record. The comparison that *can* differ is not whether a literal exists but
which literal the extractor chooses, and on the 13 rows where both were
available the extractor matched the hand-supplied phrase **0 times**. G1 is
reported as not fired and as not informative, and the extractor is not
retuned.