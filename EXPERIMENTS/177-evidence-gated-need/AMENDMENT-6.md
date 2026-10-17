<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 AMENDMENT 6 — the Fisher tail was summing ratios, and no declared control could have caught it

**Declared after the first run of `score.py` printed `p = 1.000000`.**

The gap it printed was `+0.4667` — 26 of 30 against 12 of 30. The p-value was
1.0. The cause: `fisher_2x2` computed, for each admissible table, the **ratio**
of that table's probability to the observed table's, then summed the ratios. The
observed table's own probability is a constant factor and dropping it makes the
sum meaningless. The corrected version keeps it and sums the probabilities of
every table at most as probable as the observed one.

**Verified against five tables before the number was used**, because a test that
has just been wrong should not be trusted on the one table it is about:

| table | this implementation | reference |
|---|---|---|
| `[[1,9],[11,3]]` (Fisher & Yates tea-tasting) | 0.0027594 | 0.0027594 (`scipy.stats.fisher_exact`, two-sided) |
| `[[3,1],[1,3]]` | 0.4857143 | 0.4857143 |
| `[[5,0],[0,5]]` | 0.0079365 | 0.0079365 |
| `[[0,10],[0,10]]` | 1.0 | 1.0 |
| `[[26,4],[12,18]]` — E177's own | **0.00036818** | — |

Note on convention: two-sided Fisher has two conventions, the probability-based
one used here and the doubled one-sided one. The doubled convention gives
0.005518 on the tea-tasting table and would give **0.000736** here. **Either
convention clears the declared bar of p < 0.05**, so the choice is recorded and
not argued.

## The part that matters more than the bug

**Every declared control in this experiment passed while the p-value was wrong
by a factor of 2,700.** G0a, G0b, G0c and G0d all passed on the same run that
printed `p = 1.0`. That is the finding, and it is not about Fisher.

This protocol's controls are all controls **on readers** — that the treatment is
an assistant and not a refuser, that the scorer recovers real positives and
rejects real negatives, that the arms do not overlap. **Not one of them is a
control on the arithmetic that turns verdicts into a number.** A gate can be
green across every reader check and still emit a significance figure that is
meaningless.

This is the third time in this record that a hand-written tail has been the
thing that was wrong (E091/F114 found the Fisher tail summing from the wrong
term, against a true 0.0307 where a fabricated 0.00135 was reported). The
first was found by checking the tail against the data. This one was found by
not believing a gap of 0.47 and p = 1.0 in the same row of output.

**Change of standard, adopted here and written into `docs/policy/gate-falsification.md`
as a candidate:** any test this repository writes by hand must be checked
against a table with a published value before its output is reported, and that
check is committed beside the result. A test that fails safe — a broken tail
here returns 1.0, which would have declared a positive result false — is still a
broken test, and no control in this experiment was watching it.