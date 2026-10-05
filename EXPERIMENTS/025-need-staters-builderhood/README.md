<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E025 — are the people who state needs people who build?

**Date:** 2026-10-05. Task T-0069. Protocol written before the first fetch:
[`PROTOCOL.md`](PROTOCOL.md).

## The question

E022 measured what became of 1401 publicly stated needs. Two of its numbers stand;
the third, **built by the requester: 0 of 24**, the record itself labels a *floor on
disclosure* rather than an estimate of building, because the arm could only see a
builder say so on Hacker News.

That 0/24 has since been promoted past what its instrument can carry.
[`STATE-next-actions.md`](../../STATE-next-actions.md) item 0 reads it as *"the
people who state a need are not the people who build it"* and item 0d uses it to
close the demand-side corpus as a generator. **Self-disclosure is exactly what that
sentence denies**, so two worlds fit the zero:

- **W1** — need-staters do not build. The corpus records needs the world absorbs
  conversationally, and closing it is right.
- **W2** — need-staters build at an ordinary rate and the arm could not see it. The
  corpus is a population of builders whose disclosure is not their building.

**H1.** Among the 1250 distinct authors of the corpus, the rate of having ever
publicly shipped something is materially higher than among a control arm of
commenters in the *same stories* who matched no trigger phrase. W1 predicts no
difference; W2 predicts a large one.

## What the run found

`observed`, 2026-10-05, every figure from `results.json` via `stats.py`.

| arm | authors | with ≥1 `show_hn` | rate | Wilson CI95 | refusals |
|---|---|---|---|---|---|
| **need** (stated a need) | **1250** | **278** | **0.2224** | [0.2002, 0.2463] | **0** |
| **control** (ordinary commenter, same stories) | **500** | **139** | **0.2780** | [0.2405, 0.3188] | **0** |

| gate | declared | result |
|---|---|---|
| A1, instrument validity | ≥ 6 of 6 verified positives, nonsense 0 | **6 of 6**, nonsense **0** |
| C1, the floor | need rate < 0.05 → `not_evaluated` | 0.2224, **not met** — evaluable |
| A2, positive | ≥ 2× control and disjoint intervals | ratio **0.800**, intervals **overlap** — not met |
| B1, kill | intervals overlap | **met. H1 fails.** |

**H1 fails, and it fails in the direction opposite to the hypothesis: need-staters
announce *less* than ordinary commenters in the same stories (0.80×), not more.**
This is a decisive negative, not an unresolved one — 1750 authors, zero refusals,
and the intervals overlap across nearly their whole width.

**W1 stands, and the strongest form of the record's sentence survives.** The
disclosure-floor reading (W2) is **not** supported: the instrument that E022's arm
lacked was available, and it finds need-staters are if anything *under*-represented
among builders. Item 0d's closure of the corpus is **confirmed rather than
withdrawn**, and the caveat attached to F042's third number is now a measurement
rather than an excuse.

**The number that matters most is the need arm's own: 22.2%.** More than a fifth of
the people who publicly wrote "is there a tool that…" have publicly shipped
something on Hacker News. So the sentence *"need-staters are not builders"* is
**false as an absolute** — a fifth of them demonstrably are. What the measurement
supports is the relative and weaker claim: **they build less than their
neighbours**, and the rate at which they build **what they asked for** remains the
0-of-24 floor it always was. F042's third cell is not repaired; it is bounded.

## Three things this does not say

1. **It does not reopen the corpus.** F029's 0 of 50, F039's 1250 individuals and
   the closure in item 0d are untouched. A population that builds *something else*
   is not a population of standing unmet need.
2. **It does not reopen any prior-art death.** Nothing here concerns what exists.
3. **It does not rehabilitate E022's `served` figure.** That was withdrawn by F043
   on its own control and nothing here bears on it.

## The instrument, and the defect it carries

The instrument is one Algolia query per author for items tagged both that author and
`show_hn`, counting `nbHits`. Two limits are structural and one was found by running
it:

**The floor is inherited, not lifted.** The tag is set by HN, not by the author, so
this cannot see a build that was never announced — the same blindness E022's arm
had. It is therefore a *lower bound on disclosure*, and it is a lower bound on both
arms equally. It measures disclosure, and it says nothing about whether what was
built was good, used, or related to the stated need.

**The confounder is severe and is reported, not corrected.** Within the control
arm, authors with a `show_hn` post have a **median 2416 total HN items** against
**467** for authors without one. `show_hn` is therefore heavily confounded with
overall HN activity: HN selects heavy posters into it. This is exactly why the
control arm is drawn from the need arm's *own stories* rather than from HN at
large — a control taken from HN generally would be dominated by heavy posters and
would read as "everyone builds". The exposure is shared, but a control arm with a
**different** activity distribution would still move the ratio, and the realised
control arm has a slightly higher rate than the need arm.

### The control set was wrong before it was corrected

PROTOCOL.md's Gate A1 originally named four accounts *believed* to have shipped a
`Show HN:` item. **Two of the four returned 0**, and reading all their indexed
stories shows why: `patio11` and `chromium` have no post whose title begins
`Show HN` at all. They were never positive controls, and the instrument had
recovered the tag correctly in both cases.

That is F036's shape — a control asserted positive by belief rather than verified
against what it is a control for — and it nearly produced a **false positive**:
reading "4 of 4" as a pass. The correction was made by sampling the `show_hn` tag
itself, before either arm had run, with the four originals **kept in the capture
with their zeros**. `tests` in
[`test_gates_falsified.py`](test_gates_falsified.py) assert that the two empty
controls stay recorded as empty, so a later reader cannot quietly restore them.
The gate threshold was never moved; only the membership of the control population
was corrected.

### Two limits of the design, declared

The arms are **not matched on tenure**: the need corpus spans 2024-01-01 onward
while control authors come from the same stories, so the window is shared but
membership is not. And the control arm stopped at the **declared 500**, which
resolves a 2× ratio to about ±0.035 — ample for this gate, and *not* a claim that
1250 control authors would have given the same ratio.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/025-need-staters-builderhood/fetch_authors.py
tools/x -- python3 EXPERIMENTS/025-need-staters-builderhood/fetch_control.py
tools/x -- python3 EXPERIMENTS/025-need-staters-builderhood/stats.py
python3 -m unittest discover -s . -p 'test_*.py' -t .
```

15 falsification tests, each asserted against a fixture built to break the property:
a refused fetch must not become a zero, an unread arm must not read as "no
overlap", a malformed raw line must not shorten a denominator, and the Wilson
interval for 0/24 must equal the [0.0, 0.138] the record quotes for F042.
