# E030 — Amendment 3

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the harvest and the two arms and before any rate,
cluster or recurrence statistic was computed.** Nothing in this file moves B1,
B2, B3 or A4. It records two failed controls, two implementation defects that
changed the population, and two controls added because the declared ones did not
read the property the experiment needs.

## 1. The declared positive control A2 failed, and it is kept as failed

`raw/probes.jsonl` and the run log: **1 of 6** positive probes returned an account,
against a declared requirement of 5 of 6.

| probe | accounts |
|---|---|
| `looking for a replacement for Jira` | **1** |
| `we migrated from Jenkins to` | 0 |
| `switched from Sentry to` | 0 |
| `moved off from Heroku` | 0 |
| `alternatives to Firebase` | 0 |
| `what are you using instead of Salesforce` | 0 |
| all six nonsense probes | **0** (A3 passes) |

**Diagnosis, and it is about the control rather than the harvest.** Each probe is a
*phrase plus a named artifact*, and Algolia's phrase-exact match requires the two
to be **adjacent**. So a probe returns zero unless someone wrote exactly
`switched from Sentry to` after 2024-01-01. The harvest does not require
adjacency: it finds phrase-bearing comments and then resolves whatever artifact
name follows. **The control therefore measures the probe's adjacency requirement,
not the harvest's sensitivity**, and a control that is stricter than the treatment
fails in the same direction as a broken instrument — the two cannot be told apart
from the failure. That is a general defect in positive-control design and it is
recorded as such rather than as a passing control.

**A2 stands as declared and failed.** It is not re-scoped here. What follows adds
a control that reads the property, and A2's number is reported beside it.

## 2. Two implementation defects that changed the population

Both were found before any rate and both are conformance fixes, not tuning.

1. **`raw/harvest.jsonl` was rewritten per page.** The first version re-serialised
   the whole accumulated per-framing dict after every page, putting **7 828** rows
   on disk for **2 461** comments and duplicating each row once per page after the
   first. Re-run with an incremental write: **2 461 rows, 2 457 distinct comment
   ids**, and the 4 cross-framing duplicates are dropped by the dedupe ledger in
   `raw/extract_log.jsonl`. A count taken before this fix would have been 3.2× the
   population.
2. **The control arm was capped at the flat mean, not at the treatment share.**
   The protocol says *"story-stratified so no story contributes more than its
   treatment share"*. The implementation capped each story at the arm-wide mean
   (62), which is a different rule and a weaker confound control. Corrected to the
   declared rule: the control arm went from 2 884 to **2 687** accounts, with a
   per-story cap derived from each story's share of the treatment accounts in the
   sampled stories. The corrected caps are in `raw/extract_log.jsonl`.

## 3. Two controls added, and the order they run in

**A5 — do the artifact candidates name real artifacts?** *(reader-free)* This is
the property the recurrence rule rests on, because it requires two accounts to
name **different departing artifacts**. Sample **40** treatment artifact
candidates, seeded (`random.Random(3005)`), and resolve each against GitHub's
repository index (`q=<name> in:name`, `total_count`), with **12** nonsense names
as the known-absent control. **Gate: the resolution rate's CI95 lower bound
exceeds the nonsense rate's CI95 upper bound.** One-sided by construction: a tool
that is not on GitHub reads as unresolved (F041), so a low resolution rate cannot
be distinguished from a low true rate and the gate only requires resolution to be
materially above chance.

**A6 — are these accounts about leaving?** *(one reader)* Sample **24** treatment
and **24** control accounts, seeded (`random.Random(3006)`), blinded to arm, each
rendered with its text verbatim. Treatment rows are asked two binary questions
straight out of the protocol's population definition: **q1** does this comment
describe leaving, replacing or moving off a named tool, product or service; **q2**
does the declared artifact candidate name that tool, product or service. Control
rows are asked **q1** only. **Gate: the treatment q1 rate's CI95 lower bound is
≥ 0.60.** The control q1 rate is **reported and feeds no gate**, declared here:
these stories are departure-themed, so a high control rate is a fact about the
stories rather than a fault in the reader. Reader agreement is **not measured** —
one reader — so every A6 number is descriptive of a single pass and is labelled so
in `results.json`.

**Both A5 and A6 run before `recurrence.py`.** If A5 or A6 fails, the verdict is
`not_evaluated` and no rate is reported, which is the treatment A2's failure
should have had and did not.

## 4. What this does not change

- No B-gate threshold moves. `R_t − R_c` ≥ 0.10 with CI95 excluding 0, ≥ 3
  multi-artifact clusters to survive, overlap or < 2 clusters to kill.
- A4 is met by the corrected population: **919 treatment, 2 687 control**, against
  a floor of 300 each.
- The declared syntax test is left alone, including its known false positives. The
  artifact candidates include `I` (25), `C` (13), `US` (10) and `X` (5), which are
  capitalised words the declared rule admits and a reader would not. They are
  **not** filtered out: the protocol's limits section already promised to report
  the error rate rather than repair it by judgement. The noise is one-sided against
  the hypothesis, because the rule requires two accounts to name *different*
  artifacts and a shared junk candidate blocks recurrence rather than creating it.

## 5. Population after the corrections

| | treatment | control |
|---|---|---|
| accounts | **919** | **2 687** |
| distinct authors | 835 | 1 801 |
| author overlap | **0** | **0** |
| distinct departing artifacts | 599 | — |
| distinct stories | 824 | 55 |
| median words | 90 | 74 |

The control arm draws on 55 of the sampled stories and the treatment arm on 824,
because treatment accounts are spread thin and the control pool is drawn only from
the 60 stories sampled for it. **The two arms therefore do not have identical
story support**, and the story-title tokens removed by the signature rule are the
60 sampled stories' titles, not the 824. Recorded as a limit of the confound
control rather than repaired, because repairing it means matching each treatment
account's own story, which is the topic confound the arm exists to remove.
