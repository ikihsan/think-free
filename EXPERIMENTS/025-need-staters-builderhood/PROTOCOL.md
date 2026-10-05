<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E025 protocol — are the people who state needs people who build?

**Written 2026-10-05, before the first author is fetched.** Task T-0069.
Declarations here are fixed before any number below is observed.

## The question, and why it is not E022's question

E022 measured what became of 1401 publicly stated needs (F042). Two of its three
numbers stand. The third, **built by the requester: 0 of 24**, was itself declared
a *floor on disclosure* rather than an estimate of building, because the arm could
only see a builder say so on Hacker News.

That 0/24 now carries more weight than the record gives it. `STATE-next-actions.md`
item 0 reads it as "the people who state a need are not the people who build it",
and item 0d uses it to close the demand-side corpus as a generator. **The
instrument that produced it is self-disclosure, and self-disclosure is exactly what
the sentence denies.** A population that never announces its builds is
indistinguishable from a population that does not build.

So two worlds fit 0/24 and the record cannot currently tell them apart:

- **W1.** Need-staters do not build. The corpus records needs the world absorbs
  conversationally, and closing it as a generator is right.
- **W2.** Need-staters build at an ordinary rate and the arm could not see it. The
  corpus is a population of *builders* whose disclosure is not their building.

**H1.** Among the 1250 distinct authors of the need corpus, the rate of having
ever publicly shipped something on Hacker News is **materially higher** than among
a control arm of commenters in the same stories who matched no trigger phrase.
W1 predicts no difference; W2 predicts a large one.

This is the missing arm of F042's third cell, and it is measured by the **same
public corpus E022 already used**, with the control construction E023 established.

## Instrument, and the single defect it can have

For each author, one request to the Hacker News Algolia index for items carrying
**both** that author and the `show_hn` tag. `show_hn` is assigned by HN itself to
posts that ship something; a post without it is a question or a comment.

The defect that matters is **confounding HN's own selection**: people who post a
`show_hn` item are, by construction, people who also post to HN, so a naive rate
measures *posting activity*, not building. This is why the control arm is not
optional and why it is drawn from the **same stories and the same comment
positions** as the need arm, not from HN at large.

**Known limits, declared before the run.** The tag is set by HN and not by the
author, so a builder who never announces is invisible to it — this instrument has
the *same* disclosure floor E022's arm had, and any positive reading is a lower
bound rather than a rate. `show_hn` is about announcing on one platform; it is not
about building anything. A small share of the population, not the whole. Nothing
here measures whether what they built was good, used, or related to their need.

## Gates, declared before the first fetch

**Gate A1 (instrument validity).** The `show_hn` tag must be recovered for **6 of 6**
positive controls and must return **0** for a nonsense account name. Fewer than 6
and the finding becomes a statement about the instrument.

**Gate A1 correction, 2026-10-05, after the first controls ran and before either
arm completed.** The control set was originally four names *believed* by the
author to have shipped a `Show HN:` item. Two of the four returned **0**, and a
direct read of all their indexed stories shows **why**: neither `patio11` nor
`chromium` has any post whose title begins `Show HN`. They are not builders of
HN-announced things at all, so they were never positive controls. The instrument
recovered the tag correctly in both cases and the *control set* was wrong.

That is F036's shape — a control declared positive by assertion rather than by
reading what it is a control for — and it is recorded as an instrument defect in
[`README.md`](README.md) rather than quietly replaced. The controls were then
chosen **by sampling the `show_hn` tag itself**, so each one is verified positive
by the same evidence the gate tests, and the four originals were kept in the
capture with their 0s. `pg` (1) and `antirez` (2) survive unchanged.

The gate threshold is unchanged at 6 of 6; only the membership of the control
population was corrected, and the correction was made against the instrument's
own output rather than against any figure from either arm.

**Gate A2 (positive gate, H1 survives).** The need arm's `show_hn` rate is
**at least 2x** the control arm's, with the two Wilson intervals not overlapping.
W2 is supported and item 0d's closure rests on the instrument, not on the world.

**Gate B1 (kill gate, H1 fails).** The two arms' intervals overlap. W1 stands,
E022's 0/24 is confirmed rather than withdrawn, and the corpus stays closed. **A
pass and a fail are both findings**; neither reopens a prior-art death.

**Gate C1 (the floor, declared so it cannot be reinterpreted).** If the need arm's
raw rate is below **5%**, then even a 2x control rate describes a minority of the
population and the sentence item 0d wants cannot be carried by it in either
direction. The verdict is reported as `not_evaluated` for *who builds*, and only
the null is reported.

**Arm sizes, fixed before fetching.** All 1250 need-arm authors. The control arm
is drawn from E023's control comments (`EXPERIMENTS/022-need-outcomes/raw/control.jsonl`),
which are ordinary comments in the need arm's own stories, restricted to answered
comments so both arms share the "a reply exists" condition. Target **1250** control
authors, the maximum the capture supports; if fewer distinct authors exist, the
realised number is reported and the intervals are computed on what was fetched.

### Stopping rule for the control arm, declared after the need arm and before any control figure

Written at 2026-10-05, when `raw/control_arm.jsonl` **did not exist**. No control-arm
`show_hn` count had been observed at the moment this rule was written, and the rule
is on that basis — a rule chosen after seeing the control rate would be a threshold
tuned on the evaluation data, which the protocol forbids.

Resolving all 13409 control comments one item-fetch each costs far more than the
decisive comparison needs, and it does so *before* producing a single control-arm
count. The rule therefore stops at the **first of** these conditions, checked after
each batch of 100 probed control authors:

- **500 control authors probed.** At a rate near the need arm's, 500 gives a Wilson
  half-width of about 0.035, which resolves a 2x ratio comfortably; the gate is a
  factor-of-2 comparison and does not need the full 1250.
- **E023's control capture is exhausted.** If distinct authors run out first, the
  realised number is reported.

Control authors are taken in the capture's own order, deduplicated, and **no arm
figure may be read until the stopping condition is met.** The stopped-at number,
not the target, is what `results.json` reports, and it is reported as reached
rather than as chosen.

**No threshold is tuned on the data.** Both rates, both Wilson intervals and both
arms' denominators are written to `results.json` whatever they are.

## What would make this worth running again

Nothing here selects a candidate, and nothing here reopens a prior-art death. The
run is worth exactly one thing: it decides whether a **0** in the mission's only
demand-side measurement is a fact about people or a fact about a disclosure
channel. If it returns `not_evaluated` under Gate C1, that is a positive result
about the instrument's ceiling and the run does not repeat without a different
instrument.

## Commands

```bash
tools/x -- python3 EXPERIMENTS/025-need-staters-builderhood/fetch_authors.py
tools/x -- python3 EXPERIMENTS/025-need-staters-builderhood/stats.py
```
