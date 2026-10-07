<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E029 — do the people who stated a need build that need?

**Date:** 2026-10-05. Task
[`T-0073`](../../tasks/T-0073-test-whether-the-need-staters-who-publicly-shipp.md).
Protocol declared before the first fetch
([`PROTOCOL.md`](PROTOCOL.md)), amended three times before any rate was computed
([`1`](PROTOCOL-AMENDMENT-1.md), [`2`](PROTOCOL-AMENDMENT-2.md),
[`3`](PROTOCOL-AMENDMENT-3.md)). One rubric for both readers
([`RUBRIC.md`](RUBRIC.md)). Numbers from `results.json` via `stats.py`.

## Verdict: `not_evaluated`, on two counts

| gate | declared | result |
|---|---|---|
| **A1**, fetch validity | ≥ 95% of attempted rows answer | **241 of 241** |
| **A2**, controls | 6 of 6 positive accounts ≥ 1 item, nonsense 0 | **6 of 6, and 0** |
| **A3**, reader agreement | **κ ≥ 0.6** | **κ = 0.5004** — fails |
| **C1**, the negative control | matched − mismatched ≥ 0.20 | **0.0405** — fails |
| **B1**, kill | matched upper ≤ either control's upper | does not fire |
| **B2**, survive | matched lower > both control uppers | does not fire |
| **A4** | fires if A2, A3 or C1 fails | **fires** |

**Neither reader's arm clears any declared bar, and the instrument itself is not
established.** A3 failing is the deeper of the two: the labels do not meet the
agreement floor the protocol set, so the rates below are not yet a measurement.

## The one thing the run established, which needed no reader

This is the result, and it came from the fetch rather than the labels:

> **Of the 241 need-staters who have publicly shipped something, 167 shipped it
> *before* they stated the need. Only 74 shipped anything after it.**

A build cannot answer a need stated after it, so **69% of the population was never
askable.** The experiment as first written would have read 167 rows as `unrelated`
and manufactured its own null. `PROTOCOL-AMENDMENT-1.md` exists for that reason.

