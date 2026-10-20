<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E181 AMENDMENT 2 — K1 fired; what still runs, and on what power

**Written:** 2026-10-18, after `facts.jsonl` was written and committed for the
twenty declared rows, and **before `answers.jsonl` exists**. No arm has been
answered and no verdict exists. No gate threshold is changed here.

## What happened

`EXT` read the twenty declared rows against `READER-INSTRUCTION.md` and named a
missing fact on **10 of them, 0.5000**, Wilson 95% [0.2941, 0.7059]. Ten were
written `null`, each with a stated reason in `facts.jsonl`, and every quote was
proved verbatim and proved to sit in a comment section rather than in the
question before the file was written.

The ten nulls are not shirked reading. They split into two kinds, both
recorded per row: comments that carry **the remedy itself** (row 3's `:host`
styling recipe, row 17's "run as administrator", row 19's `langchain_classic`)
and rows where the comments only carry **other reporters'** observations (row
4's .NET SDK 8, row 12's fork, row 18-adjacent self-reports). Neither is a fact
about the reporter that the reporter is missing, which is what the instruction
asked for, and inventing one would have been the worse error.

**K1 fires as declared.** Fewer than 16 rows carry both an A1 fact and an A0
answer. The protocol's ending for K1 is that the comparison does not run.

## Why a comparison still runs, and what it is worth

Because a declared stop with nothing measured is the wrong trade when the
measurement is cheap and the reading is unambiguous, the arms run anyway and are
labelled **`exploratory`** wherever they appear. **No gate is reported as passed
or failed, G1 through G5 are reported as `not evaluable`, and the arms cannot be
cited later as evidence for or against the mechanism.**

**The power this design actually has, declared so it cannot be misread.** On ten
paired rows, an exact McNemar test reaches `p < 0.05` only if the treatment
wins essentially every discordant pair — at five one-directional discordant
pairs the exact two-sided p is 0.0625. **A null result at n = 10 means nothing;
a positive result at n = 10 means a very large effect.** Stating it here means a
marginal p-value cannot later be read as evidence of no effect, or of an effect.

## The one change to the population, and its reason

**`EXT` reads the remaining ten of E177's 30 scored EVID rows — no answers, no
verdicts, no comparison — and the fact-yield rate is reported on all thirty.**

The reason is the yield, not the mechanism. The fact-supply rate is the only
quantity in this experiment that survives K1, and at n = 20 it carries a ±0.21
interval, which cannot separate "the round trip names the fact about half the
time" from anything else. Thirty rows roughly halves that interval. No threshold
depends on the number, no arm changes, and no answer or verdict exists to be
fitted to.

**The selection bias this introduces, declared:** the thirty are E177's thirty,
so this stays a conditional statement about one reused draw, exactly as the
protocol already said. Extending from 20 to 30 adds the ten rows E177's seeded
shuffle places next, not a fresh draw.

## Arm sizes actually run

Fixed by what exists at the time of writing this, with the rule given so a
reader can reproduce it:

- **A0, A1, B1** on the first **20 fact-bearing rows** of the thirty in index
  order (at the realised yield of roughly one half this is about 15 rows; the
  realised number is reported, not chosen).
- **C1** on the **first 10 fact-bearing rows**, one placebo fact each, taken by
  the protocol's fixed rule — the A1 fact of the next fact-bearing row in index
  order, wrapping — since with only ~15 fact-bearing rows a 10-row placebo can
  be drawn inside the same set rather than across it.
- **P** — E177's committed A0 answer for the first 10 fact-bearing rows,
  re-scored inside this experiment's blinded set. This is G4's drift check and
  it is the one check that does not depend on the arms.

**Cost check, declared:** 30-row ceiling × 3 arms + 10 + 10 = up to 80 graded
pairs. The declared scoring order (A1 → A0 → B1 → C1 → P) is unchanged and a
session that runs out of budget reports what it has.

## What is unchanged

Every gate as written, every arm's input format, the reader roles, the
commit-before ordering, the scoring order, the fact wording that `EXT` used, and
the rule that `G5`'s blind re-read happens after `answers.jsonl` is committed.
This amendment adds no label, moves no threshold, and changes nothing a later
reader would have to take on trust.