# E029 — do the people who stated a need build that need?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Declared 2026-10-05, before the first fetch and before any reader saw a pair.**
Task T-0073. What follows is fixed in advance; a threshold that moves after seeing
which side of it the data fell on is a rationalisation, and
[`DECISIONS-SCREENING-4.md`](../../DECISIONS-SCREENING-4.md) D058 forbids it.

## The question, and why this corpus and not another

This mission's one demand-side population is 1250 people who each publicly wrote
down what was missing from their work (`EXPERIMENTS/019`, F039). Two measurements
have been taken against it and neither reached the thing that matters:

- **F042 / E022** followed the *needs* forward: 58.0% drew a reply, and **0 of 24**
  unserved requesters built the thing. That 0-of-24 arm could only see a builder
  announce themselves, so the record labels it a **floor on disclosure**.
- **F045 / E025** followed the *people* forward and found the disclosure channel
  E022's arm lacked: **278 of the 1250 need-staters have a `Show HN` item**, 22.2%
  against 27.8% for ordinary commenters in the same stories.

E025 then closed with the sentence *"a population that builds something else is not
a population of standing unmet need"* — and **left the join unmeasured.** 278 people
in this corpus have both a demonstrated need and a demonstrated build. Nobody has
asked what the 278 shipped. That is the whole experiment.

**H1.** Among the 278 need-staters who publicly shipped something, the rate at
which the shipped item **addresses the need they stated** is materially higher
than the rate for those same shipped items paired with **a different author's**
need statement.

## The two competing explanations, and the baseline that can kill

H1 has exactly one serious rival, and it is not "no effect":

> **W-A (topic clustering).** Hacker News is topic-clustered. A person who complains
> in a database thread builds database-adjacent software because that is their
> community, not because the need caused the build.

Naming the strongest baseline specifically, as required by
[`docs/process/experiment-protocol.md`](../../docs/process/experiment-protocol.md):
the strongest available baseline is **not** another author's need — it is **the
title of the story the need statement was made in.** W-A predicts that a builder's
shipped item is as related to their thread as to their need. A mismatched-author
pairing is a *weaker* baseline, because it also removes the author's own topical
neighbourhood and so can call a real positive a null.

**Both arms run. The story-title arm is the one that can kill H1.**

## Population, and what is excluded before any result is seen

1. Every distinct author in `EXPERIMENTS/025-.../raw/need_arm.jsonl` with
   `nb_show_hn >= 1`. **278 rows**, declared here so the denominator is fixed.
2. Each such author's need statements, joined via `author` to
   `EXPERIMENTS/022-need-outcomes/raw/outcomes.jsonl` and then via `comment_id` to
   `EXPERIMENTS/026-unserved-need-structure/raw/texts.jsonl` (1401/1401 readable).
3. **Exclusions, all applied blind to any outcome:**
   - an author with **more than one** need statement is excluded, because choosing
     which need the build answers would be a labelling act made after the fact;
   - a need statement with **fewer than 15 stripped words** is excluded, because a
     reader cannot judge relatedness against it and its exclusion rate is reported.
4. For each surviving builder: their `Show HN` item titles and URLs (one request,
   comma-AND `tags=author_X,show_hn`), and the title of the story their need
   statement was made in (one `items/<story_id>` request).

Sampling for the reader arm, seeded and therefore reproducible: `random.Random(2901)`,
shuffle the eligible builders, take the first 40 matched pairs; the mismatched arm
reuses those 40 builders and takes each one's need from a seeded derangement of the
eligible pool, so no pair is self-paired.

## Instrument, and the reader's blindness

Two readers, **the same rubric**, neither told which arm a pair is in, neither shown
the author's name, the story title, or the need's thread. A reader sees exactly two
things: the need statement verbatim, and the shipped item's title and URL. Both arms
are interleaved and shuffled into one file per reader, so the arm label is not even
present in the input.

