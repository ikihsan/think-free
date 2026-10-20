<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E134 AMENDMENT-2 — the key side, and a recomputation that is not circular

Written 2026-10-14 at 01:2x UTC, after `PROTOCOL.md` (`f187edb1`) and
`AMENDMENT-1.md` (`7a630ab3`), **after Arm A ran, and after reading the shape of
the bytes it emitted — but before any recomputation was executed and before any
recomputed rate was compared to any printed rate.** No `acc` column was summed,
no aggregate was opened for comparison, and no Arm B byte was fetched. The
disclosure below says exactly what had been read.

## Disclosure: what was read before this amendment

Read: the *structure* of the emitted files — the field names present, the types
of the values, the config block, and the source of `lm_eval/api/task.py`
(`doc_iterator`, `process_results`, `consolidate_results`),
`lm_eval/loggers/evaluation_tracker.py` (`save_results_samples`) and
`lm_eval/evaluator.py` around the `n-samples` block.

Not read before this amendment: any per-row `acc`/`acc_norm` value beyond the
two rows quoted in the session log for shape, no recomputed rate, no printed
rate side by side, no Arm B output.

The three gates G1–G5 are unchanged. This amendment adds two measurements, both
of which the structure forced.

## A1 — R1 must be recomputed from the inputs, not from the verdict column

A first reading of the emitted rows invites a cheap and worthless R1: average
the shipped `acc` column and compare it to the printed `acc`. That is not a
recomputation. The shipped `acc` **is** the verdict; averaging it recovers the
aggregate by construction, so the check can only ever confirm the harness's own
arithmetic and would pass on a run whose verdicts were all fabricated.

R1 is therefore defined as the stronger version:

> **R1.** Recompute the headline rate from the *inputs the run shipped*, using
> the metric definition the run itself declares in `results.json`
> (`configs[task].metric_list`, `output_type`), and compare it to both the
> printed rate and the shipped verdict column.

For `output_type: multiple_choice` those inputs are the shipped
`filtered_resps` loglikelihoods, the shipped `target`, and the shipped `doc`
(which carries the choice texts the `acc_norm` denominator is computed from).
This is a real recomputation: it never reads the `acc` column. It is also the
only version that can detect a *wrong verdict*, which is the class that matters.

Three outcomes are possible and all three are results:

| outcome | meaning |
|---|---|
| recomputed == printed == shipped verdict column | the run's plumbing is internally consistent on these rows |
| recomputed == printed, and both differ from the verdict column | the aggregate and the per-row verdicts disagree with each other; a defect in the run |
| recomputed differs from printed | the printed number does not describe the rows it shipped; the silent-drop shape |

## A2 — the key side cannot come from the emitted files, and C1 must say so

G2 requires the adapter to read the emitted files only. That is right for the
adapter and **it makes C1 vacuous on Arm A**, for a reason worth stating
precisely rather than hiding:

With `--log_samples`, lm-eval ships `doc_id`, `target` *and* the verdict in one
file. Both sides of a C1 join can therefore be built from the same bytes, they
will agree by construction, and the check reports a clean 1.0000 on any output
whatsoever. A check that cannot fail is not a check — the protocol's own Arm C
rationalum — so the vacuous variant is **run and recorded**, and the
load-bearing key side is declared separately:

> **The key side is the dataset the run itself names in its own
> `results.json`**, read from the same public, unauthenticated source the run
> downloaded, and mapped into lm-eval's identifier vocabulary by the same
> adapter that maps the output side. The question C1 then asks is the useful
> one: *do the identifiers and targets a run shipped actually name the rows of
> the dataset that run says it evaluated?*

This is a declared departure from G2's "emitted files only", and it costs one
dependency the rest of this repository does not take: reading the cached Arrow
datasets needs `pyarrow`, which is already installed as an lm-eval dependency.
The **adapter stays stdlib-only and emitted-files-only** so G2 is still measured
as declared; the dataset reader is a separate, named module and its cost is
reported alongside the adapter's.

## A3 — R3 gets a stated carve-out

`results.json` reports `acc_stderr` beside `acc`. A standard error is by
construction an aggregate-only quantity and has no per-row column in any harness.
R3 therefore tests every reported metric except keys ending `_stderr`, and R3
also reports the `_stderr` keys separately rather than silently dropping them.
The carve-out is stated here because writing it after seeing which keys existed
would be the same defect E113 found in the classifier.

## What is unchanged

G1–G5, the kill gate, the baselines, the declared ceilings, and the declared
failure condition: **if Arm A's run is clean under C1 and the recomputations
agree, `preflight` has no observed external value and the release question
closes.**
