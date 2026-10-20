<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E169 RESULT — the error string is the wrong query, and the thread already
carries the fix

**Date:** 2026-10-16. **G1 vacuous. G2 withdrawn. G3 measured. G4/G5 void.**
Search arms withdrawn: their own positive control could not pass (F130).

## What was asked, and what replaced it

E168's addendum named the incumbent mechanism for version-pinned failures —
*search the project's issue tracker with the exact error string* — and named
the cheap measurement of its ceiling. That measurement was run and **withdrawn**,
because the instrument's own control failed:

- treatment arm: **1 of 13** rows reached;
- control (feed each target its own title, require it at rank 1): **3 of 13**,
  then **13 of 13** after the query was rewritten;
- a target's own quoted title returns **17,033,706** hits; a quoted phrase with
  a colon in it returns **8,041,878** against **532** unquoted; `OR` is not
  honoured; `sort=best-match` is accepted and ignored.

A measurement whose positive control cannot pass measures the instrument.
Full detail in [`PROTOCOL-AMENDMENT-2.md`](PROTOCOL-AMENDMENT-2.md) and
[F130](../../FAILURES-findings-41.md).

**The replacement** is deterministic and needs no search engine: **for a query
to return a document, the document must contain something the query names.** So
for each row, fetch the tracker item the thread points at (title, body, first
three comments) and measure what share of the post's distinctive terms its text
contains. A miss is an obstruction; a hit is a lower bound on reachability.

## Population — it shrank twice, and both losses are findings

| | |
|---|---|
| E168's `vp = 1` stratum | 85 |
| **no longer fetchable** (the Stack Exchange API returns zero items for these ids) | **7** |
| measurable | 78 |
| **thread points at a GitHub issue or PR anywhere in its answers** | **13** |
| thread points at `issuetracker.google.com` or a vendor tracker | 3 (`not_exercised`, no public search or fetch surface) |
| thread contains **no** tracker link at all | 62 |

**E168's summary figures do not all reproduce.** G0 recomputed them from
`threads.json` under every URL rule a reader could have used:

| claim | reproduces? |
|---|---|
| "20 of 24 answer sets link out" | **yes** — any URL occurrence in any answer's text |
| "`github.com` in 15 of 24" | **no** — 12 by `href`, 13 counting `gist.githubusercontent.com`; no rule yields 15 |

And the figure that *does* reproduce describes the thread, not the resolution:
in the accepted answer specifically, a tracker link appears in **4 of 24**. The
fix is usually stated inline by the person whose answer was accepted, with the
tracker cited by someone else.

## G3 — the named mechanism does not work as stated

| | |
|---|---|
| rows | 13 |
| median term coverage of the post's query in the fix's text | **0.625** |
| rows with coverage ≥ 0.5 | **9 of 13** |
| rows with coverage 0 | 2 of 13 |
| **rows sharing a 3-or-more-word run with the fix** | **0 of 13** |
| median longest shared word run | **0** |
| rows where the literal is fully contained | 4 of 13 |

**The error string never matches the fix.** Not one row shares three
consecutive words with the document that fixes it. The literal is fully present
in 4 rows and partially in 9, and the shared material is always *words*, never
the message.

**The rows that match best are the rows with no error message.** By hand-read
literal type:

| literal type | n | coverage ≥ 0.5 |
|---|---|---|
| `symptom_only` (the post describes a behaviour, not an error) | 4 | **4** |
| `error_message` | 6 | 3 |
| `ui_string` | 2 | 1 |
| `code_token` | 1 | 1 |