It also says what the corpus is, which nothing before it had: not chiefly people
waiting for a tool, but substantially **people who had already built something and
then hit a gap they did not close.** E025's `22.2% of need-staters have shipped
something` is consistent with this and had never been read this way, because nobody
had asked *when*.

**The proxy this rests on was falsified, not assumed.** Selection is by HN item-id
ordering. [`verify_chronology.py`](verify_chronology.py) samples four authors from
each side of the claimed cut and fetches real `created_at` for the need comment and
its first three shipped items: **8 of 8 authors agree, 0 disagree, 0 unreadable**
([`raw/chronology_verification.jsonl`](raw/chronology_verification.jsonl)). A
negative control is in the same test: `story_id` is *not* monotone (388 of 1400
adjacent pairs regress), so the two id spaces are not interchangeable.

## What the readers said, reported as description and not as a verdict

Both readers read the same 222 blinded rows from the same frozen bytes
(md5 `d604f1f9…`), blind to arm, author, story and thread. A row counts in the
primary rate only when **both** readers say `addresses` — a rule fixed in the scorer
before any label existed.

| arm | both readers `addresses` | rate | CI95 | either reader | observed agreement |
|---|---|---|---|---|---|
| **matched** — own need, own builds | **3** / 74 | 0.0405 | [0.0139, 0.1125] | 3 | κ 0.664 |
| **mismatched** — own need, another's builds | **0** / 74 | 0.0000 | [0.0000, 0.0494] | 0 | κ 0.634 |
| **story_title** — thread title, own builds | **2** / 74 | 0.0270 | [0.0074, 0.0933] | 3 | κ **0.307** |

**The two readers independently named the same three matched rows** — `M72`
(stylometry as a generation-time style prior, against a writing-profile tool), `M43`
(scheduled coding agents, against a scheduled-agent runner) and `M66` (an OCR
benchmark, against an OCR leaderboard) — and **neither named a single one of the 74
cross-paired rows.** The direction is what H1 predicts.

It is also far too small, and too imprecise, to be anything else. The descriptive
block (computed after the labels existed, **feeding no gate**, declared in
`results.json` so its provenance is on the record):

| quantity | value |
|---|---|
| matched − mismatched | 0.0405, CI95 **[−0.0156, +0.1125]** |
| matched − story_title | 0.0135, CI95 [−0.0579, +0.0881] |
| Fisher exact, two-sided | p = 0.245 |

**So the data are consistent with a separation anywhere from about −0.02 to +0.11.**
They cannot establish one and they do not exclude zero. Against the thread-topic
control — the arm that can kill H1 — the separation is essentially nil.

## The lexical arm, which is what found the worst defect

Reported with its control and feeding **no gate**, because E028 measured lexical
coverage as `informative: false`:

| arm | mean content-word overlap | rows with zero overlap |
|---|---|---|
| matched | 0.044952 | 32 / 74 |
| mismatched | 0.023632 | 40 / 74 |

The treatment arm carries about 1.9× the word overlap. **This is not evidence** — it is
the reading that exposed the replicate control, below, which is the reason it exists.

## Three defects, all in this run's own instrument

Recorded because two were found by tests written before the data existed and one by
an arm with no incentive to look right. None was found by a result.

1. **45 of 74 control rows rendered an empty SHIPPED section.** An author drawn from
   the full population may have nothing posted after their own need, and such a row
   can only be labelled `unrelated`, so the control was depressed by construction and
   would have handed C1 an artifact. Caught by a test whose *population* was the
   thing hiding it: the first version iterated only the treatment arm and passed.
   Repaired by restricting the partner pool to the 74. (`AMENDMENT-2`.)
2. **The mismatched arm was the treatment arm, renamed.** It paired each partner's
   *own* need with that partner's *own* builds: 74 self-pairs, 0 cross-pairs. The
   alarm was the lexical arm printing **byte-identical means** for both arms — two
   different pairings cannot produce identical word-overlap across 74 rows. Repaired,
   the arms read 0.044952 against 0.023632. (`AMENDMENT-3`.)
3. **A label file with 222 correct row ids and a wrong row-to-pair mapping.** Reader
   r1 detected the view being regenerated under it, discarded its own pass, and
   re-labelled — then emitted rows in the *previous* view's order. Every id present,
   none repeated, id set matching the key. Asserting the id **set** is what let it
   through; the test now asserts the **order**. My own repair script made it worse,
   re-keying the file against the wrong reference at a reassuring 221/222, and was
   deleted. Separately, reader r2's first pass returned 4 duplicated and 4 missing
   ids, caught by the pre-declared integrity test and re-run with a *mechanical*
   verification command rather than a self-check.

## What this does and does not change

- **It does not reopen item 0d.** F042's `0 of 24 built the thing themselves` is not
  refuted. The effect here is bounded above by about **+0.11** and is consistent with
  zero, so the corpus still cannot supply a candidate.
- **It does confirm the closure on an instrument 10× larger than E022's**, and it
  changes what the closure *is*: the demand corpus is a population of people who had
  already built something, not a queue of unmet need.
- **The 74 is the ceiling, and it is not this reader's to raise.** Two independent
  readers agreed on 3 rows; at n = 74 per arm a 4% rate against a 0% rate is not
  resolvable, and the reader scheme's own agreement is below its declared floor. A
  larger n is the only thing that would change the verdict, and it is the same
  instrument asked to do more.
- **It says nothing about whether the shipped things are good or used**, and nothing
  about how many unmet needs exist. `addresses` is one model's judgement of a title.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/029-need-build-match/build_population.py
tools/x -- python3 EXPERIMENTS/029-need-build-match/fetch_builds.py
tools/x -- python3 EXPERIMENTS/029-need-build-match/verify_chronology.py
tools/x -- python3 EXPERIMENTS/029-need-build-match/make_reader_views.py
#   two readers label raw/view_r1.txt and raw/view_r2.txt to raw/labels_r1.tsv, labels_r2.tsv
tools/x -- python3 EXPERIMENTS/029-need-build-match/stats.py
python3 -m unittest discover -s EXPERIMENTS/029-need-build-match -p 'test_*.py' \
  -t EXPERIMENTS/029-need-build-match
```

37 tests. Each is asserted against the committed capture rather than a fixture built
from the same object as the assertion: the Wilson interval for 0/24 must equal the
`[0.0, 0.138]` the record quotes for F042, the mismatched arm must contain zero
self-pairs and the treatment arm 74, the two arms' lexical statistics must differ,
the chronology capture must sample both directions and record zero disagreements,
reader label order must equal the frozen view's order, and no superseded label bytes
may sit in `raw/`.
