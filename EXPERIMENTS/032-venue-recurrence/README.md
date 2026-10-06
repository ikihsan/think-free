# E032 — does the recurrence zero survive a change of venue?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

**Date:** declared and run 2026-10-06. Task T-0076. Protocol declared in
[`PROTOCOL.md`](PROTOCOL.md) before any fetch, amended once
([`AMENDMENT-1`](PROTOCOL.md)) before any pair existed. Fetches captured in
[`raw/fetch_log.jsonl`](raw/fetch_log.jsonl); every reader was handed the sha256
of the sheet it read and every sheet digest is recorded in
[`sheets/MANIFEST.json`](sheets/MANIFEST.json).

## Verdict: B2 fires. The zero is **not** venue-specific.

| gate | rule | result |
|---|---|---|
| **A1** | ≥ 95% of attempted rows answer; 60 rows re-readable from disk | **passes** — 6/6 fetches 200, 60 rows on disk |
| **A2** | candidate pairs > the count chance alone produces | **passes** — **32** candidates against a chance expectation of **1.19** (span 0–6), reachable by 27× |
| **A3** | reader κ ≥ 0.6 | **passes** — **κ = 0.8344**, raw agreement 0.9167 on 60 double-read rows |
| **A4** | nonsense ≤ 0.25 clauses; negatives ≤ 0.20 `same` | **passes** — **0/24** shuffled bodies yielded a clause; **0/10** negatives `same` |
| **A5** | ≥ 16/20 positive pairs `same` | **passes** — **20/20** |
| **B1 survive** | diff ≥ 0.20, CI95 excl 0, ≥ 2 `same` | does not fire |
| **B2 kill** | 0 `same` candidates with every A-gate passing | **fires** |

| arm | n | `same` | rate | CI95 |
|---|---|---|---|---|
| candidates (shared rare token, different authors) | 32 | **0** | 0.0000 | [0.0000, 0.0894] |
| control (length-matched, reader-adjudicated) | 60 | **0** | 0.0000 | [0.0000, 0.0488] |
| difference | | | **0.0000** | **[−0.0602, +0.1072]** |
| positives | 20 | **20** | 1.0000 | A5 |
| negatives | 10 | 0 | 0.0000 | A4 |

**Nothing recurs on a structurally different venue either** — 60 long-form
questions from three non-programming Stack Exchange sites, 53 authors, 28
requirement clauses both readers agreed on, and 0 of 32 candidate pairs stating
the same requirement. The instrument returned a positive on 20 of 20 synthetic
positives and none on 10 length-matched unrelated pairs, so the zero is the
instrument talking.

## What this changes, and what it does not

**The belief survives, and it is now a better-supported belief than it was this
morning.** What was a claim about Hacker News comments is now a claim about
**two venue classes that differ on nearly every axis that could matter** —
length, self-containedness, population, subject matter, and the selection rule
itself. F051's venue ceiling ("One corpus and one channel set") is discharged on
one axis and the generator closes on evidence rather than on one platform.

**It is a bound, not a zero, and the bound is the honest product of this run.**

| | |
|---|---|
| 0 of 32 → one-sided 95% upper bound | **0.0894** |
| if the true rate were 0.05, P(0 observed) | 0.194 |
| if the true rate were 0.10, P(0 observed) | 0.034 |
| if the true rate were 0.20, P(0 observed) | 0.0008 |

So a recurring-requirement rate of about **1 in 11** is not excluded by E032
alone. Pooling E032's 32 with E031's 100 adjudicated candidate pairs gives
0 of 132 and an upper bound of **0.0223** across two venue classes. E032 on its
own is the weaker of the two; it is the run that makes the pooled number mean
something.

**Nothing here revives a candidate.** A recurring requirement would still be a
clause, not a product, and the standing reading of this mission's demand side is
unchanged by a second zero: *a need stated in public is absorbed in conversation,
and the requesters are largely people who had already built something.* F049 put
that number at 167 of 241 shipping **before** they complained, and F043's control
showed the served figure was the base rate of a Hacker News conversation.

## The two defects this run found in its own instrument, and what caught them

Both were found by **running the step and reading its output** rather than by
trusting a report — the practice F052 identifies as the one this repository has
now had to learn four times, and the reason it is written into
[`PROTOCOL.md`](PROTOCOL.md) as a gate.

1. **`link.py` read the sheets instead of the labels.** Every question body is
   non-`none`, so all 60 rows looked like clauses, both readers looked identical,
   agreement was 1.0, **κ was undefined**, and 28 clauses appeared as 60. It was
   caught because κ came out `null` against readers who independently reported 32
   and 27 `none`. A gate that cannot be computed is a gate reporting nothing; had
   κ been declared as raw agreement this would have passed as a perfect result.
2. **The pair key file was written in build order while the sheet was shuffled.**
   `tally.py`'s row-identity check **by order** (D061, from F049) caught it on the
   first run. The fix writes the key file in the sheet's order, and the sheet's
   bytes are unchanged by the fix — verified by digest — so the adjudicator's
   labels remain valid.

**A third near-miss worth recording:** the linkage rule in the original protocol
was a rank-based rare-token cutoff that is **not** E031's rule and, with fewer
than 60 clauses, has no token at rank 200 to cut at. AMENDMENT-1 replaced it with
E031's actual rule, imported from E031's own module, before any pair existed.
Had it not been caught, the run would have changed two variables at once and the
comparison it exists to make would have been void.

## Honest limitations

- **28 clauses.** Two people needing the same capability twice must both land in
  the sample. This is the same scale as E031's 63 and it is the binding
  constraint on the bound above.
- **Readers are sub-agent contexts of one model family.** κ = 0.8344 is evidence
  the question is answerable from the text, not evidence two people would agree.
  The two readers disagreed on 5 of 60 rows about whether a want is stated at all
  (reader 1 said yes on 28, reader 2 on 33, both on 28).
- **One platform, one language, one era, 2025–2026, three sites.** A positive
  would have been a requirement recurring in one venue class, not a market; a
  negative is bounded the same way.
- **`sort=votes` prefers questions that were answered.** The protocol selected
  this deliberately — popular questions are where people state needs in the most
  elaborated form — and it is a bias: it over-samples engaged users. It is the
  opposite of a popularity filter on *tools*, which is the filter F037 and F048
  showed cannot carry a claim.
- The site set is woodworking/outdoors/cooking. Nothing licenses a claim about
  any other non-programming community.

## Reproduction

    python3 harvest.py       # 6 fetches; writes raw/harvest.jsonl + raw/fetch_log.jsonl
    python3 extract.py       # blinded sheets + keymap, with digests
    python3 link.py          # linkage, chance expectation, q2 sheet + key file
    python3 tally.py --check # re-derives the gate table above from raw/ and labels/

`tally.py` reads only committed bytes and asserts row identity by order before it
computes anything, so the verdict does not depend on this session's account of
it.