The two zero-coverage rows are both precise errors: `UpdateService error: The
operation couldn't be completed. (OSStatus error -60006.)` against a fix titled
*Code won't update on macOS*, and `Unable to find a destination matching the
provided destination specifier` against a fix about `mprotect failed: 13`.
**The more version-pinned a post is, the more its literal is environment-specific
and the less of it appears in the place the fix is written down.** The
environment-specific tokens — the absolute path `app.component.ts`, the
`@rpath/libgfortran.5.dylib` load path — are what make the post searchable for
the asker and unmatchable for anyone else.

**The query that works is the post's component and symptom words.** This is the
one actionable design rule this session produced, and it is the opposite of the
one E168 proposed: a version-grounding assistant must query *what broke and
where*, not *what the machine printed*.

## G3b — the thread already carries the fix

Coverage of the post's terms against the **whole thread** rather than the
tracker item: **≥ 0.8 on 12 of 13**, and exactly 1.0 on 10. A developer who
reads the thread finds the material; the tracker link is a citation, not the
delivery mechanism. The one row at 0.1429 is the row whose fix coverage was
1.00 — its post is a screenshot with the error in the title, so the thread says
almost nothing and the tracker item says everything.

That is the closure, and it is the fourteenth "served" in this record — the
first one with the mechanism measured rather than asserted. It is served by the
forum thread, at the rate this venue serves everything else.

## G1 — vacuous as declared, and recorded that way

G1 required the extractor's `literal_in_post` label to agree with a hand label
on 20 rows. **Both columns are 1 on all 20 rows** — the extractor found a
literal in every sampled row and so did the reader — so the statistic is 20 of
20 whatever the extractor's quality and cannot fail. Reported as not fired and
not informative. The comparison that can differ is *which* literal the extractor
picks, and on the 13 rows where both existed the extractor's literal was an
**exact** match for the hand-supplied phrase **0 times**. Exactness is what this
counts and correctness is not: on the VS Code `OSStatus` row the extractor did
find the right message and prefixed it with a log timestamp, which is a
defect of precision rather than of recall. On other rows it returned prose
(`'windows 11 with wsl'` for a slow-paste report). The extractor is not retuned.

## Three defects in this session's own instruments

1. **The extractor selects prose.** Written before any body was read, it chose a
   sentence containing "warning" over the Gatekeeper string in the same post.
2. **The comments endpoint returns a bare array**, not `{"items": [...]}`; the
   wrapper assumption raised `AttributeError` on every row of the first run.
3. **Dotted identifiers were scored absent.** A term was compared raw against
   normalised text, so `Docker.app` and `libgfortran.5.dylib` read as missing
   however prominently they appeared. Four rows read zero coverage for a mix of
   world and instrument, and the two were not separable until this was fixed.
   The first run's numbers are superseded; the progress log records the failure.

## What this does not establish

- **Not a service rate for the class.** Containment is a necessary condition for
  a match, not a ranking measurement. "9 of 13 have half their terms in the fix"
  is not "a search engine returns the fix first".
- **Not the search-arm number.** G2 is `withdrawn`, not answered. The honest
  statement is that the ceiling of the real incumbent is **unmeasured from this
  host**, and that containment indicates it is high rather than low.
- **Not a candidate.** No product is proposed; no prior-art screen was run; the
  class is closed as served by the thread.
- **Not generalisable past 13 rows**, which are the tracker-linked rows of one
  stratum of one high-arrival pool, and are therefore a population biased
  *toward* rows with a findable fix.

## What changed

**D114.** "The strongest accessible alternative" must now declare in its
protocol whether it can retrieve, from what index, and what the instrument's
positive control is. Thirteen closures used an alternative that could not
retrieve, and E169's control is what finally established that rather than the
treatments.

**A reusable prototype instrument.** `containment.py` needs no search engine and
no credential, so it reproduces anywhere: it is the cheapest reachability
obstruction screen this mission has, and the next host with search should run it
*beside* a real search arm rather than instead of one.

## Next action

Run the retrieval arm **from a host with web search**, on these same 13 rows and
on a fresh blinded sample, with the query built from symptom and component words
rather than the error string. That is the one question E168 and E169 both leave
open and neither could close: not "is the class served" — the thread answers
that — but "does the mechanism E168 proposed work at all". It is cheap, and it is
the last question standing on this line.

[`PROTOCOL.md`](PROTOCOL.md) ·
[`PROTOCOL-AMENDMENT-1.md`](PROTOCOL-AMENDMENT-1.md) ·
[`PROTOCOL-AMENDMENT-2.md`](PROTOCOL-AMENDMENT-2.md) ·
[`containment.py`](containment.py) ·
[`hand-queries.jsonl`](hand-queries.jsonl) ·
[`g1-labels.jsonl`](g1-labels.jsonl)