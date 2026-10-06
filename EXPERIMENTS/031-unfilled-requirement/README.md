# E031 — do unfilled departure requirements recur?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Date:** 2026-10-05. Task T-0075. Protocol declared in
[`PROTOCOL.md`](PROTOCOL.md) before any account was read, amended four times
([`1`](PROTOCOL-AMENDMENT-1.md), [`2`](PROTOCOL-AMENDMENT-2.md),
[`3`](PROTOCOL-AMENDMENT-3.md), [`4`](PROTOCOL-AMENDMENT-4.md)). No network
fetch: the corpus is E030's captures, already on disk.

## Verdict: H1 does not survive, H2 does not survive — and the instruments passed

| gate | rule | result |
|---|---|---|
| A1 capture integrity | view digests re-read from disk | **passes** (0 mismatches; strata 326 / 593 / 2687 as declared) |
| A3 reader agreement | κ ≥ 0.6 on q1 over 96 double-read rows | **passes** — **κ = 0.7189**, raw agreement 0.875 |
| A4 nonsense control | q1 `yes` ≤ 0.25 on 24 token-shuffled rows | **passes** — 0/24 both readers |
| A5 planted separation | q3 (names the successor) separates move from seek by ≥ 0.20 | **passes** — 0.583 vs 0.097, **separation 0.486** |
| A6 pair positive control | ≥ 16/20 positives `same`, ≤ 0.20 negatives `same` | **passes** — **20/20** and **0/10** |
| **B1** H1 | seek − ordinary ≥ 0.20 with CI95 excluding 0 | **fails** — 0.347 vs 0.181, diff **0.1667** CI95 [0.0224, 0.3024] |
| **C1** H2 | P_same(candidates) − P_same(control) ≥ 0.20, and ≥ 2 same pairs | **fails** — **0 of 100** candidates and **0 of 100** controls `same`, diff 0.0000 CI95 [−0.0370, 0.0370] |

**H1 `does_not_survive`; H2 `does_not_survive`.** This is a negative result from
an instrument that passed every check available to it, which is the distinction
E028's outcome lacked and F043 insisted on.

## The two numbers that decide it

**One reader, one wording, three arms, 216 comments.** The rate at which an
account states a capability something the author relies on cannot do:

| arm | n | yes | rate | CI95 |
|---|---|---|---|---|
| seek (names no successor) | 72 | 25 | **0.347** | [0.248, 0.462] |
| move (names a successor) | 72 | 25 | **0.347** | [0.248, 0.462] |
| ordinary (no framing) | 72 | 13 | **0.181** | [0.109, 0.285] |

Departure accounts state a missing capability at nearly **twice** the rate of
ordinary comments in the same stories (0.347 vs 0.181), and the interval
excludes zero. **But the declared margin was 0.20 and the observed difference is
0.1667, so B1 fails.** The gap is real and smaller than the protocol asked for.

**The seek stratum is not distinguished from the move stratum at all**: 0.347
against 0.347, difference exactly 0.0000 CI95 [−0.1523, 0.1523]. This is the most
informative single reading in the run, and it is **negative about the
population's premise**. Accounts that named a successor state a missing capability
exactly as often as accounts that did not. **"Unfilled" is not a property this
population has** — the seek/move split is a difference in framing phrase, not in
whether anything was left unfilled. That retires the hypothesis the experiment
was built on.

**And no requirement recurs.** 100 candidate clause pairs (sharing ≥ 1 rare
content token, different authors, different departing artifacts, different
stories) produced **0 `same`** and 5 `unclear`. 100 matched random pairs produced
**0 `same`** and 0 `unclear`. The difference is 0.0000 CI95 [−0.0370, 0.0370].

## Why the zeroes are evidence rather than a broken instrument

This is the part E030 could not establish, and it is the reason A4, A5 and A6
were declared and run:

- **A6**: the same adjudicator, same wording, marked **20 of 20** synthetic
  positive pairs `same` and **0 of 10** length-matched negatives. The instrument
  returns a positive when one is there and rejects matched pairs.
- **A5**: the successor question separates the strata by **0.486** (move 0.583,
  seek 0.097), so the reader can read the distinction the arms are built on.
- **A4**: 0 of 24 token-shuffled rows drew a `yes`.
- **A3**: κ = 0.7189 over 96 double-read rows, above the 0.6 floor and well above
  the 0.5004 that closed E029's reader arm.

