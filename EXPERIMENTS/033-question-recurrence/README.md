# E033 — public questions do recur across authors, at 5.4%, and the record's zeros sat in the wrong stratum

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

**Date:** declared and run 2026-10-06. Task T-0077. Protocol declared in
[`PROTOCOL.md`](PROTOCOL.md) before any fetch of the declared population, amended twice
([`AMENDMENT-1`](PROTOCOL.md) — the declared site rule was unreachable; `AMENDMENT-2` — the
declared canonical cross-check cannot be run on this API), and once more for the labelled
post-hoc addition **D9**. Fetches in [`raw/fetch_log.jsonl`](raw/fetch_log.jsonl) and
[`raw/resolve_log.jsonl`](raw/resolve_log.jsonl); every reader was handed the sha256 of
the sheet it read, and `tally.py` recomputes that digest from committed bytes before it
reads a single label.

## Verdict: B1 fires. The record's pooled 0.0223 bound is refuted.

| gate | rule | result |
|---|---|---|
| **A1** | ≥ 95% of fetches 200; every row carries a closure reason or its documented absence | **passes** — 24/25 harvest fetches 200, 1000 rows, 5 distinct reasons |
| **A2** | the visibility calculation's inputs are measured, not assumed | **fails** — see A3; `q` depends on the canonicals A3 rejected, so the product is not printed |
| **A3** | ≥ 30 of 40 edges read `same`, and canonical author differs on ≥ 30 | **fails** — **6 of 24** sheet rows `same` by both readers; author differs on 38/40 |
| **A4** | reader κ ≥ 0.6, undefined κ ⇒ `not_evaluated` | **passes** — **κ = 0.8327** on 47 double-read rows |
| **A5** | the unrelated arm reads `same` for ≤ 0.20 | **passes** — **0 of 24** |
| **B1 survive** | the duplicate rate's CI95 **lower** bound > 0.0223 | **fires** — 0.0416 > 0.0223 |
| **B2 kill** | the duplicate rate's CI95 upper bound ≤ 0.0223 | does not fire |

### The headline number

**54 of 1000 questions = 0.0540, CI95 [0.0416, 0.0698]**, against a record bound of
**0.0223**. `travel` 33/500 = 0.0660, `math` 21/500 = 0.0420. The bound this refuted is
`EXPERIMENTS/032-venue-recurrence/README.md`'s pooled figure: 0 of 132 adjudicated
candidate pairs across two venue classes.

The label is not this repository's. It is Stack Exchange's own `closed_reason ==
"Duplicate"` — a judgement made by other people, on the platform, about the platform's own
archive. Every one of the record's five zeros was produced by a linkage rule this mission
invented and a reader adjudicating pairs it chose.

## What this says about the five zeros

The zeros were **not wrong, and not about the world**. They were about a stratum.

**The counterfactual draw (D7) is the finding that lands hardest.** Sort this population by
score and take the top 60 — which is what E032's `sort=votes` selection drew:

| draw | duplicate closures |
|---|---|
| top 60 by score | **0** |
| mean over all 941 sliding 60-question windows | 3.37 |
| max window | 12 |

**D6 shows the stratum effect directly.** Duplicate closures are **4.5× rarer in the
top score tertile** than the bottom one:

| tertile | n | duplicate | rate | CI95 |
|---|---|---|---|---|
| high | 333 | 6 | 0.0180 | [0.0083, 0.0387] |
| middle | 333 | 21 | 0.0631 | [0.0416, 0.0945] |
| low | 334 | 27 | **0.0808** | [0.0561, 0.1151] |

That is E032's declared bias ("`sort=votes` prefers answered questions") turning out to be
load-bearing rather than merely noted. A population selected for being popular is a
population selected against being a repeat.

**So both readings were true at once**, and the record kept only one: recurrence is common
in public questions (0.054 against a 0.0223 bound), and the record's samples were drawn
from where it is rarest. Five experiments ran the right question on the wrong stratum.

## Why A3 failed, and why that is the honest result

`/questions/{id}/related` returns 6–10 rows per question with full metadata, so a canonical
is *guessable* — but nothing in the public API says which row is the closure's target. The
API does not expose `closed_details` (the field that names it) or `question_type` (which
marks a related row as the duplicate), and the **four vectorised `{ids}` routes tried all return `no_method`**, so one
canonical costs one request. Details and the four routes tried:
[`API.md`](API.md).

The reader arm was built to check the guess, and it returned 6 of 24. `tally.py` therefore
refuses to print the visibility product `n·p·q`, because `q` = 0.05 would have been computed
from canonicals this run has just shown to be wrong in most cases. A number that would have
looked like a decisive mechanism check is not reported.

