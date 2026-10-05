<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E030 — do departure accounts supply a recurring unmet clause?

**Date:** 2026-10-05. Task T-0074. Protocol declared in
[`PROTOCOL.md`](PROTOCOL.md) before any fetch, amended nine times
([`1`](PROTOCOL-AMENDMENT-1.md), [`2`](PROTOCOL-AMENDMENT-2.md),
[`3`](PROTOCOL-AMENDMENT-3.md), [`4`](PROTOCOL-AMENDMENT-4.md),
[`5`](PROTOCOL-AMENDMENT-5.md), [`6`](PROTOCOL-AMENDMENT-6.md),
[`7`](PROTOCOL-AMENDMENT-7.md), [`8`](PROTOCOL-AMENDMENT-8.md),
[`9`](PROTOCOL-AMENDMENT-9.md)). Session
020 in this VM's `sessions/` tree.

## Verdict: H1 `not_evaluated` — the instrument, not the world, was measured

| gate | result |
|---|---|
| A1 fetch validity | passes |
| A2 positive control | **1 of 6 — fails** (diagnosed, AMENDMENT-3 §1) |
| A3 nonsense control | passes (0 of 6) |
| A4 population | passes (919 treatment / 2687 control) |
| A5 register resolution | passes (0.97 vs 0) |
| A6 absolute precision | **fails** — 0.3855 lower bound, unreachable at n=24 (F010's mirror) |
| A8 separation, held out | **fires** — 16/25 = 0.64 [0.445, 0.798] vs 1/28 = 0.036 [0.006, 0.177] |
| A9 permutation null | treatment does not clear its own null (0.3493 vs 0.2925 ± 0.012) |
| B1 pair-level difference | fired at 0.1338 — **verdict withdrawn** (AMENDMENT-8) |
| length-matched difference | **−0.0735**, CI95 [−0.1176, −0.0290] — sign against the treatment arm |

C1's pilot is **not run**: its referent (clusters of clauses) never survived
A9, and a gate deciding "whichever the numbers say" gets no numbers.

## What the run established

Two separable facts. **First**, the departure-framing population is real and
distinct from ordinary comments in the same stories — a held-out reader sample
puts 64% of its rows at departure content against 3.6% of controls. **Second**,
the clause-recurrence statistic declared for H1 does not read clauses: at ~8 500
rare tokens per long comment, sharing two with an unrelated comment is
expectable, and the arms differ because the treatment comments are longer
(median 90 vs 74 words) under a common-token cutoff proportional to each arm.
The mutual groups it produced are four unrelated comments about a firewall, a
mainframe, Ruby and Go linked through `abandon`, `absolute`, `allocation`,
`apis` ([`raw/mutual_treatment.jsonl`](raw/mutual_treatment.jsonl)). The
length-matched recomputation reverses the sign of the difference (−0.0735), so
the observed gap was length. **The corpus exists; the verdict on clause
recurrence is `not_evaluated`, and B1 never stands.**

## Three defects found by printing, all recorded

1. **The cluster printout is the falsifier** (AMENDMENT-8): printing the linking
   tokens showed ordinary English doing the linking. A9 is the same falsifier
   without a reader.
2. **A6 could not have passed**: at n = 24 a Wilson lower bound reaches 0.60
   only at p ≥ 0.8333 — the gate reported its own sample size (AMENDMENT-4).
3. **The extraction names the replacement, not the departure,** when the
   departed artifact is not name-shaped (`T04`: "switched from a typical
   keyboard to a 75% Keychron K2" extracts `Keychron K2`). q2 = 13/24, and
   A5's 0.97 now reads "names something on GitHub," not "names what the author
   left" (AMENDMENT-4 §2).

## What this changes

No candidate and no generator is revived. The need-corpus closure stands
(F033, F039, F042, F049), and E030's demand-side class — clauses stated by
someone who paid for leaving — produced **a real population and a falsified
ruler**, not a recurrence. If this population is ever re-read, the recurrence
claim must carry A9's null and printed linkage from the first line of its
protocol; the production token rule (rare-token pair sharing) is prior art as
an instrument of judgment only after that. Raw numbers:
[`raw/recurrence.json`](raw/recurrence.json),
[`raw/a9_permutation.json`](raw/a9_permutation.json),
[`raw/a8_separation.json`](raw/a8_separation.json),
[`raw/a8_labels_treatment.tsv`](raw/a8_labels_treatment.tsv),
[`raw/a8_labels_control.tsv`](raw/a8_labels_control.tsv),
[`PROTOCOL-AMENDMENT-9.md`](PROTOCOL-AMENDMENT-9.md).
Reproduce: `python3 recurrence.py`, `python3 permutation_control.py`,
`python3 a8_separation.py`, `python3 verify_labels.py treatment|control`
(label files checked in `raw/`).
