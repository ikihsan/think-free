<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# E022 protocol — what becomes of a publicly stated unmet need

Written 2026-10-05, **before any outcome was observed**. T-0066.

## The question, and why it is not another instrument audit

Five consecutive experiments measured the mission's own judgement. Two
(`EXPERIMENTS/020`, `021`) turned outward and asked about agent configuration —
the world, but a sample the mission's own search had chosen.

The one asset no failure in this record has touched is stated in
[`STATE-next-actions.md`](../../STATE-next-actions.md) item 0: **1250 named
people who each wrote down, publicly and unprompted, what was missing from their
work** (`EXPERIMENTS/019`, F039). E012 measured the corpus. E019 measured its
authors. **Nobody has measured what became of any of them.**

That is the outcome variable, and it is readable from public data already
recorded: E019's capture holds `comment_id`, `story_id`, `parent` and `author`
for all 1401 rows, and the Hacker News API serves both the reply tree below a
comment and an author's later posts.

## The falsifiable claim

**For a need statement published in public, the subsequent public record
distinguishes three outcomes — answered in thread, built by the requester, or
left without a response — and the distribution is measurable.**

Scope: need statements harvested by `EXPERIMENTS/012` from Hacker News comments
after 2024-01-01, observed to 2026-10-05 through the public Algolia and Firebase
APIs. **This is a property of one community's public discourse, not of unmet
needs in general.** A need never voiced, or voiced elsewhere, is outside the
population and outside the claim.

## Three outcomes, and the oracle for each

| class | what it means | how it is decided | what can falsify it |
|---|---|---|---|
| `answered` | at least one reply to the comment exists | `kids` non-empty on the Firebase item record | a thread whose replies are all noise; E016's instrument shape |
| `served` | a reply **names an artifact that serves the clause** | hand label on a random sample; the automatic lexical rule is reported beside it and never alone | a label set that disagrees with the lexical rule in one direction only |
| `built_by_requester` | the same author posts a **story** after the need statement | Algolia `tags=author_X`, filtered to `type=story` with `created_at` after the need's date | an unrelated later story counted as a build; a false positive here is worse than a false negative, so it is hand-checked |

**`answered` is not `served`.** A reply can be noise. The mission has been
burned by an instrument that answers the easier question (F036: an engine
returning HTTP 200 with ten well-formed results for each of 38 queries, every one
unrelated). The `served` cell therefore carries a hand-labelled denominator, and
the headline number is never the automatic one.

## Strongest existing alternative, named before running

**The alternative is that outcome is not about the need at all.** Three ways this
could be true, and the control that defeats each:

1. *Thread popularity drives everything.* A need on a popular thread gets
   replies because the thread is popular. **Defeated by a within-thread
   control:** reply rate of need-bearing comments against reply rate of the
   corpus's non-need comments in the *same* story. The claim that survives is the
   **lift**, not the rate.
2. *`i wish there was` is a rhetorical habit, not a need.* **Defeated by
   trigger-stratifying:** the corpus's largest trigger class (749 of 1401) is
   `i wish there was`, and the distribution is reported per trigger so a single
   dominant phrase cannot carry the headline.
3. *The requester built it and said so elsewhere.* **Defeated by the author
   join**, which is the third outcome class and the only one that can produce
   anything buildable.

## Controls

- **Positive control (C1).** 20 comments the corpus already contains a `prior_art`
  verdict for (`EXPERIMENTS/012/raw/screened.jsonl`). Their `served` rate is
  reported beside the rest. A prior-art verdict is a supply judgement; this
  measures whether the thread agreed.
- **Negative control (C2).** 20 comments in the same stories that match **none**
  of the 23 trigger phrases. If the `answered` rate does not differ, the trigger
  vocabulary carries no information and the lift is zero — reported as `not
  informative`, not as a finding.
- **Nonsense control (C3).** The instrument is asked for the reply tree of a
  fabricated comment id. A `200` with content is a falsifier of the reader, not a
  result. Mirrors F036.

## Gates, declared before observing

- **Gate A1 (population read, ≥95%).** At least 95% of 1401 rows resolve to a
  readable item record. **A failed row is `unreadable`, never `unanswered`.**
  This is the exact failure of E020, where a rate limit answered HTTP 200 with
  an HTML challenge and 33 rows read as "the index does not contain the young
  arm".
- **Gate A2 (lift, declared before the first fetch).** If the within-thread lift
  of `answered` for need comments over non-need comments is **not greater than
  1.0**, the trigger vocabulary carries no information about being answered and
  the experiment reports `not informative`. This is a **real possibility** and
  is not a failure of the run.
- **Gate A3 (build arm).** If the author join yields no story-posted-after-need
  rows at all, the arm is `not evaluable` and no rate is reported for it. A
  missing arm is named, not defaulted to zero.

## What this licenses, stated in advance

**This experiment produces a population statistic, not a candidate.** The
record's rule is that a need statement still owes a mechanism, a
differentiation and an adoption path (D050). A distribution over outcomes
licenses at most one thing: it says whether the "1250 named people" asset is a
population of *unmet* needs or a population of needs that were *served and
absorbed*. That changes item 0's reasoning. It does not select a product, and
`STATE-next-actions.md` item 12 (do not build a product) is not reopened.

**If the distribution comes out mostly `answered` and `served`, the finding is
that the corpus records needs the world had already met** — which strengthens
F029 rather than reopening it. That outcome is expected to be at least partly
likely and is not a reason to run the experiment differently.

## Honest limits, declared before running

- **One community.** Hacker News commenters are a self-selected technical
  population. Every rate here is about HN and about nothing else. No figure in
  this experiment may be generalised to unmet need in general.
- **A corpus drawn for a prior purpose.** E012 harvested by trigger phrase, not
  by a sample of needs. Its composition is the subject of A2's stratification,
  not a hidden assumption.
- **Observation window.** Replies and stories are read once, on 2026-10-05, via
  two APIs. Neither is snapshotted, so a `kid` added later is invisible. Stated
  as a limit, not corrected for.
- **The `built_by_requester` arm cannot see a build posted elsewhere.** A person
  who built the thing and posted it to GitHub rather than HN reads as
  `unanswered`. The arm measures HN self-disclosure, which is a lower bound on
  building and not an estimate of it.