Labels: `addresses` — the shipped item plausibly does the thing the need says is
missing; `unrelated` — the shipped item's subject is not the need's subject;
`unclear` — the need is too thin or too ambiguous to call. Full wording in
[`RUBRIC.md`](RUBRIC.md), written before either reader ran.

**A lexical arm is reported and feeds no gate.** Content-word overlap between a need
and a shipped title is computed for matched and mismatched pairs and printed with its
control beside it, because E028 measured lexical coverage as `informative: false`
and F043's lesson is that a bare rate without its base rate is not a finding.

## Gates, all declared now

| gate | declared rule |
|---|---|
| **A1**, fetch validity | ≥ 95% of the 278 builders return a title list; ≥ 95% of need statements join |
| **A2**, controls | 6 of 6 verified-positive accounts return ≥ 1 item; the nonsense account returns **0**. These six are E025's corrected set, sampled *from the `show_hn` tag itself*, so each is verified positive by the evidence the gate tests (F036's lesson) |
| **A3**, reader agreement | Cohen's **κ ≥ 0.6** on the three-label scheme, over all 80 rows |
| **C1**, the negative control that can refuse the experiment | the matched and mismatched arms must differ by **≥ 0.20** in reader `addresses` rate, else the instrument is blind and the verdict is **`not_evaluated`** |
| **B1**, kill | matched CI95 upper ≤ story-title CI95 upper, **or** matched CI95 upper ≤ mismatched CI95 upper → **H1 dies** |
| **B2**, survive | matched CI95 lower > **both** control uppers → H1 survives |
| **A4** | if A2, A3 or C1 fails, the verdict is `not_evaluated` and neither B1 nor B2 is read as an answer |

C1 and A4 are declared **before** the run because adding a refusal afterwards is
indistinguishable from adding it to make a result look better
([`STATE-constraints.md`](../../STATE-constraints.md)).

## What each outcome changes

- **B2 (survives).** F042's third cell is **refuted as an estimate**: a 278-row
  instrument finds a non-zero need→ship rate where a 24-row disclosure-limited arm
  found zero. Item 0d's closure rationale — *a population that builds something else
  is not a population of standing unmet need* — is falsified for a measured
  sub-population, and the generator seat stops being empty. This would be the first
  live lead in twenty-eight experiments.
- **B1 (dies).** F042's third cell is **confirmed on an instrument 11× larger** than
  the one that produced it, the demand corpus is closed at a resolution that stops
  further re-reading, and "what do need-staters build" becomes
  measured-negative rather than `inconclusive`.
- **A4 (`not_evaluated`).** The instrument is named as blind and the corpus stays
  closed — E028's outcome, and a real result.

## What this cannot decide

- **It is not a measurement of need.** It says nothing about how many unmet needs
  exist, and nothing about F029's 0-of-50.
- **It is not a usefulness or adoption claim.** No person is contacted, no artifact
  is used, and `addresses` is one model's judgement, not a person's.
- **A surviving H1 is a lead, not a candidate.** It would name a population whose
  stated needs and shipped artifacts coincide. Turning that into something requires
  reading the pairs, which is where F029's 0-of-50 will have to be answered again.
- **It inherits E025's disclosure floor**: a build never announced as `Show HN` is
  invisible here, and E025 measured `show_hn` as confounded with overall HN
  activity (median 2416 items for builders against 467). Both arms of this
  experiment carry that, and it is reported rather than corrected.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/029-need-build-match/build_population.py
tools/x -- python3 EXPERIMENTS/029-need-build-match/fetch_builds.py
tools/x -- python3 EXPERIMENTS/029-need-build-match/make_reader_views.py --reader r1
tools/x -- python3 EXPERIMENTS/029-need-build-match/make_reader_views.py --reader r2
tools/x -- python3 EXPERIMENTS/029-need-build-match/stats.py
python3 -m unittest discover -s EXPERIMENTS/029-need-build-match -p 'test_*.py' \
  -t EXPERIMENTS/029-need-build-match
```
