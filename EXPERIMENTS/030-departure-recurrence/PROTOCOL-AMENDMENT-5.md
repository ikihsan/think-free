# E030 — Amendment 5

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the A8 labels were verified and before `recurrence.py`
was run.** Two things: how an `unclear` label scores, and the one asymmetry in
the declared recurrence rule between the arms.

## 1. `unclear` (`u`) is reported both ways, and the gate does not depend on it

`AMENDMENT-3` §3 declared the alphabet `1 / 0 / u` but not what `u` scores. That is
an omission and it is closed here. **Both handlings are computed and reported:**

- **primary:** `u` counts in the denominator as a no;
- **secondary:** `u` rows are dropped.

| arm | `u` = no | `u` excluded |
|---|---|---|
| A8 treatment q1 | 16 / 30 = 0.5333, CI95 **[0.3614, 0.6977]** | 16 / 25 = 0.6400, CI95 **[0.4452, 0.7975]** |
| A8 control q1 | 1 / 30 = 0.0333, CI95 [0.0059, **0.1667**] | 1 / 28 = 0.0357, CI95 [0.0063, **0.1771**] |

**A8 fires under both**, 0.3614 > 0.1667 and 0.4452 > 0.1771. The scoring rule is
therefore **not load-bearing**, and no choice between them is needed for the gate.
It is declared after the labels existed, which is why both are reported: a rule
picked after seeing the numbers can always be the convenient one, and the only
defence available is to show the answer does not turn on it.

## 2. A8, as run

Held-out sample, seed 3007, 30 + 30 rows, one reader, views frozen and hashed,
label files accepted by `verify_labels.py` against
`raw/view_digests_a8.json` (`b4f3fbe5…`, `c51c96d3…`).

**A8 fires.** The framing phrase selects a population of departure accounts that
ordinary comments on the same stories are not: treatment **0.53** against control
**0.03**, with non-overlapping intervals.

**`q2` on the A8 treatment rows: 13 of 16 = 0.812.** On the A6 rows it was 13 of
14. So across 40 departures the artifact candidate names the artifact the account
is about about **8 times in 10** — better than A6's whole-arm 0.542 suggested, and
still wrong often enough that the field's name overstates it. The systematic
failure in `AMENDMENT-4` §2 is real and its rate is now measured twice: **3 of 30
treatment rows name the replacement instead of the departure** (`T06` iPhone →
Pixel, `T13` 2020 model → M series, `T23` Claude → Kimi).

## 3. The one asymmetry in the declared recurrence rule, and it runs against H1

The declared rule requires two accounts to name **different departing artifacts**.
The control arm **has no artifact field at all** — its accounts were selected for
*not* containing a framing phrase, so nothing was resolved.

**Amendment.** The control arm's recurrence is computed **without** the
artifact-diversity condition. The consequence is stated because it decides how the
result may be read:

- the treatment arm's rule is **stricter** than the control arm's, so treatment `R`
  can only be **understated**;
- the control arm's rule is **weaker**, so control `R` can only be **overstated**.

**Both biases point away from H1.** The declared comparison is therefore the
conservative one, and a null under it is a null against a null that was handed the
advantage.

**A matched-rule comparison is also reported**, with the artifact-diversity
condition removed from the treatment arm so both arms use an identical rule. That
version answers the question H1 actually asks — *does the departure framing add
anything over ordinary comments on the same stories* — with no asymmetry at all,
and it is the number to read if the declared version is rejected.
