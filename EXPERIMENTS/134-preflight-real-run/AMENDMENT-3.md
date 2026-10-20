<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E134 AMENDMENT-3 — one check added after the falsification arm fired

Written 2026-10-14 at ~01:5x UTC, after `PROTOCOL.md` (`f187edb1`),
`AMENDMENT-1.md` (`7a630ab3`) and `AMENDMENT-2.md` (`cad0a5d0`), and after
`run_e134.py` was executed once and produced `results_e134.json`.

## Disclosure: what was read before this amendment

Read: `results_e134.json` in full, including the Arm C-2 arm. The defect
injection itself is deterministic and declared in `PROTOCOL.md`; what the first
run added was the **observation that no declared check fired on it**.

Not changed: G1–G5, the kill gate, the baselines, the declared ceilings, and the
declared failure condition. R1, R2 and R3 keep the definitions AMENDMENT-1 and
AMENDMENT-2 gave them, including R3's `any()`-row semantics.

## What fired, and what it costs to admit

Arm C's second defect — a verdict column dropped from the final shipped row of
`openbookqa` — produced:

- R1: **agrees**. The printed rate does describe all five rows; R1 recomputes
  from `filtered_resps` and never reads the verdict column, so a dropped verdict
  is invisible to it *by construction*. This is R1 working as declared, not a miss.
- R2: **agrees**. `n-samples.effective` is 5 and 5 rows shipped. The row is
  still there; only its label is gone.
- R3 as declared: **agrees**. AMENDMENT-1 defined R3 as *does every reported
  metric have a per-row column behind it*, and the implementation asks `any()`.
  One dropped cell out of five is still "a per-row column behind it".

So the declared falsification arm did not fire. Rather than redefine R3 and
report the repaired version as though it had been declared, both are reported:

| check | as declared | added here |
|---|---|---|
| R3 | does **any** shipped row carry the metric column | does **every** shipped row carry it |

The added form is named `R3_per_row_coverage` in `results_e134.json`. On Arm A
and Arm B it is clean, so it changes no pass. On Arm C-2 it reports
`PARTIAL_COLUMN` with `rows_missing_the_column = 1`.

**Cost of the addition, stated plainly.** A check written after seeing which
defects it catches is the E113 classifier defect in a different costume. The
mitigation here is that the addition is reported *beside* the declared check and
does not replace it, and the defect it catches was declared in the protocol
before the run. G4 is scored against the **declared** R3, and it fails.

## A second disclosure: two checks returned a pass while measuring nothing

Both were found by running the committed `preflight` package on foreign bytes,
not by reading it. Neither is repaired inside this experiment; both are recorded
in `RESULT.md` as findings and repaired in `preflight/` with regression tests,
because that package is declared public in `RELEASE-MANIFEST.md`.

- C1 returned `OK` with `best_rate 0.0` and **zero key rows** on Arm A's
  `openbookqa`, because the run's own bytes do not say which split it evaluated
  and two of the three declared splits hold 500 rows.
- C2 returned `OK` with a Wilson lower bound of `0.0000` on a flagger that
  flagged **nothing at all**, on 200 labelled-correct rows and an empty
  incorrect arm.

## G5 provenance, corrected

`PROTOCOL.md` set G5 as *≥1 Arm B output published by a party other than
EleutherAI is reachable without authentication*. The bytes were obtained without
authentication. Three independent routes could not re-locate the hosting
repository afterwards: `princeton-nlp/HarnessBench` and four other spellings
return 404 from the GitHub API, `princeton-nlp` lists 83 repositories with no
such name, and the `JailbreakBench` organisation's three repositories do not
contain the file. G5 is therefore scored **PARTIAL** and the file's internal
provenance is recorded instead: lm-eval `git_hash 2389abfa`,
`allenai/llama-3-tulu-2-dpo-8b`, `model_sha 25be07dd…`, 70 tasks, 28672.9 s on
`cuda:0`, run date 2024-11-22.
