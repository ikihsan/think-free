# E029 — protocol amendment 1

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Declared 2026-10-05, after the population build and the fetch, before any reader
saw a pair and before any reader label exists.** The thresholds in
[`PROTOCOL.md`](PROTOCOL.md) are unchanged. This amendment fixes two things the
original protocol did not specify, which the fetch made unignorable.

## 1. The population must be restricted to builds that postdate the need

The original population was the 241 eligible need-staters. Fetching what they
actually shipped showed that **only 74 of the 241 shipped anything at all after the
need statement**, and **167 of 241 shipped only before it**.

A build cannot answer a need stated after it. The original population therefore
contained 167 rows where the question *"did they build what they asked for?"* is
**not askable**, and reading them as `unrelated` would have manufactured a null.

**The reader population is the 74.** The other 167 are not discarded: they are
reported separately, because the split is itself the observation (below).

The chronological test is **HN item id ordering**, not a timestamp. That proxy is
verified, not assumed: across the corpus's own 1401 need statements, sorted by
`comment_id`, **0 of 1400 adjacent pairs** go backwards in epoch time over a
466-day span. `story_id` was checked as a negative control and does *not* hold
(388 of 1400 backwards), so the two id spaces are not interchangeable and the
comparison uses item ids on both sides.

**Declared selection effect, reported rather than corrected:** the 74 eligible
authors have a median of **4** total `show_hn` items against **2** for the 167
ineligible. Being eligible means having a later item, so the eligible population is
enriched for prolific builders, and E025 already measured `show_hn` as confounded
with overall HN activity. Both the comparison and this experiment inherit it.

## 2. Which shipped item the reader is shown

The original protocol did not say, because it assumed one build per author. The
observed distribution is **44 of 74 with exactly one** item after the need, and a
maximum of 12.

**Declared rule: show the reader every `show_hn` item whose HN item id exceeds the
need statement's item id, with no cap.** No truncation and no "most recent" choice,
so nothing is selected for convenience. Items were already re-checked against the
`show_hn` tag in `_tags` at fetch time, because the API's tag filter is an OR on
repeated parameters and the answer is re-verified rather than trusted.

## 3. Sample size

The gates in `PROTOCOL.md` are written in terms of CI bounds and were declared for
40 rows per arm. The population turned out to hold **74**, and reading all of them
costs no additional fetch. **The reader arm is 74 matched + 74 mismatched = 148
rows per reader, not 40 + 40.** This strengthens both arms equally, was fixed
before any label exists, and cannot manufacture a separation.

The mismatched arm pairs each of the same 74 builders with a need statement from a
**different** author, by a seeded derangement with no self-pairing, using
`random.Random(2901)`.

## What the split itself says, recorded before the reader runs

The one thing already established by the fetch, with no label and no reader
involved:

> **Among the 241 eligible need-staters who have publicly shipped something, 167
> shipped it before they stated the need and 74 after.**

That is a direction, not a null. It says the population is not chiefly "people
waiting for a tool" but substantially **people who had already built something and
then hit a gap they did not close.** E025's `22.2% have shipped something` is
consistent with this and had not been read this way, because nobody had asked
*when*. It does not by itself reopen item 0d — a gap you did not close is still a
gap you did not close — but it changes what the corpus is, and it is the reason the
reader population had to shrink.

## Unchanged

The kill and survive gates B1/B2, the refusal gates A2/A3/C1/A4, the lexical arm's
"feeds no gate" status, and the story-title control as the arm that can kill H1.