**A3's failure is the transferable part**: on this platform a duplicate closure is a
reliable **label** and an unreachable **edge**. That is a property of the archive, and it
means any future recurrence work here must be built on rates over whole populations, with
no edge set available as a shortcut.

## D9: withdrawn as a finding — the gap is largely mechanical

**This section previously claimed that a repeat is 2.6× more likely to go unanswered, and
that the convergent and unanswered populations overlap. Both are withdrawn.** See
[`PROTOCOL.md`](PROTOCOL.md) AMENDMENT-3 §2.

The measurement stands as written:

| arm | `answer_count == 0` |
|---|---|
| closed as duplicate | **30 / 54 = 0.5556** |
| every other closure state | **200 / 946 = 0.2114** |
| difference | CI95 **[+0.2052, +0.4670]** against **open** questions only (194/900 = 0.2156); **+0.2096, +0.4710** against every non-duplicate row |

**Zero of the 54 duplicate closures has an accepted answer**, and closing a question as a
duplicate does not answer it. So the gap is substantially a property of what closure *does*,
not of what the askers needed, and it cannot be read as evidence that convergent questions
go unmet. Reporting it as the mission-facing half of the finding was wrong, and the wrong
part is the part that would have driven a next action.

What survives: duplicates were **older** than the rest — median 7.9 days old at the window
edge against 3.3 — and still carried no answer of their own. Closure mechanics explain that
too. **D9 decides nothing on its own** and is reported as a description.

So the run has one result, not two: recurrence is 4.5× more common than the stratum the
record sampled, and that is a statement about where this mission was looking.

## What this does not license

- **Nothing revives a candidate.** 54 duplicate closures over 1000 questions, and the
  canonicals are unreadable, so no clause and no cluster was recovered.
- **This is not Hacker News.** The zeros came from `hn.algolia.com`; these come from two
  Stack Exchange sites. What transfers is the **method defect**, not a rate.
- **The rate is a lower bound**, for a reason the protocol first got wrong (AMENDMENT-3 §1):
  the sample is the 500 **newest** questions in the window, not a spread across it — `math`
  is four days wide, `travel` ~90 — but closure lag is **median 0.3 days, max 64.3**, so
  every row had 26 months to be closed, and a repeat that was answered instead of closed is
  not labelled at all.
- **D7 is a within-population counterfactual**, not a re-run of E032. The populations differ
  in site, instrument and question volume. What transfers is the *direction and rough size* of
  the stratum effect, not a corrected 0.0223.
- **Two sites, 2024, English, one platform.** `math` and `travel` were chosen by volume, not
  by answer rate — and the time slice is narrow and uneven between them (four days for
  `math`, ~90 for `travel`), so this is not one population sampled twice.
- **D9 was withdrawn, not merely caveated** (AMENDMENT-3 §2). It had been the run's
  mission-facing half; the mechanical explanation arrived only after both readers had
  reported, which is the correct order and also why it was not caught sooner.

## Honest limitations

- **A3 failed, so D4 and D8 are `not_evaluated`.** The declared mechanism arm has no output.
  D7 answers the same question with a measurement that does not need a canonical, and D7 is
  the declared stand-in, not a substitute chosen after the fact.
- **AMENDMENT-1 widened the window** from one month to six and reordered the sites. The
  declared one-month rule yielded one qualifying site, so the declared population was
  unreachable; both amendments were made before any rate was computed, and the first
  attempt's bytes are committed as `raw/harvest-attempt1.jsonl`.
- **One 400 in 25 fetches** — `home-improvement`, which is not an API site identifier, kept
  from the declared order and recorded.
- **Readers are sub-agent contexts of one model family.** κ = 0.8327 says the question is
  answerable from the text, not that two people would agree. R1 and R2 differed on 3 rows
  (q2-012 `same`/`unclear`, q2-032 `same`/`not same`, q2-035 `same`/`not same`), all in the
  `edge` arm, all in the direction that lowers the edge count.
- **B1's CI does not exclude 0.0223 by a wide margin** — 0.0416 against 0.0223 — so the
  refutation is real but not enormous. It does exclude it, and the direction of the
  measurement bias (§10 of the protocol) makes the lower bound conservative.

## Reproduction

    python3 harvest.py       # 10 fetches; raw/harvest.jsonl + raw/fetch_log.jsonl
    python3 resolve.py       # 40 + 2 fetches; raw/edges.jsonl + raw/canonicals.jsonl
    python3 sheet.py         # blinded 48-row sheet + key file + MANIFEST.json
    python3 tally.py --check # re-derives every number above from committed bytes

`tally.py` recomputes the sheet's sha256 and refuses to proceed on a mismatch, checks label
rows against the key file **by order** on both readers (D061, from F049), and declines to
print the D4 product unless A3 passed. The verdict does not depend on this session's
account of it.