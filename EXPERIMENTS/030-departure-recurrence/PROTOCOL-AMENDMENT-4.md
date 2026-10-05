# E030 — Amendment 4

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the A6 labels were verified and before any recurrence
statistic was computed.** It records a gate that failed, a systematic error the
labels exposed, and one held-out gate that replaces the unreachable one.

## 1. A6 failed as declared, and the gate was unreachable at its own sample size

The declared rule was *"the treatment q1 rate's CI95 lower bound is ≥ 0.60"*. The
measurement, from `raw/a6_labels_treatment.tsv` and `raw/a6_labels_control.tsv`
after `verify_labels.py` accepted both files against the frozen views:

| arm | q1 = yes | rate | CI95 |
|---|---|---|---|
| treatment | **14** / 24 | 0.5833 | **[0.3855, 0.7548]** |
| control | **0** / 24 | 0.0000 | [0.0000, 0.1411] |

CI95 lower bound **0.3855 < 0.60**. **A6 fails as declared.**

**The gate could not have been passed at n = 24.** A Wilson lower bound reaches
0.60 at n = 24 only at **p ≥ 0.8333** (n = 30 → 0.800, n = 40 → 0.775, n = 100 →
0.700; `test_gates.py` recomputes this table from the declared rule). So A6 does
not distinguish a good population rule from a bad one: it measures **its own
sample size** as much as the extraction, and no population rule short of 83%
precision could clear it. This is the mirror image of F010 — there a declared gate
could not fail; here one could hardly pass. Both are gates that report the gate
rather than the property, and the arithmetic is derivable from the protocol's own
numbers without running anything.

**A6's failure is recorded, not repaired by moving 0.60.**

## 2. The labels exposed a systematic error in the artifact extraction

`resolve_artifact` takes the **first name-like token after the framing phrase**.
The declared population note warned that the syntax test "misses lowercase brand
names". What the labels show is worse than a miss: when the departed artifact is
not name-shaped, the extractor **returns the replacement**.

| row | text | declared candidate | the departing artifact |
|---|---|---|---|
| **T04** | "I switched from **a typical keyboard** to a 75% **Keychron K2**" | `Keychron K2` | "a typical keyboard" — not name-shaped, skipped |

`q2` — *does the candidate name the artifact the account is about?* — is
**13 / 24 = 0.542**, and **13 / 14 among the rows q1 accepted**. Every one of the
14 failure rows is a real departure account whose candidate points at the wrong
side of the transition, or at a non-artifact. `T04` is the clean instance;
`Windows`, `US`, `I`, `C`, `OF`, `E` are the noise the declared rule admits and a
reader would not.

**Direction of the error, stated because it decides whether the rate can be read.**
Naming the replacement instead of the departure does **not** inflate recurrence: the
rule requires two accounts to name *different* artifacts, so a wrong-but-distinct
candidate still has to differ. It does mean **the "departing artifact" construct is
not what the field says**, and A5's 0.97 resolution rate is now known to measure
*"does this token name something that exists on GitHub"*, not *"does it name what
the author left"*.

## 3. A7, declared post hoc and therefore not usable on its own

The control arm's q1 rate is a base rate this experiment needed and the protocol
only reported. A **separation gate** — treatment q1 CI95 lower > control q1 CI95
upper — is the rule F023 and F043 each had to add after the fact. It is declared
here as **A7**, and it is labelled **post hoc**: both numbers were in hand before
this sentence was written, so A7 is recorded as a description of the A6 sample and
**cannot serve as the gate that decides the experiment.**

## 4. A8, the gate that decides, declared before the sample exists

Same rule as A7, on a **held-out** sample, run once.

- **Population:** 30 treatment accounts and 30 control accounts drawn with
  `random.Random(3007)` from the arms, **excluding every row already read in the
  A6 sample** (`raw/a6_key_rows.jsonl`), so the sample is untouched by anything
  declared in section 3.
- **Instrument:** one reader, the same two questions, views frozen and hashed, the
  label file checked by order and not by set (`verify_labels.py`). Reader
  agreement is **not measured** and both rates are labelled as one pass.
- **Gate A8 fires** if the treatment q1 CI95 lower bound **exceeds** the control q1
  CI95 upper bound. If A8 does not fire, the verdict is `not_evaluated` and no
  recurrence rate is reported, exactly as the protocol said for A6.

**Why A8 and not a repaired A6.** A separation gate asks whether the framing
selects a distinct population, which is the property H1's comparison needs; an
absolute-precision gate asks whether the population rule is clean, which H1 does
not need. The threshold is a relation between two measured quantities, not a number
chosen to sit on one side of a result.

## 5. What is declared here so the run cannot be read as convenient

- **Contamination is one-sided against H1.** At 41.7% non-departure content, the
  treatment arm's `R` is pulled toward the control arm's, so a null is
  conservative and a positive is if anything understated.
- **A descriptive dose-response check, feeding no gate.** Because the reader
  labels a sample rather than the arm, the treatment arm is additionally split by a
  **mechanical completed-first-person-departure test** — `(I|we|my|our)` within 120
  characters before a past-tense departure verb from the declared list, or a
  first-person subject directly before one. `R` is reported for that subset beside
  the whole arm, with the subset's precision estimated from the A6 and A8 labels.
  If `R` rises with the subset, the signal sits in the departures; if it does not,
  the framing phrase was carrying nothing. **Declared before it is computed and it
  gates nothing.**
- **No B-gate threshold moves**, and C1's pilot is unchanged.
- **Reader agreement stays unmeasured.** One reader is one pass; the record's last
  three reader arms each failed a κ floor, and this arm is labelled accordingly
  rather than given a floor it cannot be held to at n = 30.

## 6. Status at this amendment

| gate | declared rule | result |
|---|---|---|
| A1 fetch validity | ≥ 90% of ids return a body; ≥ 90% of pages fetched | **0 failed pages, 35 requests — passes** |
| A2 positive control | 5 of 6 planted probes return ≥ 1 account | **1 of 6 — fails** (diagnosed in AMENDMENT-3 §1) |
| A3 nonsense control | nonsense probes return 0 | **0 of 6 — passes** |
| A4 population | ≥ 300 accounts per arm | **919 / 2 687 — passes** |
| A5 register resolution | candidates' CI95 lower > nonsense' CI95 upper | **0.9706 [0.8508, 0.9948] vs 0 [0, 0.2775] — passes** |
| A6 absolute precision | treatment q1 CI95 lower ≥ 0.60 | **0.3855 — fails**, and unreachable at n = 24 |
| **A8 separation, held out** | treatment q1 CI95 lower > control q1 CI95 upper | *not yet run* |
