<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E134 RESULT — preflight pointed at a real run of a foreign harness

`observed` 2026-10-14, Python 3.8.10, `instance-20260717-0947`, 2 CPUs, no GPU.
Raw: [`armA/`](armA/) (292 KiB, this experiment's own run), [`armB/`](armB/)
(third-party run), [`results_e134.json`](results_e134.json) (90 709 bytes),
[`run_e134.py`](run_e134.py), the install and run log in this session's
`commands.log`. Protocol order is commit order: `f187edb1` → `7a630ab3` →
`cad0a5d0` → `AMENDMENT-3.md`.

## The question, and the answer in one line

*May `preflight` report a rate for a run written by a harness nobody here wrote?*

**No — not yet, and not for the reason the tool's README gives.** The run is
clean, so the release question closes; but the same run found **two places
where `preflight` itself returns a pass while measuring nothing**, and both are
in the public front door.

## Gates

| gate | result | evidence |
|---|---|---|
| **G1** ≥5 rows with target and verdict | **PASS** | 15 rows, 5 per task; `openbookqa` and `piqa` carry `target`+`acc`+`acc_norm`, `wikitext` carries `target`+3 verdict columns |
| **G2** ≤60 stdlib lines adapt the real emitted format | **PASS** | **6** counted lines (`_identity` 1, `_verdict` 5), stdlib only, emitted-files-only, verified by AST line count over the function bodies |
| **G3** checks run on foreign data; R1 agrees or every disagreement hand-verified | **PASS** | 7 Arm A metrics and 2 Arm B metrics recomputed from shipped inputs; **zero disagreements**, so nothing needed hand-adjudication. A hand read of 5 Arm B rows is in [`handcheck.md`](handcheck.md) |
| **G4** both Arm C defects caught | **FAIL** | C-1 caught, loudly (`KeyError: 'doc_id'`, exit non-zero). C-2 caught by **no declared check**: R1 agrees, R2 agrees, R3-as-declared agrees. Only the check added after the fact (`R3_per_row_coverage`) fires |
| **G5** ≥1 third-party output reachable unauthenticated | **PARTIAL** | bytes obtained unauthenticated; the hosting repository could not be re-located by three independent routes (AMENDMENT-3) |

**Kill gate** (G5 fails → release condition not met): not met, by the PARTIAL
reading and by the declared failure condition below.

## The declared failure condition fired

`PROTOCOL.md` §"Declared failure condition for the whole line":

> If Arm A's run output is clean under C1 and R1 agrees with the printed rate,
> then `preflight` has **no observed external value**.

Arm A **is** clean under C1 (best rate 1.0000) and R1 **does** agree on every
metric. The condition fired as written. lm-evaluation-harness v0.4.4's plumbing
is internally consistent on the rows it shipped, and this repository has no
evidence that a real run of it is wrong.

## R1 — the recomputation, on both a local and a foreign run

R1 never reads the verdict column. For `wikitext` it **executes the run's own
shipped `process_results` source**, which lm-eval places in `results.json`; for
multiple-choice tasks it reimplements the documented `ConfigurableTask.process_results`
branch and cites it (`REIMPLEMENTED` in `recompute.py`).

| arm | task | metric | printed | recomputed | agrees |
|---|---|---|---|---|---|
| A | openbookqa | acc / acc_norm | 0.2 / 0.2 | 0.2 / 0.2 | yes |
| A | piqa | acc / acc_norm | 0.6 / 0.8 | 0.6 / 0.8 | yes |
| A | wikitext | bits_per_byte | 5.2851537684272105e-05 | 5.2851537684272105e-05 | yes |
| A | wikitext | byte_perplexity | 1.0000366345653635 | 1.0000366345653635 | yes |
| A | wikitext | word_perplexity | 1.0001875813623529 | 1.0001875813623529 | yes |
| B | SGXSTest (200 rows) | acc | 0.515 | 0.515 | yes |
| B | SGXSTest (200 rows) | acc_norm | 0.5 | 0.5 | yes |

**R2**: `n-samples.effective` equals rows shipped on all three Arm A tasks
(5 = 5) and on Arm B's `SGXSTest` (200 = 200).

**R3**: every reported metric has a per-row column behind it, on every task of
both arms, with the `_stderr` carve-out AMENDMENT-2 §A3 declared in advance
(`bits_per_byte_stderr,none`, `byte_perplexity_stderr,none`,
`word_perplexity_stderr,none` — reported separately, not dropped).

## Two facts a third party cannot get from `results/` alone

Both are properties of a *well-behaved* run, and both block independent
verification without reading the harness's source.

1. **The run does not record which split it evaluated.** `results.json` names
   all declared splits and records the row count of the one it chose, but no
   field saying which. On `piqa` (`n-samples.original` 1838) and `wikitext` (62)
   the count matches exactly one declared split. On **`openbookqa` it matches
   two** — `validation` and `test` both hold 500 — so `dataset_key.resolve_split`
   returns `AMBIGUOUS` and builds **zero** key rows. 1 of 3 tasks, chosen before
   any check ran: `resolve_split` returns candidates, never a choice.
2. **Three of seven reported metrics declare no aggregation.** `wikitext`'s
   `metric_list` entries are `{'metric': name}` with no `aggregation` and no
   `higher_is_better`; the harness logs a warning and defaults them. The
   per-row values are there and the run's own `process_results` is shipped as
   source, so the numbers *are* recomputable — but only by reading code the
   publisher shipped by accident, not by reading the file the numbers live in.

## What `preflight` found in itself — the two vacuous passes

Neither was found by reading the code. Both were found by pointing the committed
package at foreign bytes.

**Finding 1 — C1 returns `OK` on an empty key side.** On Arm A's `openbookqa`
the key side could not be built (Finding 1 above). `preflight.concordance`
returned `verdict: OK`, `best_rate: 0.0`, `key_rows: 0`, `output_rows: 5`. The
`SILENT_NO_MATCH` branch is guarded on `key_rows_n and out_rows_n`, so with no
key rows at all the function falls through to the default `OK`. A tool whose
purpose is to refuse to report a rate against a check that saw nothing reported
one against a check that saw nothing.

**Finding 2 — C2 returns `OK` on a flagger that flags nothing.** On Arm B,
200 rows were labelled correct by recomputation from `filtered_resps`, `target`
and `doc_to_choice` — an independent label, not the shipped `acc`. **Zero** rows
were labelled incorrect. The margin-abstention flagger at `tau = 0` flags
nothing: `verdict: OK`, Wilson lower bound `0.0000`, `recall_on_incorrect: None`.
`alternate_form_fp` guards an empty *correct* arm (`NO_LABELLED_CORRECT_ITEMS`)
and has no guard at all for an empty *incorrect* arm. On a real published run,
C2 can only ever measure false positives, and a flagger that abstains
everywhere scores a perfect pass.

This is F118's rule reaching a second population: *a control must include the
case where the subject is wrong.* A verifier's positive arm is the arm the data
cannot supply, so a verifier with no positive arm cannot fail. D109 already
recorded that a false-positive rate belongs to an arm; this is the same fact
about the **absence** of an arm.

The C2 sweep, for scale, on Arm B (200 rows):

| tau (nats) | correct rows flagged | Wilson LB | verdict |
|---|---|---|---|
| 0.00 | 0 / 200 | 0.0000 | OK (flags nothing) |
| 0.05 | 1 / 200 | 0.0009 | OK |
| 0.10 | 2 / 200 | 0.0027 | OK |
| 0.25 | 4 / 200 | 0.0078 | OK |
| 0.50 | 10 / 200 | 0.0274 | ALTERNATE_FORM_FP |
| 1.00 | 35 / 200 | 0.1286 | ALTERNATE_FORM_FP |

## Baseline 1 — lm-eval's own checks

The incumbent is free and always available, and the protocol requires preflight
to add nothing over it. Read from the committed run's own `results.json` and
from `lm_eval/api/task.py`: lm-eval **emits** the aggregate, per-row samples,
`task_hashes`, and per-row `doc_hash` / `prompt_hash` / `target_hash`; and it
**verifies** that its own printed table matches its own rows, which is
arithmetic. It does not recompute a verdict from the model's responses and the
gold label, does not record the split, does not check that every shipped row
carries the verdict it reports, and does not compare against the dataset the run
names. On this run that difference cost nothing — the run is clean.

## C3 on foreign data

**NOT_COMPUTABLE**, stated rather than substituted. C3 asks whether a declared
negative arm is negative by evidence the key does not use. A single-model run of
three public datasets has no negative arm, and a published single-model run has
none either. Nothing was put in its place.

## What this does not show

- That any other harness has a defect. One clean run on one harness, one version,
  one invocation shape, `--model dummy` for Arm A.
- Anything about scoring *quality* or any model's behaviour. Arm A's model
  returns random responses by construction; the wikitext perplexities below 1.0
  are that, not a finding.
- Any prevalence claim. Arm B is one run of one model, and 69 of its 70 tasks
  ship no per-row file, so R1 covers 200 of 11 000+ scored rows. The recomputation
  is a per-task check and was not run across the run.
- That C2 or C3 transfer. Both need an arm a third party does not publish; C2's
  transfer was measured here and the empty-arm result is the answer.

## Decision (D110)

`preflight` is **not released** and the release question **closes on this
evidence**. The declared failure condition fired: the tool has no observed
external value against a real run of the harness behind most published LLM
numbers. The two vacuous passes are repaired in `preflight/` with regression
tests, because `RELEASE-MANIFEST.md` declares that package public and a public
check that passes while measuring nothing is the harm the package exists to
prevent. That repair is a defect fix, not a re-litigation of the release.

The most useful next action is not another harness sweep. It is: does the same
six-line adapter and the same R1 reach the format a **leaderboard** publishes,
where the number is read by people who never open `results.json`.
