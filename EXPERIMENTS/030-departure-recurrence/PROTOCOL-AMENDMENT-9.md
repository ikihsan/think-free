# E030 — Amendment 9

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after `verify_labels.py` accepted both A8 label files, after
A9 ran, and after the length-matched subsample was computed.** It closes the
experiment's declared question.

## Gate results, complete

| gate | rule | result |
|---|---|---|
| A1 fetch validity | ≥ 90% ids body, ≥ 90% pages | **passes** (0 failed pages) |
| A2 positive control | 5 of 6 probes ≥ 1 account | **1 of 6 — fails** (AMENDMENT-3 §1) |
| A3 nonsense control | 0 accounts | **passes** (0 of 6) |
| A4 population | ≥ 300 / arm | **passes** (919 / 2687) |
| A5 register resolution | candidates > nonsense CI95 | **passes** (0.97 vs 0) |
| A6 absolute precision | treatment q1 lower ≥ 0.60 | **fails**, 0.3855 (unreachable at n=24) |
| **A8 separation, held out** | treatment q1 lower > control q1 upper | **fires**: 16/25 = 0.64, CI95 [0.4452, 0.7975] vs 1/28 = 0.0357, [0.0063, 0.1771] (`raw/a8_separation.json`) |
| A9 permutation null | treatment observed above its own null | **does not fire**: observed R_pair 0.3493 against a 50-permutation null of 0.2925 ± 0.012 (z = 4.72 but the declared interval rule refuses it; control arm 0.2155 vs 0.0496 ± 0.0044) |
| B1 (pair-level) | diff > 0.10, CI excludes 0 | fired at 0.1338 [0.0997, 0.1687] — **verdict withdrawn** by AMENDMENT-8 |
| length-matched diff | treatment − control at matched length | **−0.0735**, CI95 [−0.1176, −0.0290]: the sign flips, so the between-arm difference is length |

## The verdict

**H1: `not_evaluated`, third and final time.** A8 shows the framing selects a
distinct population (the population rule works), and A6's labels show that
population's q1 rate is 0.64 — but the statistic the protocol declared for H1
**does not read clause recurrence**: it reads coincidence between long comments
(AMENDMENT-8 §1), and its permutation null explains the arm difference
(A9 + the length account: medians 90 vs 74 words, the common-token cutoff at
2% of each arm's size, and a length-matched diff of −0.0735 with the sign
against the treatment arm). Both B verdicts are withdrawn; **C1's pilot is not
run, because its referent — clusters of clauses rather than clusters of
coincidences — was never established.** A2's failure stands as recorded: the
harvest instrument missed 5 of 6 planted probes on first attempt, so its
single-pass numbers carry that uncertainty.

## What survived

- The departure-framing **population** exists and differs from ordinary
  same-story comments (A8, one held-out read, one reader, agreement not
  measured): 64% vs 3.6% of rows name something a reader would call departure
  content, unanswered rows in both.
- The precise q1 number is **one reader's pass** (25 and 28 answered rows);
  no second reader exists, and the record's last three reader arms each failed
  a κ floor, so nothing stronger is claimed.
- The failure itself is the finding: a rare-shared-token recurrence statistic
  over long free-text comments **measures what the length distribution and the
  2% cutoff hand it.** The mutual groups it called "shared clauses" — firewall,
  mainframes, Ruby, Go — are ordinary English words of length ≥ 4 (full text in
  `raw/mutual_treatment.jsonl`). Any recurrence claim built on such a
  statistic needs A9's null wired in from the start, and its linking tokens
  printed, or it will fire on coincidence.
