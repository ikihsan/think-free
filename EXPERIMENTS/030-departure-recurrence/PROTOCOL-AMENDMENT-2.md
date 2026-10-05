# E030 — Amendment 2

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, before `harvest.py` fetched anything.** Found by running one
page of the harvest against a field-shape check, not by reading a rate.

## The defect this fixes

The protocol's corpus table is **phrase-exact**: the volumes were probed by putting
double quotes inside the query, so Algolia matched the whole phrase. The first
implementation passed the phrase bare, and Algolia matched it as a conjunction of
terms:

| framing | table | bare phrase, one page |
|---|---|---|
| `migrating from` | **529** | **7204** |

Both numbers are correct for what they ask. Bare terms would have admitted every
comment containing the word *migrating* and the word *from*, which is a large part
of HN, and the framing's job is to mark a comment as **about** leaving something.
So the harvest is **phrase-exact**, and the protocol's table stands.

## The arithmetic in the protocol was also wrong, and is corrected here

The protocol says *"the eight high-precision framings give ~6 500 comments before
filtering"*. Its own table sums to **18 186** across those eight rows, not 6 500.
The sentence is withdrawn and replaced by what is true:

- the eight non-vague phrasings hold **18 186** post-2024 comments *in total*;
- Algolia will not page past **1 000 hits per query**, so a pass is capped at
  **1 000 per framing** and at **500** under Amendment 1;
- the ceiling therefore binds on six of the eight, and the **maximum obtainable
  harvest is 2 456 comments** (8 + 94 + 359 + 529 + 500 + 500 + 500 + 14 for the
  eight; 2 442 without `insteadof`).

`insteadof` (14 comments) is **dropped from the harvest**: it is a
configuration-directive token, not a departure account, and a 14-row framing
cannot carry a rate. That is an exclusion made before any rate, and it is the only
framing in the table that is not harvested. The harvest runs **seven** framings.

## One more fix, declared here because it changes what a "body" is

Algolia returns `comment_text` **HTML-escaped** (`&#x27;`, `&quot;`, `<p>`). The
first implementation stripped tags and left the entities, which would have counted
`p`, `code`, `a` and `href` as content words. Harvest unescapes entities and strips
tags, in that order. `<code>` and `<a href>` text is **kept**: a tool named in a
link is the most common way a departing artifact is named on HN.

## What this does not change

No gate, no threshold, no rate definition and no arm definition moves. The three
declared gates that could refuse the experiment — A1 fetch validity, A2 positive
control, A3 nonsense control — are unchanged, and A4's floor of 300 accounts per
arm is now harder to reach than the protocol's arithmetic implied, which is the
correct direction for a kill gate and is declared rather than discovered.
