<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E196 AMENDMENT 3 — the tail walk is censored at the decisive end, so G4 is restated on exact order statistics

Declared 2026-10-19, **after panel 2 fetched all 100 codes and before it wrote
a single gate**. Panel 2's fetch is preserved: every response body is already in
`raw/`, and `client.call` reuses a capture whose stored request key matches, so
re-running costs nothing for what exists.

## What panel 2's fetch showed

All 100 codes answered. **58 of 100 hit the 6-page tail cap** (AMENDMENT-2 §1),
including every one of the ten largest cells in the head — `R499`, `6505`,
`R706`, `7A21`, `S206`, `C219`, `D304`, `1560`, `9130`, `6640` — and for those
the walk returned **600 awards of which every one was $0 or negative**.

AMENDMENT-2's rule already said what happens: a censored code cannot satisfy G4,
and the count is printed. **The rule was correct and the result is unusable.**
Censoring did not remove noise; it removed the decisive end of the distribution.

## The instrument defect, named

**The walk's cost is paid in awards, and the awards it spends are the ones that
carry no money.** A cell with a large population of zero-dollar and deobligated
records puts hundreds of pages of nothing in front of the first real purchase.
The cap is therefore not a random sample loss — it is **anti-correlated with
the thing G4 asks about**, in the direction that hides the finding.

## What had been seen before this amendment, stated plainly

A throwaway probe on **three** codes, run between panel 2's crash and this
amendment, to find out *where* the zero block ends rather than what it contains.
`7A21`: rank 1,000 ≈ $119–157, rank 10,000 ≈ $14,208–14,313, rank 30,000 ≈
$71,667–72,457. `S206`: rank 5,000 ≈ $1,472–1,577, rank 10,000 ≈ $11,075–11,445.
`R499`: rank 100,000 = **$10**, rank 200,000 = **$20**, rank 300,000 = **$30**,
rank 500,000 = **$52**. Three of one hundred codes, chosen because they were
the censored ones, with no gating statistic computed from them.

That probe is why the amendment's design is a **rank profile at declared
checkpoints** rather than a longer walk. Every number below was chosen from
that three-code shape and the amendment is declared before any *systematic*
measurement exists, which is the only thing that can be done at this point; the
checkpoint ranks are round powers of ten and the median, and none of them was
tuned to a result.

## The repair

**I3 is replaced by an exact rank profile.** For each code, fetch the ascending
page containing each declared rank and record that block's minimum and maximum:

| declared rank | 100 | 1,000 | 10,000 | 100,000 | 1,000,000 | ⌈N/2⌉ (median) |
|---|---|---|---|---|---|---|

Each checkpoint yields a **one-sided exact statement**: *at least* `k` awards of
this code are at or below the block's maximum. No interpolation, no estimate,
no claim about the rows between checkpoints.

The previous tail sum is **kept, not discarded** — it is exact for the 42
uncensored codes and is reported as a supporting statistic beside the profile.

## G4 restated, same bar

> At least one code has a checkpoint at rank **≥ 10,000** whose block maximum is
> **≤ $100,000**, and whose total obligation is **≥ $1,000,000,000**.

Two exact facts and no arithmetic. The declared bar is unchanged in substance:
≥ 10,000 purchases of ≤ $100,000 inside a cell carrying ≥ $1B is a cell bought
in small repeated units, and a program capturing 0.1% of it is $1M/yr.

**What it gives up, stated:** the exact dollar sum of sub-$100,000 purchases,
which AMENDMENT-1 promised, is **not** recovered — obtaining it needs every such
award and some cells hold tens of thousands. The replacement answers "how many
units, and is the cell big" rather than "how many dollars", and the RESULT must
say so wherever it uses G4.

## Two defects of my own code, found in the same run

1. **`fetch_code` never copied `total_awards_level` onto the record.** Every
   family money total, every family label (chosen as the highest-spend code's
   name) and the printed `$0` column were computed from a field that was absent.
   Fixed by carrying it through, and caught because the run's own progress line
   printed `$0` for `M159`, a code the endpoint reports at $16.2B.
2. **`analysis.py` used `median` without importing it**, so the run finished its
   1,300 captures and then raised. The captures were not lost.

Neither changes a declared threshold. Neither is a data defect.

## Unchanged

Population, window, `spending_level`, the $100,000 cutoff, the $1B bar, α =
0.01, the 2× base rate, G1, G2, G3, G5's design, and the six declared limits.