**A6's ceiling is declared and stands**: its positive pairs are a transform of
the source clause that shares nearly all of its content words
(AMENDMENT-4 §2), so A6 shows the instrument can return a positive and rejects
matched negatives — it does **not** validate semantic paraphrase discrimination.
The instrument's ability to separate a genuine recurrence from lexical
resemblance is not established by these gates; it is the very thing the zeroes
put in question, and a passing A6 does not settle it.

## Length, checked because E030's failure was length

E030's arm difference **was** comment length (sign flip under matching, F050).
Here the length-matched recomputation, ordinary rates reweighted to seek's
length distribution, moves the difference from **0.1667 to 0.1698** — it grows by
0.003. **The seek-minus-ordinary difference is not a length artifact**, which is
the opposite of E030's account of its own statistic. Per-band rates are in
[`raw/results.json`](raw/results.json).

## What this rules out, and what it does not

**Rules out.** The hypothesis E031 was built on: that accounts seeking an
alternative state a requirement the departed artifact failed, in a form that
**recurs across independent authors and independent artifacts**. A fourth
demand-side generator closes, and this one closes on a **measured failure of its
own premise** — not on prior art, not on a screen, and not on the trigger
vocabulary that F043 showed is blind to outcomes. The population is real (E030's
A8 separation 0.64 vs 0.036, and A5 here at 0.486), it does state missing
capabilities at double the base rate, and **two independent authors in 63 clauses
asked for the same thing zero times**.

**Does not rule out.**

- **Small genuine recurrence.** 63 clauses across three arms. Two people needing
  the same capability twice would both have to land in a 25-clause arm sample.
  AMENDMENT-4 §"ceiling" states this before the adjudication, and nothing in the
  run removes it.
- **Reader independence in the strong sense.** Both readers were sub-agent
  contexts of one model family (AMENDMENT-1 §1). κ = 0.7189 is evidence the
  question is answerable from the text, not evidence two people would agree.
- **Any other channel.** Departure accounts in GitHub issues, Reddit, support
  forums and the open web were never read, exactly as E030 declared them unread.
- **Whether the 0.347 figure is useful.** It is a rate about what people say,
  from a self-selected population of public technical argument, at 216 rows.

## Four instrument defects found by printing, all recorded

1. **A declared linkage rule that could not fire** (AMENDMENT-3). Requiring two
   independent clauses to share ≥ 2 rare content tokens yields **4 candidate
   pairs against a chance expectation of 4.9**. C1 as declared was unreachable
   whatever the world contained — the mirror image of F010's gate that could not
   fail. Replaced with reader adjudication of ≥ 1-token candidates against a
   reader-adjudicated random-pair control, the control F043 showed this record
   had been missing.
2. **The same unit change that fixed F050 broke C1.** Reader clauses are short —
   median 11 words — so a rule tuned for 90-word comments does not transfer.
3. **My own amendment carried a wrong number.** AMENDMENT-3's first table counted
   pairs *within* arms (53 at ≥ 1, 2 at ≥ 2) while `build_pairs.py` pools them
   (100 at ≥ 1, 4 at ≥ 2). Corrected in place, before any pair was adjudicated,
   with the correction visible in the file.
4. **Two checker defects on their first run**: the byte-identity gate included the
   per-row `ID:` line, which differs by arm by construction (AMENDMENT-1 §3), and
   the verbatim check rejected two correctly-copied clauses for a curly
   apostrophe and a double space (AMENDMENT-2, which declares the fold and counts
   the **2 rows in 456** it rescued).

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/recount.py
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/select_doubleread.py
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py <arm> r1|r2
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/agreement.py
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/build_pairs.py
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/build_poscontrol.py
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/stats.py
```

The four reader passes are sub-agent labelling sessions and are not re-runnable
as commands; their outputs are the `raw/e031_labels_*.tsv`,
`raw/e031_q3_*.tsv` and `raw/e031_pairlabels_*.tsv` files, each accepted by
`verify_labels.py` against the frozen view digest. Raw numbers:
[`raw/results.json`](raw/results.json), [`raw/agreement.json`](raw/agreement.json),
[`raw/pair_build.json`](raw/pair_build.json),
[`raw/poscontrol_build.json`](raw/poscontrol_build.json),
[`raw/strata.json`](raw/strata.json).