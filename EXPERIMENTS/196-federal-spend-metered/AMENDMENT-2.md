<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E196 AMENDMENT 2 — two gaps AMENDMENT-1 left open, declared before panel 2

Declared 2026-10-19, after panel 1 passed and **before panel 2 has issued a
single request**. AMENDMENT-1 changed instrument I3 and gate G4; it did not
answer two things panel 2 needs, and both are declared here rather than settled
in code and mentioned later.

## 1. The low-tail walk has a ceiling, and reaching it must be visible

`client.low_tail_awards` stops after **6 pages (600 awards)** per code. A cell
with more than 600 awards at or below $100,000 therefore yields a **partial**
tail. Three options were available — raise the ceiling, bound the head-100, or
label the censoring — and the rule this record keeps earning is that an
instrument must be able to say *"the population was not measured"* before the
measurement rather than after it (E017 `H2`, F061, E195 D7).

**Declared: the walk is capped at 6 pages, and any code that reaches the cap is
reported `censored: true` with its small-purchase sum labelled a lower bound.**
A censored code can never satisfy G4 on a sum the walk did not finish, and the
count of censored codes is printed with the verdict. The cap is not moved after
the run.

## 2. G5 needs a description source, and I3 no longer supplies one

AMENDMENT-1 kept G5's thresholds but its stated source was *"the I3
descriptions"* — and I3 is now the low tail, which on R425 is **100 rows of
zero-or-negative awards**, several of which carry no description at all. A
positive control run over empty strings would report a rate of 0 for both arms
and pass.

**Declared source, in order:**

1. descriptions on the **positive low-tail rows** (`0 < Award Amount ≤ $100,000`);
2. if a code has none, the descriptions on its **median stratum** (I4).

Each code's record states which source was used and how many rows carried a
usable description. **A code contributing fewer than 20 described rows is
excluded from G5 and counted**, because a rate over a handful of strings is not a
rate.

## 3. Family labelling is taken from the data, not from my memory

The toptier PSC labels (what `R` stands for, what `7` covers) are published
federal vocabulary, and I do not want a table of them typed from recollection
sitting underneath a gate.

**Declared: a family is the first character of the code, and its label is the
`name` of its highest-spend code as returned by the endpoint.** The label is
therefore source-supported and needs no external reference. The two **positive
control** families named in `PROTOCOL.md` are grouped by two-character prefix
(`Y1`, `3`, `S2`) and their identities were read from the API's own names in
reconnaissance — `Y1JZ CONSTRUCTION OF MISCELLANEOUS BUILDINGS` and
`S206 HOUSEKEEPING- GUARD`.

## Unchanged

Population, window, aggregation level, every threshold, G1, G3, G4's bar, G5's
thresholds, and the six declared limits.