<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# E071 — Does the software arm's `view_count` zero exist, or is it a missing observation?

**Date:** 2026-10-09 · **Status:** complete — **the kill gate fired on both arms**

Declared before any result was read. This experiment exists to settle one
question that blocks landing four unlanded experiments (E067, E067b, E069 ×2)
and one record file (`MISSION-OUTCOME.json`).

## The question

E069 (`EXPERIMENTS/069-view-count-nonsoftware/EXPERIMENT-RESULT.json`)
reports as a **confirmed** finding:

> 100% of non-software need statements have `view_count` > 0, and 14% are
> labeled unserved-open-like. **This directly contradicts the E063/E066 finding
> of unserved-open = 0 in software corpora** ... `view_count` is **0% in
> software need corpora**.

That contrast is load-bearing. It is what "validated the instrument outside
software" (E069) and "the instrument's domain scope is not software-narrow"
(E069) rest on, and it is the stated `ground_truth_context` for E070.

**The denominator is the claim.** E069's software comparison is drawn from the
E063/E066 corpora — Hacker News rows and GitHub issues. Whether those two
platforms *expose* an arrival count at all is not the same question as whether
the count is zero, and the two are indistinguishable in E069's table because
the software cells are all zero.

Per **D082** (an arm that produced no observation is a missing observation,
never a zero and never a denominator) and the owner brief's rule that an
instrument must recover independent real positive examples, this experiment
measures the **field's existence on each platform**, not its value.

## Arms

| arm | platform | what is measured |
|---|---|---|
| A | Hacker News (Firebase API, `topstories` → 60 items) | does a returned item object carry an arrival/view field? |
| B | GitHub issues (REST `GET /repos/{o}/{r}/issues/{n}`) | does a returned issue object carry an arrival/view field? |
| C | Stack Exchange (`/2.3/questions`, the E062 route) | positive control: the field exists here, so "absent" in A/B is a platform property and not an API-shape artifact of this harness |

Arm C is the control that makes A and B interpretable. Without it, "the field
is absent" could mean "the harness strips fields".

## Gates (predeclared)

- **G1 (arm C control):** Stack Exchange items carry a non-absent
  `view_count` on ≥ 95% of sampled rows. **Fires → the harness can read the
  field when it exists.**
- **G2 (arm A):** HN items carry any arrival/view field on **0%** of sampled
  rows. **Fires → the software arm's zero is a missing observation, and E069's
  "diametrical contrast" is unsupported.**
- **G3 (arm B):** GitHub issue objects carry any arrival/view field on **0%**
  of sampled rows. **Fires → same conclusion, independently.**
- **Kill condition:** G1 met and (G2 or G3) met → E069's headline is a
  **platform-measurement artifact**, its "confirmed" verdict must be withdrawn,
  and `MISSION-OUTCOME.json`'s `vc_always_100_percent` /
  `instrument_validated_outside_software` claims cannot be recorded as
  observed. **Nothing is built; the four unlanded experiments land with the
  correction recorded, and the software-arm number is reported as missing
  rather than as 0.**

G2/G3 firing is **not** evidence that the instrument is invalid. It is evidence
that it was **never measured** on the software arm. The corrected statement is
narrower and survives: `view_count` exists and varies on Stack Exchange, and no
public API exposes an arrival count for HN comments or GitHub issues, so the
E062 instrument is **Stack-Exchange-shaped**, and every software-arm reading of
it in this record is a missing observation.

## Strongest objection, stated before running

*"Absence of a search hit is not originality" (AGENTS.md) — the same discipline
applies here: absence of a field in three API responses does not establish
absence in the API. A per-item page view may exist on the web UI or an
undocumented endpoint.*

**Answer:** the claim is scoped to the **public documented API response
objects**, because that is the only surface E063/E066 harvested from and the
only surface any reproduction of them can use. The experiment does not claim HN
and GitHub have no view counters anywhere; it claims the corpora carry no
arrival field, so the software-arm cell cannot be a measured zero. Recorded as a
ceiling, not a defeat.

## Reproduction

```bash
cd EXPERIMENTS/071-viewcount-denominator
python3 probe.py     # writes raw/probe.json, prints the gate table
python3 outcome.py   # re-derives results.json from raw/probe.json
```